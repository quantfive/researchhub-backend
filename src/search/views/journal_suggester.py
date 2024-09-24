from django_elasticsearch_dsl_drf.filter_backends import (
    OrderingFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import SF, FunctionScore, Q

from search.backends.multi_match_filter import MultiMatchSearchFilterBackend
from search.documents.journal import JournalDocument
from search.serializers.hub import HubDocumentSerializer
from utils.permissions import ReadOnly


class JournalSuggesterDocumentView(DocumentViewSet):
    document = JournalDocument
    permission_classes = [ReadOnly]
    serializer_class = HubDocumentSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = "id"
    filter_backends = [
        MultiMatchSearchFilterBackend,
        SuggesterFilterBackend,
        OrderingFilterBackend,
    ]

    ordering = ("-paper_count",)
    ordering_fields = {"id": "id", "name": "name", "paper_count": "paper_count"}
    filter_fields = {
        "name": {"field": "name", "lookups": ["match"]},
    }
    multi_match_search_fields = {
        "name": {"field": "name", "boost": 1},
    }
    suggester_fields = {
        "name_suggest": {
            "field": "name_suggest",
            "suggesters": ["completion"],
            "options": {
                "size": 25,
            },
        },
    }
