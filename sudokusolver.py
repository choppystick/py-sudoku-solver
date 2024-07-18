from pulp import *
import json
import re
import requests

# CONSTANTS (ASSUMING A 9x9 SUDOKU BOARD)
VALS = ROWS = COLS = range(1, 10)

# example of what a valid sudoku input should look like
EXAMPLE = [[2, 5, 0, 7, 0, 9, 0, 0, 0],
           [0, 0, 0, 5, 0, 0, 0, 0, 0],
           [0, 9, 7, 0, 0, 3, 1, 0, 5],
           [0, 0, 0, 0, 0, 0, 0, 9, 3],
           [0, 0, 0, 0, 3, 0, 0, 0, 6],
           [0, 8, 0, 0, 0, 0, 7, 0, 2],
           [6, 0, 0, 0, 0, 0, 4, 0, 0],
           [4, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 4, 0, 2, 0, 0, 0]]


# difficulty is easy, medium, or hard. Basically a sudoku scrapper from NYT. I don't think you should run this too
# many times, JIC.
def get_sudoku_board(difficulty):
    url = f"https://www.nytimes.com/puzzles/sudoku/{difficulty}"
    if difficulty not in ["easy", "medium", "hard"]:
        print("No.")
        return

    response = requests.get(url)
    pattern = (r'<script type="text\/javascript">window\.gameData = (.+)<\/script><\/div><div '
               r'id="portal-editorial-content">')
    match = re.search(pattern, response.text)

    if match:
        data = json.loads(match.group(1))

        puzzle = data[difficulty]['puzzle_data']['puzzle']
        board = [puzzle[i:i + 9] for i in range(0, len(puzzle), 9)]

        return board


# Board: A 2D array of a valid sudoku board format. See above.
# solveall: Find every single valid solve if possible.
def sudoku_solver(board, solveall: bool):
    BOXES = []

    for i in range(3):
        for j in range(3):
            BOXES += [[(ROWS[3 * i + k], COLS[3 * j + l]) for k in range(3) for l in range(3)]]
    # this creates a sudoku puzzle where each tuple corresponds to the coordinate of a grid in the sudoku, and nested
    # arrays where the inner arrays correspond to the 9 different boxes

    prob = LpProblem("Sudoku_Solver")
    prob.setObjective(lpSum(0))  # set objective function as 0 because we are not minimizing or maximizing

    # we set up the constraints here

    # There are five constraints we need to set up:
    # WITHIN A GRID: there can only be one value within a grid (at the coordinate (i,j))
    # WITHIN A ROW: the range of values are 1-9 without any duplicates within a col for all cols and values
    # i.e. a row must contain each numbers without duplicates

    # WITHIN A COL: the range of values are 1-9 without any duplicates within a row for all rows and values
    # i.e. a column must contain each numbers without duplicates

    # WITHIN A BOX: the range of values are 1-9 without any duplicates within a box
    # i.e. a box must contain each numbers without duplicates

    # VALUES ALREADY GIVEN: if a values are already given, we have to set x_i_j_k = 1 for a given k at (i,j)

    # To model the constraints, what we can do is create a dummy variable x_i_j_k. (i,j) represents the index of the
    # row and col, k represents the values to be taken on the grid. For example, x_2_1_3 represents at (2,1),
    # the value is 3.
    # We set x_i_j_k to be a binary variable, where if k in (i,j) then x_i_j_k = 1, if not, then 0.

    # By our constraint, the sum of x_i_j_k of every row (over all columns and points), column (over all rows
    # and points), grid (over all rows and columns), or box (over all boxes and points) should be 1.
    dummy = LpVariable.dicts("dummy", (VALS, ROWS, COLS), lowBound=0, upBound=1, cat="Integer")

    # CONSTRAINT PER GRID
    for row in ROWS:
        for col in COLS:
            prob += lpSum([dummy[val][row][col] for val in VALS]) == 1, ""

    # ONLY ONE VALUE PER *
    for val in VALS:
        # ROWS
        for row in ROWS:
            prob += lpSum([dummy[val][row][col] for col in COLS]) == 1, ""

        # COLS
        for col in COLS:
            prob += lpSum([dummy[val][row][col] for row in ROWS]) == 1, ""

        # BOXES
        for box in BOXES:
            prob += lpSum([dummy[val][row][col] for (row, col) in box]) == 1, ""

    # CONSTRAINT GIVEN INPUT SUDOKU
    for rows in range(len(board)):
        for cols in range(len(board[rows])):
            if board[rows][cols] != 0:  # We set 0 to represent an empty grid
                prob += dummy[board[rows][cols]][rows + 1][cols + 1] == 1, ""

    prob.writeLP("Sudoku.lp")

    while True:
        prob.solve()
        print("Status:", LpStatus[prob.status])
        if LpStatus[prob.status] == "Optimal":
            for row in ROWS:
                print("\n", end="\n|  ")
                for col in COLS:
                    for val in VALS:
                        if value(dummy[val][row][col]) == 1:
                            num_end = "  |  " if col % 3 == 0 else "   "
                            print(val, end=num_end)

                if row % 3 == 0:
                    print("\n\n+ ----------- + ----------- + ----------- +", end="")

            if solveall:
                prob += lpSum([dummy[val][row][col] for val in VALS
                               for row in ROWS
                               for col in COLS
                               if value(dummy[val][row][col]) == 1]) <= 80
                # create a constraint that more than one value must be different so the LP get a different feasible
                # solution within the feasible solution space

            else:
                break

        else:
            break


def main():
    board = get_sudoku_board("hard")
    sudoku_solver(board, solveall=True)


if __name__ == '__main__':
    main()
