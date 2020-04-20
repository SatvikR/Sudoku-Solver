import boards
import backtrack

board = boards.board_hard_1  # initialize grids (board and cells)
cells = [[], [], [], [], [], [], [], [], []]
pairs = [[num1, num2] for num1 in range(1, 9) for num2 in range(num1 + 1, 10)]
solved = 0
runs = 0
changed = True
solved_with_unique = 0
solved_simple = 0
finished = False
pair_counter = 0
current_values = []
solved_values = []
unsolved = []


class Cell(object):
    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value
        self.possible = []
        self.box = [int(row / 3) * 3 + 2, int(column / 3) * 3 + 2]  # top left corner of sub-grid
        self.not_possible = []

    def calc_possibles(self, grid):  # calculates all possible values for self
        self.possible.clear()
        if self.value == 0:
            for value in range(1, 10):
                self.possible.append(value)
            for value in self.not_possible:
                self.possible.remove(value)
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
    for row in board:
        for cell in row:
            print(cell, end=' ')
        print("")


def get_possibles(grid):  # gets possible values for the whole board
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(grid)


def setup(grid):  # sets up grid and prints initial board
    create_cells(grid)
    print_board()


def solve_unique_sub():  # solves unique possibles in each sub-grid
    global solved, solved_with_unique, changed
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
                    cells[found_row][found_col].value = num
                    board[found_row][found_col] = cells[found_row][found_col].value
                    solved += 1
                    current_values.append(cells[found_row][found_col])
                    solved_with_unique += 1
                    changed = True


def solve_unique_row():  # solves unique possibles in each row
    global solved, solved_with_unique, changed
    found_row = 0
    found_col = 0
    for row in range(9):
        for num in range(1, 10):
            count = 0
            for col in range(9):
                if num in cells[row][col].possible:
                    count += 1
                    found_row = row
                    found_col = col
            if count == 1:
                cells[found_row][found_col].value = num
                board[found_row][found_col] = num
                solved += 1
                current_values.append(cells[found_row][found_col])
                solved_with_unique += 1
                changed = True


def solve_unique_column():  # solves unique possibles in each column
    global solved, solved_with_unique, changed
    found_row = 0
    found_col = 0
    for col in range(9):
        for num in range(1, 10):
            count = 0
            for row in range(9):
                if num in cells[row][col]:
                    found_row = row
                    found_col = col
                    count += 1
            if count == 1:
                cells[found_row][found_col].value = num
                board[found_row][found_col] = num
                solved += 1
                current_values.append(cells[found_row][found_col])
                solved_with_unique += 1
                changed = True


def solve_uniques():
    get_possibles(board)
    solve_unique_sub()
    get_possibles(board)
    solve_unique_row()


def solve_simples():  # solves cells with only one possible value
    global changed, solved, solved_simple
    for row in range(9):
        for column in range(9):
            cells[row][column].calc_possibles(board)
            if len(cells[row][column].possible) == 1:
                cells[row][column].value = cells[row][column].possible[0]
                board[row][column] = cells[row][column].possible[0]
                cells[row][column].possible.clear()
                solved += 1
                current_values.append(cells[row][column])
                changed = True
                solved_simple += 1


def solve_col_pairs():
    global changed, pairs, board, cells, pair_counter
    found_rows = []
    found_cols = []
    for col in range(9):
        for pair in pairs:
            count = 0
            found_rows.clear()
            found_cols.clear()
            for row in range(9):
                if pair == cells[row][col].possible:
                    count += 1
                    found_rows.append(row)
                    found_cols.append(col)
            if count == 2:
                pair_counter += 1
                for row in range(9):
                    for num in pair:
                        if row in found_rows:
                            continue
                        else:
                            if num not in cells[row][col].not_possible:
                                cells[row][col].not_possible.append(num)


def solve_sub_pairs():
    global changed, pairs, board, cells, pair_counter
    found_rows = []
    found_cols = []
    for g_row in range(3):
        for g_col in range(3):
            for pair in pairs:
                count = 0
                found_rows.clear()
                found_cols.clear()
                for row in range(3):
                    for col in range(3):
                        if pair == cells[g_row * 3 + row][g_col * 3 + col].possible:
                            count += 1
                            found_rows.append(g_row * 3 + row)
                            found_cols.append(g_col * 3 + col)
                if count == 2:
                    pair_counter += 1
                    changed = True
                    for row in range(3):
                        for col in range(3):
                            for num in pair:
                                if (g_row * 3 + row in found_rows) and (g_col * 3 + col in found_cols):
                                    continue
                                else:
                                    if num not in cells[g_row * 3 + row][g_col * 3 + col].not_possible:
                                        cells[g_row * 3 + row][g_col * 3 + col].not_possible.append(num)


def solve_row_pairs():
    global changed, pairs, board, cells, pair_counter
    found_rows = []
    found_cols = []
    for row in range(9):
        for pair in pairs:
            count = 0
            found_rows.clear()
            found_cols.clear()
            for col in range(9):
                if pair == cells[row][col].possible:
                    count += 1
                    found_rows.append(row)
                    found_cols.append(col)
            if count == 2:
                pair_counter += 1
                for col in range(9):
                    for num in pair:
                        if col in found_cols:
                            continue
                        else:
                            if num not in cells[row][col].not_possible:
                                cells[row][col].not_possible.append(num)

def get_unsolved():
    for row in range(9):
        for col in range(9):
            if cells[row][col].value == 0:
                unsolved.append(cells[row][col])

def get_new():
    for row in range(9):
        for col in range(9):
            if cells[row][col] in unsolved:
                cells[row][col].value = board[row][col]
                current_values.append(cells[row][col])

def main():
    global runs, board, changed, finished, solved_values
    setup(board)
    unchanged_runs = 0
    while (unchanged_runs < 3):  # main solving loop that breaks when the board doesn't change
        solved_temp = solved
        solve_col_pairs()
        solve_sub_pairs()
        solve_row_pairs()
        changed = False
        solve_uniques()
        solve_simples()
        if solved_temp == solved:
            unchanged_runs += 1
            if unchanged_runs == 3:
                get_unsolved()
                backtrack.solve_sudoku(board)
                get_new()
                solved_values.append([num for num in current_values])
                current_values.clear()
        else:
            runs += 1
            solved_values.append([num for num in current_values])
            current_values.clear()

    print("\nSolved board: ")
    print_board()
    print("solved %d cells in %d runs" % (solved, runs))
    print("solved %d cells using unique func" % solved_with_unique)
    print("solved %d cells using simple func" % solved_simple)
    print("Found %d pairs" % pair_counter)
    finished = True
    print_board()