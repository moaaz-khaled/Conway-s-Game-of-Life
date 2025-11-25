import random

def generateGrid(rows, columns, seed = None):
    RNG = random.Random(seed)
    return [[RNG.randint(0, 1) for column in range(columns)] for row in range(rows)]

def count_alive_neighbors(grid, row, column):
    rows = len(grid)
    columns = len(grid[0])
    directions = [(dr, dc) for dr in [-1 , 0 , 1] for dc in [-1 , 0 , 1] if not (dr == 0 and dc == 0)]
    return sum (
        grid[row + dr][column + dc]
        for dr, dc in directions 
            if 0 <= (row + dr) < rows and 0 <= (column + dc) < columns
    )

def apply_cell_rule(current_cell, neighbors):
    return int((current_cell == 1 and neighbors in (2, 3)) or (not current_cell and neighbors == 3))

def getNextGeneration(grid):
    rows = len(grid)
    columns = len(grid[0])
    return  [
                [apply_cell_rule( grid[i][j] , count_alive_neighbors(grid , i , j) ) 
                    for j in range(columns)]
                for i in range(rows) 
            ]

def countDeadCells(grid):
    return sum(cell == 0 for row in grid for cell in row)


def grids_are_equal(grid1, grid2):
    return all(cell1 == cell2 for row1, row2 in zip(grid1, grid2) for cell1, cell2 in zip(row1, row2))

def should_Terminate(grid , previous_grid):
    total_cells = len(grid) * len(grid[0])
    dead_count = countDeadCells(grid)

    if dead_count == total_cells:
        return True, "all_dead"
    elif grids_are_equal(grid, previous_grid):
        return True, "steady_state"
    else:
        return False, None

def printGrid(grid):
    [print(" ".join(str(cell) for cell in row)) for row in grid]

def getUserInput():
    while True:
        try:
            rows = int(input("Enter the number of rows: "))
            columns = int(input("Enter the number of columns: "))
            return rows, columns
        except ValueError:
            print("Please enter valid integers.")

def ask_Continue():
    choice = input("\nDo you want to apply the rules again? (y / any): ")
    if choice.lower() == 'y':
        return True
    return False


def simulate_generations(current_grid, previous_grid):
    next_grid = getNextGeneration(current_grid)
    
    print("\nGrid after applying rules:")
    printGrid(next_grid)
    
    should_stop, reason = should_Terminate(next_grid, current_grid)
    
    if should_stop:
        if reason == "all_dead":
            print("All cells are dead. Ending simulation.")
        elif reason == "steady_state":
            print("Grid didn't change. Ending simulation. (steady state)")
        return next_grid
    
    if not ask_Continue():
        print("Simulation ended by user.")
        return next_grid
    
    return simulate_generations(next_grid, current_grid)


def main():
    rows, columns = getUserInput()
    
    InitialGrid = generateGrid(rows, columns)
    
    print("\nInitial Grid:")
    printGrid(InitialGrid)
    
    final_grid = simulate_generations(InitialGrid, InitialGrid)

if __name__ == "__main__":
    main()