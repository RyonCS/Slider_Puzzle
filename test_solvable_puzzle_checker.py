'''
Ryon Sajnovsky
CS 5001, Fall 2022
Final Project
This program performs multiple test cases to prove that
the puzzle solution code in my Final Project can actually
detect an unsolvable puzzle.
'''

from board import Board
import unittest

class TestPuzzleSolvable(unittest.TestCase):
    '''
    A TestPuzzleSolvable is a Pyunit test that checks
    whether a puzzle is solvable.

    An odd size puzzle is solvable if the number of inversions
    is even. E.g. Luigi puzzle.

    An even size puzzle with a grid size >= 4 is solvable if the
    number of inversions plus the index of the row the blank tile
    is odd. E.g. Mario puzzle.

    An even size puzzle with a grid size < 4 is solvable only if
    it is one of 12 formations. E.g. Yoshi puzzle.

    For each test, is_solvable == True if the puzzle is solvable and
    is_solvable == False if the puzzle is not solvable.

    Note: an inversion is any pair of tiles i and j where i > j and
    i appears before j when considering the board in flattened list form.
    The 0 tile is skipped because it is just a placeholder for the blank tile.
    '''

    def test_solvable_puzzle_checker_4x4(self):
        ''' The first four tests test a 4x4 puzzle.'''
        board = Board()
        board.grid_size = 4
        board.total_pieces = 16

        '''Test 1: An even inversion count with an odd blank tile index.'''
        # Inversion count is 2 (2 -> 1, 15 -> 14)
        board.inversion_list = [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0]
        # Blank tile index is 3 because it is in the third nested list.
        board.nested_inversion_list = [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]]
        board.get_inversion_count()
        board.find_blank_index()
        board.solvable_puzzle_checker()

        # Even inversion + odd blank index = odd number, puzzle is solvable.
        self.assertEqual(board.is_solvable, True)

        '''Test 2: An odd inversion count with an even blank tile index.'''
        # Inversion count is 1: (15 > 14)
        board.inversion_list = [1, 2, 3, 4, 5, 6, 7, 8, 0, 9, 10, 11, 12, 13, 15, 14]
        # Blank tile index is 2 because it is in the third nested list.
        board.nested_inversion_list = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 10, 11], [12, 13, 15, 14]]
        board.get_inversion_count()
        board.find_blank_index()
        board.solvable_puzzle_checker()

        # Odd inversion + even blank index = odd number, puzzle is solvable.
        self.assertEqual(board.is_solvable, True)

        '''Test 3: Testing an odd inversion count with an odd blank tile index.'''
        # Inversion count is 3: (10 > 9, 15 > 13, 15 > 14)
        board.inversion_list = [1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, 13, 14, 15, 0]
        # Blank tile index is 3 because it is in the third nested list.
        board.nested_inversion_list = [[1, 2, 3, 4], [5, 6, 7, 8], [10, 9, 11, 12], [15, 13, 14, 0]]
        board.get_inversion_count()
        board.find_blank_index()
        board.solvable_puzzle_checker()

        # Odd inversion + odd blank index = even number, puzzle is not solvable.
        self.assertEqual(board.is_solvable, False)

        '''Test 3: Testing an even inversion count with an even blank tile index.'''
        # Inversion count is 6: (3 > 2, 3 > 1, 2 > 1, 11 > 10, 11 > 9, 10 > 9)
        board.inversion_list = [3, 2, 1, 4, 0, 5, 6, 7, 8, 11, 10, 9, 12, 13, 14, 15]
        # Blank tile index is 2 because it is in the second nested list.
        board.nested_inversion_list = [[3, 2, 1, 4], [5, 6, 7, 8], [0, 11, 10, 9], [12, 13, 14, 15]]
        board.get_inversion_count()
        board.find_blank_index()
        board.solvable_puzzle_checker()

        # Even inversion + even blank index = even number, puzzle is not solvable.
        self.assertEqual(board.is_solvable, False)

    def test_solvable_puzzle_checker_3x3(self):
        '''The next two tests test a 3x3 puzzle. The 3x3 puzzle only needs to know inversion count'''
        board = Board()
        board.grid_size = 3
        board.total_pieces = 9

        '''Test 1: Testing an even inversion count.'''
        # inversion count is 4: (2 > 1, 7 > 4, 7 > 5, 7 > 6)
        board.inversion_list = [2, 1, 3, 7, 4, 5, 6, 8, 0]

        board.get_inversion_count()
        board.solvable_puzzle_checker()

        # Even inversion, puzzle is solvable.
        self.assertEqual(board.is_solvable, True)

        '''Test 1: Testing an odd inversion count.'''
        # inversion count is 5: (2 > 1, 5 > 3, 5 > 4, 8 > 6, 8 > 7)
        board.inversion_list = [2, 1, 5, 3, 4, 8, 6, 7, 0]

        board.get_inversion_count()
        board.solvable_puzzle_checker()

        # Odd inversion, puzzle is not solvable.
        self.assertEqual(board.is_solvable, False)

    def test_solvable_puzzle_checker_2x2(self):
        '''The next four tests test a 2x2 puzzle. The 2x2 puzzle has 12 solvable formations:
        [4, 3, 2, 0], [4, 0, 3, 2], [0, 4, 3, 2], [2, 4, 0, 3], [2, 4, 3, 0], [2, 0, 3, 4]
        [0, 2, 3, 4], [3, 2, 0, 4], [3, 2, 4, 0], [3, 0, 4, 2], [0, 3, 4, 2], [4, 3, 0, 2]
        We will not be using inversion or blank tile index for these tests.'''

        board = Board()
        board.grid_size = 2
        board.total_pieces = 4

        '''Test 1: Testing a solvable puzzle formation.'''
        board.inversion_list = [0, 4, 3, 2]

        board.solvable_puzzle_checker()

        # Inversion_list is in a solvable formation, puzzle is solvable.
        self.assertEqual(board.is_solvable, True)

        '''Test 2: Testing a solvable puzzle formation.'''
        board.inversion_list = [4, 3, 0, 2]

        board.solvable_puzzle_checker()

        # Inversion_list is in a solvable formation, puzzle is solvable.
        self.assertEqual(board.is_solvable, True)

        '''Test 3: Testing an unsolvable formation.'''
        board.inversion_list = [4, 2, 3, 0]

        board.solvable_puzzle_checker()

        # Inversion_list is in not a solvable formation, puzzle is not solvable.
        self.assertEqual(board.is_solvable, False)

        '''Test 3: Testing an unsolvable formation.'''
        board.inversion_list = [2, 0, 4, 3]

        board.solvable_puzzle_checker()

        # Inversion_list is in not a solvable formation, puzzle is not solvable.
        self.assertEqual(board.is_solvable, False)

def main():
    unittest.main(verbosity=5)

if __name__ == "__main__":
    main()
