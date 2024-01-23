'''
Ryon Sajnovsky
CS 5001, Fall 2022
This class is used to store information about
each of the puzzle pieces.
'''

class Tile:
    '''
    A Tile is a puzzle piece in our slider puzzle. It is created when
    a our Board class creates tiles. A Tile holds its own information
    such as an individual Turtle object, an image, its index within
    a 2-D array that makes up out board and its x and y positions
    on the board. The get_tile_image returns the puzzle image assigned
    to the tile.
    '''

    def __init__(self, turtle, image, index, position_x = None, position_y = None):
        self.turtle = turtle
        self.image = image  # A .gif image.
        self.index = index  # Position within a nested list.
        self.position_x = position_x  # x coordinate on the puzzle board.
        self.position_y = position_y  # y coordinate on the puzzle board.
        self.turtle.hideturtle()

    def get_tile_image(self):
        '''
        Method -- get_tile_image
            Returns the .gif image assigned to the Tile attribute "image".
        Parameters:
            No parameters.
        Returns image assigned to Turtle object.
        '''

        return self.image




