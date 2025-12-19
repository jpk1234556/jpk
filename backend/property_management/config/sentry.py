"""
Sentry configuration for error tracking and monitoring.
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from django.conf import settings


def init_sentry():
    """
    Initialize Sentry for error tracking.
    """
    if hasattr(settings, 'SENTRY_DSN') and settings.SENTRY_DSN:
        # Configure Sentry logging integration
        sentry_logging = LoggingIntegration(
            level=settings.LOGGING_LEVEL if hasattr(settings, 'LOGGING_LEVEL') else 'INFO',
            event_level=settings.EVENT_LEVEL if hasattr(settings, 'EVENT_LEVEL') else 'ERROR'
        )
        
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                sentry_logging,
            ],
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE if hasattr(settings, 'SENTRY_TRACES_SAMPLE_RATE') else 1.0,
            send_default_pii=True,
            environment=settings.SENTRY_ENVIRONMENT if hasattr(settings, 'SENTRY_ENVIRONMENT') else 'development',
        )