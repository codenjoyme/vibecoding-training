import re, os, glob

output_dir = r'c:\Java\CopipotTraining\vibecoding-for-managers\lnd\output'
files = sorted(glob.glob(os.path.join(output_dir, 'module-*.md')))
files = [f for f in files if 'module-01' not in f]

def is_in_code_block(lines, line_idx):
    fence_count = 0
    for i in range(line_idx):
        s = lines[i].strip()
        if s.startswith('```') or s.startswith('~~~'):
            fence_count += 1
    return fence_count % 2 == 1

total = 0
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for idx, line in enumerate(lines):
        if is_in_code_block(lines, idx):
            new_lines.append(line)
            continue
        # Skip code fence lines
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            new_lines.append(line)
            continue
        
        # Replace adjacent backtick pairs within inline text
        # Pattern: end of one inline code immediately followed by start of another
        # `text1``text2` -> `text1text2`
        old_line = line
        while '``' in line:
            line = line.replace('``', '', 1)
        
        if line != old_line:
            total += 1
            fname = os.path.basename(fpath)
            print(f'{fname}:{idx+1}')
            print(f'  FIXED: {line.rstrip()}')
        
        new_lines.append(line)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print(f'\nTotal lines fixed: {total}')
