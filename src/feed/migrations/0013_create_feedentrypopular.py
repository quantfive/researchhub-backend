# Manually created

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0012_feedentry_metrics"),
    ]

    def get_sql():
        # Limit data to the last 30 days in production
        limit_data = (
            "AND fe.created_date >= (NOW() - INTERVAL '30 days')"
            if settings.PRODUCTION
            else ""
        )

        sql = f"""
                CREATE MATERIALIZED VIEW feed_feedentry_popular AS
                SELECT
                    fe.id,
                    fe.content_type_id,
                    fe.object_id,
                    fe.content,
                    fe.metrics,
                    fe.parent_content_type_id,
                    fe.parent_object_id,
                    fe.action,
                    fe.action_date,
                    fe.user_id,
                    fe.unified_document_id,
                    ud.hot_score,
                    fe.created_date,
                    fe.updated_date
                FROM
                    feed_feedentry fe
                JOIN
                    researchhub_document_researchhubunifieddocument ud ON fe.unified_document_id = ud.id
                WHERE
                    ud.is_removed = FALSE
                    {limit_data}
                ORDER BY
                    ud.hot_score DESC;

            CREATE UNIQUE INDEX feed_feedentry_popular_unique_idx ON feed_feedentry_popular (id);
            CREATE INDEX feed_feedentry_popular_hotscore_idx ON feed_feedentry_popular (hot_score DESC);
            CREATE INDEX feed_feedentry_popular_action_date_idx ON feed_feedentry_popular (action_date DESC);
            CREATE INDEX feed_feedentry_popular_parent_lookup_idx ON feed_feedentry_popular (parent_content_type_id, parent_object_id);
            """.format(
            limit_data
        )
        return sql

    operations = [
        migrations.RunSQL(
            sql=get_sql(),
            reverse_sql="""
                DROP MATERIALIZED VIEW IF EXISTS feed_feedentry_popular;
            """,
        ),
    ]
