"""
Standard feed view for ResearchHub.
"""

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import Subquery
from rest_framework import status
from rest_framework.response import Response

from feed.views.base_feed_view import BaseFeedView
from hub.models import Hub

from ..models import FeedEntryLatest, FeedEntryPopular
from ..serializers import FeedEntrySerializer
from .common import FeedPagination


class FeedViewSet(BaseFeedView):
    """
    ViewSet for accessing the main feed of ResearchHub activities.
    Supports filtering by hub, following status, and sorting by popularity.
    """

    serializer_class = FeedEntrySerializer
    permission_classes = []
    pagination_class = FeedPagination
    cache_enabled = settings.TESTING or settings.CLOUD

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.get_common_serializer_context())
        return context

    def list(self, request, *args, **kwargs):
        page = request.query_params.get("page", "1")
        page_num = int(page)
        cache_key = self.get_cache_key(request)

        disable_cache_token = request.query_params.get("disable_cache")
        force_disable_cache = disable_cache_token == settings.HEALTH_CHECK_TOKEN
        use_cache = not force_disable_cache and self.cache_enabled and page_num < 4

        if use_cache:
            # try to get cached response
            cached_response = cache.get(cache_key)
            if cached_response:
                if request.user.is_authenticated:
                    self.add_user_votes_to_response(request.user, cached_response)
                response = Response(cached_response)
                response["RH-Cache"] = "hit" + (
                    " (auth)" if request.user.is_authenticated else ""
                )
                return response

        response = super().list(request, *args, **kwargs)

        if use_cache:
            # cache response
            cache.set(cache_key, response.data, timeout=self.DEFAULT_CACHE_TIMEOUT)

        if request.user.is_authenticated:
            self.add_user_votes_to_response(request.user, response.data)

        response["RH-Cache"] = "miss" + (
            " (auth)" if request.user.is_authenticated else ""
        )
        return response

    def get_queryset(self):
        """
        Filter feed entries based on the feed view ('following' or 'latest')
        and additional filters. For 'following' view, show items related to what
        user follows. For 'latest' view, show all items. Ensure that the result
        contains only the most recent entry per (content_type, object_id),
        ordered globally by the most recent action_date.
        """
        feed_view = self.request.query_params.get("feed_view", "latest")
        hub_slug = self.request.query_params.get("hub_slug")
        source = self.request.query_params.get("source", "all")

        if feed_view == "popular":
            queryset = FeedEntryPopular.objects.all()
        else:
            queryset = FeedEntryLatest.objects.all()

        queryset = queryset.select_related(
            "content_type",
            "parent_content_type",
            "user",
            "user__author_profile",
        )

        # Apply source filter
        # If source is 'researchhub', then only show items that are related to
        # ResearchHub content. Since we don't have a dedicated field for this,
        # a simplified heuristic is to filter out papers (papers are ingested via
        # OpenAlex and do not originate on ResearchHub).
        if source == "researchhub":
            queryset = queryset.exclude(content_type=self._paper_content_type)

        # Apply following filter if feed_view is 'following' and user is authenticated
        if feed_view == "following" and self.request.user.is_authenticated:
            following = self.request.user.following.all()
            if following.exists():
                queryset = queryset.filter(
                    parent_content_type_id__in=following.values("content_type"),
                    parent_object_id__in=following.values("object_id"),
                )

        if feed_view == "popular":
            # Only show paper and post
            queryset = queryset.filter(
                content_type__in=[
                    self._paper_content_type,
                    self._post_content_type,
                ]
            )
            if hub_slug:
                try:
                    hub = Hub.objects.get(slug=hub_slug)
                except Hub.DoesNotExist:
                    return Response(
                        {"error": "Hub not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                queryset = queryset.filter(
                    parent_content_type=self._hub_content_type, parent_object_id=hub.id
                )

            # Since there can be multiple feed entries per unified document,
            # we need to select the most recent entry for each document
            # Get the IDs of the most recent feed entry for each unified document
            latest_entries_subquery = (
                queryset.values("unified_document")
                .annotate(latest_id=models.Max("id"))
                .values_list("latest_id", flat=True)
            )

            # No need to order by hotscore descending since the view is already sorted
            queryset = queryset.filter(id__in=Subquery(latest_entries_subquery))

            return queryset

        # Latest / Following

        # For other feed views (latest, following with hub filter)
        # Apply hub filter if hub_id is provided
        if hub_slug:
            try:
                hub = Hub.objects.get(slug=hub_slug)
            except Hub.DoesNotExist:
                return Response(
                    {"error": "Hub not found"}, status=status.HTTP_404_NOT_FOUND
                )

            queryset = queryset.filter(
                parent_content_type=self._hub_content_type, parent_object_id=hub.id
            )

        return queryset
