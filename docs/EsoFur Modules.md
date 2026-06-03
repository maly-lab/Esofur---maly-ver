# EsoFur Commands

## Program Structure

| Command | Description | Example |
|---------|-------------|---------|
| `OwO What's This?` | Marks the start of the program | `OwO What's This?` |
| `QwQ` | Marks the end of the program | `QwQ` |
| `Muzzles {text}` | Single line comment | `Muzzles This is a comment` |
| `Maws` | Start of a multi-line comment block | `Maws` |
| `Paws` | End of a multi-line comment block | `Paws` |

## Variables

| Command | Description | Example |
|---------|-------------|---------|
| `Notices Your {name}` | Declares a variable | `Notices Your X` |
| `{value} Pounces On {name}` | Assigns a value to a variable | `5 Pounces On X` |
| `{name} Transforms Into {type}` | Casts a variable to a different type | `X Transforms Into Int` |

### Types

| Type | Description |
|------|-------------|
| `Int` | Integer |
| `Float` | Decimal number |
| `Str` | String/text |
| `List` | List |
| `Furpile` | Set |

## Maths

| Command | Operation | Example |
|---------|-----------|---------|
| `{var} Inflates By {value}` | Addition `+` | `X Inflates By 5` |
| `{var} Pays {value}` | Subtraction `-` | `X Pays 3` |
| `{var} Breeds By {value}` | Multiplication `*` | `X Breeds By 2` |
| `{var} Baps {value}` | Division `/` | `X Baps 2` |
| `{var} Deflates By {value}` | Modulo `%` | `X Deflates By 3` |
| `{var} Gets Vored By {value}` | Logarithm | `X Gets Vored By 2` |
| `{var} Hyper-Inflates By {value}` | Exponentiation `^` | `X Hyper-Inflates By 2` |

## Input & Output

| Command | Description | Example |
|---------|-------------|---------|
| `Howl {variable/value}` | Prints a value to the console | `Howl X` |
| `Boop The User For {var}` | Takes input from the user | `Boop The User For X` |
| `Boop The User For {var} With {prompt}` | Takes input with a prompt | `Boop The User For X With "Enter a number"` |

## Control Flow

| Command | Description | Example |
|---------|-------------|---------|
| `Marks {label}` | Defines a jump label | `Marks Start` |
| `Nuzzles {label}` | Unconditional jump to a label | `Nuzzles Start` |
| `{condition} Nuzzles {label}` | Conditional jump to a label | `X Nuzzles Start` |
| `*Starts Roleplaying*` | Marks the start of a loop | `*Starts Roleplaying*` |
| `*Stops Roleplaying Because Of {condition}*` | Ends loop if condition is true | `*Stops Roleplaying Because Of X*` |

## Misc

| Command | Description | Example |
|---------|-------------|---------|
| `Eyedropper A Sparkledog At {var}` | Assigns a random float to a variable | `Eyedropper A Sparkledog At X` |
| `Drag {function} From {module}` | Imports a function from a module | `Drag MyFunc From MyModule` |
| `Drag Everything From {module}` | Imports all functions from a module | `Drag Everything From MyModule` |

> All keywords must be written in Title Case or the interpreter will throw an error.
