import numpy


def _get_unselected_neighbors(arr, selected, passed, cell):
    neighbours = {"up": (cell[0] - 1, cell[1]),
                  "down": (cell[0] + 1, cell[1]),
                  "right": (cell[0], cell[1] + 1),
                  "left": (cell[0], cell[1] - 1)}
    if cell[0] == 0:
        del neighbours["up"]
    if cell[0] == len(arr) - 1:
        del neighbours["down"]
    if cell[1] == 0:
        del neighbours["left"]
    if cell[1] == len(arr) - 1:
        del neighbours["right"]
    unselected = []
    for n in list(neighbours.values()):
        if arr[n[0]][n[1]] == 0 and n not in passed and n not in selected:
            unselected.append(n)
    return unselected


def _is_there_a_way(arr, a, b):
    passed = []
    selected = [a]
    while len(selected) != 0:
        temp = []
        for cell in selected:
            passed.append(cell)
            neighbors = _get_unselected_neighbors(arr, selected, passed, cell)
            for neighbor in neighbors:
                temp.append(neighbor)
        selected = temp
    if b in passed:
        return True
    return False


def is_there_a_way(arr, p1, p2):
    labyrinth = numpy.array(arr)
    for i, line in enumerate(arr):
        for j, el in enumerate(arr[i]):
            if el == 0 or (i == p1[0] and j == p1[1]) \
                    or (i == p2[0] and j == p2[1]):
                labyrinth[i][j] = 0
            else:
                labyrinth[i][j] = 1
    return _is_there_a_way(labyrinth, p1, p2)
