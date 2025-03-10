from celery import shared_task
from django.core.mail import send_mail
from .models import Notification, User
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

app = Celery('your_project_name')

app.conf.beat_schedule = {
    'send-unseen-notifications-email-every-hour': {
        'task': 'capstone.tasks.send_unseen_notifications_email',
        'schedule': crontab(minute=0, hour='*'),  # Runs every hour
    },
}
@shared_task
def send_unseen_notifications_email():
    users_with_unseen_notifications = set(
        Notification.objects.filter(is_seen=False).values_list('user__email', flat=True)
    )

    for email in users_with_unseen_notifications:
        user = User.objects.get(email=email)
        send_mail(
            'You Have New Notifications on Hustle Platform!',
            f'Hi {user.full_name},\n\nYou have unread notifications. Log in to check them now!\n\nBest,\nHustle Platform Team',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
