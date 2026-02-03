#!/usr/bin/env python3
"""
KISS: Simple validation script for walkthrough.md files
Uses GitHub Copilot CLI to validate each file
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
INSTRUCTION_FILE = Path("./instructions/validate-walkthrough.instruction.md")
MODULES_PATH = Path("./docs/modules")
NODE_PATH = "C:\\Java\\nvm\\v20.19.0"
COPILOT_BAT = r"c:\Users\Oleksandr_Baglai\AppData\Roaming\Code - Insiders\User\globalStorage\github.copilot-chat\copilotCli\copilot.bat"

# Find all walkthrough.md files
walkthroughs = sorted(MODULES_PATH.rglob("walkthrough.md"))

print(f"Found {len(walkthroughs)} walkthrough files\n")

# Setup environment for Node.js and Copilot CLI
env = os.environ.copy()
env['PATH'] = f"{NODE_PATH};{env.get('PATH', '')}"

# Store current directory and make paths absolute
original_dir = Path.cwd()
instruction_file_abs = (original_dir / INSTRUCTION_FILE).resolve()

for counter, walkthrough_path in enumerate(walkthroughs, 1):
    module_name = walkthrough_path.parent.name
    module_dir = walkthrough_path.parent.resolve()
    
    print(f"[{counter}/{len(walkthroughs)}] Processing: {module_name}")
    
    # Change to module directory
    os.chdir(module_dir)
    
    # Construct relative path to instruction file from module directory
    try:
        instruction_relative = os.path.relpath(instruction_file_abs, module_dir)
    except ValueError:
        # On Windows, relpath fails if paths are on different drives
        instruction_relative = str(instruction_file_abs)
    
    try:
        # Run copilot from module directory - output goes directly to terminal
        print(f"  → Running GitHub Copilot CLI...\n")
        result = subprocess.run(
            [COPILOT_BAT, "-p", f"@{instruction_relative}", 
             "--add-dir", ".", 
             "--allow-all", 
             "--no-ask-user", 
             "-s"],
            env=env,
            timeout=120
        )
        
        # Check if todo.md was created
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
        # Always return to original directory
        os.chdir(original_dir)
    
    print()

print("=" * 40)
print("✓ Complete!")
print("=" * 40)
print(f"\nProcessed {len(walkthroughs)} modules")
print("Check each module folder for todo.md with validation results")
