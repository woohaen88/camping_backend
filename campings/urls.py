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

urlpatterns = [
    path("", campGroundViewSet),
    path("<int:campGround_id>/", campGroundViewSetDetail),
]
