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
    --format FORMAT       Output format: html, json, text (default: html)
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


def format_tool_call_html(item, response_list=None, idx=0):
    """Format a tool call item as collapsible HTML."""
    tool_id = item.get('toolId', item.get('toolName', 'unknown'))
    tool_call_id = item.get('toolCallId', f'tc_{idx}')
    is_complete = item.get('isComplete', False)
    
    # Invocation message
    inv_msg = ""
    if 'invocationMessage' in item:
        inv = item['invocationMessage']
        if isinstance(inv, dict):
            inv_msg = inv.get('value', '')
        else:
            inv_msg = str(inv)
    
    # Tool-specific info
    extra_info = ""
    if 'toolSpecificData' in item:
        tsd = item['toolSpecificData']
        if tsd.get('kind') == 'terminal' and 'commandLine' in tsd:
            cmd = tsd['commandLine'].get('original', '')
            extra_info = f'<div style="padding:6px 12px;background:#0d1117;border-top:1px solid #404040;font-size:12px;"><code style="color:#7dd3fc;">{escape_html(cmd)}</code></div>'
    
    # MCP input/output
    io_html = ""
    if 'resultDetails' in item:
        rd = item['resultDetails']
        if 'input' in rd:
            inp = rd['input']
            if isinstance(inp, str):
                try:
                    inp = json.loads(inp)
                except:
                    pass
            inp_str = json.dumps(inp, indent=2, ensure_ascii=False) if isinstance(inp, (dict, list)) else str(inp)
            io_html += f'<div style="margin:6px 0;"><strong>📥 Input:</strong><pre style="background:#161b22;padding:6px;border:1px solid #30363d;border-radius:4px;font-size:11px;white-space:pre-wrap;overflow-x:auto;">{escape_html(inp_str)}</pre></div>'
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
                        io_html += f'<div style="margin:6px 0;"><strong>📤 Output {icon}:</strong><pre style="background:#161b22;padding:6px;border:1px solid #30363d;border-radius:4px;font-size:11px;white-space:pre-wrap;overflow-x:auto;">{escape_html(str(val))}</pre></div>'
            elif isinstance(out, str):
                io_html += f'<div style="margin:6px 0;"><strong>📤 Output:</strong><pre style="background:#161b22;padding:6px;border:1px solid #30363d;border-radius:4px;font-size:11px;white-space:pre-wrap;overflow-x:auto;">{escape_html(out)}</pre></div>'
    
    status = '✅' if is_complete else '⏳'
    safe_id = f"tool_{tool_call_id.replace('-', '_')}_{idx}"
    
    # Display name
    display_name = tool_id
    if tool_id.startswith('mcp_') and '-mcp_' in tool_id:
        parts = tool_id.split('-mcp_')
        if len(parts) == 2:
            display_name = f"[MCP] {parts[0]}: {parts[1]}"
    
    return f'''<div style="margin:8px 0;border:1px solid #404040;border-radius:4px;background:#1e1e1e;">
<div onclick="toggle('{safe_id}')" style="padding:8px 12px;background:#252526;border-radius:4px 4px 0 0;cursor:pointer;display:flex;align-items:center;gap:8px;font-size:13px;">
  <span>🔧</span><span style="flex:1;font-weight:500;">{escape_html(display_name)}</span><span style="font-size:12px;">{status}</span>
</div>
{extra_info}
<div id="{safe_id}" style="display:none;padding:12px;background:#0d1117;border-top:1px solid #404040;font-size:11px;max-height:400px;overflow:auto;">
  <strong>📋 Invocation:</strong><pre style="white-space:pre-wrap;margin:4px 0;padding:6px;background:#161b22;border:1px solid #30363d;border-radius:3px;font-size:11px;">{escape_html(inv_msg)}</pre>
  {io_html}
</div>
</div>'''


def build_response_html(response):
    """Build HTML for the assistant response, interleaving text and tool calls."""
    if not isinstance(response, list):
        if isinstance(response, dict) and 'value' in response:
            return simple_markdown_to_html(str(response['value']))
        return ""
    
    parts = []
    text_buffer = []
    tool_idx = 0
    i = 0
    
    while i < len(response):
        item = response[i]
        
        if isinstance(item, dict) and 'value' in item:
            text_buffer.append(str(item['value']))
            i += 1
        elif isinstance(item, dict) and item.get('kind') == 'inlineReference':
            # File reference
            fs_path = item.get('inlineReference', {}).get('fsPath', '')
            if fs_path:
                name = os.path.basename(fs_path) or fs_path
                text_buffer.append(f' 📁{name} ')
            i += 1
        elif isinstance(item, dict) and item.get('kind') == 'prepareToolInvocation':
            # Flush text buffer
            if text_buffer:
                parts.append(simple_markdown_to_html(''.join(text_buffer)))
                text_buffer = []
            
            # Find matching serialized
            tool_name = item.get('toolName')
            serialized = None
            j = i + 1
            while j < len(response):
                nxt = response[j]
                if isinstance(nxt, dict) and nxt.get('kind') == 'toolInvocationSerialized' and nxt.get('toolId') == tool_name:
                    serialized = nxt
                    break
                j += 1
            
            if serialized:
                parts.append(format_tool_call_html(serialized, response, tool_idx))
                tool_idx += 1
                i = j + 1
            else:
                parts.append(format_tool_call_html(item, response, tool_idx))
                tool_idx += 1
                i += 1
        elif isinstance(item, dict) and item.get('kind') == 'toolInvocationSerialized':
            # Orphaned serialized tool call
            if text_buffer:
                parts.append(simple_markdown_to_html(''.join(text_buffer)))
                text_buffer = []
            parts.append(format_tool_call_html(item, response, tool_idx))
            tool_idx += 1
            i += 1
        else:
            i += 1
    
    # Flush remaining text
    if text_buffer:
        parts.append(simple_markdown_to_html(''.join(text_buffer)))
    
    return '\n'.join(parts)


def format_attachments_html(variables):
    """Format user message attachments."""
    if not variables:
        return ""
    
    parts = []
    for j, var in enumerate(variables):
        kind = var.get('kind', 'unknown')
        name = var.get('name', 'Unknown')
        desc = var.get('modelDescription', '')
        
        icon = {'file': '📄', 'promptFile': '📋'}.get(kind, '🔗')
        att_id = f"att_{j}_{hash(str(var)) % 100000}"
        
        parts.append(f'''<div onclick="toggle('{att_id}')" style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;background:#1a1a1a;border:1px solid #404040;border-radius:4px;font-size:12px;color:#9cdcfe;cursor:pointer;">
  <span>{icon}</span><span style="flex:1;">{escape_html(name)}</span><span style="color:#8c8c8c;font-size:11px;">{escape_html(desc)}</span>
</div>
<div id="{att_id}" style="display:none;padding:8px;background:#0d1117;border:1px solid #404040;border-radius:4px;font-size:11px;max-height:300px;overflow:auto;margin-bottom:4px;">
  <pre style="white-space:pre-wrap;margin:0;font-size:11px;">{escape_html(json.dumps(var, indent=2, ensure_ascii=False))}</pre>
</div>''')
    
    return '\n'.join(parts)


def export_session_to_html(session_data, session_id='unknown', workspace_info=''):
    """Export a session to HTML string."""
    requests = session_data.get('requests', [])
    title = session_data.get('customTitle', f'Session {session_id[:8]}')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Copilot Chat - {escape_html(title)}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: #1e1e1e; color: #cccccc; margin: 0; padding: 0; line-height: 1.6; }}
.container {{ max-width: 860px; margin: 0 auto; min-height: 100vh; display: flex; flex-direction: column; }}
.header {{ background: #252526; padding: 16px 20px; border-bottom: 1px solid #3c3c3c; display: flex; align-items: center; gap: 12px; }}
.header h1 {{ margin: 0; font-size: 16px; font-weight: 600; }}
.messages {{ flex: 1; padding: 20px; }}
.msg {{ margin-bottom: 24px; display: flex; gap: 12px; }}
.avatar {{ width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 600; font-size: 12px; color: white; }}
.user-av {{ background: #0e639c; }}
.ai-av {{ background: linear-gradient(135deg, #0078d4, #005a9e); }}
.msg-content {{ flex: 1; min-width: 0; }}
.msg-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
.author {{ font-weight: 600; font-size: 14px; }}
.msg-body {{ background: #2d2d30; padding: 12px 16px; border-radius: 8px; border: 1px solid #3c3c3c; word-break: break-word; font-size: 14px; }}
.msg-body pre {{ white-space: pre-wrap; word-wrap: break-word; }}
.assistant .msg-body {{ background: #262626; }}
.footer {{ padding: 12px 20px; border-top: 1px solid #3c3c3c; background: #252526; font-size: 12px; color: #8c8c8c; text-align: center; }}
pre {{ margin: 0; }}
code {{ font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; }}
a {{ color: #58a6ff; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <div style="width:24px;height:24px;background:linear-gradient(135deg,#0078d4,#005a9e);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:11px;">AI</div>
  <h1>{escape_html(title)}</h1>
  <span style="color:#8c8c8c;font-size:12px;margin-left:auto;">{len(requests)} messages</span>
</div>
<div class="messages">
'''
    
    if not requests:
        html += '<div style="text-align:center;padding:60px;color:#8c8c8c;"><p>No messages in this session</p></div>'
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
            
            # Attachments
            attachments_html = ""
            if 'variableData' in req and 'variables' in req['variableData']:
                attachments_html = format_attachments_html(req['variableData']['variables'])
            
            html += f'''<div class="msg user">
  <div class="avatar user-av">U</div>
  <div class="msg-content">
    <div class="msg-header"><span class="author">You</span></div>
    <div class="msg-body">{user_html}</div>
    {attachments_html}
  </div>
</div>
'''
            
            # Assistant response
            response = req.get('response', '')
            response_html = build_response_html(response)
            
            html += f'''<div class="msg assistant">
  <div class="avatar ai-av">AI</div>
  <div class="msg-content">
    <div class="msg-header"><span class="author">GitHub Copilot</span></div>
    <div class="msg-body">{response_html}</div>
  </div>
</div>
'''
    
    html += f'''</div>
<div class="footer">
  Session: {escape_html(session_id)} &bull; Workspace: {escape_html(workspace_info)} &bull; Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
</div>
<script>
function toggle(id) {{
  var el = document.getElementById(id);
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
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
    
    # Read session
    session_data = read_session_file(session_file)
    if not session_data:
        print(f"  ❌ Failed to parse session: {session_id}")
        return None
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Export
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
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
    common.add_argument('--format', choices=['html', 'json', 'text'], default='html',
                       help='Export format (default: html)')

    parser = argparse.ArgumentParser(
        description='GitHub Copilot Chat Session Export Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s workspaces                                     List all workspaces
  %(prog)s sessions abc123def456                           List sessions in workspace
  %(prog)s export abc123def456 session-id-here             Export a session to HTML
  %(prog)s export abc123def456 * --format json             Export all sessions as JSON
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
