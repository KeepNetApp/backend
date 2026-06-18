import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    def __str__(self):
        return self.username

