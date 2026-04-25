import os
import re
from PyPDF2 import PdfReader


def fix_spaced_text(text):
    """Fix text where letters are separated by spaces like 'L e s s o n'"""
    lines = text.split('\n')
    fixed = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            fixed.append('')
            continue

        # Count single-char-space patterns
        spaced_pattern = re.findall(r'(?<!\S)\S (?=\S)', stripped)
        non_space_chars = len(re.findall(r'\S', stripped))

        if non_space_chars > 3 and len(spaced_pattern) > non_space_chars * 0.4:
            # This line has spaced-out letters - collapse them
            collapsed = re.sub(r'(?<=\S) (?=\S)', '', stripped)
            fixed.append(collapsed)
        else:
            fixed.append(stripped)

    # Remove consecutive empty lines
    result = []
    prev_empty = False
    for line in fixed:
        if line == '':
            if not prev_empty:
                result.append('')
            prev_empty = True
        else:
            result.append(line)
            prev_empty = False
    return '\n'.join(result)


def extract_pdf(path):
    reader = PdfReader(path)
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text.append(f'--- Page {i+1} ---\n{text}')
    return '\n\n'.join(all_text)


rules_dir = r'c:\Java\CopipotTraining\vibecoding-for-managers\lnd\rules'
for fname in sorted(os.listdir(rules_dir)):
    if fname.endswith('.pdf'):
        src = os.path.join(rules_dir, fname)
        raw = extract_pdf(src)
        fixed = fix_spaced_text(raw)
        dst = os.path.join(rules_dir, fname.replace('.pdf', '.md'))
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(fixed)
        reader = PdfReader(src)
        print(f'OK: {fname} ({len(reader.pages)}p) -> {os.path.basename(dst)} ({len(fixed)} chars)')
