class EsoFurCompiler:
    def __init__(self):
        self.symbol_table = {}
        self.in_comment = False
        self.imported = []
        self.imported_local = []

    # ---------------- ERROR HANDLER ----------------
    def _error(self, i, line, reason, fix):
        # ---------------- FURRY STYLE HEADER (PRESERVED) ----------------
        print("TAKE OFF YOUR FURSUIT HEAD I CAN'T HEAR YOU")
        print("------------------------------------------------")

        # ---------------- TECHNICAL INFO ----------------
        print(f"EsoFur Error (Line {i + 1})")
        print(f"Reason: {reason}")
        print(f"Offending line: {line}")

        # ---------------- HELP ----------------
        print(f"Fix: {fix}")

        raise SystemExit(1)

    # ---------------- COMPILER CORE ----------------
    def compile(self, code):
        lines = code.split('\n')
        i = 0
        built = False
        module = ''

        # ---------------- COMMENT BALANCE CHECK ----------------
        if lines.count("Maws") != lines.count("Paws"):
            self._error(
                0,
                "",
                "Unmatched comment blocks",
                "Ensure every 'Maws' has a matching 'Paws'"
            )

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # ---------------- BOOT STRAP (PROGRAM START) ----------------
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
                self._error(
                    i,
                    line,
                    "Missing program end marker",
                    "Every EsoFur program must contain 'QwQ'"
                )

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

            # ---------------- VARIABLE DECLARATION ----------------
            if line.startswith('Notices Your'):
                parts = line.split()

                if len(parts) < 3:
                    self._error(
                        i,
                        line,
                        "Invalid variable declaration",
                        "Use format: 'Notices Your <variable>'"
                    )

                var_name = parts[2]
                self.symbol_table[var_name] = 0
                i += 1
                continue

            # ---------------- ASSIGNMENT ----------------
            if 'Pounces On' in line:
                value, var_name = line.split('Pounces On')
                var_name = var_name.strip()
                value = value.strip()

                if var_name not in self.symbol_table:
                    self._error(
                        i,
                        line,
                        f"Undeclared variable '{var_name}'",
                        f"Declare it first using 'Notices Your {var_name}'"
                    )

                if value.isdigit():
                    value = int(value)

                self.symbol_table[var_name] = value
                i += 1
                continue

            # ---------------- PRINT ----------------
            if line.startswith('Howl'):
                parts = line.split(' ', 1)

                if len(parts) < 2:
                    self._error(
                        i,
                        line,
                        "Missing variable in print statement",
                        "Use format: Howl <variable>"
                    )

                var_name = parts[1].strip()
                print(self.symbol_table.get(var_name, 0))

                i += 1
                continue

            # ---------------- UNKNOWN SYNTAX ----------------
            self._error(
                i,
                line,
                "Unknown or invalid syntax",
                "Check EsoFur keyword spelling and capitalization"
            )
