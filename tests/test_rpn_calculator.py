import unittest

from src.calc import RPNCalculator
from src.exceptions import InvalidTokenError, TooManyOperandsError, NotEnoughOperandsError, WrongBracketCombinationError


class TestRPNCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = RPNCalculator()

    def test_addition(self) -> None:
        res = self.calc.solve("420 1337 +")
        self.assertEqual(res, 420 + 1337)

    def test_subtraction(self) -> None:
        res = self.calc.solve("1337 420 -")
        self.assertEqual(res, 1337 - 420)

    def test_multiplication(self) -> None:
        res = self.calc.solve("1337 420 *")
        self.assertEqual(res, 1337 * 420)

    def test_division(self) -> None:
        res = self.calc.solve("420 20 /")
        self.assertEqual(res, 420 / 20)

    def test_power(self) -> None:
        res = self.calc.solve("420 3 **")
        self.assertEqual(res, 420 ** 3)

    def test_simple_subline(self) -> None:
        res = self.calc.solve("420 ( 2 1 + ) **")
        self.assertEqual(res, 420 ** 3)

    def test_deep_sublines(self) -> None:
        res = self.calc.solve("420 ( 1337 420 ( 63 6 + ) + - ) ( 2 10 ** ) ( 28 7 / ) - * -")
        self.assertEqual(res, -864540.0)

    def test_single_number(self) -> None:
        res = self.calc.solve("420")
        self.assertEqual(res, 420.0)

    def test_invalid_token(self) -> None:
        with self.assertRaises(InvalidTokenError):
            self.calc.solve("2344 455 & 12 (>-<) + + / **")

    def test_too_many_operands(self) -> None:
        with self.assertRaises(TooManyOperandsError):
            self.calc.solve("2 2 * *")

    def test_not_enough_operands(self) -> None:
        with self.assertRaises(NotEnoughOperandsError):
            self.calc.solve("2 2 2 *")

    def test_wrong_bracket_combination(self) -> None:
        with self.assertRaises(WrongBracketCombinationError):
            self.calc.solve("2 ( 2 3 + ) ) +")

    def test_zero_division(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.solve("2 0 /")
