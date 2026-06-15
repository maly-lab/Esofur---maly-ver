# EsoFur Interpreter — Modified

A fork of the [EsoFur Interpreter](https://github.com/TaserTheFox/EsoFur-Interpreter) by TaserTheFox, with AI-assisted modifications.

The original language was missing some features I wanted to use, so I had an AI implement them rather than diving into the code myself.

---

## Changes Made

- Enabled terminal usage (Linux & Windows)
- Enabled VS Code integration

---

## Installation

### Linux

1. Download or clone the repo
2. Run the following in your terminal:

```bash
cd EsoFur---maly-ver
chmod +x install.sh
./install.sh
```

> If `cd EsoFur---maly-ver` doesn't work, use the full path to the folder.

### Windows

1. Download or clone the repo
2. Open Command Prompt in the project folder and run:

```bat
install.bat
```

---

## Running `.EsoFur` Files

```bash
esofur {file path}
```

or

```bash
esofur run {file path}
```

> Make sure to use the full or relative file path, and that the file has the `.EsoFur` extension.

A test file `test.EsoFur` is included in the repo to verify your setup.

---

## Interactive Console

Running `esofur` with no arguments opens an interactive console in your terminal:

```bash
esofur
```

> ⚠️ Pasting multi-line code may affect how the console looks, but pressing Enter should still execute it. Code entered this way cannot be saved.

---

## VS Code Integration

To run `.EsoFur` files directly from VS Code:

1. In `docs`
2. Open either
- `windows vs code` (if on windows)
- `linux vs code` (if on linux)
3. copy the `.vscode` folder and paste it into your project folder

- Enables running your file with `Ctrl+Shift+B`
- Enables running your file with `F5`

---

## Commands

A full list of EsoFur commands can be found in `docs/EsoFur_Modules.md`.
