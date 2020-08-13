#!/usr/bin/env python
""" generated source for module MiscellaneousSolver_no_german """
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
#  * Originale Beschreibung aus dem Player's Forum:
#  *    Consider the set of unfilled cells C that lies at the intersection of Box B and Row (or Column) R.
#  *    Suppose |C|>=2. Let V be the set of candidate values to occur in C. Suppose |V|>= |C|+2.
#  *    The pattern requires that we find |V|-|C| cells in B and R, with at least one cell in each,
#  *    with candidates drawn entirely from V. Label the sets of cells CB and CR and their candidates VB and VR.
#  *    Crucially, no candidate is allowed to appear in VB and VR. Then C must contain V\(VB U VR) [possibly empty],
#  *    |VB|-|CB| elements of VB and |VR|-|CR| elements of VR. The construction allows us to eliminate the
#  *    candidates V\VR from B\(C U CB) and the candidates V\VB from R\(C U CR).
#  *
#  *
#  * @author hobiwan
#  
class MiscellaneousSolver(AbstractSolver):
    """ generated source for class MiscellaneousSolver """
    #  One entry in the recursion stack for the unit search 
    class StackEntry(object):
        """ generated source for class StackEntry """
        #  The index of the cell that is currently tried 
        aktIndex = 0

        #  The indices of the cells in the current selection 
        indices = SudokuSet()

        #  The candidates in the current selection 
        candidates = 0

    #  All steps that were found in this search 
    steps = None

    #  One global step for optimization 
    globalStep = SolutionStep(SolutionType.HIDDEN_SINGLE)

    #  All indices in the current row/col (only cells that are not set yet) 
    nonBlockSet = SudokuSet()

    #  All indices in the current block (only cells that are not set yet) 
    blockSet = SudokuSet()

    #  All indices in the current intersection (only cells that are not set yet) 
    intersectionSet = SudokuSet()

    #  All indices in row/col that can hold additional cells (row/col - set cells - intersection) 
    nonBlockSourceSet = SudokuSet()

    #  All indices in block that can hold additional cells (block - set cells - intersection) 
    blockSourceSet = SudokuSet()

    #  Stack for searching rows/cols 
    stack1 = [None] * Sudoku2.UNITS

    #  Stack for searching blocks 
    stack2 = [None] * Sudoku2.UNITS

    #  Cells of the current subset of the intersection 
    intersectionActSet = SudokuSet()

    #  Candidates of all cells in {@link #intersectionActSet}. 
    intersectionActCandSet = 0

    #  Indices of the current additional cells in the row/col 
    nonBlockActSet = SudokuSet()

    #  Candidates of all cells in {@link #nonBlockActSet}. 
    nonBlockActCandSet = 0

    #  Valid candidates for block 
    blockAllowedCandSet = 0

    #  Indices of the current additional cells in the block 
    blockActSet = SudokuSet()

    #  Candidates of all cells in {@link #blockActSet}. 
    blockActCandSet = 0

    #  For temporary calculations 
    tmpSet = SudokuSet()

    # 
    #      * Creates a new instance of MiscellaneousSolver
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(MiscellaneousSolver, self).__init__(finder)
        i = 0
        while len(stack1):
            self.stack1[i] = self.StackEntry()
            self.stack2[i] = self.StackEntry()
            i += 1

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == SUE_DE_COQ:
            result = getSueDeCoq(True)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == SUE_DE_COQ:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    def getAllSueDeCoqs(self):
        """ generated source for method getAllSueDeCoqs """
        sudoku = finder.getSudoku()
        oldSteps = self.steps
        self.steps = ArrayList()
        getSueDeCoqInt(Sudoku2.LINE_TEMPLATES, Sudoku2.BLOCK_TEMPLATES, False)
        getSueDeCoqInt(Sudoku2.COL_TEMPLATES, Sudoku2.BLOCK_TEMPLATES, False)
        result = self.steps
        self.steps = oldSteps
        return result

    def getSueDeCoq(self, onlyOne):
        """ generated source for method getSueDeCoq """
        step = getSueDeCoqInt(Sudoku2.LINE_TEMPLATES, Sudoku2.BLOCK_TEMPLATES, onlyOne)
        if onlyOne and step != None:
            return step
        return getSueDeCoqInt(Sudoku2.COL_TEMPLATES, Sudoku2.BLOCK_TEMPLATES, onlyOne)

    # 
    #      * Builds all possible intersections of <code>blocks</code> and
    #      * <code>nonBlocks</code>. Delegates the check to
    #      * {@link #checkIntersection(boolean) }.
    #      * @param nonBlocks Sets containing all lines or all columns
    #      * @param blocks Sets containing all blocks
    #      * @param onlyOne
    #      * @return
    #      
    def getSueDeCoqInt(self, nonBlocks, blocks, onlyOne):
        """ generated source for method getSueDeCoqInt """
        #  get all possible intersections between blocks and nonBlocks
        emptyCells = finder.getEmptyCells()
        #  for every row/col
        i = 0
        while len(nonBlocks):
            self.nonBlockSet.setAnd(nonBlocks[i], emptyCells)
            #  and every block
            j = 0
            while len(blocks):
                self.blockSet.setAnd(blocks[j], emptyCells)
                #  get the intersection
                self.intersectionSet.set(self.nonBlockSet)
                self.intersectionSet.and_(self.blockSet)
                if self.intersectionSet.isEmpty() or len(self.intersectionSet) < 2:
                    #  nothing to do
                    j += 1
                    continue 
                #  check the intersection
                step = checkIntersection(onlyOne)
                if onlyOne and step != None:
                    return step
                j += 1
            i += 1
        return None

    # 
    #      * Checks all possible combinations of cells in the intersection. If a combination
    #      * holds 2 more candidates than cells, a SDC could possibly exist.<br>
    #      * The method doesnt use recursion. There can be only two or three cells in an
    #      * intersection for an SDC.
    #      * @param onlyOne
    #      * @return
    #      
    def checkIntersection(self, onlyOne):
        """ generated source for method checkIntersection """
        max = len(self.intersectionSet)
        nPlus = 0
        self.intersectionActSet.clear()
        i1 = 0
        while i1 < max - 1:
            #  all candidates of the first cell
            index1 = self.intersectionSet.get(i1)
            self.intersectionActSet.add(index1)
            cand1 = sudoku.getCell(index1)
            #  now try the second cell
            i2 = i1 + 1
            while i2 < max:
                index2 = self.intersectionSet.get(i2)
                cand2 = int((cand1 | sudoku.getCell(index2)))
                self.intersectionActSet.add(index2)
                #  we have two cells in the intersection
                nPlus = Sudoku2.ANZ_VALUES[cand2] - 2
                if nPlus >= 2:
                    #  possible SDC -> check
                    step = checkHouses(nPlus, cand2, onlyOne)
                    if onlyOne and step != None:
                        return step
                #  and the third cell
                i3 = i2 + 1
                while i3 < max:
                    index3 = self.intersectionSet.get(i3)
                    cand3 = int((cand2 | sudoku.getCell(index3)))
                    #  now we have three cells in the intersection
                    nPlus = Sudoku2.ANZ_VALUES[cand3] - 3
                    if nPlus >= 2:
                        #  possible SDC -> check
                        self.intersectionActSet.add(index3)
                        step = checkHouses(nPlus, cand3, onlyOne)
                        if onlyOne and step != None:
                            return step
                        self.intersectionActSet.remove(index3)
                    i3 += 1
                self.intersectionActSet.remove(index2)
                i2 += 1
            self.intersectionActSet.remove(index1)
            i1 += 1
        return None

    # 
    #      * Builds a set with all cells in the row/col that are not part of the
    #      * intersection and delegates the check to
    #      * {@link #checkHouses(int, sudoku.SudokuSet, short, short, boolean, boolean) }.
    #      * @param nPlus How many more candidates than cells
    #      * @param cand Candidates in the intersection
    #      * @param onlyOne
    #      * @return
    #      
    @overloaded
    def checkHouses(self, nPlus, cand, onlyOne):
        """ generated source for method checkHouses """
        #  store the candidates of the current intersection
        self.intersectionActCandSet = cand
        #  check nonBlocks: all cells not used in the intersection are valid
        self.nonBlockSourceSet.set(self.nonBlockSet)
        self.nonBlockSourceSet.andNot(self.intersectionActSet)
        #  now check all possible combinations of cells in nonBlockSet
        return self.checkHouses(nPlus, self.nonBlockSourceSet, Sudoku2.MAX_MASK, onlyOne, False)

    # 
    #      * Does a non recursive search: All possible combinations of indices in
    #      * <code>sourceSet</code> are tried.<br>
    #      * The method is used twice: The first run builds possible sets of cells
    #      * from the row/col. A set is valid if it contains candidates from the intersection,
    #      * has at least one cell more than extra candidates (candidates not contained in the
    #      * intersection) but leaves candidates in the intersection for the block search. If those
    #      * criteria are met, the method is called recursivly for the second run.<br>
    #      * The second run builds all possible sets of cells for the block. For every combination
    #      * that meets the SDC criteria a check for deleteable candidates is made.
    #      * @param nPlus
    #      * @param sourceSet
    #      * @param allowedCandSet
    #      * @param onlyOne
    #      * @param secondCheck
    #      * @return
    #      
    @checkHouses.register(object, int, SudokuSet, int, bool, bool)
    def checkHouses_0(self, nPlus, sourceSet, allowedCandSet, onlyOne, secondCheck):
        """ generated source for method checkHouses_0 """
        if sourceSet.isEmpty():
            #  nothing to do!
            return None
        stack = self.stack2 if secondCheck else self.stack1
        max = len(sourceSet)
        #  level 0 is only a marker, we start with level 1
        level = 1
        stack[0].aktIndex = -1
        stack[0].candidates = 0
        stack[0].indices.clear()
        stack[1].aktIndex = -1
        while True:
            while stack[level].aktIndex >= max - 1:
                level -= 1
                if level <= 0:
                    return None
            stack[level].aktIndex += 1
            stack[level].indices.set(stack[level - 1].indices)
            stack[level].indices.add(sourceSet.get(stack[level].aktIndex))
            stack[level].candidates = int((stack[level - 1].candidates | sudoku.getCell(sourceSet.get(stack[level].aktIndex))))
            if (stack[level].candidates & ~allowedCandSet) == 0:
                tmpCands = int((stack[level].candidates & self.intersectionActCandSet))
                anzContained = Sudoku2.ANZ_VALUES[tmpCands]
                tmpCands = int((stack[level].candidates & ~self.intersectionActCandSet))
                anzExtra = Sudoku2.ANZ_VALUES[tmpCands]
                if not secondCheck:
                    if anzContained > 0 and level > anzExtra and level - anzExtra < nPlus:
                        self.nonBlockActSet = stack[level].indices
                        self.nonBlockActCandSet = stack[level].candidates
                        self.blockSourceSet.set(self.blockSet)
                        self.blockSourceSet.andNot(self.intersectionActSet)
                        self.blockSourceSet.andNot(self.nonBlockActSet)
                        self.blockAllowedCandSet = self.nonBlockActCandSet
                        self.blockAllowedCandSet &= ~tmpCands
                        self.blockAllowedCandSet = int(~self.blockAllowedCandSet)
                        step = self.checkHouses(nPlus - (len(self.nonBlockActSet) - anzExtra), self.blockSourceSet, self.blockAllowedCandSet, onlyOne, True)
                        if onlyOne and step != None:
                            return step
                else:
                    if anzContained > 0 and stack[level]len(.indices) - anzExtra == nPlus:
                        self.globalStep.reset()
                        self.blockActSet = stack[level].indices
                        self.blockActCandSet = stack[level].candidates
                        tmpCandSet1 = int((self.blockActCandSet & self.nonBlockActCandSet))
                        self.tmpSet.set(self.blockSet)
                        self.tmpSet.andNot(self.blockActSet)
                        self.tmpSet.andNot(self.intersectionActSet)
                        tmpCandSet = int((((self.intersectionActCandSet | self.blockActCandSet) & ~self.nonBlockActCandSet) | tmpCandSet1))
                        checkCandidatesToDelete(self.tmpSet, tmpCandSet)
                        self.tmpSet.set(self.nonBlockSet)
                        self.tmpSet.andNot(self.nonBlockActSet)
                        self.tmpSet.andNot(self.intersectionActSet)
                        tmpCandSet = int((((self.intersectionActCandSet | self.nonBlockActCandSet) & ~self.blockActCandSet) | tmpCandSet1))
                        checkCandidatesToDelete(self.tmpSet, tmpCandSet)
                        if self.globalStep.getCandidatesToDelete().size() > 0:
                            self.globalStep.setType(SolutionType.SUE_DE_COQ)
                            j = 0
                            while j < len(self.intersectionActSet):
                                self.globalStep.addIndex(self.intersectionActSet.get(j))
                                j += 1
                            cands = Sudoku2.POSSIBLE_VALUES[self.intersectionActCandSet]
                            j = 0
                            while len(cands):
                                self.globalStep.addValue(cands[j])
                                j += 1
                            getSetCandidates(self.nonBlockActSet, self.intersectionActSet, self.nonBlockActCandSet, self.globalStep.getFins())
                            getSetCandidates(self.blockActSet, self.intersectionActSet, self.blockActCandSet, self.globalStep.getEndoFins())
                            self.globalStep.addAls(self.intersectionActSet, self.intersectionActCandSet)
                            self.globalStep.addAls(self.blockActSet, self.blockActCandSet)
                            self.globalStep.addAls(self.nonBlockActSet, self.nonBlockActCandSet)
                            step = self.globalStep.clone()
                            if onlyOne:
                                return step
                            else:
                                self.steps.add(step)
            if stack[level].aktIndex < max - 1:
                level += 1
                stack[level].aktIndex = stack[level - 1].aktIndex

    def getSetCandidates(self, srcSet1, srcSet2, candSet, dest):
        """ generated source for method getSetCandidates """
        self.tmpSet.set(srcSet1)
        self.tmpSet.or_(srcSet2)
        i = 0
        while i < len(self.tmpSet):
            index = self.tmpSet.get(i)
            if (sudoku.getCell(index) & candSet) != 0:
                cands = Sudoku2.POSSIBLE_VALUES[sudoku.getCell(index) & candSet]
                j = 0
                while len(cands):
                    dest.add(Candidate(index, cands[j]))
                    j += 1
            i += 1

    def checkCandidatesToDelete(self, tmpSet, tmpCandSet):
        """ generated source for method checkCandidatesToDelete """
        if len(tmpSet) > 0 and Sudoku2.ANZ_VALUES[tmpCandSet] > 0:
            i = 0
            while i < len(tmpSet):
                index = tmpSet.get(i)
                elimCandMask = int((sudoku.getCell(index) & tmpCandSet))
                if elimCandMask == 0:
                    i += 1
                    continue 
                cands = Sudoku2.POSSIBLE_VALUES[elimCandMask]
                j = 0
                while len(cands):
                    self.globalStep.addCandidateToDelete(index, cands[j])
                    j += 1
                i += 1

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":1101:12369:.....3+5+1+7+1+3+5+42+786+9867+91+54..+6+935+4+82+717183.+2.+54+2+54...........47.55......+4.....+5..9.::184 194 273 371 684 685 694 985::")
        solver = SudokuSolverFactory.getDefaultSolverInstance()
        singleHint = True
        if singleHint:
            step = solver.getHint(sudoku, False)
            print(step)
        else:
            steps = solver.getStepFinder().getAllSueDeCoqs(sudoku)
            solver.getStepFinder().printStatistics()
            if len(cls.steps) > 0:
                Collections.sort(cls.steps)
                for actStep in steps:
                    print(actStep)
        System.exit(0)

