"""
Session utility for managing calculator state across anonymous and authenticated sessions.

Provides consistent key names and safe operations for reading/writing/deleting
calculator inputs in Django sessions.
"""

from typing import Any

from django.http import HttpRequest

# Session key prefix for calculator inputs
CALCULATOR_SESSION_PREFIX = "calc_inputs_"


def get_calculator_session_key(calculator_type: str) -> str:
    """
    Generate session key for a specific calculator type.

    Args:
        calculator_type: Type of calculator (e.g., "distance", "cost", "time")

    Returns:
        Session key string
    """
    return f"{CALCULATOR_SESSION_PREFIX}{calculator_type}"


def get_calculator_inputs(request: HttpRequest, calculator_type: str) -> dict[str, Any] | None:
    """
    Safely retrieve calculator inputs from session.

    Args:
        request: Django HTTP request with session
        calculator_type: Type of calculator

    Returns:
        Dictionary of inputs or None if not found
    """
    key = get_calculator_session_key(calculator_type)
    return request.session.get(key)  # type: ignore[attr-defined]


def set_calculator_inputs(request: HttpRequest, calculator_type: str, inputs: dict[str, Any]) -> None:
    """
    Store calculator inputs in session.

    Args:
        request: Django HTTP request with session
        calculator_type: Type of calculator
        inputs: Dictionary of input values to store
    """
    key = get_calculator_session_key(calculator_type)
    request.session[key] = inputs  # type: ignore[attr-defined]
    request.session.modified = True  # type: ignore[attr-defined]


def clear_calculator_inputs(request: HttpRequest, calculator_type: str) -> None:
    """
    Remove calculator inputs from session.

    Args:
        request: Django HTTP request with session
        calculator_type: Type of calculator
    """
    key = get_calculator_session_key(calculator_type)
    if key in request.session:  # type: ignore[attr-defined]
        del request.session[key]  # type: ignore[attr-defined]
        request.session.modified = True  # type: ignore[attr-defined]


def get_all_calculator_inputs(request: HttpRequest) -> dict[str, dict[str, Any]]:
    """
    Retrieve all calculator inputs from session.

    Returns:
        Dictionary mapping calculator_type to inputs dict
    """
    result = {}
    for key in request.session.keys():  # type: ignore[attr-defined]
        if key.startswith(CALCULATOR_SESSION_PREFIX):
            calculator_type = key[len(CALCULATOR_SESSION_PREFIX) :]
            result[calculator_type] = request.session[key]  # type: ignore[attr-defined]
    return result


def mark_session_as_user_bound(request: HttpRequest) -> None:
    """
    Mark session as belonging to an authenticated user.

    This is called after login to indicate that any calculator inputs
    in the session are now associated with the logged-in user.
    """
    request.session["user_bound"] = True  # type: ignore[attr-defined]
    request.session.modified = True  # type: ignore[attr-defined]


def is_session_user_bound(request: HttpRequest) -> bool:
    """
    Check if session is marked as user-bound.

    Returns:
        True if session belongs to authenticated user
    """
    return request.session.get("user_bound", False)  # type: ignore[attr-defined]
