from django.urls import path
from .views import DressListAPIView, DressAvailabilityAPIView

urlpatterns = [
    path("dresses/", DressListAPIView.as_view()),
    path("dresses/<int:pk>/availability/", DressAvailabilityAPIView.as_view()),
]