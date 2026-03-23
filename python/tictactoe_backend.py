from __future__ import annotations

import ctypes
import os
import sys
from ctypes import c_int
from pathlib import Path

AI_DIFFICULTY_EASY = 0
AI_DIFFICULTY_HARD = 1


def _candidate_lib_names() -> list[str]:
    # Map platform to the expected shared library name.
    if sys.platform.startswith("win"):
        return ["TikTacToeLib.dll"]
    if sys.platform == "darwin":
        return ["libTikTacToeLib.dylib"]
    return ["libTikTacToeLib.so"]


def _find_library_path() -> Path:
    # Allow explicit override via environment variable.
    env_path = os.getenv("TICTACTOE_LIB_PATH")
    if env_path:
        path = Path(env_path).expanduser().resolve()
        if path.exists():
            return path
        raise FileNotFoundError(f"TICTACTOE_LIB_PATH was set but not found: {path}")

    root = Path(__file__).resolve().parents[1]
    names = _candidate_lib_names()

    # Common build output directories across platforms/IDEs.
    search_roots = [
        root / "build",
        root / "cmake-build-debug",
        root / "cmake-build-release",
        root / "out" / "build",
        root / "out" / "build" / "x64-Debug",
        root / "out" / "build" / "x64-Release",
    ]

    for base in search_roots:
        if not base.exists():
            continue
        for name in names:
            hit = next(base.rglob(name), None)
            if hit:
                return hit

    # Last resort: scan the project root lightly.
    for name in names:
        hit = next(root.rglob(name), None)
        if hit:
            return hit

    expected = ", ".join(names)
    raise FileNotFoundError(
        "Could not find the shared library. Build it with CMake and set "
        "TICTACTOE_LIB_PATH to the absolute path if needed. Expected: "
        f"{expected}"
    )


class TicTacToeBackend:
    def __init__(self, lib_path: str | None = None) -> None:
        # Resolve the shared library path before loading.
        if lib_path:
            path = Path(lib_path).expanduser().resolve()
        else:
            path = _find_library_path()

        self._lib = ctypes.CDLL(str(path))
        self._configure_signatures()

    def _configure_signatures(self) -> None:
        # Declare C function signatures for safe ctypes calls.
        self._lib.resetBoard.restype = None

        self._lib.placePiece.argtypes = [c_int, c_int, c_int]
        self._lib.placePiece.restype = None

        self._lib.getCell.argtypes = [c_int, c_int]
        self._lib.getCell.restype = c_int

        self._lib.checkBoardState.restype = c_int

        self._lib.aiMove.argtypes = [c_int, c_int]
        self._lib.aiMove.restype = None

    def reset_board(self) -> None:
        # Clear the board state on the C side.
        self._lib.resetBoard()

    def place_piece(self, row: int, col: int, player: int) -> None:
        # Place a piece (1 = X, 2 = O).
        self._lib.placePiece(row, col, player)

    def get_cell(self, row: int, col: int) -> int:
        # Read a single cell value from the C board.
        return int(self._lib.getCell(row, col))

    def check_state(self) -> int:
        # 0 = in progress, 1/2 = winner, 3 = draw.
        return int(self._lib.checkBoardState())

    def ai_move(self, player: int, difficulty: int) -> None:
        # Ask the C AI to make a move for the given player.
        self._lib.aiMove(player, difficulty)

    def board_snapshot(self) -> list[list[int]]:
        # Convenience helper for reading the entire board into Python.
        return [[self.get_cell(r, c) for c in range(3)] for r in range(3)]
