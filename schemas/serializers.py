from rest_framework import serializers
from .models import DynamicSchema, SchemaField

class SchemaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaField
        fields = ['id', 'name', 'field_type', 'required', 'unique']

class DynamicSchemaSerializer(serializers.ModelSerializer):
    fields = SchemaFieldSerializer(many=True, read_only=True)
    
    class Meta:
        model = DynamicSchema
        fields = ['id', 'name', 'created_at', 'fields']