from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Dress
from .serializers import DressSerializer


class DressListAPIView(ListAPIView):
    queryset = Dress.objects.filter(is_active=True)
    serializer_class = DressSerializer
