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

        return grid

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
    grid = load_instance(arguments.input)
    print(grid)