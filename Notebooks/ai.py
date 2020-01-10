
class Sudoku():

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
    technique(string): 'single_position', 'single_candidate'
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
        

    def solver(self):
            """
            Solve a puzzle
            
            """
            reduce_puzzle = all(len(self.values[s]) == 1 for s in self.boxes)
            if not reduce_puzzle:
                return False

            for unit in self.unitlist:
                digits = '123456789'
                for box in unit:
                    digits = digits.replace(self.values[box], '')
                if len(digits) != 0:
                    return False
            return True

    