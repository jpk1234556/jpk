from django.urls import path
from .views.dashboard_views import AdminDashboardStatsView
from .views.reports_views import AdminReportsView
from .views.settings_views import AdminSettingsView

app_name = 'admin_module'

urlpatterns = [
    path('dashboard-stats/', AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
    path('reports/', AdminReportsView.as_view(), name='admin-reports'),
    path('settings/', AdminSettingsView.as_view(), name='admin-settings'),
]