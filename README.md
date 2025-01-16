# Wordle Game
Python-based word guessing game Wordle, using the Pygame library for user interaction. Player can have up to 6 guesses to correctly guess a hidden 5 letter word. After each guesses, the game provides feedback by color depending on player's guess.

- **Green:** The letter is correct and in the correct index.
- **Yellow:** The letter is corrrect but in the wrong index.
- **Gray:** The letter is not in the secret word.

## How It Works:
- The game randomly selects a 5 letter word from the given text file.
- Player inputs their guesses using the keyboard and hitting enter.
- The game compares each letters player inputted with the correct word and display corresponding colors.
- The game ends when player guesses the word correctly or uses all six attempts.

## Key Features:
- **Graphical Interface:** This game provides a graphical interface with a keyboard for input and indicators for displaying guesses.
- **Play Again Option:** After the game ends, the game provides with play again option which player can press "ENTER" key to play again with a new secret word.
- **Word Loading:** The secret words are loaded from a CSV file (FreqWords.csv), allowing for easy and secure access.
