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

    largest_atomic_formula = 0

    cnf.extend(neighbour_rule(grid_size))
    cnf.extend(occurrence_rule(grid_size, instance))
    cnf.extend(continued_graph_rule(grid_size))

    for clause in cnf:
        for literal in clause:
            largest_atomic_formula = max(largest_atomic_formula, abs(literal))

    return cnf, largest_atomic_formula


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


def continued_graph_rule(grid_size):
    continued_graph_cnf = []
    cells = []

    for i in range(grid_size):
        for j in range(grid_size):
            cells.append((i, j))

    cell_count = len(cells)
    max_level = grid_size * grid_size -1

    continued_graph_cnf.extend(at_least_one_on_level_0_sub_rule(grid_size, cells))
    continued_graph_cnf.extend(at_most_one_on_level_0_sub_rule(grid_size, cells, cell_count))
    
    for i, j in cells:
        continued_graph_cnf.extend(only_white_cells_have_level_sub_rule(grid_size, max_level, i, j))
        continued_graph_cnf.extend(white_cells_have_min_1_level_sub_rule(grid_size, max_level, i, j))
        continued_graph_cnf.extend(neighbour_sub_rule(grid_size, max_level, i, j))

    return continued_graph_cnf  

def neighbour_sub_rule(grid_size, max_level, i, j):
    # Sub-rule: cell on level l = 1, ..., max_level; has a neighbour on level l-1.

    neighbours = []
    dx = [1, -1, 0, 0]
    dy = [0, 0, -1, 1]

    for k in range(len(dx)):
        new_x = i + dx[k]
        new_y = j + dy[k]

        if (0 <= new_x < grid_size and 0 <= new_y < grid_size):
            neighbours.append((new_x, new_y))

    clauses = []
    for l in range(1, max_level + 1):
        clause = [-assign_ID2level(grid_size, i, j, l)]

        for x, y in neighbours:
            clause.append(assign_ID2level(grid_size, x, y, l - 1))
        clause.append(0)

        clauses.append(clause)

    return clauses

def white_cells_have_min_1_level_sub_rule(grid_size, max_level, i, j):
    # Sub-rule: All white cells have a level
    clause = [-assign_ID2pos(grid_size, i, j)]

    for l in range(max_level + 1):
        clause.append(assign_ID2level(grid_size, i, j, l))
    clause.append(0)

    return [clause]

def only_white_cells_have_level_sub_rule(grid_size, max_level, i, j):
    # Sub-rule: Only white cells can be on a level

    clauses = []
    for l in range(max_level + 1):
        clauses.append([-assign_ID2level(grid_size, i, j, l), assign_ID2pos(grid_size, i, j), 0])

    return clauses

def at_least_one_on_level_0_sub_rule(grid_size, cells):
    # Sub-rule: At least one cell is on level 0.
        clause = []
        for i, j in cells:
            clause.append(assign_ID2level(grid_size, i, j, 0))
        clause.append(0)

        return [clause]

def at_most_one_on_level_0_sub_rule(grid_size, cells, cell_count):
    # Sub-rule: At most one cell is on level 0.
    # for each (x, y) cell pair ~x OR ~y

    clauses = []

    for x in range(cell_count):
        for y in range(cell_count):
            if x == y:
                continue

            ix, jx = cells[x]
            iy, jy = cells[y]
            clauses.append([-assign_ID2level(grid_size, ix, jx, 0), -assign_ID2level(grid_size, iy, jy, 0), 0])

    return clauses



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


def call_solver(cnf, variable_quantity, clause_quantity, verbosity, solver_name, output_name):
    # prints CNF into formula.cnf file then calls the glucose solver on it

    with open(output_name, 'w') as file:
        file.write("p cnf " + str(variable_quantity) + " " + str(clause_quantity) + "\n")
        for clause in cnf:
            file.write(" ".join(map(str, clause)) + "\n")

    # ./solver_name         ... we gonna use the glucose-syrup
    # -model                ... prints out at the an actual working model
    # -verb                 ... the verbosity of the SAT solver {0, 1, 2}
    # output_name           ... name of the .cnf file that we give to the solver
    # stdout=subprocess.PIE ... saves the output so we can process it later
    return subprocess.run(["./" + solver_name, "-model", "-verb=" + str(verbosity), output_name], stdout=subprocess.PIPE)


# assigns an int ID to each: cell c is on l level
# It starts on grid_size^2 + 1 as the assign_pos 
# already took 0, ..., grid_size^2
def assign_ID2level(grid_size, row_idx, col_idx, level):
    return assign_ID2pos(grid_size, row_idx, col_idx) + (level + 1) * grid_size * grid_size
        

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

    cnf, literal_count = encode(grid_size, grid)

    result = call_solver(cnf, literal_count, len(cnf), arguments.verb, arguments.solver, arguments.output)

    print(result.stdout.decode())