import random

while True:
    try:
        rows = int(input("Enter the number of rows: "))
        columns = int(input("Enter the number of columns: "))
        break
    except ValueError:
        print("Please enter valid integers.")

InitialGrid = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(random.randint(0, 1))
    InitialGrid.append(row)

print("Initial Grid:") 
for row in InitialGrid:
    for cell in row:
        print(cell , end = " ")
    print()

NewGrid = []
for i in range(rows):
    new_row = []
    for j in range(columns):
        new_row.append(0)
    NewGrid.append(new_row)

def count_Alive_neighbors(InitialGrid, row, column):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = column + dc
            if 0 <= nr < rows and 0 <= nc < columns:
                if InitialGrid[nr][nc] == 1:
                    count += 1
    return count

while True:
    for row in range(rows):
        for column in range(columns):
            neighbors = count_Alive_neighbors(InitialGrid, row, column)
            if InitialGrid[row][column] == 1:
                if neighbors < 2:
                    NewGrid[row][column] = 0
                elif neighbors == 2 or neighbors == 3:
                    NewGrid[row][column] = 1
                elif neighbors > 3:
                    NewGrid[row][column] = 0
            else:
                if neighbors == 3:
                    NewGrid[row][column] = 1

    CountDeadCell = 0
    print("\nGrid after applying rules:")
    for row in NewGrid:
        for cell in row:
            print(cell, end=" ")
            if cell == 0:
                CountDeadCell += 1
        print()

    if CountDeadCell == rows * columns:
        print("All cells are dead. Ending simulation.")
        break

    elif NewGrid == InitialGrid:
        print("Grid didn't change. Ending simulation. (steady state) ")
        break

    choice = input("\nDo you want to apply the rules again? (y / any): ")
    if choice != 'y' and choice != 'Y':
        print("Simulation ended by user.")
        break

    for i in range(rows):
        for j in range(columns):
            InitialGrid[i][j] = NewGrid[i][j]

    NewGrid = []
    for i in range(rows):
        new_row = []
        for j in range(columns):
            new_row.append(0)
        NewGrid.append(new_row)