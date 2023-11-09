import re
import logging
from collections import Counter
from urllib.parse import urlparse

import cloudscraper
from boto3 import session
from bs4 import BeautifulSoup
from django.db import transaction
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from analytics.amplitude import track_event
from citation.constants import CITATION_TYPE_FIELDS, JOURNAL_ARTICLE
from citation.filters import CitationEntryFilter
from citation.models import CitationEntry, CitationProject
from citation.permissions import (
    PDFUploadsS3CallBack,
    UserBelongsToOrganization,
    UserCanViewCitation,
)
from citation.schema import generate_json_for_rh_paper, generate_schema_for_citation
from citation.serializers import CitationEntrySerializer
<<<<<<< HEAD
from citation.tasks import add_pdf_to_citation, handle_creating_citation_entry
from citation.utils import get_paper_by_doi, get_paper_by_url
=======
from citation.tasks import handle_creating_citation_entry
from citation.utils import get_paper_by_doi, get_paper_by_url, create_citation_entry_from_bibtex_entry_if_not_exists
>>>>>>> 2a1feafd (Implement BibTeX (.bib) Library Upload in Reference Manager)
from paper.exceptions import DOINotFoundError
from paper.models import Paper
from paper.serializers import PaperCitationSerializer
from paper.utils import DOI_REGEX, clean_dois
from researchhub.pagination import FasterDjangoPaginator
from researchhub.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)
from utils.openalex import OpenAlex
from utils.parsers import clean_filename
from utils.sentry import log_error
<<<<<<< HEAD
from utils.throttles import THROTTLE_CLASSES
=======
from utils.bibtex import BibTeXParser
>>>>>>> 2a1feafd (Implement BibTeX (.bib) Library Upload in Reference Manager)


class CitationEntryPagination(PageNumberPagination):
    django_paginator_class = FasterDjangoPaginator
    page_size_query_param = "page_size"
    max_page_size = 10000
    page_size = 1000


class CitationEntryViewSet(ModelViewSet):
    queryset = CitationEntry.objects.all()
    filter_class = CitationEntryFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    permission_classes = [
        IsAuthenticated,
        UserCanViewCitation,
        UserBelongsToOrganization,
    ]
    serializer_class = CitationEntrySerializer
    pagination_class = CitationEntryPagination
    throttle_classes = THROTTLE_CLASSES
    ordering = ("-updated_date", "-created_date")
    ordering_fields = ("updated_date", "created_date")

    def list(self, request):
        return Response(
            "Method not allowed. Use user_citations instead",
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @track_event
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def upload_pdfs(self, request):
        data = request.data
        organization_id = data.get("organization_id")
        project_id = data.get("project_id")
        filename = data.get("filename")
        project = CitationProject.objects.get(id=project_id)
        can_upload = (
            project.status == "full_access" or project.created_by == request.user
        )

        if not can_upload:
            return Response(status=403)

        cleaned_filename = clean_filename(f"{get_random_string(8)}_{filename}")
        user_key = f"user_{request.user.id}"
        boto3_session = session.Session()
        s3_client = boto3_session.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        ascii_cleaned_filename = filename.encode("ascii", "ignore").decode()

        res = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": AWS_STORAGE_BUCKET_NAME,
                "Key": f"uploads/citation_pdfs/{user_key}_{cleaned_filename}",
                "ContentType": "application/pdf",
                "Metadata": {
                    "x-amz-meta-created-by-id": f"{request.user.id}",
                    "x-amz-meta-organization-id": f"{organization_id}",
                    "x-amz-meta-project-id": f"{project_id}",
                    "x-amz-meta-file-name": ascii_cleaned_filename,
                },
            },
            ExpiresIn=60 * 2,
        )
        return Response(res, status=200)

    @track_event
    @action(detail=False, methods=["post"], permission_classes=[PDFUploadsS3CallBack])
    def upload_pdfs_callback(self, request):
        data = request.data
        path = data.get("path")
        filename = data.get("filename")
        organization_id = data.get("organization_id")
        project_id = data.get("project_id")
        creator_id = data.get("creator_id")

        # Temporary condition to use Grobid or pdf2doi
        use_grobid = data.get("use_grobid", "False") == "True"

        if project_id == "None" or project_id is None:
            project_id = None

        handle_creating_citation_entry(
            path,
            filename,
            creator_id,
            organization_id,
            project_id,
            use_grobid,
        )
        return Response(status=200)

    @action(detail=True, methods=["post"])
    def add_paper_as_citation(self, request, pk):
        user = request.user

        with transaction.atomic():
            organization = getattr(request, "organization", None) or user.organization
            project_id = request.data.get("project_id", None)
            paper = Paper.objects.get(id=pk)
            json = generate_json_for_rh_paper(paper)

            citation_entry_data = {
                "citation_type": JOURNAL_ARTICLE,
                "fields": json,
                "created_by": user.id,
                "organization": organization.id,
                "doi": paper.doi,
                "related_unified_doc": paper.unified_document.id,
                "project": project_id,
            }
            request._mutable = True
            request._full_data = citation_entry_data
            request._mutable = False
            res = super().create(request)

            if file := paper.file:
                add_pdf_to_citation.apply_async(
                    (res.data["id"], file.name), countdown=3, priority=6
                )
            return res

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated, UserBelongsToOrganization],
    )
    def check_paper_in_reference_manager(self, request, pk=None):
        user = request.user
        project_ids = request.query_params.get("project_ids", None)
        organization = getattr(request, "organization", None) or user.organization
        organization_references = organization.created_citations

        if not project_ids:
            project_ids = [None]
        else:
            project_ids = list(map(int, project_ids.split(",")))

        def _check_if_citation_exists(project_id):
            return organization_references.filter(
                related_unified_doc=pk, project=project_id
            ).values_list("id", flat=True)

        res = dict(zip(project_ids, map(_check_if_citation_exists, project_ids)))
        return Response(res, status=200)
    
    
    @track_event
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def upload_library(self, request):
        """
        Upload and process bulk library imports.
        Currently only supports .bib files.
        """
        data = request.data
        file_type = data.get('type')
        organization_id = data.get("organization_id")
        project_id = data.get("project_id")
        creator_id = data.get("creator_id")
        if not file_type:
            # assume it's bib for now
            file_type = 'bibtex'

        if file_type != 'bibtex':
            return Response({'error': 'Invalid file type specified. Only "bibtex" is allowed.'}, status=400)

        if not request.FILES:
            return Response({'error': 'No files provided.'}, status=400)

        files = request.FILES.getlist('file')
        bibtex_entries = []

        # Parse and decode all files (just .bib for now)
        for uploaded_file in files:
            # Check the file extension
            file_name = uploaded_file.name
            if not file_name.endswith('.bib'):
                # ignore non-bib files
                logging.warning(f'Ignoring file type in reference library import: {file_name}')

            try:
                # `uploaded_file` is in binary format, so we need to decode it
                contents = uploaded_file.read().decode('utf-8')
                entries = BibTeXParser.parse_bibtext_as_string(contents)
                bibtex_entries.extend(entries)
            except Exception as e:
                log_error(e)
                return Response({'error': f'Error parsing file: {file_name}'}, status=400)

        # Create citation entries for each of the parsed entries
        created_entries = []
        errors = []
        for entry in bibtex_entries:
            e, already_exists, error_message = create_citation_entry_from_bibtex_entry_if_not_exists(
                bibtex_entry=entry,
                user_id=creator_id,
                organization_id=organization_id,
                project_id=project_id,
            )
            if not already_exists:
                created_entries.append(e)

            if error_message:
                errors.append({
                    'citation_id': e.id,
                    'error': error_message,
                })

        citations = self.get_serializer(created_entries, many=True).data

        return Response({
            'citations': citations,
            'errors': errors,
        }, status=200)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user_citations(self, request):
        citations_query = self.filter_queryset(self.get_queryset().none()).order_by(
            *self.ordering
        )

        # page = self.paginate_queryset(qs)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(citations_query, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def get_schema_for_citation(self, request):
        query_params = request.query_params
        citation_type = query_params.get("citation_type", None)
        if citation_type not in CITATION_TYPE_FIELDS:
            return Response(
                {"error": "Provided citation type does not exist"}, status=400
            )
        schema = generate_schema_for_citation(citation_type)
        return Response(schema)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def get_citation_types(self, request):
        citation_types = CITATION_TYPE_FIELDS.keys()
        return Response(citation_types)

    @track_event
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def doi_search(self, request):
        doi_string = request.query_params.get("doi", None)
        if doi_string is None:
            return Response(status=404)
        try:
            paper = get_paper_by_doi(doi_string)
            result = PaperCitationSerializer(paper).data
        except Paper.DoesNotExist:
            open_alex = OpenAlex()
            open_alex_json = open_alex.get_data_from_doi(doi_string)
            result = open_alex.map_to_csl_format(open_alex_json)
        return Response(result, status=200)

    @track_event
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def url_search(self, request):
        url_string = request.query_params.get("url", None)
        if url_string is None:
            return Response(status=404)

        try:
            paper = get_paper_by_url(url_string)
            result = PaperCitationSerializer(paper).data
            return Response(result, status=200)
        except Paper.DoesNotExist:
            scraper_result = cloudscraper.create_scraper().get(url_string, timeout=5)
            status_code = scraper_result.status_code
            dois = []

            if status_code >= 200 and status_code < 400:
                content = BeautifulSoup(scraper_result.content, "lxml")
                dois = re.findall(DOI_REGEX, str(content))
                parsed_url = urlparse(url_string)
                cleaned_dois = clean_dois(parsed_url, list(map(str.strip, dois)))
                doi_counter = Counter(cleaned_dois)
                formatted_dois = [doi for doi, _ in doi_counter.most_common(1)]

                if len(formatted_dois) == 0:
                    raise DOINotFoundError()

                # Using first most common doi
                doi = formatted_dois[0]
                try:
                    paper = get_paper_by_doi(doi)
                    result = PaperCitationSerializer(paper).data
                except Paper.DoesNotExist:
                    open_alex = OpenAlex()
                    open_alex_json = open_alex.get_data_from_doi(doi)
                    result = open_alex.map_to_csl_format(open_alex_json)

                return Response(result, status=200)
            return Response({"result": "DOI / URL not found"}, status=400)
        except Exception as e:
            log_error(e)
            return Response({"result": "DOI / URL not found"}, status=400)

    @track_event
    @action(
        detail=False,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated, UserBelongsToOrganization],
    )
    def remove(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                target_citation_ids = request.data.get("citation_entry_ids", [])
                current_user = request.user
                for citation_id in target_citation_ids:
                    target_ref = self.get_queryset().filter(id=citation_id)
                    if target_ref.exists():
                        target_ref = target_ref.first()
                        if target_ref.is_user_allowed_to_edit(current_user):
                            target_ref.delete()
                        else:
                            return Response(status=403)
                return Response(target_citation_ids, status=status.HTTP_200_OK)

            except Exception as error:
                print(error)
                log_error(error)
                return Response(status=status.HTTP_400_BAD_REQUEST)
