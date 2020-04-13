import boards
# Test that this git thing actually works
board = boards.board_medium  # initialize grids (board and cells)
cells = [[], [], [], [], [], [], [], [], []]
solved = 0
runs = 0
changed = True


class Cell(object):
    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value
        self.possible = []
        self.box = [int(row / 3) * 3 + 2, int(column / 3) * 3 + 2]  # top left corner of sub-grid

    def calc_possibles(self, grid):  # calculates all possible values for self
        self.possible.clear()
        if self.value == 0:
            for value in range(1, 10):
                self.possible.append(value)
            for cell in grid[self.row]:  # checks row
                if cell in self.possible:
                    self.possible.remove(cell)
            for row in grid:  # checks column
                if row[self.column] in self.possible:
                    self.possible.remove(row[self.column])
            for row in range(self.box[0] - 2, self.box[0] + 1):  # checks sub-grid
                for column in range(self.box[1] - 2, self.box[1] + 1):
                    if grid[row][column] in self.possible:
                        self.possible.remove(grid[row][column])


def create_cells(grid):  # creates cell grid that matches given board
    for row in range(9):
        for column in range(9):
            base_value = grid[row][column]
            cells[row].append(Cell(row, column, base_value))


def print_board():  # prints board in correct order
    for row in cells:
        for cell in row:
            print(cell.value, end=' ')
        print("")


def get_possibles(grid):  # gets possible values for the whole board
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(grid)


def setup(grid):  # sets up grid and prints initial board
    create_cells(grid)
    print_board()


def solve_unique():  # solves cells that instead of having one possible value, have a unique possible value
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


def solve_simples():  # solves cells with only one possible value
    global changed, solved
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(board)
            if len(cells[row][column].possible) == 1:
                cells[row][column].value = cells[row][column].possible[0]
                board[row][column] = cells[row][column].possible[0]
                cells[row][column].possible.clear()
                solved += 1
                changed = True


setup(board)
while changed: # main solving loop that breaks when the board doesn't change
    get_possibles(board)
    solve_unique()
    changed = False
    solve_simples()
    runs += 1

print("\nSolved board: ")
print_board()
print("solved", solved, "cells in", runs, "runs")
