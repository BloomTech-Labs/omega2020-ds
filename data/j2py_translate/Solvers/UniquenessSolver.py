#!/usr/bin/env python
""" generated source for module UniquenessSolver_no_german """
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
class UniquenessSolver(AbstractSolver):
    """ generated source for class UniquenessSolver """
    #  An array vor caching constraint indices while searching for BUG +1 
    bugConstraints = [None] * 3

    #  One global step for optimization 
    globalStep = SolutionStep(SolutionType.FULL_HOUSE)

    #  All steps that were found in this search 
    steps = ArrayList()

    #  All already checked rectangles: One int aabbccdd with "aa"... the indices of the corners (sorted ascending) 
    rectangles = [None] * 400

    #  Current index in {@link #rectangles}. 
    rectAnz = 0

    #  Contains the indices of the current rectangle 
    indexe = [None] * 4

    #  Temporary array for sorting 
    tmpRect = [None] * 4

    #  The first candidate of the UR 
    cand1 = int()

    #  The second candidate of the UR 
    cand2 = int()

    #  A list of cached steps 
    cachedSteps = ArrayList()

    #  The {@link SudokuStepFinder#stepNumber} under which the cached steps were found 
    stepNumber = -1

    #  A set with all cells that hold only {@link #cand1} and/or {@link #cand2}. 
    twoCandidates = SudokuSet()

    #  A set with all cells that hold additional candidates 
    additionalCandidates = SudokuSet()

    #  A set for various checks 
    tmpSet = SudokuSet()

    #  A set for various checks 
    tmpSet1 = SudokuSet()

    #  A flag that indicates if the last search was for URs 
    lastSearchWasUR = False

    #  A flag that indicates if the last search was for ARs 
    lastSearchWasAR = False

    #  Creates a new instance of SimpleSolver
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(UniquenessSolver, self).__init__(finder)

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if sudoku.getStatus() != SudokuStatus.VALID:
            #  Uniqueness only for sudokus, that are strictly valid!
            return None
        if type_ == UNIQUENESS_1:
            pass
        elif type_ == UNIQUENESS_2:
            pass
        elif type_ == UNIQUENESS_3:
            pass
        elif type_ == UNIQUENESS_4:
            pass
        elif type_ == UNIQUENESS_5:
            pass
        elif type_ == UNIQUENESS_6:
            pass
        elif type_ == HIDDEN_RECTANGLE:
            result = getUniqueness(type_)
        elif type_ == AVOIDABLE_RECTANGLE_1:
            pass
        elif type_ == AVOIDABLE_RECTANGLE_2:
            if sudoku.getStatusGivens() != SudokuStatus.VALID:
                # only, if the givens themselves have only one solution!
                return None
            result = getAvoidableRectangle(type_)
        elif type_ == BUG_PLUS_1:
            result = getBugPlus1()
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == UNIQUENESS_1:
            pass
        elif step.getType() == UNIQUENESS_2:
            pass
        elif step.getType() == UNIQUENESS_3:
            pass
        elif step.getType() == UNIQUENESS_4:
            pass
        elif step.getType() == UNIQUENESS_5:
            pass
        elif step.getType() == UNIQUENESS_6:
            pass
        elif step.getType() == HIDDEN_RECTANGLE:
            pass
        elif step.getType() == AVOIDABLE_RECTANGLE_1:
            pass
        elif step.getType() == AVOIDABLE_RECTANGLE_2:
            pass
        elif step.getType() == BUG_PLUS_1:
            if step.getCandidatesToDelete().isEmpty():
                print("ERROR: No candidate to delete!")
                print(step.toString(2))
                print(sudoku.getSudoku(ClipboardMode.LIBRARY))
            for cand in step.getCandidatesToDelete():
                if not sudoku.isCandidate(cand.getIndex(), cand.getValue()):
                    print("ERROR: " + cand.getIndex() + "/" + cand.getValue())
                    print(step.toString(2))
                    print(sudoku.getSudoku(ClipboardMode.LIBRARY))
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    # 
    #      * Try to get an appropriate step from the cache {@link #cachedSteps}. If none is
    #      * available or the sudoku has changed since the last call find a new one. If no
    #      * step is found but the sudoku has not changed the already found and stored URs
    #      * ({@link #rectangles}) are not reset (they have already been searched and if a step
    #      * was in them it would have been cached).
    #      * @param type
    #      * @return
    #      
    def getUniqueness(self, type_):
        """ generated source for method getUniqueness """
        if finder.getStepNumber() == self.stepNumber and self.lastSearchWasUR:
            if len(self.cachedSteps) > 0:
                #  try to find the step in cachedSteps
                for step in cachedSteps:
                    if step.getType() == type_:
                        return step
        else:
            self.stepNumber = finder.getStepNumber()
            self.cachedSteps.clear()
            self.rectAnz = 0
        self.lastSearchWasUR = True
        self.lastSearchWasAR = False
        return getAllUniquenessInternal(type_, True)

    # 
    #      * More or less equal to {@link #getUniqueness(sudoku.SolutionType)}.
    #      * @param type
    #      * @return
    #      
    def getAvoidableRectangle(self, type_):
        """ generated source for method getAvoidableRectangle """
        if finder.getStepNumber() == self.stepNumber and self.lastSearchWasAR:
            if len(self.cachedSteps) > 0:
                #  try to find the step in cachedSteps
                for step in cachedSteps:
                    if step.getType() == type_:
                        return step
        else:
            self.stepNumber = finder.getStepNumber()
            self.cachedSteps.clear()
            self.rectAnz = 0
        self.lastSearchWasUR = False
        self.lastSearchWasAR = True
        return getAllAvoidableRectangles(type_, True)

    # 
    #      * Find all Uniqueness steps except BUG+1
    #      * @return
    #      
    def getAllUniqueness(self):
        """ generated source for method getAllUniqueness """
        self.stepNumber = -1
        self.cachedSteps.clear()
        self.rectAnz = 0
        self.lastSearchWasAR = False
        self.lastSearchWasUR = False
        sudoku = finder.getSudoku()
        tmpSteps = ArrayList()
        oldSteps = self.steps
        self.steps = tmpSteps
        getAllUniquenessInternal(None, False)
        getAllAvoidableRectangles(None, False)
        self.steps = oldSteps
        return tmpSteps

    # 
    #      * Find all available Avoidable Rectangles. If <code>onlyone</code> is
    #      * <code>true</code>, the first one found is returned.
    #      * @param type
    #      * @param onlyOne
    #      * @return
    #      
    def getAllAvoidableRectangles(self, type_, onlyOne):
        """ generated source for method getAllAvoidableRectangles """
        #  check for solved cells that are not givens
        i = 0
        while i < Sudoku2.LENGTH:
            if sudoku.getValue(i) == 0 or sudoku.isFixed(i):
                #  cell is either not solved or a given
                i += 1
                continue 
            self.cand1 = sudoku.getValue(i)
            step = findUniquenessForStartCell(i, True, type_, onlyOne)
            if step != None and onlyOne:
                return step
            step = findUniquenessForStartCell(i, True, type_, onlyOne)
            if step != None and onlyOne:
                return step
            i += 1
        return None

    # 
    #      * Find all bivalue cells and take them as starting point for a search.
    #      * the search itself is delegated to ....
    #      * @param type
    #      * @param onlyOne
    #      * @return
    #      
    def getAllUniquenessInternal(self, type_, onlyOne):
        """ generated source for method getAllUniquenessInternal """
        #  get bivalue cells
        i = 0
        while i < Sudoku2.LENGTH:
            if sudoku.getAnzCandidates(i) == 2:
                cands = sudoku.getAllCandidates(i)
                self.cand1 = cands[0]
                self.cand2 = cands[1]
                step = findUniquenessForStartCell(i, False, type_, onlyOne)
                if step != None and onlyOne:
                    return step
            i += 1
        return None

    # 
    #      * Only one cell exists with three candidates, all other cells have two candidates.
    #      * All candidates appear in all units exactly twice, except one of the candidates
    #      * in the cell with the three candidates.
    #      * @return
    #      
    def getBugPlus1(self):
        """ generated source for method getBugPlus1 """
        #  check the number of candidates in all cells
        index3 = -1
        i = 0
        while i < Sudoku2.LENGTH:
            anz = sudoku.getAnzCandidates(i)
            if anz > 3:
                #  no BUG+1!
                return None
            elif anz == 3:
                if index3 != -1:
                    #  second cell with three candidates -> no BUG+1!
                    return None
                index3 = i
            i += 1
        if index3 == -1:
            #  no cell with three candidates exists -> no BUG+1
            return None
        #  all cells have two candidates except one and that cell is index3
        #  -> check for possible BUG+1
        cand3 = -1
        self.bugConstraints[0] = -1
        self.bugConstraints[1] = -1
        self.bugConstraints[2] = -1
        free = sudoku.getFree()
        constr = 0
        while len(free):
            cand = 1
            while cand <= 9:
                anz = free[constr][cand]
                if anz > 3:
                    return None
                elif anz == 3:
                    if self.bugConstraints[constr / 9] != -1 or (cand3 != -1 and cand3 != cand):
                        return None
                    cand3 = cand
                    self.bugConstraints[constr / 9] = constr
                cand += 1
            constr += 1
        if sudoku.isCandidate(index3, cand3) and Sudoku2.CONSTRAINTS[index3][0] == self.bugConstraints[0] and Sudoku2.CONSTRAINTS[index3][1] == self.bugConstraints[1] and Sudoku2.CONSTRAINTS[index3][2] == self.bugConstraints[2]:
            self.globalStep.reset()
            self.globalStep.setType(SolutionType.BUG_PLUS_1)
            candArr = sudoku.getAllCandidates(index3)
            i = 0
            while len(candArr):
                if candArr[i] != cand3:
                    self.globalStep.addCandidateToDelete(index3, candArr[i])
                i += 1
            return self.globalStep.clone()
        return None

    def findUniquenessForStartCell(self, index11, avoidable, type_, onlyOne):
        """ generated source for method findUniquenessForStartCell """
        allowMissing = Options.getInstance().isAllowUniquenessMissingCandidates()
        line11 = Sudoku2.getLine(index11)
        col11 = Sudoku2.getCol(index11)
        block11 = Sudoku2.getBlock(index11)
        cell11 = sudoku.getCell(index11)
        allowedCand1 = finder.getCandidatesAllowed()[self.cand1]
        allowedCand2 = finder.getCandidatesAllowed()[self.cand2]
        blockIndices = Sudoku2.BLOCKS[Sudoku2.getBlock(index11)]
        i = 0
        while len(blockIndices):
            if blockIndices[i] == index11:
                i += 1
                continue 
            index12 = blockIndices[i]
            if line11 != Sudoku2.getLine(index12) and col11 != Sudoku2.getCol(index12):
                i += 1
                continue 
            cell12 = sudoku.getCell(index12)
            if (not avoidable and (sudoku.getValue(index12) == 0 and ((not allowMissing and (cell11 & cell12) == cell11) or (allowMissing and allowedCand1.contains(index12) and allowedCand2.contains(index12))))) or (avoidable and (sudoku.getValue(index12) != 0 and not sudoku.isFixed(index12))):
                if avoidable:
                    self.cand2 = sudoku.getValue(index12)
                isLines = line11 == Sudoku2.getLine(index12)
                unit11 = Sudoku2.ALL_UNITS[Sudoku2.getCol(index11) + 9 if isLines else Sudoku2.getLine(index11)]
                unit12 = Sudoku2.ALL_UNITS[Sudoku2.getCol(index12) + 9 if isLines else Sudoku2.getLine(index12)]
                j = 0
                while len(unit11):
                    if Sudoku2.getBlock(unit11[j]) == block11:
                        j += 1
                        continue 
                    index21 = unit11[j]
                    index22 = unit12[j]
                    cell21 = sudoku.getCell(index21)
                    cell22 = sudoku.getCell(index22)
                    if (not avoidable and (not allowMissing and (cell21 & cell11) == cell11 and (cell22 & cell11) == cell11)) or (allowMissing and allowedCand1.contains(index21) and allowedCand1.contains(index22) and allowedCand2.contains(index22) and allowedCand2.contains(index22)) or (avoidable and ((sudoku.getValue(index21) == self.cand2 and not sudoku.isFixed(index21) and sudoku.getValue(index22) == 0 and sudoku.isCandidate(index22, self.cand1) and sudoku.getAnzCandidates(index22) == 2) or (sudoku.getValue(index22) == self.cand1 and not sudoku.isFixed(index22) and sudoku.getValue(index21) == 0 and sudoku.isCandidate(index21, self.cand2) and sudoku.getAnzCandidates(index21) == 2) or (sudoku.getValue(index21) == 0 and sudoku.isCandidate(index21, self.cand2) and sudoku.getAnzCandidates(index21) == 2 and sudoku.getValue(index22) == 0 and sudoku.isCandidate(index22, self.cand1) and sudoku.getAnzCandidates(index22) == 2))):
                        if checkRect(index11, index12, index21, index22):
                            self.indexe[0] = index11
                            self.indexe[1] = index12
                            self.indexe[2] = index21
                            self.indexe[3] = index22
                            step = None
                            if avoidable:
                                step = checkAvoidableRectangle(index21, index22, type_, onlyOne)
                            else:
                                step = checkURForStep(type_, onlyOne)
                            if step != None and onlyOne:
                                return step
                    j += 1
            i += 1
        return None

    def checkURForStep(self, searchType, onlyOne):
        """ generated source for method checkURForStep """
        initCheck(self.indexe)
        step = None
        twoSize = len(self.twoCandidates)
        urMask = int((Sudoku2.MASKS[self.cand1] | Sudoku2.MASKS[self.cand2]))
        if twoSize == 3:
            initStep(SolutionType.UNIQUENESS_1)
            delIndex = self.additionalCandidates.get(0)
            if sudoku.isCandidate(delIndex, self.cand1):
                self.globalStep.addCandidateToDelete(delIndex, self.cand1)
            if sudoku.isCandidate(delIndex, self.cand2):
                self.globalStep.addCandidateToDelete(delIndex, self.cand2)
            if self.globalStep.getCandidatesToDelete().size() > 0:
                step = self.globalStep.clone()
                if onlyOne:
                    if searchType == step.getType():
                        return step
                    else:
                        self.cachedSteps.add(step)
                else:
                    self.steps.add(step)
        if twoSize == 2 or twoSize == 1:
            addMask = 0
            self.tmpSet.setAll()
            i = 0
            while i < len(self.additionalCandidates):
                index3 = self.additionalCandidates.get(i)
                addMask |= int((sudoku.getCell(index3) & ~urMask))
                if Sudoku2.ANZ_VALUES[addMask] > 1:
                    break
                self.tmpSet.and_(Sudoku2.buddies[index3])
                i += 1
            if Sudoku2.ANZ_VALUES[addMask] == 1:
                addCand = Sudoku2.CAND_FROM_MASK[addMask]
                self.tmpSet.and_(finder.getCandidates()[addCand])
                if not self.tmpSet.isEmpty():
                    type_ = SolutionType.UNIQUENESS_2
                    i1 = self.additionalCandidates.get(0)
                    i2 = self.additionalCandidates.get(1)
                    if len(self.additionalCandidates) == 3 or (Sudoku2.getLine(i1) != Sudoku2.getLine(i2) and Sudoku2.getCol(i1) != Sudoku2.getCol(i2)):
                        type_ = SolutionType.UNIQUENESS_5
                    initStep(type_)
                    i = 0
                    while i < len(self.tmpSet):
                        self.globalStep.addCandidateToDelete(self.tmpSet.get(i), addCand)
                        i += 1
                    step = self.globalStep.clone()
                    if onlyOne:
                        if searchType == step.getType():
                            return step
                        else:
                            self.cachedSteps.add(step)
                    else:
                        self.steps.add(step)
        if twoSize == 2:
            u3Cands = 0
            i = 0
            while i < len(self.additionalCandidates):
                index3 = self.additionalCandidates.get(i)
                u3Cands |= int((sudoku.getCell(index3) & ~urMask))
                i += 1
            i1 = self.additionalCandidates.get(0)
            i2 = self.additionalCandidates.get(1)
            if Sudoku2.getLine(i1) == Sudoku2.getLine(i2):
                step = checkUniqueness3(Sudoku2.LINE, Sudoku2.LINES[Sudoku2.getLine(i1)], u3Cands, urMask, searchType, onlyOne)
                if step != None and onlyOne:
                    return step
            if Sudoku2.getCol(i1) == Sudoku2.getCol(i2):
                step = checkUniqueness3(Sudoku2.COL, Sudoku2.COLS[Sudoku2.getCol(i1)], u3Cands, urMask, searchType, onlyOne)
                if step != None and onlyOne:
                    return step
            if Sudoku2.getBlock(i1) == Sudoku2.getBlock(i2):
                step = checkUniqueness3(Sudoku2.BLOCK, Sudoku2.BLOCKS[Sudoku2.getBlock(i1)], u3Cands, urMask, searchType, onlyOne)
                if step != None and onlyOne:
                    return step
        if twoSize == 2:
            i1 = self.additionalCandidates.get(0)
            i2 = self.additionalCandidates.get(1)
            if (Sudoku2.getLine(i1) == Sudoku2.getLine(i2)) or (Sudoku2.getCol(i1) == Sudoku2.getCol(i2)):
                self.tmpSet.setAnd(Sudoku2.buddies[i1], Sudoku2.buddies[i2])
                delCand = -1
                self.tmpSet1.setAnd(self.tmpSet, finder.getCandidates()[self.cand1])
                if self.tmpSet1.isEmpty():
                    delCand = self.cand2
                else:
                    self.tmpSet1.setAnd(self.tmpSet, finder.getCandidates()[self.cand2])
                    if self.tmpSet1.isEmpty():
                        delCand = self.cand1
                if delCand != -1:
                    initStep(SolutionType.UNIQUENESS_4)
                    if sudoku.isCandidate(i1, delCand):
                        self.globalStep.addCandidateToDelete(i1, delCand)
                    if sudoku.isCandidate(i2, delCand):
                        self.globalStep.addCandidateToDelete(i2, delCand)
                    if self.globalStep.getCandidatesToDelete().size() > 0:
                        step = self.globalStep.clone()
                        if onlyOne:
                            if searchType == step.getType():
                                return step
                            else:
                                self.cachedSteps.add(step)
                        else:
                            self.steps.add(step)
        if twoSize == 2:
            i1 = self.additionalCandidates.get(0)
            i2 = self.additionalCandidates.get(1)
            if (Sudoku2.getLine(i1) != Sudoku2.getLine(i2)) and (Sudoku2.getCol(i1) != Sudoku2.getCol(i2)):
                self.tmpSet.set(Sudoku2.LINE_TEMPLATES[Sudoku2.getLine(i1)])
                self.tmpSet.or_(Sudoku2.COL_TEMPLATES[Sudoku2.getCol(i1)])
                self.tmpSet.or_(Sudoku2.LINE_TEMPLATES[Sudoku2.getLine(i2)])
                self.tmpSet.or_(Sudoku2.COL_TEMPLATES[Sudoku2.getCol(i2)])
                self.tmpSet.andNot(self.additionalCandidates)
                self.tmpSet.andNot(self.twoCandidates)
                delCand = -1
                self.tmpSet1.setAnd(self.tmpSet, finder.getCandidates()[self.cand1])
                if self.tmpSet1.isEmpty():
                    delCand = self.cand1
                else:
                    self.tmpSet1.setAnd(self.tmpSet, finder.getCandidates()[self.cand2])
                    if self.tmpSet1.isEmpty():
                        delCand = self.cand2
                if delCand != -1:
                    initStep(SolutionType.UNIQUENESS_6)
                    if sudoku.isCandidate(i1, delCand):
                        self.globalStep.addCandidateToDelete(i1, delCand)
                    if sudoku.isCandidate(i2, delCand):
                        self.globalStep.addCandidateToDelete(i2, delCand)
                    if self.globalStep.getCandidatesToDelete().size() > 0:
                        step = self.globalStep.clone()
                        if onlyOne:
                            if searchType == step.getType():
                                return step
                            else:
                                self.cachedSteps.add(step)
                        else:
                            self.steps.add(step)
        if twoSize == 2 or twoSize == 1:
            i1 = self.twoCandidates.get(0)
            i2 = self.twoCandidates.get(1)
            doCheck = True
            if twoSize == 2:
                if Sudoku2.getLine(i1) == Sudoku2.getLine(i2) or Sudoku2.getCol(i1) == Sudoku2.getCol(i2):
                    doCheck = False
            if doCheck:
                step = checkHiddenRectangle(i1, searchType, onlyOne)
                if step != None and onlyOne:
                    return step
                if len(self.twoCandidates) == 2:
                    step = checkHiddenRectangle(i2, searchType, onlyOne)
                    if step != None and onlyOne:
                        return step
        return None

    def checkAvoidableRectangle(self, index21, index22, type_, onlyOne):
        """ generated source for method checkAvoidableRectangle """
        step = None
        if sudoku.getValue(index21) != 0 or sudoku.getValue(index22) != 0:
            initStep(SolutionType.AVOIDABLE_RECTANGLE_1)
            if sudoku.getValue(index21) != 0:
                if sudoku.isCandidate(index22, self.cand1):
                    self.globalStep.addCandidateToDelete(index22, self.cand1)
            else:
                if sudoku.isCandidate(index21, self.cand2):
                    self.globalStep.addCandidateToDelete(index21, self.cand2)
            if self.globalStep.getCandidatesToDelete().size() > 0:
                step = self.globalStep.clone()
                if onlyOne:
                    if type_ == SolutionType.AVOIDABLE_RECTANGLE_1:
                        return step
                    else:
                        self.cachedSteps.add(step)
                else:
                    self.steps.add(step)
        else:
            cands = sudoku.getAllCandidates(index21)
            additionalCand = cands[0]
            if additionalCand == self.cand2:
                additionalCand = cands[1]
            if not sudoku.isCandidate(index22, additionalCand):
                return None
            self.tmpSet.set(Sudoku2.buddies[index21])
            self.tmpSet.and_(Sudoku2.buddies[index22])
            self.tmpSet.and_(finder.getCandidates()[additionalCand])
            if self.tmpSet.isEmpty():
                return None
            initStep(SolutionType.AVOIDABLE_RECTANGLE_2)
            i = 0
            while i < len(self.tmpSet):
                self.globalStep.addCandidateToDelete(self.tmpSet.get(i), additionalCand)
                i += 1
            self.globalStep.addEndoFin(index21, additionalCand)
            self.globalStep.addEndoFin(index22, additionalCand)
            step = self.globalStep.clone()
            if onlyOne:
                if type_ == SolutionType.AVOIDABLE_RECTANGLE_2:
                    return step
                else:
                    self.cachedSteps.add(step)
            else:
                self.steps.add(step)
        return None

    def checkHiddenRectangle(self, cornerIndex, type_, onlyOne):
        """ generated source for method checkHiddenRectangle """
        lineC = Sudoku2.getLine(cornerIndex)
        colC = Sudoku2.getCol(cornerIndex)
        i1 = self.additionalCandidates.get(0)
        i2 = self.additionalCandidates.get(1)
        line1 = Sudoku2.getLine(i1)
        if line1 == lineC:
            line1 = Sudoku2.getLine(i2)
        col1 = Sudoku2.getCol(i1)
        if col1 == colC:
            col1 = Sudoku2.getCol(i2)
        step = checkCandForHiddenRectangle(line1, col1, self.cand1, self.cand2, type_, onlyOne)
        if step != None and onlyOne:
            return step
        step = checkCandForHiddenRectangle(line1, col1, self.cand2, self.cand1, type_, onlyOne)
        if step != None and onlyOne:
            return step
        return None

    def checkCandForHiddenRectangle(self, line, col, cand1, cand2, type_, onlyOne):
        """ generated source for method checkCandForHiddenRectangle """
        self.tmpSet1.setOr(self.twoCandidates, self.additionalCandidates)
        self.tmpSet.set(finder.getCandidates()[cand1])
        self.tmpSet.and_(Sudoku2.LINE_TEMPLATES[line])
        self.tmpSet.andNot(self.tmpSet1)
        if not self.tmpSet.isEmpty():
            return None
        self.tmpSet.set(finder.getCandidates()[cand1])
        self.tmpSet.and_(Sudoku2.COL_TEMPLATES[col])
        self.tmpSet.andNot(self.tmpSet1)
        if not self.tmpSet.isEmpty():
            return None
        delIndex = Sudoku2.getIndex(line, col)
        initStep(SolutionType.HIDDEN_RECTANGLE)
        if sudoku.isCandidate(delIndex, cand2):
            self.globalStep.addCandidateToDelete(delIndex, cand2)
        if self.globalStep.getCandidatesToDelete().size() > 0:
            step = self.globalStep.clone()
            if onlyOne:
                if type_ == step.getType():
                    return step
                else:
                    self.cachedSteps.add(step)
            else:
                self.steps.add(step)
        return None

    def checkUniqueness3(self, unitType, unit, u3Cands, urMask, searchType, onlyOne):
        """ generated source for method checkUniqueness3 """
        u3Indices = SudokuSet()
        self.tmpSet.set(self.twoCandidates)
        self.tmpSet.or_(self.additionalCandidates)
        i = 0
        while len(unit):
            cell = sudoku.getCell(unit[i])
            if cell != 0 and (cell & urMask) == 0 and not self.tmpSet.contains(unit[i]):
                u3Indices.add(unit[i])
            i += 1
        if not u3Indices.isEmpty():
            step = checkUniqueness3Recursive(unitType, unit, u3Indices, u3Cands, SudokuSet(self.additionalCandidates), 0, searchType, onlyOne)
            if step != None and onlyOne:
                return step
        return None

    def checkUniqueness3Recursive(self, type_, unit, u3Indices, candsIncluded, indicesIncluded, startIndex, searchType, onlyOne):
        """ generated source for method checkUniqueness3Recursive """
        step = None
        i = startIndex
        while i < len(u3Indices):
            aktCands = candsIncluded
            aktIndices = indicesIncluded.clone()
            aktIndices.add(u3Indices.get(i))
            aktCands |= sudoku.getCell(u3Indices.get(i))
            if type_ != Sudoku2.BLOCK or not isSameLineOrCol(aktIndices):
                if Sudoku2.ANZ_VALUES[aktCands] == (len(aktIndices) - 1):
                    initStep(SolutionType.UNIQUENESS_3)
                    j = 0
                    while len(unit):
                        if sudoku.getValue(unit[j]) == 0 and not aktIndices.contains(unit[j]):
                            delCands = int((sudoku.getCell(unit[j]) & aktCands))
                            if Sudoku2.ANZ_VALUES[delCands] == 0:
                                j += 1
                                continue 
                            delCandsArray = Sudoku2.POSSIBLE_VALUES[delCands]
                            k = 0
                            while len(delCandsArray):
                                self.globalStep.addCandidateToDelete(unit[j], delCandsArray[k])
                                k += 1
                        j += 1
                    if self.globalStep.getCandidatesToDelete().size() > 0:
                        aktCandsArray = Sudoku2.POSSIBLE_VALUES[aktCands]
                        k = 0
                        while len(aktCandsArray):
                            cTmp = aktCandsArray[k]
                            l = 0
                            while l < len(aktIndices):
                                if sudoku.isCandidate(aktIndices.get(l), cTmp):
                                    self.globalStep.addFin(aktIndices.get(l), cTmp)
                                l += 1
                            k += 1
                        if type_ == Sudoku2.LINE or type_ == Sudoku2.COL:
                            block = getBlockForCheck3(aktIndices)
                            if block != -1:
                                unit1 = Sudoku2.BLOCKS[block]
                                j = 0
                                while len(unit1):
                                    if sudoku.getValue(unit1[j]) == 0 and not aktIndices.contains(unit1[j]):
                                        delCands = int((sudoku.getCell(unit1[j]) & aktCands))
                                        if Sudoku2.ANZ_VALUES[delCands] == 0:
                                            j += 1
                                            continue 
                                        delCandsArray = Sudoku2.POSSIBLE_VALUES[delCands]
                                        k = 0
                                        while len(delCandsArray):
                                            self.globalStep.addCandidateToDelete(unit1[j], delCandsArray[k])
                                            k += 1
                                    j += 1
                        step = self.globalStep.clone()
                        if onlyOne:
                            if searchType == step.getType():
                                return step
                            else:
                                self.cachedSteps.add(step)
                        else:
                            self.steps.add(step)
            step = self.checkUniqueness3Recursive(type_, unit, u3Indices, aktCands, aktIndices, i + 1, searchType, onlyOne)
            if step != None and onlyOne:
                return step
            i += 1
        return None

    def getBlockForCheck3(self, aktIndices):
        """ generated source for method getBlockForCheck3 """
        if aktIndices.isEmpty():
            return -1
        block = Sudoku2.getBlock(aktIndices.get(0))
        i = 1
        while i < len(aktIndices):
            if Sudoku2.getBlock(aktIndices.get(i)) != block:
                return -1
            i += 1
        return block

    def isSameLineOrCol(self, aktIndices):
        """ generated source for method isSameLineOrCol """
        if aktIndices.isEmpty():
            return False
        sameLine = True
        sameCol = True
        line = Sudoku2.getLine(aktIndices.get(0))
        col = Sudoku2.getCol(aktIndices.get(0))
        i = 1
        while i < len(aktIndices):
            if Sudoku2.getLine(aktIndices.get(i)) != line:
                sameLine = False
            if Sudoku2.getCol(aktIndices.get(i)) != col:
                sameCol = False
            i += 1
        return sameLine or sameCol

    def initStep(self, type_):
        """ generated source for method initStep """
        self.globalStep.reset()
        self.globalStep.setType(type_)
        if self.indexe != None:
            self.globalStep.addValue(self.cand1)
            self.globalStep.addValue(self.cand2)
            self.globalStep.addIndex(self.indexe[0])
            self.globalStep.addIndex(self.indexe[1])
            self.globalStep.addIndex(self.indexe[2])
            self.globalStep.addIndex(self.indexe[3])

    def initCheck(self, indices):
        """ generated source for method initCheck """
        self.twoCandidates.clear()
        self.additionalCandidates.clear()
        mask = int(~(Sudoku2.MASKS[self.cand1] | Sudoku2.MASKS[self.cand2]))
        i = 0
        while len(indices):
            addTemp = int((sudoku.getCell(indices[i]) & mask))
            if addTemp == 0:
                self.twoCandidates.add(indices[i])
            else:
                self.additionalCandidates.add(indices[i])
            i += 1

    def checkRect(self, i11, i12, i21, i22):
        """ generated source for method checkRect """
        self.tmpRect[0] = i11
        self.tmpRect[1] = i12
        self.tmpRect[2] = i21
        self.tmpRect[3] = i22
        i = int()
        while i > 1:
            changed = False
            j = 1
            while j < i:
                if self.tmpRect[j - 1] > self.tmpRect[j]:
                    tmp = self.tmpRect[j - 1]
                    self.tmpRect[j - 1] = self.tmpRect[j]
                    self.tmpRect[j] = tmp
                    changed = True
                j += 1
            if changed == False:
                break
            i -= 1
        rect = (((self.tmpRect[0] * 10) + self.tmpRect[1]) * 10 + self.tmpRect[2]) * 10 + self.tmpRect[3]
        i = 0
        while i < self.rectAnz:
            if self.rectangles[i] == rect:
                return False
            i += 1
        if len(rectangles):
        __rectAnz_0 = rectAnz
        rectAnz += 1
            self.rectangles[__rectAnz_0] = rect
        else:
            Logger.getLogger(getClass().__name__).log(Level.WARNING, "Find Uniqueness: Kein Platz mehr in rectangles!")
        return True

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":0000:x:..513.9.2..1..97..89..2.4..45.29.136962351847.1...6..9.349...78...8..39..89.736..:625 271 571 485::")
        sudoku.setSudoku(":0000:x:+41+67+8.5...35..4+8+178+7.+13+5.+46..4+5716..+1.3+4..7.+5+6+5789+34+2+15+4..1+7.+683.+82+5.17+4+7.1.+48.5.:942 948 252 297 399::")
        sudoku.setSudoku(":0610::8+4+9325+6+1+77+3+2+8..9+4+5+5+6+1+7..+32+8+49327+85+61+1+5+7.3.8+9+2+2+86...+4+7+3+9+7+8..+213+4+3+149+87+2566+2+5..+3+7+8+9::565 965::")
        sudoku.setSudoku(":0610::+1+4.+7+8...+9+2+8.+4+5.1.73+7.6+1...+89+5+38+7+1..+2+72+4+9+6+581+3+86+1+324+9+7+5+6+18+2+3759+4+5+971+4+832+64+3+2596+7+8+1::318 518::")
        sudoku.setSudoku(":0600:13:+5+2+3+9+7+8+1466+1+832+4...+4+7+9+5+6+1+38+29+5+1+6+32.+7.+86+2+49+7+5..+7+34+18526+9+38+7+21....295+8+4....+14+67+5..+2.::189 389::")
        sudoku.setSudoku(":0601:12:....6..2.394...7..2.+6..41....2....4..6.8........6.9....4...739...1.8...2.+2....51.:114 116 819 829 839 849 869 574 575 581 582 495:514 516 526 528 529 534 535::")
        sudoku.setSudoku(":0602:15:+7+1+3+4+5+862+9+4927+63..+8+8+6+51+9+2374+67158+9+4+3+2+9+5+42+3+7+8+612+386+4+1+7+9+5.8..+1.+24+71+47.+2.....+2..+74...::391::")
        sudoku.setSudoku(":0602:16:..3.+1+6.9...78....6.6......1....+8.......45....45..61..7..81.926.9....3........8.1.:514 225 425 226 334 534 934 235 435 735 236 736 244 744 347 447 547 947 248 348 249 349 949 357 857 957 858 859 264 284 784 294 794:233 241 242 251 252 283 293 933 942 952::")
        sudoku.setSudoku(":0602:57:+54.........72+4.5..9.....+463...964.....5...+6........1.281...7........5+7867+5.3.....:213 613 714 715 626 134 834 135 835 151 251 252 663 568 373 195 196:355 356 361 362 363 368 854 855 856 862 863:")
        sudoku.setSudoku(":0603:48:+3+9+6+17+52+8481+4+29+63..5+27.+8.+1+6+9..+5+9.2..1+2.38.19..9.+16.+7...+1.+2+7+6.5+98..8.2+9+7137.9.1+8...:448 465 468 492 692 494:442 447::")
        sudoku.setSudoku(":0608:12:......+531.96...7+425.....+6+9+8......8..7.94..+1.+3....329..+9..+1+28+3+65+832.5.+41+9+6+51+3+49+287:814 815 141 142:714 715 716 732 733 736::")
        sudoku.setSudoku(":0606:34:.51.+8..4+2....2.3...........3..8.+29.....5.4......1.+9+4.....7+5+6+214.6.+29....2........:432 732 832 932 433 633 733 833 933 334 335 635 735 336 881 383 883 392 492 892 992 393 493 893 993 395:435::")
        solver = SudokuSolverFactory.getDefaultSolverInstance()
        finder = solver.getStepFinder()
        singleHint = False
        if singleHint:
            finder.setSudoku(sudoku)
            step = finder.getStep(SolutionType.BUG_PLUS_1)
            print(step)
        else:
            steps = solver.getStepFinder().getAllUniqueness(sudoku)
            solver.getStepFinder().printStatistics()
            if len(cls.steps) > 0:
                Collections.sort(cls.steps)
                for actStep in steps:
                    print(actStep)
        System.exit(0)

