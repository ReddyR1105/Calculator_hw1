# Assignment 01: Calculator App

Name: [ADD YOUR NAME]

Student ID: [ADD YOUR STUDENT ID]

Course: [CONFIRM CSC 4360 OR CSC 6370]

Test date: October 7, 2026

Draft items to finish: confirm the course level, add name and ID, and complete
the required comparisons using actual responses from two agents. The current
app covers the undergraduate feature menu. The graduate pathway would need
three advanced features before submission.

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
those three features. The course level still needs confirmation.

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
section explains how generated suggestions would be checked against the
implementation instead of being treated as proof.

For example, a suggestion that two-operand calculators should replace a
pending operator needs a specific input sequence to verify it. The test
8 + × 2 = confirms that this app displays 16. Another useful check is whether
AC clears the stored first operand. Entering 9 × AC 2 + 3 = gives 5, which
supports the reset behavior in _clear().

Advice about accessibility also needs a clear limit. A semantic label and a
passing widget test show that the label exists; they do not prove that the
TalkBack reading order feels natural. Any agent advice included in the final
comparison should identify the actual response, explain what was accepted or
rejected, and point to a test or source-code detail that supports the choice.
The real agent responses still need to be recorded.

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

Required agent comparison: [ADD THE ACTUAL GEMINI AND CHATGPT RESPONSES TO
THE TRADE-OFF QUESTION, THEIR TEST DATES, AND THE COMPARISON. DO NOT ATTRIBUTE
THE DESIGN EXPLANATION ABOVE TO AN AGENT WITHOUT ITS REAL RESPONSE.]

## Required AI Test Drive records

Use docs/AI_Test_Drive_Worksheet.md to send the Bug Hunt and State Design
prompts unchanged to both Gemini and ChatGPT. Two prompts sent to two agents
produce four responses. The worksheet preserves the prompts and lists real
project tests that can verify a claim.

Bug Hunt comparison: [ADD BOTH ACTUAL RESPONSES, DATES, AN AGREEMENT OR
DISAGREEMENT, WHAT WAS ACCEPTED OR REJECTED, AND ONE VERIFIED CLAIM.]

State Design comparison: [ADD BOTH ACTUAL RESPONSES, DATES, AN AGREEMENT OR
DISAGREEMENT, WHAT WAS ACCEPTED OR REJECTED, AND ONE VERIFIED CLAIM.]

Existing evidence can support a claim, but it cannot stand in for the missing
responses. No responses or agent-to-agent comparisons have been invented.

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

flutter test: all 10 widget test groups passed.

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
