import uuid

from django.db.models import SET_NULL
from django.utils import timezone

from config import settings
from users.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.

class Session(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = 'PRIVATE', 'Private'
        FRIENDS = 'FRIENDS', 'Friends Only'
        PUBLIC = 'PUBLIC', 'Public'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE
    )

    notes = models.TextField(null=True, blank=True)


class Catch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    species = models.ForeignKey(to="fishing.Species", on_delete=models.CASCADE)
    session = models.ForeignKey(to="fishing.Session", on_delete=SET_NULL, null=True, blank=True, related_name='catches')
    location = gis_models.PointField()
    time_caught = models.DateTimeField()
    weight_kg = models.FloatField(null=True, blank=True)
    length_m = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            gis_models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.species} caught by {self.user} on {self.time_caught.strftime('%Y-%m-%d')}"


class CatchPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catch = models.ForeignKey(to="fishing.Catch", on_delete=models.CASCADE, related_name="photo")
    photo = models.URLField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField()

class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserSpeciesStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    species = models.ForeignKey(to="fishing.Species", on_delete=models.CASCADE)
    total_caught = models.IntegerField(default=0)

    first_catch = models.ForeignKey(to="fishing.Catch", on_delete=SET_NULL, null=True, blank=True, related_name="+")
    max_weight_catch = models.ForeignKey(to="fishing.Catch", on_delete=SET_NULL, null=True, blank=True, related_name="+")
    max_length_catch = models.ForeignKey(to="fishing.Catch", on_delete=SET_NULL, null=True, blank=True, related_name="+")

    class Meta:
        unique_together = ("user", "species")


    def __str__(self):
        return f"{self.user}'s stats for {self.species}"
