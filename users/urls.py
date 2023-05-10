from django.urls import path

from users.views import SignUPViewSet

signUPViewSet = SignUPViewSet.as_view(
    {
        "post": "create",
    }
)
urlpatterns = [path("signup/", signUPViewSet)]
