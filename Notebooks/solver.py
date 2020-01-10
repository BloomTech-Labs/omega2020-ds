from ai import Sudoku

class SudokuMain():
    """
    Class with solving functions 
    """
#     row_values = "ABCDEFGHI"
#     column_values = "123456789"
    
    def initial_values(self, puzzle):
        self.boxes = puzzle.boxes
        self.unitlist = puzzle.unitlist
        self.units = puzzle.units
        self.peers = puzzle.peers
    
    def single_position(self, values):                
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_values:
            digit = values[box]
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(digit, "")
        return values


    def single_candidate(self, values):
        for unit in self.unitlist:
            for digit in "123456789":
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    values[dplaces[0]] = digit
        return values
    
    #### Naked Twins:
    def naked_twins(self,values):
        
        for unit in self.unitlist:
            #1. Find twins 
            twins = [v for v in [self.values[box] for box in unit] if [self.values[box] for box in unit].count(v) == 2 and len(v) == 2]
            
            for box in unit:
                if values[box] in twins:
                    continue
                for twin in twins :
                    for digit in twin:
                        values[box] = values[box].replace(digit, "")
        return values
            
            #2. eliminate twin values
            
#             values = dict([[box, ''.join(sorted(self.values[box]))] for box in unit])
#             double_digits = dict([[box, values[box]] for box in values if len(values[box])==2])
#             double_digits_occuring_twice = dict([[box, val] for box, val in double_digits.items() if list(double_digits.values()).count(val)==2])        
            
#             if len(double_digits_occuring_twice.items()) != 0:
#                 # reverse the dictionary to get the key-pairs easily
#                 reverse_dict = {}
#                 for k, v in double_digits_occuring_twice.items():
#                     reverse_dict.setdefault(v, []).append(k)
#                 # it is a list of 2 items(keys | boxes) only
#                 naked_twins = list(reverse_dict.items())[0][1]
#                 # remove the naked_twins digits from other boxes in the unit
#                 for k,v in values.items():
#                     if (k not in naked_twins) and (len(v) > 1):
#                         values[k] = ''.join(set(values[k]) - set(values[naked_twins[0]]))            
#             # replace the values in grid_dict with the updated values
#             for k,v in values.items():
#                 values[k] = v
#         return values

    def reduce_puzzle(self, values):
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
            values = self.single_position(values)
            values = self.single_candidate(values)
            values = self.naked_twins(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values    
    
    def search(self, values):
        "Using depth-first search and propagation, try all possible values."
        # First, reduce the puzzle using the previous function
        values = self.reduce_puzzle(values)
        if values is False:
            return False ## Failed earlier
        
        if all(len(values[s]) == 1 for s in self.boxes): 
            return self.values ## Solved!
        n,s = min((len(values[s]), s) for s in self.boxes if len(values[s]) > 1)
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def solvebytechnique(self):

        """
        Returns a tuple with three elements:
        1. string - "Solved" or "Not Solved"
        2. dictionary - Key = The squares coordinate (example: A1)
                        Value = Number that goes into the sqaure (example: 1)
        3. string - "Number of iterations made: 5" This is how many times the
                     algorithm had to iterate through the puzzle
        """

        if self.technique == "single_position":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in self.values.keys() if len(self.values[box]) == 1])
                values = self.single_position(self.values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", str(values), f"Number of iterations made: {start}")
            else:
                return ("Not solved", str(values), f"Number of iterations made: {start}")
            

        elif self.technique == "single_candidate":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in self.values.keys() if len(self.values[box]) == 1])
                values = self.single_position(self.values)
                values = self.single_candidate(values)
                solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in values.keys() if len(values[box]) == 0]):
                    return False

            if solved_values_before == 81: 
                return ("Solved", str(values), f"Number of iterations made: {start}")
            else:
                return ("Not solved", str(values), f"Number of iterations made: {start}")
            
            
        elif self.technique == "naked_twins":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in self.values.keys() if len( self.values[box]) == 1])
                values = self.single_position(self.values)
#                 values = self.single_candidate(values)
                values = self.naked_twins(values)
                solved_values_after = len([box for box in  values.keys() if len( values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in  values.keys() if len( values[box]) == 0]):
                    return False

            if solved_values_before == 81: 
                return ("Solved", str( values), f"Number of iterations made: {start}")
            else:
                return ("Not solved", str( values), f"Number of iterations made: {start}")

        else:
            print("That is not an option.")
    
    
    
    def solve(self, dictionary ):
        """Find the solution to a Sudoku puzzle using search and constraint propagation.
            Args:
                - puzzle (obj): an instance of a Sudoku
                - display_solution (boolean): whether or not to print the solution to sdout
        """
        values = self.values
        if not isinstance(dictionary, Sudoku):
            raise Exception("The puzzle needs to be an instance of Sudoku")

        self.initial_values(dictionary)
        dictionary.values = self.search(self.values)

        if dictionary.solver():
            return ("Solved", str(values))
           
        else:
            return("Not solved")

        

    def show_puzzle(self):

        width = 1+max(len(self.values[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.row_values:
            print(''.join(self.values[r+c].center(width)+('|' if c in '36' else '') for c in self.column_values))
            if r in 'CF': print(line)

    def show_solved_attempt(self):

        width = 1+max(len(self.solve()[1][s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.row_values:
            print(''.join(self.solve()[1][r+c].center(width)+('|' if c in '36' else '') for c in self.column_values))
            if r in 'CF': print(line)

