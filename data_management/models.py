from django.db import models

class Table(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Field(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255)
    is_unique = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.field_type})"
