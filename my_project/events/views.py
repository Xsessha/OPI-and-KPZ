from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import UserRegistrationForm, EventForm, WishlistForm
from .services import run_draw
import random

from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required
def home(request):
    events = Event.objects.all()
    return render(request, 'events/home.html', {'events': events})


@login_required
def create_event(request):
    form = EventForm(request.POST or None)

    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.join_code = str(random.randint(100000, 999999))
        event.save()

        EventParticipant.objects.create(event=event, user=request.user)

        return redirect('home')

    return render(request, 'events/create_event.html', {'form': form})


@login_required
def join_event(request):
    if request.method == "POST":
        code = request.POST.get('code')
        # Використовуй get_object_or_404, щоб замість помилки коду 
        # видати сторінку "Не знайдено" (404)
        event = get_object_or_404(Event, join_code=code)

        EventParticipant.objects.get_or_create(
            event=event,
            user=request.user
        )
        return redirect('home')

    return render(request, 'events/join_event.html')


@login_required
def wishlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    obj, _ = Wishlist.objects.get_or_create(
        user=request.user,
        event=event
    )

    form = WishlistForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'events/wishlist.html', {'form': form})


@login_required
def run_draw_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        return redirect('home')

    run_draw(event)

    return redirect('home')


@login_required
def assignment(request, event_id):
    a = Assignment.objects.get(event_id=event_id, giver=request.user)

    wishlist = Wishlist.objects.get(user=a.receiver, event_id=event_id)

    return render(request, 'events/assignment.html', {
        'assignment': a,
        'wishlist': wishlist
    })