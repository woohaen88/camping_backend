from django.contrib import admin
from django.urls import path, include


BASE_URL = "api/v1/"
urlpatterns = [
    path("admin/", admin.site.urls),
    path(BASE_URL + "camping/", include("campings.urls")),
    path(BASE_URL + "user/", include("users.urls")),
    path(BASE_URL + "media/", include("medias.urls")),
]
