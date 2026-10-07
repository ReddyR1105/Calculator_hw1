# Required two-agent Test Drive

Send each prompt below unchanged to both Gemini and ChatGPT. Record the dates
and keep the actual responses. The assignment requires two prompts across
two different agents, so four real responses are needed.

## Prompt 01: Bug hunt

For a two-operand calculator with +, −, ×, and ÷, propose six test cases with exact inputs and expected outcomes. Include normal, boundary, and invalid sequences. Mark which cases require optional error handling or graduate decimal support. Do not write code.

Gemini test date: [TO COMPLETE]

Gemini response: [PASTE ACTUAL RESPONSE]

ChatGPT test date: [TO COMPLETE]

ChatGPT response: [PASTE ACTUAL RESPONSE]

Comparison: [Explain a useful agreement or disagreement. Identify advice
accepted or rejected and a specific check used to verify it.]

Verification already available in this project:

- `8 × 7 =` displays `56`.
- `7 ÷ 2 =` displays `3.5`.
- `9 ÷ 0 =` gives a recoverable message; `4 + 2 =` afterward displays `6`.
- `5 + =` gives an incomplete-input message.
- `8 + × 2 =` displays `16`, because the pending operator is replaced.
- `9 × AC 2 + 3 =` displays `5`, because AC removes the pending calculation.

Source: `test/widget_test.dart`, `evidence/widget-tests.txt`, and
`evidence/android-release-checks.json`. Match a real agent's claim to the
relevant observation; do not describe these observations as an agent response.

## Prompt 03: State design

A calculator stores displayText, firstOperand, pendingOperator, resultText, and isError. Which values need to be stored, which can be derived, and what bug could happen if resultText and displayText drift apart? Suggest one test that catches it.

Gemini test date: [TO COMPLETE]

Gemini response: [PASTE ACTUAL RESPONSE]

ChatGPT test date: [TO COMPLETE]

ChatGPT response: [PASTE ACTUAL RESPONSE]

Comparison: [Record what each agent said about duplicated display/result state,
then explain what matches this app and what does not.]

Verification available: this app uses `_input` as its only current numeric
display value. The result is written back to `_input`. The test named
"Digits start fresh after a result and operators reuse results" verifies
`8 × 7 = + 4 =` displays `60`, then entering `3` displays `3`.

## Reflection question 06

Send this question unchanged to the same two agents:

For my calculator implementation, what trade-off should I make between reusing widgets, adding dependencies, and keeping the project small?

Record both actual responses and test dates. Compare the advice with the
shared `_button` helper and the app's use of `StatefulWidget` and `setState`.
The runtime dependencies currently include Flutter and the starter project's
Cupertino icon package; no expression parser or state-management package was
added. Do not claim an agent recommended an option without its actual response.
