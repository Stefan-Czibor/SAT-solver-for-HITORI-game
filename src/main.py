from argparse import ArgumentParser

def load_instance(file_name):
    grid = []   # 2D matrix to store the table

    with open(file_name, "r") as file:
        first_line = list(map(int, file.readline().split()))
        grid.append(first_line)
        # based on the quantity of the numbers in the first line we know how many more are coming
        GRID_SIZE = len(first_line)

        for _ in range(GRID_SIZE - 1):      # read the remaining rows of the table
            line = list(map(int, file.readline().split()))
            grid.append(line)

        return grid, GRID_SIZE

def encode(grid_size):
    cnf = []

    cnf.append(neighbour_rule(grid_size))

    return cnf

def neighbour_rule(grid_size):
    # Rule: black cells can't be vertically nor horizantally adjacent

    neighbour_cnf = []

    for i in range(grid_size):
        for j in range(grid_size):

            # Check if they are in range
            if (i + 1 < grid_size):
                # Horizontal neighbour
                neighbour_cnf.append([assign_ID2pos(grid_size, i, j), assign_ID2pos(grid_size, i+1, j), 0])

            if (j + 1 < grid_size):
                # Vertical neighbour
                neighbour_cnf.append([assign_ID2pos(grid_size, i, j), assign_ID2pos(grid_size, i, j+1), 0])

    return neighbour_cnf

def assign_ID2pos(grid_size, row_idx, col_idx):
    return grid_size * row_idx + col_idx + 1

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="instances/input-1.in",
        type=str,
        help="The instance file."
    )

    arguments = parser.parse_args()

    # the input grid that we read from the file
    grid, GRID_SIZE = load_instance(arguments.input)
    print(grid)