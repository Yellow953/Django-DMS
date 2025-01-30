from rest_framework import serializers
from schemas.models import DataEntry

class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEntry
        fields = ['id', 'schema', 'data', 'created_at']
        read_only_fields = ['schema', 'created_at']