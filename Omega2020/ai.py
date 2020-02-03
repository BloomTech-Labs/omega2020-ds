##################################################
## Omega2020 Flask App
##################################################
## MIT License
##################################################
## Authors: Leydy Johana Luna
## Contributors: Rudy Enriquez
## References:  Peter Norvig, http://hodoku.sourceforge.net/en/tech_naked.php
## Version: 1.0.0
##################################################


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from collections import Counter
import pickle
import copy

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = [s + t for s in rows for t in cols]
row_units = [[s + t for s in r for t in cols] for r in rows]
column_units = [[s + t for s in rows for t in c] for c in cols]
square_units = [[s + t for s in rs for t in cs] for
                rs in ('ABC', 'DEF', 'GHI') for
                cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def single_position(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
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
    Go through all the units, and whenever there is a unit with a value that
    only fits in one box, assign the value to this box.
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
    """
    Eliminate values using the naked twins strategy.
    Check if there are two pairs with the sames digits in a row, column or square
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # 1. Find twins
        twins = [v for v in [values[box] for box in unit] if
                 [values[box] for box in unit].count(v) == 2 and len(v) == 2]
        for box in unit:
            if values[box] in twins:
                continue
            for twin in twins:
                for digit in twin:
                    values[box] = values[box].replace(digit, "")
    return values


def naked_triple(values):
    """ 
    Eliminate values using the naked twins strategy.
    Check if there are three triples with the sames digits in a row, column or square    
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    values_triples = [a for a, b in Counter([v for k, v in values.items() if
                      len(v) == 3]).items() if b > 2]
    triples = [([k for k, v in values.items() if v == value_triple]) for
               value_triple in values_triples]
    for triple in triples:
        for unit in unitlist:
            if(set(triple).issubset(set(unit))):
                values_remove = [x for x in unit if x not in triple]
                digits = values[triple[0]]
                for vr in values_remove:
                    for digit in digits:
                        values[vr] = values[vr].replace(digit, "")
    return values


def reduce_puzzle(values):
    """
    Iterate the techniques. If at some point,
    there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration all the techniques,
    the sudoku remains the same, return the resulting 
    sudoku in dictionary form.
    
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if
                     len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if
                                    len(values[box]) == 1])
        values = single_position(values)
        values = single_candidate(values)
        values = naked_twins(values)
        values = naked_triple(values)
        solved_values_after = len([box for box in values.keys() if
                                   len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if
                len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Try to reduce the puzzle using all the techniques. 
    If after an iteration reduce_puzzle,
    the sudoku remains the same, guess a number
    and iterate again the techniques until can solve the 
    puzzle(search and propagation,try all possible values)
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        # Failed earlier
        return False
    if all(len(values[s]) == 1 for s in boxes):
        # Solved!
        return values
    n, s = min((len(values[s]), s) for s in boxes if
               len(values[s]) > 1)
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
    Output: print the grid
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r+c].center(width) +
              ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()


def validator(grid):
    """
    Check that the puzzle follows the Sudoku rules
    Input : grid(string puzzle)
            empty spaces are "."
    Output: Array
            Valid : empty array []
            Invalid : False and the position of the 
            all wring values that are in conflict.
    
    """
    valuesv = dict(zip(boxes, ["." if element == "." else
                   element for element in grid]))
    answ = []
    values_grid = dict(filter(lambda n: n[1] != ".", valuesv.items()))
    a = [(valuesv[n], [valuesv[p] for p in peers[n]], n) for
         n in list(values_grid.keys())]
    for x in a:
        if x[0] in x[1]:
            answ.append([False, x[0], x[2]])
        else:
            pass
    return answ


def transf(values):
    """
    Convert dictionary to a string
    Input : dictionary
    Output: string of length 81
    """
    return len("".join([value for value in values.values()]))


def tracker(values):
    """
    Check how many times the solver uses a function solve a puzzle
    Input : tracker(dictionary)
    Output : array[single_position, single_candidate,
                   naked_twins, naked_triple, search]
    """
    stalled = False
    start = 0
    answ = [0, 0, 0, 0, 0]
    while not stalled:
        initial = transf(values)
        values_before = values.values()
        values = single_position(values)
        values_after = transf(values)
        answ = (answ if values_before == values_after else
                np.add(answ, [1, 0, 0, 0, 0]))
        values_before = values_after
        values = single_candidate(values)
        values_after = transf(values)
        answ = (answ if values_before == values_after else
                np.add(answ, [0, 1, 0, 0, 0]))
        values_before = values_after
        values = naked_twins(values)
        values_after = transf(values)
        answ = (answ if values_before == values_after else
                np.add(answ, [0, 0, 1, 0, 0]))
        values_before = values_after
        values = naked_triple(values)
        values_after = transf(values)
        answ = (answ if values_before == values_after else
                np.add(answ, [0, 0, 0, 1, 0]))
        solved_values = len([box for box in values.keys()
                             if len(values[box]) == 1])
        if solved_values is 81:
            break
        stalled = solved_values == 81
        if initial == values_after:
            start += 1
            aa = [(len(values[s]), s) for
                  s in boxes if len(values[s]) > 1]
            if len(aa) is 0:
                pass
            if len(aa) > 0:
                answ = np.add(answ, [0, 0, 0, 0, 1])
                _, s = min(aa)
                for value in values[s]:
                    new_sudoku = values.copy()
                    new_sudoku[s] = value
                    values = new_sudoku
            if start is 10:
                break
    return(answ)


def conv_values(grid):
    """
    Convert a puzzle string into a dictionary form
    Empty spaces are change with the numbers 1 to 9
    Input : string of length 81
    Output : dictionary
    """
    return dict(zip(boxes, ["123456789" if
                    element == "." else element for element in grid]))


def train_model():
    """
    Train the model using the dataset to predict a difficulty level
    Model : Logistic Regression
    Target : Level
    Features : Tracker() --> split array into 5 new columns
    Input : dataset
    Output : pickle file qith the model trained
    """
    df = pd.read_csv(
                     '../Omega2020/data/dataset.csv').drop('Unnamed: 0',
                                                           axis=1)
    df = df.drop(df[df.Level == 'TEST'].index)
    df['Tracker'] = df['Sudoku'].apply(lambda x: tracker(conv_values(x)))
    df[['Single', 'Candidate', 'Twins',
        'Triples', 'Guess']] = pd.DataFrame(df['Tracker'].values.tolist(),
                                            index=df.index)
    target = ['Level']
    features = ['Single', 'Candidate', 'Twins', 'Triples', 'Guess']
    y = df[target]
    X = df[features]
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=42)
    model = LogisticRegression(solver='lbfgs',
                               multi_class='auto',
                               max_iter=1000)
    outfile = open('difficulty_level_model', 'wb')
    pickle.dump(model.fit(X_train, y_train.values.ravel()), outfile)
    outfile.close()

