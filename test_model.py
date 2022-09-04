import unittest
from unittest import TestCase

from model.board import MineBoard
from model.cell import Cell, HIDDEN_CELL


class TestCell(TestCase):

    def test_cells_repr(self):
        c = Cell()
        self.assertEqual(c.get_representation(), HIDDEN_CELL)

        c = Cell(has_mine=True)
        self.assertEqual(c.get_representation(), HIDDEN_CELL)

        c = Cell(has_mine=True)
        c.reveal()
        self.assertEqual(c.get_representation(), 'M')

        c = Cell()
        c.no_adjacent_mines = 1
        self.assertEqual(c.get_representation(), HIDDEN_CELL)

        c = Cell()
        c.no_adjacent_mines = 1
        c.reveal()
        self.assertEqual(c.get_representation(), '1')

    def test_cells_debug_repr(self):
        c = Cell()
        self.assertEqual(c.get_debug_representation(), '[F0FF]')

        c = Cell(has_mine=True)
        self.assertEqual(c.get_debug_representation(), '[T0FF]')

        c = Cell()
        c.no_adjacent_mines = 1
        c.reveal()
        self.assertEqual(c.get_debug_representation(), '[F1FT]')


class TestMineBoard(TestCase):
    def test_is_valid(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        self.assertFalse(mb.is_valid_row(-1))
        self.assertTrue(mb.is_valid_row(0))
        self.assertTrue(mb.is_valid_row(1))
        self.assertTrue(mb.is_valid_row(NO_OF_ROWS - 1))
        self.assertFalse(mb.is_valid_row(NO_OF_ROWS))

        self.assertFalse(mb.is_valid_col(-1))
        self.assertTrue(mb.is_valid_col(0))
        self.assertTrue(mb.is_valid_col(1))
        self.assertTrue(mb.is_valid_col(NO_OF_COLS - 1))
        self.assertFalse(mb.is_valid_col(NO_OF_COLS))

    def test_dont_allow_double_plant(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        with self.assertRaises(RuntimeError) as re:
            x, y = 1, 1
            mb.plant_mine(x, y)
            mb.plant_mine(x, y)

        print(re.exception)

    def test_plant_invalid(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        with self.assertRaises(RuntimeError) as re:
            mb.plant_mine(-1, 0)

        with self.assertRaises(RuntimeError) as re:
            mb.plant_mine(0, mb.width)

    def test_surrounding_neighbours(self):
        def test(mb: MineBoard, x, y):
            from_x, from_y, to_x, to_y = mb._MineBoard__get_neighbours_range(x, y)
            print(f"{x, y} --> {from_x, from_y, to_x, to_y}")
            return from_x, from_y, to_x, to_y

        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)
        print(f"min_x = 0, min_y = 0, max_x = {NO_OF_COLS - 1}, max_y = {NO_OF_ROWS - 1}")

        self.assertEqual(test(mb, 1, 1), (0, 0, 2, 2))
        self.assertEqual(test(mb, 2, 2), (1, 1, 3, 3))
        self.assertEqual(test(mb, 0, 0), (0, 0, 1, 1))
        self.assertEqual(test(mb, mb.width - 1, mb.height - 1),
                         (NO_OF_COLS - 2, NO_OF_ROWS - 2, NO_OF_COLS - 1, NO_OF_ROWS - 1))

    def test_surrounding_neighbours_invalid_coordinates(self):
        def test(mb: MineBoard, x, y):
            from_x, from_y, to_x, to_y = mb._MineBoard__get_neighbours_range(x, y)
            print(f"{x, y} --> {from_x, from_y, to_x, to_y}")

        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        with self.assertRaises(RuntimeError) as re:
            test(mb, mb.width, mb.height)  # should fail, invalid coordinates

        with self.assertRaises(RuntimeError) as re:
            test(mb, 2 * mb.width, 2 * mb.height)  # should fail

    def test_plant_1_1(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        current_no_of_mines = mb.number_of_mines

        x, y = 1, 1
        mb.plant_mine(x, y)
        print(mb)

        # @formatter:off                  # <-- requires proper settings in pycharm (editor->code style->formatter)
        should_increase_coords = [
            (0, 0), (1, 0), (2, 0),
            (0, 1),         (2, 1),
            (0, 2), (1, 2), (2, 2),
        ]
        # @formatter:on

        # check if all neighbours increased their value of number of mines
        for c in should_increase_coords:
            n = mb.cells[c[1]][c[0]]
            self.assertEqual(n.no_adjacent_mines, 1)

        # check that the cell itself have not increased the value
        self.assertEqual(mb.cells[y][x].no_adjacent_mines, 0)

        # check if number of mines increased for the board
        self.assertEqual(mb.number_of_mines, current_no_of_mines + 1)

    def test_plant_0_0(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        current_no_of_mines = mb.number_of_mines

        x, y = 0, 0
        mb.plant_mine(x, y)
        print(mb)

        # @formatter:off                  # <-- requires proper settings in pycharm (editor->code style->formatter)
        should_increase_coords = [
                    (1, 0),
            (0, 1), (1, 1),
        ]
        # @formatter:on

        # check if all neighbours increased their value of number of mines
        for c in should_increase_coords:
            n = mb.cells[c[1]][c[0]]
            self.assertEqual(n.no_adjacent_mines, 1)

        # check that the cell itself have not increased the value
        self.assertEqual(mb.cells[y][x].no_adjacent_mines, 0)

        # check if number of mines increased for the board
        self.assertEqual(mb.number_of_mines, current_no_of_mines + 1)

    def test_plant_do_not_update_mine_cnt_for_mine(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        x, y = 1, 1
        # plant the first mine
        mb.plant_mine(x + 1, y)
        # plant a  mine next to the previous one; hopefully `no_adjacent_mines` of the first mine won't be increased
        mb.plant_mine(x, y)
        print(mb)
        # [F1FF][F2FF][F2FF][F1FF][F0FF][F0FF]
        # [F1FF][T0FF][T1FF][F1FF][F0FF][F0FF] <-- both mines (fields with [Txxx] should have the second digit = 0
        # [F1FF][F2FF][F2FF][F1FF][F0FF][F0FF]
        # [F0FF][F0FF][F0FF][F0FF][F0FF][F0FF]

        # tmp = [[c.reveal() for c in line] for line in mb.cells]
        # print(mb)
        # # 1221□□
        # # 1MM1□□
        # # 1221□□
        # # □□□□□□

        # @formatter:off                  # <-- requires proper settings in pycharm (editor->code style->formatter)
        expected_counts = [
            [1, 2, 2, 1],
            [1, 0, 0, 1],
            [1, 2, 2, 1]
        ]
        # @formatter:on

        # check if all neighbours increased their value of number of mines
        for i, counts in enumerate(expected_counts):
            for j, cnt in enumerate(counts):
                self.assertEqual(mb.cells[y - 1 + i][x - 1 + j].no_adjacent_mines, cnt)

    def test_plant_increase_by_2(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        print(mb)

        x, y = 1, 1
        mb.plant_mine(x, y)
        mb.plant_mine(x + 2, y)
        print(mb)
        # □□□□□□
        # □▣□▣□□
        # □□□□□□
        # □□□□□□

        # @formatter:off                  # <-- requires proper settings in pycharm (editor->code style->formatter)
        expected_counts = [
            [1, 1, 2, 1, 1],
            [1, 0, 2, 0, 1],
            [1, 1, 2, 1, 1]
        ]
        # @formatter:on

        # check if all neighbours increased their value of number of mines
        for i, counts in enumerate(expected_counts):
            for j, cnt in enumerate(counts):
                self.assertEqual(mb.cells[y - 1 + i][x - 1 + j].no_adjacent_mines, cnt)

    def test_plant_should_clear_mines_number(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 0, 0

        mb.cells[y][x].no_adjacent_mines = 2
        print(mb)

        mb.plant_mine(x, y)
        print(mb)

        # check that the cell itself have not increased the value
        self.assertEqual(mb.cells[y][x].no_adjacent_mines, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
