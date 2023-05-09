from typing import Iterable, Optional
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
