board1 = [[3, 0, 0, 6, 0, 7, 0, 9, 0],
          [0, 0, 9, 5, 0, 1, 8, 0, 7],
          [0, 0, 6, 0, 9, 0, 2, 3, 5],
          [1, 2, 3, 4, 0, 6, 7, 8, 9],
          [8, 9, 0, 7, 1, 0, 0, 0, 0],
          [0, 0, 4, 3, 0, 9, 1, 5, 0],
          [4, 6, 1, 0, 0, 0, 5, 0, 8],
          [0, 3, 0, 2, 6, 0, 9, 1, 0],
          [0, 0, 2, 1, 0, 0, 3, 0, 6]]
board = [[7, 9, 0, 2, 0, 0, 0, 0, 0],
         [0, 0, 3, 9, 5, 4, 6, 8, 7],
         [4, 6, 8, 3, 1, 7, 9, 5, 0],
         [0, 5, 0, 8, 0, 2, 0, 1, 6],
         [9, 7, 0, 0, 0, 6, 5, 3, 8],
         [0, 0, 1, 0, 0, 0, 2, 0, 4],
         [0, 4, 0, 6, 2, 3, 0, 7, 1],
         [0, 1, 0, 0, 0, 0, 3, 2, 5],
         [2, 3, 0, 0, 8, 1, 4, 0, 9]]
cells = [[], [], [], [], [], [], [], [], []]
corners = [3, 6, 9]


def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


class Cell(object):
    def __init__(self, row, column, value):
        global corners
        self.row = row
        self.column = column
        self.value = value
        self.possible = []
        self.box = [closest(corners, self.row) - 1, closest(corners, self.column) - 1]

    def calc_possibles(self, grid):
        self.possible.clear()
        if self.value == 0:
            for value in range(1, 10):
                self.possible.append(value)
            for cell in grid[self.row]:
                if cell in self.possible:
                    self.possible.remove(cell)
            for row in grid:
                if row[self.column] in self.possible:
                    self.possible.remove(row[self.column])
            for row in range(self.box[0] - 2, self.box[0] + 1):
                for column in range(self.box[1] - 2, self.box[1] + 1):
                    if grid[row][column] in self.possible:
                        self.possible.remove(grid[row][column])


def create_cells(grid):
    for row in range(9):
        for column in range(9):
            base_value = grid[row][column]
            cells[row].append(Cell(row, column, base_value))


def get_possibles(grid):
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(grid)


create_cells(board)
for row in cells:
    for cell in row:
        print(cell.value, end=' ')
    print("")

solved = 0
runs = 0
while True:
    if runs > 500:
        break
    # get_possibles(board)
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(board)
            if len(cells[row][column].possible) == 1:
                cells[row][column].value = cells[row][column].possible[0]
                board[row][column] = cells[row][column].possible[0]
                cells[row][column].possible.clear()
                solved += 1
    runs += 1

print("\n \n \n")
for row in cells:
    for cell in row:
        print(cell.value, end=' ')
    print("")
print(solved)
cells[0][8].calc_possibles(board)
print(cells[0][8].possible)
