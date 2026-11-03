

## 1. Project Overview

This project provides a robust, object-oriented Python implementation of a mathematical expression evaluator powered by a custom **Stack** data structure. 

The program:
1. Reads arbitrary mathematical expressions separated by delimiter lines (e.g., `-----`) from an input file (`input.txt`).
2. Evaluates each expression using **Dijkstra's Shunting-Yard Algorithm** for infix-to-postfix conversion and a stack-based postfix evaluator, correctly obeying mathematical operator precedence (`*`, `/` over `+`, `-`), associativity (left-to-right), and parenthetical subexpressions.
3. Writes the calculated results into an output file (`output.txt`), replacing each expression with its corresponding result while preserving delimiters and original file formatting.

---

## 2. File and Directory Structure

The submission comprises the following files:

| File Name | Description |
| :--- | :--- |
| `expression_evaluator.py` | Core module containing the `Stack` class, `ExpressionEvaluator` engine, tokenizer, and file I/O processors. |
| `main.py` | Primary executable entry point for running the evaluation workflow. |
| `input.txt` | Sample input file containing mathematical expressions separated by `-----` as specified in the assignment brief. |
| `output.txt` | Result file generated automatically by the program corresponding to `input.txt`. |
| `test_evaluator.py` | Comprehensive automated unit test suite with 17 test cases covering all operations and edge scenarios. |
| `test_comprehensive_input.txt` | Extended test input file testing complex nested expressions, decimals, negatives, and error conditions. |
| `test_comprehensive_output.txt` | Output produced from the extended test suite. |
| `README.md` | Complete soft-copy documentation, user guide, assumptions, and limitations. |
| `REPORT.md` | Academic report for hard-copy submission containing Introduction, Data Structures, Architecture, Pseudocode, and Results. |
| `REPORT.html` | Print-ready, professionally styled document formatted strictly according to university specifications (Tahoma, 10pt, 1.15 line spacing, Justify). |

---

## 3. How to Run the Program

### Prerequisites
- Python 3.8 or higher (tested on Python 3.13.x).
- No external third-party dependencies or `pip install` commands required (utilizes pure Python standard library for maximum portability).

### A. Running the Default Evaluation
Ensure `input.txt` is present in the project directory, then run:

```bash
python main.py
```
or
```bash
python expression_evaluator.py
```

**Expected Console Output:**
```text
=================================================================
 Limkokwing University of Creative Technology - Sierra Leone
 DCOMP320: Data Structures and Algorithm - Stacks Implementation
 Mathematical Expression Evaluator
=================================================================
Reading expressions from : input.txt
Writing results to       : output.txt
-----------------------------------------------------------------
  [1] 3 + 5 * 2  ==>  13
  -----
  [2] (8 / 4) + 7 * 2  ==>  16
  -----
  [3] 10 - (2 + 3) * 4  ==>  -10
-----------------------------------------------------------------
Success! Processed 3 expression(s).
Results successfully saved to 'output.txt'.
=================================================================
```

### B. Specifying Custom Input and Output Files
You can pass custom input and output file paths via command-line arguments:

```bash
python main.py custom_input.txt custom_output.txt
```

Example with the provided extended test set:
```bash
python main.py test_comprehensive_input.txt test_comprehensive_output.txt
```

### C. Running the Automated Unit Test Suite
To verify all 17 unit tests validating stack operations, operator precedence, parentheses matching, floating-point numbers, negative numbers, and error handling:

```bash
python -m unittest test_evaluator.py -v
```

---

## 4. Structure of Input and Output Files

### Input File (`input.txt`)
- Contains mathematical expressions, each on its own line.
- Expressions are separated by lines consisting solely of delimiter characters, such as `-----` (or `===`, `***`).
- Arbitrary whitespace within expressions is automatically trimmed and handled.

**Sample `input.txt`:**
```text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

### Output File (`output.txt`)
- Contains the calculated result for each expression on the corresponding line.
- Retains the exact separator lines from the input file in identical relative positions.
- Whole numbers are cleanly formatted as integers (e.g. `13`, `-10`), and decimal results display only necessary significant digits (e.g. `3.5`).
- If an invalid mathematical operation occurs (e.g., division by zero or unmatched parentheses), a clear, non-crashing error message is written to that line.

**Sample `output.txt`:**
```text
13
-----
16
-----
-10
```

*(Note regarding Example 2: In the assignment brief image, expression `(8 / 4) + 7 * 2` mathematically equates to `2 + 14 = 16`. If `17` was pictured due to a typographical artifact or if the original intended expression was `(6 / 2) + 7 * 2 = 17`, our program rigorously computes the exact mathematical value `16` as required).*

---

## 5. Program Architecture and Features

### 1. `Stack` Class
Implements a strict LIFO container with the following operations:
- `push(item)`: Appends an item to the top of the stack ($O(1)$ amortized).
- `pop()`: Removes and returns the top item; raises `StackUnderflowError` if empty ($O(1)$).
- `peek()`: Returns the top item without removing it; raises `StackUnderflowError` if empty ($O(1)$).
- `is_empty()`: Returns boolean `True` if empty, `False` otherwise ($O(1)$).
- `size()`: Returns current count of stored items ($O(1)$).
- `clear()`: Empties the stack.

### 2. `ExpressionEvaluator` Class
- **Lexical Tokenizer (`tokenize`)**: Accurately extracts numbers (including multi-digit integers and floating-point values), parentheses, and operators. Intelligently distinguishes binary subtraction from unary minus/negative numbers (e.g., `-5 + 10` or `-(2 + 3)`).
- **Infix to Postfix Converter (`infix_to_postfix`)**: Uses an operator `Stack` following Dijkstra's Shunting-Yard algorithm to establish operator precedence (`*`, `/` > `+`, `-`) and enforce left-to-right associativity.
- **Postfix Evaluator (`evaluate_postfix`)**: Uses an operand `Stack` to compute the postfix expression in linear time $O(N)$.
- **Error Handling**: Gracefully handles and reports zero-division (`ZeroDivisionError`) and syntax/parentheses mismatches (`ValueError`).

### 3. File I/O Engine (`process_file`)
- Line-by-line streaming that preserves separators, handles empty lines, and writes formatted outputs to disk without memory bloat.

---

## 6. Assumptions and Limitations

### Assumptions
1. **Standard Infix Notation:** Input expressions follow standard arithmetic notation.
2. **Supported Operators:** The basic arithmetic operators supported are addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`). Parentheses `(` and `)` are supported to override precedence.
3. **Delimiter Recognition:** Any line consisting of 2 or more consecutive separator characters (such as hyphens `-`, underscores `_`, or asterisks `*`) is treated as an expression separator.
4. **Division Semantics:** Standard real floating-point division is performed. If the quotient is a whole number (e.g., `8 / 4 = 2.0`), it is formatted as an integer (`2`) to match standard academic presentation.

### Limitations
1. **Trigonometric and Transcendental Functions:** Functions such as `sin()`, `cos()`, `log()`, and `sqrt()` are not part of the standard basic four-operator specification and are not supported.
2. **Implicit Multiplication:** Expressions must use explicit multiplication operators (e.g., `2 * (3 + 4)` rather than `2(3 + 4)`).
3. **Variable Names:** Expressions are evaluated numerically; algebraic variables (e.g., `x + y`) are not supported.

---

## 7. GitHub Repository and Collaboration Instructions

As demanded in Section D.b.6 of the assignment specification:

### A. Initializing and Committing Locally
Run the following commands in the project folder:
```bash
git init
git add .
git commit -m "Initial submission: Stack implementation and expression evaluator for DCOMP320"
```

### B. Creating and Pushing to Remote Repository
1. Create a private or public repository on GitHub (e.g., `DCOMP320-Stacks-Assignment`).
2. Link and push your local branch:
```bash
git remote add origin https://github.com/<your-username>/DCOMP320-Stacks-Assignment.git
git branch -M main
git push -u origin main
```

### C. Adding the Lecturer as Collaborator
1. Open your repository on [GitHub](https://github.com).
2. Click **Settings** > **Collaborators** > **Add people**.
3. Enter the examiner's email address:  
   `amandus.bcoker@limkokwing.edu.sl`
4. Confirm invitation.

---

## 8. Author Information
- **Student Name:** Osman Kaimapo Momoh
- **Department:** Department of Information and Communication Technology
- **University:** Limkokwing University of Creative Technology, Sierra Leone
- **Module:** DCOMP320 — Data Structures and Algorithm
