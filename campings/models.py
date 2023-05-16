from django.conf import settings
from django.db import models

from common.models import CommonModel


class CampGround(CommonModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campgrounds",
    )

    price = models.PositiveIntegerField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    pet_friendly = models.BooleanField(default=False)
    ev_friendly = models.BooleanField(default=False)
    address = models.CharField(max_length=255)

    check_in = models.DateField()
    check_out = models.DateField()

    ratings = models.PositiveIntegerField()

    name = models.CharField(max_length=255)

    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="campgrounds",
        
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
