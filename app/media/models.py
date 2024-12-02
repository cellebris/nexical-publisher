from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from private_storage.fields import PrivateFileField

from app.events.models import Event
from app.teams.models import Team
from app.utils.models import BaseUUIDModel
from app.utils.python import get_identifier


def team_media_path(instance, filename):
    # file will be uploaded to PRIVATE_STORAGE_ROOT/uploads/media/<collection_id>/<filename>
    return f"uploads/media/{instance.collection.id}/{filename}"


class TeamMediaCollection(BaseUUIDModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="media_collections")
    name = models.CharField(_("Media Collection Name"), blank=False, max_length=255)
    description = models.TextField(
        _("Media Collection Description"),
        help_text=_(
            "The images in this media collection are used by the publishing AI to match relevant images with data cards.  "
            "This description will help the recommendation engine find appropriate images for site content."
        ),
        blank=True,
    )
    processed_time = models.DateTimeField(_("Processed Time"), blank=True, null=True)

    access_teams = models.ManyToManyField(
        Team,
        related_name="media_collection_access",
        help_text=_(
            "You can share this media collection with other teams on this platform. "
            "You can search teams by team name or team owner email address."
        ),
        blank=True,
    )

    def __str__(self):
        return f"{self.name} @ {self.team}"

    def create_event(self, operation="update"):
        files = []
        for file in self.files.all():
            content = ""
            handle = None
            try:
                handle = file.file.open(mode="rb")
                content = handle.read()
            finally:
                if handle:
                    handle.close()

            files.append(
                {
                    "id": str(file.id),
                    "name": str(file.file).split("/")[-1],
                    "description": file.description,
                    "hash": get_identifier(content),
                }
            )

        bookmarks = []
        for bookmark in self.bookmarks.all():
            bookmarks.append(
                {
                    "id": str(bookmark.id),
                    "description": bookmark.description,
                    "url": bookmark.url,
                }
            )

        Event.objects.create(
            type="media_collection",
            data={
                "operation": operation,
                "team_id": str(self.team.id),
                "team_name": self.team.name,
                "id": str(self.id),
                "name": self.name,
                "description": self.description,
                "files": files,
                "bookmarks": bookmarks,
                "access_teams": [str(team_id) for team_id in self.access_teams.values_list("id", flat=True)],
            },
        )
        if operation != "delete":
            self.processed_time = None
            self.save()


@receiver(post_delete, sender=TeamMediaCollection)
def delete_media_collection_hook(sender, instance, using, **kwargs):
    instance.create_event("delete")


class TeamMedia(BaseUUIDModel):
    collection = models.ForeignKey(TeamMediaCollection, on_delete=models.CASCADE, related_name="files")
    description = models.TextField(
        _("Media Description"),
        help_text=_(
            "The images in this media collection are used by the publishing AI to match relevant images with data cards.  "
            "This description will help the recommendation engine find appropriate images for site content."
        ),
        blank=True,
    )
    file = PrivateFileField(
        _("Image File"),
        upload_to=team_media_path,
        content_types=[
            "image/apng",
            "image/avif",
            "image/gif",
            "image/jpeg",
            "image/png",
            "image/svg+xml",
        ],
        max_file_size=settings.PRIVATE_STORAGE_MAX_FILE_SIZE,
    )

    def save(self, *args, **kwargs):
        try:
            existing = TeamMedia.objects.get(id=self.id)
            if existing.file != self.file:
                existing.file.delete(save=False)
        except TeamMedia.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)


class TeamMediaBookmark(BaseUUIDModel):
    collection = models.ForeignKey(TeamMediaCollection, on_delete=models.CASCADE, related_name="bookmarks")
    description = models.TextField(
        _("Media Description"),
        help_text=_(
            "The images in this media collection are used by the publishing AI to match relevant images with data cards.  "
            "This description will help the recommendation engine find appropriate images for site content."
        ),
        blank=True,
    )
    url = models.URLField(_("URL"), max_length=500)
