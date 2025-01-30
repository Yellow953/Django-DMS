from rest_framework import generics, filters
from schemas.models import DataEntry
from .serializers import DataEntrySerializer

class DataEntryListView(generics.ListCreateAPIView):
    serializer_class = DataEntrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['data']
    ordering_fields = ['created_at']

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        return DataEntry.objects.filter(schema_id=schema_id)