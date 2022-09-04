import unittest
from unittest import TestCase

from model.board import MineBoard


class TestMineBoardExpand(TestCase):

    def test_expand_1(self):
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 2, 2

        mb.plant_mine(x, y)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■▣■■■
        # ■■■■■■

        tmp = mb.uncover(NO_OF_COLS - 1, NO_OF_ROWS - 1)
        print(mb)
        # □□□□□□
        # □111□□
        # □1▣1□□
        # □1■1□□

    def test_expand_1_1(self):
        """
        Uncover right-down corner, which should result in uncovering almost all the board.

        ■■■■■■          □□□□□□
        ■■■■■■   -->    □111□□
        ■■▣■■■          □1▣1□□
        ■■■■■■          □1■1□□
        """
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 2, 2

        mb.plant_mine(x, y)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■▣■■■
        # ■■■■■■

        # uncover right-down corner, which should result in uncovering almost all the board
        tmp = mb.uncover(NO_OF_COLS - 1, NO_OF_ROWS - 1)
        print(mb)
        # □□□□□□
        # □111□□
        # □1▣1□□
        # □1■1□□
        print(tmp)

    def test_expand_1_2(self):
        """
        Uncover top-left corner, which should result in uncovering almost all the board.

        ■■■■■■          □□□□□□
        ■■■■■■   -->    □111□□
        ■■▣■■■          □1▣1□□
        ■■■■■■          □1■1□□
        """
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 2, 2

        mb.plant_mine(x, y)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■▣■■■
        # ■■■■■■

        # uncover top-left corner, which should result in uncovering almost all the board
        tmp = mb.uncover(0, 0)
        print(mb)
        # □□□□□□
        # □111□□
        # □1▣1□□
        # □1■1□□

        print(tmp)

    def test_expand_1_3(self):
        """
        Uncover the cell which is 1-neighbour field (current_no_of_mines == 1),
        and shouldn't cause further expansion.

        ■■■■■■         ■■■■■■
        ■■■■■■   -->   ■■■■■■
        ■■▣■■■         ■■▣■■■
        ■■■■■■         ■■1■■■
        """
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 2, 2

        mb.plant_mine(x, y)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■▣■■■
        # ■■■■■■

        # uncover the cell under the mine, which is 1-neighbour field (current_no_of_mines == 1),
        # and shouldn't cause further expansion
        tmp = mb.uncover(x, y + 1)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■▣■■■
        # ■■1■■■

        self.assertFalse(tmp.has_mine)
        self.assertEqual(tmp.no_adjacent_mines, 1)

    def test_expand_1_4(self):
        """
        Try expand on a mine, which should cause expansion to happen.

        ■■■■■■         ■■■■■■
        ■■■■■■   -->   ■■■■■■
        ■■▣■■■         ■■▣■■■
        ■■■■■■         ■■1■■■
        """
        NO_OF_ROWS, NO_OF_COLS = 4, 6
        mb = MineBoard(NO_OF_COLS, NO_OF_ROWS)
        x, y = 2, 2

        # expand the mine, which should cause expansion to happen
        mb.plant_mine(x, y)
        print(mb)
        # ■■■■■■
        # ■■■■■■
        # ■■M■■■
        # ■■■■■■

        # uncover the mine
        tmp = mb.uncover(x, y)
        print(mb)

        self.assertTrue(tmp.has_mine)
        self.assertEqual(tmp.no_adjacent_mines, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
