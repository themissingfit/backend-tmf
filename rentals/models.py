# missingfit_backend/rentals/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from cloudinary.models import CloudinaryField


class Dress(models.Model):

    DRESS_TYPE_CHOICES = [
        ("saree", "Saree"),
        ("lehenga", "Lehenga"),
        ("sharara", "Sharara"),
        ("gown", "Gown"),
        ("anarkali", "Anarkali"),
        ("indo_western", "Indo-Western"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("rented", "Rented"),
        ("maintenance", "Maintenance"),
    ]

    SIZE_CHOICES = [
        ("free", "Free Size"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    dress_type = models.CharField(
        max_length=50, choices=DRESS_TYPE_CHOICES
    )

    sizes = models.JSONField(default=list)

    price_without_jewelry = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    price_with_jewelry = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    security_deposit = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_status(self):
        today = now().date()
        active_rental = self.rental_periods.filter(
            start_date__lte=today,
            end_date__gte=today,
        ).exists()

        if self.status != "maintenance":
            self.status = "rented" if active_rental else "available"
            self.save(update_fields=["status"])

    def __str__(self):
        return self.name


class DressRentalPeriod(models.Model):
    dress = models.ForeignKey(
        Dress,
        on_delete=models.CASCADE,
        related_name="rental_periods"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        overlapping = DressRentalPeriod.objects.filter(
            dress=self.dress,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError(
                "This dress is already rented for the selected dates."
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.dress.update_status()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.dress.update_status()


class DressImage(models.Model):
    dress = models.ForeignKey(
        Dress,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField("image")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.dress.name}"
