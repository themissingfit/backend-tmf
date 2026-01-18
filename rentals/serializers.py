from rest_framework import serializers
from .models import Dress, DressImage


class DressImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="image.url")

    class Meta:
        model = DressImage
        fields = ["url"]


class DressSerializer(serializers.ModelSerializer):
    images = DressImageSerializer(many=True, read_only=True)
    available_after = serializers.SerializerMethodField()

    class Meta:
        model = Dress
        fields = [
            "id",
            "name",
            "description",
            "dress_type",
            "price_without_jewelry",
            "price_with_jewelry",
            "security_deposit",
            "status",
            "available_after",
            "sizes",
            "images",
        ]

    def get_available_after(self, obj):
        latest_rental = obj.rental_periods.order_by("-end_date").first()
        return latest_rental.end_date if latest_rental else None
