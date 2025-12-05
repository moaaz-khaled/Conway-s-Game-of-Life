import random
import os
import time

Grid = tuple[tuple[int, ...], ...]

def generate_grid(rows: int, cols: int, rng: random.Random) -> Grid:
    return tuple(
        tuple(rng.randint(0, 1) for _ in range(cols))
        for _ in range(rows)
    )

def render_grid(grid: Grid) -> str:
    return "\n".join(" ".join(str(c) for c in row) for row in grid)

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def count_neighbors(grid: Grid, r: int, c: int) -> int:
    deltas = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0),  (1, 1)
    )
    rows, cols = len(grid), len(grid[0])
    return sum(
        grid[r + dr][c + dc]
        for dr, dc in deltas
        if 0 <= r + dr < rows and 0 <= c + dc < cols
    )


def apply_rule(cell: int, neighbors: int) -> int:
    if cell == 1:
        return 1 if neighbors in (2, 3) else 0
    return 1 if neighbors == 3 else 0


def next_generation(grid: Grid) -> Grid:
    rows, cols = len(grid), len(grid[0])
    return tuple(
        tuple(
            apply_rule(grid[r][c], count_neighbors(grid, r, c))
            for c in range(cols)
        )
        for r in range(rows)
    )


def is_stable(current: Grid, previous: Grid) -> bool:
    return current == previous


def is_extinct(grid: Grid) -> bool:
    return sum(sum(row) for row in grid) == 0


def evolve(initial: Grid):
    prev = None
    curr = initial
    gen = 0
    while True:
        yield curr, prev, gen
        prev = curr
        curr = next_generation(curr)
        gen += 1


def get_user_confirmation() -> bool:
    choice = input("Continue? (y/n): ").lower().strip()
    return choice == "y"


def main():
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    seed = int(input("Seed (int): "))
    rng = random.Random(seed)

    initial = generate_grid(rows, cols, rng)

    simulation = evolve(initial)

    for grid, prev, gen in simulation:
        clear_screen()
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