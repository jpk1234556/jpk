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


class PropertyOwnerReportsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is property owner
        if not (hasattr(request.user, 'role') and request.user.role == 'property_owner'):
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
        
        # Validate property ownership if property_id is specified
        if property_id:
            try:
                property_obj = Property.objects.get(id=property_id, owner=request.user)
            except Property.DoesNotExist:
                return Response({'error': 'Property not found or access denied'}, status=403)
        
        # Generate report based on type
        if report_type == 'income':
            data = self.generate_income_report(request.user, start_date, end_date, property_id)
        elif report_type == 'occupancy':
            data = self.generate_occupancy_report(request.user, start_date, end_date, property_id)
        elif report_type == 'maintenance':
            data = self.generate_maintenance_report(request.user, start_date, end_date, property_id)
        elif report_type == 'tenants':
            data = self.generate_tenant_report(request.user, start_date, end_date, property_id)
        else:
            data = self.generate_summary_report(request.user)
        
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
        
        # Validate property ownership if property_id is specified
        if property_id:
            try:
                property_obj = Property.objects.get(id=property_id, owner=request.user)
            except Property.DoesNotExist:
                return Response({'error': 'Property not found or access denied'}, status=403)
        
        # Generate report data
        if report_type == 'income':
            data = self.generate_income_report(request.user, start_date, end_date, property_id)
        elif report_type == 'occupancy':
            data = self.generate_occupancy_report(request.user, start_date, end_date, property_id)
        elif report_type == 'maintenance':
            data = self.generate_maintenance_report(request.user, start_date, end_date, property_id)
        elif report_type == 'tenants':
            data = self.generate_tenant_report(request.user, start_date, end_date, property_id)
        else:
            data = self.generate_summary_report(request.user)
        
        if export_format.lower() == 'csv':
            return self.export_to_csv(data, report_type, request.user)
        else:
            return Response({'error': 'Unsupported export format'}, status=400)
    
    def export_to_csv(self, data, report_type, user):
        """Export data to CSV format"""
        # Create a StringIO object to hold CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write CSV based on report type
        if report_type == 'income':
            # Write headers
            writer.writerow(['Property', 'Amount'])
            
            # Write data
            if 'property_income' in data:
                for item in data['property_income']:
                    writer.writerow([item['property'], item['amount']])
            
            filename = 'income_report.csv'
        elif report_type == 'occupancy':
            # Write headers
            writer.writerow(['Property', 'Total Units', 'Occupied Units', 'Occupancy Rate'])
            
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
            writer.writerow(['Property', 'Unit', 'Title', 'Status', 'Priority', 'Date Submitted'])
            
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
            writer.writerow(['Property', 'Tenant Name', 'Unit', 'Lease End', 'Created At'])
            
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
            writer.writerow(['Total Properties', data.get('total_properties', 0)])
            writer.writerow(['Total Units', data.get('total_units', 0)])
            writer.writerow(['Occupied Units', data.get('occupied_units', 0)])
            writer.writerow(['Total Income (30 days)', data.get('total_income_30_days', 0)])
            writer.writerow(['Total Maintenance Requests', data.get('total_maintenance_requests', 0)])
            filename = 'summary_report.csv'
        
        # Create HTTP response with CSV data
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    def generate_summary_report(self, user):
        """Generate summary statistics for the property owner dashboard"""
        # Get properties owned by this user
        properties = Property.objects.filter(owner=user)
        
        # Total properties
        total_properties = properties.count()
        
        # Total units
        total_units = Unit.objects.filter(property__owner=user).count()
        
        # Occupied units
        occupied_units = Unit.objects.filter(
            property__owner=user,
            tenants__isnull=False
        ).distinct().count()
        
        # Total income (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        total_income = Payment.objects.filter(
            tenant__unit__property__owner=user,
            payment_date__gte=thirty_days_ago.date()
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Maintenance requests
        total_maintenance = MaintenanceRequest.objects.filter(
            unit__property__owner=user
        ).count()
        
        return {
            'total_properties': total_properties,
            'total_units': total_units,
            'occupied_units': occupied_units,
            'total_income_30_days': float(total_income),
            'total_maintenance_requests': total_maintenance
        }
    
    def generate_income_report(self, user, start_date=None, end_date=None, property_id=None):
        """Generate income report for property owner"""
        # Filter payments by property owner
        payments = Payment.objects.filter(tenant__unit__property__owner=user)
        
        if start_date:
            payments = payments.filter(payment_date__gte=start_date)
        
        if end_date:
            payments = payments.filter(payment_date__lte=end_date)
        
        if property_id:
            payments = payments.filter(tenant__unit__property_id=property_id)
        
        # Calculate total income
        total_income = payments.aggregate(total=Sum('amount'))['total'] or 0
        
        # Group by property
        property_income = payments.values(
            'tenant__unit__property__name'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        # Group by month for trend data
        monthly_income = payments.extra(
            select={'month': "strftime('%%Y-%%m', payment_date)"}
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Recent payments
        recent_payments = payments.order_by('-payment_date')[:10]
        
        return {
            'report_type': 'income',
            'total_income': float(total_income),
            'property_income': [
                {
                    'property': item['tenant__unit__property__name'],
                    'amount': float(item['total'])
                }
                for item in property_income
            ],
            'monthly_income': [
                {
                    'month': item['month'],
                    'amount': float(item['total'])
                }
                for item in monthly_income
            ],
            'recent_payments': [
                {
                    'id': payment.id,
                    'tenant': f"{payment.tenant.first_name} {payment.tenant.last_name}",
                    'property': payment.tenant.unit.property.name,
                    'unit': payment.tenant.unit.unit_number,
                    'amount': float(payment.amount),
                    'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
                    'method': payment.payment_method or 'N/A'
                }
                for payment in recent_payments
            ]
        }
    
    def generate_occupancy_report(self, user, start_date=None, end_date=None, property_id=None):
        """Generate occupancy report for property owner"""
        # Get properties owned by this user
        properties = Property.objects.filter(owner=user)
        
        if property_id:
            properties = properties.filter(id=property_id)
        
        occupancy_data = []
        total_units = 0
        occupied_units = 0
        
        for property_obj in properties:
            # Get units for this property
            units = Unit.objects.filter(property=property_obj)
            total_property_units = units.count()
            
            # Count occupied units (units with tenants)
            occupied_property_units = units.filter(
                tenants__isnull=False
            ).distinct().count()
            
            total_units += total_property_units
            occupied_units += occupied_property_units
            
            if total_property_units > 0:
                occupancy_rate = (occupied_property_units / total_property_units) * 100
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
    
    def generate_maintenance_report(self, user, start_date=None, end_date=None, property_id=None):
        """Generate maintenance report for property owner"""
        # Filter maintenance requests by property owner
        maintenance_requests = MaintenanceRequest.objects.filter(
            unit__property__owner=user
        )
        
        if start_date:
            maintenance_requests = maintenance_requests.filter(created_at__date__gte=start_date)
        
        if end_date:
            maintenance_requests = maintenance_requests.filter(created_at__date__lte=end_date)
        
        if property_id:
            maintenance_requests = maintenance_requests.filter(unit__property_id=property_id)
        
        # Count by status
        status_counts = maintenance_requests.values('status').annotate(
            count=Count('id')
        )
        
        # Count by priority
        priority_counts = maintenance_requests.values('priority').annotate(
            count=Count('id')
        )
        
        # Recent requests
        recent_requests = maintenance_requests.order_by('-created_at')[:10]
        
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
    
    def generate_tenant_report(self, user, start_date=None, end_date=None, property_id=None):
        """Generate tenant report for property owner"""
        # Filter tenants by property owner
        tenants = Tenant.objects.filter(unit__property__owner=user)
        
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
        
        # Recent tenants
        recent_tenants = tenants.order_by('-created_at')[:10]
        
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