import random

def sum_tail(list):
    def helper(remaining_elements, acc):
        if not remaining_elements:
            return acc
        return helper(remaining_elements[1:], acc + remaining_elements[0])
    return helper(list, 0)


def render_row_tail(row):
    def helper(remaining_cells, acc):
        if not remaining_cells:
            return acc
        sep = " " if len(remaining_cells) > 1 else ""
        return helper(remaining_cells[1:], acc + str(remaining_cells[0]) + sep)
    
    return helper(row, "")


def render_grid(grid):
    def helper(remaining_rows, acc):
        if not remaining_rows:
            return acc
        rendered = render_row_tail(remaining_rows[0])
        sep = "\n" if len(remaining_rows) > 1 else ""
        return helper(remaining_rows[1:], acc + rendered + sep)

    return helper(grid, "")


def generate_grid(rows, cols, rng):
    def generate_row(remaining_cols, acc):
        if remaining_cols == 0:
            return tuple(acc)
        return generate_row(remaining_cols - 1, acc + (rng.randint(0, 1),))
    
    def generate_rows(remaining_rows, acc):
        if remaining_rows == 0:
            return tuple(acc)
        row = generate_row(cols, ())
        return generate_rows(remaining_rows - 1, acc + (row,))
    
    return generate_rows(rows, ())


def count_neighbors(grid, r, c):
    deltas = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0),  (1, 1)
    )
    rows, cols = len(grid), len(grid[0])

    def helper(remaining_deltas, acc):
        if not remaining_deltas:
            return acc
        dr, dc = remaining_deltas[0]
        if 0 <= r + dr < rows and 0 <= c + dc < cols:
            return helper(remaining_deltas[1:], acc + grid[r + dr][c + dc])
        return helper(remaining_deltas[1:], acc)

    return helper(deltas, 0)


# def make_rule(rule_func): 
#     return lambda cell, neighbors: rule_func(cell, neighbors) 

# rule = make_rule(lambda cell, n: 1 if (cell == 1 and n in (2,3)) or (cell == 0 and n == 3) else 0)


def make_rule(rule_func):
    def wrapper(cell, neighbors):
        return rule_func(cell, neighbors)
    return wrapper

def my_rule(cell, n):
    if cell == 1 and n in (2,3):
        return 1
    elif cell == 0 and n == 3:
        return 1
    else:
        return 0

rule = make_rule(my_rule)


def make_grid_mapper(cell_func):
    def mapper(grid):
        rows, cols = len(grid), len(grid[0])

        def process_row(r, c, acc_row):
            if c == cols:
                return tuple(acc_row)
            new_cell = cell_func(r, c, grid)
            return process_row(r, c + 1, acc_row + (new_cell,))

        def process_grid(r, acc_grid):
            if r == rows:
                return tuple(acc_grid)
            row_tuple = process_row(r, 0, ())
            return process_grid(r + 1, acc_grid + (row_tuple,))

        return process_grid(0, ())
    
    return mapper


# next_generation = make_grid_mapper(
#     lambda r, c, grid: rule(grid[r][c], count_neighbors(grid, r, c))
# )

def cell_rule(r, c, grid):
    return rule(grid[r][c], count_neighbors(grid, r, c))

next_generation = make_grid_mapper(cell_rule)


def is_extinct(grid):
    def helper(remaining_rows, acc):
        if not remaining_rows:
            return acc == 0
        return helper(remaining_rows[1:], acc + sum_tail(remaining_rows[0]))

    return helper(grid, 0)


def is_stable(current, previous):
    return current == previous


def evolve(initial, next_gen, is_stable_func):
    def loop(curr, prev, gen, acc):
        new_grid = next_gen(curr)
        new_acc = acc + [(curr, prev, gen)]
        
        if prev and is_stable_func(new_grid, curr):
            return new_acc + [(new_grid, curr, gen + 1)]
        return loop(new_grid, curr, gen + 1, new_acc)
    
    return loop(initial, None, 0, [])


def main():
    while True:
        try:
            rows = int(input("Enter the number of rows: "))
            cols = int(input("Enter the number of columns: "))
            break
        except ValueError:
            print("Please enter valid integers.")
    rng = random.Random()

    initial = generate_grid(rows, cols, rng)

    simulation = evolve(initial, next_generation, is_stable)

    for grid, prev, gen in simulation:
        print(f"Generation {gen}:")
        print(render_grid(grid))
        print("-" * 20)

        if is_extinct(grid):
            print("Simulation stopped: all cells are dead.")
            break

        if prev and is_stable(grid, prev):
            print("Simulation stopped: steady state reached.")
            break

        choice = input("Continue? (y/n): ").lower().strip()
        if choice != "y":
            print("Stopped by user.")
            break


if __name__ == "__main__":
    main()