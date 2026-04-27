import random
from .models import EventParticipant, Assignment, Event

def run_draw(event):
    participants = list(
        EventParticipant.objects.filter(event=event).values_list('user', flat=True)
    )

    if len(participants) < 3:
        raise Exception("Minimum 3 users required")

    while True:
        shuffled = participants.copy()
        random.shuffle(shuffled)

        valid = True
        for g, r in zip(participants, shuffled):
            if g == r:
                valid = False
                break

        if valid:
            break

    Assignment.objects.filter(event=event).delete()

    for g, r in zip(participants, shuffled):
        Assignment.objects.create(
            event=event,
            giver_id=g,
            receiver_id=r
        )

    event.is_drawn = True
    event.save()