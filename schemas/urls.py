from django.urls import path
from .views import (
    SchemaListCreateView,
    SchemaRetrieveUpdateDestroyView,
    SchemaFieldCreateView,
    SchemaFieldUpdateDestroyView
)

urlpatterns = [
    path('', SchemaListCreateView.as_view(), name='schema-list-create'),
    path('<int:pk>/', SchemaRetrieveUpdateDestroyView.as_view(), name='schema-detail'),
    
    path('<int:schema_id>/fields/', SchemaFieldCreateView.as_view(), name='field-create'),
    path('<int:schema_id>/fields/<int:pk>/', SchemaFieldUpdateDestroyView.as_view(), name='field-update-delete'),
]