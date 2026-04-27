import random
from .models import Event, Assignment, EventParticipant

def run_secret_santa(event_id):
    event = Event.objects.get(id=event_id)

    participants = list(
        EventParticipant.objects.filter(event=event).values_list('user', flat=True)
    )

    if len(participants) < 3:
        raise Exception("Minimum 3 participants required")

    receivers = participants.copy()

    success = False

    while not success:
        random.shuffle(receivers)
        success = True

        for giver, receiver in zip(participants, receivers):
            if giver == receiver:
                success = False
                break

    # очищаємо старі призначення
    Assignment.objects.filter(event=event).delete()

    # створюємо нові
    for giver, receiver in zip(participants, receivers):
        Assignment.objects.create(
            event=event,
            giver_id=giver,
            receiver_id=receiver
        )

    event.status = 'DRAWN'
    event.save()