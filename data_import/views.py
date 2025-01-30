from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from schemas.models import DataEntry, DynamicSchema
from .serializers import DataEntrySerializer
from .tasks import process_csv_import

class DataEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = DataEntrySerializer

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        return DataEntry.objects.filter(schema_id=schema_id)

    def perform_create(self, serializer):
        schema_id = self.kwargs['schema_id']
        schema = DynamicSchema.objects.get(id=schema_id)
        serializer.save(schema=schema)

class DataEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataEntrySerializer

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        return DataEntry.objects.filter(schema_id=schema_id)

class DataImportView(generics.CreateAPIView):
    parser_classes = [MultiPartParser]

    def post(self, request, schema_id):
        csv_file = request.FILES.get('file')
        user_email = request.user.email 

        if not csv_file:
            return Response({"error": "No CSV file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        process_csv_import.delay(schema_id, csv_file.temporary_file_path(), user_email)

        return Response({"status": "Import started"}, status=status.HTTP_202_ACCEPTED)