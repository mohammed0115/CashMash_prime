from rest_framework import filters

from .models import TopUpCardTransaction
from accounts.models import User
from django_filters import rest_framework as df
from .models import Card


class IsTopUpTransactionCardOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects by checking the card belongs to them.
    """
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.user_type is User.USER_TYPE_CARD_HOLDER:
            return queryset.filter(PAN__in=Card.objects.filter(card_holder=user)
                                   .values_list('pan', flat=True))


class TopUpTransactionFilter(df.FilterSet):
    # successful transactions will have an approval_code so use the field being null or not
    # to filter only successful or failed transactions
    successful = df.BooleanFilter(name='approval_code', lookup_expr='isnull', exclude=True)

    date_before = df.IsoDateTimeFilter(name="transaction_date", lookup_expr="lte")
    date_after = df.IsoDateTimeFilter(name="transaction_date", lookup_expr="gte")

    class Meta:
        model = TopUpCardTransaction
        fields = ('successful', 'date_before', 'date_after')