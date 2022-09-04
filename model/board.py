import random
from typing import Tuple, List

from model import REVEAL_HIDDEN_MINE, DEBUG_INFO
from model.cell import Cell


class MineBoard:
    def __init__(self, width: int = 8, height: int = 8, expected_number_of_mines: int = 0):
        self.width: int = width
        self.height: int = height

        # this is a nominal/declared/given number of mines on the board (not calculated based on the actual board data)
        # in the future, it will be probably gone (used only as a constructor parameter)
        self.expected_number_of_mines = expected_number_of_mines

        # actual number of mines (derived from the board data)
        self.number_of_mines = 0

        # board content, holds `height` rows of `width` of Cell instances
        self.cells: List[List[Cell]] = None
        self.fill()
        # generate the mines, if needed
        if expected_number_of_mines > 0:
            self.__generate_mines(expected_number_of_mines)

        # self.cells = [[None for x in range(width)] for y in range(height)]

    def __str__(self):
        return '\n'.join(
            ''.join(c.get_representation(reveal_hidden_mine=REVEAL_HIDDEN_MINE) if c else "?" for c in row) for row in
            self.cells
        ) + '\n' if not DEBUG_INFO else self.__repr__()

    def __repr__(self):
        cells_str = '\n'.join(
            ''.join(c.get_debug_representation() if c else "[????]" for c in row) for row in
            self.cells
        ) + '\n'
        return f"no_of_mines: {self.number_of_mines}\n" + cells_str

    def fill(self):
        """
        Fills the board with "clear" cells (cells that don't contain mines)
        :return:
        """
        self.cells = [[Cell() for y in range(self.width)] for x in range(self.height)]

    def is_valid_row(self, y: int) -> bool:
        """
        Check if given row number is valid (belongs to the board)
        :param y:
        :return:
        """
        return self.height > y >= 0

    def is_valid_col(self, x: int):
        """
        Check if given column number is valid (belongs to the board)

        :param x:
        :return:
        """
        return 0 <= x < self.width

    def __get_neighbours_range(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get bounding coordinates of neighbouring cells.
        The method makes sure they do not "go outside the board".
        :param x:
        :param y:
        :return: from_x, from_y, to_x, to_y
        """
        # check if the coords are valid
        if not (self.is_valid_col(x) and self.is_valid_row(y)):
            raise RuntimeError(f"Invalid coordinates ({x}, {y}).")

        from_x = x - 1 if x > 0 else x
        from_y = y - 1 if y > 0 else y
        to_x = x + 1 if x < self.width - 1 else x
        to_y = y + 1 if y < self.height - 1 else y
        return from_x, from_y, to_x, to_y

    def is_mine_at(self, x: int, y: int) -> bool:
        return self.cells[y][x].has_mine

    def plant_mine(self, x: int, y: int):
        """
        Place a mine at given location.
        The method updates the board state:
            * increases the number of mines on the board
            * updates _no_adjacent_mines_ attribute of cells that surrounds the mine

        :param x:
        :param y:
        :return:
        """
        # check if the coords are valid
        if not (self.is_valid_col(x) and self.is_valid_row(y)):
            raise RuntimeError(f"Invalid coordinates ({x}, {y}).")

        # check if there is already a mine placed there
        if self.is_mine_at(x, y):
            raise RuntimeError(f"There is a mine already placed at ({x}, {y}).")

        # create a cell with a mine
        mine = Cell(has_mine=True)

        # place the mine on the board
        self.cells[y][x] = mine

        # update no_adjacent_mines of all the neighbours (cells adjacent to the mine)
        from_x, from_y, to_x, to_y = self.__get_neighbours_range(x, y)
        for row in range(from_y, to_y + 1):
            for col in range(from_x, to_x + 1):
                if (col, row) != (x, y):  # do not update the mine cell itself
                    if not self.is_mine_at(col, row):  # do not update adjacent mines
                        self.cells[row][col].no_adjacent_mines += 1

        # increase number of mines on the board
        self.number_of_mines += 1

    def expand(self, x: int, y: int):
        """
        TODO add description
        :param x:
        :param y:
        :return:
        """
        from_x, from_y, to_x, to_y = self.__get_neighbours_range(x, y)
        for row in range(from_y, to_y + 1):
            for col in range(from_x, to_x + 1):
                if (col, row) != (x, y):  # do not update the mine cell itself
                    c = self.cells[row][col]

                    # Only unrevealed cells need to be revealed.  <-- XXX TODO: assumption copied mindlessly from other solution; validate.
                    if not c.uncovered:
                        c.reveal()
                        if c.no_adjacent_mines > 0:
                            pass
                        else:  # it is an empty cell, expand neighbours
                            self.expand(col, row)

    def uncover(self, x: int, y: int) -> Cell:
        """

        :param x:
        :param y:
        :return:
        """
        # check if the coords are valid
        if not (self.is_valid_col(x) and self.is_valid_row(y)):
            raise RuntimeError(f"Invalid coordinates ({x}, {y}).")

        cell = self.cells[y][x]

        cell.reveal()
        if cell.has_mine:  # it's a mine, nothing to do more
            pass
        elif cell.no_adjacent_mines > 0:
            pass
        else:
            # no_adjacent_mines == 0, we need to expand the selection to all adjoining cells
            # that also have no adjacent mines
            self.expand(x, y)

        return cell

    def __generate_mines(self, expected_number_of_mines: int):
        # check if expected number of mines is realistic for this board
        field_cnt: int = self.width * self.height
        if not 0 <= expected_number_of_mines <= field_cnt:
            raise RuntimeError(f"Invalid mine count ({expected_number_of_mines}) for the board ({field_cnt} cells).")
        # track of number of mines already set up
        while self.number_of_mines < expected_number_of_mines:

            # get random board position
            shot = random.randint(0, self.width * self.height - 1)

            # get column and from the number
            x, y = shot % self.width, shot // self.height

            # Place the mine, if it doesn't already have one
            if not self.is_mine_at(x, y):
                self.plant_mine(x, y)
