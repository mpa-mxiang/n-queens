import random
import time
import math
from math import trunc
from queue import Queue

# DIM = 0                 # Dimension of the board (n value)
board = []              # Stores the board
row_conflicts = []      # Keeps track of row conflicts
diagr_conflicts = []    # Keeps track of right diagonal conflicts
diagl_conflicts = []    # Keeps track of left diagonal conflicts


# Read in the test n dimensions of the file into a list and return
def readInFile():
    file = open('test.txt', 'r')
    dArrary = []
    for line in file:
        dArrary.append(int(line.rstrip('\n')))
    file.close()
    return dArrary


# Append the solution array to the output file
def writeToFile():
    # Add one to each index to convert from 0 to 1 base indexing
    solutionArrayStr = str([x + 1 for x in board])
    with open('nqueens_out.txt', 'a', 64) as file:
        file.write(solutionArrayStr + "\n\n")
    file.close()


# Updates the conflict table with new conflicts from the updated queen position
# When the parameter val is 1 it will add a conflict to the global lists
# When the parameter val as -1, it will subtract a conflict to the global lists
# The values in the conflict arrays represent the number of queens in each row or diagonal
#       (i.e. a count of 1 indicates no conflict because there is only one queen in the row or diagonal)
def changeConflicts(col, row, val, dim):
    row_conflicts[row] = row_conflicts[row] + val
    diagr_conflicts[col + row] = diagr_conflicts[col + row] + val
    diagl_conflicts[col + (dim - row - 1)
                    ] = diagl_conflicts[col + (dim - row - 1)] + val


# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current column index
def minConflictPos(col, dim):
    minConflicts = dim
    minConflictRows = []
    for row in range(dim):
        # calculate the number of conflicts using the conflict arrays
        conflicts = row_conflicts[row] + diagr_conflicts[col +
                                                         row] + diagl_conflicts[col + (dim - row - 1)]
        # if there are no conflicts in a row, immediately return that row value
        if conflicts == 0:
            return row
        # if the number of conflicts is less, change it to the minConflicts value
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        # if the number of conflicts is equal, append the index instead of changing it
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    # randomly choose the index from the list of tied conflict values
    choice = random.choice(minConflictRows)
    return choice


# Sets up the board using a greedy algorithm
def createBoard(dim):
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts

    # Begin with an empty board
    board = []

    # Initialize the conflict arrays
    # The diagonal conflict lists are the size of the number of diagonals of the board
    diagr_conflicts = [0] * ((2 * dim) - 1)
    diagl_conflicts = [0] * ((2 * dim) - 1)
    row_conflicts = [0] * dim

    # Create an ordered set of all possible row values
    rowSet = set(range(0, dim))
    # Create a list to keep track of which queens have not been placed
    notPlaced = []

    for col in range(0, dim):
        # Pop the next possible row location to test
        testRow = rowSet.pop()
        # Calculate the conflicts for potential location
        conflicts = row_conflicts[testRow] + diagr_conflicts[col +
                                                             testRow] + diagl_conflicts[col + (dim - testRow - 1)]
        # If there are no conflicts, place a queen in that location on the board
        if conflicts == 0:
            board.append(testRow)
            changeConflicts(col, board[col], 1, dim)
        # If a conflict is found...
        else:
            # Place the potential row to the back of the set
            rowSet.add(testRow)
            # Take the next row from the set to test
            testRow2 = rowSet.pop()
            # Calculate the conflicts
            conflicts2 = row_conflicts[testRow2] + diagr_conflicts[col +
                                                                   testRow2] + diagl_conflicts[col + (dim - testRow2 - 1)]
            # If there are no conflicts, place a queen in that location on the board
            if conflicts2 == 0:
                board.append(testRow2)
                changeConflicts(col, board[col], 1, dim)
            else:
                # Otherwise, add the possible row back to the set
                rowSet.add(testRow2)
                # Add a None to the board to hold the place of the potential queen
                board.append(None)
                # Keep track of which column was not placed to be handled later
                notPlaced.append(col)

    for col in notPlaced:
        # Place the remaining queen locations
        board[col] = rowSet.pop()
        # Update the conflict lists
        changeConflicts(col, board[col], 1, dim)


# Finds the column with the most conflicts
def findMaxConflictCol(dim):
    conflicts = 0
    maxConflicts = 0
    maxConflictCols = []

    for col in range(0, dim):
        # Determine the row value for the current column
        row = board[col]
        # Calculate the number of conflicts using the conflict lists
        conflicts = row_conflicts[row] + diagr_conflicts[col +
                                                         row] + diagl_conflicts[col+(dim-row-1)]
        # If conflicts are greater than the current max, make that column the maximum
        if (conflicts > maxConflicts):
            maxConflictCols = [col]
            maxConflicts = conflicts
        # If the conflicts equal the current max, append the index value to the maxConflictCols list
        elif conflicts == maxConflicts:
            maxConflictCols.append(col)
    # Randomly choose from the list of tied maximums
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


# Sets up the board using createBoard() and then solves it with a min-conflict algorithm
def solveNQueens(dim):
    createBoard(dim)
    iteration = 0
    maxIteration = 0.6 * dim    # Define the maximum iterations as 0.6 * size of board
    print("I am here to solve queens")
    print(iteration)
    print(maxIteration)
    while (iteration < maxIteration):
        # Calculate the maximum conflicting column and the number of conflicts it contains
        print("find max conflict col")
        col, numConflicts = findMaxConflictCol(dim)
        # If the number of queens in the row, and diagonals is greater than 1 each (i.e. there are conflicts)
        if (numConflicts > 3):
            print("find new min")
            newLocation = minConflictPos(col, dim)
            # If the better location is not its current location, switch the location
            if (newLocation != board[col]):
                print("change location ")
                # Remove the conflicts from the position the queen is leaving
                changeConflicts(col, board[col], -1, dim)
                board[col] = newLocation
                # Add a conflict to the position the queen is entering
                changeConflicts(col, newLocation, 1, dim)
        # If the max number of conflicts (i.e. the number of queens in each row and diagonals) on the board
        #       equals 3, then there are no conflicts since the queen is alone in it's row and both diagonals
        elif numConflicts == 3:
            # Solution is found
            return True
        iteration += 1
    # If no solution is found in under average number of iterations, return False
    return False


def solve_dfs(dim):
    if dim < 1:
        return []
    solutions = []
    stack = [[]]
    while stack:
        solution = stack.pop()
        if conflict(solution):
            continue
        row = len(solution)
        if row == dim:
            solutions.append(solution)
            continue
        for col in range(dim):
            queen = (row, col)
            queens = solution.copy()
            queens.append(queen)
            stack.append(queens)
    return solutions


def conflict(q):
    for i in range(1, len(q)):
        for j in range(0, i):
            a, b = q[i]
            c, d = q[j]
            if a == c or b == d or abs(a - c) == abs(b - d):
                return True
    return False


def main():

    # Read in the file containing the DIM values
    dimensionArray = readInFile()
    dim = 0
    for dimension in dimensionArray:
        # If the dimension is outside the constraints
        if dimension <= 3 or dimension > 10000000:
            # Print error and write empty array to file
            print("Cannot build board of size: " + str(dimension))
            writeToFile()
        else:
            # Set DIM equal to the current test dimension
            dim = dimension
            # Start timer and set/reset boolen
            time0 = time.time()
            solved = False
            print("Searching for board configuration of size " +
                  str(dimension)+"...")
            # 6 is a special case, return hard-coded solution and skip while loop
            if (dim == 6):
                board = [1, 3, 5, 0, 2, 4]
                solved = True
            else:
               # while (not solved):
                # Solved will be True when a solution is returned
                print("I am going to solve queens")
                solved = solveNQueens(dim)
                print("Board configuration found for size " + str(dimension))
            if solved == False:
                dfs_sol = solve_dfs(dim)
            print("Board configuration found for size " + str(dfs_sol))

            writeToFile()

            # Calculate and print time taken to find solution
            time1 = time.time()
            tot_time = time1 - time0
            time_string = str(trunc(tot_time*100)/100)
            print("   Took " + time_string + " seconds\n")


if __name__ == "__main__":
    main()
