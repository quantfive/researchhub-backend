# Manually created

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0014_feedentrypopular"),
    ]

    def get_sql():
        # Limit data to the last 30 days in production
        limit_data = (
            "AND fe.created_date >= (NOW() - INTERVAL '30 days')"
            if settings.PRODUCTION
            else ""
        )

        sql = f"""
                CREATE MATERIALIZED VIEW feed_feedentry_latest AS
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
                        fe.created_date,
                        fe.updated_date
                    FROM
                        feed_feedentry fe
                    WHERE
                        fe.id IN (
                            SELECT DISTINCT ON (content_type_id, object_id) id
                            FROM feed_feedentry
                            ORDER BY content_type_id ASC, object_id ASC, action_date DESC
                        )
                        {limit_data}
                    ORDER BY
                        fe.action_date DESC;

            CREATE UNIQUE INDEX feed_feedentry_latest_unique_idx ON feed_feedentry_latest (id);
            CREATE INDEX feed_feedentry_latest_action_date_idx ON feed_feedentry_latest (action_date DESC);
            CREATE INDEX feed_feedentry_latest_parent_lookup_idx ON feed_feedentry_latest (parent_content_type_id, parent_object_id);

            """.format(
            limit_data
        )
        return sql

    operations = [
        migrations.RunSQL(
            sql=get_sql(),
            reverse_sql="""
                DROP MATERIALIZED VIEW IF EXISTS feed_feedentry_latest;
            """,
        ),
    ]
