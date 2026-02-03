#!/usr/bin/env python3
"""
Bulk File Processing with AI Agent - Example Script
Validates multiple walkthrough.md files using GitHub Copilot CLI
"""

import os
import subprocess
from pathlib import Path

# Configuration
INSTRUCTION_FILE = Path("./tools/validate-walkthrough.instruction.md")
MODULES_PATH = Path("../../../docs/modules")  # Adjust based on your structure
NODE_PATH = "C:\\Java\\nvm\\v20.19.0"  # Adjust to your nvm path
COPILOT_BAT = r"c:\Users\<USERNAME>\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\copilotCli\copilot.bat"

# Find copilot.bat automatically
def find_copilot_bat():
    """Find copilot.bat in system"""
    result = subprocess.run(['where.exe', 'copilot'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().split('\n')[0]
    return None

# Auto-detect paths
copilot_path = find_copilot_bat()
if copilot_path:
    COPILOT_BAT = copilot_path

# Find all walkthrough.md files
walkthroughs = sorted(MODULES_PATH.rglob("walkthrough.md"))

print(f"Found {len(walkthroughs)} walkthrough files\n")

# Setup environment
env = os.environ.copy()
env['PATH'] = f"{NODE_PATH};{env.get('PATH', '')}"

# Store current directory
original_dir = Path.cwd()
instruction_file_abs = (original_dir / INSTRUCTION_FILE).resolve()

for counter, walkthrough_path in enumerate(walkthroughs, 1):
    module_name = walkthrough_path.parent.name
    module_dir = walkthrough_path.parent.resolve()
    
    print(f"[{counter}/{len(walkthroughs)}] Processing: {module_name}")
    
    # Change to module directory
    os.chdir(module_dir)
    
    # Get relative path to instruction
    try:
        instruction_relative = os.path.relpath(instruction_file_abs, module_dir)
    except ValueError:
        instruction_relative = str(instruction_file_abs)
    
    try:
        # Run copilot CLI from module directory
        print(f"  → Running AI agent...\n")
        result = subprocess.run(
            [COPILOT_BAT, "-p", f"@{instruction_relative}", 
             "--add-dir", ".", 
             "--allow-all", 
             "--no-ask-user", 
             "-s"],
            env=env,
            timeout=120
        )
        
        # Check result
        todo_path = module_dir / "todo.md"
        if todo_path.exists():
            print(f"\n  ✓ Validation complete, todo.md created")
        else:
            print(f"\n  ⚠️ Validation ran but todo.md not found")
            
    except FileNotFoundError as e:
        print(f"  ⚠️ Copilot CLI not found: {e}")
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ Timeout (120s)")
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    finally:
        os.chdir(original_dir)
    
    print()

print("=" * 40)
print("✓ Complete!")
print("=" * 40)
print(f"\nProcessed {len(walkthroughs)} modules")
