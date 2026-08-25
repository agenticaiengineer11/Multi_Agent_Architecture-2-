import argparse
import sys
from typing import Callable

from .calculator import add, subtract, multiply, divide
from .validator import validate_number, validate_operator


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple command‑line calculator supporting +, -, *, / operations."
    )
    parser.add_argument(
        "-a",
        "--operand1",
        type=str,
        help="First numeric operand (integer or float).",
    )
    parser.add_argument(
        "-b",
        "--operand2",
        type=str,
        help="Second numeric operand (integer or float).",
    )
    parser.add_argument(
        "-o",
        "--operator",
        type=str,
        choices=["+", "-", "*", "/"],
        help="Arithmetic operator: +, -, *, /.",
    )
    return parser.parse_args()


def _interactive_prompt() -> tuple[float, float, str]:
    while True:
        try:
            raw_a = input("Enter first number: ").strip()
            a = validate_number(raw_a)
            break
        except ValueError as exc:
            print(f"Invalid input for first number: {exc}")

    while True:
        try:
            raw_b = input("Enter second number: ").strip()
            b = validate_number(raw_b)
            break
        except ValueError as exc:
            print(f"Invalid input for second number: {exc}")

    while True:
        try:
            raw_op = input("Enter operator (+, -, *, /): ").strip()
            op = validate_operator(raw_op)
            break
        except ValueError as exc:
            print(f"Invalid operator: {exc}")

    return a, b, op


def _select_operation(operator: str) -> Callable[[float, float], float]:
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    return operations[operator]


def run() -> None:
    args = _parse_arguments()

    if args.operand1 and args.operand2 and args.operator:
        try:
            operand1 = validate_number(args.operand1)
            operand2 = validate_number(args.operand2)
            operator = validate_operator(args.operator)
        except ValueError as exc:
            print(f"Input validation error: {exc}")
            sys.exit(1)
    else:
        operand1, operand2, operator = _interactive_prompt()

    operation_func = _select_operation(operator)

    try:
        result = operation_func(operand1, operand2)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        sys.exit(1)
    except Exception as exc:  # pragma: no cover
        print(f"An unexpected error occurred: {exc}")
        sys.exit(1)
    else:
        print(f"Result: {result}")


if __name__ == "__main__":
    run()