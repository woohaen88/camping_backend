from django.urls import path

from campings.views import CampGroundViewSet

campGroundViewSet = CampGroundViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

campGroundViewSetDetail = CampGroundViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


app_name = "campings"
urlpatterns = [
    path("", campGroundViewSet, name="list"),
    path("<int:campGround_id>/", campGroundViewSetDetail, name="detail"),
]
