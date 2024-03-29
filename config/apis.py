from ninja import NinjaAPI

# from campgrounds.apis import router as campground_router
from campgrounds.apis import router as campground_router
from users.api import router as users_router


api = NinjaAPI(csrf=True, docs_url="docs/")

api.add_router("/campgrounds/", campground_router)
api.add_router("/users/", users_router)
