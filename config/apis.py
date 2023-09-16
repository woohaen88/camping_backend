from ninja import NinjaAPI

from campgrounds.api import router as campground_router

api = NinjaAPI(csrf=True, docs_url="docs/")

api.add_router("/campgrounds/", campground_router)
