from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from schemas.models import DataEntry, DynamicSchema
from .serializers import DataEntrySerializer
from .tasks import process_csv_import
from django.core.files.storage import default_storage

class DataEntryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataEntrySerializer

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        return DataEntry.objects.filter(schema_id=schema_id)

    def perform_create(self, serializer):
        schema_id = self.kwargs['schema_id']
        schema = DynamicSchema.objects.get(id=schema_id)
        serializer.save(schema=schema)

class DataEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataEntrySerializer

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        return DataEntry.objects.filter(schema_id=schema_id)

class DataImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, schema_id):
        csv_file = request.FILES.get('file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return Response(
                {"error": "Invalid or missing CSV file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            file_path = default_storage.save(f'tmp/{csv_file.name}', csv_file)
            
            process_csv_import.delay(
                schema_id=schema_id,
                csv_path=default_storage.path(file_path), 
                user_email=request.user.email
            )

            return Response(
                {"status": "Import started", "task_id": process_csv_import.request.id},
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )