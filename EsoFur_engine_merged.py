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

    def _error(self, i, line, reason, fix):
        print("TAKE OFF YOUR FURSUIT HEAD I CAN'T HEAR YOU")
        print("------------------------------------------------")
        print(f"EsoFur Error (Line {i + 1})")
        print(f"Reason: {reason}")
        print(f"Offending line: {line}")
        print(f"Fix: {fix}")
        raise SystemExit(1)

    def compile(self, code):
        lines = code.split("\\n")
        i = 0
        built = False
        module = ""

        if lines.count("Maws") != lines.count("Paws"):
            self._error(0, "", "Unmatched comment blocks",
                        "Ensure every 'Maws' has a matching 'Paws'")

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            while not built:
                if line == "OwO What's This?":
                    built = True
                    break
                i += 1
                if i >= len(lines):
                    return
                line = lines[i].strip()

            if line == "OwO What's This?":
                i += 1
                continue

            if line == "QwQ":
                return

            if "QwQ" not in lines:
                self._error(i, line, "Missing program end marker",
                            "Every EsoFur program must contain 'QwQ'")

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

            if line.startswith("Marks"):
                i += 1
                continue

            if not (line.startswith("*") and line.endswith("*")):
                if line.istitle() is False:
                    self._error(i, line, "Capitalization error",
                                "Use EsoFur keyword capitalization")

            if line.startswith("Drag"):
                parse = line.split()
                if len(parse) < 4 or parse[2] != "From":
                    self._error(i, line, "Malformed import",
                                "Use: Drag <Thing> From <Module>")
                try:
                    if parse[1] == "Everything":
                        module += "\\n" + self._grabfile(parse[3])
                        self.imported.append(parse[3])
                    else:
                        module += "\\n" + self._grabfile(parse[3], parse[1])
                        self.imported_local.append(parse[3] + "." + parse[1])
                except Exception as e:
                    self._error(i, line, str(e), "Check module name")
                i += 1
                continue

            try:
                parse_value = self._parse_value
                for mod in self.imported_local:
                    if line.startswith(mod):
                        line = line.split(".", 1)[1]
                        break
                if module:
                    exec(module, globals(), locals())
            except SystemExit:
                i += 1
                continue
            except Exception:
                pass

            if line.startswith("Notices Your"):
                self.symbol_table[line.split()[2]] = None
                i += 1
                continue

            if "Pounces On" in line:
                value, var_name = line.split("Pounces On")
                var_name = var_name.strip()
                if var_name not in self.symbol_table:
                    self._error(i, line, "Undeclared variable",
                                f"Declare {var_name} first")
                self.symbol_table[var_name] = self._assign(value.strip())
                i += 1
                continue

            if "Nuzzles" in line:
                if not line.startswith("Nuzzles"):
                    condition, label = line.split("Nuzzles")
                    if bool(self._parse_value(condition.strip())):
                        label = self._assign(label.strip())
                        if str(label).isdigit():
                            i += int(label)
                        else:
                            i = self._find_label_index(lines, label)
                    else:
                        i += 1
                else:
                    label = self._assign(line.split()[1])
                    if isinstance(label, int):
                        i += label
                    else:
                        i = self._find_label_index(lines, label)
                continue

            if line == '*Starts Roleplaying*':
                i += 1
                continue

            if line.startswith('*Stops Roleplaying Because Of') and line.endswith('*'):
                condition = line.split(' ')[-1][:-1].strip()
                if bool(self._parse_value(condition)):
                    i = self._find_loop_start_index(lines, i)
                else:
                    i += 1
                continue

            if line.startswith("Howl"):
                print(self._assign(line.split(" ", 1)[1].strip()))
                i += 1
                continue

            if line.startswith("Eyedropper A Sparkledog At"):
                self.symbol_table[line.split()[4]] = random()
                i += 1
                continue

            if line.startswith("Boop The User For"):
                text = line.split(" ", 6)
                var_name = text[4]
                prompt = ""
                if len(text) == 7:
                    prompt = str(self._assign(text[6])) + ":"
                value = input(prompt)
                self.symbol_table[var_name] = self._assign(value)
                i += 1
                continue

            if "Transforms Into" in line:
                var_name, type_name = line.split("Transforms Into")
                var_name = var_name.strip()
                self.symbol_table[var_name] = self._cast_value(
                    self._parse_value(var_name), type_name.strip())
                i += 1
                continue

            for key, op in [
                ("Inflates By", "+"),
                ("Pays", "-"),
                ("Breeds By", "*"),
                ("Baps", "/"),
                ("Deflates By", "%"),
                ("Gets Vored By", "l"),
                ("Hyper-Inflates By", "^"),
            ]:
                if key in line:
                    self._do_maths(line, key, op)
                    i += 1
                    break
            else:
                self._error(i, line, "Unknown or invalid syntax",
                            "Check EsoFur keyword spelling")

    def execute_line(self, line):
        return self.compile("OwO What's This?\\n" + line + "\\nQwQ")

    def _find_label_index(self, lines, label):
        for i, line in enumerate(lines):
            if line.startswith("Marks") and line.split()[1] == label:
                return i
        raise _noLabel(label)

    def _find_loop_start_index(self, lines, end_index):
        loop_count = 0
        for i in range(end_index - 1, -1, -1):
            if lines[i].startswith('*Stops Roleplaying Because Of'):
                loop_count += 1
            if lines[i] == '*Starts Roleplaying*':
                if loop_count == 0:
                    return i
                loop_count -= 1
        raise _noStart()

    def _assign(self, value_str):
        if value_str.isdigit():
            return int(value_str)
        if '"' in value_str:
            return value_str[value_str.find('"') + 1:value_str.rfind('"')]
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        return value_str

    def _parse_value(self, value_str):
        if value_str.isdigit():
            return int(value_str)
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        return eval(value_str, {}, self.symbol_table)

    def _cast_value(self, value, type_name):
        return {"Int": int, "Float": float, "Str": str,
                "List": list, "Furpile": set}[type_name](value)

    def _do_maths(self, line, keyword, operation):
        var_1, var_2 = map(lambda x: x.strip(), line.split(keyword))
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
                raise _divideByZero()
            num_1 /= num_2
        elif operation == "%":
            num_1 %= num_2
        elif operation == "l":
            num_1 = math.log(num_1, num_2)
        elif operation == "^":
            num_1 **= num_2

        self.symbol_table[var_1] = num_1

    def _grabfile(self, module, *word):
        with open(module + ".EsoFurMod", "r") as file:
            source_code = file.read()

        if not word:
            return source_code

        for block in source_code.split("#NEXT"):
            if block.startswith("\\n#" + word[0]):
                return block
