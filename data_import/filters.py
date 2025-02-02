from django_filters import rest_framework as filters
from schemas.models import DataEntry

class DataEntryFilter(filters.FilterSet):
    data = filters.CharFilter(method='filter_data')

    class Meta:
        model = DataEntry
        fields = []

    def filter_data(self, queryset, name, value):
        schema_id = self.request.parser_context['kwargs']['schema_id']
        schema_fields = self.request.schema.fields.all()

        lookup = self.request.query_params.get('lookup', 'exact')
        field_name = name.replace('data__', '')

        if not schema_fields.filter(name=field_name).exists():
            return queryset.none()

        if lookup == 'exact':
            return queryset.filter(data__contains={field_name: value})
        elif lookup == 'contains':
            return queryset.filter(data__icontains=value)
        elif lookup == 'gt':
            return queryset.filter(data__field_name__gt=value)

        return queryset