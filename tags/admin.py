from django.contrib import admin
from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
