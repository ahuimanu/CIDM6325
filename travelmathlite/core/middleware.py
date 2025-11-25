"""Middleware for request ID tracking and timing.

Implements request ID injection and duration tracking as specified in ADR-1.0.9.
Ensures every request has a unique identifier and timing information for logging.
"""

import time
import uuid
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


class RequestIDMiddleware:
    """Inject X-Request-ID and track request duration.

    This middleware:
    - Reads X-Request-ID from request headers or generates a UUID4
    - Attaches request_id to the request object for logging
    - Records start/end timestamps and calculates duration_ms
    - Adds X-Request-ID to the response headers
    - Survives exceptions to ensure duration is always available

    Invariants:
    - INV-1: request.request_id is always present (never None)
    - INV-2: request.duration_ms is logged even when exceptions occur
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with the next handler in the chain.

        Args:
            get_response: The next middleware or view to call.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process request, inject request ID, and track duration.

        Args:
            request: The incoming HTTP request.

        Returns:
            The HTTP response with X-Request-ID header added.
        """
        # Read X-Request-ID from headers or generate a new UUID4
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        # Attach request_id to request for logging (INV-1)
        request.request_id = request_id  # type: ignore[attr-defined]

        # Record start time
        start_time = time.perf_counter()

        try:
            # Process the request through the rest of the middleware chain
            response = self.get_response(request)
        finally:
            # Calculate duration even if an exception occurred (INV-2)
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000.0
            request.duration_ms = duration_ms  # type: ignore[attr-defined]

        # Add X-Request-ID to response headers
        response["X-Request-ID"] = request_id

        return response


class CacheHeaderMiddleware:
    """Add appropriate HTTP cache headers to responses.

    This middleware sets Cache-Control and Vary headers for browser/CDN caching
    as specified in ADR-1.0.10. It applies different caching strategies based on
    content type and authentication state.

    Cache strategies:
    - Static assets: Handled by WhiteNoise (public, max-age=31536000)
    - Search results: public, max-age=300, Vary: Accept, Cookie
    - Calculator results: public, max-age=600
    - Authenticated content: private, max-age=0
    - Default public content: public, max-age=300
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with the next handler in the chain.

        Args:
            get_response: The next middleware or view to call.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process request and add cache headers to response.

        Args:
            request: The incoming HTTP request.

        Returns:
            The HTTP response with Cache-Control and Vary headers added.
        """
        from django.utils.cache import patch_cache_control

        response = self.get_response(request)

        # Static files already handled by WhiteNoise - skip
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return response

        # Check if Cache-Control already exists (from @cache_page decorator)
        has_cache_control = response.has_header("Cache-Control")

        # Search results: ensure public cache and Vary headers
        if request.path.startswith("/search/"):
            if not has_cache_control:
                patch_cache_control(response, public=True, max_age=300)
            else:
                # @cache_page already set max-age, add public directive
                patch_cache_control(response, public=True)
            # Always add Vary headers for content negotiation
            response["Vary"] = "Accept, Cookie"

        # Calculator results: ensure public cache and Vary headers
        elif request.path.startswith("/calculators/"):
            if not has_cache_control:
                patch_cache_control(response, public=True, max_age=600)
            else:
                # @cache_page already set max-age, add public directive
                patch_cache_control(response, public=True)
            # Add Vary header for content negotiation
            response["Vary"] = "Accept"

        # Authenticated pages: private cache only
        elif request.user.is_authenticated and not has_cache_control:
            patch_cache_control(response, private=True, max_age=0, must_revalidate=True)

        # Default public content: cache for 5 minutes
        elif not has_cache_control:
            patch_cache_control(response, public=True, max_age=300)

        return response
