from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid

# ================= BASE =================
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# ================= USER =================
class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# ================= PROFILE (OneToOne) =================
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)


# ================= EVENT =================
class EventStatus(models.TextChoices):
    WAITING = 'WAITING'
    DRAWN = 'DRAWN'


class Event(BaseModel):
    title = models.CharField(max_length=255)
    exchange_date = models.DateTimeField()
    join_code = models.CharField(max_length=20, unique=True)

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=EventStatus.choices,
        default=EventStatus.WAITING
    )


# ================= PARTICIPANT =================
class EventParticipant(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')


# ================= WISHLIST =================
class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')


class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=255)


# ================= ASSIGNMENT =================
class Assignment(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giver')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    def clean(self):
        if self.giver == self.receiver:
            raise ValidationError("Cannot assign yourself")