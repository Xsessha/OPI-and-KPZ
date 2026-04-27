from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Event, Wishlist

# Форма реєстрації спеціально для твого User
class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username") # email обов'язковий, бо він головний у тебе

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'budget', 'exchange_date'] 
        widgets = {
            'exchange_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class WishlistForm(forms.ModelForm):
    # У твоїй моделі Wishlist не було поля 'wish_text', 
    # але воно було у WishlistItem. 
    # Якщо хочеш просте поле, додай 'wish_text' у модель Wishlist.
    wish_text = forms.CharField(widget=forms.Textarea, label="Твої побажання")

    class Meta:
        model = Wishlist
        fields = ['wish_text']