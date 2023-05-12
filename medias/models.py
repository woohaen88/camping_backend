from django.db import models
from django.conf import settings
from cloudflare_images.field import CloudflareImagesField


class Photo(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    campgrounds = models.ForeignKey(
        "campings.CampGround",
        on_delete=models.CASCADE,
        related_name="photos",
    )
    file = CloudflareImagesField()
    description = models.TextField(
        null=True,
        blank=True,
    )
