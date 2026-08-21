#!/usr/bin/env python3
"""Direct launcher for the skills CLI source checkout."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from skills_cli.__main__ import main


if __name__ == "__main__":
    main()
