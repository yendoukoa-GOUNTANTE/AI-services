#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# Custom Colors for CLI
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def log_info(message):
    print(f"{BLUE}[INFO]{RESET} {message}")

def log_success(message):
    print(f"{GREEN}[SUCCESS]{RESET} {message}")

def log_warning(message):
    print(f"{YELLOW}[WARNING]{RESET} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{RESET} {message}")

def run_command(args, cwd=None, env=None, description=""):
    log_info(f"Running: {description}")
    # Construct full env if PYTHONPATH needed
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    result = subprocess.run(args, cwd=cwd, env=full_env, capture_output=True, text=True)
    if result.returncode == 0:
        log_success(f"{description} completed successfully.")
        return True, result.stdout
    else:
        log_error(f"{description} failed.")
        print(f"--- STDOUT ---\n{result.stdout}")
        print(f"--- STDERR ---\n{result.stderr}")
        return False, result.stderr

def run_flake8():
    args = [
        "uv", "run", "--with", "flake8",
        "flake8", ".",
        "--exclude=.venv,venv,node_modules,build,dist,.git",
        "--ignore=E501,E302,E128,E305,E261,E701,E702,E225,E251,E111,E114,W291,W293,W391,E203,E303,E722,E402,F401,F841,F811,E117,E127,F541,E741,W504,E226,E301"
    ]
    return run_command(args, description="Code syntax checking (flake8)")

def run_tests():
    # Set PYTHONPATH=. so that 'app' module can be found
    args = ["uv", "run", "--with-requirements", "requirements.txt", "--with", "pytest-mock", "pytest"]
    return run_command(args, env={"PYTHONPATH": "."}, description="Unit test execution (pytest)")

def run_translations():
    args = ["uv", "run", "--with", "Babel", "pybabel", "compile", "-d", "translations"]
    return run_command(args, description="Translation compilation (Babel)")

def run_frontend_build():
    # First make sure npm dependencies are installed, then build
    log_info("Installing frontend dependencies...")
    install_args = ["npm", "install"]
    ok, err = run_command(install_args, cwd="marketplace-frontend", description="npm install")
    if not ok:
        return False, err

    build_args = ["npm", "run", "build"]
    return run_command(build_args, cwd="marketplace-frontend", description="React marketplace build")

def run_packaging():
    # Remove existing build and dist folders if any to build cleanly
    for folder in ["build", "dist", "ai_services_agent.egg-info"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    args = ["uv", "run", "--with", "setuptools", "--with", "wheel", "python", "setup.py", "sdist", "bdist_wheel"]
    return run_command(args, description="Python package distribution build")

def main():
    print(f"{BLUE}===================================================={RESET}")
    print(f"{BLUE}      Yendoukoa AI - Custom Release Validation      {RESET}")
    print(f"{BLUE}===================================================={RESET}\n")

    steps = [
        ("Flake8 Code Syntax Checking", run_flake8),
        ("Babel Translation Compilation", run_translations),
        ("React Marketplace Frontend Build", run_frontend_build),
        ("Python Distribution Packaging", run_packaging),
        ("Unit Test Execution (pytest)", run_tests)
    ]

    for name, step_func in steps:
        print(f"\n{BLUE}--- Step: {name} ---{RESET}")
        success, _ = step_func()
        if not success:
            log_error(f"Release validation failed on step: {name}")
            sys.exit(1)

    print(f"\n{GREEN}===================================================={RESET}")
    print(f"{GREEN}   All release validation checks passed! Ready for Prod!   {RESET}")
    print(f"{GREEN}===================================================={RESET}")

if __name__ == "__main__":
    main()
