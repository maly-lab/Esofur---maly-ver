import math
import re
import sys
import random
from exceptions import (
    _divideByZero, _debug, _undefinedKeyword, _alreadyImported, _importError,
    _noEnd, _undeclaredVar, _capError, _jumpError, _noLabel, _noStart,
    _noBoop, _tooManyBoop, _castingFail, _unmatchedComment, _notImplemented
)


class EsoFurCompiler:
    def __init__(self):
        self.symbol_table = {}
        self.local_table = {}
        self.in_comment = False
        self.imported = []
        self.imported_local = []
        self.functions = {}  # stores function definitions
        self.in_function = False  # flag for when we're inside a function definition
        self.current_function = None  # name of function being defined
        self.return_value = None  # value to return from function (if any)

    # ---------------- COMPILER CORE ----------------
    def compile(self, code):
        lines = code.split("\n")
        i = 0
        built = False
        module = ""

        if sum(1 for l in lines if "Maws" in l.strip()) != sum(1 for l in lines if "Paws" in l.strip()):
        	raise _unmatchedComment()

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

            # ---------------- INSIDE FUNCTION BODY ----------------
            if self.in_function:
                if line == "Finishes Fursuit":
                    self.in_function = False
                    self.current_function = None
                else:
                    self.functions[self.current_function]["body"].append(line)
                i += 1
                continue

            # ---------------- TOSS BACK (RETURN) ----------------
            if line.startswith("Toss Back"):
                parts = line.split(" ", 2)
                if len(parts) < 3:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                self.return_value = self._assign(parts[2].strip())
                return

            # ---------------- CLEAN EXIT ----------------
            if line == "QwQ":
                return

            if "QwQ" not in [l.strip() for l in lines]:
                raise _noEnd()

            # ---------------- COMMENTS ----------------
            if line.startswith("Muzzles"):
                i += 1
                continue
            if "Maws" in line:
                self.in_comment = True
                i += 1
                continue
                
            if "Paws" in line:
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

            # ---------------- FUNCTION DEFINITION ----------------
            if line.startswith("Makes Fursuit"):
                parts = line.split()
                if len(parts) < 3:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                func_name = parts[2]
                params = []
                if "With" in parts:
                    with_index = parts.index("With")
                    param_parts = parts[with_index + 1:]
                    params = [p for p in param_parts if p != "And"]
                self.functions[func_name] = {"params": params, "body": [], "start": i + 1}
                self.in_function = True
                self.current_function = func_name
                i += 1
                continue

            # ---------------- FUNCTION CALL ----------------
            if line.startswith("Fursuit"):
                parts = line.split()
                if len(parts) < 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                func_name = parts[1]
                if func_name not in self.functions:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                func = self.functions[func_name]

                # Check for Into <variable> at the end
                return_var = None
                if "Into" in parts:
                    into_index = parts.index("Into")
                    return_var = parts[into_index + 1]
                    parts = parts[:into_index]

                # Parse arguments
                args = []
                if "With" in parts:
                    with_index = parts.index("With")
                    arg_parts = parts[with_index + 1:]
                    args = [self._assign(a) for a in arg_parts if a != "And"]

                # Check parameter count matches
                if len(args) != len(func["params"]):
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)

                # Save current state
                saved_table = self.symbol_table.copy()
                saved_local = self.local_table.copy()

                # Bind parameters to arguments in symbol table
                for param, arg in zip(func["params"], args):
                    self.symbol_table[param] = arg

                # Build function code from stored body lines
                func_code = "\n".join(func["body"])

                # Execute function body with fresh local table
                func_compiler = EsoFurCompiler()
                func_compiler.symbol_table = self.symbol_table
                func_compiler.local_table = {}
                func_compiler.functions = self.functions
                func_compiler.compile("OwO What's This?\n" + func_code + "\nQwQ")

                # Restore symbol table, keeping changes to existing global variables
                # but ignoring any new variables created inside the function
                for key in saved_table:
                    if key not in func["params"] and key != return_var:
                        saved_table[key] = func_compiler.symbol_table.get(key, saved_table[key])
                self.symbol_table = saved_table

                # Restore local table, discarding anything leashed inside the function
                self.local_table = saved_local

                # Store return value if Into was specified
                if return_var and func_compiler.return_value is not None:
                    if return_var not in self.symbol_table:
                        raise _undeclaredVar(return_var)
                    self.symbol_table[return_var] = func_compiler.return_value

                i += 1
                continue

            # ---------------- SYNTAX CHECK (ignores quoted strings) ----------------
            line_no_strings = re.sub(r'"[^"]*"', '', line)
            if line_no_strings.strip() and not line_no_strings.istitle():
                raise _capError()

            # ---------------- IMPORTS ----------------
            if line.startswith("Drag"):
                parse = line.split()
                if len(parse) < 4 or parse[2] != "From":
                    raise _capError()
                try:
                    if parse[1] == "Everything":
                        if parse[3] in self.imported:
                            raise _alreadyImported()
                        module += "\n" + self._grabfile(parse[3])
                        self.imported.append(parse[3])
                    else:
                        key = parse[3] + "." + parse[1]
                        if key in self.imported_local or parse[3] in self.imported:
                            raise _alreadyImported()
                        module += "\n" + self._grabfile(parse[3], parse[1])
                        self.imported_local.append(key)
                        self.imported.append(parse[3])
                except (_alreadyImported, _importError):
                    raise
                except Exception:
                    raise _importError(parse[3])

                try:
                    parse_value = self._parse_value
                    exec(module, globals(), locals())
                except SystemExit:
                    pass
                except Exception:
                    raise _importError(parse[3])

                i += 1
                continue

            # Run already-loaded module code
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
                    raise _capError()
                var_name = parts[2]
                # Checks if the variable is declared as local
                is_local = "And" in parts and "Leashes" in parts and "It" in parts
                value = None
                if "As" in parts:
                    as_index = parts.index("As")
                    type_name = parts[as_index + 1]
                    defaults = {
                        "Int":     0,
                        "Float":   0.0,
                        "Str":     "",
                        "List":    [],
                        "Furpile": set(),
                    }
                    if type_name not in defaults:
                        raise _castingFail()
                    value = defaults[type_name]
                if is_local:
                    self.local_table[var_name] = value
                else:
                    self.symbol_table[var_name] = value
                i += 1
                continue

            # ---------------- CLEAR VARIABLE ----------------
            if line.endswith("Gets Canceled"):
                var_name = line.split("Gets Canceled")[0].strip()
                if var_name in self.local_table:
                    self.local_table[var_name] = None
                elif var_name in self.symbol_table:
                    self.symbol_table[var_name] = None
                else:
                    raise _undeclaredVar(var_name)
                i += 1
                continue

            # ---------------- ASSIGNMENT ----------------
            if "Pounces On" in line:
                parts = line.split("Pounces On")
                if len(parts) != 2:
                    raise _capError()
                value_str = parts[0].strip()
                var_name = parts[1].strip()
                if var_name not in self.symbol_table and var_name not in self.local_table:
                    raise _undeclaredVar(var_name)
                value = self._assign(value_str)
                if var_name in self.local_table:
                    self.local_table[var_name] = value
                else:
                    self.symbol_table[var_name] = value
                i += 1
                continue

            # ---------------- JUMPS ----------------
            if "Nuzzles" in line:
                if not line.startswith("Nuzzles"):
                    condition_str, label_str = line.split("Nuzzles", 1)
                    condition = self._parse_value(condition_str.strip())
                    label = self._assign(label_str.strip())
                    if bool(condition):
                        if isinstance(label, int):
                            i += label
                        else:
                            i = self._find_label_index(lines, label)
                    else:
                        i += 1
                else:
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
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                value = self._assign(parts[1].strip())
                print(value)
                i += 1
                continue

            # ---------------- PRINT CHAR ----------------
            if line.startswith("Awoo"):
                parts = line.split()
                if len(parts) < 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                value = self._parse_value(parts[1])
                if not isinstance(value, int):
                    raise _castingFail()
                char = chr(value)
                if len(parts) == 4 and parts[2] == "At":
                    target = parts[3]
                    if target not in self.symbol_table and target not in self.local_table:
                        raise _undeclaredVar(target)
                    if target in self.local_table:
                        self.local_table[target] = char
                    else:
                        self.symbol_table[target] = char
                else:
                    print(char)
                i += 1
                continue

            # ---------------- RANDOM FLOAT ----------------
            if line.startswith("Eyedropper A Sparkledog At"):
                parts = line.split()
                if len(parts) < 5:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                self.symbol_table[parts[4]] = random.random()
                i += 1
                continue

            # ---------------- RANDOM INT ------------------
            if line.startswith("Paw A Die With") and "Sides" in line and "Into" in line:
                parts = line.split()
                if len(parts) < 8 or parts[2] != "Die" or parts[3] != "With" or parts[5] != "Sides" or parts[6] != "Into":
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                sides = self._parse_value(parts[4])
                var_name = parts[7]
                if not isinstance(sides, int) or sides <= 0:
                    raise _castingFail()
                result = random.randint(1, sides)
                if var_name in self.local_table:
                    self.local_table[var_name] = result
                else:
                    self.symbol_table[var_name] = result
                i += 1
                continue

            # ---------------- USER INPUT ----------------
            if line.startswith("Boop The User For"):
                text = line.split(" ", 6)
                if len(text) < 5:
                    raise _noBoop()
                var_name = text[4]
                prompt = ""
                if len(text) == 7:
                    if text[5] != "With":
                        raise _noBoop()
                    prompt = str(self._assign(text[6])) + ":"
                if len(text) > 7:
                    raise _tooManyBoop()
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
                    raise _castingFail()
                var_name = parts[0].strip()
                type_name = parts[1].strip()
                value = self._parse_value(var_name)
                result = self._cast_value(value, type_name)
                if var_name in self.local_table:
                    self.local_table[var_name] = result
                else:
                    self.symbol_table[var_name] = result
                i += 1
                continue

            # ---------------- CONVERT TO LIST ----------------
            if line.endswith("Suits Up"):
                var_name = line.split("Suits Up")[0].strip()
                if var_name not in self.symbol_table and var_name not in self.local_table:
                    raise _undeclaredVar(var_name)
                value = self._parse_value(var_name)
                result = list(value) if value is not None else []
                if var_name in self.local_table:
                    self.local_table[var_name] = result
                else:
                    self.symbol_table[var_name] = result
                i += 1
                continue

            # ---------------- CONVERT TO FURPILE ----------------
            if line.endswith("Starts A Furpile"):
                var_name = line.split("Starts A Furpile")[0].strip()
                if var_name not in self.symbol_table and var_name not in self.local_table:
                    raise _undeclaredVar(var_name)
                value = self._parse_value(var_name)
                result = set(value) if value is not None else set()
                if var_name in self.local_table:
                    self.local_table[var_name] = result
                else:
                    self.symbol_table[var_name] = result
                i += 1
                continue

            # ---------------- APPEND TO LIST ----------------
            if line.startswith("Sew") and "Onto" in line:
                parts = line.split("Onto")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                var_name = parts[0].replace("Sew", "").strip()
                list_name = parts[1].strip()
                value = self._parse_value(var_name)
                lst = self._parse_value(list_name)
                if not isinstance(lst, list):
                    raise _castingFail()
                lst.append(value)
                if list_name in self.local_table:
                    self.local_table[list_name] = lst
                else:
                    self.symbol_table[list_name] = lst
                i += 1
                continue

            #---------------- LIST ITEM BY INDEX ----------------
            if line.startswith("Fetch") and "At" in line and "From" in line and "Into" in line:
                list_name = line.split("Fetch")[1].split("At")[0].strip()
                index_str = line.split("At")[1].split("From")[0].strip()
                target_name = line.split("Into")[1].strip()
                index = self._parse_value(index_str)
                lst = self._parse_value(list_name)
                if not isinstance(lst, list):
                    raise _castingFail()
                if not isinstance(index, int):
                    raise _castingFail()
                if target_name not in self.symbol_table and target_name not in self.local_table:
                    raise _undeclaredVar(target_name)
                try:
                    result = lst[index]
                except IndexError:
                    raise _castingFail()
                if target_name in self.local_table:
                    self.local_table[target_name] = result
                else:
                    self.symbol_table[target_name] = result
                i += 1
                continue
            # ---------------- APPEND TO FURPILE ----------------
            if "Joins The Pile At" in line:
                parts = line.split("Joins The Pile At")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                var_name = parts[0].strip()
                pile_name = parts[1].strip()
                value = self._parse_value(var_name)
                pile = self._parse_value(pile_name)
                if not isinstance(pile, set):
                    raise _castingFail()
                pile.add(value)
                self.symbol_table[pile_name] = pile
                i += 1
                continue

            # ---------------- STRING CONCATENATION ----------------
            if line.startswith("Look!") and "Joined The" in line:
                rest = line[len("Look!"):].strip()
                parts = rest.split("Joined The")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                src_name = parts[0].strip()
                tgt_name = parts[1].strip()
                src_value = str(self._parse_value(src_name))
                tgt_value = str(self._parse_value(tgt_name))
                result = tgt_value + src_value
                if tgt_name in self.local_table:
                    self.local_table[tgt_name] = result
                else:
                    self.symbol_table[tgt_name] = result
                i += 1
                continue

            # ---------------- POP FROM LIST ----------------
            if "'S Raffle Winner Is" in line:
                parts = line.split("'S Raffle Winner Is")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                list_name = parts[0].strip()
                var_name = parts[1].strip()
                lst = self._parse_value(list_name)
                if not isinstance(lst, list):
                    raise _castingFail()
                if var_name not in self.symbol_table and var_name not in self.local_table:
                    raise _undeclaredVar(var_name)
                popped = lst.pop()
                self.symbol_table[list_name] = lst
                if var_name in self.local_table:
                    self.local_table[var_name] = popped
                else:
                    self.symbol_table[var_name] = popped
                i += 1
                continue

            # ---------------- CHECK MEMBERSHIP ----------------
            if line.startswith("Is") and "In" in line and line.endswith("?"):
                inner = line[len("Is"):].rstrip("?").strip()
                parts = inner.split("In")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                var_name = parts[0].strip()
                pile_name = parts[1].strip()
                value = self._parse_value(var_name)
                pile = self._parse_value(pile_name)
                if not isinstance(pile, set):
                    raise _castingFail()
                self.symbol_table["_result"] = 1 if value in pile else 0
                i += 1
                continue

            # ---------------- REMOVE FROM LIST/FURPILE ----------------
            if line.startswith("Escort") and "To" in line and "From" in line:
                rest = line[len("Escort"):].strip()
                to_split = rest.split("To")
                if len(to_split) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                key_name = to_split[0].strip()
                from_split = to_split[1].split("From")
                if len(from_split) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                var_name = from_split[0].strip()
                collection_name = from_split[1].strip()
                key = self._parse_value(key_name)
                collection = self._parse_value(collection_name)
                if var_name not in self.symbol_table and var_name not in self.local_table:
                    raise _undeclaredVar(var_name)
                if isinstance(collection, list):
                    if not isinstance(key, int):
                        raise _castingFail()
                    removed = collection.pop(key)
                elif isinstance(collection, set):
                    removed = key
                    collection.discard(key)
                else:
                    raise _castingFail()
                self.symbol_table[collection_name] = collection
                if var_name in self.local_table:
                    self.local_table[var_name] = removed
                else:
                    self.symbol_table[var_name] = removed
                i += 1
                continue

            # ---------------- MEASURE LENGTH ----------------
            if "'S Tail Length To" in line:
                parts = line.split("'S Tail Length To")
                if len(parts) != 2:
                    raise _undefinedKeyword(self.imported, line, self.symbol_table)
                src_name = parts[0].replace("Measure", "").strip()
                tgt_name = parts[1].strip()
                value = self._parse_value(src_name)
                if tgt_name not in self.symbol_table and tgt_name not in self.local_table:
                    raise _undeclaredVar(tgt_name)
                try:
                    length = len(value)
                except TypeError:
                    raise _castingFail()
                if tgt_name in self.local_table:
                    self.local_table[tgt_name] = length
                else:
                    self.symbol_table[tgt_name] = length
                i += 1
                continue

            # ---------------- MATHS ----------------
            if "Inflates By" in line:
                self._do_maths(line, "Inflates By", "+")
                i += 1
                continue

            if "Pays" in line:
                self._do_maths(line, "Pays", "-")
                i += 1
                continue

            if "Breeds By" in line:
                self._do_maths(line, "Breeds By", "*")
                i += 1
                continue

            if "Baps" in line:
                self._do_maths(line, "Baps", "/")
                i += 1
                continue

            if "Deflates By" in line:
                self._do_maths(line, "Deflates By", "%")
                i += 1
                continue

            if "Gets Vored By" in line:
                self._do_maths(line, "Gets Vored By", "l")
                i += 1
                continue

            if "Hyper-Inflates By" in line:
                self._do_maths(line, "Hyper-Inflates By", "^")
                i += 1
                continue

            # ---------------- UNKNOWN SYNTAX ----------------
            raise _undefinedKeyword(self.imported, line, self.symbol_table)

    # ---------------- REPL EXECUTION ----------------
    def execute_line(self, line):
        line = line.strip()

        if not line:
            return None

        # Create a one line comment
        if line.startswith("Muzzles"):
            return None
        
        # Start multi-line comment
        if line == "Maws":
            self.in_comment = True
            return None

        # End multi-line comment
        if line == "Paws":
            self.in_comment = False
            return None

        if self.in_comment:
            return None

        # Initialises a variable
        if line.startswith("Notices Your"):
            parts = line.split()
            if len(parts) < 3:
                raise _capError()
            var_name = parts[2]
            is_local = line.rstrip().endswith("And Leashes It")
            value = None
            if "As" in parts:
                as_index = parts.index("As")
                type_name = parts[as_index + 1]
                defaults = {
                    "Int":     0,
                    "Float":   0.0,
                    "Str":     "",
                    "List":    [],
                    "Furpile": set(),
                }
                if type_name not in defaults:
                    raise _castingFail()
                value = defaults[type_name]
            if is_local:
                self.local_table[var_name] = value
            else:
                self.symbol_table[var_name] = value
            return None

        # Clears a variable
        if line.endswith("Gets Canceled"):
            var_name = line.split("Gets Canceled")[0].strip()
            if var_name in self.symbol_table:
                self.symbol_table[var_name] = None
            else:
                raise _undeclaredVar(var_name)
            return None

        # Assigns a variable with a value
        if "Pounces On" in line:
            parts = line.split("Pounces On")
            if len(parts) != 2:
                raise _capError()
            value_str = parts[0].strip()
            var_name = parts[1].strip()
            if var_name not in self.symbol_table:
                raise _undeclaredVar(var_name)
            self.symbol_table[var_name] = self._assign(value_str)
            return None

        # Output
        if line.startswith("Howl"):
            parts = line.split(" ", 1)
            if len(parts) < 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            return self._assign(parts[1].strip())

        # Output char
        if line.startswith("Awoo"):
            parts = line.split()
            if len(parts) < 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            value = self._parse_value(parts[1])
            if not isinstance(value, int):
                raise _castingFail()
            char = chr(value)
            if len(parts) == 4 and parts[2] == "At":
                target = parts[3]
                if target not in self.symbol_table:
                    raise _undeclaredVar(target)
                self.symbol_table[target] = char
                return None
            return char

        # Random float generation
        if line.startswith("Eyedropper A Sparkledog At"):
            parts = line.split()
            if len(parts) < 5:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            self.symbol_table[parts[4]] = random.random()
            return None

        # Prompts user for input
        if line.startswith("Boop The User For"):
            text = line.split(" ", 6)
            if len(text) < 5:
                raise _noBoop()
            var_name = text[4]
            prompt = ""
            if len(text) == 7:
                # Checks for a varible to add the input into
                if text[5] != "With":
                    raise _noBoop()
                prompt = str(self._assign(text[6])) + ":"
            try:
                value = input(prompt)
            except ValueError:
                sys.stdin = open(0, "r")
                value = input(prompt)
            self.symbol_table[var_name] = self._assign(value)
            return None

        # Type casting
        if "Transforms Into" in line:
            parts = line.split("Transforms Into")
            if len(parts) != 2:
                raise _castingFail()
            var_name = parts[0].strip()
            type_name = parts[1].strip()
            value = self._parse_value(var_name)
            self.symbol_table[var_name] = self._cast_value(value, type_name)
            return None

        # Convert to list
        if line.endswith("Suits Up"):
            var_name = line.split("Suits Up")[0].strip()
            if var_name not in self.symbol_table:
                raise _undeclaredVar(var_name)
            value = self._parse_value(var_name)
            self.symbol_table[var_name] = list(value) if value is not None else []
            return None

        # Convert to furpile
        if line.endswith("Starts A Furpile"):
            var_name = line.split("Starts A Furpile")[0].strip()
            if var_name not in self.symbol_table:
                raise _undeclaredVar(var_name)
            value = self._parse_value(var_name)
            self.symbol_table[var_name] = set(value) if value is not None else set()
            return None

        # Append to list
        if line.startswith("Sew") and "Onto" in line:
            parts = line.split("Onto")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            var_name = parts[0].replace("Sew", "").strip()
            list_name = parts[1].strip()
            value = self._parse_value(var_name)
            lst = self._parse_value(list_name)
            if not isinstance(lst, list):
                raise _castingFail()
            lst.append(value)
            self.symbol_table[list_name] = lst
            return None

        # Append to furpile
        if "Joins The Pile At" in line:
            parts = line.split("Joins The Pile At")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            var_name = parts[0].strip()
            pile_name = parts[1].strip()
            value = self._parse_value(var_name)
            pile = self._parse_value(pile_name)
            if not isinstance(pile, set):
                raise _castingFail()
            pile.add(value)
            self.symbol_table[pile_name] = pile
            return None

        # String concatenation
        if line.startswith("Look!") and "Joined The" in line:
            rest = line[len("Look!"):].strip()
            parts = rest.split("Joined The")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            src_name = parts[0].strip()
            tgt_name = parts[1].strip()
            src_value = str(self._parse_value(src_name))
            tgt_value = str(self._parse_value(tgt_name))
            self.symbol_table[tgt_name] = tgt_value + src_value
            return None

        # Removes item from list
        if "'S Raffle Winner Is" in line:
            parts = line.split("'S Raffle Winner Is")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            list_name = parts[0].strip()
            var_name = parts[1].strip()
            lst = self._parse_value(list_name)
            if not isinstance(lst, list):
                raise _castingFail()
            popped = lst.pop()
            self.symbol_table[list_name] = lst
            self.symbol_table[var_name] = popped
            return None

        # Check membership in furpile
        if line.startswith("Is") and "In" in line and line.endswith("?"):
            inner = line[len("Is"):].rstrip("?").strip()
            parts = inner.split("In")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            var_name = parts[0].strip()
            pile_name = parts[1].strip()
            value = self._parse_value(var_name)
            pile = self._parse_value(pile_name)
            if not isinstance(pile, set):
                raise _castingFail()
            self.symbol_table["_result"] = 1 if value in pile else 0
            return None

        # Remove from list/furpile
        if line.startswith("Escort") and "To" in line and "From" in line:
            rest = line[len("Escort"):].strip()
            to_split = rest.split("To")
            if len(to_split) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            key_name = to_split[0].strip()
            from_split = to_split[1].split("From")
            if len(from_split) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            var_name = from_split[0].strip()
            collection_name = from_split[1].strip()
            key = self._parse_value(key_name)
            collection = self._parse_value(collection_name)
            if isinstance(collection, list):
                removed = collection.pop(key)
            elif isinstance(collection, set):
                removed = key
                collection.discard(key)
            else:
                raise _castingFail()
            self.symbol_table[collection_name] = collection
            self.symbol_table[var_name] = removed
            return None

        # Measure length of string/list
        if "'S Tail Length To" in line:
            parts = line.split("'S Tail Length To")
            if len(parts) != 2:
                raise _undefinedKeyword(self.imported, line, self.symbol_table)
            src_name = parts[0].replace("Measure", "").strip()
            tgt_name = parts[1].strip()
            value = self._parse_value(src_name)
            try:
                length = len(value)
            except TypeError:
                raise _castingFail()
            self.symbol_table[tgt_name] = length
            return None

        # ---------------- MATHS OPERATIONS ----------------
        # Adds second value to first value and stores in first value
        if "Inflates By" in line:
            self._do_maths(line, "Inflates By", "+")
            return None

        # Subtracts second value from first value and stores in first value
        if "Pays" in line:
            self._do_maths(line, "Pays", "-")
            return None

        # Multiplies first value by second value and stores in first value
        if "Breeds By" in line:
            self._do_maths(line, "Breeds By", "*")
            return None

        # Divides first value by second value and stores in first value
        if "Baps" in line:
            self._do_maths(line, "Baps", "/")
            return None

        # Takes modulus of first value by second value and stores in first value
        if "Deflates By" in line:
            self._do_maths(line, "Deflates By", "%")
            return None

        # Takes logarithm of first value with base of second value and stores in first value
        if "Gets Vored By" in line:
            self._do_maths(line, "Gets Vored By", "l")
            return None

        # Raises first value to the power of second value and stores in first value
        if "Hyper-Inflates By" in line:
            self._do_maths(line, "Hyper-Inflates By", "^")
            return None

        raise _undefinedKeyword(self.imported, line, self.symbol_table)

    # ================================================
    # ---------------- HELPER METHODS ----------------
    # ================================================

    # Finds the index of a label in the source code
    def _find_label_index(self, lines, label):
        for idx, l in enumerate(lines):
            if l.strip().startswith("Marks") and l.strip().split(" ")[1] == label:
                return idx
        raise _noLabel(label)

    # Finds the index of the start of a loop given the index of the end of the loop
    def _find_loop_start_index(self, lines, end_index):
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
        raise _noStart()

    # Parses a value string for assignment, handling literals, variables, and indexed access
    def _assign(self, value_str):
        value_str = str(value_str)
        if " At " in value_str:
            parts = value_str.split(" At ")
            collection = self._parse_value(parts[0].strip())
            index = self._parse_value(parts[1].strip())
            if not isinstance(collection, (list, str)):
                raise _castingFail()
            try:
                return collection[index]
            except IndexError:
                raise _castingFail()
        if value_str.lstrip('-').isdigit():
            return int(value_str)
        try:
            return float(value_str)
        except ValueError:
            pass
        if '"' in value_str:
            return value_str[value_str.find('"') + 1:value_str.rfind('"')]
        if value_str in self.local_table:
            return self.local_table[value_str]
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        return value_str

    # Parses a value string for evaluation in expressions, handling literals, variables, indexed access, and eval
    def _parse_value(self, value_str):
        value_str = str(value_str)
        if " At " in value_str:
            parts = value_str.split(" At ")
            collection = self._parse_value(parts[0].strip())
            index = self._parse_value(parts[1].strip())
            if not isinstance(collection, (list, str)):
                raise _castingFail()
            try:
                return collection[index]
            except IndexError:
                raise _castingFail()
        if value_str.isdigit():
            return int(value_str)
        if value_str in self.local_table:
            return self.local_table[value_str]
        if value_str in self.symbol_table:
            return self.symbol_table[value_str]
        try:
            combined = {**self.symbol_table, **self.local_table}
            return eval(value_str, {}, combined)
        except Exception:
            raise _jumpError(value_str, self.symbol_table)

    # Casts a value to a specified type
    def _cast_value(self, value, type_name):
        type_map = {
            "Int":     int,
            "Float":   float,
            "Str":     str,
            "List":    list,
            "Furpile": set,
        }
        if type_name not in type_map:
            raise _castingFail()
        try:
            return type_map[type_name](value)
        except (ValueError, TypeError):
            raise _castingFail()

    # Performs a math operation on two values and stores the result in the first value
    def _do_maths(self, line, keyword, operation):
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
                raise _divideByZero()
            num_1 = num_1 / num_2
        elif operation == "%":
            num_1 %= num_2
        elif operation == "l":
            num_1 = math.log(num_1, num_2)
        elif operation == "^":
            num_1 **= num_2

        if var_1 in self.local_table:
            self.local_table[var_1] = num_1
        else:
            self.symbol_table[var_1] = num_1

    # Grabs the source code of a module, or a specific block within that module if a block name is provided
    def _grabfile(self, module, *word):
        with open(module + ".EsoFurMod", "r") as f:
            source_code = f.read()
        if not word:
            return source_code
        blocks = source_code.split("#NEXT")
        for block in blocks:
            if block.startswith("\n#" + word[0]):
                return block
        raise _importError(module)
