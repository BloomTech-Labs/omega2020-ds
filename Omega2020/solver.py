from ai import *
import copy

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [s+t for s in rows for t in cols]

def solve(grid):
    """
    Solving the sudoku using function in utils.py
    Input: The sudoku in string format of 81 characters
    Output: There are three kind of outputs depending of the state.
            STATE 1: Valid and solvable Sudoku
                a) State
                b) Solution: String with length of 81
                c) Dictionary of the solution 
                d) Dictionary of the initial puzzle
            STATE 2: Invaid Sudoku
                a) State
                b) Invalid cells
            STATE 3: Valid Sudoku(the initial puzzle follows the Sudoku rules) 
            but doesn't have a solution
                a) State
                b) Message --> "Solution not found"
                c) Dictionary of the initial puzzle

    """
    values = dict(zip(boxes, ["123456789" if element == "." else element for element in grid]))
    valuesb = dict(zip(boxes,["." if element == "." else element for element in grid]))
    validation = validator(grid)

    if len(validation) is 0:

        values = search(values)
        if values is False:
            return (3,'Solution not found', valuesb) #
        else:
            values_solved = len([box for box in values.keys() if len(values[box]) == 1])
            solution = "".join([value if len(value) == 1 else "." for value in values.values()])
            if values_solved == 81:
                return (1, solution, values, valuesb)
    #             return ("Solved", values, solution)
            else:
                return ("Not solved")
    else: 
        for element in validation :
            element.remove(False)       
        return(2,validation)


def solve_technique(grid,technique):
    values = dict(zip(boxes, ["123456789" if element == "." else element for element in grid]))
    
    if technique == "single_position":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
                values = single_position(values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return ("Not solved", values, f"Number of iterations made: {start}")
            if solved_values_before == 81:
                return ("Solved", values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", values, f"Number of iterations made: {start}")
            
    if technique == "single_candidate":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
                values = single_position(values)
                values = single_candidate(values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", values, f"Number of iterations made: {start}")
            
    if technique == "naked_twins":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
                values = single_position(values)
                values = naked_twins(values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", values, f"Number of iterations made: {start}")
            
    if technique == "naked_triple":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
                values = single_position(values)
                values = naked_triple(values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", values, f"Number of iterations made: {start}")        
            

if __name__ == '__main__':
#     if validator(grid) is True:
        
    solve(grid)
    solve_technique(grid,tecnique)