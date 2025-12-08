from django.urls import path
from .views.dashboard_views import PropertyOwnerDashboardStatsView
from .views.reports_views import PropertyOwnerReportsView

app_name = 'property_owner_module'

urlpatterns = [
    path('dashboard-stats/', PropertyOwnerDashboardStatsView.as_view(), name='property-owner-dashboard-stats'),
    path('reports/', PropertyOwnerReportsView.as_view(), name='property-owner-reports'),
]