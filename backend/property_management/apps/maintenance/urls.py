from django.urls import path
from .views import MaintenanceRequestListCreateView, MaintenanceRequestDetailView

urlpatterns = [
    path('', MaintenanceRequestListCreateView.as_view(), name='maintenance-request-list-create'),
    path('<int:pk>/', MaintenanceRequestDetailView.as_view(), name='maintenance-request-detail'),
]