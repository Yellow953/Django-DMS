import csv
from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from schemas.models import DynamicSchema, DataEntry, SchemaField

def validate_csv_row(row, schema):
    """
    Validate a CSV row against the schema's field definitions
    """
    errors = []
    
    for field in schema.fields.all():
        value = row.get(field.name)
        
        if field.required and not value:
            errors.append(f"{field.name} is required")
            continue
            
        try:
            if field.field_type == 'number':
                float(value)
            elif field.field_type == 'date':
                datetime.strptime(value, '%Y-%m-%d')
            elif field.field_type == 'boolean':
                if value.lower() not in ['true', 'false', '1', '0']:
                    raise ValueError()
        except (ValueError, TypeError):
            errors.append(f"{field.name}: Invalid {field.field_type} format")
            
        if field.unique and value:
            exists = DataEntry.objects.filter(
                schema=schema,
                data__contains={field.name: value}
            ).exists()
            if exists:
                errors.append(f"{field.name} must be unique")
    
    if errors:
        raise ValidationError(", ".join(errors))

@shared_task
def process_csv_import(schema_id, csv_path, user_email):
    """
    Process CSV import asynchronously
    """
    schema = DynamicSchema.objects.get(id=schema_id)
    errors = []
    success_count = 0
    entries_to_create = []

    try:
        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for i, row in enumerate(reader, start=1):
                try:
                    validate_csv_row(row, schema)
                    entries_to_create.append(
                        DataEntry(schema=schema, data=row)
                    )
                    success_count += 1
                    
                    if len(entries_to_create) >= 1000:
                        DataEntry.objects.bulk_create(entries_to_create)
                        entries_to_create = []
                        
                except ValidationError as e:
                    errors.append(f"Row {i}: {', '.join(e.messages)}")

        if entries_to_create:
            DataEntry.objects.bulk_create(entries_to_create)

        subject = "CSV Import Complete"
        message = (
            f"Successfully imported {success_count} records.\n"
            f"Errors ({len(errors)}):\n" + "\n".join(errors[:10])
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )

    except Exception as e:
        send_mail(
            subject="CSV Import Failed",
            message=f"Critical error during import: {str(e)}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )
        raise 