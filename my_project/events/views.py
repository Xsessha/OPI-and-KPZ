from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Exists, OuterRef, Prefetch

from .models import Event, EventParticipant, Wishlist, Assignment
from .forms import UserRegistrationForm, EventForm, WishlistForm
from .services import run_draw


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome aboard! Your Secret Santa journey begins now.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required
def home(request):
    from django.db.models import Q
    
    wishlist_exists = Wishlist.objects.filter(user=request.user, event=OuterRef('pk'))
    assignment_exists = Assignment.objects.filter(event=OuterRef('pk'), giver=request.user)

    # Show events where user is a participant OR organizer
    events = (
        Event.objects.filter(Q(eventparticipant__user=request.user) | Q(organizer=request.user))
        .select_related('organizer')
        .distinct()
        .annotate(
            participant_count=Count('eventparticipant'),
            has_wishlist=Exists(wishlist_exists),
            has_assignment=Exists(assignment_exists)
        )
        .prefetch_related(
            Prefetch('eventparticipant_set', queryset=EventParticipant.objects.select_related('user'))
        )
        .order_by('exchange_date')
    )

    return render(request, 'events/home.html', {'events': events})


@login_required
def create_event(request):
    form = EventForm(request.POST or None)

    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user  # Set the creator as organizer
        event.save()
        # Add the organizer as a participant (use get_or_create to avoid duplicates)
        EventParticipant.objects.get_or_create(event=event, user=request.user)
        messages.success(request, f'Event "{event.title}" created! Share code {event.join_code} with your group.')
        return redirect('home')

    return render(request, 'events/create_event.html', {'form': form})


@login_required
def join_event(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        if not code:
            messages.error(request, 'Enter the event code to join.')
            return redirect('join_event')

        try:
            event = Event.objects.get(join_code=code)
            participant, created = EventParticipant.objects.get_or_create(event=event, user=request.user)
            if created:
                messages.success(request, f'✅ Joined {event.title}! Add your wishlist to help your Secret Santa.')
            else:
                messages.info(request, f'You are already a participant in {event.title}.')
            return redirect('home')
        except Event.DoesNotExist:
            messages.error(request, 'That code does not match any event. Double-check and try again.')
            return redirect('join_event')

    return render(request, 'events/join_event.html')


@login_required
def wishlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    obj, _ = Wishlist.objects.get_or_create(user=request.user, event=event)
    form = WishlistForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        messages.success(request, 'Wishlist saved! Your Secret Santa is one step closer.')
        return redirect('home')

    suggestions = [
        'I love coffee ☕',
        'No socks please 😅',
        'Tech gadgets are welcome',
    ]

    return render(request, 'events/wishlist.html', {
        'form': form,
        'event': event,
        'suggestions': suggestions,
    })


@login_required
def run_draw_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)

    try:
        run_draw(event)
        messages.success(request, 'The draw is complete! Everyone has their assignment. 🎁')
    except Exception as exc:
        messages.error(request, f'Draw failed: {str(exc)}')
    
    return redirect('home')


@login_required
def assignment(request, event_id):
    assignment = Assignment.objects.filter(event_id=event_id, giver=request.user).first()
    if not assignment:
        messages.error(request, 'Assignment not available yet. Wait for the organizer to run the draw.')
        return redirect('home')

    wishlist = Wishlist.objects.filter(user=assignment.receiver, event_id=event_id).first()
    return render(request, 'events/assignment.html', {
        'assignment': assignment,
        'wishlist': wishlist,
    })


@login_required
def mark_gift_sent(request, event_id):
    assignment = get_object_or_404(Assignment, event_id=event_id, giver=request.user)
    assignment.is_gift_sent = True
    assignment.save()
    messages.success(request, 'Nice! Gift status updated to sent.')
    return redirect('assignment', event_id=event_id)
