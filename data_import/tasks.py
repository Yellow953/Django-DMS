import csv
from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from schemas.models import DynamicSchema, DataEntry, SchemaField

def validate_csv_row(row, schema):
    errors = []
    for field in schema.fields.all():
        value = row.get(field.name)
        
        if field.required and not value:
            errors.append(f"{field.name}: Required")
            continue
        
        if not value and not field.required:
            continue
        
        try:
            if field.field_type == 'text':
                if not isinstance(value, str):
                    raise ValueError("Must be text")
                    
            elif field.field_type == 'number':
                float(value)
                
            elif field.field_type == 'date':
                datetime.strptime(value, '%Y-%m-%d')
                
            elif field.field_type == 'boolean':
                if value.lower() not in ['true', 'false', '1', '0']:
                    raise ValueError("Use true/false, 1/0")
                
        except (ValueError, TypeError, AttributeError) as e:
            errors.append(f"{field.name}: Invalid {field.field_type} ({str(e)})")
        
        if field.unique:
            exists = DataEntry.objects.filter(
                schema=schema,
                data__contains={field.name: value}
            ).exists()
            if exists:
                errors.append(f"{field.name}: Must be unique")
    
    if errors:
        raise ValidationError(errors)

@shared_task
def process_csv_import(schema_id, csv_path, user_email):
    schema = DynamicSchema.objects.get(id=schema_id)
    errors = []
    success_count = 0

    try:
        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row_number, row in enumerate(reader, start=1):
                try:
                    validate_csv_row(row, schema)
                    DataEntry.objects.create(schema=schema, data=row)
                    success_count += 1
                except ValidationError as e:
                    errors.append({
                        "row": row_number,
                        "errors": e.messages,
                        "data": row 
                    })

        subject = "CSV Import Report"
        error_list = "\n".join(
            [f"Row {e['row']}: {', '.join(e['errors'])}" for e in errors[:10]]  
        )
        message = (
            f"Imported {success_count} rows successfully.\n"
            f"Errors ({len(errors)}):\n{error_list}"
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
            "CSV Import Failed",
            f"Critical error: {str(e)}",
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )
        raise