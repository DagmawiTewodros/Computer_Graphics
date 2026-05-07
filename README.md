Name Dagmawi Tewodros  
ID NO UGR/7661/16  
Section 2  
# Maze Generator & Solver

A Python + pygame program that builds and solves a random maze.

## How It Works

**Generation:** A "mouse" starts in a random cell and eats through walls using depth-first search (stack). It always moves to an unvisited neighbour, backtracking when stuck — until every cell is connected.

**Solving:** A second mouse backtracks from entrance to exit. Red dots = current path, blue dots = dead ends.

**Data structure:**
```python
northWall[R][C]  # 1 = wall intact, 0 = open
eastWall[R][C]   # row 0 and col 0 are phantom rows for outer edges
```

## Run

```bash
pip install pygame
python maze.py
```

Press **R** to regenerate a new maze.

## Config

Edit the top of `maze.py` to change `ROWS`, `COLS`, `CELL` (cell size), or `EXTRA_WALLS` (adds cycles).
