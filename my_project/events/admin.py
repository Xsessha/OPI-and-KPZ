from django.contrib import admin
from .models import User, Event, EventParticipant, Wishlist, Assignment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_staff']
    search_fields = ['email', 'username']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'exchange_date', 'is_drawn', 'join_code']
    search_fields = ['title', 'join_code']
    list_filter = ['is_drawn', 'exchange_date']

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user']
    search_fields = ['event__title', 'user__email']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'wish_text']
    search_fields = ['user__email', 'event__title']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['event', 'giver', 'receiver', 'is_gift_sent']
    search_fields = ['event__title', 'giver__email', 'receiver__email']
    list_filter = ['is_gift_sent']
