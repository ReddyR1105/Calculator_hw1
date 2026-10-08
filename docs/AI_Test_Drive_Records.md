# Actual AI Test Drive records

Test date: October 7, 2026. Agents: Google Gemini (interface model: 3.5 Flash-Lite) and an independent OpenAI workspace assistant.

The prompts below were sent unchanged to both agents. These are their actual responses, including mistakes. No follow-up corrections have been inserted into their answers.

Course requirement note: the guide names Gemini, ChatGPT, and Copilot. The OpenAI workspace assistant is a substitute and needs instructor acceptance. ChatGPT stopped at browser verification and Copilot required sign-in; neither returned an answer. OpenAI is the provider label for the actual workspace assistant; these responses did not come from the ChatGPT website.

Comparisons and decisions are in [Implementation.md](Implementation.md). The widget test "Check real agent suggestions against calculator behavior" verifies the arithmetic, input rules, and both state-design test sequences. Results are in [widget-tests.txt](../evidence/widget-tests.txt).

## Prompt 01: Bug Hunt

### Unchanged prompt

For a two-operand calculator with +, −, ×, and ÷, propose six test cases with exact inputs and expected outcomes. Include normal, boundary, and invalid sequences. Mark which cases require optional error handling or graduate decimal support. Do not write code.

### Gemini response

Gemini said
Two-Operand Calculator Test Suite

Below are six test cases designed to evaluate a two-operand calculator supporting addition, subtraction, multiplication, and division. Each case specifies the category, exact input sequence, expected outcome, and any special architectural requirements.

Test Case Summary
Case #	Category	Exact Inputs	Expected Outcome	Special Requirements
1	Normal	5 + 3	8	None (Standard Integer Math)
2	Normal	2.5 × 4	10 (or 10.0)	Gradual Decimal Support
3	Boundary	1 ÷ 3	0.3333... (or precision cap)	Gradual Decimal Support & Precision Handling
4	Boundary	5 ÷ 0	Error / Undefined / Infinity	Optional Error Handling
5	Invalid	5 + × 3	Error / Invalid Input Sequence	Optional Error Handling
6	Invalid	2.2.1 + 4	Error / Malformed Operand	Optional Error Handling
Detailed Case Descriptions

Case 1 (Normal Addition): Tests standard two-operand integer entry and basic addition. The expected result is a clean integer (8).

Case 2 (Normal Decimal Multiplication): Tests multiplication involving a decimal operand. Requires gradual decimal support to parse fractional inputs and properly format the resulting product.

Case 3 (Boundary Precision): Tests a repeating decimal outcome (1 ÷ 3). This challenges the display buffer and requires gradual decimal support alongside rounding or truncation limits to prevent memory overflow.

Case 4 (Boundary Division by Zero): Tests the arithmetic rule where a denominator is zero. Requires optional error handling to gracefully catch the operation and display a message (e.g., "Error" or "Undefined") instead of crashing.

Case 5 (Invalid Operator Sequence): Tests consecutive operators (+ followed immediately by ×). Requires optional error handling to lock out or reject the invalid syntax state.

Case 6 (Invalid Malformed Operand): Tests an operand containing multiple decimal points (2.2.1). Requires optional error handling to catch formatting violations during input parsing.

Would you like to explore edge cases involving negative number entry or memory persistence features next?

### OpenAI response

| # | Exact input sequence | Expected outcome | Coverage / requirement |
|---|---|---|---|
| 1 | `12 + 7 =` | `19` | Normal addition |
| 2 | `4 − 9 =` | `−5` | Subtraction producing a negative result |
| 3 | `0 × 85 =` | `0` | Boundary: zero operand |
| 4 | `7 ÷ 2 =` | `3.5` | Division; requires graduate decimal-result support |
| 5 | `8 ÷ 0 =` | Show a division-by-zero error; no numeric result | Invalid operation; requires optional error handling |
| 6 | `5 + × 2 =` | Reject the malformed sequence and show an error | Invalid sequence; requires optional error handling |

Start each case from a cleared calculator. Cases 5–6 assume error handling is implemented; otherwise, record their behavior without treating the proposed error display as mandatory.

## Prompt 03: State Design

### Unchanged prompt

A calculator stores displayText, firstOperand, pendingOperator, resultText, and isError. Which values need to be stored, which can be derived, and what bug could happen if resultText and displayText drift apart? Suggest one test that catches it.

### Gemini response

Gemini said

Here is the breakdown of what needs to be stored versus derived in your calculator state, along with the potential bug and a catch test.

1. Stored vs. Derived Values

Values that need to be stored (Core State):

firstOperand: The first number entered in a binary operation (e.g., 5 in 5 + 3).

pendingOperator: The active operator waiting for a second operand (e.g., +, -, *, /).

isError: A boolean flag indicating if an invalid operation (like division by zero) occurred.

displayText: The active string currently rendered on the screen.

Values that can be derived (Redundant):

resultText: Should ideally be eliminated. Keeping both displayText and resultText as independent state variables creates redundant source-of-truth problems. The screen (displayText) should either reflect the current input or the computed result directly.

2. What Bug Happens if resultText and displayText Drift Apart?

Ghost Inputs & Stale Calculations: If resultText and displayText fall out of sync, the calculator will display one number to the user while performing math with a completely different number in the background.

Example: After calculating 5 + 3 = 8, resultText might retain 8. If the user types a new number 9 (updating displayText to 9, but failing to update resultText), pressing + next could cause the calculator to add 8 instead of 9 to the next operation, resulting in completely wrong arithmetic.

3. Suggested Test to Catch the Bug

Test Name: test_subsequent_input_overwrites_stale_result

JavaScript
test('calculator uses current displayText instead of stale resultText after a completed calculation', () => {
  const calc = new Calculator();
  
  // 1. Complete a calculation: 5 + 3 = 8
  calc.pressDigit('5');
  calc.pressOperator('+');
  calc.pressDigit('3');
  calc.pressEquals();
  expect(calc.displayText).toBe('8');

  // 2. Type a new number immediately without clearing (e.g., typing '9')
  calc.pressDigit('9');
  expect(calc.displayText).toBe('9');

  // 3. Chain another operation: press '+' and '1' then '='
  calc.pressOperator('+');
  calc.pressDigit('1');
  calc.pressEquals();

  // 4. Verify it calculated 9 + 1 = 10, NOT stale 8 + 1 = 9
  expect(calc.displayText).toBe('10');
});

### OpenAI response

- **Store `displayText`:** preserves the current input exactly, including partial entries such as `0.`.
- **Store `firstOperand` and `pendingOperator`:** needed while the user enters the second operand.
- **Store `isError` or an explicit status:** avoid inferring an error from display text. If you store a structured error instead, derive `isError` from it.
- **Derive `resultText`:** if it duplicates the displayed result, remove the independent copy and use one source of truth. Separate storage is justified only if it preserves something distinct, such as calculation history.

If `displayText` shows `5` while `resultText` contains an older value, the next calculation could use a different number from the one the user sees.

**Test:** enter `2 + 3 =`, verify `5`, then enter `× 2 =` and verify `10`. This catches stale result state when chaining is supported.

## Reflection question 06: Trade-off

### Unchanged prompt

For my calculator implementation, what trade-off should I make between reusing widgets, adding dependencies, and keeping the project small?

### Gemini response

Gemini said

Building a calculator project sits at a fascinating intersection of UI design and logic processing. Balancing widget reuse, external dependencies, and project size comes down to the complexity of the calculator you are building.

Reusing Widgets: Consistency vs. Over-Engineering

Pros: Standardizing your UI (such as creating a single, reusable Button component for numbers and operators) keeps your styling uniform and drastically cuts down on repetitive layout code.

Cons: Over-abstracting too early can trap you in rigid component architectures before you fully understand your layout needs.

Rule of thumb: Build a generic button widget only after you find yourself copy-pasting the same button structure three times.

Adding Dependencies: Speed vs. Bloat

Pros: Using an established third-party library for expression parsing or complex math saves you from writing complex algorithms (like the Shunting-yard algorithm) from scratch.

Cons: External packages bloat your bundle size, introduce security vulnerabilities, and risk breaking changes during framework updates.

Rule of thumb: Avoid dependencies for basic arithmetic. Only pull in a library if you are building an advanced scientific or graphing calculator.

Keeping the Project Small: Simplicity vs. Reinventing the Wheel

Pros: A lean codebase means faster compilation, zero "dependency hell," and total control over every single line of code.

Cons: Writing a robust mathematical expression evaluator by hand is time-consuming and notorious for edge-case bugs (like handling order of operations and negative numbers).

Rule of thumb: Lean towards writing a lightweight custom state machine for simple inputs, keeping your footprint minimal.

For standard calculators, reusing custom UI widgets while avoiding heavy math dependencies usually hits the sweet spot. It keeps your codebase tiny, maintainable, and fun to build.

What framework or technology stack are you using to build your calculator?

### OpenAI response

For a small calculator, reuse the framework’s built-in widgets and keep dependencies minimal.

- Use one reusable calculator-button widget for consistent styling and behavior.
- Keep calculation logic separate from the screen so it is easy to test.
- Avoid a third-party package for basic arithmetic or layout. Add one only when a required feature would otherwise need substantial custom code.

Accept a little repetition when it keeps the code clearer. Your target is a small, readable project—not the fewest possible lines or the most generalized design.
