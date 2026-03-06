from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError

from .models import Dress
from .serializers import DressSerializer


class BurstThrottle(AnonRateThrottle):
    rate = "2000/day"


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


@method_decorator(cache_page(60 * 5), name="dispatch")
class DressListAPIView(ListAPIView):
    serializer_class = DressSerializer
    throttle_classes = [AnonRateThrottle, BurstThrottle]
    pagination_class = StandardLimitOffsetPagination

    def get_queryset(self):
        qs = (
            Dress.objects
            .annotate(available_after=Max("rental_periods__end_date"))
            .prefetch_related("images")
            .filter(is_active=True)
        )

        params = self.request.query_params

        dress_type = params.get("dress_type")
        if dress_type:
            qs = qs.filter(dress_type=dress_type)

        if params.get("featured_only") == "true":
            qs = qs.filter(is_featured=True)

        min_price = params.get("min_price")
        max_price = params.get("max_price")

        if min_price:
            qs = qs.filter(price_without_jewelry__gte=min_price)

        if max_price:
            qs = qs.filter(price_without_jewelry__lte=max_price)

        size = params.get("size")
        if size:
            qs = qs.filter(sizes__contains=[size])

        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return qs.order_by("-is_featured", "-created_at")


class DressAvailabilityAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        date = request.query_params.get("date")

        if not date:
            raise ValidationError({"date": "Query parameter 'date' is required."})

        dress = get_object_or_404(Dress, pk=pk)

        is_available = not dress.rental_periods.filter(
            start_date__lte=date,
            end_date__gte=date,
        ).exists()

        return Response({"available": is_available})