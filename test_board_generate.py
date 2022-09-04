import unittest
from unittest import TestCase

from model.board import MineBoard


class TestMineBoardGenerate(TestCase):
    def test_generate_1_1(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4

        expected_number_of_mines: int = 1
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
        print(mb)
        self.assertEqual(mb.number_of_mines, expected_number_of_mines)

    def test_generate_1_2(self):
        expected_number_of_mines: int = 1
        for i in range(32):
            mb = MineBoard(1 + i, 1 + i, expected_number_of_mines)
            print(mb)
            self.assertEqual(mb.number_of_mines, expected_number_of_mines)

    def test_generate_1_2(self):
        for i in range(1, 33):
            expected_number_of_mines: int = i
            mb = MineBoard(i, i, expected_number_of_mines)
            print(mb)
            self.assertEqual(mb.number_of_mines, expected_number_of_mines)

    def test_generate_full_board(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4

        expected_number_of_mines: int = NO_OF_ROWS * NO_OF_COLS
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
        print(mb)
        self.assertEqual(mb.number_of_mines, expected_number_of_mines)

    def test_generate_more_mines_than_cell(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 4

        expected_number_of_mines: int = NO_OF_ROWS * NO_OF_COLS + 1
        with self.assertRaises(RuntimeError) as re:
            mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
        print(re.exception)

    def test_generate_check_position_freq(self):
        def find_mines(mb: MineBoard, return_only_first: bool = True):
            mines = []
            for y in range(0, mb.height):
                for x in range(0, mb.width):
                    if mb.is_mine_at(x, y):
                        mines.append((x, y))
            return None if len(mines) == 0 else mines[0] if return_only_first else mines

        NO_OF_ROWS, NO_OF_COLS = 4, 4
        expected_number_of_mines: int = 1
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
        print(mb)
        mine_pos = find_mines(mb)
        print(mine_pos)

        # how many times given column/row was randomly picked
        col_cnt = [0] * mb.width
        row_cnt = [0] * mb.width

        for i in range(1000):
            mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
            # print(mb)
            self.assertEqual(mb.number_of_mines, 1)

    def test_generate_xxx(self):
        def find_mines(mb: MineBoard, return_only_first: bool = True):
            mines = [(i % mb.width, i // mb.height) for i, m in enumerate(sum(mb.cells, [])) if m.has_mine]
            return None if len(mines) == 0 else mines[0] if return_only_first else mines

        NO_OF_ROWS, NO_OF_COLS = 4, 4

        # how many times given column/row was randomly picked
        col_cnt = [0] * NO_OF_COLS
        row_cnt = [0] * NO_OF_ROWS

        expected_number_of_mines: int = 1
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS, expected_number_of_mines)
        print(mb)
        print(find_mines(mb))
        self.assertEqual(mb.number_of_mines, expected_number_of_mines)


if __name__ == '__main__':
    unittest.main(verbosity=2)
