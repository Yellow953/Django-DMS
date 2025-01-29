from rest_framework import viewsets
from .models import Table, Field
from .serializers import TableSerializer, FieldSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=['post'])
    def add_field(self, request, pk=None):
        table = self.get_object()
        field_data = request.data.copy()
        field_data['table'] = table.id

        serializer = FieldSerializer(data=field_data)
        if serializer.is_valid():
            serializer.save(table=table)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def delete_field(self, request, pk=None):
        table = self.get_object()
        field_id = request.data.get('field_id')
        try:
            field = Field.objects.get(id=field_id, table=table)
            field.delete()
            return Response(status=204)
        except Field.DoesNotExist:
            return Response({"detail": "Field not found."}, status=404)
