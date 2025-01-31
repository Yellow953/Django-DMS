from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import DynamicSchema, SchemaField
from .serializers import (
    DynamicSchemaSerializer,
    SchemaFieldSerializer
)

class SchemaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = DynamicSchema.objects.all()
    serializer_class = DynamicSchemaSerializer

class SchemaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = DynamicSchema.objects.all()
    serializer_class = DynamicSchemaSerializer

class SchemaFieldCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SchemaField.objects.all()
    serializer_class = SchemaFieldSerializer

    def perform_create(self, serializer):
        schema_id = self.kwargs['schema_id']
        schema = DynamicSchema.objects.get(id=schema_id)
        serializer.save(schema=schema)

class SchemaFieldUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SchemaField.objects.all()
    serializer_class = SchemaFieldSerializer