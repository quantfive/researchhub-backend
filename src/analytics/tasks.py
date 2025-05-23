from typing import Literal

from analytics.amplitude import Amplitude
from purchase.related_models.rsc_exchange_rate_model import RscExchangeRate
from researchhub.celery import QUEUE_EXTERNAL_REPORTING, app
from researchhub.settings import DEVELOPMENT
from utils.sentry import log_error


@app.task(queue=QUEUE_EXTERNAL_REPORTING)
def track_revenue_event(
    user_id,
    revenue_type: Literal[
        "BOUNTY_FEE",
        "FUNDRAISE_CONTRIBUTION_FEE",
        "SUPPORT_FEE",
        "DOI_FEE",
        "WITHDRAWAL_FEE",
    ],
    rsc_revenue: str,
    usd_revenue: str = None,
    transaction_method: Literal["OFF_CHAIN", "ON_CHAIN"] = None,
    # it's useful to be able to see e.g. how much did we make on paper tips versus comment tips.
    # so we should use these fields to point to the object that the revenue is associated with.
    # and not simply the Purchase/Balance/Fundraise object.
    content_type: str = None,
    object_id: str = None,
    additional_properties: dict = {},
):
    """
    Helper function to track revenue events.
    Performs the conversion from RSC to USD if usd_revenue is None.
    """

    from user.models import User

    amp = None
    user = None
    if DEVELOPMENT:
        return

    def handle_log_error(e, message):
        """Helper to add useful JSON data to Sentry"""
        log_error(
            e,
            message=message,
            json_data={
                "user_id": user_id,
                "rsc_revenue": rsc_revenue,
                "usd_revenue": usd_revenue,
                "revenue_type": revenue_type,
                "transaction_method": transaction_method,
                "content_type": content_type,
                "object_id": object_id,
            },
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        handle_log_error(e, "Error tracking revenue event")
        return

    try:
        if usd_revenue is None:
            if not isinstance(rsc_revenue, float):
                rsc_revenue_float = float(rsc_revenue)
            else:
                rsc_revenue_float = rsc_revenue

            usd_revenue_float = RscExchangeRate.rsc_to_usd(rsc_revenue_float)
            usd_revenue = str(usd_revenue_float)
    except Exception as e:
        handle_log_error(e, "Error converting RSC to USD")

    try:
        additional_properties["transaction_method"] = transaction_method
        additional_properties["content_type"] = content_type
        additional_properties["object_id"] = object_id

        amp = Amplitude()
        amp._track_revenue_event(
            user,
            revenue_type,
            rsc_revenue,
            usd_revenue,
            additional_properties,
        )
    except Exception as e:
        handle_log_error(e, "Error tracking revenue event")
