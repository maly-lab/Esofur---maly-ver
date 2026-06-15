import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: launcher.py <file>")
    sys.exit(1)

result = subprocess.run(["esofur", sys.argv[1]], shell=True)
sys.exit(result.returncode)