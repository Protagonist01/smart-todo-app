"""
Smart Todo Application
Main entry point for the application
"""

import sys
from pathlib import Path
from src.cli.interface import main

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    main()