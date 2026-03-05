from django.contrib import admin
from django.urls import path, include
from django.db import connection
from django.http import JsonResponse

def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1") 
        return JsonResponse({"status": "ok", "db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Database unreachable"}, status=500)

urlpatterns = [
    path("", health),
    path("admin/", admin.site.urls),
    path("api/", include("rentals.urls")),
]