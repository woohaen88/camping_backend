from django.urls import path

from users.views import SignUPViewSet, LoginView, MeView

app_name = "users"

signUPViewSet = SignUPViewSet.as_view(
    {
        "post": "create",
    }
)


urlpatterns = [
    path("signup/", signUPViewSet),
    path("log-in/", LoginView.as_view(), name="log-in"),
    path("me/", MeView.as_view(), name="me"),
]
