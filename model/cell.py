from model import REVEAL_HIDDEN_MINE

# Some Unicode characters that may be useful for showing/debugging the board
# (https://www.fileformat.info/info/unicode/block/geometric_shapes/list.htm):
# U+25A0	BLACK SQUARE (U+25A0)	■
# U+25A1	WHITE SQUARE (U+25A1)	□
# U+25A2	WHITE SQUARE WITH ROUNDED CORNERS (U+25A2)	▢
# U+25A3	WHITE SQUARE CONTAINING BLACK SMALL SQUARE (U+25A3)	▣
EMPTY_CELL = "\u25A1"
HIDDEN_CELL = "\u25A0"
HIDDEN_MINE = "\u25A3"


class Cell:
    def __init__(self, has_mine: bool = False):
        # do the cell hold the mine
        self.has_mine = has_mine

        # how many mines are neighbouring a given cell
        self.no_adjacent_mines: int = 0

        # has the user marked the field as flagged
        self.flagged: bool = False

        # is the cell uncovered (initially all the cells are concealed, then the user uncovers cells one by one)
        self.uncovered: bool = False

    def reveal(self) -> None:
        """
        Update the state of the cell if it gets uncovered.
        :return:
        """
        self.uncovered = True

        # set the other attributes
        self.flagged = False

    def flag(self, on_off: bool) -> None:
        """
        Set the `flagged` attribute.
        :return:
        """

        if self.uncovered:
            raise RuntimeError("Uncovered field cannot be flagged")

        self.flagged = on_off

    # for debugging purposes right now
    #
    def get_representation(self, reveal_hidden_mine: bool = False):
        """
        First attempt. Probably needs to be fixed.
        :return:
        """
        if not self.uncovered:
            # TODO: for now you deliberately omit Flag representation
            # value = "F" if self.flagged ...

            value = HIDDEN_CELL
            if self.has_mine and reveal_hidden_mine:
                value = HIDDEN_MINE
        else:
            if self.has_mine:
                value = "M"
            else:
                value = str(self.no_adjacent_mines) if self.no_adjacent_mines > 0 else EMPTY_CELL
        return value

    # for debugging purposes right now
    #
    def get_debug_representation(self):
        def shorten(b: bool) -> str:
            return "T" if b else "F"

        return f"[{shorten(self.has_mine)}{self.no_adjacent_mines}{shorten(self.flagged)}{shorten(self.uncovered)}]"

    def __str__(self):
        return self.get_representation(reveal_hidden_mine=REVEAL_HIDDEN_MINE)

    def __repr__(self):
        return self.get_debug_representation()
