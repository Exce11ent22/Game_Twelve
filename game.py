from random import randint, shuffle
from find_path import is_there_a_way


class Cell:

    def __init__(self, i, j, value):
        self.i = i
        self.j = j
        self.value = value


class Game:

    def __init__(self):
        self._table = [[0 for j in range(5)] for i in range(5)]
        self._score = 0
        self._selected_cell = None
        self._is_won = False
        self.spawn_cell(3)
        self._table = [[j + i * 5 for j in range(5)] for i in range(5)]

    def set_new_game(self, num_of_el=3):
        self._table = [[0 for j in range(5)] for i in range(5)]
        self._is_won = False
        self._score = 0
        self.spawn_cell(num_of_el)

    def get_table(self):
        return self._table

    def get_score(self):
        return self._score

    def _add_cells(self, c1: Cell, c2: Cell):
        if c2.value == 0:
            self._table[c2.i][c2.j] += self._table[c1.i][c1.j]
            self._table[c1.i][c1.j] = 0
            self.spawn_cell(2)
        else:
            self._table[c2.i][c2.j] += 1
            self._table[c1.i][c1.j] = 0
            self.spawn_cell(1)
            self._score += self._table[c2.i][c2.j]

    def is_selected(self, i, j):
        if self._selected_cell is None:
            return False
        if self._selected_cell.i == i and self._selected_cell.j == j:
            return True
        return False

    def select_cell(self, i, j):
        if self._selected_cell is not None:
            if self._selected_cell.i == i and self._selected_cell.j == j:
                self._selected_cell = None

            elif self._selected_cell.value == self._table[i][j] or self._table[i][j] == 0:
                if is_there_a_way(self._table, (self._selected_cell.i, self._selected_cell.j), (i, j)):
                    self._add_cells(self._selected_cell, Cell(i, j, self._table[i][j]))
                    self._selected_cell = None

        else:
            if self._table[i][j] != 0:
                self._selected_cell = Cell(i, j, self._table[i][j])

    def spawn_cell(self, amount):
        to_spawn = [1, 1, 1, 1, 1, 1, 2, 2, 3]
        none_cells = [(i, j) for i in range(len(self._table))
                      for j in range(len(self._table[0]))
                      if self._table[i][j] == 0]

        amount = len(none_cells) if len(none_cells) < amount else amount
        shuffle(none_cells)
        none_cells = none_cells[:amount]

        for i in range(len(none_cells)):
            self._table[none_cells[i][0]][none_cells[i][1]] = to_spawn[randint(0, len(to_spawn) - 1)]

    def is_win(self):
        max_cell = max(max(self._table))
        if max_cell >= 12 and not self._is_won:
            self._is_won = not self._is_won
            return True
        return False

    def _get_neighbors(self, i, j):
        neighbors = {"up": (i - 1, j),
                     "down": (i + 1, j),
                     "right": (i, j + 1),
                     "left": (i, j - 1)}
        if i == 0:
            del neighbors["up"]
        if i == len(self._table) - 1:
            del neighbors["down"]
        if j == 0:
            del neighbors["left"]
        if j == len(self._table) - 1:
            del neighbors["right"]
        return list(neighbors.values())

    def is_lose(self):
        cells = set([el for row in self._table for el in row])
        if 0 in cells:
            return False

        for i in range(len(self._table)):
            for j in range(len(self._table[0])):
                for neighbor in self._get_neighbors(i, j):
                    if self._table[i][j] == self._table[neighbor[0]][neighbor[1]]:
                        return False
        return True
