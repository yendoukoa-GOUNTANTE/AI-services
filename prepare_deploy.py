#!/usr/bin/env python3
import os
import sys
import subprocess

def check_env():
    print("Checking environment...")
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"]
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        print(f"Warning: Missing environment variables: {', '.join(missing)}")
    else:
        print("Environment variables OK.")

def verify_config():
    print("Verifying configuration files...")
    files = ["Dockerfile", "cloudbuild.yaml", "app.py", "requirements.txt"]
    for f in files:
        if os.path.exists(f):
            print(f"  [OK] {f} exists.")
        else:
            print(f"  [ERROR] {f} is missing!")
            return False
    return True

def run_tests():
    print("Running backend tests...")
    try:
        # PYTHONPATH=. python3 -m pytest
        result = subprocess.run(["python3", "-m", "pytest"], capture_output=True, text=True, env={**os.environ, "PYTHONPATH": "."})
        if result.returncode == 0:
            print("  [OK] Tests passed.")
            return True
        else:
            print("  [ERROR] Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"  [ERROR] Could not run tests: {e}")
        return False

def main():
    print("--- Yendoukoa AI Deployment Preparation ---")
    check_env()
    if not verify_config():
        sys.exit(1)

    # Optional: run tests
    # if not run_tests():
    #     sys.exit(1)

    print("\nPreparation complete. You can now deploy using:")
    print("gcloud builds submit --config cloudbuild.yaml")

if __name__ == "__main__":
    main()
