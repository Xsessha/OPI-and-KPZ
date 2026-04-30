from django.test import TestCase
from django.urls import reverse
from .models import User, Event, EventParticipant, Wishlist, Assignment
from .services import run_draw
from datetime import datetime, timedelta


class PleaseNoSocksTests(TestCase):

    def setUp(self):
        # Створюємо 3 користувачів
        self.u1 = User.objects.create_user(email='u1@test.com', username='u1', password='pass1234')
        self.u2 = User.objects.create_user(email='u2@test.com', username='u2', password='pass1234')
        self.u3 = User.objects.create_user(email='u3@test.com', username='u3', password='pass1234')

        # Створюємо подію
        self.event = Event.objects.create(
            title="Test Event",
            budget="500",
            exchange_date=datetime.now() + timedelta(days=5),
            organizer=self.u1
        )

        # Додаємо учасників
        EventParticipant.objects.create(event=self.event, user=self.u1)
        EventParticipant.objects.create(event=self.event, user=self.u2)
        EventParticipant.objects.create(event=self.event, user=self.u3)

    # 1. Тест створення Wishlist
    def test_wishlist_creation(self):
        Wishlist.objects.create(user=self.u1, event=self.event, wish_text="Coffee")
        self.assertEqual(Wishlist.objects.count(), 1)

    # 2. Тест приєднання до події по коду
    def test_join_event_by_code(self):
        code = self.event.join_code
        found_event = Event.objects.get(join_code=code)
        self.assertEqual(found_event.id, self.event.id)

    # 3. Тест алгоритму розподілу (створюються Assignment)
    def test_run_draw_creates_assignments(self):
        run_draw(self.event)
        self.assertEqual(Assignment.objects.count(), 3)

    # 4. Немає самопризначення
    def test_no_self_assignment(self):
        run_draw(self.event)
        for a in Assignment.objects.all():
            self.assertNotEqual(a.giver, a.receiver)

    # 5. Кожен має одного отримувача і одного дарувальника
    def test_unique_giver_and_receiver(self):
        run_draw(self.event)
        givers = Assignment.objects.values_list('giver', flat=True)
        receivers = Assignment.objects.values_list('receiver', flat=True)

        self.assertEqual(len(set(givers)), 3)
        self.assertEqual(len(set(receivers)), 3)