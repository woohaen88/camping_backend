from django.contrib import admin

from campings.models import CampGround
from medias.models import Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3


@admin.register(CampGround)
class CampGroundAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]
