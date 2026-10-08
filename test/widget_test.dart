import 'package:calculator_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

Future<void> press(WidgetTester tester, List<String> buttons) async {
  for (final button in buttons) {
    final finder = find.byKey(Key('button_$button'));
    await tester.ensureVisible(finder);
    await tester.tap(finder);
    await tester.pumpAndSettle();
  }
}

String display(WidgetTester tester) =>
    tester.widget<Text>(find.byKey(const Key('display'))).data!;
String status(WidgetTester tester) =>
    tester.widget<Text>(find.byKey(const Key('status'))).data!;

void main() {
  testWidgets('Four operations, zero, negative results, and decimals', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    final cases = [
      (['1', '2', '+', '8', '='], '20'),
      (['5', '−', '9', '='], '-4'),
      (['8', '×', '7', '='], '56'),
      (['7', '÷', '2', '='], '3.5'),
      (['0', '×', '9', '='], '0'),
      (['0', '.', '1', '+', '0', '.', '2', '='], '0.3'),
      (['2', '.', '5', '−', '1', '.', '2', '='], '1.3'),
      (['1', '.', '5', '×', '2', '.', '4', '='], '3.6'),
      (['7', '.', '5', '÷', '2', '.', '5', '='], '3'),
    ];
    for (final (buttons, expected) in cases) {
      await press(tester, ['AC', ...buttons]);
      expect(display(tester), expected, reason: buttons.join(' '));
    }
  });
  testWidgets('Division by zero gives a message and a digit recovers', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['9', '÷', '0', '=']);
    expect(status(tester), contains('Cannot divide by zero'));
    await press(tester, ['4', '+', '2', '=']);
    expect(display(tester), '6');
    expect(status(tester), isNot(contains('Cannot divide by zero')));
  });
  testWidgets('Incomplete sequences give recoverable messages', (tester) async {
    await tester.pumpWidget(const CalculatorApp());
    for (final buttons in [
      <String>['='],
      ['5', '='],
      ['5', '+', '='],
      ['+'],
    ]) {
      await press(tester, ['AC', ...buttons]);
      expect(status(tester), contains('restart'));
      await press(tester, ['2', '+', '3', '=']);
      expect(display(tester), '5');
    }
  });
  testWidgets('Repeated operators replace the pending operation', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['8', '+', '×', '2', '=']);
    expect(display(tester), '16');
    await press(tester, ['AC', '8', '+', '2', '×']);
    expect(status(tester), contains('Press ='));
  });
  testWidgets('All clear resets the pending operand and operator', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['9', '×', 'AC']);
    expect(display(tester), '0');
    expect(
      tester.widget<Text>(find.byKey(const Key('expression'))).data,
      'Ready',
    );
    await press(tester, ['2', '+', '3', '=']);
    expect(display(tester), '5');
    await press(tester, ['AC', '=']);
    expect(status(tester), contains('Enter two numbers'));
  });
  testWidgets('Digits start fresh after a result and operators reuse results', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['8', '×', '7', '=', '=']);
    expect(display(tester), '56');
    await press(tester, ['+', '4', '=']);
    expect(display(tester), '60');
    await press(tester, ['3']);
    expect(display(tester), '3');
  });
  testWidgets('Only one decimal point per input and input length is bounded', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['.', '5', '.', '2']);
    expect(display(tester), '0.52');
    await press(tester, ['AC', ...List.filled(13, '9')]);
    expect(status(tester), contains('12 digits'));
    await press(tester, ['1']);
    expect(display(tester), '1');
  });
  testWidgets('Theme toggle preserves an unfinished calculation', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['6', '+']);
    await tester.ensureVisible(find.byType(Switch));
    await tester.tap(find.byType(Switch));
    await tester.pumpAndSettle();
    expect(
      Theme.of(tester.element(find.byType(Scaffold))).brightness,
      Brightness.dark,
    );
    await press(tester, ['4', '=']);
    expect(display(tester), '10');
  });
  testWidgets('Narrow screen and large text scroll without overflow', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 568);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
    await tester.pumpWidget(const CalculatorApp());
    await press(tester, ['8', '×', '7', '=']);
    expect(display(tester), '56');
    expect(tester.takeException(), isNull);
  });
  testWidgets('Screen reader labels and Android touch targets', (tester) async {
    final semantics = tester.ensureSemantics();
    await tester.pumpWidget(const CalculatorApp());
    expect(find.bySemanticsLabel('All clear'), findsOneWidget);
    expect(find.bySemanticsLabel('Multiply'), findsOneWidget);
    expect(find.bySemanticsLabel('Display: 0'), findsOneWidget);
    await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
    semantics.dispose();
  });
  testWidgets('Check real agent suggestions against calculator behavior', (
    tester,
  ) async {
    await tester.pumpWidget(const CalculatorApp());
    final cases = [
      (['5', '+', '3', '='], '8'),
      (['2', '.', '5', '×', '4', '='], '10'),
      (['1', '÷', '3', '='], '0.333333333333'),
      (['1', '2', '+', '7', '='], '19'),
      (['4', '−', '9', '='], '-5'),
      (['0', '×', '8', '5', '='], '0'),
      (['5', '+', '×', '3', '='], '15'),
      (['5', '+', '×', '2', '='], '10'),
      (['2', '.', '2', '.', '1', '+', '4', '='], '6.21'),
      (['2', '+', '3', '=', '×', '2', '='], '10'),
      (['5', '+', '3', '=', '9', '+', '1', '='], '10'),
    ];
    for (final (buttons, expected) in cases) {
      await press(tester, ['AC', ...buttons]);
      expect(display(tester), expected, reason: buttons.join(' '));
    }
    for (final first in ['5', '8']) {
      await press(tester, ['AC', first, '÷', '0', '=']);
      expect(status(tester), contains('Cannot divide by zero'));
    }
  });
}
