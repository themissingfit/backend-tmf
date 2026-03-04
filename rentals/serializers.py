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
        periods = obj.rental_periods.all()
        if periods:
            latest = max(periods, key=lambda p: p.end_date)
            return latest.end_date
        return None