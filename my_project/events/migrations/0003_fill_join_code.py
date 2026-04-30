from django.db import migrations


def generate_join_code(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    import random

    letters = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'

    def make_code(length=6):
        code = ''.join(random.choice(letters) for _ in range(length))
        while Event.objects.filter(join_code=code).exists():
            code = ''.join(random.choice(letters) for _ in range(length))
        return code

    for event in Event.objects.filter(join_code=''):
        event.join_code = make_code()
        event.save(update_fields=['join_code'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_wishlistitem_wishlist_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_join_code, noop),
    ]
