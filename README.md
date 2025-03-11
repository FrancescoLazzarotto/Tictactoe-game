# Tictactoe-game
This project is a Python implementation of an advanced version of Tic-Tac-Toe called "Filetto." The game is played on an NxN grid, and players earn points based on the length of contiguous sequences of their symbols. The game allows multiple players, including AI opponents with different difficulty levels:

Easy: Random moves.
Medium: Moves that maximize immediate points.
Hard: Moves that consider both maximizing own points and minimizing opponent advantages.
The game includes:

A scoring system where sequences of length 3, 4, and 5+ provide increasing points.
A turn-based mechanism with an automatic switch between players.
A function to evaluate all rows, columns, diagonals, and anti-diagonals to calculate scores.
A victory condition based on reaching a predefined score threshold.
Players can interact with the game via a command-line interface (CLI) or a graphical user interface (GUI) (if Tkinter is available). The GUI allows easy interaction, while the CLI prompts users for moves.

The AI opponents analyze the game board and make strategic decisions based on difficulty level. The hardest level aims to optimize moves while also blocking opponents’ winning strategies.

This project is a blend of game mechanics, AI decision-making, and user interaction, making it a great study case for game logic and AI strategy implementation.
