from django.urls import path
from src.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path("", DataColumnListView.as_view(), name='data_list'),
    path("data_detail/<int:schema_id>", DataColumnDetailView.as_view(), name='data_detail'),
    path("data_create/", DataSchemaCreateView.as_view(), name='data_create'),
    path("data_column_create/<int:data_schema_id>", DataColumnCreateView.as_view(), name='data_column_create'),
    path("data_update/<int:pk>/", DataColumnUpdateView.as_view(), name='data_update'),
    path("data_delete/<int:pk>", DataSchemaDeleteView.as_view(), name='data_delete'),
    path("data_column_delete/<int:pk>", DataColumnDeleteView.as_view(), name='data_column_delete'),
    path('data_download/<int:schema_id>/', DataSchemaDownloadView.as_view(), name='data_download'),

]
