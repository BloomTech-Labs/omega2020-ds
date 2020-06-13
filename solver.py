##################################################
## Omega2020 Solver
##################################################
## MIT License
##################################################
## Authors: Leydy Johana Luna
## Contributors: Rudy Enriquez
## References:  Peter Norvig, http://hodoku.sourceforge.net/en/tech_naked.php
## Version: 1.0.0
##################################################


from .ai import *
import pickle
import copy
import sys


picklefile = open('data/difficulty_level_model', 'rb')
model_level = pickle.load(picklefile)
picklefile.close()

def get_boxes_and_values(grid):
    rows = None
    cols = None
    boxes = None
    values = None
    valuesb = None
    size = None
    if len(grid) == 81:
        rows = 'ABCDEFGHI'
        cols = '123456789'
        size = 9
        boxes = [s+t for s in rows for t in cols]
        values = dict(zip(boxes, ["123456789" if x == "." else x for x in grid]))
        valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    elif len(grid) == 16:
        rows = 'ABCD'
        cols = '1234'
        size = 4
        boxes = [s+t for s in rows for t in cols]
        values = dict(zip(boxes, ["1234" if x == "." else x for x in grid]))
        valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    elif len(grid) == 36:
        rows = 'ABCDEF'
        cols = '123456'
        size = 6
        boxes = [s+t for s in rows for t in cols]
        values = dict(zip(boxes, ["1234" if x == "." else x for x in grid]))
        valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    elif len(grid) == 144:
        rows = 'ABCDEFGHIJKL'
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        size = 12
        boxes = [s+t for s in rows for t in cols]
        values = dict(zip(boxes, ["123456789" if x == "." else x for x in grid]))
        valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    elif len(grid) == 256:
        rows = 'ABCDEFGHIJKLMNOP'
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
        size = 16
        boxes = [s+t for s in rows for t in cols]
        values = dict(zip(boxes, ["123456789" if x == "." else x for x in grid]))
        valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    return boxes, values, valuesb, size, rows, cols


def solve(grid):
    """
    Solving the sudoku using function in utils.py
    Input: The sudoku in string format of 81 characters
    Output: There are three kind of outputs depending of the state.
            STATE 1: Valid and solvable Sudoku
                a) State
                b) Solution: String with length of 81
                c) Prediction initial puzzle (String)
                d) Prediction Difficulty Level --> (String)
                e) Solve by technique 
                    array['Single_position','Single_Candidate',
                          'Naked_twins','Naked_Triple']
            STATE 2: Invaid Sudoku
                a) State
                b) Invalid cells
                c) Prediction initial puzzle (String)
                d) Message --> "No Difficulty Level"
            STATE 3: Valid Sudoku(the initial puzzle follows the Sudoku rules)
            but doesn't have a solution
                a) State
                b) Message --> "Not Solution"
                c) Prediction initial puzzle (String)
                d) Message --> "No Difficulty Level"
    """

    boxes, values, valuesb, size, rows, cols = get_boxes_and_values(grid)
    
    # commented out the following 3 lines to test the rewrite
    # values = dict(zip(boxes, ["123456789" if x == "." else x for x in grid]))
    # valuesb = dict(zip(boxes, ["." if x == "." else x for x in grid]))
    validation = validator(grid)

    # keep this and uncomment for debugging larger dimensional puzzles later
    # print(f"validation: {validation}", file=sys.stderr)

    if len(validation) is 0:
        tech=[]
        values = search(values)
        if values is False:
            return (3, 'Not Solution', grid, 'No Difficulty Level')
        else:
            values_solved = len([box for box in values.keys() if
                                len(values[box]) == 1])
            solution = "".join([value if len(value) == 1 else "."
                                for value in values.values()])
            if values_solved == size**2:
                init_values = dict(zip(boxes, [cols
                                   if x == "." else x for x in grid]))
                tracker_solve = tracker(init_values).reshape(1, -1)
                level = model_level.predict(tracker_solve)[0]
                techniques= ['single_position', 'single_candidate',
                             'naked_twins','naked_triple']
                for technique in techniques:
                    tech.append(solve_technique(grid, technique)[0])
                return (1, solution, grid, level, tech)
            else:
                return ("Not solved")
    else:
        for element in validation:
            element.remove(False)
        return(2, validation, grid, 'No Difficulty Level')


def solve_technique(grid, technique):
    """
    Check if a puzzle can be solved using a specific technique
    """
    boxes, values, valuesb, size, rows, cols = get_boxes_and_values(grid)

    values = dict(zip(boxes, [cols
                  if element == "." else element for element in grid]))
    if technique == "single_position":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys()
                                            if len(values[box]) == 1])
                values = single_position(values)
                solved_values_after = len([box for box in values.keys()
                                           if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys()
                        if len(values[box]) == 0]):
                    # Not Solved
                    return False
            if solved_values_after == size:
                # Solved
                return (1, values)
            else:
                # Not Solved
                return (0, values)
            
    if technique == "single_candidate":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys()
                                            if len(values[box]) == 1])
                values = single_position(values)
                values = single_candidate(values)
                solved_values_after = len([box for box in values.keys()
                                           if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys()
                        if len(values[box]) == 0]):
                    return False
            if solved_values_after == size:
                return (1, values)
            else:
                return (0, values)
    if technique == "naked_twins":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys()
                                            if len(values[box]) == 1])
                values = single_position(values)
                values = naked_twins(values)
                solved_values_after = len([box for box in values.keys()
                                           if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys()
                        if len(values[box]) == 0]):
                    return False
            if solved_values_after == size:
                return (1, values)
            else:
                return (0, values)
    if technique == "naked_triple":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in values.keys()
                                            if len(values[box]) == 1])
                values = single_position(values)
                values = naked_triple(values)
                solved_values_after = len([box for box in values.keys()
                                          if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys()
                        if len(values[box]) == 0]):
                    return False
            if solved_values_after == size:
                return (1, values)
            else:
                return (0, values)

if __name__ == '__main__':
    solve(grid)
    solve_technique(grid, technique)

