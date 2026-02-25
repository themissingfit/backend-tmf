from rest_framework import serializers
from .models import Dress, DressImage


class DressImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = DressImage
        fields = ["url"]

    def get_url(self, obj):
        if obj.image:
            return obj.image.build_url(
                secure=True,
                quality="auto",
                fetch_format="auto",
            )
        return None


class DressSerializer(serializers.ModelSerializer):
    images = DressImageSerializer(many=True, read_only=True)
    available_after = serializers.SerializerMethodField()

    class Meta:
        model = Dress
        fields = "__all__"

    def get_available_after(self, obj):
        latest = obj.rental_periods.order_by("-end_date").first()
        return latest.end_date if latest else None