import copy

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = [s+t for s in rows for t in cols]
row_units = [[s+t for s in r for t in cols] for r in rows]
column_units = [[s+t for s in rows for t in c] for c in cols]
square_units = [[s+t for s in rs for t in cs]for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def single_position(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, "")
    return values

def single_candidate(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in "123456789":
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
        
    for unit in unitlist:
        #1. Find twins 
        twins = [v for v in [values[box] for box in unit] if [values[box] for box in unit].count(v) == 2 and len(v) == 2]
            
        for box in unit:
            if values[box] in twins:
                continue
            for twin in twins :
                for digit in twin:
                    values[box] = values[box].replace(digit, "")
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = single_position(values)
        values = naked_twins(values)
        values = single_candidate(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*4)]*3)
    clean = []
    for r in rows:
        clean.append(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
    
    clean.insert(3,line)
    clean.insert(7,line)
    return clean

def validator(grid):
    valuesv = dict(zip(boxes,["." if element == "." else element for element in grid]))  
    answ=[]
    values_grid = dict(filter(lambda n: n[1]!=".", valuesv.items()))
    a=[(valuesv[n],[valuesv[p] for p in peers[n]],n) for n in list(values_grid.keys())]
    for x in a:
        if x[0] in x[1]:
            answ.append([False,x[0],x[2]])
        else: 
            pass
    return answ