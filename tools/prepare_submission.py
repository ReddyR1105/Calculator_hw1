"""Create the Word document and a portable source/submission bundle."""
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import re
import shutil
import struct
import xml.etree.ElementTree as ET

PROJECT = Path(__file__).resolve().parents[1]
DEST = PROJECT.parent / 'Calculator_Assignment01_Submission'
metadata_file = PROJECT / 'docs/submission_metadata.json'
if not metadata_file.is_file():
    metadata_file = PROJECT / 'docs/submission_metadata.example.json'
META = json.loads(metadata_file.read_text(encoding='utf-8'))
NAME = META.get('filename_name') or 'YourName'
assert re.fullmatch(r'[A-Za-z0-9_-]+', NAME), 'Use a simple filename name.'
DEST.mkdir(exist_ok=True)
EXTRAS = DEST / 'Extras'
EXTRAS.mkdir(exist_ok=True)

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

def paragraph(text, style=None, page_break=False):
    props = (f'<w:pStyle w:val="{style}"/>' if style else '')
    if page_break:
        props += '<w:pageBreakBefore/>'
    return '<w:p><w:pPr>' + props + '</w:pPr><w:r><w:t xml:space="preserve">' + escape(text) + '</w:t></w:r></w:p>'

def image_paragraph(index, path, width_inches=1.9):
    data = path.read_bytes()
    width, height = struct.unpack('>II', data[16:24])
    cx = int(width_inches * 914400)
    cy = int(cx * height / width)
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0">
    <wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{index}" name="Screenshot {index}" descr="{escape(path.stem)}"/>
    <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <pic:pic><pic:nvPicPr><pic:cNvPr id="{index}" name="{escape(path.name)}"/><pic:cNvPicPr/></pic:nvPicPr>
    <pic:blipFill><a:blip r:embed="image{index}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
    <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>
    </a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''

markdown = (PROJECT / 'docs/Implementation.md').read_text(encoding='utf-8')
if META.get('name'):
    markdown = markdown.replace('[ADD YOUR NAME]', META['name'])
if META.get('student_id'):
    markdown = markdown.replace('[ADD YOUR STUDENT ID]', META['student_id'])
if META.get('name') and META.get('student_id'):
    markdown = markdown.replace('add name and ID, and complete', 'complete')
if META.get('course'):
    markdown = markdown.replace('[CONFIRM CSC 4360 OR CSC 6370]', META['course'])

blocks = []
for block in re.split(r'\n\s*\n', markdown.strip()):
    text = ' '.join(block.splitlines())
    if text.startswith('# '):
        blocks.append(paragraph(text[2:], 'Title'))
    elif text.startswith('## '):
        blocks.append(paragraph(text[3:], 'Heading1'))
    else:
        blocks.append(paragraph(text))

screenshots = [(PROJECT / 'evidence' / filename, caption) for filename, caption in [
    ('light_theme_result.png', 'Light theme: 8 × 7 = 56'),
    ('dark_theme_result.png', 'Dark theme: 6 + 4 = 10'),
    ('division_by_zero.png', 'Recoverable division error'),
]]
assert all(path.is_file() for path, _ in screenshots), 'Capture screenshots first.'
blocks.append(paragraph('Screenshot appendix', 'Heading1', page_break=True))
cells = []
for index, (path, caption) in enumerate(screenshots, 1):
    cells.append('<w:tc><w:tcPr><w:tcW w:w="3120" w:type="dxa"/></w:tcPr>' +
                 paragraph(caption, 'Caption') + image_paragraph(index, path) + '<w:p/></w:tc>')
blocks.append('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/></w:tblPr>'
              '<w:tblGrid><w:gridCol w:w="3120"/><w:gridCol w:w="3120"/><w:gridCol w:w="3120"/></w:tblGrid>'
              '<w:tr>' + ''.join(cells) + '</w:tr></w:tbl>')
blocks.append(paragraph('Captures from the installed release APK on the Pixel_4a emulator.'))

document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}" xmlns:r="{R}"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>{''.join(blocks)}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1080" w:right="1440" w:bottom="1080" w:left="1440" w:header="720" w:footer="720"/>
</w:sectPr></w:body></w:document>'''
styles = f'''<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="{W}"><w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:lang w:val="en-US"/>
</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="276" w:lineRule="auto"/>
</w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="240"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="215C47"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="220" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="27"/><w:color w:val="215C47"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
<w:pPr><w:keepNext/><w:jc w:val="center"/></w:pPr><w:rPr><w:i/><w:sz w:val="18"/></w:rPr></w:style>
</w:styles>'''
types = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
root_rels = f'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="officeDocument" Type="{R}/officeDocument" Target="word/document.xml"/></Relationships>'''
image_rels = ''.join(f'<Relationship Id="image{i}" Type="{R}/image" Target="media/image{i}.png"/>' for i in range(1, 4))
doc_rels = f'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="styles" Type="{R}/styles" Target="styles.xml"/>{image_rels}</Relationships>'''

word_file = DEST / f'{NAME}_Implementation.docx'
with ZipFile(word_file, 'w', ZIP_DEFLATED) as archive:
    archive.writestr('[Content_Types].xml', types)
    archive.writestr('_rels/.rels', root_rels)
    archive.writestr('word/document.xml', document)
    archive.writestr('word/styles.xml', styles)
    archive.writestr('word/_rels/document.xml.rels', doc_rels)
    for index, (path, _) in enumerate(screenshots, 1):
        archive.write(path, f'word/media/image{index}.png')

with ZipFile(word_file) as archive:
    assert archive.testzip() is None
    for filename in archive.namelist():
        if filename.endswith(('.xml', '.rels')):
            ET.fromstring(archive.read(filename))
    content = archive.read('word/document.xml').decode()
    for number in ['01.', '02.', '03.', '04.', '05.', '06.']:
        assert number in content, number

apk = PROJECT / 'build/app/outputs/flutter-apk/app-release.apk'
assert apk.is_file(), 'Build the release APK first.'
shutil.copy2(apk, DEST / f'{NAME}_CalculatorApp.apk')
url = META.get('github_url')
if url:
    assert re.fullmatch(r'https://github\.com/[^/\s]+/[^/\s]+/?', url), 'Use an actual repository URL.'
(DEST / 'github_link.txt').write_text(url or 'REPLACE_WITH_THE_URL_OF_YOUR_PUBLISHED_GITHUB_REPOSITORY', encoding='utf-8')
shutil.copy2(PROJECT / 'docs/AI_Test_Drive_Worksheet.md', EXTRAS / 'AI_Test_Drive_Worksheet.md')
shutil.copy2(PROJECT / 'docs/AI_Test_Drive_Records.md', EXTRAS / 'AI_Test_Drive_Records.md')
(EXTRAS / 'Implementation_editable.md').write_text(markdown, encoding='utf-8')

source_file = EXTRAS / 'calculator_app_source.zip'
excluded_parts = {'build', '.dart_tool', '.gradle', '.kotlin', '.git', '.idea', '__pycache__'}
excluded_names = {'local.properties', 'submission_metadata.json', 'software_graphics_check.png'}
with ZipFile(source_file, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(PROJECT.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(PROJECT)
        if any(part in excluded_parts for part in rel.parts) or path.name in excluded_names or path.suffix == '.iml':
            continue
        archive.write(path, (Path('calculator_app') / rel).as_posix())
with ZipFile(source_file) as archive:
    assert archive.testzip() is None
    assert 'calculator_app/lib/main.dart' in archive.namelist()
    assert 'calculator_app/pubspec.yaml' in archive.namelist()

readme = f'''Calculator Assignment 01 — submission files

Three required LMS uploads:
1. {NAME}_CalculatorApp.apk — built, installed, and tested on the Android emulator.
2. {NAME}_Implementation.docx — rationale, questions 01–06, agent comparisons, and screenshots.
3. github_link.txt — {url or 'add the published repository URL'}.

Course: {META.get('course') or 'confirm the course'}.
The three selected enhanced features are theme toggle, all-clear, and error handling.

Actual Gemini and Codex responses are recorded in Extras/AI_Test_Drive_Records.md.
The unchanged Bug Hunt and State Design prompts each received two real responses.
Both agents also answered the question 06 trade-off prompt. Claims were checked
against additional widget tests and the source code.

One requirement needs instructor acceptance: Codex is the second actual agent.
The course guide's named options are Gemini, ChatGPT, and Copilot. ChatGPT's
browser verification and Copilot's sign-in prevented obtaining their responses.
Codex is not presented as ChatGPT. A grade cannot be guaranteed.

The complete source is uploaded to the public GitHub repository. The student's
ID is included in the private Word document and excluded from the public source.
Extras/calculator_app_source.zip is a portable copy. Run flutter pub get after
extracting it on another machine.

Evidence: 11 passing widget test groups and 10 passing Android release checks.
Manual TalkBack listening and older-device performance measurements are unverified.

Upload the three required files to the correct course LMS assignment area and
check the receipt. The ZIP is for downloading; it does not replace separate
uploads unless the course site explicitly permits that. No LMS upload was made.
'''
(DEST / 'READ_ME_FIRST.txt').write_text(readme, encoding='utf-8')
manifest = {}
for path in sorted(DEST.rglob('*')):
    if path.is_file() and path.name != 'file_hashes.json':
        manifest[path.relative_to(DEST).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
(DEST / 'file_hashes.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
bundle = DEST.parent / 'Calculator_Assignment01_Files.zip'
with ZipFile(bundle, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(DEST.rglob('*')):
        if path.is_file():
            archive.write(path, (Path(DEST.name) / path.relative_to(DEST)).as_posix())
with ZipFile(bundle) as archive:
    assert archive.testzip() is None
print(json.dumps({'word': str(word_file), 'apk': str(DEST / f'{NAME}_CalculatorApp.apk'),
                  'source': str(source_file), 'bundle': str(bundle),
                  'github_link_is_placeholder': not bool(url), 'course_confirmed': bool(META.get('course'))}, indent=2))
