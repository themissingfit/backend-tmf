from django.urls import path
from .views import DressListAPIView

urlpatterns = [
    path("dresses/", DressListAPIView.as_view(), name="dress-list"),
]
