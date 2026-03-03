"""
Custom exception handler for consistent API error responses.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error response format.
    
    Format:
    {
        "error": "Human-readable error message",
        "detail": { ... original error details ... }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Log server errors
        if response.status_code >= 500:
            logger.error(
                "Server error in %s: %s",
                context.get('view', 'unknown'),
                exc,
                exc_info=True,
            )
        elif response.status_code >= 400:
            logger.warning(
                "Client error %d in %s: %s",
                response.status_code,
                context.get('view', 'unknown'),
                response.data,
            )

        # Wrap the response in a consistent format
        custom_data = {
            'error': _get_error_message(response),
            'detail': response.data,
        }
        response.data = custom_data

    return response


def _get_error_message(response):
    """Extract a human-readable error message from the DRF response."""
    if isinstance(response.data, dict):
        if 'detail' in response.data:
            return str(response.data['detail'])
        # Collect field errors into a single message
        messages = []
        for field, errors in response.data.items():
            if isinstance(errors, list):
                messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
            else:
                messages.append(f"{field}: {errors}")
        return '; '.join(messages) if messages else 'An error occurred.'
    return str(response.data)
