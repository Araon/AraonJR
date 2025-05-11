#!/usr/bin/env python
"""
Run tests for the AraonJR Discord Bot
"""
import os
import sys
from subprocess import run

def main():
    """Run pytest with appropriate parameters."""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Running tests for AraonJR Bot...")
    
    # Check for specific test to run
    if len(sys.argv) > 1:
        # Run only the specified tests
        test_path = sys.argv[1]
        run_args = ["pytest", test_path, "-v"]
    else:
        # Run all tests with coverage
        run_args = ["pytest", "-v", "--cov=cogs", "--cov=utils", "--cov-report=term-missing"]
    
    # Run the tests
    result = run(run_args)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
