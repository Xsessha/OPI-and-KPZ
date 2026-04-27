from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, EventParticipant, Assignment
from .services import run_secret_santa


@login_required
def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


@login_required
def create_event(request):
    if request.method == "POST":
        title = request.POST.get('title')

        event = Event.objects.create(
            title=title,
            organizer=request.user,
            join_code=str(request.user.id)[:6]
        )

        EventParticipant.objects.create(
            event=event,
            user=request.user
        )

        return redirect('home')

    return render(request, 'create_event.html')


@login_required
def join_event(request):
    if request.method == "POST":
        code = request.POST.get('code')
        event = Event.objects.get(join_code=code)

        EventParticipant.objects.get_or_create(
            event=event,
            user=request.user
        )

        return redirect('home')

    return render(request, 'join_event.html')


@login_required
def run_draw(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.organizer != request.user:
        return redirect('home')

    run_secret_santa(event.id)

    return redirect('home')


@login_required
def my_assignment(request, event_id):
    assignment = Assignment.objects.get(
        event_id=event_id,
        giver=request.user
    )

    return render(request, 'assignment.html', {
        'assignment': assignment
    })