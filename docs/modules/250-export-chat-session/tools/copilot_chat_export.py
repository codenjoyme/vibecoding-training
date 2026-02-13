#!/usr/bin/env python3
"""
GitHub Copilot Chat Session Export Tool
=======================================
Standalone script to list workspaces, sessions, and export chat sessions
from VS Code (both regular and Insiders) to HTML format.

Supports both legacy .json and modern .jsonl (delta/CRDT) session formats.

Usage:
    python copilot_chat_export.py workspaces                      # List all workspaces
    python copilot_chat_export.py sessions <workspace_id>         # List sessions in workspace
    python copilot_chat_export.py export <workspace_id> <session> # Export session(s)
    python copilot_chat_export.py search <text>                   # Search text across all sessions
    
Options:
    --vscode-path PATH    Override VS Code settings path
    --output-dir DIR      Output directory for exports (default: ./copilot_export)
    --format FORMAT       Output format: html, json, jsonl, text (default: html)
"""

import json
import os
import sys
import argparse
import re
import io
from pathlib import Path

# Fix Windows console encoding for Unicode (emoji etc.)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from datetime import datetime
from urllib.parse import unquote


# ============================================================================
# JSONL Session Parser (new VS Code format)
# ============================================================================

def parse_jsonl_session(file_path):
    """
    Parse a .jsonl session file (delta/CRDT format) into a complete session object.
    
    Format:
      Line 0: kind=0 -> initial full state (v = full session dict)
      Lines 1+: kind=1 -> set value at key path (k = path, v = value)
                kind=2 -> append to array at key path (k = path, v = items to append)
                          optional 'i' = insert index
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    # Parse initial state
    first = json.loads(lines[0].strip())
    if first.get('kind') != 0:
        return None
    
    session = first['v']
    
    # Apply deltas
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        try:
            delta = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        kind = delta.get('kind')
        key_path_input = delta.get('k')
        value = delta.get('v')
        insert_idx = delta.get('i')
        
        if not key_path_input:
            continue
        
        # Parse key path (can be list or string like "['requests', 0, 'response']")
        key_path = _parse_key_path(key_path_input)
        if not key_path:
            continue
        
        if kind == 1:
            # Set value at path
            _set_at_path(session, key_path, value)
        elif kind == 2:
            # Append to array at path
            _append_at_path(session, key_path, value, insert_idx)
    
    return session


def _parse_key_path(path_input):
    """Parse key path into a list. Handles both string and list formats."""
    if isinstance(path_input, list):
        return path_input
    if isinstance(path_input, str):
        try:
            import ast
            return ast.literal_eval(path_input)
        except:
            return None
    return None


def _navigate_to_parent(obj, path):
    """Navigate to the parent container of the target and return (parent, last_key)."""
    current = obj
    for key in path[:-1]:
        if isinstance(current, dict):
            if key not in current:
                current[key] = {}
            current = current[key]
        elif isinstance(current, list):
            idx = int(key)
            while len(current) <= idx:
                current.append(None)
            current = current[idx]
        else:
            return None, None
    return current, path[-1]


def _set_at_path(obj, path, value):
    """Set a value at the given key path."""
    parent, key = _navigate_to_parent(obj, path)
    if parent is None:
        return
    
    if isinstance(parent, dict):
        parent[key] = value
    elif isinstance(parent, list):
        idx = int(key)
        while len(parent) <= idx:
            parent.append(None)
        parent[idx] = value


def _append_at_path(obj, path, value, insert_idx=None):
    """Append items to an array at the given key path."""
    parent, key = _navigate_to_parent(obj, path)
    if parent is None:
        return
    
    # Get the target array
    if isinstance(parent, dict):
        if key not in parent:
            parent[key] = []
        target = parent[key]
    elif isinstance(parent, list):
        idx = int(key)
        while len(parent) <= idx:
            parent.append(None)
        if parent[idx] is None:
            parent[idx] = []
        target = parent[idx]
    else:
        return
    
    if not isinstance(target, list):
        return
    
    # Append or insert items
    if isinstance(value, list):
        if insert_idx is not None:
            for i, item in enumerate(value):
                target.insert(insert_idx + i, item)
        else:
            target.extend(value)
    else:
        if insert_idx is not None:
            target.insert(insert_idx, value)
        else:
            target.append(value)


# ============================================================================
# Session Reader (supports both .json and .jsonl)
# ============================================================================

def read_session_file(file_path):
    """Read a session file, supporting both .json and .jsonl formats."""
    file_path = Path(file_path)
    
    if file_path.suffix == '.jsonl':
        return parse_jsonl_session(file_path)
    elif file_path.suffix == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None


# ============================================================================
# Workspace and Session Discovery
# ============================================================================

def detect_vscode_paths():
    """Auto-detect VS Code settings paths for the current OS."""
    paths = []
    
    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            for variant in ['Code', 'Code - Insiders']:
                p = os.path.join(appdata, variant)
                if os.path.isdir(p):
                    paths.append(p)
    elif sys.platform == 'darwin':
        home = os.path.expanduser('~')
        for variant in ['Code', 'Code - Insiders']:
            p = os.path.join(home, 'Library', 'Application Support', variant)
            if os.path.isdir(p):
                paths.append(p)
    else:  # Linux
        home = os.path.expanduser('~')
        for variant in ['Code', 'Code - Insiders']:
            p = os.path.join(home, '.config', variant)
            if os.path.isdir(p):
                paths.append(p)
    
    return paths


def list_workspaces(vscode_path=None):
    """List all workspaces with chat sessions."""
    paths = [vscode_path] if vscode_path else detect_vscode_paths()
    
    workspaces = []
    
    for vs_path in paths:
        ws_storage = os.path.join(vs_path, 'User', 'workspaceStorage')
        if not os.path.isdir(ws_storage):
            continue
        
        variant_name = os.path.basename(vs_path)
        
        for ws_dir in os.listdir(ws_storage):
            ws_full = os.path.join(ws_storage, ws_dir)
            chat_dir = os.path.join(ws_full, 'chatSessions')
            
            if not os.path.isdir(chat_dir):
                continue
            
            # Count sessions (both .json and .jsonl)
            sessions = [f for f in os.listdir(chat_dir) 
                       if f.endswith('.json') or f.endswith('.jsonl')]
            if not sessions:
                continue
            
            # Get workspace name
            ws_name = ws_dir
            ws_json = os.path.join(ws_full, 'workspace.json')
            if os.path.exists(ws_json):
                try:
                    with open(ws_json, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    folder = data.get('folder', '')
                    if folder:
                        # Decode URI
                        folder = unquote(folder).replace('file:///', '').replace('file://', '')
                        ws_name = os.path.basename(folder) or folder
                except:
                    pass
            
            workspaces.append({
                'workspace_id': ws_dir,
                'workspace_name': ws_name,
                'sessions_count': len(sessions),
                'vscode_variant': variant_name,
                'vscode_path': vs_path,
                'path': ws_full
            })
    
    # Sort by session count descending
    workspaces.sort(key=lambda x: x['sessions_count'], reverse=True)
    return workspaces


def list_sessions(workspace_id, vscode_path=None):
    """List all sessions in a specific workspace."""
    paths = [vscode_path] if vscode_path else detect_vscode_paths()
    
    sessions = []
    
    for vs_path in paths:
        chat_dir = os.path.join(vs_path, 'User', 'workspaceStorage', 
                                workspace_id, 'chatSessions')
        if not os.path.isdir(chat_dir):
            continue
        
        for f in os.listdir(chat_dir):
            if not (f.endswith('.json') or f.endswith('.jsonl')):
                continue
            
            fp = os.path.join(chat_dir, f)
            stat = os.stat(fp)
            
            session_info = {
                'id': f.rsplit('.', 1)[0],
                'file': f,
                'format': 'jsonl' if f.endswith('.jsonl') else 'json',
                'size_bytes': stat.st_size,
                'size_human': _human_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified_ts': stat.st_mtime,
                'file_path': fp,
                'messages_count': 0,
                'title': ''
            }
            
            # Try to get message count and title
            try:
                data = read_session_file(fp)
                if data:
                    requests = data.get('requests', [])
                    session_info['messages_count'] = len(requests)
                    session_info['title'] = data.get('customTitle', '')
            except:
                pass
            
            sessions.append(session_info)
    
    # Sort by modification time (newest first)
    sessions.sort(key=lambda x: x['modified_ts'], reverse=True)
    return sessions


def search_sessions(search_text, vscode_path=None):
    """Search for text across all sessions in all workspaces."""
    paths = [vscode_path] if vscode_path else detect_vscode_paths()
    results = []
    
    for vs_path in paths:
        ws_storage = os.path.join(vs_path, 'User', 'workspaceStorage')
        if not os.path.isdir(ws_storage):
            continue
        
        variant_name = os.path.basename(vs_path)
        
        for ws_dir in os.listdir(ws_storage):
            chat_dir = os.path.join(ws_storage, ws_dir, 'chatSessions')
            if not os.path.isdir(chat_dir):
                continue
            
            # Get workspace name
            ws_name = ws_dir
            ws_json = os.path.join(ws_storage, ws_dir, 'workspace.json')
            if os.path.exists(ws_json):
                try:
                    with open(ws_json, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    folder = data.get('folder', '')
                    if folder:
                        folder = unquote(folder).replace('file:///', '').replace('file://', '')
                        ws_name = os.path.basename(folder) or folder
                except:
                    pass
            
            for f in os.listdir(chat_dir):
                if not (f.endswith('.json') or f.endswith('.jsonl')):
                    continue
                
                fp = os.path.join(chat_dir, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    if search_text in content:
                        sz = os.path.getsize(fp)
                        results.append({
                            'workspace_id': ws_dir,
                            'workspace_name': ws_name,
                            'session_id': f.rsplit('.', 1)[0],
                            'file': f,
                            'size_human': _human_size(sz),
                            'vscode_variant': variant_name,
                            'vscode_path': vs_path,
                            'file_path': fp
                        })
                except:
                    pass
    
    return results


def _human_size(size_bytes):
    """Convert bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ============================================================================
# HTML Export
# ============================================================================

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def extract_text_from_response(response):
    """Extract plain text from response array, skipping tool calls."""
    if isinstance(response, list):
        parts = []
        for item in response:
            if isinstance(item, dict) and 'value' in item:
                parts.append(str(item['value']))
        return ''.join(parts)
    elif isinstance(response, dict) and 'value' in response:
        return str(response['value'])
    return ""


def simple_markdown_to_html(text):
    """Convert basic Markdown to HTML."""
    if not text:
        return ""
    
    html = escape_html(text)
    
    # Code blocks
    html = re.sub(
        r'```(\w*)\n(.*?)```',
        r'<pre style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d;overflow-x:auto;"><code>\2</code></pre>',
        html, flags=re.DOTALL
    )
    
    # Inline code
    html = re.sub(
        r'`([^`]+?)`',
        r'<code style="background:#161b22;padding:2px 6px;border-radius:3px;font-size:0.9em;">\1</code>',
        html
    )
    
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3 style="color:#f0f6fc;margin:16px 0 8px;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 style="color:#f0f6fc;margin:20px 0 10px;border-bottom:1px solid #30363d;padding-bottom:8px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1 style="color:#f0f6fc;margin:24px 0 16px;">\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+?)\]\(([^)]+?)\)', r'<a href="\2" style="color:#58a6ff;" target="_blank">\1</a>', html)
    
    # Line breaks
    html = html.replace('\n', '<br>')
    
    # Clean consecutive breaks around block elements
    html = re.sub(r'<br>\s*(<h[123])', r'\1', html)
    html = re.sub(r'(</h[123]>)\s*<br>', r'\1', html)
    html = re.sub(r'<br>\s*(<pre)', r'\1', html)
    html = re.sub(r'(</pre>)\s*<br>', r'\1', html)
    
    return html


def _strip_ansi(text):
    """Remove ANSI escape codes and normalize line endings from terminal output."""
    if not text:
        return text
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')  # normalize Windows line endings
    return text


def format_tool_call_html(item, response_list=None, idx=0):
    """Format a tool call item as collapsible HTML with full details."""
    tool_id = item.get('toolId', item.get('toolName', 'unknown'))
    tool_call_id = item.get('toolCallId', f'tc_{idx}')
    is_complete = item.get('isComplete', False)
    
    # Past-tense message (shown as summary when collapsed)
    past_msg = ""
    if 'pastTenseMessage' in item:
        pm = item['pastTenseMessage']
        if isinstance(pm, dict):
            past_msg = pm.get('value', '')
        elif pm:
            past_msg = str(pm)
    
    # Invocation message
    inv_msg = ""
    if 'invocationMessage' in item:
        inv = item['invocationMessage']
        if isinstance(inv, dict):
            inv_msg = inv.get('value', '')
        else:
            inv_msg = str(inv)
    
    # Confirmation info
    confirmation_html = ""
    is_confirmed = item.get('isConfirmed', {})
    if isinstance(is_confirmed, dict):
        conf_type = is_confirmed.get('type', 0)
        conf_labels = {1: 'Auto-approved', 2: 'User approved', 3: 'User rejected', 4: 'Auto-approved'}
        if conf_type in conf_labels:
            confirmation_html = f'<span class="tool-meta-badge">{conf_labels[conf_type]}</span>'

    # Source info
    source_html = ""
    source = item.get('source', {})
    if isinstance(source, dict):
        s_label = source.get('label', '')
        s_type = source.get('type', '')
        if s_label:
            source_html = f'<span class="tool-meta-badge">{escape_html(s_label)}</span>'
    
    # Tool-specific info (terminal commands)
    terminal_html = ""
    if 'toolSpecificData' in item:
        tsd = item['toolSpecificData']
        if tsd.get('kind') == 'terminal':
            # Command line
            cmd = ''
            if 'commandLine' in tsd:
                cmd_data = tsd['commandLine']
                cmd = cmd_data.get('original', '') if isinstance(cmd_data, dict) else str(cmd_data)
            
            # CWD
            cwd = ''
            if 'cwd' in tsd:
                cwd_data = tsd['cwd']
                if isinstance(cwd_data, dict):
                    cwd = cwd_data.get('fsPath', cwd_data.get('path', ''))
                else:
                    cwd = str(cwd_data)
            
            # Terminal state (exit code, duration)
            exit_code = None
            duration_ms = None
            if 'terminalCommandState' in tsd:
                state = tsd['terminalCommandState']
                if isinstance(state, dict):
                    exit_code = state.get('exitCode')
                    duration_ms = state.get('duration')
            
            # Terminal output
            term_output = ''
            if 'terminalCommandOutput' in tsd:
                out_data = tsd['terminalCommandOutput']
                if isinstance(out_data, dict):
                    term_output = out_data.get('text', '')
                elif out_data:
                    term_output = str(out_data)
                term_output = _strip_ansi(term_output)
            
            # Build terminal block
            exit_class = 'exit-success' if exit_code == 0 else 'exit-error' if exit_code is not None else ''
            exit_badge = ''
            if exit_code is not None:
                exit_badge = f'<span class="{exit_class}">exit: {exit_code}</span>'
            duration_badge = ''
            if duration_ms is not None:
                if duration_ms > 1000:
                    duration_badge = f'<span class="tool-meta-badge">{duration_ms/1000:.1f}s</span>'
                else:
                    duration_badge = f'<span class="tool-meta-badge">{duration_ms}ms</span>'
            
            cwd_line = f'<div class="terminal-cwd">📂 {escape_html(cwd)}</div>' if cwd else ''
            
            terminal_html = f'''<div class="terminal-block">
  <div class="terminal-header">{cwd_line}<div class="terminal-cmd">$ {escape_html(cmd)}</div></div>
  <div class="terminal-badges">{exit_badge}{duration_badge}</div>
  <pre class="terminal-output">{escape_html(term_output.strip()) if term_output.strip() else '(no output)'}</pre>
</div>'''
    
    # Todo list rendering (manage_todo_list)
    todo_html = ""
    if 'toolSpecificData' in item:
        tsd = item.get('toolSpecificData', {})
        if isinstance(tsd, dict) and tsd.get('kind') == 'todoList':
            todo_items = tsd.get('todoList', [])
            if isinstance(todo_items, list) and todo_items:
                todo_rows = []
                for t in todo_items:
                    if isinstance(t, dict):
                        t_status = t.get('status', 'unknown')
                        t_title = t.get('title', '')
                        t_id = t.get('id', '')
                        status_icon = {'completed': '✅', 'in-progress': '🔄', 'not-started': '⬜'}.get(t_status, '❓')
                        status_class = {'completed': 'todo-done', 'in-progress': 'todo-progress', 'not-started': 'todo-pending'}.get(t_status, '')
                        todo_rows.append(f'<tr class="{status_class}"><td>{status_icon}</td><td>{escape_html(str(t_id))}</td><td>{escape_html(t_title)}</td><td>{escape_html(t_status)}</td></tr>')
                todo_html = '<div class="todo-list-block"><table class="todo-table"><tr><th></th><th>#</th><th>Task</th><th>Status</th></tr>' + ''.join(todo_rows) + '</table></div>'

    # Search results rendering (findTextInFiles resultDetails with uri+range)
    search_results_html = ""
    if 'resultDetails' in item and isinstance(item['resultDetails'], list):
        rd_list = item['resultDetails']
        if rd_list and isinstance(rd_list[0], dict) and 'uri' in rd_list[0]:
            result_rows = []
            for sr in rd_list[:50]:  # limit to 50
                sr_uri = sr.get('uri', {})
                sr_path = sr_uri.get('fsPath', sr_uri.get('path', '')) if isinstance(sr_uri, dict) else str(sr_uri)
                sr_file = os.path.basename(sr_path) if sr_path else '?'
                sr_range = sr.get('range', {})
                if isinstance(sr_range, dict):
                    start_line = sr_range.get('startLineNumber', sr_range.get('start', {}).get('line', '?'))
                    end_line = sr_range.get('endLineNumber', sr_range.get('end', {}).get('line', ''))
                else:
                    start_line = '?'
                    end_line = ''
                line_str = f'L{start_line}' + (f'-L{end_line}' if end_line and end_line != start_line else '')
                result_rows.append(f'<div class="search-result-item">📄 <span class="search-file">{escape_html(sr_file)}</span> <span class="search-line">{escape_html(str(line_str))}</span> <span class="search-path">{escape_html(sr_path)}</span></div>')
            if len(rd_list) > 50:
                result_rows.append(f'<div class="search-result-item" style="color:var(--text-muted);">... and {len(rd_list) - 50} more results</div>')
            search_results_html = '<div class="search-results-block">' + ''.join(result_rows) + '</div>'

    # MCP input/output
    io_html = ""
    if 'resultDetails' in item and isinstance(item['resultDetails'], dict):
        rd = item['resultDetails']
        if 'input' in rd:
            inp = rd['input']
            if isinstance(inp, str):
                try:
                    inp = json.loads(inp)
                except:
                    pass
            inp_str = json.dumps(inp, indent=2, ensure_ascii=False) if isinstance(inp, (dict, list)) else str(inp)
            io_html += f'<div class="mcp-io"><strong>📥 Input:</strong><pre class="mcp-io-pre">{escape_html(inp_str)}</pre></div>'
        if 'output' in rd:
            out = rd['output']
            if isinstance(out, list):
                for bi, block in enumerate(out):
                    if isinstance(block, dict):
                        val = block.get('value', '')
                        if isinstance(val, str):
                            try:
                                val = json.loads(val)
                                val = json.dumps(val, indent=2, ensure_ascii=False)
                            except:
                                pass
                        err = block.get('error', False)
                        icon = "❌" if err else "✅"
                        io_html += f'<div class="mcp-io"><strong>📤 Output {icon}:</strong><pre class="mcp-io-pre">{escape_html(str(val))}</pre></div>'
            elif isinstance(out, str):
                io_html += f'<div class="mcp-io"><strong>📤 Output:</strong><pre class="mcp-io-pre">{escape_html(out)}</pre></div>'
    
    status = '✅' if is_complete else '⏳'
    safe_id = f"tool_{tool_call_id.replace('-', '_')}_{idx}"
    
    # Display name mapping
    display_name = tool_id
    tool_icon = '🔧'
    if tool_id.startswith('mcp_') and '-mcp_' in tool_id:
        parts = tool_id.split('-mcp_')
        if len(parts) == 2:
            display_name = f"[MCP] {parts[0]}: {parts[1]}"
        tool_icon = '🔌'
    elif tool_id == 'run_in_terminal':
        tool_icon = '💻'
        display_name = 'Terminal'
    elif tool_id.startswith('copilot_'):
        tool_icon = '📝'
        name_map = {'copilot_createFile': 'Create File', 'copilot_readFile': 'Read File',
                    'copilot_editFile': 'Edit File', 'copilot_listDirectory': 'List Directory',
                    'copilot_semanticSearch': 'Semantic Search', 'copilot_grepSearch': 'Grep Search',
                    'copilot_fileSearch': 'File Search', 'copilot_runNotebookCell': 'Run Notebook Cell'}
        display_name = name_map.get(tool_id, tool_id.replace('copilot_', '').replace('_', ' ').title())
    elif tool_id == 'manage_todo_list':
        tool_icon = '📋'
        display_name = 'Todo List'
    elif tool_id == 'list_code_usages':
        tool_icon = '🔍'
        display_name = 'List Code Usages'
    elif tool_id == 'copilot_findTextInFiles':
        tool_icon = '🔍'
        display_name = 'Find in Files'
    elif tool_id == 'copilot_replaceString':
        tool_icon = '✏️'
        display_name = 'Replace String'
    elif tool_id == 'copilot_multiReplaceString':
        tool_icon = '✏️'
        display_name = 'Multi Replace'
    
    # Summary line (shown in header)
    summary = ""
    if past_msg:
        summary = f'<span class="tool-summary">{escape_html(past_msg)}</span>'
    elif inv_msg:
        summary = f'<span class="tool-summary">{escape_html(inv_msg[:120])}</span>'
    
    # Build expandable content
    details_parts = []
    if inv_msg:
        details_parts.append(f'<div class="tool-detail-section"><strong>📋 Invocation:</strong><pre class="tool-detail-pre">{escape_html(inv_msg)}</pre></div>')
    if terminal_html:
        details_parts.append(terminal_html)
    if todo_html:
        details_parts.append(todo_html)
    if search_results_html:
        details_parts.append(search_results_html)
    if io_html:
        details_parts.append(io_html)
    details_content = '\n'.join(details_parts) if details_parts else '<span style="color:#8c8c8c;">No additional details</span>'
    
    # Propagate generatedTitle as data attribute for grouping in build_response_html
    gen_title = item.get('generatedTitle', '')
    data_attr = f' data-gentitle="{escape_html(gen_title)}"' if gen_title else ''
    
    return f'''<div class="tool-call"{data_attr}>
<div onclick="toggle('{safe_id}')" class="tool-header">
  <span>{tool_icon}</span><span class="tool-name">{escape_html(display_name)}</span>{summary}<span class="tool-badges">{confirmation_html}{source_html}<span style="font-size:12px;">{status}</span></span>
</div>
<div id="{safe_id}" style="display:none;" class="tool-details">
  {details_content}
</div>
</div>'''


def format_thinking_html(item, think_idx):
    """Format a thinking/reasoning block as collapsible HTML."""
    value = item.get('value', '')
    title = item.get('generatedTitle', '')
    metadata = item.get('metadata', {})
    
    if not value and not title:
        return ""
    
    safe_id = f"think_{think_idx}"
    
    # Check if this is the "done" marker
    if isinstance(metadata, dict) and metadata.get('vscodeReasoningDone'):
        stop_reason = metadata.get('stopReason', '')
        return f'<div class="thinking-done">💭 Reasoning complete{" (" + escape_html(stop_reason) + ")" if stop_reason else ""}</div>'
    
    if not value:
        return ""
    
    title_text = f': {escape_html(title)}' if title else ''
    # Show first 100 chars as preview
    preview = value[:150].replace('\n', ' ')
    if len(value) > 150:
        preview += '...'
    
    return f'''<div class="thinking-block">
<div onclick="toggle('{safe_id}')" class="thinking-header">
  <span>💭</span><span class="thinking-title">Thinking{title_text}</span><span class="thinking-preview">{escape_html(preview)}</span>
</div>
<div id="{safe_id}" style="display:none;" class="thinking-content">
  <pre class="thinking-pre">{escape_html(value)}</pre>
</div>
</div>'''


def format_text_edit_group_html(item, edit_idx):
    """Format a textEditGroup (file creation/edit) as collapsible HTML."""
    uri = item.get('uri', {})
    path = uri.get('path', uri.get('fsPath', 'unknown'))
    file_name = os.path.basename(path) or path
    done = item.get('done', False)
    edits = item.get('edits', [])
    
    # Collect all edit text
    edit_texts = []
    total_edits = 0
    for edit_group in edits:
        if isinstance(edit_group, list):
            for edit in edit_group:
                if isinstance(edit, dict) and 'text' in edit:
                    edit_texts.append(edit['text'])
                    total_edits += 1
        elif isinstance(edit_group, dict) and 'text' in edit_group:
            edit_texts.append(edit_group['text'])
            total_edits += 1
    
    full_text = ''.join(edit_texts)
    lines_count = full_text.count('\n') + 1 if full_text else 0
    safe_id = f"edit_{edit_idx}"
    status = '✅' if done else '⏳'
    
    return f'''<div class="file-edit-block">
<div onclick="toggle('{safe_id}')" class="file-edit-header">
  <span>📝</span><span class="file-edit-name">{escape_html(file_name)}</span>
  <span class="file-edit-meta">{total_edits} edits, ~{lines_count} lines</span>
  <span class="file-edit-path">{escape_html(path)}</span>
  <span>{status}</span>
</div>
<div id="{safe_id}" style="display:none;" class="file-edit-content">
  <pre class="file-edit-pre">{escape_html(full_text)}</pre>
</div>
</div>'''


def format_progress_task_html(item):
    """Format a progressTaskSerialized item."""
    content = item.get('content', {})
    value = ''
    if isinstance(content, dict):
        value = content.get('value', '')
    elif isinstance(content, str):
        value = content
    
    title = item.get('title', '')
    is_complete = item.get('isComplete', False)
    status = '✅' if is_complete else '⏳'
    
    display = value or title or 'Processing...'
    return f'<div class="progress-task">{status} <span>{escape_html(display)}</span></div>'


def format_mcp_servers_html(item):
    """Format an mcpServersStarting item."""
    server_ids = item.get('didStartServerIds', [])
    if not server_ids:
        return '<div class="mcp-servers">🔌 MCP servers initialized</div>'
    servers_str = ', '.join(str(s) for s in server_ids)
    return f'<div class="mcp-servers">🔌 MCP servers started: {escape_html(servers_str)}</div>'


def format_codeblock_uri_html(item):
    """Format a codeblockUri item."""
    uri = item.get('uri', {})
    path = ''
    if isinstance(uri, dict):
        path = uri.get('path', uri.get('fsPath', ''))
    elif isinstance(uri, str):
        path = uri
    file_name = os.path.basename(path) or path
    is_edit = item.get('isEdit', False)
    icon = '✏️' if is_edit else '📄'
    return f'<div class="codeblock-uri">{icon} <span class="codeblock-path">{escape_html(file_name)}</span></div>'


def format_inline_reference_html(item):
    """Format an inlineReference to a file/symbol."""
    ref = item.get('inlineReference', item)
    name = ''
    if isinstance(ref, dict):
        fs_path = ref.get('fsPath', ref.get('path', ref.get('name', '')))
        name = os.path.basename(fs_path) if fs_path else str(ref)
    else:
        name = str(ref)
    return f'<span class="inline-ref">📁 {escape_html(name)}</span>'


def _group_tool_calls(parts):
    """
    Post-process HTML parts to group consecutive tool-call divs
    into collapsible group blocks, matching VS Code's UI grouping.
    
    Only groups items that have an explicit data-gentitle attribute
    (from the generatedTitle field in JSONL data). Items without
    generatedTitle are rendered as-is, without any auto-grouping.
    
    When a named group is found:
    - Preceding non-text items (thinking, progress, MCP, tool-calls w/o GT)
      are pulled backward into the group.
    - Following non-text, non-GT items (textEditGroup, tool-calls w/o GT,
      codeblockUri) are absorbed forward into the group — matching VS Code's
      behavior where the group wraps all items in the same "round".
    """
    import re
    import random
    from html import unescape as html_unescape
    
    toolcall_re = re.compile(r'^<div class="tool-call"')
    gentitle_re = re.compile(r'data-gentitle="([^"]*)"')
    # Non-text items that can be absorbed into a group
    nontextblock_re = re.compile(
        r'^<div class="(tool-call|thinking-block|progress-task|mcp-servers|file-edit-block|codeblock-uri)"'
    )
    
    grouped = []
    i = 0
    id_prefix = f'{random.randint(1000, 9999)}'
    group_counter = 0
    
    def _get_gentitle(html_str):
        m = gentitle_re.search(html_str)
        return html_unescape(m.group(1)) if m else None
    
    def _is_nontext_block(html_str):
        """Check if HTML part is a non-text block (tool, thinking, progress, mcp, file-edit, codeblock)."""
        return bool(nontextblock_re.match(html_str))
    
    def _build_group(run, title):
        nonlocal group_counter
        gid = f'tg_{id_prefix}_{group_counter}'
        group_counter += 1
        # Count success/pending only among tool-call divs in the group
        tool_parts = [r for r in run if toolcall_re.match(r)]
        ok = sum(1 for r in tool_parts if '<span style="font-size:12px;">\u2705</span>' in r)
        fail = len(tool_parts) - ok
        status_parts = []
        if ok: status_parts.append(f'{ok} \u2705')
        if fail: status_parts.append(f'{fail} \u23f3')
        check = '\u2714' if fail == 0 and ok > 0 else '\u25cb'
        count = len(tool_parts)
        return f'''<div class="tool-group">
<div onclick="toggle('{gid}')" class="tool-group-header">
  <span class="tool-group-chevron" id="chevron_{gid}">\u25b6</span>
  <span class="tool-group-check">{check}</span>
  <span class="tool-group-title">{title}</span>
  <span class="tool-group-count">{count} tool{"s" if count != 1 else ""}</span>
  <span class="tool-group-status">{" ".join(status_parts)}</span>
</div>
<div id="{gid}" style="display:none;" class="tool-group-content">
''' + '\n'.join(run) + '\n</div>\n</div>'
    
    while i < len(parts):
        part = parts[i]
        
        # Only attempt grouping for tool-call divs with generatedTitle
        if not toolcall_re.match(part):
            grouped.append(part)
            i += 1
            continue
        
        gentitle = _get_gentitle(part)
        
        if gentitle:
            # Named group — collect consecutive tool-calls with same generatedTitle
            run = [part]
            j = i + 1
            while j < len(parts):
                if toolcall_re.match(parts[j]) and _get_gentitle(parts[j]) == gentitle:
                    run.append(parts[j])
                    j += 1
                else:
                    break
            
            # Forward lookback: absorb following non-text, non-GT items
            # (textEditGroup, tool-calls without GT, codeblockUri, etc.)
            # until hitting text content or another GT-tagged tool.
            while j < len(parts):
                if _is_nontext_block(parts[j]) and not _get_gentitle(parts[j]):
                    run.append(parts[j])
                    j += 1
                else:
                    break
            
            # Backward lookback: pull preceding non-text blocks into the group.
            pulled = []
            while grouped and _is_nontext_block(grouped[-1]):
                pulled.append(grouped.pop())
            pulled.reverse()
            
            grouped.append(_build_group(pulled + run, gentitle))
            i = j
        else:
            # No generatedTitle — render as-is, no auto-grouping
            grouped.append(part)
            i += 1
    
    return '\n'.join(grouped)


def build_response_html(response):
    """Build HTML for the assistant response, rendering all item kinds."""
    if not isinstance(response, list):
        if isinstance(response, dict) and 'value' in response:
            return simple_markdown_to_html(str(response['value']))
        return ""
    
    parts = []
    text_buffer = []
    tool_idx = 0
    think_idx = 0
    edit_idx = 0
    # Track already-rendered tool invocations by toolCallId
    rendered_tools = set()
    i = 0
    
    def flush_text():
        nonlocal text_buffer
        if text_buffer:
            parts.append(simple_markdown_to_html(''.join(text_buffer)))
            text_buffer = []
    
    while i < len(response):
        item = response[i]
        if not isinstance(item, dict):
            i += 1
            continue
        
        kind = item.get('kind', '')
        
        # --- Text fragments (no kind, has value) ---
        if not kind and 'value' in item:
            text_buffer.append(str(item['value']))
            i += 1
        
        # --- Thinking / Reasoning ---
        elif kind == 'thinking':
            flush_text()
            html = format_thinking_html(item, think_idx)
            if html:
                parts.append(html)
                think_idx += 1
            i += 1
        
        # --- Inline file reference ---
        elif kind == 'inlineReference':
            text_buffer.append(' ' + format_inline_reference_html(item) + ' ')
            i += 1
        
        # --- Tool preparation -> find matching serialized ---
        elif kind == 'prepareToolInvocation':
            flush_text()
            tool_name = item.get('toolName', '')
            tool_call_id = item.get('toolCallId', '')
            serialized = None
            j = i + 1
            while j < len(response):
                nxt = response[j]
                if isinstance(nxt, dict) and nxt.get('kind') == 'toolInvocationSerialized':
                    if nxt.get('toolId') == tool_name or nxt.get('toolCallId') == tool_call_id:
                        serialized = nxt
                        break
                j += 1
            
            if serialized:
                parts.append(format_tool_call_html(serialized, response, tool_idx))
                rendered_tools.add(serialized.get('toolCallId', ''))
                tool_idx += 1
                i = j + 1
            else:
                parts.append(format_tool_call_html(item, response, tool_idx))
                tool_idx += 1
                i += 1
        
        # --- Orphaned serialized tool call ---
        elif kind == 'toolInvocationSerialized':
            tcid = item.get('toolCallId', '')
            if tcid not in rendered_tools:
                flush_text()
                parts.append(format_tool_call_html(item, response, tool_idx))
                rendered_tools.add(tcid)
                tool_idx += 1
            i += 1
        
        # --- File edits (textEditGroup) ---
        elif kind == 'textEditGroup':
            flush_text()
            parts.append(format_text_edit_group_html(item, edit_idx))
            edit_idx += 1
            i += 1
        
        # --- Progress tasks ---
        elif kind == 'progressTaskSerialized' or kind == 'progressTask':
            flush_text()
            parts.append(format_progress_task_html(item))
            i += 1
        
        # --- MCP servers starting ---
        elif kind == 'mcpServersStarting':
            flush_text()
            parts.append(format_mcp_servers_html(item))
            i += 1
        
        # --- Codeblock URI ---
        elif kind == 'codeblockUri':
            flush_text()
            parts.append(format_codeblock_uri_html(item))
            i += 1
        
        # --- Undo stop (skip) ---
        elif kind == 'undoStop':
            i += 1
        
        # --- Unknown kinds with value -> treat as text ---
        elif 'value' in item:
            text_buffer.append(str(item['value']))
            i += 1
        
        else:
            i += 1
    
    # Flush remaining text
    flush_text()
    
    # Post-process: group consecutive tool-call divs with same generatedTitle
    return _group_tool_calls(parts)


def _format_request_metadata_html(req, req_idx):
    """Format request-level metadata as a collapsible info bar."""
    parts = []
    
    # Model
    model_id = req.get('modelId', '')
    if model_id:
        parts.append(f'<span class="meta-badge meta-model">🤖 {escape_html(model_id)}</span>')
    
    # Timestamp
    timestamp = req.get('timestamp')
    if timestamp:
        try:
            ts_str = datetime.fromtimestamp(timestamp / 1000).strftime('%H:%M:%S')
            parts.append(f'<span class="meta-badge">🕐 {ts_str}</span>')
        except:
            pass
    
    # Result details string (e.g. "Claude Opus 4.6 • 3x")
    result = req.get('result', {})
    if isinstance(result, dict):
        details_str = result.get('details', '')
        if details_str and isinstance(details_str, str):
            parts.append(f'<span class="meta-badge meta-details">📌 {escape_html(details_str)}</span>')

    # Model state
    model_state = req.get('modelState', {})
    if isinstance(model_state, dict):
        state_val = model_state.get('value')
        completed_at = model_state.get('completedAt')
        state_labels = {0: '⬜ Pending', 1: '🔄 In Progress', 2: '❌ Canceled', 4: '✅ Completed'}
        if state_val is not None:
            label = state_labels.get(state_val, f'State: {state_val}')
            parts.append(f'<span class="meta-badge meta-state">{label}</span>')

    # Agent info
    agent = req.get('agent', {})
    if isinstance(agent, dict):
        agent_name = agent.get('name', '')
        agent_ext_ver = agent.get('extensionVersion', '')
        agent_slash = agent.get('slashCommands', [])
        if agent_name:
            agent_str = f'🤖 Agent: {agent_name}'
            if agent_ext_ver:
                agent_str += f' v{agent_ext_ver}'
            parts.append(f'<span class="meta-badge">{escape_html(agent_str)}</span>')

    # Error details
    if isinstance(result, dict):
        error_details = result.get('errorDetails', {})
        if isinstance(error_details, dict) and error_details:
            error_msg = error_details.get('message', '')
            error_code = error_details.get('code', '')
            is_incomplete = error_details.get('responseIsIncomplete', False)
            error_text = ''
            if error_msg:
                error_text = error_msg
            elif error_code:
                error_text = str(error_code)
            if is_incomplete:
                error_text = (error_text + ' (incomplete)') if error_text else 'Response incomplete'
            if error_text:
                parts.append(f'<span class="meta-badge meta-error">⚠️ {escape_html(error_text)}</span>')

    # Timing
    if isinstance(result, dict):
        timings = result.get('timings', {})
        if isinstance(timings, dict):
            total = timings.get('totalElapsed')
            first = timings.get('firstProgress')
            if total:
                if total > 1000:
                    parts.append(f'<span class="meta-badge">⏱️ {total/1000:.1f}s total</span>')
                else:
                    parts.append(f'<span class="meta-badge">⏱️ {total}ms total</span>')
            if first:
                if first > 1000:
                    parts.append(f'<span class="meta-badge">⚡ {first/1000:.1f}s first token</span>')
                else:
                    parts.append(f'<span class="meta-badge">⚡ {first}ms first token</span>')

    # Token counts
    if isinstance(result, dict):
        metadata = result.get('metadata', {})
        if isinstance(metadata, dict):
            prompt_tokens = metadata.get('promptTokens')
            output_tokens = metadata.get('outputTokens')
            tool_rounds = metadata.get('toolCallRounds')
            if prompt_tokens is not None:
                parts.append(f'<span class="meta-badge meta-tokens">📥 {prompt_tokens:,} prompt tokens</span>')
            if output_tokens is not None:
                parts.append(f'<span class="meta-badge meta-tokens">📤 {output_tokens:,} output tokens</span>')
            if tool_rounds is not None:
                parts.append(f'<span class="meta-badge">🔄 {tool_rounds} tool call rounds</span>')
    
    # Content references (instructions loaded)
    refs = req.get('contentReferences', [])
    if refs:
        ref_names = []
        for r in refs:
            if isinstance(r, dict):
                ref_data = r.get('reference', r)
                if isinstance(ref_data, dict):
                    p = ref_data.get('fsPath', ref_data.get('path', ''))
                    if p:
                        ref_names.append(os.path.basename(p))
        if ref_names:
            parts.append(f'<span class="meta-badge">📎 {escape_html(", ".join(ref_names))}</span>')
    
    # Edited files
    edited = req.get('editedFileEvents', [])
    if edited:
        file_names = []
        for e in edited:
            if isinstance(e, dict):
                uri = e.get('uri', {})
                if isinstance(uri, dict):
                    p = uri.get('fsPath', uri.get('path', ''))
                    if p:
                        file_names.append(os.path.basename(p))
        if file_names:
            parts.append(f'<span class="meta-badge meta-edited">✏️ Edited: {escape_html(", ".join(file_names))}</span>')
    
    # Followups
    followups = req.get('followups', [])
    if followups:
        parts.append(f'<span class="meta-badge">{len(followups)} follow-ups</span>')
    
    if not parts:
        return ""
    
    safe_id = f"meta_{req_idx}"
    return f'''<div class="request-meta">
  <div onclick="toggle('{safe_id}')" class="meta-toggle">ℹ️ Request info</div>
  <div id="{safe_id}" style="display:none;" class="meta-details">{' '.join(parts)}</div>
</div>'''


def _format_variable_attachments_html(variables):
    """Format variable data (attachments, screenshots, prompt files) with size info."""
    if not variables:
        return ""
    
    parts = []
    for j, var in enumerate(variables):
        var_id = var.get('id', '')
        name = var.get('name', 'Unknown')
        value = var.get('value', '')
        value_len = len(str(value)) if value else 0
        
        # Determine type and icon
        icon = '🔗'
        type_label = ''
        if 'prompt' in var_id.lower() or 'prompt' in name.lower():
            icon = '📋'
            type_label = 'prompt'
        elif 'image' in name.lower() or 'pasted' in name.lower() or 'screenshot' in name.lower():
            icon = '🖼️'
            type_label = 'image'
        elif 'copilot-instructions' in var_id.lower():
            icon = '⚙️'
            type_label = 'instructions'
        elif value_len > 100000:
            icon = '📦'
            type_label = 'large attachment'
        else:
            icon = '📄'
            type_label = 'file'
        
        size_str = _human_size(value_len) if value_len else ''
        att_id = f"att_{j}_{hash(str(var_id)) % 100000}"
        
        # For images, show as data URI preview if base64
        preview_html = ''
        if type_label == 'image' and isinstance(value, str) and len(value) > 1000:
            # Check if it looks like base64
            if value.startswith('data:image'):
                preview_html = f'<div style="margin:4px 0;"><img src="{value}" style="max-width:100%;max-height:300px;border-radius:4px;" /></div>'
            else:
                preview_html = f'<div style="color:#8c8c8c;font-size:11px;">Image data ({size_str})</div>'
        
        # Truncate value for display with JSON pretty-print
        display_val = ''
        if isinstance(value, (dict, list)):
            try:
                display_val = json.dumps(value, indent=2, ensure_ascii=False)
            except (TypeError, ValueError):
                display_val = str(value)
        elif isinstance(value, str):
            # Try to parse as JSON string
            try:
                parsed = json.loads(value)
                if isinstance(parsed, (dict, list)):
                    display_val = json.dumps(parsed, indent=2, ensure_ascii=False)
                else:
                    display_val = value
            except (json.JSONDecodeError, ValueError):
                display_val = value
        else:
            display_val = str(value)
        
        # Truncate if too long
        if len(display_val) > 5000:
            display_val = display_val[:5000] + f'\n\n... (truncated, total {size_str})'
        
        # Also prepare full var metadata as JSON
        var_meta = {k: v for k, v in var.items() if k != 'value'}
        var_meta_json = ''
        if var_meta:
            try:
                var_meta_json = json.dumps(var_meta, indent=2, ensure_ascii=False)
            except (TypeError, ValueError):
                var_meta_json = ''
        
        meta_block = ''
        if var_meta_json:
            meta_id = f"{att_id}_meta"
            meta_block = f'''<div style="margin-top:4px;"><span onclick="toggle('{meta_id}')" style="color:var(--text-muted);font-size:10px;cursor:pointer;">📋 metadata ▸</span><pre id="{meta_id}" style="display:none;" class="attachment-pre" style="font-size:10px;color:var(--text-muted);">{escape_html(var_meta_json)}</pre></div>'''
        
        parts.append(f'''<div class="attachment-item">
<div onclick="toggle('{att_id}')" class="attachment-header">
  <span>{icon}</span><span class="attachment-name">{escape_html(name)}</span><span class="attachment-meta">{escape_html(type_label)} • {size_str}</span>
</div>
<div id="{att_id}" style="display:none;" class="attachment-content">
  {preview_html}
  <pre class="attachment-pre">{escape_html(display_val)}</pre>{meta_block}
</div>
</div>''')
    
    return '\n'.join(parts)


def export_session_to_html(session_data, session_id='unknown', workspace_info=''):
    """Export a session to a comprehensive HTML document with all metadata."""
    requests = session_data.get('requests', [])
    title = session_data.get('customTitle', f'Session {session_id[:8]}')
    
    # Collect model info
    models_used = set()
    total_time_ms = 0
    for req in requests:
        m = req.get('modelId', '')
        if m:
            models_used.add(m)
        result = req.get('result', {})
        if isinstance(result, dict):
            timings = result.get('timings', {})
            if isinstance(timings, dict):
                t = timings.get('totalElapsed', 0)
                if t:
                    total_time_ms += t
    
    models_str = ', '.join(models_used) if models_used else 'unknown'
    total_time_str = f'{total_time_ms/1000:.0f}s' if total_time_ms > 0 else 'N/A'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Copilot Chat - {escape_html(title)}</title>
<style>
:root {{
  --bg: #1e1e1e; --bg-elevated: #252526; --bg-input: #2d2d30; --bg-deep: #0d1117;
  --border: #3c3c3c; --border-light: #404040; --border-subtle: #30363d;
  --text: #cccccc; --text-muted: #8c8c8c; --text-bright: #f0f6fc;
  --accent: #0078d4; --accent2: #005a9e; --blue: #58a6ff; --green: #3fb950;
  --red: #f85149; --yellow: #d29922; --cyan: #7dd3fc; --purple: #bc8cff;
}}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; line-height: 1.6; }}
.container {{ max-width: 960px; margin: 0 auto; min-height: 100vh; display: flex; flex-direction: column; }}

/* Header */
.header {{ background: var(--bg-elevated); padding: 16px 24px; border-bottom: 1px solid var(--border); }}
.header-top {{ display: flex; align-items: center; gap: 12px; }}
.header h1 {{ margin: 0; font-size: 16px; font-weight: 600; color: var(--text-bright); }}
.header-stats {{ display: flex; gap: 12px; margin-top: 8px; flex-wrap: wrap; }}
.header-stat {{ font-size: 11px; color: var(--text-muted); background: var(--bg-deep); padding: 2px 8px; border-radius: 10px; }}

/* Messages */
.messages {{ flex: 1; padding: 20px 24px; }}
.msg {{ margin-bottom: 28px; display: flex; gap: 12px; }}
.avatar {{ width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 600; font-size: 12px; color: white; }}
.user-av {{ background: #0e639c; }}
.ai-av {{ background: linear-gradient(135deg, var(--accent), var(--accent2)); }}
.msg-content {{ flex: 1; min-width: 0; }}
.msg-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
.author {{ font-weight: 600; font-size: 14px; color: var(--text-bright); }}
.msg-number {{ font-size: 11px; color: var(--text-muted); background: var(--bg-deep); padding: 1px 6px; border-radius: 8px; }}
.msg-body {{ background: var(--bg-input); padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border); word-break: break-word; font-size: 14px; }}
.msg-body pre {{ white-space: pre-wrap; word-wrap: break-word; }}
.assistant .msg-body {{ background: #262626; }}

/* Request metadata */
.request-meta {{ margin-top: 6px; }}
.meta-toggle {{ font-size: 11px; color: var(--text-muted); cursor: pointer; padding: 2px 8px; display: inline-block; }}
.meta-toggle:hover {{ color: var(--blue); }}
.meta-details {{ display: flex; flex-wrap: wrap; gap: 6px; padding: 6px 0; }}
.meta-badge {{ font-size: 11px; padding: 2px 8px; border-radius: 10px; background: var(--bg-deep); color: var(--text-muted); border: 1px solid var(--border-subtle); white-space: nowrap; }}
.meta-model {{ color: var(--purple); border-color: var(--purple); }}
.meta-edited {{ color: var(--green); border-color: var(--green); }}

/* Tool calls */
/* Tool groups */
.tool-group {{ margin: 8px 0; border: 1px solid var(--border-light); border-radius: 8px; background: var(--bg); overflow: hidden; }}
.tool-group-header {{ padding: 8px 12px; background: var(--bg-elevated); cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13px; border-bottom: 1px solid var(--border-subtle); }}
.tool-group-header:hover {{ background: #2a2a2a; }}
.tool-group-chevron {{ font-size: 10px; color: var(--text-muted); transition: transform 0.15s; }}
.tool-group-check {{ color: var(--green); font-size: 13px; }}
.tool-group-title {{ font-weight: 600; color: var(--text); flex: 1; }}
.tool-group-count {{ font-size: 11px; color: var(--text-muted); padding: 1px 8px; background: var(--bg-deep); border-radius: 8px; }}
.tool-group-status {{ font-size: 11px; color: var(--text-muted); }}
.tool-group-content {{ padding: 4px 8px; }}
.tool-group-content .tool-call {{ margin: 4px 0; }}

.tool-call {{ margin: 8px 0; border: 1px solid var(--border-light); border-radius: 6px; background: var(--bg); }}
.tool-header {{ padding: 8px 12px; background: var(--bg-elevated); border-radius: 6px 6px 0 0; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13px; }}
.tool-header:hover {{ background: #2a2a2a; }}
.tool-name {{ font-weight: 600; color: var(--cyan); }}
.tool-summary {{ color: var(--text-muted); font-size: 12px; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.tool-badges {{ display: flex; gap: 6px; align-items: center; flex-shrink: 0; }}
.tool-meta-badge {{ font-size: 10px; padding: 1px 6px; border-radius: 8px; background: var(--bg-deep); color: var(--text-muted); }}
.tool-details {{ padding: 12px; background: var(--bg-deep); border-top: 1px solid var(--border-light); font-size: 12px; max-height: 600px; overflow: auto; }}
.tool-detail-section {{ margin-bottom: 8px; }}
.tool-detail-pre {{ white-space: pre-wrap; margin: 4px 0; padding: 8px; background: #161b22; border: 1px solid var(--border-subtle); border-radius: 4px; font-size: 11px; }}

/* Terminal blocks */
.terminal-block {{ margin: 6px 0; border: 1px solid #1a3a1a; border-radius: 6px; background: #0d1117; overflow: hidden; }}
.terminal-header {{ padding: 6px 12px; background: #161b22; border-bottom: 1px solid #21262d; }}
.terminal-cwd {{ font-size: 10px; color: var(--text-muted); margin-bottom: 2px; }}
.terminal-cmd {{ font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; font-size: 12px; color: var(--green); }}
.terminal-badges {{ padding: 4px 12px; display: flex; gap: 8px; }}
.terminal-output {{ margin: 0; padding: 8px 12px; font-size: 11px; color: #d4d4d4; background: #0d1117; white-space: pre-wrap; word-wrap: break-word; max-height: 400px; overflow: auto; font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; border-top: 1px solid #21262d; }}
.exit-success {{ font-size: 10px; padding: 1px 6px; border-radius: 8px; background: #1a3a1a; color: var(--green); }}
.exit-error {{ font-size: 10px; padding: 1px 6px; border-radius: 8px; background: #3a1a1a; color: var(--red); }}

/* Thinking blocks */
.thinking-block {{ margin: 8px 0; border: 1px solid #3d3080; border-radius: 6px; background: #1a1535; }}
.thinking-header {{ padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 12px; }}
.thinking-header:hover {{ background: #221d45; }}
.thinking-title {{ font-weight: 600; color: var(--purple); }}
.thinking-preview {{ color: var(--text-muted); font-size: 11px; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.thinking-content {{ padding: 12px; background: #12102a; border-top: 1px solid #3d3080; }}
.thinking-pre {{ white-space: pre-wrap; margin: 0; font-size: 12px; color: #c4b5fd; line-height: 1.5; }}
.thinking-done {{ font-size: 11px; color: var(--purple); padding: 4px 12px; opacity: 0.6; }}

/* File edit blocks */
.file-edit-block {{ margin: 8px 0; border: 1px solid #1a3a1a; border-radius: 6px; background: #0d1117; }}
.file-edit-header {{ padding: 8px 12px; background: #161b22; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13px; flex-wrap: wrap; }}
.file-edit-header:hover {{ background: #1c2128; }}
.file-edit-name {{ font-weight: 600; color: var(--green); }}
.file-edit-meta {{ font-size: 11px; color: var(--text-muted); }}
.file-edit-path {{ font-size: 10px; color: var(--text-muted); flex: 1; text-align: right; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.file-edit-content {{ border-top: 1px solid #21262d; max-height: 600px; overflow: auto; }}
.file-edit-pre {{ margin: 0; padding: 12px; font-size: 11px; color: #adbac7; white-space: pre-wrap; font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; }}

/* MCP IO */
.mcp-io {{ margin: 6px 0; }}
.mcp-io-pre {{ background: #161b22; padding: 6px; border: 1px solid var(--border-subtle); border-radius: 4px; font-size: 11px; white-space: pre-wrap; overflow-x: auto; }}

/* Progress tasks */
.progress-task {{ font-size: 12px; color: var(--text-muted); padding: 4px 12px; }}

/* MCP servers */
.mcp-servers {{ font-size: 12px; color: var(--purple); padding: 4px 12px; background: #1a1535; border-radius: 4px; margin: 4px 0; }}

/* Codeblock URI */
.codeblock-uri {{ font-size: 12px; padding: 2px 12px; }}
.codeblock-path {{ color: var(--blue); }}

/* Inline reference */
.inline-ref {{ color: var(--blue); font-size: 13px; }}

/* Attachment items */
.attachment-item {{ margin: 3px 0; }}
.attachment-header {{ display: flex; align-items: center; gap: 8px; padding: 6px 10px; background: #1a1a1a; border: 1px solid var(--border-light); border-radius: 4px; font-size: 12px; cursor: pointer; }}
.attachment-header:hover {{ background: #222; }}
.attachment-name {{ color: var(--cyan); flex: 1; }}
.attachment-meta {{ color: var(--text-muted); font-size: 11px; }}
.attachment-content {{ padding: 8px; background: var(--bg-deep); border: 1px solid var(--border-light); border-radius: 4px; max-height: 400px; overflow: auto; margin-bottom: 4px; }}
.attachment-pre {{ white-space: pre-wrap; margin: 0; font-size: 11px; }}

/* Todo list */
.todo-list-block {{ margin: 6px 0; border: 1px solid var(--border-light); border-radius: 6px; overflow: hidden; }}
.todo-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
.todo-table th {{ background: var(--bg-elevated); padding: 4px 8px; text-align: left; color: var(--text-muted); font-weight: 600; border-bottom: 1px solid var(--border); }}
.todo-table td {{ padding: 4px 8px; border-bottom: 1px solid var(--border-subtle); }}
.todo-done {{ opacity: 0.7; }}
.todo-done td:nth-child(3) {{ text-decoration: line-through; color: var(--text-muted); }}
.todo-progress td:nth-child(3) {{ color: var(--yellow); }}
.todo-pending td:nth-child(3) {{ color: var(--text); }}

/* Search results */
.search-results-block {{ margin: 6px 0; padding: 8px; background: var(--bg-deep); border: 1px solid var(--border-subtle); border-radius: 6px; max-height: 300px; overflow: auto; }}
.search-result-item {{ padding: 2px 4px; font-size: 12px; display: flex; align-items: center; gap: 6px; }}
.search-result-item:hover {{ background: var(--bg-input); }}
.search-file {{ color: var(--blue); font-weight: 600; }}
.search-line {{ color: var(--yellow); font-size: 11px; }}
.search-path {{ color: var(--text-muted); font-size: 10px; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

/* Additional meta badges */
.meta-error {{ color: var(--red); border-color: var(--red); background: #3a1a1a; }}
.meta-tokens {{ color: var(--cyan); border-color: #2a4a5a; }}
.meta-details {{ color: var(--yellow); border-color: var(--yellow); }}
.meta-state {{ }}

/* Footer */
.footer {{ padding: 12px 24px; border-top: 1px solid var(--border); background: var(--bg-elevated); font-size: 12px; color: var(--text-muted); text-align: center; }}

pre {{ margin: 0; }}
code {{ font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; }}
a {{ color: var(--blue); }}

/* Expand all / collapse all buttons */
.controls {{ padding: 8px 24px; background: var(--bg-elevated); border-bottom: 1px solid var(--border); display: flex; gap: 8px; }}
.controls button {{ background: var(--bg-deep); color: var(--text-muted); border: 1px solid var(--border-subtle); padding: 4px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }}
.controls button:hover {{ color: var(--text); border-color: var(--blue); }}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <div class="header-top">
    <div style="width:24px;height:24px;background:linear-gradient(135deg,var(--accent),var(--accent2));border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:11px;">AI</div>
    <h1>{escape_html(title)}</h1>
    <span style="color:var(--text-muted);font-size:12px;margin-left:auto;">{len(requests)} exchanges</span>
  </div>
  <div class="header-stats">
    <span class="header-stat">🤖 {escape_html(models_str)}</span>
    <span class="header-stat">⏱️ Total: {total_time_str}</span>
    <span class="header-stat">📝 Session: {escape_html(session_id[:16])}...</span>
    <span class="header-stat">📁 Workspace: {escape_html(workspace_info)}</span>
  </div>
</div>
<div class="controls">
  <button onclick="expandAll()">▼ Expand all</button>
  <button onclick="collapseAll()">▲ Collapse all</button>
  <button onclick="expandByClass('thinking-content')">💭 All thinking</button>
  <button onclick="expandByClass('terminal-block')">💻 All terminal</button>
</div>
<div class="messages">
'''
    
    if not requests:
        html += '<div style="text-align:center;padding:60px;color:var(--text-muted);"><p>No messages in this session</p></div>'
    else:
        for i, req in enumerate(requests):
            # User message
            user_text = ""
            if 'message' in req:
                msg = req['message']
                if isinstance(msg, dict):
                    if 'text' in msg:
                        user_text = msg['text']
                    elif 'parts' in msg:
                        for part in msg['parts']:
                            if isinstance(part, dict) and 'text' in part:
                                user_text += part['text']
                elif isinstance(msg, str):
                    user_text = msg
            
            user_html = simple_markdown_to_html(user_text)
            
            # Attachments (from variableData)
            attachments_html = ""
            if 'variableData' in req and 'variables' in req['variableData']:
                attachments_html = _format_variable_attachments_html(req['variableData']['variables'])
            
            # Timestamp for user message
            ts_str = ""
            timestamp = req.get('timestamp')
            if timestamp:
                try:
                    ts_str = f'<span style="color:var(--text-muted);font-size:11px;margin-left:auto;">{datetime.fromtimestamp(timestamp/1000).strftime("%H:%M:%S")}</span>'
                except:
                    pass
            
            html += f'''<div class="msg user">
  <div class="avatar user-av">U</div>
  <div class="msg-content">
    <div class="msg-header"><span class="author">You</span><span class="msg-number">#{i+1}</span>{ts_str}</div>
    <div class="msg-body">{user_html}</div>
    {attachments_html}
  </div>
</div>
'''
            
            # Assistant response
            response = req.get('response', '')
            response_html = build_response_html(response)
            
            # Request metadata (model, timing, etc.)
            meta_html = _format_request_metadata_html(req, i)
            
            html += f'''<div class="msg assistant">
  <div class="avatar ai-av">AI</div>
  <div class="msg-content">
    <div class="msg-header"><span class="author">GitHub Copilot</span></div>
    <div class="msg-body">{response_html}</div>
    {meta_html}
  </div>
</div>
'''
    
    html += f'''</div>
<div class="footer">
  Session: {escape_html(session_id)} &bull; Workspace: {escape_html(workspace_info)} &bull; Model: {escape_html(models_str)} &bull; Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
</div>
<script>
function toggle(id) {{
  var el = document.getElementById(id);
  if (el) {{
    var show = el.style.display === 'none';
    el.style.display = show ? 'block' : 'none';
    var chev = document.getElementById('chevron_' + id);
    if (chev) chev.textContent = show ? '\u25bc' : '\u25b6';
  }}
}}
function expandAll() {{
  document.querySelectorAll('[id^="tool_"],[id^="think_"],[id^="edit_"],[id^="meta_"],[id^="att_"],[id^="toolgroup_"]').forEach(function(el) {{ el.style.display = 'block'; }});
  document.querySelectorAll('[id^="chevron_toolgroup_"]').forEach(function(el) {{ el.textContent = '\u25bc'; }});
}}
function collapseAll() {{
  document.querySelectorAll('[id^="tool_"],[id^="think_"],[id^="edit_"],[id^="meta_"],[id^="att_"],[id^="toolgroup_"]').forEach(function(el) {{ el.style.display = 'none'; }});
}}
function expandByClass(cls) {{
  // Toggle visibility of all elements of a given class
  var els = document.querySelectorAll('.' + cls);
  if (!els.length) return;
  var allVisible = true;
  els.forEach(function(el) {{ if (el.closest('[style*="display: none"]') || el.closest('[style*="display:none"]')) allVisible = false; }});
  // For collapsible parents, toggle their corresponding id
  document.querySelectorAll('[id^="think_"],[id^="tool_"],[id^="edit_"]').forEach(function(el) {{
    var hasChild = el.querySelector('.' + cls) || el.classList.contains(cls);
    if (hasChild) el.style.display = el.style.display === 'none' ? 'block' : 'none';
  }});
}}
</script>
</body>
</html>'''
    
    return html


def export_session_to_text(session_data, session_id='unknown'):
    """Export session as plain text."""
    requests = session_data.get('requests', [])
    title = session_data.get('customTitle', session_id)
    
    lines = [f"# Copilot Chat: {title}", f"# Session: {session_id}", f"# Messages: {len(requests)}", ""]
    
    for i, req in enumerate(requests):
        # User
        user_text = ""
        if 'message' in req:
            msg = req['message']
            if isinstance(msg, dict):
                user_text = msg.get('text', '')
            elif isinstance(msg, str):
                user_text = msg
        
        lines.append(f"{'='*60}")
        lines.append(f"[USER] Message {i+1}")
        lines.append(f"{'='*60}")
        lines.append(user_text)
        lines.append("")
        
        # Assistant
        response = req.get('response', '')
        assistant_text = extract_text_from_response(response)
        
        lines.append(f"[ASSISTANT]")
        lines.append(f"{'-'*60}")
        lines.append(assistant_text)
        lines.append("")
    
    return '\n'.join(lines)


# ============================================================================
# Main Export Function
# ============================================================================

def export_session(workspace_id, session_id, vscode_path=None, output_dir='./copilot_export', fmt='html'):
    """Export a session to a file. Returns the output file path."""
    paths = [vscode_path] if vscode_path else detect_vscode_paths()
    
    # Find the session file
    session_file = None
    for vs_path in paths:
        for ext in ['.jsonl', '.json']:
            fp = os.path.join(vs_path, 'User', 'workspaceStorage', 
                             workspace_id, 'chatSessions', f'{session_id}{ext}')
            if os.path.exists(fp):
                session_file = fp
                break
        if session_file:
            break
    
    if not session_file:
        print(f"  ❌ Session file not found: {session_id}")
        return None
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # JSONL: copy original file as-is (raw, lossless) — no parsing needed
    if fmt == 'jsonl':
        import shutil
        ext = os.path.splitext(session_file)[1]  # .jsonl or .json
        out_file = os.path.join(output_dir, f'chat_{session_id[:12]}_{timestamp}{ext}')
        shutil.copy2(session_file, out_file)
        return out_file
    
    # Read & parse session for other formats
    session_data = read_session_file(session_file)
    if not session_data:
        print(f"  ❌ Failed to parse session: {session_id}")
        return None
    
    # Export
    if fmt == 'html':
        content = export_session_to_html(session_data, session_id, workspace_id)
        out_file = os.path.join(output_dir, f'chat_{session_id[:12]}_{timestamp}.html')
    elif fmt == 'text':
        content = export_session_to_text(session_data, session_id)
        out_file = os.path.join(output_dir, f'chat_{session_id[:12]}_{timestamp}.txt')
    elif fmt == 'json':
        content = json.dumps(session_data, indent=2, ensure_ascii=False)
        out_file = os.path.join(output_dir, f'chat_{session_id[:12]}_{timestamp}.json')
    else:
        print(f"  ❌ Unknown format: {fmt}")
        return None
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return out_file


# ============================================================================
# CLI
# ============================================================================

def cmd_workspaces(args):
    """Handle 'workspaces' command."""
    workspaces = list_workspaces(args.vscode_path)
    
    if not workspaces:
        print("No workspaces with chat sessions found.")
        return
    
    print(f"\n{'='*80}")
    print(f"  Found {len(workspaces)} workspace(s) with chat sessions")
    print(f"{'='*80}\n")
    
    # Group by variant
    by_variant = {}
    for ws in workspaces:
        variant = ws['vscode_variant']
        by_variant.setdefault(variant, []).append(ws)
    
    for variant, ws_list in by_variant.items():
        print(f"  📁 {variant}")
        print(f"  {'─'*70}")
        for ws in ws_list:
            name = ws['workspace_name']
            count = ws['sessions_count']
            wid = ws['workspace_id']
            print(f"  {count:>4} sessions  │  {name:<40}  │  {wid}")
        print()


def cmd_sessions(args):
    """Handle 'sessions' command."""
    sessions = list_sessions(args.workspace_id, args.vscode_path)
    
    if not sessions:
        print(f"No sessions found in workspace: {args.workspace_id}")
        return
    
    print(f"\n{'='*80}")
    print(f"  Found {len(sessions)} session(s) in workspace {args.workspace_id}")
    print(f"{'='*80}\n")
    
    for s in sessions:
        title = s['title'] or '(untitled)'
        print(f"  📝 {title}")
        print(f"     ID: {s['id']}")
        print(f"     Messages: {s['messages_count']}  │  Size: {s['size_human']}  │  Modified: {s['modified']}  │  Format: {s['format']}")
        print()


def cmd_export(args):
    """Handle 'export' command."""
    session_ids = args.session
    
    if session_ids == '*':
        # Export all sessions
        sessions = list_sessions(args.workspace_id, args.vscode_path)
        session_ids = [s['id'] for s in sessions]
        print(f"Exporting all {len(session_ids)} sessions...")
    elif ',' in session_ids:
        session_ids = [s.strip() for s in session_ids.split(',')]
    else:
        session_ids = [session_ids]
    
    exported = []
    failed = []
    
    for sid in session_ids:
        print(f"  Exporting {sid}...")
        result = export_session(args.workspace_id, sid, args.vscode_path, 
                              args.output_dir, args.format)
        if result:
            print(f"  ✅ {result}")
            exported.append(result)
        else:
            failed.append(sid)
    
    print(f"\n{'='*60}")
    print(f"  Exported: {len(exported)}  │  Failed: {len(failed)}")
    if exported:
        print(f"  Output: {os.path.abspath(args.output_dir)}")
    print(f"{'='*60}")


def cmd_search(args):
    """Handle 'search' command."""
    print(f"\nSearching for '{args.text}' across all sessions...")
    results = search_sessions(args.text, args.vscode_path)
    
    if not results:
        print("  No matches found.")
        return
    
    print(f"\n  Found {len(results)} matching session(s):\n")
    for r in results:
        print(f"  📍 {r['workspace_name']}")
        print(f"     Workspace ID: {r['workspace_id']}")
        print(f"     Session ID:   {r['session_id']}")
        print(f"     Size: {r['size_human']}  │  VS Code: {r['vscode_variant']}")
        print()


def main():
    # Common arguments shared by all subcommands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--vscode-path', default=None,
                       help='Override VS Code settings path')
    common.add_argument('--output-dir', default='./copilot_export',
                       help='Output directory for exports (default: ./copilot_export)')
    common.add_argument('--format', choices=['html', 'json', 'jsonl', 'text'], default='html',
                       help='Export format: html, json (parsed), jsonl (raw original), text (default: html)')

    parser = argparse.ArgumentParser(
        description='GitHub Copilot Chat Session Export Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s workspaces                                     List all workspaces
  %(prog)s sessions abc123def456                           List sessions in workspace
  %(prog)s export abc123def456 session-id-here             Export a session to HTML
  %(prog)s export abc123def456 * --format json             Export all sessions as JSON (parsed)
  %(prog)s export abc123def456 session-id --format jsonl   Export raw original JSONL file
  %(prog)s search "some text"                              Search across all sessions
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # workspaces
    sub_ws = subparsers.add_parser('workspaces', parents=[common],
                                   help='List all workspaces with chat sessions')
    
    # sessions
    sub_sess = subparsers.add_parser('sessions', parents=[common],
                                     help='List sessions in a workspace')
    sub_sess.add_argument('workspace_id', help='Workspace ID')
    
    # export
    sub_exp = subparsers.add_parser('export', parents=[common],
                                    help='Export session(s) to file')
    sub_exp.add_argument('workspace_id', help='Workspace ID')
    sub_exp.add_argument('session', help='Session ID, comma-separated IDs, or * for all')
    
    # search
    sub_search = subparsers.add_parser('search', parents=[common],
                                       help='Search text across all sessions')
    sub_search.add_argument('text', help='Text to search for')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'workspaces':
        cmd_workspaces(args)
    elif args.command == 'sessions':
        cmd_sessions(args)
    elif args.command == 'export':
        cmd_export(args)
    elif args.command == 'search':
        cmd_search(args)


if __name__ == '__main__':
    main()
