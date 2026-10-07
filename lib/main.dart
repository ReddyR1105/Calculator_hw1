import 'package:flutter/material.dart';

void main() => runApp(const CalculatorApp());

class CalculatorApp extends StatefulWidget {
  const CalculatorApp({super.key});
  @override
  State<CalculatorApp> createState() => _CalculatorAppState();
}

class _CalculatorAppState extends State<CalculatorApp> {
  bool _darkMode = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculator',
      debugShowCheckedModeBanner: false,
      themeAnimationDuration: const Duration(milliseconds: 250),
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF215C47)),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF91D5B4),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: _darkMode ? ThemeMode.dark : ThemeMode.light,
      home: CalculatorPage(
        darkMode: _darkMode,
        onThemeChanged: (value) => setState(() => _darkMode = value),
      ),
    );
  }
}

class CalculatorPage extends StatefulWidget {
  const CalculatorPage({
    super.key,
    required this.darkMode,
    required this.onThemeChanged,
  });
  final bool darkMode;
  final ValueChanged<bool> onThemeChanged;
  @override
  State<CalculatorPage> createState() => _CalculatorPageState();
}

class _CalculatorPageState extends State<CalculatorPage> {
  String _input = '0';
  double? _firstOperand;
  String? _operator;
  String _expression = '';
  String? _error;
  bool _startNewInput = false;
  bool _hasInput = false;
  bool _showingResult = false;

  void _clear() {
    _input = '0';
    _firstOperand = null;
    _operator = null;
    _expression = '';
    _error = null;
    _startNewInput = false;
    _hasInput = false;
    _showingResult = false;
  }

  void _showError(String message) {
    _clear();
    _error = message;
  }

  void _enterDigit(String digit) {
    // A digit after a result or error starts a fresh calculation.
    if (_showingResult || _error != null) _clear();
    if (_startNewInput) {
      _input = '0';
      _startNewInput = false;
    }
    if (digit == '.') {
      if (!_input.contains('.')) _input += '.';
    } else {
      if (_input.replaceAll('.', '').length >= 12) {
        _showError('Use up to 12 digits. Tap a number to restart.');
        return;
      }
      _input = _input == '0' ? digit : _input + digit;
    }
    _hasInput = true;
  }

  void _chooseOperator(String operation) {
    if (_error != null) return;
    // Before the second number, another operator replaces the first one.
    if (_operator != null && _startNewInput) {
      _operator = operation;
      _expression = '${_format(_firstOperand!)} $operation';
      return;
    }
    if (!_hasInput) {
      _showError('Enter a number first. Tap a number to restart.');
      return;
    }
    if (_operator != null) {
      _showError('Press = before another operation. Tap a number to restart.');
      return;
    }
    _firstOperand = double.parse(_input);
    _operator = operation;
    _expression = '${_format(_firstOperand!)} $operation';
    _startNewInput = true;
    _hasInput = false;
    _showingResult = false;
  }

  String _format(double value) {
    if (value == 0) return '0';
    // Round display text to avoid results such as 0.30000000000000004.
    final rounded = double.parse(value.toStringAsPrecision(12));
    final text = rounded.toString();
    return text.endsWith('.0') ? text.substring(0, text.length - 2) : text;
  }

  void _calculate() {
    if (_error != null || _showingResult) return;
    if (_firstOperand == null || _operator == null || !_hasInput) {
      _showError('Enter two numbers and an operator. Tap a number to restart.');
      return;
    }
    final secondOperand = double.parse(_input);
    final firstOperand = _firstOperand!;
    final operation = _operator!;
    double result;
    switch (operation) {
      case '+':
        result = firstOperand + secondOperand;
      case '−':
        result = firstOperand - secondOperand;
      case '×':
        result = firstOperand * secondOperand;
      case '÷':
        if (secondOperand == 0) {
          _showError('Cannot divide by zero. Tap a number to restart.');
          return;
        }
        result = firstOperand / secondOperand;
      default:
        _showError('Choose a valid operator. Tap a number to restart.');
        return;
    }
    if (!result.isFinite) {
      _showError('Result is too large. Tap a number to restart.');
      return;
    }
    _expression =
        '${_format(firstOperand)} $operation ${_format(secondOperand)} =';
    _input = _format(result);
    _firstOperand = null;
    _operator = null;
    _hasInput = true;
    _startNewInput = false;
    _showingResult = true;
  }

  void _press(String label) {
    setState(() {
      if (label == 'AC') {
        _clear();
      } else if (label == '=') {
        _calculate();
      } else if (['+', '−', '×', '÷'].contains(label)) {
        _chooseOperator(label);
      } else {
        _enterDigit(label);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: colors.surface,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 440),
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          'Calculator',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                      ),
                      Icon(
                        widget.darkMode
                            ? Icons.dark_mode_outlined
                            : Icons.light_mode_outlined,
                      ),
                      Semantics(
                        label: 'Dark theme',
                        child: Switch(
                          value: widget.darkMode,
                          onChanged: widget.onThemeChanged,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: colors.surfaceContainer,
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          _expression.isEmpty ? 'Ready' : _expression,
                          key: const Key('expression'),
                          style: TextStyle(color: colors.onSurfaceVariant),
                        ),
                        const SizedBox(height: 16),
                        Semantics(
                          liveRegion: true,
                          label: 'Display: $_input',
                          excludeSemantics: true,
                          child: SingleChildScrollView(
                            scrollDirection: Axis.horizontal,
                            reverse: true,
                            child: Text(
                              _input,
                              key: const Key('display'),
                              style: Theme.of(context).textTheme.displayMedium,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  Semantics(
                    liveRegion: true,
                    child: Text(
                      _error ?? 'Enter a number, choose an operator, then enter the next number.',
                      key: const Key('status'),
                      style: TextStyle(
                        color: _error == null
                            ? colors.onSurfaceVariant
                            : colors.error,
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  _button('AC', spokenLabel: 'All clear', utility: true),
                  const SizedBox(height: 12),
                  for (final row in [
                    ['7', '8', '9', '÷'],
                    ['4', '5', '6', '×'],
                    ['1', '2', '3', '−'],
                    ['0', '.', '=', '+'],
                  ])
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Row(
                        children: [
                          for (var i = 0; i < row.length; i++) ...[
                            if (i > 0) const SizedBox(width: 12),
                            Expanded(child: _button(row[i])),
                          ],
                        ],
                      ),
                    ),
                  Text(
                    'Two numbers. One operation.',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodySmall
                        ?.copyWith(color: colors.onSurfaceVariant),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _button(String label, {String? spokenLabel, bool utility = false}) {
    final colors = Theme.of(context).colorScheme;
    final isOperator = ['+', '−', '×', '÷'].contains(label);
    final descriptions = {
      '+': 'Add',
      '−': 'Subtract',
      '×': 'Multiply',
      '÷': 'Divide',
      '=': 'Equals',
      '.': 'Decimal point',
    };
    return Semantics(
      label: spokenLabel ?? descriptions[label] ?? label,
      button: true,
      excludeSemantics: true,
      onTap: () => _press(label),
      child: FilledButton(
        key: Key('button_$label'),
        onPressed: () => _press(label),
        style: FilledButton.styleFrom(
          minimumSize: const Size(64, 64),
          padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
          backgroundColor: label == '='
              ? colors.primary
              : isOperator
              ? colors.primaryContainer
              : utility
              ? colors.secondaryContainer
              : colors.surfaceContainerHighest,
          foregroundColor: label == '='
              ? colors.onPrimary
              : isOperator
              ? colors.onPrimaryContainer
              : utility
              ? colors.onSecondaryContainer
              : colors.onSurface,
          textStyle: Theme.of(context).textTheme.titleLarge,
        ),
        child: Text(label),
      ),
    );
  }
}
