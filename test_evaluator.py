"""
=============================================================================
DCOMP320 - DATA STRUCTURES AND ALGORITHM
Assignment: Stacks Implementation (Unit Test Suite)
Limkokwing University of Creative Technology, Sierra Leone
Student Name: Osman Kaimapo Momoh
Examiner: Amandus Benjamin Coker (amandus.bcoker@limkokwing.edu.sl)
=============================================================================

Comprehensive test suite verifying:
1. Stack class operations (push, pop, peek, is_empty, size, underflow)
2. Infix to Postfix conversion
3. Postfix expression evaluation
4. Precedence rules (*, / over +, -)
5. Parentheses handling & nested brackets
6. Multi-digit numbers & decimals
7. Negative numbers and unary negation
8. Error handling (Division by zero, mismatched parentheses)
9. File I/O processing with separators
"""

import os
import unittest
from expression_evaluator import (
    Stack,
    StackUnderflowError,
    ExpressionEvaluator,
    is_separator_line,
    process_file,
)


class TestStackOperations(unittest.TestCase):
    """Unit tests for the Stack data structure implementation."""

    def setUp(self):
        self.stack = Stack()

    def test_initial_state(self):
        """A new stack should be empty with size 0."""
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack), 0)

    def test_push_and_peek(self):
        """Pushed items should become the top item returned by peek without removal."""
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 10)

        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)
        self.assertEqual(self.stack.peek(), 20)

    def test_push_and_pop_lifo_order(self):
        """Items must be removed in Last-In, First-Out (LIFO) order."""
        self.stack.push("A")
        self.stack.push("B")
        self.stack.push("C")

        self.assertEqual(self.stack.pop(), "C")
        self.assertEqual(self.stack.pop(), "B")
        self.assertEqual(self.stack.pop(), "A")
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_stack_raises_error(self):
        """Popping from an empty stack must raise StackUnderflowError."""
        with self.assertRaises(StackUnderflowError):
            self.stack.pop()

    def test_peek_empty_stack_raises_error(self):
        """Peeking at an empty stack must raise StackUnderflowError."""
        with self.assertRaises(StackUnderflowError):
            self.stack.peek()

    def test_clear(self):
        """Clear should remove all items."""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)


class TestExpressionEvaluator(unittest.TestCase):
    """Unit tests for mathematical expression evaluation."""

    def test_assignment_examples(self):
        """Verify the exact sample expressions from the assignment brief."""
        # 3 + 5 * 2 = 3 + 10 = 13
        self.assertEqual(ExpressionEvaluator.evaluate("3 + 5 * 2"), 13)

        # (8 / 4) + 7 * 2 = 2 + 14 = 16
        self.assertEqual(ExpressionEvaluator.evaluate("(8 / 4) + 7 * 2"), 16)

        # 10 - (2 + 3) * 4 = 10 - 20 = -10
        self.assertEqual(ExpressionEvaluator.evaluate("10 - (2 + 3) * 4"), -10)

    def test_operator_precedence(self):
        """Test multiplication and division precedence over addition and subtraction."""
        self.assertEqual(ExpressionEvaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(ExpressionEvaluator.evaluate("2 * 3 + 4"), 10)
        self.assertEqual(ExpressionEvaluator.evaluate("20 - 10 / 2"), 15)
        self.assertEqual(ExpressionEvaluator.evaluate("20 / 4 + 3 * 2"), 11)

    def test_associativity(self):
        """Test left-to-right associativity for operators with the same precedence."""
        # 10 - 4 - 2 should be (10 - 4) - 2 = 4, NOT 10 - (4 - 2) = 8
        self.assertEqual(ExpressionEvaluator.evaluate("10 - 4 - 2"), 4)
        # 24 / 4 / 2 should be (24 / 4) / 2 = 3, NOT 24 / (4 / 2) = 12
        self.assertEqual(ExpressionEvaluator.evaluate("24 / 4 / 2"), 3)

    def test_parentheses(self):
        """Test expression evaluation with simple and nested parentheses."""
        self.assertEqual(ExpressionEvaluator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(ExpressionEvaluator.evaluate("2 * (3 + 4)"), 14)
        self.assertEqual(ExpressionEvaluator.evaluate("((2 + 3) * (4 + 1)) / 5"), 5)
        self.assertEqual(ExpressionEvaluator.evaluate("100 / ((2 + 3) * 2)"), 10)

    def test_multi_digit_and_floating_point(self):
        """Test multi-digit integers and decimal numbers."""
        self.assertEqual(ExpressionEvaluator.evaluate("150 + 250"), 400)
        self.assertEqual(ExpressionEvaluator.evaluate("10.5 + 4.5"), 15)
        self.assertAlmostEqual(ExpressionEvaluator.evaluate("7.5 * 2.0"), 15.0)
        self.assertAlmostEqual(ExpressionEvaluator.evaluate("1 / 4"), 0.25)

    def test_negative_numbers_and_unary_minus(self):
        """Test negative numbers and expressions with leading/unary minus."""
        self.assertEqual(ExpressionEvaluator.evaluate("-5 + 10"), 5)
        self.assertEqual(ExpressionEvaluator.evaluate("10 + -3"), 7)
        self.assertEqual(ExpressionEvaluator.evaluate("-(4 + 6) * 2"), -20)
        self.assertEqual(ExpressionEvaluator.evaluate("-10 - -5"), -5)

    def test_division_by_zero(self):
        """Division by zero must raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            ExpressionEvaluator.evaluate("10 / 0")

        with self.assertRaises(ZeroDivisionError):
            ExpressionEvaluator.evaluate("5 / (3 - 3)")

    def test_mismatched_parentheses(self):
        """Mismatched parentheses must raise ValueError."""
        with self.assertRaises(ValueError):
            ExpressionEvaluator.evaluate("(2 + 3")

        with self.assertRaises(ValueError):
            ExpressionEvaluator.evaluate("2 + 3)")

        with self.assertRaises(ValueError):
            ExpressionEvaluator.evaluate("((5 + 2) * 3")

    def test_format_result(self):
        """Test formatting of integer vs floating results."""
        self.assertEqual(ExpressionEvaluator.format_result(13.0), "13")
        self.assertEqual(ExpressionEvaluator.format_result(-10.0), "-10")
        self.assertEqual(ExpressionEvaluator.format_result(2.5), "2.5")
        self.assertEqual(ExpressionEvaluator.format_result(42), "42")


class TestFileProcessing(unittest.TestCase):
    """Unit tests for reading input.txt, preserving separators, and generating output.txt."""

    def test_is_separator_line(self):
        """Verify separator line detector."""
        self.assertTrue(is_separator_line("-----"))
        self.assertTrue(is_separator_line("---"))
        self.assertTrue(is_separator_line("=========="))
        self.assertTrue(is_separator_line("***"))
        self.assertFalse(is_separator_line("3 + 5 * 2"))
        self.assertFalse(is_separator_line("-5"))
        self.assertFalse(is_separator_line("-"))

    def test_process_file_roundtrip(self):
        """Verify file reading, evaluation, and output file formatting."""
        test_in = "temp_test_input.txt"
        test_out = "temp_test_output.txt"

        input_data = (
            "3 + 5 * 2\n"
            "-----\n"
            "(8 / 4) + 7 * 2\n"
            "-----\n"
            "10 - (2 + 3) * 4\n"
            "-----\n"
            "10 / 0\n"
        )
        with open(test_in, "w", encoding="utf-8") as f:
            f.write(input_data)

        try:
            results = process_file(test_in, test_out)
            self.assertEqual(len(results), 7)

            with open(test_out, "r", encoding="utf-8") as f:
                output_content = f.read().splitlines()

            expected = [
                "13",
                "-----",
                "16",
                "-----",
                "-10",
                "-----",
                "Error: Division by zero",
            ]
            self.assertEqual(output_content, expected)
        finally:
            if os.path.exists(test_in):
                os.remove(test_in)
            if os.path.exists(test_out):
                os.remove(test_out)


if __name__ == "__main__":
    unittest.main()
