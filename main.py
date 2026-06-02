import sys
from esofur_engine import EsoFurCompiler  # import from new file

# ---------------- READ FILE ----------------
filename = sys.argv[1]

with open(filename) as file:
    code = file.read()

print(code)
print('---------------------')

# ---------------- RUN INTERPRETER ----------------
compiler = EsoFurCompiler()
compiler.compile(code)
