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