from django.urls import path

from tags.views import TagViewSet

app_name = "tags"

tagViewSet = TagViewSet.as_view(
    {
        "get": "list",
    }
)

urlpatterns = [
    path("", tagViewSet, name="list_or_create"),
]
