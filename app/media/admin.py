from django.contrib import admin

from . import models


class TeamMediaInline(admin.TabularInline):
    model = models.TeamMedia
    extra = 1


class TeamMediaBookmarkInline(admin.TabularInline):
    model = models.TeamMediaBookmark
    extra = 1


@admin.register(models.TeamMediaCollection)
class TeamMediaCollectionAdmin(admin.ModelAdmin):
    inlines = [TeamMediaInline, TeamMediaBookmarkInline]
