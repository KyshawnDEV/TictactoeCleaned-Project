# TicTacToe (C backend + PySide6 GUI)

This project implements Tic-Tac-Toe in C and exposes the game logic as a shared library for a Python PySide6 GUI. There is also a simple console app built from the same C code.

**Project Layout**
- `include/` public C headers
- `src/` C source files
- `python/` PySide6 GUI and ctypes backend wrapper

**Build the C Library and Console App**

Prereqs:
- CMake 3.30+
- A C compiler (Clang, GCC, or MSVC)

Commands:
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

Run the console app:
```sh
./build/TikTacToe
```

On Windows:
```sh
.\build\TikTacToe.exe
```

**Run the PySide6 GUI**

Create a venv and install PySide6:
```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install PySide6
```

Run the GUI:
```sh
python python/app.py
```

If the GUI cannot find the shared library, set `TICTACTOE_LIB_PATH` to the full path of the library and run again:

macOS example:
```sh
export TICTACTOE_LIB_PATH="/absolute/path/to/build/libTikTacToeLib.dylib"
python python/app.py
```

Windows example:
```bat
set TICTACTOE_LIB_PATH=C:\path\to\build\TikTacToeLib.dll
python python\app.py
```

Linux example:
```sh
export TICTACTOE_LIB_PATH="/absolute/path/to/build/libTikTacToeLib.so"
python python/app.py
```

**VS Code Run and Debug**
- Use the Run and Debug configuration named `Launch PySide6 GUI`.
- It runs a CMake build task and launches `python/app.py` with the library path pre-set.

**Notes**
- The PySide6 GUI talks to the C backend via `python/tictactoe_backend.py` using `ctypes`.
- The C API includes a `getCell(row, col)` function so the GUI can read the board state.
