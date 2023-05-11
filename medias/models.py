from django.db import models
from django.conf import settings


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
    file = models.URLField()
    description = models.TextField(
        null=True,
        blank=True,
    )
