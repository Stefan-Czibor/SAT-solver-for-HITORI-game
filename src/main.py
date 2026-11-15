from argparse import ArgumentParser
import subprocess

def load_instance(file_name):
    grid = []   # 2D matrix to store the table

    with open(file_name, "r") as file:
        first_line = list(map(int, file.readline().split()))
        grid.append(first_line)
        # based on the quantity of the numbers in the first line we know how many more are coming
        grid_size = len(first_line)

        for _ in range(grid_size - 1):      # read the remaining rows of the table
            line = list(map(int, file.readline().split()))
            grid.append(line)

        return grid, grid_size

def encode(grid_size, instance):
    cnf = []

    cnf.append(neighbour_rule(grid_size))
    cnf.append(occurrence_rule(grid_size, instance))


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

# TODO: 
def continued_graph_rule():
    continued_graph_cnf = []
    return continued_graph_cnf

def occurrence_rule(grid_size, instance):
    # Rule: no row or column can have more than 1 white occurrence of a number
    # There is at most one white occurrence of a number on all axises

    occurrence_cnf = []

    # Check the row
    for i in range(grid_size):
        for j in range(grid_size):
            # now for each element we have to check the other ones in the row
            for k in range(grid_size):            
                if j != k and instance[i][j] == instance[i][k]:
                    occurrence_cnf.append([-assign_ID2pos(grid_size, i, j), -assign_ID2pos(grid_size, i, k), 0])

    # Check the column
    for i in range(grid_size):
        for j in range(grid_size):
            # now for each element we have to check the other ones in the column
            for k in range(grid_size):            
                if i != k and instance[i][j] == instance[k][j]:
                    occurrence_cnf.append([-assign_ID2pos(grid_size, i, j), -assign_ID2pos(grid_size, k, j), 0])

    return occurrence_cnf

def call_solver(cnf, output_name, variable_quantity, clause_quantity, solver_name, verbosity):
    # prints CNF into formula.cnf file then calls the glucose solver on it

    with open(output_name, 'w') as file:
        file.write("p cnf ", str(variable_quantity), str(clause_quantity) + "\n")
        for clause in cnf:
            file.write(" ".join(map(str, clause)) + "\n")

    # ./solver_name         ... we gonna use the glucose-syrup
    # -model                ... prints out at the an actual working model
    # -verb                 ... the verbosity of the SAT solver {0, 1, 2}
    # output_name           ... name of the .cnf file that we give to the solver
    # stdout=subprocess.PIE ... saves the output so we can process it later
    return subprocess.run(["./" + solver_name, "model", "-verb=", str(verbosity), output_name], stdout=subprocess.PIPE)

        

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

    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help="Output file for the DIMACS format (i.e. the CNF formula)."
    )

    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help="The SAT solver we are about to use."
    )

    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        help="Verbosity of the SAT solver used."
    )

    arguments = parser.parse_args()

    # the input grid that we read from the file
    grid, grid_size = load_instance(arguments.input)

    cnf = encode(grid_size, grid)

    print(len(cnf), "clause")
    for x in cnf:
        print(x)