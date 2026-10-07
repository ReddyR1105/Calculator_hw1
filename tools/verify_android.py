"""Exercise the installed release APK and save real emulator evidence."""
from pathlib import Path
import json
import hashlib
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ADB = r'D:\Map\platform-tools\adb.exe'
SERIAL = 'emulator-5554'
EVIDENCE = Path(__file__).resolve().parents[1] / 'evidence'
EVIDENCE.mkdir(exist_ok=True)

def adb(*args, binary=False):
    result = subprocess.run([ADB, '-s', SERIAL, *map(str, args)],
                            capture_output=True, timeout=45, check=True)
    return result.stdout if binary else result.stdout.decode(errors='replace')

def nodes(label):
    adb('shell', 'uiautomator', 'dump', '/sdcard/calculator_check.xml')
    xml = adb('shell', 'cat', '/sdcard/calculator_check.xml')
    (EVIDENCE / f'{label}.xml').write_text(xml, encoding='utf-8')
    return [n.attrib for n in ET.fromstring(xml).iter('node')]

def points(items):
    controls = {}
    for n in items:
        if n.get('clickable') == 'true':
            x1, y1, x2, y2 = map(int, re.findall(r'\d+', n['bounds']))
            controls[n['content-desc']] = ((x1 + x2)//2, (y1 + y2)//2)
    return controls

def tap(controls, labels):
    for label in labels:
        adb('shell', 'input', 'tap', *controls[label])
        time.sleep(0.15)

def screenshot(label):
    (EVIDENCE / f'{label}.png').write_bytes(adb('exec-out', 'screencap', '-p', binary=True))

results = []
controls = points(nodes('initial'))
cases = [
    ('addition', ['1', '2', 'Add', '8', 'Equals'], '20'),
    ('subtraction', ['5', 'Subtract', '9', 'Equals'], '-4'),
    ('multiplication', ['8', 'Multiply', '7', 'Equals'], '56'),
    ('division', ['7', 'Divide', '2', 'Equals'], '3.5'),
    ('decimal_addition', ['0', 'Decimal point', '1', 'Add', '0', 'Decimal point', '2', 'Equals'], '0.3'),
    ('operator_replacement', ['8', 'Add', 'Multiply', '2', 'Equals'], '16'),
    ('clear_pending', ['9', 'Multiply', 'All clear', '2', 'Add', '3', 'Equals'], '5'),
]
for label, buttons, expected in cases:
    tap(controls, ['All clear'])
    controls = points(nodes(f'{label}_start'))
    tap(controls, buttons)
    observed = nodes(label)
    values = [n.get('content-desc', '') for n in observed]
    assert f'Display: {expected}' in values, (label, values)
    results.append({'case': label, 'buttons': buttons, 'expected': expected, 'passed': True})
    print(label + ': passed', flush=True)
    if label == 'multiplication': screenshot('light_theme_result')

tap(controls, ['All clear', '9', 'Divide', '0', 'Equals'])
error_nodes = nodes('division_by_zero')
assert any('Cannot divide by zero' in n.get('content-desc', '') for n in error_nodes)
screenshot('division_by_zero')
controls = points(error_nodes)
tap(controls, ['4'])
controls = points(nodes('error_recovered'))
tap(controls, ['Add', '2', 'Equals'])
assert any(n.get('content-desc') == 'Display: 6' for n in nodes('recovery_result'))
results.append({'case': 'division_by_zero_and_recovery', 'expected': 'Error, then 4 + 2 = 6', 'passed': True})
print('division_by_zero_and_recovery: passed', flush=True)

tap(controls, ['All clear', '5', 'Add', 'Equals'])
assert any('Enter two numbers' in n.get('content-desc', '') for n in nodes('incomplete_input'))
results.append({'case': 'incomplete_input', 'expected': 'Recoverable incomplete-input message', 'passed': True})
tap(points(nodes('before_theme')), ['All clear'])
controls = points(nodes('theme_start'))
tap(controls, ['6', 'Add', 'Dark theme'])
controls = points(nodes('theme_changed'))
tap(controls, ['4', 'Equals'])
dark_nodes = nodes('dark_theme_result')
assert any(n.get('content-desc') == 'Display: 10' for n in dark_nodes)
assert any(n.get('content-desc') == 'Dark theme' and n.get('checked') == 'true' for n in dark_nodes)
screenshot('dark_theme_result')
results.append({'case': 'theme_preserves_calculation', 'expected': 'Dark theme and 6 + 4 = 10', 'passed': True})
print('theme_preserves_calculation: passed', flush=True)

(EVIDENCE / 'android-release-checks.json').write_text(json.dumps({
    'test_date': '2026-10-07', 'device': 'Pixel_4a / emulator-5554',
    'package': 'edu.course.calculator_app', 'build': 'release',
    'apk_sha256': hashlib.sha256((EVIDENCE.parent / 'build/app/outputs/flutter-apk/app-release.apk').read_bytes()).hexdigest(),
    'renderer': 'Skia compatibility renderer',
    'installation': 'adb install -r: Success', 'results': results,
    'limitations': ['TalkBack listening was not manually tested.', 'Performance on an older physical device was not measured.'],
}, indent=2), encoding='utf-8')
print(f'{len(results)} Android release checks passed.', flush=True)
