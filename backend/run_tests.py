#!/usr/bin/env python3
"""
Test runner script for the backend application.
This script sets up the test environment and runs the test suite.
"""

import os
import sys
import subprocess
import time

def setup_test_environment():
    """Set up test environment variables"""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DATABASE_URL"] = "postgresql://intsea:OceanHides1000Pearls@localhost:5433/intseadb_test"
    os.environ["REDIS_URL"] = "redis://localhost:6380"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["DEBUG"] = "true"

def wait_for_services():
    """Wait for test services to be ready"""
    print("Waiting for test services to be ready...")
    time.sleep(10)  # Give services time to start
    print("Services should be ready now.")

def run_tests():
    """Run the test suite"""
    print("Starting test suite...")
    
    # Run pytest with verbose output using virtual environment Python
    venv_python = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        python_executable = venv_python
    else:
        python_executable = sys.executable
    
    result = subprocess.run([
        python_executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "--cov=app",
        "--cov-report=term-missing"
    ])
    
    return result.returncode

if __name__ == "__main__":
    setup_test_environment()
    wait_for_services()
    
    exit_code = run_tests()
    sys.exit(exit_code)
