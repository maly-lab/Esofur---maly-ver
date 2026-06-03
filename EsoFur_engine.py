import math
import sys
from random import random
from exceptions import *


class EsoFurCompiler:
    def __init__(self):
        self.symbol_table = {}
        self.in_comment = False
        self.imported = []
        self.imported_local = []

    # ---------------- ERROR HANDLER ----------------
    def _error(self, i, line, reason, fix):
        print("TAKE OFF YOUR FURSUIT HEAD I CAN'T HEAR YOU")
        print("------------------------------------------------")
        print(f"EsoFur Error (Line {i + 1})")
        print(f"Reason: {reason}")
        print(f"Offending line: {line}")
        print(f"Fix: {fix}")
        raise SystemExit(1)

    # ---------------- COMPILER CORE ----------------
    def compile(self, code):
        lines = code.split("\n")
        i = 0
        built = False
        module = ""

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

            # ---------------- BOOT STRAP ----------------
            while not built:
                if line == "OwO What's This?":
                    built = True
                    break

                i += 1
                if i >= len(lines):
                    return

                line = lines[i].strip()

            # START MARKER
            if line == "OwO What's This?":
                i += 1
                continue

            # ---------------- CLEAN EXIT ----------------
            if line == "QwQ":
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

            # ---------------- SYNTAX CHECK ----------------
            if not line.istitle():
                self._error(
                    i,
                    line,
                    "Capitalisation error",
                    "Every keyword must be written in Title Case"
                )

            # ---------------- IMPORTS ----------------
            if line.startswith("Drag"):
                parse = line.split()  # Drag [function] From [module]
                if len(parse) < 4 or parse[2] != "From":
                    self._error(
                        i,
                        line,
                        "Malformed import statement",
                        "Use: Drag <function> From <module>  or  Drag Everything From <module>"
                    )
                try:
                    if parse[1] == "Everything":
                        if parse[3] in self.imported:
                            self._error(i, line, f"Module '{parse[3]}' already imported", "Remove the duplicate import")
                        module += "\n" + self._grabfile(parse[3])
                        self.imported.append(parse[3])
                    else:
                        key = parse[3] + "." + parse[1]
                        if key in self.imported_local or parse[3] in self.imported:
                            self._error(i, line, f"'{key}' already imported", "Remove the duplicate import")
                        module += "\n" + self._grabfile(parse[3], parse[1])
                        self.imported_local.append(key)
                        self.imported.append(parse[3])
                except SystemExit:
                    raise
                except Exception:
                    self._error(i, line, f"Failed to import module '{parse[3]}'", "Check the module file exists and is valid")

                # Execute module code so its functions are available
                try:
                    parse_value = self._parse_value
                    exec(module, globals(), locals())
                except SystemExit:
                    pass
                except Exception:
                    self._error(i, line, "Module execution failed", "Check the module for errors")

                i += 1
                continue

            # Run any already-loaded module code for module-prefixed calls
            try:
                parse_value = self._parse_value
                for mod in self.imported_local:
                    if line.startswith(mod):
                        line = line.split(".")[1]
                        break
                exec(module, globals(), locals())
            except SystemExit:
                i += 1
                continue
            except Exception:
                pass

            # ---------------- VARIABLE DECLARATION ----------------
            if line.startswith("Notices Your"):
                parts = line.split()

                if len(parts) < 3:
                    self._error(i, line, "Invalid variable declaration", "Use: Notices Your <variable>")

                var_name = parts[2]
                self.symbol_table[var_name] = None
                i += 1
                continue

            # ---------------- ASSIGNMENT ----------------
            if "Pounces On" in line:
                parts = line.split("Pounces On")

                if len(parts) != 2:
                    self._error(i, line, "Malformed assignment", "Use: <value> Pounces On <variable>")

                value_str = parts[0].strip()
                var_name = parts[1].strip()

                if var_name not in self.symbol_table:
                    self._error(
                        i,
                        line,
                        f"Undeclared variable '{var_name}'",
                        f"Declare it first using: Notices Your {var_name}"
                    )

                self.symbol_table[var_name] = self._assign(value_str)
                i += 1
                continue

            # ---------------- JUMPS ----------------
            if "Nuzzles" in line:
                if not line.startswith("Nuzzles"):
                    # Conditional jump: <condition> Nuzzles <label>
                    condition_str, label_str = line.split("Nuzzles", 1)
                    condition = self._parse_value(condition_str.strip())
                    label = self._assign(label_str.strip())
                    if bool(condition):
                        if str(label).isdigit():
                            i += int(label)
                        else:
                            i = self._find_label_index(lines, label)
                    else:
                        i += 1
                else:
                    # Unconditional jump: Nuzzles <label>
                    label = self._assign(line.split()[1].strip())
                    if isinstance(label, int):
                        i += label
                    else:
                        i = self._find_label_index(lines, label)
                continue

            # ---------------- LOOPS ----------------
            if line == "*Starts Roleplaying*":
                i += 1
                continue

            if line.startswith("*Stops Roleplaying Because Of") and line.endswith("*"):
                condition_str = line.split(" ")[-1][:-1].strip()
                condition = self._parse_value(condition_str)
                if bool(condition):
                    i = self._find_loop_start_index(lines, i)
                else:
                    i += 1
                continue

            # ---------------- PRINT ----------------
            if line.startswith("Howl"):
                parts = line.split(" ", 1)

                if len(parts) < 2:
                    self._error(i, line, "Missing print target", "Use: Howl <variable or value>")

                value = self._assign(parts[1].strip())
                print(value)
                i += 1
                continue

            # ---------------- RANDOM FLOAT ----------------
            if line.startswith("Eyedropper A Sparkledog At"):
                parts = line.split()
                if len(parts) < 5:
                    self._error(i, line, "Malformed random command", "Use: Eyedropper A Sparkledog At <variable>")
                var_name = parts[4]
                self.symbol_table[var_name] = random()
                i += 1
                continue

            # ---------------- USER INPUT ----------------
            if line.startswith("Boop The User For"):
                text = line.split(" ", 6)
                if len(text) < 5:
                    self._error(i, line, "Malformed input command", "Use: Boop The User For <variable> [With <prompt>]")
                var_name = text[4]
                prompt = ""
                if len(text) == 7:
                    if text[5] != "With":
                        self._error(i, line, "Missing 'With' keyword in input command", "Use: Boop The User For <variable> With <prompt>")
                    prompt = str(self._assign(text[6])) + ":"
                if len(text) > 7:
                    self._error(i, line, "Too many arguments in input command", "Use: Boop The User For <variable> [With <prompt>]")
                try:
                    value = input(prompt)
                except ValueError:
                    sys.stdin = open(0, "r")
                    value = input(prompt)
                self.symbol_table[var_name] = self._assign(value)
                i += 1
                continue

            # ---------------- TYPE CASTING ----------------
            if "Transforms Into" in line:
                parts = line.split("Transforms Into")
                if len(parts) != 2:
                    self._error(i, line, "Malformed type cast", "Use: <variable> Transforms Into <type>")
                var_name = parts[0].strip()
                type_name = parts[1].strip()
                value = self._parse_value(var_name)
                self.symbol_table[var_name] = self._cast_value(value, type_name, i, line)
                i += 1
                continue

            # ---------------- MATHS ----------------
            if "Inflates By" in line:
                self._do_maths(line, "Inflates By", "+", i)
                i += 1
                continue

            if "Pays" in line:
                self._do_maths(line, "Pays", "-", i)
                i += 1
                continue

            if "Breeds By" in line:
                self._do_maths(line, "Breeds By", "*", i)
                i += 1
                continue

            if "Baps" in line:
                self._do_maths(line, "Baps", "/", i)
                i += 1
                continue

            if "Deflates By" in line:
                self._do_maths(line, "Deflates By", "%", i)
                i += 1
                continue

            if "Gets Vored By" in line:
                self._do_maths(line, "Gets Vored By", "l", i)
                i += 1
                continue

            if "Hyper-Inflates By" in line:
                self._do_maths(line, "Hyper-Inflates By", "^", i)
                i += 1
                continue

            # ---------------- UNKNOWN SYNTAX ----------------
            self._error(
                i,
                line,
                "Unknown or invalid syntax",
                "Check EsoFur keyword spelling and capitalization"
            )

    # ---------------- REPL EXECUTION ----------------
    def execute_line(self, line):
        i = 0
        line = line.strip()

        if not line:
            return None

        # ---------------- COMMENTS ----------------
        if line.startswith("Muzzles"):
            return None

        if line == "Maws":
            self.in_comment = True
            return None

        if line == "Paws":
            self.in_comment = False
            return None

        if self.in_comment:
            return None

        # ---------------- VARIABLE DECLARATION ----------------
        if line.startswith("Notices Your"):
            parts = line.split()

            if len(parts) < 3:
                self._error(i, line, "Invalid variable declaration", "Use: Notices Your <variable>")

            var_name = parts[2]
            self.symbol_table[var_name] = None
            return None

        # ---------------- ASSIGNMENT ----------------
        if "Pounces On" in line:
            parts = line.split("Pounces On")

            if len(parts) != 2:
                self._error(i, line, "Malformed assignment", "Use: <value> Pounces On <variable>")

            value_str = parts[0].strip()
            var_name = parts[1].strip()

            if var_name not in self.symbol_table:
                self._error(
                    i,
                    line,
                    f"Undeclared variable '{var_name}'",
                    f"Declare it first using: Notices Your {var_name}"
                )

            self.symbol_table[var_name] = self._assign(value_str)
            return None

        # ---------------- PRINT ----------------
        if line.startswith("Howl"):
            parts = line.split(" ", 1)

            if len(parts) < 2:
                self._error(i, line, "Missing print target", "Use: Howl <variable or value>")

            value = self._assign(parts[1].strip())
            return value

        # ---------------- RANDOM FLOAT ----------------
        if line.startswith("Eyedropper A Sparkledog At"):
            parts = line.split()
            if len(parts) < 5:
                self._error(i, line, "Malformed random command", "Use: Eyedropper A Sparkledog At <variable>")
            var_name = parts[4]
            self.symbol_table[var_name] = random()
            return None

        # ---------------- USER INPUT ----------------
        if line.startswith("Boop The User For"):
            text = line.split(" ", 6)
            if len(text) < 5:
                self._error(i, line, "Malformed input command", "Use: Boop The User For <variable> [With <prompt>]")
            var_name = text[4]
            prompt = ""
            if len(text) == 7:
                if text[5] != "With":
                    self._error(i, line, "Missing 'With' keyword", "Use: Boop The User For <variable> With <prompt>")
                prompt = str(self._assign(text[6])) + ":"
            try:
                value = input(prompt)
            except ValueError:
                sys.stdin = open(0, "r")
                value = input(prompt)
            self.symbol_table[var_name] = self._assign(value)
            return None

        # ---------------- TYPE CASTING ----------------
        if "Transforms Into" in line:
            parts = line.split("Transforms Into")
            if len(parts) != 2:
                self._error(i, line, "Malformed type cast", "Use: <variable> Transforms Into <type>")
            var_name = parts[0].strip()
            type_name = parts[1].strip()
            value = self._parse_value(var_name)
            self.symbol_table[var_name] = self._cast_value(value, type_name, i, line)
            return None

        # ---------------- MATHS ----------------
        if "Inflates By" in line:
            self._do_maths(line, "Inflates By", "+", i)
            return None

        if "Pays" in line:
            self._do_maths(line, "Pays", "-", i)
            return None

        if "Breeds By" in line:
            self._do_maths(line, "Breeds By", "*", i)
            return None

        if "Baps" in line:
            self._do_maths(line, "Baps", "/", i)
            return None

        if "Deflates By" in line:
            self._do_maths(line, "Deflates By", "%", i)
            return None

        if "Gets Vored By" in line:
            self._do_maths(line, "Gets Vored By", "l", i)
            return None

        if "Hyper-Inflates By" in line:
            self._do_maths(line, "Hyper-Inflates By", "^", i)
            return None

        # ---------------- UNKNOWN ----------------
        self._error(i, line, "Unknown keyword", "Invalid EsoFur command")
        return None

    # ================================================
    # ---------------- HELPER METHODS ----------------
    # ================================================

    def _find_label_index(self, lines, label):
        """Find the line index of a Marks label."""
        for idx, l in enumerate(lines):
            if l.strip().startswith("Marks") and l.strip().split(" ")[1] == label:
                return idx
        self._error(0, label, f"Label '{label}' not found", "Ensure the label is defined with: Marks <label>")

    def _find_loop_start_index(self, lines, end_index):
        """Walk backwards from a loop end to find the matching *Starts Roleplaying* line, supporting nesting."""
        loop_count = 0
        for idx in range(end_index - 1, -1, -1):
            stripped = lines[idx].strip()
            if stripped.startswith("*Stops Roleplaying Because Of") and stripped.endswith("*"):
                loop_count += 1
            if stripped == "*Starts Roleplaying*":
                if loop_count == 0:
                    return idx
                else:
                    loop_count -= 1
        self._error(end_index, "*Stops Roleplaying*", "No matching loop start found", "Add '*Starts Roleplaying*' before this loop end")

    def _assign(self, value_str):
        """Resolve a value string to a Python value: integer literal, quoted string, or variable lookup."""
        value_str = str(value_str)
        if value_str.isdigit():
            return int(value_str)
        if '"' in value_str:
            return value_str[value_str.find('"') + 1:value_str.rfind('"')]
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        return value_str

    def _parse_value(self, value_str):
        """Evaluate a value string, supporting literals, variables, and expressions."""
        value_str = str(value_str)
        if value_str.isdigit():
            return int(value_str)
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        try:
            return eval(value_str, {}, self.symbol_table)
        except Exception:
            self._error(0, value_str, f"Cannot evaluate expression '{value_str}'", "Check the expression uses valid variables and operators")

    def _cast_value(self, value, type_name, i=0, line=""):
        """Cast a value to the requested EsoFur type."""
        type_map = {
            "Int":      int,
            "Float":    float,
            "Str":      str,
            "List":     list,
            "Furpile":  set,
        }
        if type_name not in type_map:
            self._error(i, line, f"Unknown type '{type_name}'", "Valid types: Int, Float, Str, List, Furpile")
        try:
            return type_map[type_name](value)
        except (ValueError, TypeError):
            self._error(i, line, f"Cannot cast '{value}' to {type_name}", "Check the value is compatible with the target type")

    def _do_maths(self, line, keyword, operation, i=0):
        """Apply a math operation between two operands and store the result in the left variable."""
        var_1, var_2 = map(str.strip, line.split(keyword, 1))
        num_1 = self._parse_value(var_1)
        num_2 = self._parse_value(var_2)

        if operation == "+":
            num_1 += num_2
        elif operation == "-":
            num_1 -= num_2
        elif operation == "*":
            num_1 *= num_2
        elif operation == "/":
            if num_2 == 0:
                self._error(i, line, "Division by zero", "The divisor (right-hand value) must not be zero")
            num_1 = num_1 / num_2
        elif operation == "%":
            num_1 %= num_2
        elif operation == "l":
            num_1 = math.log(num_1, num_2)
        elif operation == "^":
            num_1 **= num_2

        self.symbol_table[var_1] = num_1

    def _grabfile(self, module, *word):
        """Read an EsoFur module file, optionally extracting a single named block."""
        with open(module + ".EsoFurMod", "r") as f:
            source_code = f.read()
        if not word:
            return source_code
        blocks = source_code.split("#NEXT")
        for block in blocks:
            if block.startswith("\n#" + word[0]):
                return block
        self._error(0, module, f"Function '{word[0]}' not found in module '{module}'", "Check the module file contains a matching #NEXT block")
