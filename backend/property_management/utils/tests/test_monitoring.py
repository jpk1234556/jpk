"""
Tests for monitoring and health check functionality.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTestCase(TestCase):
    """Test cases for health check endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_simple_health_check(self):
        """Test the simple health check endpoint."""
        url = reverse('simple_health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')

    def test_comprehensive_health_check(self):
        """Test the comprehensive health check endpoint."""
        url = reverse('health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('checks', response.data)
        self.assertIn('timestamp', response.data)