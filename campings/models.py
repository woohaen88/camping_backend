from django.conf import settings
from django.db import models

from common.models import CommonModel


class CampGround(CommonModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campgrounds",
    )

    check_in = models.DateField()
    check_out = models.DateField()

    ratings = models.PositiveIntegerField()
    description = models.TextField(
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="campgrounds",
    )

    def __str__(self) -> str:
        return self.name
