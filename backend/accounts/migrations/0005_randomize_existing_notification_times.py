import random
from datetime import time
from django.db import migrations


def get_random_notification_time():
    hour = random.randint(7, 9)
    minute = random.randint(0, 59)
    return time(hour, minute)


def randomize_notification_times(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    # Randomize for all users who have no time set
    for user in User.objects.filter(notification_time__isnull=True):
        user.notification_time = get_random_notification_time()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_notification_time'),
    ]

    operations = [
        migrations.RunPython(randomize_notification_times),
    ]
