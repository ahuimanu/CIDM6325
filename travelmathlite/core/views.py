"""Core application views.

Implements health check and operational endpoints per ADR-1.0.9.
"""

import os

from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for monitoring and load balancers.

    Returns HTTP 200 with JSON status. Optionally includes X-Commit-SHA
    header when LOG_COMMIT_SHA environment variable is set.

    This endpoint is designed to remain accessible even if middleware
    encounters issues, providing a basic liveness check.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse with {"status": "ok"} and HTTP 200.
    """
    response = JsonResponse({"status": "ok"})

    # Add commit SHA header if configured
    commit_sha = os.getenv("LOG_COMMIT_SHA")
    if commit_sha:
        response["X-Commit-SHA"] = commit_sha

    return response
