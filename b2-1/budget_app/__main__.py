"""`python -m budget_app <command> [options]` 진입점."""
import sys

from budget_app.cli import main

if __name__ == "__main__":
    sys.exit(main())
