import unittest
from src.calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Unit tests for the calculator engine."""

    # Basic operation tests
    def test_addition_integers(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, -5), -6)

    def test_addition_floats(self):
        self.assertAlmostEqual(add(2.5, 3.1), 5.6)
        self.assertAlmostEqual(add(-0.1, 0.2), 0.1)

    def test_subtraction_integers(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(-3, -7), 4)

    def test_subtraction_floats(self):
        self.assertAlmostEqual(subtract(5.5, 2.2), 3.3)
        self.assertAlmostEqual(subtract(-1.0, 1.0), -2.0)

    def test_multiplication_integers(self):
        self.assertEqual(multiply(3, 7), 21)
        self.assertEqual(multiply(-2, 4), -8)

    def test_multiplication_floats(self):
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0)
        self.assertAlmostEqual(multiply(-1.5, -2.0), 3.0)

    def test_division_integers(self):
        self.assertEqual(divide(8, 2), 4.0)
        self.assertEqual(divide(-9, 3), -3.0)

    def test_division_floats(self):
        self.assertAlmostEqual(divide(7.5, 2.5), 3.0)
        self.assertAlmostEqual(divide(-5.0, -2.0), 2.5)

    # Edge case tests
    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_zero_operands(self):
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(multiply(0, 0), 0)
        self.assertEqual(divide(0, 1), 0.0)

    def test_large_numbers(self):
        large = 1e308
        self.assertAlmostEqual(add(large, large), large * 2)
        self.assertAlmostEqual(multiply(large, 2), large * 2)

    def test_small_numbers(self):
        small = 1e-308
        self.assertAlmostEqual(add(small, small), small * 2)
        self.assertAlmostEqual(multiply(small, 2), small * 2)

    def test_negative_numbers(self):
        self.assertEqual(add(-5, 3), -2)
        self.assertEqual(subtract(-5, 3), -8)
        self.assertEqual(multiply(-5, -3), 15)
        self.assertEqual(divide(-6, -2), 3.0)


if __name__ == "__main__":
    unittest.main()