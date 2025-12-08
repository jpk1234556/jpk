from django.urls import path
from .views import UnitListCreateView, UnitDetailView

urlpatterns = [
    path('', UnitListCreateView.as_view(), name='unit-list-create'),
    path('<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
]