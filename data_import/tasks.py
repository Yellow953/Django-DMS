from celery import shared_task
from django.core.mail import send_mail
from schemas.models import DataEntry

@shared_task
def process_csv_import(schema_id, csv_path, user_email):
    send_mail(
        'Import Successful',
        'Your data import has completed.',
        'noreply@example.com',
        [user_email]
    )
