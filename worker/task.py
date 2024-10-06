# task.py
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject: str, message: str, email_from: str, recipient_list: list) -> None:
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
