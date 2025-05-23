import datetime

import rest_framework.serializers as serializers
from django.db.models import IntegerField, Sum
from django.db.models.functions import Cast

from paper.serializers import BasePaperSerializer, DynamicPaperSerializer
from purchase.models import AggregatePurchase, Purchase
from researchhub.serializers import DynamicModelFieldSerializer
from researchhub_document.serializers import ResearchhubPostSerializer
from researchhub_document.serializers.researchhub_post_serializer import (
    DynamicPostSerializer,
)
from user.serializers import DynamicUserSerializer
from utils import sentry


class PurchaseSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = [
            "id",
            "purchase_hash",
            "created_date",
            "transaction_hash",
            "boost_time",
            "group",
            "updated_date",
        ]

    def get_source(self, purchase):
        model_name = purchase.content_type.name
        if self.context.get("exclude_source", False):
            return None

        serializer = None
        object_id = purchase.object_id
        model_class = purchase.content_type.model_class()
        if model_name == "paper":
            paper = model_class.objects.get(id=object_id)
            serializer = BasePaperSerializer(paper, context=self.context)
        elif model_name == "researchhub post":
            post = model_class.objects.get(id=object_id)
            serializer = ResearchhubPostSerializer(post, context=self.context)

        if serializer is not None:
            return serializer.data

        return None

    def get_end_date(self, purchase):
        status = purchase.paid_status
        purchase_method = purchase.purchase_method

        if purchase_method == Purchase.ON_CHAIN and status != Purchase.PAID:
            return None

        created_date = purchase.created_date
        timedelta = datetime.timedelta(days=int(purchase.amount))
        end_date = created_date + timedelta
        return end_date.isoformat()


class DynamicPurchaseSerializer(DynamicModelFieldSerializer):
    content_type = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = "__all__"

    def get_source(self, purchase):
        context = self.context
        _context_fields = context.get("pch_dps_get_source", {})
        model_name = purchase.content_type.name

        serializer = None
        item = None
        object_id = purchase.object_id
        model_class = purchase.content_type.model_class()
        try:
            if model_name == "paper":
                item = model_class.objects.get(id=object_id)
                serializer = DynamicPaperSerializer
            elif model_name == "researchhub post":
                item = model_class.objects.get(id=object_id)
                serializer = DynamicPostSerializer
            elif model_name == "rh comment model":
                from researchhub_comment.serializers import DynamicRhCommentSerializer

                item = model_class.objects.get(id=object_id)
                serializer = DynamicRhCommentSerializer
            elif model_name == "fundraise":
                item = model_class.objects.get(id=object_id)
                serializer = None

            if serializer is not None:
                data = serializer(item, context=context, **_context_fields).data
                return data
        except Exception as e:
            print(e)
            sentry.log_error(e)

        return None

    def get_user(self, purchase):
        context = self.context
        _context_fields = context.get("pch_dps_get_user", {})
        serializer = DynamicUserSerializer(
            purchase.user, context=context, **_context_fields
        )
        return serializer.data

    def get_end_date(self, purchase):
        status = purchase.paid_status
        purchase_method = purchase.purchase_method

        if purchase_method == Purchase.ON_CHAIN and status != Purchase.PAID:
            return None

        created_date = purchase.created_date
        timedelta = datetime.timedelta(days=int(purchase.amount))
        end_date = created_date + timedelta
        return end_date.isoformat()

    def get_content_type(self, purchase):
        content = purchase.content_type
        return {"app_label": content.app_label, "model": content.model}


class AggregatePurchaseSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    purchases = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = AggregatePurchase
        fields = "__all__"

    def get_source(self, purchase):
        model_name = purchase.content_type.name
        if model_name == "paper":
            Paper = purchase.content_type.model_class()
            paper = Paper.objects.get(id=purchase.object_id)
            serializer = BasePaperSerializer(paper, context=self.context)
            data = serializer.data
            return data
        elif model_name == "researchhub post":
            Post = purchase.content_type.model_class()
            post = Post.objects.get(id=purchase.object_id)
            serializer = ResearchhubPostSerializer(post, context=self.context)
            data = serializer.data
            return data
        return None

    def get_purchases(self, purchase):
        purchases = purchase.purchases
        self.context["exclude_source"] = True
        self.context["exclude_stats"] = True
        serializer = PurchaseSerializer(purchases, context=self.context, many=True)
        data = serializer.data
        return data

    def get_stats(self, purchase):
        total_amount = sum(
            map(float, purchase.purchases.values_list("amount", flat=True))
        )

        created_date = purchase.created_date

        max_boost = (
            purchase.purchases.annotate(amount_as_int=Cast("amount", IntegerField()))
            .aggregate(sum=Sum("amount_as_int"))
            .get("sum", 0)
            or 0
        )

        timedelta = datetime.timedelta(days=int(max_boost))
        end_date = (created_date + timedelta).isoformat()

        stats = {
            "total_views": 0,  # TODO: Remove deprecated field
            "total_clicks": 0,  # TODO: Remove deprecated field
            "total_amount": total_amount,
            "end_date": end_date,
        }
        return stats
