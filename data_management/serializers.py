from rest_framework import serializers
from .models import Table, Field

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'field_type', 'is_unique', 'is_required']

class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Table
        fields = ['id', 'name', 'fields']

    def create(self, validated_data):
        """Custom create method to handle nested field creation"""
        fields_data = validated_data.pop('fields', [])
        table = Table.objects.create(**validated_data)
        for field_data in fields_data:
            Field.objects.create(table=table, **field_data)
        return table
