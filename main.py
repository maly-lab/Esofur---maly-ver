import math, sys
from random import random
from exceptions import (
    _divideByZero, _debug, _undefinedKeyword, _alreadyImported,
    _importError, _noEnd, _undeclaredVar, _capError,
    _noLabel, _noStart, _noBoop, _tooManyBoop,
    _castingFail, _unmatchedComment
)

class EsoFurCompiler:
    def __init__(self):
        self.symbol_table = {}
        self.in_comment = False
        self.imported = []
        self.imported_local = []

    def compile(self, code):
        lines = code.split('\n')
        i = 0
        built = False
        module = ''

        if lines.count("Maws") != lines.count("Paws"):
            raise _unmatchedComment()

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # ---------------- BOOT ----------------
            while not built:
                if line == "OwO What's This?":
                    built = True
                    break
                i += 1
                if i >= len(lines):
                    return
                line = lines[i].strip()

            # ---------------- CLEAN EXIT ----------------
            if line == "QwQ":
                print("\033[38;5;15mfinished")
                return

            if "QwQ" not in lines:
                raise _noEnd()

            # ---------------- COMMENTS ----------------
            if line.startswith("Muzzles"):
                i += 1
                continue

            if line == "Maws":
                self.in_comment = True
                i += 1
                continue

            if line == "Paws":
                self.in_comment = False
                i += 1
                continue

            if self.in_comment:
                i += 1
                continue

            # ---------------- LABELS ----------------
            if line.startswith("Marks"):
                i += 1
                continue

            # -------------------------------------------------
            # FIX: REMOVED istitle() CHECK (was breaking syntax)
            # -------------------------------------------------

            # ---------------- VARIABLES ----------------
            if line.startswith('Notices Your'):
                parts = line.split()
                var_name = parts[2]
                self.symbol_table[var_name] = 0   # FIX: no more None
                i += 1
                continue

            # ---------------- ASSIGNMENT ----------------
            if 'Pounces On' in line:
                value, var_name = line.split('Pounces On')
                var_name = var_name.strip()

                if var_name not in self.symbol_table:
                    raise _undeclaredVar(var_name)

                value = value.strip()

                # FIX: convert numbers properly
                if value.isdigit():
                    value = int(value)

                self.symbol_table[var_name] = value
                i += 1
                continue

            # ---------------- PRINT ----------------
            if line.startswith('Howl'):
                var_name = line.split(' ', 1)[1].strip()
                print(self.symbol_table.get(var_name, 0))
                i += 1
                continue

            i += 1


# ================= ENTRY POINT =================

filename = sys.argv[1]

with open(filename) as file:
    code = file.read()

print(code)
print('---------------------')

compiler = EsoFurCompiler()
compiler.compile(code)

sys.exit(0)
