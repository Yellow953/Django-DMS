from rest_framework import generics, filters
from schemas.models import DataEntry
from .serializers import DataEntrySerializer

class DataEntryListView(generics.ListCreateAPIView):
    serializer_class = DataEntrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['data']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = DataEntry.objects.filter(schema_id=schema_id)
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(data__icontains=search_term)
            
        return queryset