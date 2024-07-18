# Sudoku Solver using Linear Programming

This repository contains a Python implementation of a Sudoku solver using Linear Programming (LP). The solver can handle Sudoku puzzles of varying difficulties and can find multiple solutions if they exist.

## Features

- Solves 9x9 Sudoku puzzles
- Utilizes Linear Programming for efficient solving
- Can find all possible solutions for a given puzzle
- Includes a function to fetch Sudoku puzzles from the New York Times website

## Requirements

- Python 3.x
- PuLP library (`pip install pulp`)
- Requests library (`pip install requests`)

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/choppystick/py-sudoku-solver
   cd sudoku-solver-lp
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Run the solver:
   ```
   python sudoku_solver.py
   ```

By default, the script will fetch a "hard" difficulty Sudoku puzzle from the New York Times website and solve it, displaying all possible solutions.

## How It Works

The Sudoku solver uses Linear Programming to model the Sudoku puzzle as a constraint satisfaction problem. Here's a deep dive into how LP works in this context:

### Linear Programming in Sudoku Solving

Linear Programming is a mathematical optimization technique used to find the best outcome in a mathematical model whose requirements are represented by linear relationships. In the context of Sudoku, we're not trying to optimize anything, but rather find a feasible solution that satisfies all the constraints of the puzzle.

1. **Variables**: We create binary variables `x[i,j,k]` for each cell (i,j) and possible value k (1-9). If `x[i,j,k] = 1`, it means the value k is placed in cell (i,j).

2. **Constraints**: The Sudoku rules are modeled as linear constraints:
   - Each cell must have exactly one value: `∑k x[i,j,k] = 1` for each (i,j)
   - Each row must contain each number once: `∑j x[i,j,k] = 1` for each i and k
   - Each column must contain each number once: `∑i x[i,j,k] = 1` for each j and k
   - Each 3x3 box must contain each number once: `∑(i,j in box) x[i,j,k] = 1` for each box and k
   - Pre-filled cells: If cell (i,j) is given as value m, then `x[i,j,m] = 1`

3. **Objective Function**: In this case, we don't need to optimize anything, so we set a dummy objective function of 0.

4. **Solving**: We use the PuLP library to model and solve the LP problem. PuLP translates our model into a format that can be solved by various LP solvers.

5. **Solution Interpretation**: After solving, we interpret the results. If `x[i,j,k] = 1` in the solution, we place value k in cell (i,j) of our Sudoku grid.

6. **Multiple Solutions**: To find all solutions, we add a constraint after each solution is found that forces at least one change in the next solution.

This approach is effective for Sudoku because:
- It naturally expresses the logical constraints of Sudoku.
- LP solvers are highly optimized and can quickly find solutions to large systems of linear equations and inequalities.
- It guarantees finding a solution if one exists, or proving no solution exists if the puzzle is unsolvable.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
