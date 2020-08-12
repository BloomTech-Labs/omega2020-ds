#!/usr/bin/env python
""" generated source for module WingSolver_no_german """
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
class WingSolver(AbstractSolver):
    """ generated source for class WingSolver """
    #  One global step for eliminations 
    globalStep = SolutionStep(SolutionType.FULL_HOUSE)

    #  A list for all steps found in one search 
    steps = ArrayList()

    #  A set for elimination checks 
    preCalcSet1 = SudokuSet()

    #  A set for elimination checks 
    preCalcSet2 = SudokuSet()

    #  A set for elimination checks 
    elimSet = SudokuSet()

    #  The indices of all bivalue cells in the current sudoku (for XY-Wing) 
    biCells = [None] * Sudoku2.LENGTH

    #  The indices of all trivalue cells in the current sudoku (for XYZ-Wing) 
    triCells = [None] * Sudoku2.LENGTH

    #  The first index of the strong link for W-Wings 
    wIndex1 = -1

    #  The second index of the strong link for W-Wings 
    wIndex2 = -1

    #  Creates a new instance of WingSolver
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(WingSolver, self).__init__(finder)

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == XY_WING:
            result = getXYWing()
        elif type_ == XYZ_WING:
            result = getXYZWing()
        elif type_ == W_WING:
            result = getWWing(True)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == XY_WING:
            pass
        elif step.getType() == W_WING:
            pass
        elif step.getType() == XYZ_WING:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    # 
    #      * get the next XY-Wing
    #      * @return
    #      
    def getXYWing(self):
        """ generated source for method getXYWing """
        return getWing(False, True)

    # 
    #      * get the next XYZ-Wing
    #      * @return
    #      
    def getXYZWing(self):
        """ generated source for method getXYZWing """
        return getWing(True, True)

    # 
    #      * Searches for all types of wings.
    #      * @return
    #      
    def getAllWings(self):
        """ generated source for method getAllWings """
        sudoku = finder.getSudoku()
        newSteps = ArrayList()
        oldSteps = self.steps
        self.steps = newSteps
        getWing(True, False)
        getWing(False, False)
        getWWing(False)
        self.steps = oldSteps
        return newSteps

    def getWing(self, xyz, onlyOne):
        """ generated source for method getWing """
        #  first get all bivalue/trivalue cells
        biValueCount = 0
        triValueCount = 0
        i = 0
        while i < Sudoku2.LENGTH:
        __biValueCount_0 = biValueCount
        biValueCount += 1
        __triValueCount_1 = triValueCount
        triValueCount += 1
            if sudoku.getAnzCandidates(i) == 2:
                self.biCells[__biValueCount_0] = i
            if xyz and sudoku.getAnzCandidates(i) == 3:
                self.triCells[__triValueCount_1] = i
            i += 1
        #  now iterate them; use local variables to cover xy and xyz
        endIndex = triValueCount if xyz else biValueCount
        biTri = self.triCells if xyz else self.biCells
        #  we check all combinations of bivalue cells (one tri + 2 bi for xyz)
        i = 0
        while i < endIndex:
            j = 0 if xyz else i + 1
            while j < biValueCount:
                #  any given combination of two cells must give exactly three
                #  candidates; if that is not the case, skip it right away
                if Sudoku2.ANZ_VALUES[sudoku.getCell(biTri[i]) | sudoku.getCell(self.biCells[j])] != 3:
                    #  cant become a wing
                    j += 1
                    continue 
                k = j + 1
                while k < biValueCount:
                    index1 = biTri[i]
                    index2 = self.biCells[j]
                    index3 = self.biCells[k]
                    cell1 = sudoku.getCell(index1)
                    cell2 = sudoku.getCell(index2)
                    cell3 = sudoku.getCell(index3)
                    #  all three cells combined must have exactly three candidates
                    if Sudoku2.ANZ_VALUES[cell1 | cell2 | cell3] != 3:
                        #  incorrect number of candidates
                        k += 1
                        continue 
                    #  none of the cells may be equal
                    if cell1 == cell2 or cell2 == cell3 or cell3 == cell1:
                        #  cant be a wing
                        k += 1
                        continue 
                    #  three possibilities for XY-Wing: each cell could be the pincer
                    #  XYZ-Wing exits the loop after the first iteration
                    maxTries = 1 if xyz else 3
                    tries = 0
                    while tries < maxTries:
                        #  swap cells accordingly
                        if tries == 1:
                            index1 = self.biCells[j]
                            index2 = biTri[i]
                            cell1 = sudoku.getCell(index1)
                            cell2 = sudoku.getCell(index2)
                        elif tries == 2:
                            index1 = self.biCells[k]
                            index2 = self.biCells[j]
                            index3 = biTri[i]
                            cell1 = sudoku.getCell(index1)
                            cell2 = sudoku.getCell(index2)
                            cell3 = sudoku.getCell(index3)
                        #  the pivot must see the pincers
                        if not Sudoku2.buddies[index1].contains(index2) or not Sudoku2.buddies[index1].contains(index3):
                            tries += 1
                            continue 
                        cell = int((cell2 & cell3))
                        if Sudoku2.ANZ_VALUES[cell] != 1:
                            tries += 1
                            continue 
                        candZ = Sudoku2.CAND_FROM_MASK[cell]
                        self.elimSet.setAnd(Sudoku2.buddies[index2], Sudoku2.buddies[index3])
                        self.elimSet.and_(finder.getCandidates()[candZ])
                        if xyz:
                            self.elimSet.and_(Sudoku2.buddies[index1])
                        if self.elimSet.isEmpty():
                            tries += 1
                            continue 
                        self.globalStep.reset()
                        if xyz:
                            self.globalStep.setType(SolutionType.XYZ_WING)
                        else:
                            self.globalStep.setType(SolutionType.XY_WING)
                        cands = sudoku.getAllCandidates(index1)
                        self.globalStep.addValue(cands[0])
                        self.globalStep.addValue(cands[1])
                        if xyz:
                            self.globalStep.addValue(cands[2])
                        else:
                            self.globalStep.addValue(candZ)
                        self.globalStep.addIndex(index1)
                        self.globalStep.addIndex(index2)
                        self.globalStep.addIndex(index3)
                        if xyz:
                            self.globalStep.addFin(index1, candZ)
                        self.globalStep.addFin(index2, candZ)
                        self.globalStep.addFin(index3, candZ)
                        l = 0
                        while l < len(self.elimSet):
                            self.globalStep.addCandidateToDelete(self.elimSet.get(l), candZ)
                            l += 1
                        step = self.globalStep.clone()
                        if onlyOne:
                            return step
                        else:
                            self.steps.add(step)
                        tries += 1
                    k += 1
                j += 1
            i += 1
        return None

    def getWWing(self, onlyOne):
        """ generated source for method getWWing """
        i = 0
        while len(length):
            if sudoku.getValue(i) != 0 or sudoku.getAnzCandidates(i) != 2:
                i += 1
                continue 
            cell1 = sudoku.getCell(i)
            cand1 = sudoku.getAllCandidates(i)[0]
            cand2 = sudoku.getAllCandidates(i)[1]
            self.preCalcSet1.setAnd(Sudoku2.buddies[i], finder.getCandidates()[cand1])
            self.preCalcSet2.setAnd(Sudoku2.buddies[i], finder.getCandidates()[cand2])
            j = i + 1
            while len(length):
                if sudoku.getCell(j) != cell1:
                    j += 1
                    continue 
                self.elimSet.setAnd(self.preCalcSet1, Sudoku2.buddies[j])
                if not self.elimSet.isEmpty():
                    step = checkLink(cand1, cand2, i, j, self.elimSet, onlyOne)
                    if onlyOne and step != None:
                        return step
                self.elimSet.setAnd(self.preCalcSet2, Sudoku2.buddies[j])
                if not self.elimSet.isEmpty():
                    step = checkLink(cand2, cand1, i, j, self.elimSet, onlyOne)
                    if onlyOne and step != None:
                        return step
                j += 1
            i += 1
        return None

    def checkLink(self, cand1, cand2, index1, index2, elimSet, onlyOne):
        """ generated source for method checkLink """
        free = sudoku.getFree()
        constr = 0
        while len(free):
            if free[constr][cand2] == 2:
                sees1 = False
                sees2 = False
                indices = Sudoku2.ALL_UNITS[constr]
                i = 0
                while len(indices):
                    aktIndex = indices[i]
                    if aktIndex != index1 and aktIndex != index2 and sudoku.isCandidate(aktIndex, cand2):
                        if Sudoku2.buddies[aktIndex].contains(index1):
                            sees1 = True
                            self.wIndex1 = aktIndex
                        elif Sudoku2.buddies[aktIndex].contains(index2):
                            sees2 = True
                            self.wIndex2 = aktIndex
                    if sees1 and sees2:
                        break
                    i += 1
                if sees1 and sees2:
                    step = createWWingStep(cand1, cand2, index1, index2, elimSet, onlyOne)
                    if onlyOne and step != None:
                        return step
            constr += 1
        return None

    def createWWingStep(self, cand1, cand2, index1, index2, elimSet, onlyOne):
        """ generated source for method createWWingStep """
        self.globalStep.reset()
        self.globalStep.setType(SolutionType.W_WING)
        self.globalStep.addValue(cand1)
        self.globalStep.addValue(cand2)
        self.globalStep.addIndex(index1)
        self.globalStep.addIndex(index2)
        self.globalStep.addFin(index1, cand2)
        self.globalStep.addFin(index2, cand2)
        self.globalStep.addFin(self.wIndex1, cand2)
        self.globalStep.addFin(self.wIndex2, cand2)
        i = 0
        while i < len(elimSet):
            self.globalStep.addCandidateToDelete(elimSet.get(i), cand1)
            i += 1
        step = self.globalStep.clone()
        if onlyOne:
            return step
        else:
            self.steps.add(step)
        return None

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":0803:14:6..+9+5..7...+9.2.....58.+31...+1+64+3+8+9+7+52...1+7+59+46597+24+6..892+54+1+76+8+3...5+6+2.....68+93...::417 427 437 489 499::")
        sudoku.setSudoku(":0800:123:..+8+2..57.+7.+54....+8..9+8+57...4+5+17+2+98+6+3+2765+83+94+1+9+8+3+6+1+4+7+526+9+23+4+5+1+8+7537+168...+81+4+9+726+3+5::337::")
        solver = SudokuSolverFactory.getDefaultSolverInstance()
        step = solver.getHint(sudoku, False)
        print(step)
        print(sudoku.getSudoku(ClipboardMode.LIBRARY, step))
        System.exit(0)

