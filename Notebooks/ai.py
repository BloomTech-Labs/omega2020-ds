class Sudoku:

    """
    Sudoku class
    ------------
    Solves Sudoku puzzles using various techniques. Can display starting
    position and solved attempts as a 2-D string

    Parameters
    -----------
    puzzle(string): A sudoku puzzle in the format '8...74...1.........7.5.9.4.'
                    where the period (.) represents an empty square
                    puzzle string must have length of 81
    technique(string): 'single_position' or 'single_candidate'
                        default = 'single_position'
                        all techniques use 'single_position'
    """

    row_values = "ABCDEFGHI"
    column_values = "123456789"

    def __init__(self, puzzle, technique='single_position'):

        assert len(puzzle) == 81, "Not a valid puzzle. Must have len == 81"
        self.puzzle = puzzle
        self.technique = technique
        self.combined = lambda rows, columns: [each_letter + every_number for each_letter in rows for every_number in columns]
        self.boxes = self.combined(self.row_values, self.column_values)
        self.row_units = [self.combined(each_letter, self.column_values) for each_letter in self.row_values]
        self.column_units = [self.combined(self.row_values, every_number) for every_number in self.column_values]
        self.square_units = [self.combined(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
        self.unitlist = self.row_units + self.column_units + self.square_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)
        self.values = dict(zip(self.boxes, ["123456789" if element == "." else element for element in self.puzzle]))


    def single_position(self):

        solved_values = [box for box in self.values.keys() if len(self.values[box]) == 1]
        for box in solved_values:
            digit = self.values[box]
            for peer in self.peers[box]:
                self.values[peer] = self.values[peer].replace(digit, "")
        return self.values


    def single_candidate(self):

        for unit in self.unitlist:
            for digit in "123456789":
                dplaces = [box for box in self.units if digit in self.values[box]]
                if len(dplaces) == 1:
                    self.values[dplaces[0]] = digit

        return self.values


    def solve(self):

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
                self.values = self.single_position()
                solved_values_after = len([box for box in self.values.keys() if len(self.values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in self.values.keys() if len(self.values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", self.values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", self.values, f"Number of iterations made: {start}")

        elif self.technique == "single_candidate":
            stalled = False
            start = 0
            while not stalled:
                start += 1
                solved_values_before = len([box for box in self.values.keys() if len(self.values[box]) == 1])
                self.values = self.single_position()
                self.values = self.single_candidate()
                solved_values_after = len([box for box in self.values.keys() if len(self.values[box]) == 1])
                stalled = solved_values_before == solved_values_after
                if len([box for box in self.values.keys() if len(self.values[box]) == 0]):
                    return False

            if solved_values_before == 81:
                return ("Solved", self.values, f"Number of iterations made: {start}")
            else:
                return ("Not solved", self.values, f"Number of iterations made: {start}")

        else:
            print("That is not an option.")

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
