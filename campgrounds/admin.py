from django.contrib import admin
from campgrounds.models import Campground, Image, Amenity, Review


class ImageInline(admin.TabularInline):
    model = Image
    extra = 5


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 4


@admin.register(Campground)
class CampgroundAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
