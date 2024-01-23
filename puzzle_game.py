'''
Ryon Sajnovsky
CS 5001, Fall 2022
Project
This program creates a slider puzzle game using Turtle
and python.
'''

from board import Board

def main():

    # Initializes a Board object.
    board = Board()

    # Calls the run_puzzle method to run the game.
    board.run_puzzle()

    # Allows the Turtle screen to stay up
    # while the user plays the game.
    board.screen.mainloop()

if __name__ == "__main__":
    main()