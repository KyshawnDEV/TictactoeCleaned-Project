#include "gameBoard.h"
#include <stdio.h>

/*
    3x3 Tic-Tac-Toe board

    Value meanings:
    0 = empty cell
    1 = Player 1 (X)
    2 = Player 2 (O)
*/
TTT_API int board[BOARD_SIZE][BOARD_SIZE] = {
    {0,0,0},
    {0,0,0},
    {0,0,0}
};

/*
    placePiece() - Attempts to place a player's piece at the given row and column.

    Parameters:
        row    -> board row (0-2)
        col    -> board column (0-2)
        player -> player number (1 = X, 2 = O)

    The function validates:
        - The position is within the board boundaries
        - The player value is valid
        - The selected cell is currently empty

    If any condition fails the function returns without modifying the board.
*/
void placePiece(int row, int col, int player) {

    // Check if row/column are outside the board
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
        return;
    }

    // Validate player number
    if (player != 1 && player != 2) {
        return;
    }

    // Prevent overwriting an existing piece
    if (board[row][col] != 0) {
        return;
    }

    // Place the player's piece on the board
    board[row][col] = player;
}

/*
    checkBoardState()

    Determines the current state of the game.

    Return values:
        0 = Game still in progress
        1 = Player 1 (X) wins
        2 = Player 2 (O) wins
        3 = Draw (board full, no winner)

    The function checks:
        1. All rows
        2. All columns
        3. Both diagonals
        4. Whether the board is full
*/
int checkBoardState() {

    int i;

    // Check all rows for a win
    for (i = 0; i < BOARD_SIZE; i++) {
        if (board[i][0] != 0 &&
            board[i][0] == board[i][1] &&
            board[i][1] == board[i][2]) {

            return board[i][0]; // return the winning player
        }
    }

    // Check all columns for a win
    for (i = 0; i < BOARD_SIZE; i++) {
        if (board[0][i] != 0 &&
            board[0][i] == board[1][i] &&
            board[1][i] == board[2][i]) {

            return board[0][i]; // return the winning player
        }
    }

    // Check top-left -> bottom-right diagonal
    if (board[0][0] != 0 &&
        board[0][0] == board[1][1] &&
        board[1][1] == board[2][2]) {

        return board[0][0];
    }

    // Check top-right -> bottom-left diagonal
    if (board[0][2] != 0 &&
        board[0][2] == board[1][1] &&
        board[1][1] == board[2][0]) {

        return board[0][2];
    }

    // Check if any empty spaces remain on the board
    for (i = 0; i < BOARD_SIZE; i++) {

        int j;

        for (j = 0; j < BOARD_SIZE; j++) {

            // If an empty cell exists, the game is still in progress
            if (board[i][j] == 0) {
                return 0;
            }
        }
    }

    // If no empty cells and no winner, it's a draw
    return 3;
}

/*
    printBoard()

    Displays the current board in a human-readable
    Tic-Tac-Toe grid format.

    Example output:

     X | O | X
    ---+---+---
       | X |
    ---+---+---
     O |   | O
*/
void printBoard() {

    int row;
    int col;

    for (row = 0; row < BOARD_SIZE; row++) {

        for (col = 0; col < BOARD_SIZE; col++) {

            // Default symbol for empty cells
            char symbol = ' ';

            // Convert stored values into display characters
            if (board[row][col] == 1) {
                symbol = 'X';
            }
            else if (board[row][col] == 2) {
                symbol = 'O';
            }

            printf(" %c ", symbol);

            // Print vertical divider between columns
            if (col < BOARD_SIZE - 1) {
                printf("|");
            }
        }

        printf("\n");

        // Print horizontal divider between rows
        if (row < BOARD_SIZE - 1) {
            printf("---+---+---\n");
        }
    }
}

/*
    getCell()

    Returns the raw value stored at a given cell.
    -1 is returned for out-of-bounds requests.
*/
int getCell(int row, int col) {
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
        return -1;
    }
    return board[row][col];
}

/*
    resetBoard()

    Clears the board by setting every cell back to 0.
    This is useful when starting a new game.
*/
void resetBoard() {

    int row;
    int col;

    for (row = 0; row < BOARD_SIZE; row++) {
        for (col = 0; col < BOARD_SIZE; col++) {

            board[row][col] = 0;

        }
    }
}
