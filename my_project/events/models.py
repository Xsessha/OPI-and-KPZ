from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    budget = models.CharField(max_length=100, default='')
    exchange_date = models.DateTimeField()

    join_code = models.CharField(max_length=10, unique=True, default='')

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')

    is_drawn = models.BooleanField(default=False)
    
    def is_organizer(self, user):
        """Check if a user is the organizer of this event"""
        return user and self.organizer_id == user.id

    @staticmethod
    def generate_join_code(length=6):
        letters = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
        code = ''.join(random.choice(letters) for _ in range(length))
        while Event.objects.filter(join_code=code).exists():
            code = ''.join(random.choice(letters) for _ in range(length))
        return code

    def save(self, *args, **kwargs):
        if not self.join_code:
            self.join_code = self.generate_join_code()
        super().save(*args, **kwargs)


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    wish_text = models.TextField(default='')

    class Meta:
        unique_together = ('user', 'event')


class Assignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giver')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    is_gift_sent = models.BooleanField(default=False)