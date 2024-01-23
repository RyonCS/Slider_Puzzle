'''
Ryon Sajnovsky
CS 5001, Fall 2022
Final Project
This class is used to create the puzzle board,
puzzle pieces, and controls all actions on the board.
'''

import os
import turtle
import math
from tiles import Tile
import random
import time
import datetime

class Board:
    '''
    A Board is an initialized playing area for our puzzle slider game.
    It holds voluminous amounts of information necessary for controlling
    the actions in our game. It creates puzzle pieces, a leaderboard,
    and buttons. It draws outlines of Tiles, and can draw the board
    outline. Further, it can read and siphon information from .txt
    files, slide tiles, reset the puzzle, load a new puzzle, quit the
    puzzle, track moves made, and see if a loaded puzzle is solvable.
    '''

    def __init__(self):
        self.puzzle_puz = "mario.puz" # Default puzzle file.
        self.total_pieces = None
        self.image_size = 98 # Default image size.
        self.puzzle_name = "mario" # Default puzzle name.
        self.puzzle_solution = None
        self.tiles = []  # A matrix of tile objects.
        self.grid_size = None
        self.turtle_images = None  # A matrix of random .gifs.
        self.swapped_images = []
        self.resource_images = []
        self.list_of_puzzles = []
        self.user_name = None
        self.max_moves = None
        self.error_list = []

        self.inversion_list = []
        self.nested_inversion_list = []
        self.inversion_count = None
        self.inversion_blank_index = None
        self.is_solvable = None

        self.screen = turtle.Screen()
        self.screen.onclick(self.swap_tile)

        self.square_turtle = turtle.Turtle()
        self.square_turtle.hideturtle()
        self.tile_image_turtle = turtle.Turtle()
        self.tile_image_turtle.hideturtle()

        self.click_counter = 0
        self.writer = None
        self.leader_board = []

        self.quitbutton = None
        self.load_button = None
        self.reset_button = None
        self.thumbnail = None

    def setup(self):
        '''
        Method -- setup
            Sets up the puzzle game's screen and presents
            a splash screen. Then, calls the user_inputs
            method to gather inputs from the user.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.screen.title("CS 5001 Sliding Puzzle Game")
        self.screen.register_shape("resources/splash_screen.gif")
        # Initializes a Turtle object to display the splash screen.
        tr = turtle.Turtle()
        tr.hideturtle()
        tr.goto(0, 0)
        tr.shape("resources/splash_screen.gif")
        start = time.time()
        while time.time() - start < 3:
            tr.showturtle()
            time.sleep(3)
        tr.hideturtle()
        # Calls a method to gather inputs from the user.
        self.user_inputs()

    def user_inputs(self):
        '''
        Method -- user_inputs
            Presents the user with two dialogue boxes. The first gathers
            the user's name. The second asks how many moves the user wants.
            The number of moves must be between 5 and 200. If the user
            inputs a number out of this range, they are presented with a
            dialogue box informing them their number was out of range. This
            will continue until the user enters a valid number.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Collects the user's name.
        self.user_name = turtle.textinput("CS5001 Puzzle Slide",
                                          "Your Name:")
        # Collects the user's desired moves.
        # Sets the range from 5-200.
        self.max_moves = turtle.numinput("5001 Puzzle Slide - Moves",
                                         "Enter the number of moves (chances)"
                                         " you want(5-200)", None, 5, 200)

    def run_puzzle(self):
        '''
        Method -- run_puzzle
            Calls the essential methods to set up the initial puzzle. It is
            called in our main function to run the puzzle.For more
            information on these methods, please read the docstrings
            assigned to these methods.
        Parameters:
            No parameters.
        Returns nothing.
        '''
        self.setup()
        self.draw_board_outline()
        self.register_puzzle_files()
        self.piece_counter()
        self.image_file_reader()
        self.register_turtle_images()
        self.register_resource_images()
        self.create_leaderboard()
        self.create_buttons()
        self.create_thumbnail()
        self.create_move_counter()
        self.create_tiles()
        self.draw_puzzle_pieces()
        self.inversion_list_maker()
        self.get_inversion_count()
        self.find_blank_index()
        self.solvable_puzzle_checker()
        print(self.is_solvable)
        if not self.is_solvable:
            self.show_unsolvable()
            self.redraw_loaded_board()

    def piece_counter(self, puzzle_name = None):
        '''
        Method -- piece_counter
            Reads a .txt file and extracts the number of pieces in the
            puzzle.
        Parameters:
            puzzle_name -- On first load of the game, this method does
            not take any parameters. On further loads of the game, the method
            take the name of the .puz file to read it and extract information.
        Returns nothing.
        '''

        with open(self.puzzle_puz, mode="r") as infile:
            # Line to read.
            line_number = [1]
            # Storing Line values.
            lines = []
            for i, line in enumerate(infile):
                # Read line 2.
                if i in line_number:
                    lines.append(line.strip())
            lines = ' '.join(lines)

            # Iterating through "lines" to pull out numbers and mush them
            # into a string.
            total_pieces = []
            for i in range(0, len(lines)):
                if lines[i].isnumeric():
                    total_pieces.append(lines[i])
                    # Converting number of pieces to an int and storing
                    # the number value.
            total_pieces = int(''.join(total_pieces))

        self.total_pieces = total_pieces

        # Squaring the total number of pieces to find the height and width
        # in tiles of our puzzle.
        grid_size = math.sqrt(self.total_pieces)
        self.grid_size = int(grid_size)

    def get_puzzle_name(self):
        '''
        Method -- get_puzzle_name
            Reads a .txt file and extracts the name of the puzzle.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        with open(self.puzzle_puz, mode="r") as infile:
            # Line to read.
            line_number = [0]
            # Storing Line values.
            lines = []
            for i, line in enumerate(infile):
                # Read line 0.
                if i in line_number:
                    lines.append(line.split())
            for i in range(len(lines)):
                lines[i].pop(0)
            puzzle_title = []
            for sublist in lines:
                for item in sublist:
                    puzzle_title.append(item)
            puzzle_title = ''.join(puzzle_title)

        self.puzzle_name = puzzle_title

    def get_image_size(self):
        '''
        Method -- get_image_size
            Reads a .txt file and extracts the size of the images.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        with open(self.puzzle_puz, mode="r") as infile:
            # Line to read.
            line_number = [2]
            # Storing Line values.
            lines = []
            for i, line in enumerate(infile):
                # Read line 3.
                if i in line_number:
                    lines.append(line.split())
            for i in range(len(lines)):
                lines[i].pop(0)
            image_size = []
            for sublist in lines:
                for item in sublist:
                    image_size.append(item)
            image_size = ''.join(image_size)

        self.image_size = int(image_size)

    def register_puzzle_files(self):
        '''
        Method -- register_puzzle_files
            Reads the directory containing our puzzle files and appends the
            attribute self.list_of_puzzles with each file containing ".puz".
        Parameters:
            No parameters.
        Returns nothing.
        '''

        for path in os.listdir():
            if ".puz" in path:
                self.list_of_puzzles.append(path)

    def register_resource_images(self):
        '''
        Method -- register_resource_images
            Reads the folder "resources" and extracts all images in the folder.
            Then calls the Screen object to add the images to the list of Turtle
            shapes.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        resource_images = []
        for file in os.listdir("Resources"):
            resource_images.append(file.strip())

        for image in resource_images:
            self.screen.addshape(f"resources/{image}")

    def image_file_reader(self):
        '''
        Method -- image_file_reader
            Reads a .txt file and extracts all .gif images listed in the file.
            Then,
        Parameters:
            puzzle_name -- On first load of the game, this method does
            not take any parameters. On further loads of the game, the method
            take the name of the .puz file to read it and extract information.
        Returns nothing.
        '''

        with open(self.puzzle_puz, mode="r") as infile:
            line_number = infile.readlines()
            temp_image_list = []
            temp_image_list_2 = []
            temp_list_3 = []
            shuffled_image_list = []
            # Reading lines of the text file from index 4 to end.
            for line in line_number[4:]:
                temp_image_list.append(line.split())
            for i in range(len(temp_image_list)):
                temp_image_list[i].pop(0)
            # Temp_image_list is a nested list. This pulls the strings from
            # the nested list.
            for sublist in temp_image_list:
                for item in sublist:
                    temp_image_list_2.append(item.lower())
            # The last item in temp_image_list_2 is the blank tile.
            blank_tile = temp_image_list_2.pop()

            temp_list_3.append(blank_tile)
            for i in range(self.total_pieces - 1):
                item = temp_image_list_2.pop()
                temp_list_3.append(item)

            # Reversing temp_list_3 gives us the correct order of the solved
            # puzzle.
            temp_list_3.reverse()
            solution_list = [temp_list_3[i:i + self.grid_size]
                             for i in range(0, len(temp_list_3), self.grid_size)]

            self.puzzle_solution = solution_list

            # Creates a nested list for our shuffled images used to create
            # our puzzle board.
            random.shuffle(temp_list_3)
            for i in range(self.grid_size):
                shuffled_image_list.append([])

            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    random_image = temp_list_3.pop()
                    shuffled_image_list[j].append(random_image)
            list.sort(shuffled_image_list)
            random.shuffle(shuffled_image_list)

        self.turtle_images = shuffled_image_list

    def register_turtle_images(self):
        '''
        Method -- register_turtle_images
            Adds .gif puzzle piece images and thumbnail to Turtle shapes.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        for row in self.turtle_images:
            for image in row:
                self.screen.addshape(image)

        self.screen.addshape(f"images/{self.puzzle_name}/"
                             f"{self.puzzle_name}_thumbnail.gif")

    def create_leaderboard(self):
        '''
        Method -- create_leaderboard
            Reads our leaderboard.txt file and extracts all lines. Then sorts the
            lines to create a list of our leaderboard value. Then uses this list
            and calls the draw_leaderboard method to create a visual leaderboard.
            If the leaderboard.txt file does not exist, presents the user with an
            error message and logs the error to our error .txt file.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        try:
            with open("leaderboard.txt", mode="r") as infile:
                # Storing Line values.
                lines = []
                temp = []
                for line in infile:
                    temp.append(line.split())

                # Temp is a nested list.
                for i in range(len(temp)):
                    temp[i][0] = int(temp[i][0])
                temp.sort()
                for i in range(len(temp)):
                    temp[i][0] = str(temp[i][0])
                for each in temp:
                    joined_each = ' '.join(each)
                    lines.append(joined_each)

            self.leader_board = lines

            # This method draws the leaderboard.
            self.draw_leaderboard()

        # If file not found, present user with a warning image and log error.
        except FileNotFoundError:
            error_time = datetime.datetime.now()
            tr = turtle.Turtle()
            tr.hideturtle()
            tr.goto(0, 0)
            tr.shape("resources/leaderboard_error.gif")
            start = time.time()
            time.time()
            while time.time() - start < 2:
                tr.showturtle()
                time.sleep(2)
            tr.hideturtle()
            self.error_logger(error_time,
                              f"Could not open leaderboard.txt.",
                              "self.create_leaderboard()")

    def draw_leaderboard(self):
        '''
        Method -- draw_leaderboard
            Initializes a Turtle object and writes the first 10 leaders from the
            Class's leader_board attribute in the leaderboard section.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        tr = turtle.Turtle()
        location = (125, 225)
        tr.penup()
        tr.hideturtle()
        tr.goto(125, 275)
        tr.color("Blue")
        tr.write("Leaders:", font=("Verdana", 16, "normal"))
        tr.showturtle()

        # Writes the first 10 values of our list in self.leader_board.
        # If less than 10 values in our list, writes all values.
        counter = 0
        for i in range(len(self.leader_board)):
            if counter != len(self.leader_board) and counter < 10:
                tr.penup()
                tr.hideturtle()
                tr.goto(location[0], location[1] - (25 * i))
                tr.pendown()
                tr.write(self.leader_board[i], font=("Verdana", 14, "normal"))
                counter += 1

    def create_thumbnail(self):
        '''
        Method -- create_thumbnail
            Initializes a Turtle object, sends the object to its location on the
            screen and displays the associated thumbnail image.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.thumbnail = turtle.Turtle()
        self.thumbnail.hideturtle()
        self.thumbnail.penup()
        self.thumbnail.goto(280, 275)
        self.thumbnail.pendown()
        self.thumbnail.shape(f"images/{self.puzzle_name}/{self.puzzle_name}_thumbnail.gif")
        self.thumbnail.showturtle()

    def error_logger(self, error_time, error_type, method_name):
        '''
        Method -- error_logger
            When an error occurs, the Board attribute "error_list" is appended
            with the error. When the program ends, this list is written to
            our error .txt file. The error includes: the time and date of the
            error, a description, and the method where the error occurred.
        Parameters:
            error_time -- The date and time of the error.
            error_type -- A short description of the error.
            method_name -- The name of the method where the error occurred.
        Returns nothing.
        '''

        error_to_log = []
        temp = f"{error_time}", f"Error: {error_type}", \
               f"LOCATION: {method_name}"
        temp = ' '.join(temp)
        error_to_log.append(temp)
        self.error_list.append(error_to_log)

    def create_reset_button(self):
        '''
        Method -- create_reset_button
            Initializes a Turtle object, sends it to its location on the board and
            displays the reset button image. When the turtle is clicked, it calls
            the method "reset_puzzle()".
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.reset_button = turtle.Turtle()
        self.reset_button.hideturtle()
        self.reset_button.penup()
        self.reset_button.speed(0)
        self.reset_button.goto(50, -225)
        self.reset_button.pendown()
        self.reset_button.shape("resources/resetbutton.gif")
        self.reset_button.showturtle()
        self.reset_button.onclick(self.reset_puzzle)

    def reset_puzzle(self, x, y):
        '''
        Method -- image_file_reader
            Method is called when the user clicks the reset button. It takes the
            puzzle solution list and assigns the Tile objects an image one by one.
            Then calls the "add_tiles()" method to redraw the board and displaying
            the puzzle in it's solved form.
        Parameters:
            x -- passed in because it is an onclick() function, but not used.
            y -- passed in because it is an onclick() function, but not used.
        Returns nothing.
        '''

        # Changes Tile image attributes to the puzzle solution.
        for i in range(len(self.puzzle_solution)):
            for j in range(len(self.puzzle_solution)):
                image = self.puzzle_solution[i][j]
                self.tiles[i][j].image = image

        # Adds the new images to the puzzle board.
        self.add_tiles()

    def create_load_button(self):
        '''
        Method -- create_load_button
            Initializes a Turtle object, sends it to its location on the board and
            displays the load button image. When the turtle is clicked, it calls
            the method "load_puzzle()".
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.load_button = turtle.Turtle()
        self.load_button.speed(0)
        self.load_button.hideturtle()
        self.load_button.penup()
        self.load_button.goto(150, -225)
        self.load_button.pendown()
        self.load_button.shape("resources/loadbutton.gif")
        self.load_button.showturtle()
        self.load_button.onclick(self.load_puzzle)

    def load_puzzle(self, x, y):
        '''
        Method -- load_puzzle
            First, creates a string that includes the names of the first 10 .puz
            files in our list_of_puzzles attribute. If there are more than 10 puzzles,
            a message is presented to the user, but the program continues. Then, asks
            the user for the .puz file they would like to load. If the puzzle name is
            in our list, our redraw_loaded_board() method is called. If the puzzle name
            is not in the list, an error is presented to the user and is logged in our
            error .txt file.
        Parameters:
            x -- passed in because it is an onclick() function, but not used.
            y -- passed in because it is an onclick() function, but not used.
        Returns nothing.
        '''

        # Creates a string of the first 10 puzzle names to present to the user.
        puzzle_names = ''
        counter = 0
        for i in range(len(self.list_of_puzzles)):
            if counter < 10 and counter != len(self.list_of_puzzles):
                puzzle_names += self.list_of_puzzles[i] + "\n"
                counter += 1

        # If the amount of puzzles is greater than 10, presents the user with a
        # message and logs the error.
        if len(self.list_of_puzzles) > 10:
            error_time = datetime.datetime.now()
            tr = turtle.Turtle()
            tr.hideturtle()
            tr.goto(0, 0)
            tr.shape("resources/file_warning.gif")
            start = time.time()
            while time.time() - start < 3:
                tr.showturtle()
                time.sleep(3)
            tr.hideturtle()
            self.error_logger(error_time,
                              f"More than 10 puzzles.",
                              "self.load_puzzle()")

        # Gathers the user's input.
        text_file = self.screen.textinput("Load Puzzle",
                                          "Enter the name of the puzzle "
                                          "you wish to load. Choices are:\n"
                                          + puzzle_names).lower()

        '''self.piece_counter(text_file)
        if not isinstance(self.grid_size, int):
            error_time = datetime.datetime.now()
            tr = turtle.Turtle()
            tr.hideturtle()
            tr.goto(0, 0)
            tr.shape("resources/file_error.gif")
            start = time.time()
            while time.time() - start < 3:
                tr.showturtle()
                time.sleep(3)
            tr.hideturtle()
            self.error_logger(error_time,
                              f"File: {text_file} number not a square number.",
                              "self.load_puzzle()")'''

        if text_file in self.list_of_puzzles:
                if isinstance(self.grid_size, int):
                    self.piece_counter(text_file)
                    self.puzzle_puz = text_file
                    self.redraw_loaded_board()

        # If user input is not a valid puzzle, presents the user with an error
        # message and logs the error.
        if text_file not in self.list_of_puzzles:
            error_time = datetime.datetime.now()
            tr = turtle.Turtle()
            tr.hideturtle()
            tr.goto(0,0)
            tr.shape("resources/file_error.gif")
            start = time.time()
            while time.time() - start < 3:
                tr.showturtle()
                time.sleep(3)
            tr.hideturtle()
            self.error_logger(error_time,
                              f"File: {text_file} does not exist.",
                              "self.load_puzzle()")

    def create_quit_button(self):
        '''
        Method -- create_quit_button
            Initializes a Turtle object, sends it to its location on the board and
            displays the quit button image. When the turtle is clicked, it calls
            the method "quit_puzzle()".
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.quitbutton = turtle.Turtle()
        self.quitbutton.hideturtle()
        self.quitbutton.speed(0)
        self.quitbutton.penup()
        self.quitbutton.goto(250, -225)
        self.quitbutton.pendown()
        self.quitbutton.shape("resources/quitbutton.gif")
        self.quitbutton.showturtle()
        self.quitbutton.onclick(self.quit_puzzle)

    def quit_puzzle(self, x, y):
        '''
        Method -- quit_puzzle
            Initializes a Turtle object, sends it to its location on the board and
            displays the quit button image. When the turtle is clicked, it calls
            the method "quit_puzzle()".
        Parameters:
            x -- passed in because it is an onclick() function, but not used.
            y -- passed in because it is an onclick() function, but not used.
        Returns nothing.
        '''

        tr = turtle.Turtle()
        tr.hideturtle()
        tr.penup()
        tr.goto(0, 0)
        tr.shape("resources/quitmsg.gif")
        start = time.time()
        while time.time() - start < 3:
            tr.showturtle()
            time.sleep(3)
        tr.shape("resources/credits.gif")
        start = time.time()
        while time.time() - start < 4:
            tr.showturtle()
            time.sleep(4)

        # Writes error list to .err file.
        with open("5001_puzzle.err", mode="a") as infile:
            for each in self.error_list:
                to_write = ' '.join(each)
                infile.write(to_write)
                infile.write("\n")
        self.screen.bye()

    def create_move_counter(self):
        '''
        Method -- create_move_counter
            Initializes a Turtle object, sends it to its location on the board and
            writes the amount of moves the user has taken.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.speed(0)
        self.writer.goto(-310, -235)
        self.writer.write(f"Player Moves: {self.click_counter}", font=("Verdana", 20, "normal"))

    def redraw_loaded_board(self):
        '''
        Method -- redraw_loaded_board
            This method is called when the user clicks on the load button and
            enters a valid puzzle name. First, this method clears Board attributes
            that relate to Tile objects including Tile attributes and lists holding
            solutions, and resets the click counter. Then calls the various methods
            to recreate the game with the loaded puzzle.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Clearing Board attributes.
        self.turtle_images.clear()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.tiles[i][j].turtle.shape("blank")
        self.square_turtle.clear()
        self.puzzle_solution.clear()
        self.swapped_images.clear()
        self.tiles.clear()
        self.reset_click_counter()

        # Running various methods needed to reload the board.
        self.piece_counter()
        self.get_puzzle_name()
        self.get_image_size()
        self.image_file_reader()
        self.register_turtle_images()
        self.thumbnail.shape("blank")
        self.create_thumbnail()
        self.create_move_counter()
        self.create_tiles()
        self.draw_puzzle_pieces()
        self.inversion_list.clear()
        self.nested_inversion_list = []
        self.inversion_list_maker()
        self.inversion_blank_index = None

        # Prints back-end information about the puzzle's solvability.
        print("Grid side: ", self.grid_size)
        self.get_inversion_count()
        print("Inv Count: ", self.inversion_count)
        self.find_blank_index()
        print("Blank Index from top: ", self.inversion_blank_index)
        if self.grid_size == 4:
            print("Inversion List + Blank Index: ", (self.inversion_count + self.inversion_blank_index))
        print("Inversion List: ", self.nested_inversion_list)
        self.solvable_puzzle_checker()
        print("Solvable?", self.is_solvable)

        # If puzzle is not solvable, reruns this method until puzzle is solvable.
        if not self.is_solvable:
            self.show_unsolvable()
            self.redraw_loaded_board()

    def reset_click_counter(self):
        '''
        Method -- reset_click_counter
            A simple method that clears the Turtle object that writes the user's
            total moves and resets the click_counter to 0. Called when we redraw
            our board with a new loaded puzzle.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.writer.clear()
        self.click_counter = 0

    def inversion_list_maker(self):
        '''
        Method -- inversion_list_maker
            Creates two lists: 1. A nested list of the current puzzle pieces. 2. A
             list which takes the nested list and flattens it from 2D to 1D. The
            values of the list are based on the number of the image gif. The blank
            tile is given the value of zero. The nested list is used to find the
            index of the row containing the blank tile. The 1D list is used to count
            the number of inversions. The 1D list is assigned to Board attribute
            "inversion_list". The 2D list is assigned to Board attribute
            "nested_inversion_list".
        Parameters:
            No parameters.
        Returns nothing.
        '''
        temp2 = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                image = self.tiles[i][j].image
                temp2.append(image)

        for i in range(len(temp2)):
            image = temp2[i].replace(f"images/{self.puzzle_name}/", '').replace(".gif", '')
            self.inversion_list.append(image)

        for i in range(len(self.inversion_list)):
            if self.inversion_list[i] == "blank":
                self.inversion_list[i] = "0"

        for i in range(len(self.inversion_list)):
            try:
                self.inversion_list[i] = int(self.inversion_list[i])
            except ValueError:
                continue

        for i in range(self.grid_size):
            temp = []
            for j in range(self.grid_size):
                temp.append(self.inversion_list[i * self.grid_size + j])
            self.nested_inversion_list.append(temp)

        for i in range(len(self.nested_inversion_list)):
            for j in range(len(self.nested_inversion_list)):
                try:
                    self.nested_inversion_list[i][j] = int(self.nested_inversion_list[i][j])
                except ValueError:
                    continue

    def get_inversion_count(self):
        '''
        Method -- get_inversion_count
            Takes the first number in a list, then iterates through each other number
            in the list. If the first number is larger than another number in the list,
            the count increases. Once the end of the list is reached, takes the second
            number and repeats, over and over until list has been run through. The 0 in
            the list is the blank tile and is skipped when comparing two numbers.
            The count is assigned to Board attribute "inversion_count".
        Parameters:
            No parameters.
        Returns nothing.
        '''

        test_list = self.inversion_list
        count = 0

        for i in range(self.total_pieces - 1):
            for j in range(i + 1, self.total_pieces):
                if test_list[j] and test_list[i] and test_list[i] > test_list[j]:
                    if test_list[j] == 0:
                        continue
                    count += 1

        self.inversion_count = count

    def find_blank_index(self):
        '''
        Method -- find_blank_index
            Iterates through a nested list. Once 0 is found, the
            loop stops and the index of the row containing the 0
            is assigned to the Board attribute "inversion_blank_index".
        Parameters:
            No parameters.
        Returns nothing.
        '''
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.nested_inversion_list[i][j] == 0:
                    self.inversion_blank_index = i
                    break

    def solvable_puzzle_checker(self):
        '''
        Method -- solvable_puzzle_checker
            Checks whether the loaded puzzle is solvable. If the grid size of the
            puzzle is odd, the puzzle is solvable if the inversion count is even.
            If the grid size is even and > 2, the puzzle is solvable if the inversion
            count plus the index of the blank tile is odd. If the grid size is even and
            < 4, the puzzle is solvable if it is in one of 12 formations.
            Board attribute "is_solvable" is updated with the results.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # If grid is odd, puzzle is solvable if inversion count is even.
        if self.grid_size % 2 != 0 and self.inversion_count % 2 == 0:
            self.is_solvable = True
        else:
            self.is_solvable = False

        # If grid is even and > 2, puzzle is solvable if
        # inversion count + index of row containing blank index = odd number.
        if self.grid_size % 2 == 0 and self.grid_size > 2:
            if (self.inversion_count + self.inversion_blank_index) % 2 != 0:
                self.is_solvable = True
            else:
                self.is_solvable = False

        # If grid is even and < 4, puzzle is solvable if the inversion_list
        # is one of the following below.
        if self.grid_size % 2 == 0 and self.grid_size == 2:
            print(self.inversion_list)
            if self.inversion_list == [4, 3, 2, 0] or self.inversion_list == [4, 0, 3, 2] or \
                self.inversion_list == [0, 4, 3, 2] or self.inversion_list == [2, 4, 0, 3] or \
                self.inversion_list == [2, 4, 3, 0] or self.inversion_list == [2, 0, 3, 4] or \
                self.inversion_list == [0, 2, 3, 4] or self.inversion_list == [3, 2, 0, 4] or \
                self.inversion_list == [3, 2, 4, 0] or self.inversion_list == [3, 0, 4, 2] or \
                self.inversion_list == [0, 3, 4, 2] or self.inversion_list == [4, 3, 0, 2]:
                self.is_solvable = True
            else:
                self.is_solvable = False

                '''[4, 3, 2, 0], [4, 0, 3, 2], [0, 4, 3, 2], [2, 4, 0, 3], [2, 4, 3, 0], [2, 0, 3, 4]
                [0, 2, 3, 4], [3, 2, 0, 4], [3, 2, 4, 0], [3, 0, 4, 2], [0, 3, 4, 2], [4, 3, 0, 2]'''

                '''if self.inversion_list == [4, 3, 2, 0] or self.inversion_list == [4, 0, 2, 3] or \
                self.inversion_list == [0, 4, 2, 3] or self.inversion_list == [2, 4, 0, 3] or \
                self.inversion_list == [2, 0, 3, 4] or self.inversion_list == [0, 2, 3, 4] or \
                self.inversion_list == [3, 2, 0, 4] or self.inversion_list == [3, 2, 4, 0] or \
                self.inversion_list == [3, 0, 4, 2] or self.inversion_list == [0, 3, 4, 2] or \
                self.inversion_list == [4, 3, 0, 2]:
                self.is_solvable = True
            else:
                self.is_solvable = False'''

    def find_blank_tile(self):
        '''
        Method -- find_blank_tile
            Iterates through the 2D list of Tile objects stored in Board
            attribute "tiles" to find the tile with the image of the
            blank tile. This method is called in "swap_tile" method.
        Parameters:
            No parameters.
        Returns the index of the blank tile.
        '''

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if str(self.tiles[i][j].image) == f"images/{self.puzzle_name}/blank.gif":
                    blank_index = [i, j]
                    return blank_index

    def show_unsolvable(self):
        '''
        Method -- show_unsolvable
            Initializes a Turtle Object, sends it to the center of the
            screen and displays an image informing the user the puzzle
            that was loaded was unsolvable and that a new puzzle will be
            loaded.
        Parameters:
            No parameters.
        Returns nothing.
        '''
        tr = turtle.Turtle()
        tr.hideturtle()
        tr.penup()
        tr.goto(0, 0)
        tr.shape("resources/unsolvable.gif")
        start = time.time()
        while time.time() - start < 2:
            tr.showturtle()
            time.sleep(2)
        tr.hideturtle()

    def create_tiles(self):
        '''
        Method -- create_tiles
            Creates a 2D list of Tile Objects. Each Tile object is assigned
            a Turtle object and an image and its index within the 2D list.
            This method is called whenever a new puzzle is created.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Creates an empty nested list.
        for i in range(self.grid_size):
            self.tiles.append([])
        # Appends empty nested list with Tile objects.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.tiles[j].append(Tile(turtle.Turtle(), self.turtle_images[i][j], (i, j)))

    def draw_board_outline(self):
        '''
        Method -- draw_board_outline
            Initializes a Turtle object and has it draw the three
            rectangles that make up the puzzle game board.
        Parameters:
            No parameters.
        Returns nothing.
        '''
        tr = turtle.Turtle()
        tr.hideturtle()
        tr.speed(0)
        tr.width(3.5)

        # Draw Game Board
        tr.penup()
        tr.goto(-337, 305)
        tr.pendown()
        tr.forward(435)  # top of board
        tr.right(90)
        tr.forward(445)  # right side
        tr.right(90)
        tr.forward(435)  # bottom of board
        tr.right(90)
        tr.forward(445)  # left_side
        tr.right(90)

        # Draw leaderboard.
        tr.color("Blue")
        tr.penup()
        tr.goto(111, 305)
        tr.pendown()
        tr.forward(200)  # top of board
        tr.right(90)
        tr.forward(445)  # right side
        tr.right(90)
        tr.forward(200)  # bottom of board
        tr.right(90)
        tr.forward(445)  # left_side
        tr.right(90)

        # Draw Control Panel.
        tr.color("Black")
        tr.penup()
        tr.goto(-337, -180)
        tr.pendown()
        tr.forward(648)  # top of board
        tr.right(90)
        tr.forward(90)  # right side
        tr.right(90)
        tr.forward(648)  # bottom of board
        tr.right(90)
        tr.forward(90)  # left_side
        tr.right(90)

    def draw_puzzle_pieces(self):
        '''
        Method -- draw_puzzle_pieces
            Initializes a Turtle object. The Turtle goes to the top left
            corner of the screen and draws a matrix of  squares based on
            the size of the image. Then, it calls the add_tiles method to
            add puzzle images to the center of each square.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Draws tile squares and assigns Tile turtle its corresponding image.
        tr = self.square_turtle
        tr.hideturtle()
        tr.speed(0)
        tr.width(2)
        tr.penup()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Sets a starting location for our grid.
                location = (-326, 288)

                # Directs the Turtle to the top left of the screen.
                next_location = location[0] + (104 * j), location[1] - (104 * i)
                tr.goto(next_location)
                tr.pendown()

                # Draws a simple square. The edges of the square are the length
                # of the puzzle image size.
                tr.forward(self.image_size)  # Top.
                tr.right(90)
                tr.forward(self.image_size)  # Right.
                tr.right(90)
                tr.forward(self.image_size)  # Left.
                tr.right(90)
                tr.forward(self.image_size)  # Bottom.
                tr.right(90)
                tr.penup()

        # Calls a method that adds images to the center of the squares drawn.
        self.add_tiles()

    def create_buttons(self):
        '''
        Method -- create_buttons
            Calls three methods that create the reset, quit, and load buttons.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        self.create_reset_button()
        self.create_load_button()
        self.create_quit_button()

    def add_tiles(self):
        '''
        Method -- add_tiles
            Places a Tile object at the center of each square drawn in the
            draw_puzzle_pieces method. Screen animation is shut off at the
            beginning of this method for a more seamless user experience.
            This method is called whenever the draw_puzzle_pieces method is
            called.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Turns off screen animation.
        self.screen.tracer(0)

        # Sets the initial location to the top left of the screen.
        location = (-326, 288)

        for i in range(self.grid_size):
            for j in range(self.grid_size):

                # Sets the Tile's location on the board to the center of each square
                # drawn on the board.
                next_location = location[0] + (104 * j), location[1] - (104 * i)
                image_location_x = next_location[0] + (self.image_size / 2)
                image_location_y = next_location[1] - (self.image_size / 2)
                puzzle_piece = self.tiles[i][j].turtle
                puzzle_piece.hideturtle()

                # Assigns the Tile object it's x and y coordinates.
                self.tiles[i][j].position_x = image_location_x
                self.tiles[i][j].position_y = image_location_y

                # Sends the Tile object to the center of each square.
                puzzle_piece.penup()
                puzzle_piece.goto(image_location_x, image_location_y)
                puzzle_piece.shape(self.tiles[i][j].image)
                puzzle_piece.showturtle()

        # Restores screen animation.
        self.screen.tracer(1)

    def is_adjacent(self, tile_1, tile_2):
        '''
        Method -- is_adjacent
            Checks whether the index of a clicked Tile object, within the
            2D matrix of Tile objects stores in Board attribute "tile", is
            adjacent to the index of a blank tile within the 2D matrix. It
            checks vertically and horizontally.
        Parameters:
            tile_1 -- The index of the clicked tile's row and column
                      within the nested list of Tile objects.
            tile_2 -- The index of the blank tile's row and column
                      within the nested list of Tile objects.
        Returns True if tile_1 is adjacent vertically or horizontally
            to tile_2 within the nested list of Tile objects.
        '''

        # Checks whether the clicked tile and blank tile are adjacent horizontally.
        if abs(tile_2[1] - tile_1[1]) == 1 and abs(tile_2[0] - tile_1[0]) == 0:
            return True

        # Checks whether the clicked tile and blank tile are adjacent vertically.
        if abs(tile_2[0] - tile_1[0]) == 1 and abs(tile_2[1] - tile_1[1]) == 0:
            return True

        else:
            return False

    def get_all_tile_images(self):
        '''
        Method -- get_all_tile-images
            Creates a nested list of .gifs in order that they appear in
            the 2D list of Tile objects stored in Board attribute "tiles".
            The nested list is stored in Board attribute "swapped_images".
            This method is called whenever a tile is successfully swapped.
            This list is used in another method to see if the puzzle has
            been solved.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Creates a nested list filled with #.
        # The "#" is used as a placeholder.
        self.swapped_images = [["#" for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Checks Tile objects for their images and
        # changes the "#" in the nested list to the Tile objects image.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile_image = self.tiles[i][j].get_tile_image()
                self.swapped_images[i][j] = tile_image

    def swap_tile(self, x, y):
        '''
        Method -- swap_tile
            First, checks whether a Tile object has been clicked on by creating
            an x and y boundary for each tile. If a Tile is clicked, its index within
            the 2D matrix of Tiles is stored. Tt then calls the find_blank_tile function
            to find the index of the blank tile. Then, the is_adjacent method is called.
            If is_adjacent returns True, the Tile objects are swapped and the Tiles are
            reinitialized. Each time a tile is swapped, the move_counter increases by +1.
            Also, each time a tile is swapped, the check_winner method is called to check
            whether the list of all images is equal to the puzzle solution.
        Parameters:
            x -- passed in because it is an onclick() function, but is unused.
            y -- passed in because it is an onclick() function, but is unused.
        Returns nothing.
        '''

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Creates an x, y boundary for each tile object based on
                # The size of the image.
                if (self.tiles[i][j].position_x - (self.image_size / 2) < x
                        < self.tiles[i][j].position_x + (self.image_size / 2)
                        and self.tiles[i][j].position_y - (self.image_size / 2) <
                        y < self.tiles[i][j].position_y + (self.image_size / 2)):
                    tile_index = [i, j]
                    blank_index = self.find_blank_tile()

                    # Checks whether the Tile clicked is adjacent to the blank tile
                    # In the 2D matrix of Tile objects.
                    if self.is_adjacent(tile_index, blank_index):
                        self.click_counter += 1
                        # Animation is turned off for a more seamless user experience.
                        self.screen.tracer(0)
                        self.writer.clear()
                        self.writer.write(f"Player Moves: {self.click_counter}",
                                          font=("Verdana", 20, "normal"))
                        self.screen.tracer(1)

                        # Swaps the blank tile and clicked Tile object in the
                        # nested list of Tile objects.
                        temp = self.tiles[blank_index[0]][blank_index[1]]
                        self.tiles[blank_index[0]][blank_index[1]] = self.tiles[tile_index[0]][tile_index[1]]
                        self.tiles[tile_index[0]][tile_index[1]] = temp

                        # Updates the swapped_images list because the Tile objects
                        # and their images have moved within the list.
                        self.swapped_images.clear()
                        self.get_all_tile_images()
                        self.add_tiles()

                        # Checks if the swapped_images list == solution_list.
                        self.check_winner()

    def check_winner(self):
        '''
        Method -- check_winner
            First, checks whether the amount of user's moves is less than they
            entered at the start of the game. If it is, checks whether the image
            list after the last swapped tile matches the solution list.
            If it does, it writes the user's name and the amount of moves to the
            leaderboard file, shows an image saying they won and quits the game.
            If the user has not won, and the user's moves is less than the amount
            of moves they entered at the start of the game, this method does nothing
            further. If the leaderboard.txt file is not found, one is created, the
            user is shown an error message and the error is logged in the error list.
            Then, the error_list is written to the .err txt file.

            Second, if the amount of user's moves is greater than they entered at the
            start of the game, an image is shown saying they lost, the credits are shown,
            and the game quits. Then, the error_list is written to the .err txt file.
        Parameters:
            No parameters.
        Returns nothing.
        '''

        # Compares user's moves to their max moves.
        if self.click_counter < self.max_moves:
            # Compares order of current Tile images to solution list.
            if self.puzzle_solution == self.swapped_images:
                with open("leaderboard.txt", mode="a") as outfile:
                    outfile.write((f"{self.click_counter} : {self.user_name} \n"))

                # Initializes a Turtle to show winner image.
                tr = turtle.Turtle()
                tr.hideturtle()
                tr.penup()
                tr.goto(0, 0)
                tr.pendown()
                tr.shape("resources/winner.gif")
                start = time.time()
                while time.time() - start < 3:
                    tr.showturtle()
                    time.sleep(3)

                # Writes error list to .err file.
                with open("5001_puzzle.err", mode="a") as infile:
                    for each in self.error_list:
                        to_write = ' '.join(each)
                        infile.write(to_write)
                        infile.write("\n")
                self.screen.bye()

        else:
            # Initializes a Turtle to show lose image.
            tr = turtle.Turtle()
            tr.hideturtle()
            tr.penup()
            tr.goto(0, 0)
            tr.pendown()
            tr.shape("resources/Lose.gif")
            start = time.time()
            while time.time() - start < 3:
                tr.showturtle()
                time.sleep(3)

            # Shows credits.
            tr.shape("resources/credits.gif")
            start = time.time()
            while time.time() - start < 4:
                tr.showturtle()
                time.sleep(4)

            # Writes error list to .err file.
            with open("5001_puzzle.err", mode="a") as infile:
                for each in self.error_list:
                    to_write = ' '.join(each)
                    infile.write(to_write)
                    infile.write("\n")
            self.screen.bye()