import uuid

from django.db import models
from django.utils import timezone

from config import settings


# Create your models here.


class SessionLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey("fishing.Session", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session_likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("session", "user")


    def __str__(self):
        return f"{self.user} liked {self.session.id}"


class SessionComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey("fishing.Session", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session_comments")

    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]


    def __str__(self):
        return f"Comment by {self.author} on {self.session.id}"




class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_friend_requests")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_friend_requests")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("sender", "receiver")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == self.Status.ACCEPTED:
            self.sender.friends.add(self.receiver)

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"
