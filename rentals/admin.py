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
        "is_featured",
        "is_active",
    )
    list_filter = ("dress_type", "status", "is_featured", "is_active")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    inlines = [DressImageInline]


@admin.register(DressRentalPeriod)
class DressRentalPeriodAdmin(admin.ModelAdmin):
    list_display = ("dress", "start_date", "end_date")
    search_fields = ("dress__name",)
    list_select_related = ("dress",)
    autocomplete_fields = ("dress",)