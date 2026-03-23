#ifndef BOARD_H
#define BOARD_H

#include "tictactoe_api.h"

#define BOARD_SIZE 3

// Game board
TTT_API extern int board[BOARD_SIZE][BOARD_SIZE];

// Places a piece on the board
// player should be 1 (X) or 2 (O)
TTT_API void placePiece(int row, int col, int player);

// Returns:
// 0 = game still in progress
// 1 = player 1 wins
// 2 = player 2 wins
// 3 = draw
TTT_API int checkBoardState();

// Prints the current board to the console
TTT_API void printBoard();

// Returns the value stored at a given cell:
// 0 = empty, 1 = Player 1 (X), 2 = Player 2 (O), -1 = invalid location
TTT_API int getCell(int row, int col);

// Resets the board to empty
TTT_API void resetBoard();

#endif // BOARD_H
