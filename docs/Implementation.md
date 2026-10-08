# Assignment 01: Calculator App

Name: [ADD YOUR NAME]

Student ID: [ADD YOUR STUDENT ID]

Course: CSC 4360 — Undergraduate

Test date: October 7, 2026

This project follows the CSC 4360 undergraduate pathway. The comparisons use
actual Gemini and Codex responses from October 7, 2026. The assignment's named
options are Gemini, ChatGPT, and Copilot, so using Codex as the second agent
needs instructor acceptance. No graduate extension is included.

## App overview

The goal was to make a calculator that is easy to follow. The main screen has
a result display, number buttons, four operators, an equals button, and an AC
button. A smaller line above the result shows the operation, so it is clear
which numbers produced the answer. The layout stays narrow on larger screens
and scrolls when there is not enough room.

The calculation flow uses two numbers and one operator. For example, entering
8, multiplication, 7, and equals gives 56. The app also accepts decimal input
and prevents a second decimal point in the same number. It is a basic
calculator, so it does not parse a long expression.

The main code is in lib/main.dart. CalculatorApp controls the theme, and
CalculatorPage controls input and calculations. Keeping these separate means
that changing the theme does not reset a calculation.

## Three enhanced features implemented

Theme toggle: The switch at the top changes between light and dark themes.
The display, buttons, background, and message colors come from the active
ColorScheme. MaterialApp uses a 250-millisecond theme transition. The test
starts 6 +, changes the theme, then enters 4 =. The result stays correct at 10.

Clear/all clear: AC calls _clear(), which resets the input, stored operand,
operator, operation text, error, and input/result flags. Clearing only the
visible text would leave part of the old calculation behind. The test enters
9 ×, presses AC, and then enters 2 + 3 =. The answer is 5.

Error handling: Division by zero and incomplete operations show a short
message explaining what happened and how to restart. _showError() clears the
calculation before storing that message. A number starts a fresh calculation,
and AC also clears the error. After 9 ÷ 0 =, entering 4 + 2 = gives 6.

These are the three enhanced features selected from the undergraduate menu.
Decimal input is an extra convenience; it is not being counted as one of
those three features.

## 01. State and architecture

The app stores _input as text because a value such as 0. needs to stay visible
while the number is being typed. It also stores _firstOperand, _operator, and
flags describing whether the next digit starts a new input and whether the
current display is a result. _error holds the recovery message. The theme
flag belongs to CalculatorApp rather than the calculation page.

There is no separate current resultText. _calculate() puts the formatted
result into _input, which is also what the screen reads. _expression keeps
the short operation label because the operands are cleared after a completed
calculation. Button colors and spoken labels are calculated when the widgets
are built instead of being copied into state.

For longer expressions, the next step would be to move calculation logic
into a separate Dart class with a defined evaluation rule. History would
need a list of completed calculation records. A history list should store
the equation and result together so that reusing an answer does not depend
on the current display text.

## 02. Correctness under pressure

Division by zero produces a recovery message instead of an infinite result.
Pressing equals without a complete calculation also gives a message. If the
second number has not started, another operator replaces the first one. That
means 8 + × 2 = uses multiplication and gives 16. Once the second number is
entered, another operator asks the user to press equals first.

A digit after a completed result starts a new calculation. An operator after
a result uses that result as the first number. For example, 8 × 7 = + 4 =
gives 60, while entering 3 after that displays 3. Pressing equals again
leaves the existing result unchanged.

The tests compare exact expected display values. Checking that the display
is merely nonempty would miss a wrong but believable answer. The arithmetic
test covers addition, subtraction, multiplication, and division, including
zero, negative results, and decimal operations. The reset and recovery tests
check the next calculation too, since a leftover operator could cause a bug
that is invisible immediately after clearing.

## 03. Accessibility is behavior

The operator buttons have spoken labels such as Multiply and Divide instead
of depending on how a screen reader pronounces a symbol. AC is labeled All
clear, and the theme switch is labeled Dark theme. The display and status
message use live regions so changes can be exposed to accessibility tools.
Each calculator button includes a semantic tap action.

Buttons have a minimum height of 64 logical pixels. The automated Android
tap-target and labeled-target checks passed. A separate test uses a
320-by-568 logical-pixel screen with text enlarged to 200 percent. It scrolls
to the needed controls, completes 8 × 7 =, and checks that no layout exception
occurs. Errors have written explanations, so color is not the only clue.

These checks verify labels, target sizes, and layout behavior. They do not
replace listening to the app with TalkBack on a device. Manual TalkBack
testing remains a check to complete before submission.

## 04. Performance without visual loss

If tapping felt slow on an older phone, the first step would be to reproduce
it in a profile build and inspect the frame timing in Flutter DevTools. The
useful measurements would be startup time, slow frames during tapping, and
frames during the theme transition. The same tap sequence should be used
before and after a change so the comparison is fair.

The app does very little work per tap: it changes a few state values and
performs one calculation. There is no network request or expression parser
in that path. If rebuilds became expensive, the button widget and display
could be split into smaller widgets after the timing results show a problem.
Useful button feedback and the theme transition should stay in place unless
measurements show they are causing the delay. No older-device performance
measurements were collected, so there is no claimed speed improvement.

## 05. AI output under review

The supplied assignment lists this heading without a separate question. This
section explains how generated suggestions were checked against the
implementation instead of being treated as proof.

Both agents treated consecutive operators as an error. I did not use that
rule because this app lets the user change a pending operator before typing
the second number. The test 5 + × 3 = gives 15, and 5 + × 2 = gives 10.
These results match _chooseOperator(), which replaces the pending operator.
An error is still shown if another operator is pressed after the second
number has already started.

Advice about accessibility also needs a clear limit. A semantic label and a
passing widget test show that the label exists; they do not prove that the
TalkBack reading order feels natural. Similarly, Gemini suggested limiting
repeating decimals to prevent memory overflow. In this app, Dart double
arithmetic has finite precision; formatting to 12 significant digits makes
the display readable. It is not an overflow fix. The test 1 ÷ 3 = displays
0.333333333333 and checks the actual formatting decision.

## 06. AI advice, trade-offs, and maintainability

This project uses one _button() helper for the calculator controls. That keeps
their sizing, labels, and colors consistent. It also uses StatefulWidget and
setState because the screen has a small amount of local state. No expression
parser or state-management package was added. The generated starter's
Cupertino icon dependency is still present, although this screen uses
Material icons.

An alternative would be to use an expression package or a separate state
library. Those options could help with a larger calculator, but they add
concepts and setup that the current two-number flow does not need. The first
refactor for another developer would be moving the arithmetic and input
rules into a small Dart class. That would allow direct unit tests while
keeping the widgets focused on the screen.

The exact question sent to both agents was: For my calculator implementation,
what trade-off should I make between reusing widgets, adding dependencies,
and keeping the project small?

Gemini recommended reusing a button component, avoiding early over-abstraction,
and saving expression libraries for more complicated calculators. Codex also
recommended a reusable button and minimal dependencies, but stressed separating
calculation logic from the screen and accepting some repetition for clarity.
Both responses were obtained on October 7, 2026.

I kept the shared _button() helper because the controls need the same size
and labels. I also kept StatefulWidget and setState for this small screen.
Codex's suggestion to separate the logic is a useful next refactor, but the
current methods remain in CalculatorPage and are checked through widget tests.
Gemini's blanket statements about packages causing bloat or security problems
are too broad. No package-size comparison was measured, and the project still
depends on Flutter and the starter icon package. A new dependency should solve
a specific requirement rather than be added just to reduce a few lines.

## Required AI Test Drive records

Agents and date: Google Gemini, shown as 3.5 Flash-Lite in its interface, and
an independent OpenAI Codex agent; October 7, 2026. Each received the same
unchanged Bug Hunt and State Design prompts, producing four real responses.
They also answered the question 06 trade-off prompt. Full response records
are in docs/AI_Test_Drive_Records.md in the repository.

ChatGPT stopped at browser verification, and Copilot required sign-in. Neither
returned an answer. Codex is recorded under its actual name; it is not labeled
as ChatGPT. Instructor acceptance of this substitute remains necessary because
the guide lists Gemini, ChatGPT, and Copilot as its named choices.

Bug Hunt prompt: For a two-operand calculator with +, −, ×, and ÷, propose six
test cases with exact inputs and expected outcomes. Include normal, boundary,
and invalid sequences. Mark which cases require optional error handling or
graduate decimal support. Do not write code.

Gemini's six suggestions were 5 + 3 → 8, 2.5 × 4 → 10, 1 ÷ 3 → a repeating
decimal, 5 ÷ 0 → Error/Undefined/Infinity, 5 + × 3 → an error, and 2.2.1 + 4
→ a malformed-input error. Its decimal-support label said "Gradual," which
appears to be a wording mistake. Codex suggested 12 + 7 → 19, 4 − 9 → −5,
0 × 85 → 0, 7 ÷ 2 → 3.5, 8 ÷ 0 → an error, and 5 + × 2 → an error.
Equals was pressed to complete each operation when testing these suggestions.

The normal arithmetic suggestions were useful and passed. Both agents
included zero-division tests, but Gemini allowed Infinity as one outcome.
I rejected Infinity because error handling is one of my chosen features:
5 ÷ 0 and 8 ÷ 0 both show a recovery message. I also rejected both agents'
repeated-operator assumptions for the replacement behavior explained above.
For Gemini's malformed decimal, the second decimal point is ignored by
_enterDigit(), so tapping 2.2.1 + 4 = displays 6.21. The app prevents the
malformed number instead of accepting it and failing during parsing.

Codex labeled 7 ÷ 2 as requiring graduate decimal-result support. I did not
use that label to limit undergraduate division: integer operands can produce
a fractional answer, and the test correctly displays 3.5. Decimal input is
an extra convenience here, separate from the three selected enhancements.

State Design prompt: A calculator stores displayText, firstOperand,
pendingOperator, resultText, and isError. Which values need to be stored,
which can be derived, and what bug could happen if resultText and displayText
drift apart? Suggest one test that catches it.

Both agents recommended storing the current input text and pending operation,
and removing a separate resultText when it duplicates the display. Both
described the risk of showing one number while calculating with an older
result. Gemini wanted isError stored as a flag; Codex also allowed deriving
it from a stored error object. I used _error as the stored message and check
whether it is null, avoiding another error flag that could drift out of sync.

Gemini's test completes 5 + 3 = 8, types 9, and then checks 9 + 1 = 10.
Codex's test completes 2 + 3 = 5 and then checks × 2 = 10. Both sequences
passed in the widget test named "Check real agent suggestions against
calculator behavior." This app stores the formatted result in _input and
reuses it after equals, so Codex's sequence is supported without adding
long-expression evaluation. Gemini supplied JavaScript test code; I used
the suggested sequence in a Flutter widget test rather than copying code
for a different framework.

The checks verified useful claims and also caught advice that did not match
the chosen input rules. The agent responses helped choose additional tests;
the passing tests and source code support the final decisions.

## Challenges and limits

The main design challenge was deciding what the same button means at different
points in a calculation. A digit after an operator should begin the second
number, but a digit after a result should begin a new calculation. Keeping
those states explicit makes the behavior easier to follow and test.

Another issue is decimal precision. Dart double values can produce a result
such as 0.30000000000000004 for 0.1 + 0.2. _format() limits the displayed
answer to 12 significant digits, so this example displays 0.3. This is a
display choice, not exact decimal arithmetic. Reusing a result also reuses
the rounded display value. A financial calculator would need a different
number representation.

Release testing also caught a rendering problem. The emulator exposed the
buttons to the test tool, but the saved screen image was black. Switching
the Android manifest to Flutter's compatibility renderer made it possible
to check the visible screen as well as the calculations. That option is
deprecated for future Flutter releases, so an SDK upgrade should include
another rendering check. The calculator logic did not need to change.

## Verification evidence

flutter analyze: no issues found.

flutter test: all 11 widget test groups passed.

flutter build apk --release: completed successfully.

The release APK was installed on the Pixel_4a Android emulator. Ten release
interaction checks passed, including the four arithmetic operations, decimal
addition, repeated-operator replacement, clearing a pending operation,
division-by-zero recovery, incomplete input, and a theme change during input.

The recorded results are in evidence/analyze.txt, evidence/widget-tests.txt,
and evidence/android-release-checks.json. The screenshot appendix uses
captures from the installed release app. Manual TalkBack listening and
older-device performance measurements remain unverified.

## References

Flutter widget testing: https://docs.flutter.dev/cookbook/testing/widget/introduction

Flutter accessibility testing: https://docs.flutter.dev/ui/accessibility/accessibility-testing

Flutter accessibility guidance: https://docs.flutter.dev/ui/accessibility

Flutter rendering options: https://docs.flutter.dev/perf/impeller
