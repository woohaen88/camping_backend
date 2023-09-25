from django.db import models
from django.conf import settings

# custom
from common.models import CommonModel


class Campground(CommonModel):
    class KindOfView(models.TextChoices):
        MOUNTAIN = "mountain", "Mountain"
        RIVER = "river", "River"
        LAKE = "lake", "Lake"
        OTHER = "other", "Other"

    class KindOfCamping(models.TextChoices):
        AUTO = "auto", "Auto"
        OTHER = "other", "Other"

    name = models.CharField(max_length=150)
    rating = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    view = models.CharField(max_length=10, choices=KindOfView.choices)

    visited_at = models.DateField()
    visited_end = models.DateField()
    manner_time_start = models.TimeField()
    manner_time_end = models.TimeField()

    content = models.TextField(blank=True, null=True)

    maximum_people = models.PositiveIntegerField(default=4)
    is_ev_charge = models.BooleanField(default=False)

    camping_kind = models.CharField(
        max_length=10, choices=KindOfCamping.choices, default=KindOfCamping.AUTO
    )

    amenities = models.ManyToManyField(
        "campgrounds.Amenity", blank=True, related_name="campgrounds"
    )

    location = models.CharField(max_length=150, blank=True, null=True)
    location_lat_lon = models.CharField(max_length=150, blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campgrounds"
    )

    def __str__(self):
        return self.name


class Amenity(CommonModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Review(CommonModel):
    content = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    campground = models.ForeignKey(
        "campgrounds.Campground", on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return self.content[:10]


class Image(CommonModel):
    file = models.URLField()

    campground = models.ForeignKey(
        "campgrounds.Campground", on_delete=models.CASCADE, related_name="images"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        return self.file[:10]
