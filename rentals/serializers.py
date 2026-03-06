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

    # populated by queryset annotation in the view
    available_after = serializers.DateField(read_only=True)

    class Meta:
        model = Dress
        fields = [
            "id",
            "name",
            "description",
            "dress_type",
            "sizes",
            "price_without_jewelry",
            "price_with_jewelry",
            "security_deposit",
            "status",
            "available_after",
            "images",
        ]