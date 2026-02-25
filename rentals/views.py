from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from .models import Dress
from .serializers import DressSerializer


class BurstThrottle(AnonRateThrottle):
    rate = "2000/day"


@method_decorator(cache_page(60 * 5), name="dispatch")
class DressListAPIView(ListAPIView):
    serializer_class = DressSerializer
    throttle_classes = [AnonRateThrottle, BurstThrottle]

    def get_queryset(self):
        qs = (
            Dress.objects
            .prefetch_related("images", "rental_periods")
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        limit = request.query_params.get("limit")
        offset = request.query_params.get("offset")

        if limit and offset:
            limit = int(limit)
            offset = int(offset)
            queryset = queryset[offset:offset + limit]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DressAvailabilityAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        date = request.query_params.get("date")
        dress = Dress.objects.get(pk=pk)

        is_available = not dress.rental_periods.filter(
            start_date__lte=date,
            end_date__gte=date,
        ).exists()

        return Response({"available": is_available})