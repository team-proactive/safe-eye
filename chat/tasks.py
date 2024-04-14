from celery import shared_task
from .models import Message


@shared_task
def send_alarm(message_id):
    message = Message.objects.get(id=message_id)


@shared_task
def process_media_mention(message_id):
    message = Message.objects.get(id=message_id)
