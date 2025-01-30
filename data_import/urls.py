from django.urls import path
from .views import (
    DataEntryListCreateView,
    DataEntryRetrieveUpdateDestroyView,
    DataImportView
)

urlpatterns = [
    path('<int:schema_id>/entries/', DataEntryListCreateView.as_view(), name='dataentry-list-create'),
    path('<int:schema_id>/entries/<int:pk>/', DataEntryRetrieveUpdateDestroyView.as_view(), name='dataentry-detail'),
    
    path('<int:schema_id>/import/', DataImportView.as_view(), name='data-import'),
]