"""Calculator engine for basic arithmetic operations.

Provides four functions:
- add(a, b): Return the sum of a and b.
- subtract(a, b): Return the difference of a and b (a - b).
- multiply(a, b): Return the product of a and b.
- divide(a, b): Return the quotient of a divided by b. Raises
  ZeroDivisionError if b is zero.

All functions accept int or float and return a float for consistency.
"""

from __future__ import annotations

from typing import Union

Number = Union[int, float]

__all__ = ["add", "subtract", "multiply", "divide"]


def _to_float(value: Number) -> float:
    """Convert a numeric value to float, preserving NaN and infinities."""
    return float(value)


def add(a: Number, b: Number) -> float:
    """Return the sum of *a* and *b*.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        The arithmetic sum as a float.
    """
    return _to_float(a) + _to_float(b)


def subtract(a: Number, b: Number) -> float:
    """Return the difference of *a* minus *b*.

    Args:
        a: Minuend.
        b: Subtrahend.

    Returns:
        The arithmetic difference as a float.
    """
    return _to_float(a) - _to_float(b)


def multiply(a: Number, b: Number) -> float:
    """Return the product of *a* and *b*.

    Args:
        a: First factor.
        b: Second factor.

    Returns:
        The arithmetic product as a float.
    """
    return _to_float(a) * _to_float(b)


def divide(a: Number, b: Number) -> float:
    """Return the quotient of *a* divided by *b*.

    Args:
        a: Dividend.
        b: Divisor.

    Raises:
        ZeroDivisionError: If *b* is zero.

    Returns:
        The arithmetic quotient as a float.
    """
    divisor = _to_float(b)
    if divisor == 0.0:
        raise ZeroDivisionError("Division by zero is undefined.")
    return _to_float(a) / divisor