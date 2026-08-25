import os
import sys
import unittest

# Ensure the src package is on the import path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from validator import validate_number, validate_operator


class TestValidateNumber(unittest.TestCase):
    def test_integer_string(self):
        self.assertEqual(validate_number("42"), 42.0)

    def test_negative_integer(self):
        self.assertEqual(validate_number("-7"), -7.0)

    def test_float_string(self):
        self.assertAlmostEqual(validate_number("3.1415"), 3.1415)

    def test_negative_float(self):
        self.assertAlmostEqual(validate_number("-0.001"), -0.001)

    def test_scientific_notation(self):
        self.assertAlmostEqual(validate_number("1e3"), 1000.0)
        self.assertAlmostEqual(validate_number("-2.5e-2"), -0.025)

    def test_whitespace_handling(self):
        self.assertEqual(validate_number("  15  "), 15.0)

    def test_invalid_numeric_raises(self):
        with self.assertRaises(ValueError) as cm:
            validate_number("abc")
        self.assertIn("numeric", str(cm.exception).lower())

        with self.assertRaises(ValueError) as cm:
            validate_number("")
        self.assertIn("numeric", str(cm.exception).lower())

        with self.assertRaises(ValueError) as cm:
            validate_number("12a")
        self.assertIn("numeric", str(cm.exception).lower())


class TestValidateOperator(unittest.TestCase):
    def test_valid_operators(self):
        for op in ["+", "-", "*", "/"]:
            self.assertEqual(validate_operator(op), op)

    def test_operator_with_whitespace(self):
        self.assertEqual(validate_operator("  +  "), "+")

    def test_invalid_operator_raises(self):
        invalid_ops = ["%", "x", "add", "", "++"]
        for op in invalid_ops:
            with self.subTest(op=op):
                with self.assertRaises(ValueError) as cm:
                    validate_operator(op)
                self.assertIn("operator", str(cm.exception).lower())


if __name__ == "__main__":
    unittest.main()