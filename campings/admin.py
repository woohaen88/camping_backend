from django.contrib import admin

from campings.models import CampGround


@admin.register(CampGround)
class CampGroundAdmin(admin.ModelAdmin):
    pass
