"""
=============================================================================
DCOMP320 - DATA STRUCTURES AND ALGORITHM
Assignment: Stacks Implementation (Mathematical Expression Evaluator)
Limkokwing University of Creative Technology, Sierra Leone
Student Name: Osman Kaimapo Momoh
Examiner: Amandus Benjamin Coker (amandus.bcoker@limkokwing.edu.sl)
=============================================================================

This module implements a stack-based mathematical expression evaluator.
It reads mathematical expressions from an input file, parses and evaluates
them using the Stack data structure (implementing Dijkstra's Shunting-Yard
algorithm for Infix-to-Postfix conversion and Postfix evaluation), and writes
the evaluated results to an output file while preserving separators.
"""

import os
import re
import sys
from typing import List, Union, Tuple


class StackUnderflowError(Exception):
    """Exception raised when an operation is performed on an empty stack."""
    pass


class Stack:
    """
    A generic Last-In, First-Out (LIFO) Stack data structure implementation.
    
    Attributes:
        _items (list): Internal list used to store stack elements.
    """

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: List = []

    def push(self, item) -> None:
        """
        Add an item to the top of the stack.
        
        Args:
            item: The element to be pushed onto the stack.
        """
        self._items.append(item)

    def pop(self):
        """
        Remove and return the item at the top of the stack.
        
        Returns:
            The element popped from the top of the stack.
            
        Raises:
            StackUnderflowError: If the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        """
        Return the item at the top of the stack without removing it.
        
        Returns:
            The element at the top of the stack.
            
        Raises:
            StackUnderflowError: If the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Check whether the stack contains any items.
        
        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the total number of items currently in the stack.
        
        Returns:
            int: Number of elements in the stack.
        """
        return len(self._items)

    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()

    def to_list(self) -> List:
        """
        Return a copy of the underlying list of elements (bottom to top).
        
        Returns:
            List: Shallow copy of stack elements.
        """
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"Stack({self._items})"

    def __str__(self) -> str:
        return f"Top -> {list(reversed(self._items))}"


class ExpressionEvaluator:
    """
    Evaluates mathematical expressions using a stack-based algorithm.
    
    Supports:
        - Arithmetic operators: +, -, *, /
        - Parentheses: (, )
        - Standard operator precedence and left-associativity
        - Multi-digit numbers and floating-point values
        - Unary minus and negative numbers
    """

    # Operator precedence mapping
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    OPERATORS = {'+', '-', '*', '/'}

    @classmethod
    def tokenize(cls, expression: str) -> List[str]:
        """
        Convert a raw mathematical expression string into a list of tokens.
        
        Handles:
            - Multi-digit integers and decimals
            - Arithmetic operators (+, -, *, /)
            - Parentheses
            - Negative numbers and unary minus
            
        Args:
            expression: The raw string expression (e.g. '(8 / 4) + 7 * 2').
            
        Returns:
            List[str]: List of string tokens.
            
        Raises:
            ValueError: If an unrecognized character is encountered.
        """
        tokens: List[str] = []
        i = 0
        n = len(expression)

        while i < n:
            ch = expression[i]

            # 1. Skip whitespace
            if ch.isspace():
                i += 1
                continue

            # 2. Number (integer or float)
            if ch.isdigit() or ch == '.':
                num_str = ''
                has_dot = False
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        if has_dot:
                            raise ValueError(f"Invalid decimal format in expression at position {i}")
                        has_dot = True
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            # 3. Unary minus / negative number check
            # A minus is unary if:
            # - It is at the start of expression, OR
            # - Preceded by an operator, OR
            # - Preceded by an opening parenthesis '('
            if ch == '-':
                is_unary = (
                    len(tokens) == 0 or
                    tokens[-1] in cls.OPERATORS or
                    tokens[-1] == '('
                )
                if is_unary:
                    # Look ahead: if followed immediately by a digit or dot, combine as negative number
                    j = i + 1
                    while j < n and expression[j].isspace():
                        j += 1
                    if j < n and (expression[j].isdigit() or expression[j] == '.'):
                        # Advance i to j and parse negative number
                        num_str = '-'
                        has_dot = False
                        i = j
                        while i < n and (expression[i].isdigit() or expression[i] == '.'):
                            if expression[i] == '.':
                                if has_dot:
                                    raise ValueError(f"Invalid decimal format at position {i}")
                                has_dot = True
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                        continue
                    else:
                        # Unary minus before subexpression e.g. -(2+3) -> replace with 0 - ...
                        tokens.append('0')
                        tokens.append('-')
                        i += 1
                        continue

            # 4. Binary operators and parentheses
            if ch in cls.OPERATORS or ch in {'(', ')'}:
                tokens.append(ch)
                i += 1
                continue

            # 5. Invalid character encountered
            raise ValueError(f"Unsupported character '{ch}' at position {i}")

        return tokens

    @classmethod
    def infix_to_postfix(cls, tokens: List[str]) -> List[str]:
        """
        Convert infix tokens to postfix (Reverse Polish Notation) using Dijkstra's
        Shunting-Yard algorithm with an operator Stack.
        
        Args:
            tokens: List of infix tokens.
            
        Returns:
            List[str]: Postfix token list.
            
        Raises:
            ValueError: If parentheses are mismatched.
        """
        output: List[str] = []
        op_stack = Stack()

        for token in tokens:
            # If operand (number), append to output
            if cls._is_number(token):
                output.append(token)
            elif token == '(':
                op_stack.push(token)
            elif token == ')':
                # Pop until matching '(' is found
                found_match = False
                while not op_stack.is_empty():
                    top = op_stack.pop()
                    if top == '(':
                        found_match = True
                        break
                    output.append(top)
                if not found_match:
                    raise ValueError("Mismatched parentheses: closing ')' has no matching '('.")
            elif token in cls.OPERATORS:
                # Pop operators with greater or equal precedence
                current_prec = cls.PRECEDENCE[token]
                while (not op_stack.is_empty() and
                       op_stack.peek() != '(' and
                       cls.PRECEDENCE.get(op_stack.peek(), 0) >= current_prec):
                    output.append(op_stack.pop())
                op_stack.push(token)
            else:
                raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack
        while not op_stack.is_empty():
            top = op_stack.pop()
            if top == '(' or top == ')':
                raise ValueError("Mismatched parentheses: unclosed '(' detected.")
            output.append(top)

        return output

    @classmethod
    def evaluate_postfix(cls, postfix_tokens: List[str]) -> Union[int, float]:
        """
        Evaluate a postfix expression using an operand Stack.
        
        Args:
            postfix_tokens: List of tokens in Reverse Polish Notation.
            
        Returns:
            Union[int, float]: Evaluated numerical result.
            
        Raises:
            ValueError: For malformed expressions.
            ZeroDivisionError: For division by zero.
        """
        val_stack = Stack()

        for token in postfix_tokens:
            if cls._is_number(token):
                # Push number onto operand stack
                if '.' in token:
                    val_stack.push(float(token))
                else:
                    val_stack.push(int(token))
            elif token in cls.OPERATORS:
                if val_stack.size() < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'.")
                
                # Note the order of operands: top is right operand (b), next is left (a)
                b = val_stack.pop()
                a = val_stack.pop()

                if token == '+':
                    res = a + b
                elif token == '-':
                    res = a - b
                elif token == '*':
                    res = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Error: Division by zero")
                    res = a / b
                else:
                    raise ValueError(f"Unsupported operator: {token}")

                val_stack.push(res)
            else:
                raise ValueError(f"Invalid postfix token: {token}")

        if val_stack.size() != 1:
            raise ValueError("Malformed expression: extraneous operands detected.")

        result = val_stack.pop()
        return result

    @classmethod
    def evaluate(cls, expression: str) -> Union[int, float]:
        """
        End-to-end evaluation of an infix mathematical expression.
        
        Tokenizes -> Infix to Postfix -> Evaluates Postfix.
        
        Args:
            expression: Infix expression string.
            
        Returns:
            Union[int, float]: Result of the evaluation.
        """
        stripped = expression.strip()
        if not stripped:
            raise ValueError("Empty expression.")
        
        tokens = cls.tokenize(stripped)
        if not tokens:
            raise ValueError("No valid tokens found.")
            
        postfix = cls.infix_to_postfix(tokens)
        result = cls.evaluate_postfix(postfix)
        return result

    @staticmethod
    def format_result(value: Union[int, float]) -> str:
        """
        Format a numerical result cleanly for output display.
        
        If the number is mathematically an integer (e.g. 13.0 or -10.0),
        formats without trailing decimals ('13', '-10').
        If fractional, formats with up to 6 significant decimal places.
        
        Args:
            value: Numerical value (int or float).
            
        Returns:
            str: Cleanly formatted string representation.
        """
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            # Format floating point and strip trailing zeros
            formatted = f"{value:.6f}".rstrip('0').rstrip('.')
            return formatted
        return str(value)

    @staticmethod
    def _is_number(token: str) -> bool:
        """Check if a token string represents an integer or float."""
        try:
            float(token)
            return True
        except ValueError:
            return False


def is_separator_line(line: str) -> bool:
    """
    Check if a given line is a separator line (e.g., '-----', '===', '***').
    
    A line is classified as a separator if it contains at least 2 characters
    and consists entirely of standard divider characters.
    
    Args:
        line: The line to check.
        
    Returns:
        bool: True if line is a separator, False otherwise.
    """
    stripped = line.strip()
    if len(stripped) < 2:
        return False
    separator_chars = {'-', '=', '_', '*', '~'}
    return all(ch in separator_chars for ch in stripped)


def process_file(input_filepath: str = "input.txt",
                 output_filepath: str = "output.txt") -> List[Tuple[str, str]]:
    """
    Read expressions from input_filepath, evaluate each expression using the
    stack-based evaluator, and write results to output_filepath preserving
    the exact separator lines.
    
    Args:
        input_filepath: Path to the input text file.
        output_filepath: Path to the output text file.
        
    Returns:
        List[Tuple[str, str]]: List of (original_line, result_or_separator) pairs.
    """
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"Input file '{input_filepath}' not found.")

    with open(input_filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results: List[Tuple[str, str]] = []
    output_lines: List[str] = []

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip('\r\n')
        stripped = line.strip()

        # Handle blank lines
        if not stripped:
            output_lines.append("")
            results.append((line, ""))
            continue

        # Handle separator lines
        if is_separator_line(stripped):
            output_lines.append(stripped)
            results.append((line, stripped))
            continue

        # It's an expression line -> evaluate it
        try:
            val = ExpressionEvaluator.evaluate(stripped)
            formatted = ExpressionEvaluator.format_result(val)
            output_lines.append(formatted)
            results.append((stripped, formatted))
        except ZeroDivisionError as zde:
            error_msg = str(zde)
            output_lines.append(error_msg)
            results.append((stripped, error_msg))
        except ValueError as ve:
            error_msg = f"Error: {ve}"
            output_lines.append(error_msg)
            results.append((stripped, error_msg))
        except Exception as ex:
            error_msg = f"Error: {type(ex).__name__}: {ex}"
            output_lines.append(error_msg)
            results.append((stripped, error_msg))

    # Write results to output file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        for out_line in output_lines:
            f.write(out_line + "\n")

    return results


def main() -> None:
    """CLI Entry point for executing the expression evaluator."""
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    print("=" * 65)
    print(" Limkokwing University of Creative Technology - Sierra Leone")
    print(" DCOMP320: Data Structures and Algorithm - Stacks Implementation")
    print(" Mathematical Expression Evaluator")
    print("=" * 65)
    print(f"Reading expressions from : {input_file}")
    print(f"Writing results to       : {output_file}")
    print("-" * 65)

    try:
        results = process_file(input_file, output_file)
        count = 0
        for original, evaluated in results:
            if is_separator_line(evaluated):
                print(f"  {evaluated}")
            elif original.strip() == "":
                continue
            else:
                count += 1
                print(f"  [{count}] {original}  ==>  {evaluated}")

        print("-" * 65)
        print(f"Success! Processed {count} expression(s).")
        print(f"Results successfully saved to '{output_file}'.")
        print("=" * 65)
    except FileNotFoundError as fnf:
        print(f"Error: {fnf}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
