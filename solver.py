import boards
board = boards.board_medium
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
        # self.box = [closest(corners, self.row) - 1, closest(corners, self.column) - 1]
        self.box = [int(row / 3) * 3 + 2, int(column / 3) * 3 + 2]

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
            print(" ")


def create_cells(grid):
    for row in range(9):
        for column in range(9):
            base_value = grid[row][column]
            cells[row].append(Cell(row, column, base_value))


def print_board():
    for row in cells:
        for cell in row:
            print(cell.value, end=' ')
        print("")


def get_possibles(grid):
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(grid)


create_cells(board)
for row in cells:
    for cell in row:
        print(cell.value, end=' ')
    print("")


def solve_unique():
    global board, cells
    count = 0
    found_row = 0
    found_col = 0
    for g_row in range(3):
        for g_col in range(3):
            for num in range(1, 10):
                count = 0
                for row in range(3):
                    for col in range(3):
                        if num in cells[g_row * 3 + row][g_col * 3 + col].possible:
                            count += 1
                            found_row = g_row * 3 + row
                            found_col = g_col * 3 + col
                if count == 1:
                    cells[found_row][found_col].possible = [num]
                    cells[found_row][found_col].value = num
                    board[found_row][found_col] = cells[found_row][found_col].value


solved = 0
runs = 0
changed = True
while changed:
    # get_possibles(board)
    get_possibles(board)
    solve_unique()
    changed = False
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(board)
            if len(cells[row][column].possible) == 1:
                cells[row][column].value = cells[row][column].possible[0]
                board[row][column] = cells[row][column].possible[0]
                cells[row][column].possible.clear()
                solved += 1
                changed = True

    runs += 1

print("\n \n \n")
for row in cells:
    for cell in row:
        print(cell.value, end=' ')
    print("")
print(solved)
print(runs)
cells[0][8].calc_possibles(board)
print(cells[0][8].possible)
