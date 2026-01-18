# missingfit_backend/rentals/admin.py
from django.contrib import admin
from .models import Dress, DressRentalPeriod, DressImage


class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1


@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dress_type",
        "status",
        "price_without_jewelry",
        "price_with_jewelry",
        "security_deposit",
        "is_active",
    )

    list_filter = (
        "dress_type",
        "status",
        "is_active",
    )

    search_fields = ("name",)
    inlines = [DressImageInline]


@admin.register(DressRentalPeriod)
class DressRentalPeriodAdmin(admin.ModelAdmin):
    list_display = ("dress", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
