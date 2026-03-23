from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tictactoe_backend import (
    AI_DIFFICULTY_EASY,
    AI_DIFFICULTY_HARD,
    TicTacToeBackend,
)

BOARD_SIZE = 3


class TicTacToeWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe")

        # Backend wraps the C shared library.
        self.backend = TicTacToeBackend()
        self.current_player = 1
        self.ai_player = 2
        self.game_over = False

        # Status line at the top of the window.
        self.status = QLabel("Player X's turn")
        self.status.setAlignment(Qt.AlignCenter)

        # UI controls for AI settings.
        self.vs_ai = QCheckBox("Play vs AI")
        self.vs_ai.setChecked(True)

        self.difficulty = QComboBox()
        self.difficulty.addItem("Easy", AI_DIFFICULTY_EASY)
        self.difficulty.addItem("Hard", AI_DIFFICULTY_HARD)

        self.new_game_button = QPushButton("New Game")
        self.new_game_button.clicked.connect(self.start_new_game)

        # Control row.
        controls = QHBoxLayout()
        controls.addWidget(self.vs_ai)
        controls.addWidget(QLabel("Difficulty:"))
        controls.addWidget(self.difficulty)
        controls.addStretch(1)
        controls.addWidget(self.new_game_button)

        self.grid = QGridLayout()
        self.buttons = [[QPushButton(" ") for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.buttons[r][c]
                btn.setFixedSize(90, 90)
                btn.setStyleSheet("font-size: 28px;")
                # Capture row/col so each button calls with its own coordinates.
                btn.clicked.connect(lambda checked, rr=r, cc=c: self.handle_move(rr, cc))
                self.grid.addWidget(btn, r, c)

        # Overall layout.
        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addLayout(controls)
        layout.addLayout(self.grid)
        self.setLayout(layout)

        self.start_new_game()

    def start_new_game(self) -> None:
        # Reset C-side state and refresh UI.
        self.backend.reset_board()
        self.current_player = 1
        self.game_over = False
        self.update_board()
        self.update_status()

    def handle_move(self, row: int, col: int) -> None:
        # Ignore input once the game is over.
        if self.game_over:
            return

        # Ignore clicks on occupied cells.
        if self.backend.get_cell(row, col) != 0:
            return

        # Human move.
        self.backend.place_piece(row, col, self.current_player)
        self.update_board()

        # Check for win/draw after the move.
        if self.finish_if_over():
            return

        self.switch_player()
        self.update_status()

        # If AI is enabled, let it respond.
        if self.vs_ai.isChecked() and self.current_player == self.ai_player:
            self.backend.ai_move(self.ai_player, self.current_difficulty())
            self.update_board()

            if self.finish_if_over():
                return

            self.switch_player()
            self.update_status()

    def finish_if_over(self) -> bool:
        # Check the board state in the C backend and update UI.
        state = self.backend.check_state()
        if state == 0:
            return False

        self.game_over = True
        if state == 3:
            self.status.setText("Draw!")
        elif self.vs_ai.isChecked() and state == self.ai_player:
            self.status.setText("Computer wins!")
        else:
            winner = "X" if state == 1 else "O"
            self.status.setText(f"Player {winner} wins!")
        return True

    def current_difficulty(self) -> int:
        # Pull the numeric difficulty enum from the combo box.
        return int(self.difficulty.currentData())

    def switch_player(self) -> None:
        # Alternate between player 1 (X) and player 2 (O).
        self.current_player = 2 if self.current_player == 1 else 1

    def update_status(self) -> None:
        # Only update the status when a game is active.
        if self.game_over:
            return
        player = "X" if self.current_player == 1 else "O"
        self.status.setText(f"Player {player}'s turn")

    def update_board(self) -> None:
        # Refresh the button labels from the C board.
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                value = self.backend.get_cell(r, c)
                text = " "
                if value == 1:
                    text = "X"
                elif value == 2:
                    text = "O"
                self.buttons[r][c].setText(text)


if __name__ == "__main__":
    app = QApplication([])
    window = TicTacToeWindow()
    window.show()
    app.exec()
