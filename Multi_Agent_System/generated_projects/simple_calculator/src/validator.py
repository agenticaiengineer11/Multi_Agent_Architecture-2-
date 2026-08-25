"""Validator utilities for the simple calculator.

Provides functions to validate and convert user input into the appropriate
numeric types and to ensure that the selected operator is supported.
All validation errors raise :class:`ValueError` with descriptive messages.
"""

from __future__ import annotations

from typing import Tuple

ALLOWED_OPERATORS = {"+", "-", "*", "/"}


def to_number(value: str) -> float:
    """Convert a string to a float.

    Args:
        value: The string representation of a number.

    Returns:
        The numeric value as a ``float``.

    Raises:
        ValueError: If *value* cannot be converted to a float.
    """
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value: {value!r}") from exc


def validate_operator(operator: str) -> str:
    """Validate that the operator is one of the supported symbols.

    Args:
        operator: The operator string supplied by the user.

    Returns:
        The validated operator string.

    Raises:
        ValueError: If *operator* is not among the supported operators.
    """
    if operator not in ALLOWED_OPERATORS:
        allowed = ", ".join(sorted(ALLOWED_OPERATORS))
        raise ValueError(
            f"Unsupported operator: {operator!r}. Supported operators are: {allowed}"
        )
    return operator


def validate_operands(
    left: str, right: str
) -> Tuple[float, float]:
    """Validate and convert both operand strings to floats.

    Args:
        left: The left‑hand operand as a string.
        right: The right‑hand operand as a string.

    Returns:
        A tuple ``(left_number, right_number)`` containing the converted floats.

    Raises:
        ValueError: If either operand cannot be converted to a float.
    """
    left_num = to_number(left)
    right_num = to_number(right)
    return left_num, right_num


def validate_all(
    left: str, right: str, operator: str
) -> Tuple[float, float, str]:
    """Validate the full set of user inputs.

    This helper validates the two operands and the operator, returning the
    converted numeric values together with the validated operator.

    Args:
        left: Left operand as a string.
        right: Right operand as a string.
        operator: Operator as a string.

    Returns:
        A tuple ``(left_number, right_number, operator)``.

    Raises:
        ValueError: Propagates any validation error from the underlying checks.
    """
    left_num, right_num = validate_operands(left, right)
    op = validate_operator(operator)
    return left_num, right_num, op


__all__ = [
    "ALLOWED_OPERATORS",
    "to_number",
    "validate_operator",
    "validate_operands",
    "validate_all",
]