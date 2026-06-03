# EsoFur Module Template

Modules let you extend EsoFur with custom keywords written in Python.
Since the interpreter is written in Python, all module code is Python too.

---

## Rules

- The file extension must be `.EsoFurMod`
- Every command block must be preceded by `#NEXT` on its own line, followed by a commented line with the keyword name
- Keywords must be written in Title Case to pass the interpreter's syntax check
- Use `parse_value()` to resolve a variable name or literal to its actual value
- Use `self.symbol_table` to read or write variables directly
- Each block is a plain `if` statement — no functions, no classes

---

## Available Helpers

| Helper | Description | Example |
|--------|-------------|---------|
| `parse_value(x)` | Resolves a variable name or literal to its value | `parse_value("MyVar")` → `42` |
| `self.symbol_table` | Dictionary of all declared variables | `self.symbol_table["MyVar"] = 5` |

> `parse_value` is a direct reference to `self._parse_value` injected by the interpreter at import time.

---

## File Structure

```
#NEXT
#KeywordOne
if line.startswith("Keyword One"):
    # your code here

#NEXT
#KeywordTwo
if line.startswith("Keyword Two"):
    # your code here
```

---

## Template

Copy this file, rename it to `YourModuleName.EsoFurMod`, and replace the placeholders.

```python
#NEXT
#YourKeyword
if line.startswith("Your Keyword"):
    # Read a variable or literal from the line
    # Example: "Your Keyword MyVar" → gets the value of MyVar
    value = parse_value(line.split()[2])

    # Do something with the value
    print(value)

#NEXT
#YourKeywordWith
if line.startswith("Your Keyword With"):
    # Write a value back to a variable
    # Example: "Your Keyword With MyVar" → sets MyVar to the result
    var_name = line.split()[3]
    self.symbol_table[var_name] = 42  # replace 42 with your result
```

---

## Full Example

A module called `MathExtra.EsoFurMod` that adds a square root keyword:

```python
#NEXT
#Sqrt
if line.startswith("Sqrt"):
    # "Sqrt MyVar" → prints the square root of MyVar
    import math
    value = parse_value(line.split()[1])
    print(math.sqrt(value))

#NEXT
#SqrtInto
if line.startswith("Sqrt Into"):
    # "Sqrt Into MyVar ResultVar" → stores the result in ResultVar
    import math
    value = parse_value(line.split()[2])
    result_var = line.split()[3]
    self.symbol_table[result_var] = math.sqrt(value)
```

Used in an EsoFur program like this:

```
OwO What's This?
Drag Sqrt From MathExtra
Notices Your X
16 Pounces On X
Sqrt X
QwQ
```

---

## Importing Your Module

```
Drag Everything From YourModuleName
```

or import a single keyword:

```
Drag YourKeyword From YourModuleName
```

> The module file must be in the same directory as the `.EsoFur` file being run.
