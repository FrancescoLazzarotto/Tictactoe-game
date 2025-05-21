# TicTacToe-Game (Filetto)

## Overview

This project is a Python implementation of an advanced version of Tic-Tac-Toe, called **Filetto**.  
Unlike the classic 3x3 game, Filetto is played on an **NxN grid**, where players earn points based on the length of contiguous sequences of their symbols.

The game supports multiple players, including AI-controlled opponents with adjustable difficulty levels.

---

## Game Features

### AI Difficulty Levels

- **Easy:** Random moves.  
- **Medium-Hard:** Selects moves that maximize immediate point gain.  

### Scoring System

- Contiguous sequences grant points based on their length:
  - 3-symbol sequence: base score
  - 4-symbol sequence: higher score
  - 5 or more: highest score
- All sequences are evaluated across:
  - Rows
  - Columns
  - Diagonals
  - Anti-diagonals

### Game Logic

- **Turn-based system** with automatic player rotation  
- **Victory condition** based on reaching a **predefined score threshold**  
- Modular architecture for evaluating game states and computing scores

---

## Interfaces

- **Command-Line Interface (CLI):**
  - Prompts users for input
  - Displays board and game messages via console

- **Graphical User Interface (GUI):**
  - Built with **Tkinter** (optional)
  - Interactive grid and buttons for player moves
  - Intuitive feedback and visualization of current scores and board status

---

## AI Strategy

The AI components evaluate the board based on difficulty:
- **Easy AI:** purely random
- **Medium-Hard AI:** uses heuristics to score high-value positions

This strategic depth provides a strong foundation for studying AI behavior in turn-based games.

---

## Learning Objectives

This project is a useful resource for learning about:

- Game mechanics and logic design
- User interaction via CLI and GUI
- Turn-based systems and evaluation functions

---

## Requirements

- Python 3.x  
- (Optional) Tkinter for GUI

---

## Author

Francesco Lazzarotto  
Contact: francesco.lazzarotto@edu.unito.it  
