import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'property_management'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def update_admin_user():
    try:
        # Get the admin user
        admin = User.objects.get(username='admin')
        print(f"Found admin user: {admin.username}")
        print(f"Current role: {admin.role}")
        print(f"Current approval status: {admin.is_approved}")
        
        # Update the admin user
        admin.role = 'admin'
        admin.is_approved = True
        admin.save()
        
        print("Updated admin user successfully!")
        print(f"New role: {admin.role}")
        print(f"New approval status: {admin.is_approved}")
        
    except User.DoesNotExist:
        print("Admin user not found!")
    except Exception as e:
        print(f"Error updating admin user: {e}")

if __name__ == '__main__':
    update_admin_user()