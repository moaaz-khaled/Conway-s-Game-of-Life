import random
import os
import time

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
    return tuple(tuple(rng.randint(0, 1) for _ in range(cols)) for _ in range(rows))


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


def apply_rule(cell, neighbors):
    if cell == 1:
        return 1 if neighbors in (2, 3) else 0
    return 1 if neighbors == 3 else 0


def next_generation(grid):
    rows, cols = len(grid), len(grid[0])

    def process_row(r, c, acc_row):
        if c == cols:
            return tuple(acc_row)
        new_cell = apply_rule(grid[r][c], count_neighbors(grid, r, c))
        return process_row(r, c + 1, acc_row + (new_cell,))

    def process_grid(r, acc_grid):
        if r == rows:
            return tuple(acc_grid)
        row_tuple = process_row(r, 0, ())
        return process_grid(r + 1, acc_grid + (row_tuple,))

    return process_grid(0, ())


def is_extinct(grid):
    def helper(remaining_rows, acc):
        if not remaining_rows:
            return acc == 0
        return helper(remaining_rows[1:], acc + sum_tail(remaining_rows[0]))

    return helper(grid, 0)


def is_stable(current, previous):
    return current == previous


def evolve(initial):
    def loop(curr, prev, gen):
        yield curr, prev, gen
        new_grid = next_generation(curr)
        yield from loop(new_grid, curr, gen + 1)

    yield from loop(initial, None, 0)


def get_user_confirmation():
    choice = input("Continue? (y/n): ").lower().strip()
    return choice == "y"


def main():
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    rng = random.Random()

    initial = generate_grid(rows, cols, rng)

    simulation = evolve(initial)

    for grid, prev, gen in simulation:
        print(f"Generation {gen}:")
        print(render_grid(grid))
        print("-" * 20)
        time.sleep(0.5)

        if is_extinct(grid):
            print("Simulation stopped: all cells are dead.")
            break

        if prev and is_stable(grid, prev):
            print("Simulation stopped: steady state reached.")
            break

        if not get_user_confirmation():
            print("Stopped by user.")
            break

if __name__ == "__main__":
    main()