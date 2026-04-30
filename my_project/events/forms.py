from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Event, Wishlist

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'you@domain.com'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Your display name'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username", "password1", "password2")

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password'
        })
    )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'budget', 'exchange_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Holiday gift exchange'
            }),
            'budget': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'For example: $30 - $40'
            }),
            'exchange_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'input-field'
            }),
        }

class WishlistForm(forms.ModelForm):
    wish_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-field',
            'placeholder': 'Tell your Secret Santa what makes your heart happy...',
            'rows': 5
        }),
        label="Your wishlist"
    )

    class Meta:
        model = Wishlist
        fields = ['wish_text']
