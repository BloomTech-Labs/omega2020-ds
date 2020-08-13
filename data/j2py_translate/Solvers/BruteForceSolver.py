#!/usr/bin/env python
""" generated source for module BruteForceSolver_no_german """
from __future__ import print_function
# 
#  * Copyright (C) 2008-12  Bernhard Hobiger
#  *
#  * This file is part of HoDoKu.
#  *
#  * HoDoKu is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License as published by
#  * the Free Software Foundation, either version 3 of the License, or
#  * (at your option) any later version.
#  *
#  * HoDoKu is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with HoDoKu. If not, see <http://www.gnu.org/licenses/>.
#  
# package: solver
# 
#  *
#  * @author hobiwan
#  
class BruteForceSolver(AbstractSolver):
    """ generated source for class BruteForceSolver """
    #  Creates a new instance of BruteForceSolver
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(BruteForceSolver, self).__init__(finder)

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == BRUTE_FORCE:
            result = getBruteForce()
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == BRUTE_FORCE:
            value = step.getValues().get(0)
            for index in step.getIndices():
                sudoku.setCell(index, value)
        else:
            handled = False
        return handled

    # 
    #      * If the sudoku is invalid, no result is returned.
    #      
    def getBruteForce(self):
        """ generated source for method getBruteForce """
        #         print("Brute Force: " + Arrays.toString(sudoku.getValues()));
        if not sudoku.isSolutionSet():
            #  can happen, when command line mode is used (no brute force solving is done)
            #  sets the solution in the sudoku
            #             print("   no solution set");
            isValid = SudokuGeneratorFactory.getDefaultGeneratorInstance().validSolution(sudoku)
            if not isValid:
                return None
        unsolved = SudokuSet()
        i = 0
        while i < Sudoku2.LENGTH:
            if sudoku.getValue(i) == 0:
                #                 print("   adding: " + i);
                unsolved.add(i)
            i += 1
        index = len(unsolved) / 2
        #         print("   index = " + index);
        index = unsolved.get(index)
        step = SolutionStep(SolutionType.BRUTE_FORCE)
        step.addIndex(index)
        step.addValue(sudoku.getSolution(index))
        return step

