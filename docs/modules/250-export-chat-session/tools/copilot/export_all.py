#!/usr/bin/env python3
"""
Batch export ALL GitHub Copilot chat sessions from ALL workspaces to HTML.

Preserves directory structure:
  <output_dir>/<VSCode Variant>/<workspace_name>/chat_<id>_<ts>.html

Usage:
  python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py
  python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py --output-dir ./work/my_export
  python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py --format json

Default output: ./work/copilot_export_all/
"""

import sys
import os
import re
import argparse

# Import the main export module from the same package directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import chat_export as export_mod


def sanitize_dirname(name):
    """Sanitize a string for use as directory name."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'[_\s]+', '_', name).strip('_. ')
    return name or 'unnamed'


def main():
    parser = argparse.ArgumentParser(
        description='Batch export ALL GitHub Copilot chat sessions from ALL workspaces.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                                          Export all to ./work/copilot_export_all/
  %(prog)s --output-dir ./my_exports                Custom output directory
  %(prog)s --format json                            Export as JSON instead of HTML
  %(prog)s --vscode-path "C:/Users/me/AppData/Roaming/Code - Insiders"
        '''
    )
    parser.add_argument('--output-dir', default=None,
                        help='Output root directory (default: ./work/copilot_export_all)')
    parser.add_argument('--format', choices=['html', 'json', 'jsonl', 'text'], default='html',
                        help='Export format (default: html)')
    parser.add_argument('--vscode-path', default=None,
                        help='Override VS Code settings path')
    args = parser.parse_args()

    # Default output dir: ./work/copilot_export_all relative to project root
    if args.output_dir:
        output_root = os.path.abspath(args.output_dir)
    else:
        # Walk up to find project root (containing 'work' folder)
        project_root = os.path.abspath('.')
        output_root = os.path.join(project_root, 'work', 'copilot_export_all')

    fmt = args.format

    print("=" * 70)
    print(f"  Batch Export: ALL Copilot Chat Sessions → {fmt.upper()}")
    print("=" * 70)

    # 1. Discover all workspaces
    workspaces = export_mod.list_workspaces(args.vscode_path)
    if not workspaces:
        print("\n  ❌ No workspaces with chat sessions found.")
        return

    total_sessions = sum(ws['sessions_count'] for ws in workspaces)
    print(f"\n  Found {len(workspaces)} workspaces, {total_sessions} total sessions")
    print(f"  Output: {output_root}\n")

    exported_total = 0
    failed_total = 0
    skipped_total = 0

    for ws_idx, ws in enumerate(workspaces, 1):
        variant = sanitize_dirname(ws['vscode_variant'])
        ws_name = sanitize_dirname(ws['workspace_name'])
        ws_id = ws['workspace_id']
        vs_path = ws['vscode_path']

        ws_output_dir = os.path.join(output_root, variant, ws_name)
        os.makedirs(ws_output_dir, exist_ok=True)

        print(f"  [{ws_idx}/{len(workspaces)}] 📁 {variant}/{ws_name}  ({ws['sessions_count']} sessions)")

        # List all sessions in this workspace
        sessions = export_mod.list_sessions(ws_id, vs_path)
        if not sessions:
            print(f"           ⚠️  No sessions found (possibly different VS Code path)")
            continue

        ext_map = {'html': '.html', 'json': '.json', 'jsonl': '.jsonl', 'text': '.txt'}
        file_ext = ext_map.get(fmt, '.html')

        for s_idx, sess in enumerate(sessions, 1):
            sid = sess['id']
            title = sess.get('title', '') or 'untitled'
            msg_count = sess.get('messages_count', 0)

            # Check if already exported (by session id prefix in filenames)
            try:
                existing = [f for f in os.listdir(ws_output_dir)
                            if f.startswith(f"chat_{sid[:12]}") and f.endswith(file_ext)]
            except OSError:
                existing = []

            if existing:
                skipped_total += 1
                continue

            try:
                result = export_mod.export_session(
                    ws_id, sid,
                    vscode_path=vs_path,
                    output_dir=ws_output_dir,
                    fmt=fmt
                )
                if result:
                    exported_total += 1
                    if s_idx <= 3 or s_idx == len(sessions):
                        print(f"           ✅ [{s_idx}/{len(sessions)}] {title[:50]} ({msg_count} msgs)")
                    elif s_idx == 4:
                        print(f"           ... exporting remaining sessions ...")
                else:
                    failed_total += 1
                    print(f"           ❌ [{s_idx}/{len(sessions)}] {sid[:12]} - export returned None")
            except Exception as e:
                failed_total += 1
                print(f"           ❌ [{s_idx}/{len(sessions)}] {sid[:12]} - {str(e)[:80]}")

    print(f"\n{'=' * 70}")
    print(f"  ✅ Exported: {exported_total}")
    print(f"  ⏭️  Skipped (already exist): {skipped_total}")
    print(f"  ❌ Failed: {failed_total}")
    print(f"  📂 Output: {output_root}")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
