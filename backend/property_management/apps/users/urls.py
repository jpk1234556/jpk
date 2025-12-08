from django.urls import path
from .views import UserListCreateView, UserDetailView, LoginView, LogoutView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]