# AI Test Drive prompt index

Completed actual responses are in [AI_Test_Drive_Records.md](AI_Test_Drive_Records.md). Comparisons are in [Implementation.md](Implementation.md).

Both prompts and the question 06 trade-off question were sent unchanged to Google Gemini and an independent OpenAI Codex agent on October 7, 2026. Codex as a substitute needs instructor acceptance because the guide names Gemini, ChatGPT, and Copilot.

## Prompt 01: Bug Hunt

For a two-operand calculator with +, −, ×, and ÷, propose six test cases with exact inputs and expected outcomes. Include normal, boundary, and invalid sequences. Mark which cases require optional error handling or graduate decimal support. Do not write code.

## Prompt 03: State Design

A calculator stores displayText, firstOperand, pendingOperator, resultText, and isError. Which values need to be stored, which can be derived, and what bug could happen if resultText and displayText drift apart? Suggest one test that catches it.

## Reflection question 06: Trade-off

For my calculator implementation, what trade-off should I make between reusing widgets, adding dependencies, and keeping the project small?
