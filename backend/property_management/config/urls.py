"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403, handler400
from utils.health_check import health_check, simple_health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/properties/', include('apps.properties.urls')),
    path('api/units/', include('apps.units.urls')),
    path('api/tenants/', include('apps.tenants.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/admin-module/', include('modules.admin.urls')),
    path('api/property-owner-module/', include('modules.property_owner.urls')),
    # Health check endpoints
    path('api/health/', health_check, name='health_check'),
    path('api/health/simple/', simple_health_check, name='simple_health_check'),
]

# Custom error handlers
handler404 = 'utils.error_handlers.custom_page_not_found'
handler500 = 'utils.error_handlers.custom_server_error'
handler403 = 'utils.error_handlers.custom_permission_denied'
handler400 = 'utils.error_handlers.custom_bad_request'