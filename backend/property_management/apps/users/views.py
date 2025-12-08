from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)

from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from utils.email_utils import EmailNotificationService


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Allow any user to create an account, but require admin access for listing users.
        """
        if self.request.method == 'POST':
            # Allow anyone to create a user account
            return [permissions.AllowAny()]
        else:
            # Only admin users can list users
            return [permissions.IsAuthenticated(), IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        # Let the serializer handle setting role and is_approved
        user = serializer.save()
        
        # Send notification to admin about new user registration
        try:
            EmailNotificationService.send_user_registration_notification(user)
        except Exception as e:
            logger.error(f"Failed to send registration notification: {str(e)}")
        
        return user


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Override update to send notification when user is approved
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Check if is_approved is being changed to True
        old_is_approved = instance.is_approved
        new_is_approved = request.data.get('is_approved', old_is_approved)
        
        self.perform_update(serializer)
        
        # If user was just approved, send notification
        if not old_is_approved and new_is_approved:
            try:
                EmailNotificationService.send_user_approval_notification(instance)
            except Exception as e:
                logger.error(f"Failed to send approval notification: {str(e)}")
        
        return Response(serializer.data)


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if user is approved
            if not user.is_approved:
                return Response({'error': 'Account pending approval by administrator'}, status=403)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            token = request.user.auth_token
            token.delete()
            return Response({'message': 'Logged out successfully'})
        except Token.DoesNotExist:
            logger.warning(f"Logout attempt failed for user {request.user.id}: No auth token found")
            return Response({'message': 'Already logged out'}, status=200)
        except Exception as e:
            logger.error(f"Logout error for user {request.user.id}: {str(e)}")
            return Response({'error': 'Error logging out'}, status=500)