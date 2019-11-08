from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from researchhub.settings import (
    ELASTICSEARCH_AUTO_REINDEX_IN_DEVELOPMENT,
    TESTING
)
from user.models import University


@registry.register_document
class UniversityDocument(Document):

    class Index:
        name = 'university'

    class Django:
        model = University
        fields = [
            'id',
            'name',
            'country',
            'state',
            'city',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted (defaults to False):
        ignore_signals = (TESTING is True) or (
            ELASTICSEARCH_AUTO_REINDEX_IN_DEVELOPMENT is False
        )

        # Don't perform an index refresh after every update (False overrides
        # global setting of True):
        auto_refresh = (TESTING is False) or (
            ELASTICSEARCH_AUTO_REINDEX_IN_DEVELOPMENT is True
        )
