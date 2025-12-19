from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from apps.properties.models import Property
from apps.units.models import Unit
from apps.tenants.models import Tenant
from apps.payments.models import Payment
from apps.maintenance.models import MaintenanceRequest
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
import csv
import io
from django.http import HttpResponse
from django.core.cache import cache


class AdminReportsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Check if user is admin
        if not (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return Response({'error': 'Access denied'}, status=403)

        # Check if export is requested
        export_format = request.GET.get('export', None)
        if export_format:
            return self.export_report(request, export_format)

        # Get query parameters
        report_type = request.GET.get('type', 'summary')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        property_id = request.GET.get('property_id')

        # Parse dates if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = None

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                end_date = None

        # Create cache key based on parameters
        cache_key = f"admin_report_{report_type}_{start_date}_{end_date}_{property_id}_{request.user.id}"
        
        # Try to get data from cache first
        data = cache.get(cache_key)
        
        if data is None:
            # Generate report based on type
            if report_type == 'revenue':
                data = self.generate_revenue_report(
                    start_date, end_date, property_id)
            elif report_type == 'occupancy':
                data = self.generate_occupancy_report(
                    start_date, end_date, property_id)
            elif report_type == 'maintenance':
                data = self.generate_maintenance_report(
                    start_date, end_date, property_id)
            elif report_type == 'tenants':
                data = self.generate_tenant_report(
                    start_date, end_date, property_id)
            else:
                data = self.generate_summary_report()
            
            # Cache for 5 minutes (300 seconds)
            cache.set(cache_key, data, 300)

        return Response(data)

    def export_report(self, request, export_format):
        """Export report data in specified format (CSV)"""
        report_type = request.GET.get('type', 'summary')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        property_id = request.GET.get('property_id')

        # Parse dates if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = None

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                end_date = None

        # Generate report data
        if report_type == 'revenue':
            data = self.generate_revenue_report(
                start_date, end_date, property_id)
        elif report_type == 'occupancy':
            data = self.generate_occupancy_report(
                start_date, end_date, property_id)
        elif report_type == 'maintenance':
            data = self.generate_maintenance_report(
                start_date, end_date, property_id)
        elif report_type == 'tenants':
            data = self.generate_tenant_report(
                start_date, end_date, property_id)
        else:
            data = self.generate_summary_report()

        if export_format.lower() == 'csv':
            return self.export_to_csv(data, report_type)
        else:
            return Response({'error': 'Unsupported export format'}, status=400)

    def export_to_csv(self, data, report_type):
        """Export data to CSV format"""
        # Create a StringIO object to hold CSV data
        output = io.StringIO()
        writer = csv.writer(output)

        # Write CSV based on report type
        if report_type == 'revenue':
            # Write headers
            writer.writerow(['Property', 'Amount'])

            # Write data
            if 'property_revenue' in data:
                for item in data['property_revenue']:
                    writer.writerow([item['property'], item['amount']])

            filename = 'revenue_report.csv'
        elif report_type == 'occupancy':
            # Write headers
            writer.writerow(['Property', 'Total Units',
                            'Occupied Units', 'Occupancy Rate'])

            # Write data
            if 'property_occupancy' in data:
                for item in data['property_occupancy']:
                    writer.writerow([
                        item['property'],
                        item['total_units'],
                        item['occupied_units'],
                        f"{item['occupancy_rate']}%"
                    ])

            filename = 'occupancy_report.csv'
        elif report_type == 'maintenance':
            # Write headers
            writer.writerow(['Property', 'Unit', 'Title',
                            'Status', 'Priority', 'Date Submitted'])

            # Write data
            if 'recent_requests' in data:
                for item in data['recent_requests']:
                    writer.writerow([
                        item['property'],
                        item['unit'],
                        item['title'],
                        item['status'],
                        item['priority'],
                        item['created_at']
                    ])

            filename = 'maintenance_report.csv'
        elif report_type == 'tenants':
            # Write headers
            writer.writerow(['Property', 'Tenant Name',
                            'Unit', 'Lease End', 'Created At'])

            # Write data
            if 'recent_tenants' in data:
                for item in data['recent_tenants']:
                    writer.writerow([
                        item['property'],
                        item['name'],
                        item['unit'],
                        item['lease_end'] or '',
                        item['created_at']
                    ])

            filename = 'tenants_report.csv'
        else:
            # Default export for summary
            writer.writerow(['Metric', 'Value'])
            writer.writerow(
                ['Total Properties', data.get('total_properties', 0)])
            writer.writerow(['Total Owners', data.get('total_owners', 0)])
            writer.writerow(['Total Tenants', data.get('total_tenants', 0)])
            writer.writerow(['Total Revenue (30 days)',
                            data.get('total_revenue_30_days', 0)])
            writer.writerow(['Total Maintenance Requests',
                            data.get('total_maintenance_requests', 0)])
            writer.writerow(['Pending Maintenance Requests',
                            data.get('pending_maintenance_requests', 0)])
            filename = 'summary_report.csv'

        # Create HTTP response with CSV data
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    def generate_summary_report(self):
        """Generate summary statistics for the admin dashboard"""
        # Total properties with optimized query
        total_properties = Property.objects.count()
            
        # Total property owners with optimized query
        total_owners = Property.objects.values('owner').distinct().count()
            
        # Total tenants with optimized query
        total_tenants = Tenant.objects.count()
            
        # Total revenue (last 30 days) with optimized query
        thirty_days_ago = timezone.now() - timedelta(days=30)
        total_revenue = Payment.objects.filter(
            payment_date__gte=thirty_days_ago.date()
        ).select_related('tenant__unit__property').aggregate(total=Sum('amount'))['total'] or 0
            
        # Maintenance requests with optimized query
        total_maintenance = MaintenanceRequest.objects.count()
        pending_maintenance = MaintenanceRequest.objects.filter(
            status='pending'
        ).select_related('unit__property').count()
            
        return {
            'total_properties': total_properties,
            'total_owners': total_owners,
            'total_tenants': total_tenants,
            'total_revenue_30_days': float(total_revenue),
            'total_maintenance_requests': total_maintenance,
            'pending_maintenance_requests': pending_maintenance
        }

    def generate_revenue_report(self, start_date=None, end_date=None, property_id=None):
        """Generate revenue report"""
        # Filter payments by date range with related data
        payments = Payment.objects.all().select_related(
            'tenant__unit__property'
        )
            
        if start_date:
            payments = payments.filter(payment_date__gte=start_date)
            
        if end_date:
            payments = payments.filter(payment_date__lte=end_date)
            
        if property_id:
            payments = payments.filter(tenant__unit__property_id=property_id)
            
        # Calculate total revenue
        total_revenue = payments.aggregate(total=Sum('amount'))['total'] or 0
            
        # Group by property
        property_revenue = payments.values(
            'tenant__unit__property__name'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
            
        # Group by month for trend data
        monthly_revenue = payments.extra(
            select={'month': "strftime('%%Y-%%m', payment_date)"}
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
            
        return {
            'report_type': 'revenue',
            'total_revenue': float(total_revenue),
            'property_revenue': [
                {
                    'property': item['tenant__unit__property__name'],
                    'amount': float(item['total'])
                }
                for item in property_revenue
            ],
            'monthly_revenue': [
                {
                    'month': item['month'],
                    'amount': float(item['total'])
                }
                for item in monthly_revenue
            ]
        }

    def generate_occupancy_report(self, start_date=None, end_date=None, property_id=None):
        """Generate occupancy report"""
        # Get all properties with related data
        properties = Property.objects.all().prefetch_related(
            'units'
        )
            
        if property_id:
            properties = properties.filter(id=property_id)
            
        occupancy_data = []
        total_units = 0
        occupied_units = 0
            
        for property_obj in properties:
            # Get units for this property with related data
            units = Unit.objects.filter(property=property_obj).select_related(
                'property'
            )
            total_property_units = units.count()
                
            # Count occupied units (using status field instead of tenant check)
            occupied_property_units = units.filter(
                status='occupied'
            ).count()
                
            total_units += total_property_units
            occupied_units += occupied_property_units
                
            if total_property_units > 0:
                occupancy_rate = (occupied_property_units /
                                  total_property_units) * 100
            else:
                occupancy_rate = 0
                
            occupancy_data.append({
                'property': property_obj.name,
                'total_units': total_property_units,
                'occupied_units': occupied_property_units,
                'occupancy_rate': round(occupancy_rate, 2)
            })
            
        # Calculate overall occupancy rate
        if total_units > 0:
            overall_occupancy = (occupied_units / total_units) * 100
        else:
            overall_occupancy = 0
            
        return {
            'report_type': 'occupancy',
            'overall_occupancy_rate': round(overall_occupancy, 2),
            'total_units': total_units,
            'occupied_units': occupied_units,
            'property_occupancy': occupancy_data
        }

    def generate_maintenance_report(self, start_date=None, end_date=None, property_id=None):
        """Generate maintenance report"""
        # Filter maintenance requests by date range with related data
        maintenance_requests = MaintenanceRequest.objects.all().select_related(
            'unit__property'
        )
            
        if start_date:
            maintenance_requests = maintenance_requests.filter(
                created_at__date__gte=start_date)
            
        if end_date:
            maintenance_requests = maintenance_requests.filter(
                created_at__date__lte=end_date)
            
        if property_id:
            maintenance_requests = maintenance_requests.filter(
                unit__property_id=property_id)
            
        # Count by status
        status_counts = maintenance_requests.values('status').annotate(
            count=Count('id')
        )
            
        # Count by priority
        priority_counts = maintenance_requests.values('priority').annotate(
            count=Count('id')
        )
            
        # Recent requests with related data
        recent_requests = maintenance_requests.select_related(
            'unit__property'
        ).order_by('-created_at')[:10]
            
        return {
            'report_type': 'maintenance',
            'total_requests': maintenance_requests.count(),
            'status_breakdown': {
                item['status']: item['count']
                for item in status_counts
            },
            'priority_breakdown': {
                item['priority']: item['count']
                for item in priority_counts
            },
            'recent_requests': [
                {
                    'id': req.id,
                    'property': req.unit.property.name,
                    'unit': req.unit.unit_number,
                    'title': req.title,
                    'status': req.status,
                    'priority': req.priority,
                    'created_at': req.created_at.strftime('%Y-%m-%d')
                }
                for req in recent_requests
            ]
        }

    def generate_tenant_report(self, start_date=None, end_date=None, property_id=None):
        """Generate tenant report"""
        # Filter tenants by property with related data
        tenants = Tenant.objects.all().select_related(
            'unit__property'
        )
            
        if property_id:
            tenants = tenants.filter(unit__property_id=property_id)
            
        # Count active vs expired leases
        today = timezone.now().date()
        active_tenants = tenants.filter(
            lease_start__lte=today,
            lease_end__gte=today
        ).count()
            
        expired_tenants = tenants.filter(
            lease_end__lt=today
        ).count()
            
        # Group by property
        property_tenants = tenants.values(
            'unit__property__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
            
        # Recent tenants with related data
        recent_tenants = tenants.select_related(
            'unit__property'
        ).order_by('-created_at')[:10]
            
        return {
            'report_type': 'tenants',
            'total_tenants': tenants.count(),
            'active_tenants': active_tenants,
            'expired_tenants': expired_tenants,
            'property_breakdown': [
                {
                    'property': item['unit__property__name'],
                    'tenant_count': item['count']
                }
                for item in property_tenants
            ],
            'recent_tenants': [
                {
                    'id': tenant.id,
                    'name': f"{tenant.first_name} {tenant.last_name}",
                    'property': tenant.unit.property.name,
                    'unit': tenant.unit.unit_number,
                    'lease_end': tenant.lease_end.strftime('%Y-%m-%d') if tenant.lease_end else None,
                    'created_at': tenant.created_at.strftime('%Y-%m-%d')
                }
                for tenant in recent_tenants
            ]
        }
