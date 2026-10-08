# Rohan Calculator HW1

Repository: https://github.com/ReddyR1105/Calculator_hw1

A small Flutter calculator for Assignment 01. Enter a number, choose an
operator, enter a second number, and press equals.

The app includes the four arithmetic operations, decimal input, and three
features for CSC 4360 — Undergraduate: a light/dark theme switch, all-clear,
and recoverable error messages.

## Run and check

Built with Flutter 3.47.4 and Dart 3.13.3. Use that Flutter version or newer.

```text
flutter pub get
flutter analyze
flutter test
flutter run
flutter build apk --release
```

The release APK is at `build/app/outputs/flutter-apk/app-release.apk`.
Install it with `adb install -r` or open the APK on an Android device.
The Android package name is `edu.course.calculator_app`.
The standard Flutter development signing key is used for the class APK.

The Android manifest selects Flutter's compatibility renderer because the
course emulator showed a black app surface with Impeller. This opt-out is
supported by the installed Flutter version but is deprecated for future
versions. Recheck the renderer when upgrading Flutter. The relevant Flutter
reference is https://docs.flutter.dev/perf/impeller.

## Button behavior

- AC resets the display, stored operand, operator, result flag, and error.
- Before a second number, tapping another operator replaces the pending one.
- After the second number, press equals before selecting another operator.
- Pressing equals too early gives an explanation. Tap a number or AC to recover.
- Division by zero gives a recoverable message.
- A digit after a result starts over. An operator after a result reuses that result.
- Pressing equals again leaves the result unchanged.
- Only one decimal point is allowed in each input; input is limited to 12 digits.
- Results use 12 significant digits for display. This is a basic calculator,
  so rounded `double` values should not be treated as exact financial arithmetic.

## Project files

- `lib/main.dart`: calculator widgets, input state, arithmetic, and themes.
- `test/widget_test.dart`: arithmetic, reset, error recovery, themes, layout,
  and accessibility checks.
- `evidence/`: analyzer output, test output, release-device observations, and
  screenshots.
- `tools/verify_android.py`: the emulator verification script used in this
  workspace. Change its ADB path and emulator serial for another machine.

Ten automated widget test groups passed on October 7, 2026. The large-text
check uses a 320 x 568 logical-pixel screen at 200% text scaling. Semantics
and tap-target checks passed; manual TalkBack listening and older-device
performance measurements remain separate checks.

## Before submission

Complete the two-agent Test Drive records using real responses and upload
the project to the repository linked above. Confirm the instructor can access
the project files. The three LMS deliverables are `github_link.txt`, the
release APK, and the completed Word implementation document.
