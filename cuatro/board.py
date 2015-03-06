from fields import *

import texttable


class Board:

    col_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}

    def __init__(self):
        self.matrix = [[FullHouse(), ThreeOfAKind(), FourOfAKind(), Straight(), One, ThreeOfAKind()],
                       [Straight(), Six, ThreeOfAKind(), FullHouse(), Yahtzee(), FourOfAKind()],
                       [FourOfAKind(), FullHouse(), Yahtzee(), Straight(), ThreeOfAKind(), Three],
                       [FullHouse(), Straight(), Five, FourOfAKind(), FullHouse(), ThreeOfAKind()],
                       [Two, Yahtzee(), FullHouse(), ThreeOfAKind(), FourOfAKind(), Straight()],
                       [ThreeOfAKind(), FourOfAKind(), Straight(), Four, Straight(), FullHouse()]
                      ]
        self.size = len(self.matrix)

    def place(self, loc, player, dice):
        row, col = self._parse_location(loc)
        field = self.matrix[row][col]
        return field.place(player, dice)

    def _parse_location(self, loc):
        a, b = loc[0], loc[1]
        if b.isdigit():
            a, b = b, a
        return int(a), self.col_map[b]

    def _four_in_a_row_fields(self, fields):
        count = 0
        last = None
        for field in fields:
            if field.player is None:
                count = 0
            elif field.player == last or last is None:
                count += 1
                last = field.player
            if count == 4:
                return True
        return False

    def four_in_a_row(self):
        # check rows
        for fields in self._rows():
            if self._four_in_a_row_fields(fields):
                return True
        # check cols
        for fields in self._cols():
            if self._four_in_a_row_fields(fields):
                return True
        # check diagonals 1
        for fields in self._diagonals():
            if len(fields) >= 4 and self._four_in_a_row_fields(fields):
                return True
        return False


    def _cols(self):
        for col in range(self.size):
            yield [row[col] for row in self.matrix]

    def _rows(self):
        for row in self.matrix:
            yield row

    def _diagonals(self):
        n = self.size
        for y in range(self.size * 2 - 1):
            yield [self.matrix[y - x][x] for x in range(n) if 0 <= y - x < n]
            yield [self.matrix[y + x - n + 1][x] for x in range(n) if 0 <= y + x - n +1 < n]

    def __repr__(self):
        table = texttable.Texttable(max_width=120)
        table.set_cols_align(["c"] * (self.size + 1))
        table.add_row(["", "A", "B", "C", "D", "E", "F"])
        for num, row in enumerate(self.matrix):
            items = [num]
            for field in row:
                if field.player is None:
                    player_str = "-"
                else:
                    player_str = field.player.name
                items.append("%s\n\n%s\n%i" % (field.name, player_str, field.height))
            table.add_row(items)
        return table.draw()
