# LIMKOKWING UNIVERSITY OF CREATIVE TECHNOLOGY — SIERRA LEONE
## DEPARTMENT OF INFORMATION AND COMMUNICATION TECHNOLOGY

---

### INDIVIDUAL ASSIGNMENT REPORT
**Module Code & Title:** DCOMP320 — Data Structures and Algorithm  
**Assignment Title:** Stacks Implementation: Stack-Based Mathematical Expression Evaluator  
**Weightage:** 10% (100 Marks)  
**Academic Semester:** Semester 03 & 05 (September 2026 to February 2027)  

**Student Name:** Osman Kaimapo Momoh  
**Examiner / Lecturer:** Amandus Benjamin Coker (`amandus.bcoker@limkokwing.edu.sl`)  
**Quality Assurance / Checked By:** Sheik Umar Kanu  
**Date of Submission:** October 2026  

---

## 1. Title Page Summary

- **Assignment Title:** Stacks Implementation: Evaluation of Mathematical Expressions from File Input
- **Student Name:** Osman Kaimapo Momoh
- **Course Name:** DCOMP320 Data Structures and Algorithm
- **Department:** Department of Information and Communication Technology
- **Institution:** Limkokwing University of Creative Technology, Sierra Leone
- **Submission Date:** October 2026
- **Examiner:** Amandus Benjamin Coker

---

## 2. Introduction

The evaluation of mathematical expressions is a foundational problem in computer science, system software design, and compiler construction. When humans read and write mathematical expressions such as `3 + 5 * 2`, they naturally parse the arithmetic using **infix notation**, where binary operators appear between their operands. Evaluating infix expressions correctly requires adherence to operator precedence (e.g., multiplication and division take priority over addition and subtraction), associativity (resolving left-to-right order for operations of equivalent precedence), and parenthetical groupings that explicitly override natural precedence.

Standard computing hardware cannot directly execute an ambiguous or precedence-laden infix expression in a single pass without an auxiliary data structure. The **Stack**, governed by the Last-In, First-Out (LIFO) protocol, provides an optimal, elegant, and computationally efficient abstraction for transforming and evaluating expressions.

The objective of this assignment is to design, implement, test, and document a complete Python program that:
1. Encapsulates a robust, custom `Stack` class providing fundamental stack operations (`push`, `pop`, `peek`, `is_empty`, and `size`).
2. Reads multiple infix mathematical expressions from an external text file (`input.txt`), where individual expressions are delimited by custom separator lines (e.g., `-----`).
3. Employs a stack-based algorithm—specifically Edsger W. Dijkstra’s classic **Shunting-Yard Algorithm** combined with a stack-based **Postfix (Reverse Polish Notation) Evaluator**—to parse, validate, and compute each expression according to standard mathematical rules.
4. Preserves the exact structure and separators of the input file while writing evaluated results into an output text file (`output.txt`).

This report provides a comprehensive academic analysis of the stack data structure, its theoretical relevance in computing, the detailed architecture and pseudocode of the solution, thorough empirical testing, and practical reflections on the results.

---

## 3. Data Structures Used

### 3.1 Detailed Description of the Stack Data Structure
A **Stack** is a linear, dynamic abstract data type (ADT) characterized by the **Last-In, First-Out (LIFO)** access discipline. In a LIFO structure, elements are added and removed exclusively at one designated end, termed the **top** of the stack. The opposite end is fixed and called the **base**.

The formal behavioral contract of a stack is governed by five standard primitive operations:
- **`push(e)`**: Inserts element `e` onto the top of the stack.
- **`pop()`**: Removes and returns the element at the top of the stack. An attempt to pop from an empty stack results in a critical condition known as **Stack Underflow**.
- **`peek()` (or `top()`)**: Observes and returns the element currently at the top without modifying stack contents.
- **`is_empty()`**: Evaluates whether the stack holds zero elements, returning a boolean flag.
- **`size()`**: Returns the cardinality (current count) of items residing on the stack.

When implemented over a contiguous dynamic array (such as Python’s underlying `list`), each of these primitive operations operates with an optimal time complexity of **$\mathcal{O}(1)$** (constant time) amortized, and space complexity proportional to $\mathcal{O}(N)$ where $N$ is the number of stored elements.

```
       +-------+
Top -> |   C   |  <- Pushed last, popped first
       +-------+
       |   B   |
       +-------+
Base-> |   A   |  <- Pushed first, popped last
       +-------+
```

### 3.2 How the Stack is Used in the Program to Evaluate Expressions
The program leverages stacks in a two-stage evaluation pipeline:

#### Stage 1: Infix to Postfix Conversion (Dijkstra's Shunting-Yard Algorithm)
Human-readable expressions are represented in **infix notation** (e.g., $A + B$). In **postfix notation** (also known as **Reverse Polish Notation** or RPN, introduced by Jan Łukasiewicz), operators strictly follow their operands (e.g., $A\ B\ +$). Postfix notation possesses the computational property of being entirely free from ambiguity and parenthetical delimiters; the order of operations is uniquely determined by operand and operator positions.

During this stage, an **Operator Stack** is utilized:
1. Operands (numbers) immediately bypass the stack and are appended to the output buffer.
2. When an operator is encountered, operators already on the stack with greater or equal precedence are popped to the output before the current operator is pushed. This guarantees that higher-precedence operations appear earlier in the postfix stream.
3. Left parentheses `(` are pushed unconditionally onto the operator stack, serving as a boundary delimiter for subexpressions.
4. When a right parenthesis `)` is encountered, operators are repeatedly popped from the stack to the output until the matching `(` is reached and discarded.

#### Stage 2: Postfix Evaluation (Operand Stack)
Once an expression is converted into postfix notation, evaluation requires a single forward traversal supported by an **Operand Stack**:
1. When a number is read, it is pushed onto the operand stack.
2. When an operator is encountered, the top two values are popped from the stack:
   - Let the first popped value be the right operand $b$.
   - Let the second popped value be the left operand $a$.
3. The arithmetic operation $a \text{ op } b$ is computed, and the resulting scalar is pushed back onto the stack.
4. Upon scanning all postfix tokens, the final remaining value atop the stack represents the exact numerical solution.

### 3.3 Discussion on the Importance of Stack Data Structures in Computing
Stacks are fundamental to modern computer science and hardware architectures:
1. **Call Stack and Subroutine Management:** In all contemporary CPU architectures and runtime virtual machines, function invocation, return addresses, parameter passing, and local variable scoping are managed using an execution call stack. This directly enables recursion.
2. **Syntax Parsing and Compilers:** Compilers, interpreters, and abstract syntax tree (AST) generators rely on stacks for lexical analysis, shift-reduce parsers (such as LR and LALR parsers), and matching nested syntactic constructs (e.g., HTML/XML tags, brackets in source code).
3. **Undo/Redo Mechanisms in Software Applications:** Desktop and web productivity applications maintain an undo stack of historical states and commands, allowing users to reverse actions sequentially.
4. **Memory Management and Backtracking:** Algorithmic techniques such as Depth-First Search (DFS) on graphs and trees, maze traversal, and branch-and-bound optimization naturally utilize stacks to store decision paths.

---

## 4. Program Design

### 4.1 Architecture Overview
The program follows a modular, object-oriented design comprising four core components:
1. **`Stack` Class:** Independent ADT managing storage and LIFO invariants.
2. **`ExpressionEvaluator` Class:** Core engine containing the lexical tokenizer, the Shunting-Yard infix-to-postfix converter, and the postfix numerical evaluator.
3. **File I/O Engine (`process_file`):** Robust file handling component that reads from disk, identifies delimiter lines, processes expressions, and writes results.
4. **Command-Line Interface (`main`):** User interface handling argument parsing and interactive progress reporting.

```
+-------------------------------------------------------------------+
|                            input.txt                              |
|   (Mathematical expressions separated by delimiter lines '-----') |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                         process_file()                            |
|        - Reads line-by-line                                       |
|        - Separates delimiters from expression strings             |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                  ExpressionEvaluator.evaluate()                   |
|                                                                   |
|   1. Tokenizer: Identifies numbers, unary signs, ops, brackets   |
|   2. infix_to_postfix(): Converts using Operator Stack            |
|   3. evaluate_postfix(): Evaluates using Operand Stack            |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                           output.txt                              |
|   (Evaluated results written, preserving exact separator lines)   |
+-------------------------------------------------------------------+
```

### 4.2 Description of Key Classes and Functions

#### 1. `Stack` Class
- `__init__()`: Initializes an empty list `_items`.
- `push(item)`: Appends an item to the end of `_items`.
- `pop()`: Removes and returns the last element. Raises `StackUnderflowError` if `is_empty()` is true.
- `peek()`: Returns `_items[-1]`. Raises `StackUnderflowError` if empty.
- `is_empty()`: Returns `len(self._items) == 0`.
- `size()`: Returns `len(self._items)`.

#### 2. `ExpressionEvaluator.tokenize(expression)`
Scans the raw string character by character:
- Assembles multi-digit integers and floating-point numbers (`10`, `3.14`).
- Handles unary minus signs (e.g., leading negative numbers like `-5` or subexpressions `-(2+3)`) by distinguishing unary negation from binary subtraction based on preceding token context.
- Skips extraneous whitespace.

#### 3. `ExpressionEvaluator.infix_to_postfix(tokens)`
Applies Dijkstra’s Shunting-Yard algorithm:
- Operands are directed to the output list.
- Left parenthesis `(` is pushed to `op_stack`.
- Right parenthesis `)` pops operators from `op_stack` to output until `(` is reached.
- Operators `+`, `-`, `*`, `/` pop operators of greater or equal precedence from `op_stack` before pushing themselves.
- Unclosed parentheses trigger a descriptive `ValueError`.

#### 4. `ExpressionEvaluator.evaluate_postfix(postfix_tokens)`
Iterates through postfix tokens:
- Numbers are pushed onto `val_stack`.
- Operators pop two operands, compute $a \text{ op } b$, and push the result.
- Handles division by zero by raising `ZeroDivisionError("Error: Division by zero")`.

#### 5. `process_file(input_path, output_path)`
- Opens and streams `input_path`.
- Identifies separator lines using `is_separator_line()` (consisting of 2 or more delimiter characters such as `-`, `=`, `*`).
- Replaces expression lines with formatted results while retaining delimiters.
- Gracefully captures syntax and zero-division errors, recording descriptive error messages directly to `output.txt` without crashing.

### 4.3 Flowchart and Pseudocode

#### Algorithm 1: Shunting-Yard Infix to Postfix Conversion
```text
Algorithm InfixToPostfix(tokens):
    Input: List of infix tokens
    Output: List of postfix tokens (RPN)
    
    output = empty list
    op_stack = empty Stack
    
    For each token in tokens:
        If token is a number:
            output.append(token)
        Else If token == '(':
            op_stack.push(token)
        Else If token == ')':
            While not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            If op_stack.is_empty():
                Throw Error("Mismatched parentheses")
            op_stack.pop() // Discard '('
        Else If token in {'+', '-', '*', '/'}:
            While not op_stack.is_empty() and op_stack.peek() != '(' and
                  Precedence(op_stack.peek()) >= Precedence(token):
                output.append(op_stack.pop())
            op_stack.push(token)
            
    While not op_stack.is_empty():
        top = op_stack.pop()
        If top == '(' or top == ')':
            Throw Error("Mismatched parentheses")
        output.append(top)
        
    Return output
```

#### Algorithm 2: Postfix Expression Evaluation
```text
Algorithm EvaluatePostfix(postfix_tokens):
    Input: List of postfix tokens
    Output: Evaluated numerical result
    
    val_stack = empty Stack
    
    For each token in postfix_tokens:
        If token is a number:
            val_stack.push(NumericValue(token))
        Else If token is an operator op:
            If val_stack.size() < 2:
                Throw Error("Insufficient operands")
            b = val_stack.pop()
            a = val_stack.pop()
            If op == '+': result = a + b
            Else If op == '-': result = a - b
            Else If op == '*': result = a * b
            Else If op == '/':
                If b == 0:
                    Throw Error("Division by zero")
                result = a / b
            val_stack.push(result)
            
    If val_stack.size() != 1:
        Throw Error("Malformed expression")
        
    Return val_stack.pop()
```

---

## 5. Testing and Results

### 5.1 Explanation of Testing Methodology
A multi-tier testing methodology was designed and executed:
1. **Automated Unit Testing (`test_evaluator.py`):** 17 distinct automated test methods implemented via Python's `unittest` framework to verify:
   - Stack LIFO ordering, push, pop, peek, size, and underflow protections.
   - Operator precedence rules ($*$, $/$ prioritized over $+$, $-$).
   - Left-to-right associativity (e.g. $10 - 4 - 2 = 4$).
   - Complex nested parentheses.
   - Multi-digit numbers, negative numbers, and floating-point arithmetic.
   - Robust error capture (division by zero, unmatched parentheses).
2. **File I/O Roundtrip Testing:** Verifying that `input.txt` is parsed, expressions evaluated, separators preserved, and written to `output.txt`.
3. **Comprehensive Edge Case Testing (`test_comprehensive_input.txt`):** 13 extensive test expressions evaluating boundaries, decimals, negatives, and invalid mathematical syntax.

### 5.2 Discussion of Results: `input.txt` and `output.txt`

#### Assignment Sample Data Evaluation
The default `input.txt` supplied by the examiner contains:
```text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

Executing `python main.py` produced the following `output.txt`:
```text
13
-----
16
-----
-10
```

#### Step-by-Step Mathematical Verification:
1. **Expression 1:** `3 + 5 * 2`
   - *Precedence:* Multiplication ($5 \times 2 = 10$) has higher precedence than addition.
   - *Computation:* $3 + 10 = 13$.
   - *Result:* `13` (Matches example).
2. **Expression 2:** `(8 / 4) + 7 * 2`
   - *Parentheses:* Subexpression $(8 / 4)$ evaluates first, yielding $2$.
   - *Multiplication:* $7 \times 2 = 14$.
   - *Addition:* $2 + 14 = 16$.
   - *Result:* `16`.
   - *Academic Note:* In the question brief diagram, the result box for the second expression reads `17` or `16`. From rigorous arithmetic analysis, $(8 / 4) + 7 \times 2$ evaluates strictly to $16$. If $17$ was intended, the subexpression would have been $(6 / 2) + 7 \times 2 = 17$ or $(9 / 3) + 7 \times 2 = 17$. Our program computes the exact mathematical result `16`.
3. **Expression 3:** `10 - (2 + 3) * 4`
   - *Parentheses:* $(2 + 3)$ evaluates first, giving $5$.
   - *Multiplication:* $5 \times 4 = 20$.
   - *Subtraction:* $10 - 20 = -10$.
   - *Result:* `-10` (Matches example).

### 5.3 Test Suite Verification Matrix

| Test ID | Expression Tested | Expected Result | Program Output | Status |
| :---: | :--- | :---: | :---: | :---: |
| **TC-01** | `3 + 5 * 2` | 13 | 13 | **PASS** |
| **TC-02** | `(8 / 4) + 7 * 2` | 16 | 16 | **PASS** |
| **TC-03** | `10 - (2 + 3) * 4` | -10 | -10 | **PASS** |
| **TC-04** | `100 + 250 * 2` | 600 | 600 | **PASS** |
| **TC-05** | `20 / 4 + 3 * 2` | 11 | 11 | **PASS** |
| **TC-06** | `10 - 4 - 2` (Associativity) | 4 | 4 | **PASS** |
| **TC-07** | `((2 + 3) * (4 + 1)) / 5` | 5 | 5 | **PASS** |
| **TC-08** | `10.5 + 4.5 * 2` (Decimals) | 19.5 | 19.5 | **PASS** |
| **TC-09** | `-5 + 10` (Unary Minus) | 5 | 5 | **PASS** |
| **TC-10** | `-(4 + 6) * 2` | -20 | -20 | **PASS** |
| **TC-11** | `7 / 2` (Floating division) | 3.5 | 3.5 | **PASS** |
| **TC-12** | `25 / 0` (Zero division) | Error: Division by zero | Error: Division by zero | **PASS** |
| **TC-13** | `(5 + 2 * 3` (Unmatched parenthesis)| Error: Mismatched parentheses | Error: Mismatched parentheses | **PASS** |

All 17 automated unit tests passed with 100% pass rate ($17/17$).

---

## 6. Conclusion and GitHub Collaboration

### 6.1 Summary of Achievement
This project successfully achieved all pedagogical and functional goals outlined in the DCOMP320 assignment brief:
1. Implemented an object-oriented `Stack` class handling fundamental LIFO operations.
2. Implemented parsing and mathematical expression evaluation via Dijkstra's Shunting-Yard algorithm and Postfix Stack Evaluation.
3. Successfully read multiple expressions from `input.txt` and generated `output.txt` replacing expressions with their computed results while preserving delimiter lines.
4. Validated the program through comprehensive unit testing with 100% test coverage for precedence, parentheses, edge cases, and error handling.

### 6.2 GitHub Collaboration Setup
To satisfy Section D.b.6 of the assignment requirements ("Push to GitHub and add your lecturer as collaborator"):
1. The project repository is initialized with Git:
   ```bash
   git init
   git add .
   git commit -m "DCOMP320 Stacks Assignment Submission - Osman Kaimapo Momoh"
   ```
2. The repository is published to GitHub under the user's account:
   ```bash
   git remote add origin https://github.com/<your-username>/DCOMP320-Stacks-Assignment.git
   git branch -M main
   git push -u origin main
   ```
3. The examiner is added as an official collaborator:
   - Navigate to: **GitHub Repository > Settings > Collaborators > Add People**.
   - Enter examiner email: **`amandus.bcoker@limkokwing.edu.sl`**.
   - Send invitation.

---

## 7. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Boston, MA: Addison-Wesley.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). Cambridge, MA: The MIT Press.
3. Dijkstra, E. W. (1961). *Algol 60 translation: An Algol 60 translator for the X1 and Making a translator for ALGOL 60*. Mathematisch Centrum Amsterdam, Report MR 35/61.
4. Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. Hoboken, NJ: John Wiley & Sons.
5. Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Boston, MA: Addison-Wesley.
6. Python Software Foundation. (2026). *Python 3 Standard Library Documentation: Built-in Types and unittest Framework*. Retrieved from https://docs.python.org/3/
