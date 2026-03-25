import re, os, glob

output_dir = r'c:\Java\CopipotTraining\vibecoding-for-managers\lnd\output'
files = sorted(glob.glob(os.path.join(output_dir, 'module-*.md')))
# Skip module-01 (already done by user)
files = [f for f in files if 'module-01' not in f]

# Terms to wrap in backticks, longest first to avoid partial matches
# Format: (pattern, is_regex, case_sensitive)
TERMS = [
    # Multi-word product names (longest first)
    'Visual Studio Code',
    'GitHub Copilot Coding Agent',
    'GitHub Copilot',
    'GitHub Actions',
    'Docker Desktop',
    'Docker Compose',
    'Docker Engine',
    'Google Chrome',
    'Chrome DevTools MCP',
    'Chrome DevTools',
    'Copilot Chat',
    'Copilot Coding Agent',
    'Source Control',
    'Command Palette',
    'File Explorer',
    'Agent Mode',
    'Ask Mode',
    'Snip & Sketch',
    'Snipping Tool',
    'Node Package Manager',
    'Node Version Manager',
    'REST API',
    'API key',
    'API keys',
    'API tokens',
    'API token',
    'VS Code',
    'DIAL API',
    'AI DIAL',
    'Rancher Desktop',

    # Single-word product/company names
    'Copilot',
    'GitHub',
    'Microsoft',
    'EPAM',
    'Cursor',
    'Node.js',
    'Docker',
    'React',
    'Vite',
    'Express',
    'PostgreSQL',
    'Chrome',
    'Python',
    'JavaScript',
    'PowerShell',
    'Bash',
    'Jira',
    'Confluence',
    'Atlassian',
    'Slack',
    'Gemini',
    'Podman',
    'SpecKit',
    'DIAL',

    # OS names
    'Windows',
    'macOS',
    'Linux',

    # Technical terms
    'JSON-RPC',
    'MCP',
    'JQL',
    'Git',
    'npm',
    'nvm',
    'cURL',
    'JSON',
    'HTTP',
    'WSL',
    'CSS',
    'HTML',
    'SQL',
    'CLI',
    'ARIA',
    'SSH',
]

# File extensions and names to wrap (handled separately with special regex)
FILE_PATTERNS = [
    '.gitignore',
    '.nvmrc',
    '.env',
    '.exe',
    '.dmg',
    '.mdc',
]

# Specific filenames to wrap
FILENAMES = [
    'docker-compose.yml',
    'package.json',
    'copilot-instructions.md',
    'main.agent.md',
    'walkthrough.md',
    'about.md',
    'PROJECT_SPEC.md',
    'PROJECT_IDEAS.md',
    'BACKLOG.md',
    'TODO.md',
    'CHANGELOG',
    'README.md',
    'calculator.py',
    'main.py',
    'operations.py',
    'hello.txt',
    'math_helper.py',
    'bubble_sort.py',
    'compound_interest.py',
    'template.md',
    'instructions.md',
    'example.md',
    'specification.md',
    'constitution.md',
    'clarify.md',
    'plan.md',
    'tasks.md',
    'analyze.md',
    'checklist.md',
    'qa-report.md',
    'validation-rules.md',
    'settings.json',
    'mcp.json',
]

# Specific paths/folder refs
PATHS = [
    'instructions/',
    'tools/',
    'frontend/',
    'backend/',
    '.vscode/',
    '.cursor/',
    '.github/',
    'spec/',
    'docs/',
    'work/',
    'modules/',
    'reports/',
]

def is_in_code_block(lines, line_idx):
    fence_count = 0
    for i in range(line_idx):
        s = lines[i].strip()
        if s.startswith('```') or s.startswith('~~~'):
            fence_count += 1
    return fence_count % 2 == 1


def wrap_term_in_line(line, term):
    """Wrap occurrences of term in backticks, skipping those already in backticks or inside markdown link URLs."""
    if term not in line:
        return line

    result = []
    i = 0
    while i < len(line):
        # Skip existing backtick content
        if line[i] == '`':
            end = line.find('`', i + 1)
            if end == -1:
                result.append(line[i:])
                break
            result.append(line[i:end + 1])
            i = end + 1
            continue

        # Skip markdown link URL part: ](url)
        if line[i] == ']' and i + 1 < len(line) and line[i + 1] == '(':
            paren_end = line.find(')', i + 2)
            if paren_end != -1:
                result.append(line[i:paren_end + 1])
                i = paren_end + 1
                continue

        # Skip markdown image: ![alt](url)
        if line[i] == '!' and i + 1 < len(line) and line[i + 1] == '[':
            # Find end of ![alt](url)
            bracket_end = line.find(']', i + 2)
            if bracket_end != -1 and bracket_end + 1 < len(line) and line[bracket_end + 1] == '(':
                paren_end = line.find(')', bracket_end + 2)
                if paren_end != -1:
                    result.append(line[i:paren_end + 1])
                    i = paren_end + 1
                    continue

        # Try to match term at current position
        chunk = line[i:]
        if chunk.startswith(term):
            # Check word boundaries
            # Before: either start of relevant text or non-alphanumeric
            before_ok = (i == 0) or (not line[i - 1].isalnum() and line[i - 1] not in '`/')
            # After: either end of string or non-alphanumeric (allow punctuation after)
            after_pos = i + len(term)
            after_ok = (after_pos >= len(line)) or (not line[after_pos].isalnum() and line[after_pos] not in '`')

            # Special handling for terms with dots (like Node.js) - the dot is part of the term
            if before_ok and after_ok:
                # Check we're not already inside backticks by looking at result so far
                result_so_far = ''.join(result)
                open_backticks = result_so_far.count('`') % 2
                if open_backticks == 0:
                    result.append('`' + term + '`')
                    i += len(term)
                    continue

        result.append(line[i])
        i += 1

    return ''.join(result)


def wrap_file_pattern_in_line(line, pattern):
    """Wrap file extension or filename patterns."""
    if pattern not in line:
        return line

    result = []
    i = 0
    while i < len(line):
        # Skip existing backticks
        if line[i] == '`':
            end = line.find('`', i + 1)
            if end == -1:
                result.append(line[i:])
                break
            result.append(line[i:end + 1])
            i = end + 1
            continue

        # Skip markdown link URL part
        if line[i] == ']' and i + 1 < len(line) and line[i + 1] == '(':
            paren_end = line.find(')', i + 2)
            if paren_end != -1:
                result.append(line[i:paren_end + 1])
                i = paren_end + 1
                continue

        # Skip markdown image
        if line[i] == '!' and i + 1 < len(line) and line[i + 1] == '[':
            bracket_end = line.find(']', i + 2)
            if bracket_end != -1 and bracket_end + 1 < len(line) and line[bracket_end + 1] == '(':
                paren_end = line.find(')', bracket_end + 2)
                if paren_end != -1:
                    result.append(line[i:paren_end + 1])
                    i = paren_end + 1
                    continue

        chunk = line[i:]
        if chunk.startswith(pattern):
            # For file extensions like .exe, check that before is whitespace or ( or start
            before_ok = (i == 0) or (line[i-1] in ' \t(,/')
            after_pos = i + len(pattern)
            after_ok = (after_pos >= len(line)) or (not line[after_pos].isalnum())

            if before_ok and after_ok:
                result_so_far = ''.join(result)
                if result_so_far.count('`') % 2 == 0:
                    result.append('`' + pattern + '`')
                    i += len(pattern)
                    continue

        result.append(line[i])
        i += 1

    return ''.join(result)


def process_line(line):
    """Apply all term wrapping to a single line."""
    # Skip lines that are just markdown headings with # - still process them
    # Skip blank lines
    if not line.strip():
        return line

    # Process multi-word terms first (longest first - they're already sorted)
    for term in TERMS:
        line = wrap_term_in_line(line, term)

    # Process filenames
    for fname in FILENAMES:
        line = wrap_file_pattern_in_line(line, fname)

    # Process file extension patterns
    for pat in FILE_PATTERNS:
        line = wrap_file_pattern_in_line(line, pat)

    # Process folder/path references
    for path in PATHS:
        line = wrap_file_pattern_in_line(line, path)

    return line


total_changes = 0
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    file_changes = 0
    for idx, line in enumerate(lines):
        # Skip lines in fenced code blocks
        if is_in_code_block(lines, idx):
            new_lines.append(line)
            continue

        # Skip fenced code block markers themselves
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            new_lines.append(line)
            continue

        new_line = process_line(line)
        if new_line != line:
            file_changes += 1
            total_changes += 1
        new_lines.append(new_line)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    fname = os.path.basename(fpath)
    if file_changes > 0:
        print(f'{fname}: {file_changes} lines changed')

print(f'\nTotal lines changed across all files: {total_changes}')
