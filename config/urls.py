from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


BASE_URL = "api/v1/"
urlpatterns = [
    path("admin/", admin.site.urls),
    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # custom
    path(BASE_URL + "camping/", include("campings.urls")),
    path(BASE_URL + "user/", include("users.urls")),
]
