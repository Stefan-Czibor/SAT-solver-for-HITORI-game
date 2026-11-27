# SAT-solver-for-HITORI-game
School project at the Charles University, Matfyz

## Documentation

### Problem description
Hitori is a logic puzzle similar to Sudoku. Initially, you are given an $n \times n$ grid where every cell contains a number. The game is played by eliminating (blacking out) squares, so in the end the grid satisfies the following rules:
- no row or column can have more than one occurrence of any given number
- black cells cannot be horizontally or vertically adjacent, although they can be diagonal to one another.
- the remaining numbered cells must be all connected to each other, horizontally or vertically.

More information about the game can be found [online](https://en.wikipedia.org/wiki/Hitori)

An example of a valid input format is:
```
1 2 2
3 3 1
3 1 1
```
where each number represents the value of a cell in the grid. Note that there must be the same number of elements in each row and column.

One of the valid solutions for the instance above is:
```
1 2 #
# 3 1
3 1 #
```
where `#` means that the given cell is blacked out.

### Encoding
Let $C = \{(i, j) \mid 0 \le i, j < n\}$ be the set of cells in the $n \times n$ grid and the number inside them $a_{i, j}$ the number written in cell $(i, j)$
The problem is encoded using two sets of variables:
- $White(i, j)$ means that cell $(i, j)$ is white. If $White(i, j)$ is false the cell is black.
- $Level(i, j, l)$ represents whether the cell (i, j) is on a level $l$ where $l = 0, ... max\_level$ and $max\_level = n^2 - 1$

Each variable is an integer
- $White(i, j)$ has ID's $1 \dots n^2$
- $Level(i, j, l)$ has ID's $n^2 + 1 \dots n^2 \cdot(max\_level + 1)$ $\equiv$ $n^2 + 1 \dots n^2 \cdot(n^2 + 1)$

#### Rules
- **One number in each row and column:**
$\forall i, j, k \in \{1 \dots \}, j \ne k: a_{i, j} = a_{i, k} \implies (\neg White(i, j) \lor \neg White(i, k))
\land a_{j, i} = a_{k, i} \implies (\neg White(j, i) \lor \neg White(k, i))$