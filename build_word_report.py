"""
Generates the official hard-copy academic report in Microsoft Word (.docx) format
conforming to the strict university submission formatting specifications:
- Font Type: Tahoma
- Font Size: 10 pt
- Line Spacing: 1.15
- Text Alignment: Justify
"""

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Page Margins (Normal: 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles Configuration
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Tahoma'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_p(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, color=None):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(space_after)
        if text:
            run = p.add_run(text)
            run.font.name = 'Tahoma'
            run.font.size = Pt(10)
            run.bold = bold
            run.italic = italic
            if color:
                run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Tahoma'
        run.font.size = Pt(13)
        run.bold = True
        run.font.color.rgb = RGBColor(13, 59, 102)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Tahoma'
        run.font.size = Pt(11)
        run.bold = True
        run.font.color.rgb = RGBColor(13, 59, 102)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Tahoma'
            r_pre.font.size = Pt(10)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(13, 59, 102)
        r_text = p.add_run(text)
        r_text.font.name = 'Tahoma'
        r_text.font.size = Pt(10)
        return p

    def add_code_block(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.25)
        run = p.add_run(text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(15, 23, 42)
        # Background shading
        tcPr = p._element.get_or_add_pPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
        tcPr.append(shd)
        return p

    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # ================= COVER / TITLE PAGE =================
    p_univ = add_p("LIMKOKWING UNIVERSITY OF CREATIVE TECHNOLOGY", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, color=RGBColor(13, 59, 102))
    p_univ.runs[0].font.size = Pt(15)

    p_dept = add_p("SIERRA LEONE — DEPARTMENT OF INFORMATION AND COMMUNICATION TECHNOLOGY", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, color=RGBColor(71, 85, 105))
    p_dept.runs[0].font.size = Pt(10.5)

    add_p("----------------------------------------------------------------------------------------------------", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, color=RGBColor(203, 213, 225))

    p_badge = add_p("INDIVIDUAL ASSIGNMENT (10% OF MODULE TOTAL)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12, color=RGBColor(13, 59, 102))
    p_badge.runs[0].font.size = Pt(11)

    p_title = add_p("STACKS IMPLEMENTATION:\nMATHEMATICAL EXPRESSION EVALUATOR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8, color=RGBColor(15, 23, 42))
    p_title.runs[0].font.size = Pt(14)

    p_sub = add_p("A Stack-Based Parsing and Evaluation System for Text-Delimited Mathematical Expressions", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=28, color=RGBColor(100, 116, 139))
    p_sub.runs[0].font.size = Pt(10.5)

    # Metadata Table
    table_meta = doc.add_table(rows=7, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False

    meta_data = [
        ("Course Code & Title:", "DCOMP320 — Data Structures and Algorithm"),
        ("Assignment Name:", "Stacks Implementation (Expression Evaluation from File)"),
        ("Student Name:", "Osman Kaimapo Momoh"),
        ("Academic Semester:", "Semester 03 & 05 (September 2026 – February 2027)"),
        ("Examiner / Lecturer:", "Amandus Benjamin Coker (amandus.bcoker@limkokwing.edu.sl)"),
        ("Checked By:", "Sheik Umar Kanu"),
        ("Submission Date:", "October 2026"),
    ]

    for i, (k, v) in enumerate(meta_data):
        row = table_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.font.name = 'Tahoma'
        r0.font.size = Pt(10)
        r0.bold = True
        r0.font.color.rgb = RGBColor(13, 59, 102)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.name = 'Tahoma'
        r1.font.size = Pt(10)
        r1.bold = (k in ["Student Name:", "Course Code & Title:"])

        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")

    add_p("", space_after=24)
    add_p("Submitted in partial fulfillment of the assessment requirements for DCOMP320. Formatted strictly in accordance with official university submission instructions: Tahoma font, 10 pt size, 1.15 line spacing, and justified alignment.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, color=RGBColor(100, 116, 139))

    doc.add_page_break()

    # ================= 2. INTRODUCTION =================
    add_h1("2. Introduction")
    add_p("The evaluation of mathematical expressions is a foundational topic in data structures, computer theory, and language interpreter architecture. In human communication, arithmetic calculations are represented in infix notation, where operators sit between operands (such as 3 + 5 * 2). While straightforward for human inspection, infix notation presents substantial computational ambiguity because the order of operations depends not on simple left-to-right scanning, but on operator precedence hierarchy, left-to-right associativity rules, and parenthetical subexpression groupings.")
    add_p("Computing hardware evaluates linear instruction streams and cannot evaluate precedence-governed infix expressions in a single sequential pass without an auxiliary data structure. The Stack abstract data type (ADT), governed by the Last-In, First-Out (LIFO) protocol, provides the ideal mechanism for transforming, tracking, and calculating such expressions efficiently.")
    add_p("The core objectives of this assignment are as follows:")
    add_bullet("Implement a robust, custom Stack class in Python offering complete LIFO primitives: push, pop, peek, is_empty, and size.", "1. Object-Oriented Stack: ")
    add_bullet("Read multiple mathematical expressions from an input file (input.txt), where individual expressions are separated by line dividers (e.g., -----).", "2. External File Ingestion: ")
    add_bullet("Apply Dijkstra's classic Shunting-Yard algorithm (infix-to-postfix transformation) combined with a stack-based postfix evaluator to evaluate each mathematical expression accurately.", "3. Stack-Based Evaluation Engine: ")
    add_bullet("Write the calculated results into an output file (output.txt), replacing expressions with their computed values while preserving the exact divider format.", "4. Formatted File Output: ")
    add_bullet("Conduct comprehensive testing, empirical validation, and provide professional documentation and Git version control.", "5. Verification & Documentation: ")

    # ================= 3. DATA STRUCTURES USED =================
    add_h1("3. Data Structures Used")
    add_h2("3.1 Detailed Description of the Stack Data Structure")
    add_p("A Stack is a linear, dynamic data structure governed strictly by the Last-In, First-Out (LIFO) access principle. In a stack, elements are added and removed exclusively at one designated end, termed the top of the stack. The opposite fixed boundary is termed the base.")
    add_p("The abstract data type is defined by five standard primitive operations:")
    add_bullet("Inserts an element onto the top of the stack. In a dynamic-array-backed implementation (such as Python's list), push exhibits O(1) amortized time complexity.", "• push(item): ")
    add_bullet("Removes and returns the element at the top. Invoking pop on an empty stack raises a StackUnderflowError exception. Runs in O(1) time.", "• pop(): ")
    add_bullet("Observes and returns the top element without removal, operating in O(1) time.", "• peek(): ")
    add_bullet("Returns a boolean indicating whether the stack contains zero elements (O(1)).", "• is_empty(): ")
    add_bullet("Returns the total integer count of elements currently stored on the stack (O(1)).", "• size(): ")

    add_h2("3.2 How the Stack is Used to Evaluate Expressions")
    add_p("The system evaluates mathematical expressions using a coordinated two-stage stack architecture:")
    add_p("Stage 1: Infix to Postfix Conversion (Dijkstra's Shunting-Yard Algorithm)")
    add_p("In Postfix notation (Reverse Polish Notation), operators strictly follow their operands, eliminating all parentheses and precedence ambiguity. An Operator Stack is utilized during conversion:")
    add_bullet("Operands (integers and floating-point numbers) bypass the stack and append directly to the postfix output stream.")
    add_bullet("Left parentheses '(' are pushed unconditionally onto the operator stack, demarcating the boundary of a nested subexpression.")
    add_bullet("Right parentheses ')' trigger continuous popping of operators from the stack to the output stream until the matching '(' is encountered and removed.")
    add_bullet("When an operator arrives (+, -, *, /), operators currently atop the stack with greater or equal precedence are popped to output before the new operator is pushed.")

    add_p("Stage 2: Postfix Evaluation (Operand Stack)")
    add_p("The converted postfix token list is then evaluated in a single forward pass using an Operand Stack:")
    add_bullet("Whenever a numerical operand is encountered, it is pushed onto the operand stack.")
    add_bullet("Whenever an operator is encountered, the top two values are popped: the first popped value becomes the right operand (b), and the second popped value becomes the left operand (a). The arithmetic calculation a op b is evaluated, and the result is pushed back onto the stack.")
    add_bullet("Upon processing all tokens, the final remaining value atop the operand stack is popped as the definitive mathematical answer.")

    add_h2("3.3 Discussion on the Importance of Stack Data Structures in Computing")
    add_p("Stacks are fundamental across all layers of modern computer systems:")
    add_bullet("Modern microprocessors and programming language runtimes allocate stack frames during subroutine calls to preserve instruction pointers, return addresses, parameter bindings, and local variable scopes. This enables recursion.", "• Call Stack & Function Execution: ")
    add_bullet("Compilers and interpreters employ deterministic shift-reduce stack parsers (such as LR and LALR parsers) to validate grammatical correctness and assemble abstract syntax trees.", "• Compiler Syntax Parsing: ")
    add_bullet("Depth-First Search (DFS) graph traversals, backtracking engines for constraint satisfaction, and maze-solving algorithms use stacks to store decision frontiers.", "• Backtracking & Graph Algorithms: ")
    add_bullet("Application-level undo and redo features maintain state diffs on dedicated stacks, permitting seamless reversal of user actions.", "• State Reversal (Undo/Redo): ")

    # ================= 4. PROGRAM DESIGN =================
    add_h1("4. Program Design")
    add_h2("4.1 Architecture Overview")
    add_p("The software architecture is modularized into four decoupled components: the Stack ADT container, the ExpressionEvaluator engine (comprising the lexical tokenizer, Shunting-Yard converter, and postfix evaluator), the File Processing layer (streaming I/O and separator preservation), and the Command-Line Interface.")

    add_h2("4.2 Description of Key Functions")
    # Table of key functions
    table_fn = doc.add_table(rows=10, cols=3)
    table_fn.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_fn.autofit = False

    fn_headers = ["Function / Method", "Scope / Class", "Description"]
    for j, h in enumerate(fn_headers):
        cell = table_fn.rows[0].cells[j]
        set_cell_background(cell, "0D3B66")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Tahoma'
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    fn_data = [
        ("push(item)", "Stack", "Appends item to the top of stack in O(1) amortized time."),
        ("pop()", "Stack", "Removes and returns top element; raises StackUnderflowError if empty."),
        ("peek()", "Stack", "Returns top element without modifying stack state."),
        ("is_empty()", "Stack", "Returns boolean True if stack holds zero elements."),
        ("tokenize(expr)", "ExpressionEvaluator", "Extracts numbers, decimals, operators, and handles unary negative values."),
        ("infix_to_postfix(tokens)", "ExpressionEvaluator", "Converts infix token stream to postfix using Operator Stack and precedence rules."),
        ("evaluate_postfix(tokens)", "ExpressionEvaluator", "Evaluates postfix tokens using Operand Stack; validates against zero division."),
        ("format_result(val)", "ExpressionEvaluator", "Formats whole numbers cleanly as integers (e.g., 13 instead of 13.0)."),
        ("process_file(in, out)", "Global File I/O Engine", "Streams input.txt, evaluates expressions, preserves delimiters, and writes output.txt.")
    ]

    col_widths = [Inches(2.2), Inches(1.8), Inches(2.5)]
    for i, row_data in enumerate(fn_data, start=1):
        row = table_fn.rows[i]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = col_widths[j]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Tahoma'
            r.font.size = Pt(9)
            set_cell_background(cell, "F8FAFC" if i % 2 == 1 else "FFFFFF")

    add_h2("4.3 Flowchart and Pseudocode")
    add_p("Algorithm 1: Infix to Postfix Conversion (Shunting-Yard)")
    add_code_block(
"""Algorithm InfixToPostfix(tokens):
    output = empty list; op_stack = new Stack()
    For each token in tokens:
        If token is number: output.append(token)
        Else If token == '(': op_stack.push(token)
        Else If token == ')':
            While not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            If op_stack.is_empty(): Throw Error("Mismatched parentheses")
            op_stack.pop() // Discard '('
        Else If token in {'+', '-', '*', '/'}:
            While not op_stack.is_empty() and op_stack.peek() != '(' and
                  Precedence(op_stack.peek()) >= Precedence(token):
                output.append(op_stack.pop())
            op_stack.push(token)
    While not op_stack.is_empty():
        output.append(op_stack.pop())
    Return output"""
    )

    add_p("Algorithm 2: Postfix Expression Evaluation")
    add_code_block(
"""Algorithm EvaluatePostfix(postfix_tokens):
    val_stack = new Stack()
    For each token in postfix_tokens:
        If token is number: val_stack.push(ParseNumber(token))
        Else If token in {'+', '-', '*', '/'}:
            If val_stack.size() < 2: Throw Error("Insufficient operands")
            b = val_stack.pop(); a = val_stack.pop()
            If token == '+': res = a + b
            Else If token == '-': res = a - b
            Else If token == '*': res = a * b
            Else If token == '/':
                If b == 0: Throw Error("Division by zero")
                res = a / b
            val_stack.push(res)
    Return val_stack.pop()"""
    )

    # ================= 5. TESTING AND RESULTS =================
    add_h1("5. Testing and Results")
    add_h2("5.1 Explanation of Testing Methodology")
    add_p("The software was verified using a three-tier quality assurance suite:")
    add_bullet("17 automated test cases under Python's official unittest library testing stack invariants, underflow, operator precedence, associativity, parentheses, decimals, negatives, and zero division.", "1. Automated Unit Tests: ")
    add_bullet("Verifying that input.txt is ingested, expressions computed, delimiter lines preserved, and output.txt written.", "2. File I/O Integration Tests: ")
    add_bullet("13 complex expressions validating multi-digit numbers, division by zero, non-integer division, and syntax error recovery.", "3. Comprehensive Boundary Tests: ")

    add_h2("5.2 Discussion of Results: input.txt and output.txt")
    add_p("Running the application on the required input.txt:")
    add_code_block("3 + 5 * 2\n-----\n(8 / 4) + 7 * 2\n-----\n10 - (2 + 3) * 4")
    add_p("Produced the generated output.txt:")
    add_code_block("13\n-----\n16\n-----\n-10")

    add_p("Step-by-Step Analysis:")
    add_bullet("Multiplication takes precedence over addition: 5 * 2 = 10, then 3 + 10 = 13. Cleanly matches assignment example.", "• Expression 1 (3 + 5 * 2 = 13): ")
    add_bullet("Parentheses evaluate first: (8 / 4) = 2. Then multiplication: 7 * 2 = 14. Finally addition: 2 + 14 = 16. Note: In the assignment brief image, the example output displays 17 or 16. Rigorous mathematical evaluation confirms that (8 / 4) + 7 * 2 is strictly 16. If 17 was intended, the subexpression would have been (6 / 2) + 7 * 2 = 17 or (9 / 3) + 7 * 2 = 17. The program rigorously yields 16.", "• Expression 2 ((8 / 4) + 7 * 2 = 16): ")
    add_bullet("Parentheses evaluate first: (2 + 3) = 5. Then multiplication: 5 * 4 = 20. Then subtraction: 10 - 20 = -10. Exactly matches assignment example.", "• Expression 3 (10 - (2 + 3) * 4 = -10): ")

    add_h2("5.3 Empirical Test Matrix")
    test_cases = [
        ("TC-01", "3 + 5 * 2", "13", "13", "PASS"),
        ("TC-02", "(8 / 4) + 7 * 2", "16", "16", "PASS"),
        ("TC-03", "10 - (2 + 3) * 4", "-10", "-10", "PASS"),
        ("TC-04", "100 + 250 * 2", "600", "600", "PASS"),
        ("TC-05", "20 / 4 + 3 * 2", "11", "11", "PASS"),
        ("TC-06", "10 - 4 - 2 (Associativity)", "4", "4", "PASS"),
        ("TC-07", "((2 + 3) * (4 + 1)) / 5", "5", "5", "PASS"),
        ("TC-08", "10.5 + 4.5 * 2 (Decimals)", "19.5", "19.5", "PASS"),
        ("TC-09", "-5 + 10 (Unary Minus)", "5", "5", "PASS"),
        ("TC-10", "-(4 + 6) * 2", "-20", "-20", "PASS"),
        ("TC-11", "7 / 2 (Floating division)", "3.5", "3.5", "PASS"),
        ("TC-12", "25 / 0 (Zero division)", "Error: Division by zero", "Error: Division by zero", "PASS"),
        ("TC-13", "(5 + 2 * 3 (Unclosed bracket)", "Error: Mismatched parentheses", "Error: Mismatched parentheses", "PASS"),
    ]

    table_tests = doc.add_table(rows=len(test_cases) + 1, cols=5)
    table_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tests.autofit = False

    t_headers = ["ID", "Expression Tested", "Expected", "Observed", "Status"]
    t_widths = [Inches(0.8), Inches(2.2), Inches(1.4), Inches(1.4), Inches(0.7)]

    for j, h in enumerate(t_headers):
        cell = table_tests.rows[0].cells[j]
        cell.width = t_widths[j]
        set_cell_background(cell, "0D3B66")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = 'Tahoma'
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, (tid, expr, exp, obs, st) in enumerate(test_cases, start=1):
        row = table_tests.rows[i]
        vals = [tid, expr, exp, obs, st]
        for j, v in enumerate(vals):
            cell = row.cells[j]
            cell.width = t_widths[j]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(v)
            r.font.name = 'Tahoma'
            r.font.size = Pt(9)
            if j == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            set_cell_background(cell, "F8FAFC" if i % 2 == 1 else "FFFFFF")

    # ================= 6. CONCLUSION =================
    add_h1("6. Conclusion")
    add_p("The project fulfilled every functional and pedagogical specification prescribed for DCOMP320. By combining a custom Stack class with Dijkstra's Shunting-Yard conversion and Postfix evaluation, mathematical expressions are evaluated with complete precedence and parenthesis integrity. The system correctly replaces expressions with computed results in output.txt while preserving all delimiter lines. All 17 automated tests achieved a 100% pass rate.")
    add_h2("6.1 GitHub Repository & Collaboration Setup")
    add_p("In adherence to Section D.b.6 of the assignment brief:")
    add_bullet("The full project codebase is tracked with Git, including source files, input/output files, tests, and documentation.", "1. Git Tracking: ")
    add_bullet("Hosted on GitHub under the student's repository.", "2. Remote Repository: ")
    add_bullet("The examiner, Amandus Benjamin Coker (amandus.bcoker@limkokwing.edu.sl), is invited as an official collaborator under Repository Settings > Collaborators.", "3. Examiner Collaborator: ")

    # ================= 7. REFERENCES =================
    add_h1("7. References")
    refs = [
        "Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Boston, MA: Addison-Wesley.",
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms (4th ed.). Cambridge, MA: The MIT Press.",
        "Dijkstra, E. W. (1961). Algol 60 translation: An Algol 60 translator for the X1 and Making a translator for ALGOL 60. Mathematisch Centrum Amsterdam, Report MR 35/61.",
        "Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). Data Structures and Algorithms in Python. Hoboken, NJ: John Wiley & Sons.",
        "Knuth, D. E. (1997). The Art of Computer Programming, Volume 1: Fundamental Algorithms (3rd ed.). Boston, MA: Addison-Wesley.",
        "Python Software Foundation. (2026). Python 3 Standard Library Documentation: Built-in Types and unittest Framework. https://docs.python.org/3/"
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(r)
        run.font.name = 'Tahoma'
        run.font.size = Pt(9.5)

    output_path = "REPORT.docx"
    doc.save(output_path)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_report()
