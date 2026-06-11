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
| `Notices Your {name} As {type}` | Declares a variable with a default value for the given type | `Notices Your X As Int` |
| `Notices Your {name} And Leashes It` | Declares a local variable scoped to the current function | `Notices Your X And Leashes It` |
| `{value} Pounces On {name}` | Assigns a value to a variable | `5 Pounces On X` |
| `{name} Transforms Into {type}` | Casts a variable to a different type | `X Transforms Into Int` |
| `{name} Gets Canceled` | Clears a variable, setting it to `None` | `X Gets Canceled` |

### Types

| Type | Description | Default Value |
|------|-------------|---------------|
| `Int` | Integer | `0` |
| `Float` | Decimal number | `0.0` |
| `Str` | String/text | `""` |
| `List` | List | `[]` |
| `Furpile` | Set | `set()` |

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
| `Awoo {value}` | Prints a character from its ASCII code | `Awoo 65` |
| `Awoo {value} At {var}` | Stores a character from its ASCII code into a variable | `Awoo 65 At X` |
| `Boop The User For {var}` | Takes input from the user | `Boop The User For X` |
| `Boop The User For {var} With {prompt}` | Takes input from the user with a prompt | `Boop The User For X With "Enter a number"` |

## Control Flow

| Command | Description | Example |
|---------|-------------|---------|
| `Marks {label}` | Defines a jump label | `Marks Start` |
| `Nuzzles {label}` | Unconditional jump to a label | `Nuzzles Start` |
| `{condition} Nuzzles {label}` | Jumps to a label if condition is truthy | `X Nuzzles Start` |
| `*Starts Roleplaying*` | Marks the start of a loop | `*Starts Roleplaying*` |
| `*Stops Roleplaying Because Of {condition}*` | Keeps looping while condition is truthy; exits the loop when it becomes falsy | `*Stops Roleplaying Because Of X*` |

## Functions

| Command | Description | Example |
|---------|-------------|---------|
| `Makes Fursuit {name}` | Defines a function | `Makes Fursuit Greet` |
| `Makes Fursuit {name} With {params}` | Defines a function with parameters, separated by `And` | `Makes Fursuit Add With A And B` |
| `Finishes Fursuit` | Marks the end of a function definition | `Finishes Fursuit` |
| `Fursuit {name}` | Calls a function | `Fursuit Greet` |
| `Fursuit {name} With {args}` | Calls a function with arguments, separated by `And` | `Fursuit Add With 3 And 5` |
| `Fursuit {name} Into {var}` | Calls a function and stores its return value | `Fursuit Greet Into Result` |
| `Fursuit {name} With {args} Into {var}` | Calls a function with arguments and stores its return value | `Fursuit Add With 3 And 5 Into Result` |
| `Toss Back {value}` | Returns a value from the current function | `Toss Back X` |

## Lists

| Command | Description | Example |
|---------|-------------|---------|
| `Sew {value} Onto {list}` | Appends a value to a list | `Sew X Onto Items` |
| `Fetch {list} At {index} From {list} Into {var}` | Retrieves the item at the given index and stores it in a variable | `Fetch Items At 0 From Items Into X` |
| `{list}'S Raffle Winner Is {var}` | Pops the last item from a list into a variable | `Items'S Raffle Winner Is X` |
| `{var} Suits Up` | Converts a variable to a list | `X Suits Up` |

## Furpiles

| Command | Description | Example |
|---------|-------------|---------|
| `{value} Joins The Pile At {furpile}` | Adds a value to a furpile | `X Joins The Pile At Pile` |
| `Is {value} In {furpile}?` | Checks if a value is in a furpile; stores `1` in `_result` if found, `0` if not | `Is X In Pile?` |
| `{var} Starts A Furpile` | Converts a variable to a furpile | `X Starts A Furpile` |

## Collections

These commands work on both lists and furpiles.

| Command | Description | Example |
|---------|-------------|---------|
| `Escort {key} To {var} From {collection}` | Removes an item from a list by index, or from a furpile by value, and stores it in a variable | `Escort 0 To X From Items` |
| `Measure {var}'S Tail Length To {target}` | Stores the length of a string, list, or furpile in a variable | `Measure Items'S Tail Length To Len` |

## Strings

| Command | Description | Example |
|---------|-------------|---------|
| `Look! {src} Joined The {target}` | Appends the value of `{src}` to the string in `{target}` | `Look! Name Joined The Msg` |

## Misc

| Command | Description | Example |
|---------|-------------|---------|
| `Eyedropper A Sparkledog At {var}` | Assigns a random float between 0 and 1 to a variable | `Eyedropper A Sparkledog At X` |
| `Paw A Die With {n} Sides Into {var}` | Assigns a random integer between 1 and n to a variable | `Paw A Die With 6 Sides Into X` |
| `Drag {function} From {module}` | Imports a specific function from a module | `Drag MyFunc From MyModule` |
| `Drag Everything From {module}` | Imports all functions from a module | `Drag Everything From MyModule` |

> All keywords must be written in Title Case or the interpreter will throw an error.
