#!/usr/bin/env python
""" generated source for module SimpleSolver """
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
class SimpleSolver(AbstractSolver):
    """ generated source for class SimpleSolver """
    #  Flags that indicate, if a search for all Hidden Singles was already successful. 
    singleFound = [None] * Sudoku2.LENGTH

    #  The list with all newly found steps. 
    steps = None

    #  One global instance of {@link SolutionStep}. Reduces the number of unnecessarily created objects. 
    globalStep = SolutionStep()

    #  Buffer for checking for locked Subsets. 
    sameConstraint = [None] * 

    #  Buffer for checking for locked Subsets. 
    foundConstraint = [None] * 

    #  Buffer for checking for locked Subsets. 
    constraint = [None] * 

    #  Buffer for subset check. 
    indices2 = [None] * 2

    #  Buffer for subset check. 
    indices3 = [None] * 3

    #  Buffer for subset check. 
    indices4 = [None] * 4

    #  Cache for steps that were found but cannot be used right now 
    cachedSteps = ArrayList()

    #  {@link SudokuStepFinder#stepNumber} that was valid when {@link #cachedSteps} was filled. 
    cachedStepsNumber = -1

    #  Temporary array for holding cell indices 
    tmpArr1 = [None] * 9

    #  Bitmaps for indices per candidate in one unit. 
    ipcMask = [None] * 10

    #  Creates a new instance of SimpleSolver
    #      * @param finder 
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(SimpleSolver, self).__init__(finder)
        self.steps = ArrayList()

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == FULL_HOUSE:
            result = findFullHouse(False)
        elif type_ == HIDDEN_SINGLE:
            result = findHiddenSingle()
        elif type_ == HIDDEN_PAIR:
            result = findHiddenXle(2)
        elif type_ == HIDDEN_TRIPLE:
            result = findHiddenXle(3)
        elif type_ == HIDDEN_QUADRUPLE:
            result = findHiddenXle(4)
        elif type_ == NAKED_SINGLE:
            result = findNakedSingle()
        elif type_ == LOCKED_PAIR:
            result = findNakedXle(2, True)
        elif type_ == NAKED_PAIR:
            result = findNakedXle(2, False)
        elif type_ == LOCKED_TRIPLE:
            result = findNakedXle(3, True)
        elif type_ == NAKED_TRIPLE:
            result = findNakedXle(3, False)
        elif type_ == NAKED_QUADRUPLE:
            result = findNakedXle(4, False)
        elif type_ == LOCKED_CANDIDATES:
            pass
        elif type_ == LOCKED_CANDIDATES_1:
            pass
        elif type_ == LOCKED_CANDIDATES_2:
            result = findLockedCandidates(type_)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == FULL_HOUSE:
            pass
        elif step.getType() == HIDDEN_SINGLE:
            pass
        elif step.getType() == NAKED_SINGLE:
            sudoku.setCell(step.getIndices().get(0), step.getValues().get(0))
        elif step.getType() == HIDDEN_PAIR:
            pass
        elif step.getType() == HIDDEN_TRIPLE:
            pass
        elif step.getType() == HIDDEN_QUADRUPLE:
            pass
        elif step.getType() == NAKED_PAIR:
            pass
        elif step.getType() == NAKED_TRIPLE:
            pass
        elif step.getType() == NAKED_QUADRUPLE:
            pass
        elif step.getType() == LOCKED_PAIR:
            pass
        elif step.getType() == LOCKED_TRIPLE:
            pass
        elif step.getType() == LOCKED_CANDIDATES:
            pass
        elif step.getType() == LOCKED_CANDIDATES_1:
            pass
        elif step.getType() == LOCKED_CANDIDATES_2:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
                #                     SudokuCell cell = sudoku.getCell(cand.index);
                #                     cell.delCandidate(candType, cand.value);
        else:
            handled = False
        return handled

    # 
    #      * Finds and returns all Full Houses present in the grid.
    #      * @return
    #      
    def findAllFullHouses(self):
        """ generated source for method findAllFullHouses """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findFullHouse(True)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    # 
    #      * Full House: Last unset cell in an entity<br>
    #      * A Full House is always also a Naked Single. The method therefore
    #      * traverses the Naked Single queue and checks the number of candidates
    #      * for all other candidates in the constraint.
    #      * @param all If <code>true</code>, all Full houses are returned
    #      * @return
    #      
    def findFullHouse(self, all):
        """ generated source for method findFullHouse """
        # SudokuUtil.clearStepList(steps);
        step = None
        free = sudoku.getFree()
        nsQueue = sudoku.getNsQueue()
        queueIndex = nsQueue.getFirstIndex()
        while queueIndex != -1:
            index = nsQueue.getIndex(queueIndex)
            value = nsQueue.getValue(queueIndex)
            if sudoku.getValue(index) == 0:
                #  cell is still a valid Naked Single -> check constraints
                #  the cell is a member of three constraints
                i = 0
                while len(length):
                    constr = Sudoku2.CONSTRAINTS[index][i]
                    valid = True
                    j = 1
                    while j <= 9:
                        if j != value and free[constr][j] != 0:
                            valid = False
                            break
                        j += 1
                    if valid:
                        step = SolutionStep(SolutionType.FULL_HOUSE)
                        step.addValue(value)
                        step.addIndex(index)
                        if all:
                            self.steps.add(step)
                            break
                        else:
                            return step
                    i += 1
            queueIndex = nsQueue.getNextIndex()
        return step

    def findNakedSingle(self):
        """ generated source for method findNakedSingle """
        step = None
        nsQueue = sudoku.getNsQueue()
        queueIndex = -1
        while (queueIndex = nsQueue.getSingle()) != -1:
            index = nsQueue.getIndex(queueIndex)
            value = nsQueue.getValue(queueIndex)
            if sudoku.getValue(index) == 0:
                step = SolutionStep(SolutionType.NAKED_SINGLE)
                step.addValue(value)
                step.addIndex(index)
                break
        return step

    def findAllNakedSingles(self):
        """ generated source for method findAllNakedSingles """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        nsQueue = sudoku.getNsQueue()
        queueIndex = nsQueue.getFirstIndex()
        while queueIndex != -1:
            index = nsQueue.getIndex(queueIndex)
            value = nsQueue.getValue(queueIndex)
            if sudoku.getValue(index) == 0:
                step = SolutionStep(SolutionType.NAKED_SINGLE)
                step.addValue(value)
                step.addIndex(index)
                self.steps.add(step)
            queueIndex = nsQueue.getNextIndex()
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findNakedXle(self, anz, lockedOnly):
        """ generated source for method findNakedXle """
        SudokuUtil.clearStepList(self.steps)
        if len(self.cachedSteps) > 0 and self.cachedStepsNumber == finder.getStepNumber():
            type_ = SolutionType.NAKED_PAIR
            if anz == 2 and lockedOnly:
                type_ = SolutionType.LOCKED_PAIR
            if anz == 3 and not lockedOnly:
                type_ = SolutionType.NAKED_TRIPLE
            if anz == 3 and lockedOnly:
                type_ = SolutionType.LOCKED_TRIPLE
            if anz == 4:
                type_ = SolutionType.NAKED_QUADRUPLE
            for step in cachedSteps:
                if step.getType() == type_:
                    return step
        self.cachedSteps.clear()
        self.cachedStepsNumber = finder.getStepNumber()
        step = findNakedXleInEntity(Sudoku2.BLOCKS, anz, lockedOnly, not lockedOnly, True)
        if step != None or lockedOnly:
            return step
        step = findNakedXleInEntity(Sudoku2.LINES, anz, lockedOnly, not lockedOnly, True)
        if step != None:
            return step
        step = findNakedXleInEntity(Sudoku2.COLS, anz, lockedOnly, not lockedOnly, True)
        return step

    def findAllNakedXle(self):
        """ generated source for method findAllNakedXle """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        tmpSteps = self.findAllNakedSingles()
        self.steps.addAll(tmpSteps)
        i = 2
        while i <= 4:
            findNakedXleInEntity(Sudoku2.BLOCKS, i, False, False, False)
            findNakedXleInEntity(Sudoku2.LINES, i, False, False, False)
            findNakedXleInEntity(Sudoku2.COLS, i, False, False, False)
            i += 1
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findNakedXleInEntity(self, indices, anz, lockedOnly, nakedOnly, onlyOne):
        """ generated source for method findNakedXleInEntity """
        step = None
        entity = 0
        while len(indices):
        __maxIndex_0 = maxIndex
        maxIndex += 1
            maxIndex = 0
            i = 0
            while len(length):
                tmpAnz = Sudoku2.ANZ_VALUES[sudoku.getCell(indices[entity][i])]
                if tmpAnz != 0 and tmpAnz <= anz:
                    self.tmpArr1[__maxIndex_0] = indices[entity][i]
                i += 1
            if maxIndex < anz:
                entity += 1
                continue 
            i1 = 0
            while i1 < maxIndex - anz + 1:
                cell1 = sudoku.getCell(self.tmpArr1[i1])
                i2 = i1 + 1
                while i2 < maxIndex - anz + 2:
                    cell2 = int((cell1 | sudoku.getCell(self.tmpArr1[i2])))
                    if Sudoku2.ANZ_VALUES[cell2] > anz:
                        i2 += 1
                        continue 
                    if anz == 2:
                        if Sudoku2.ANZ_VALUES[cell2] == anz:
                            step = createSubsetStep(self.tmpArr1[i1], self.tmpArr1[i2], -1, -1, cell2, SolutionType.NAKED_PAIR, lockedOnly, nakedOnly)
                            if step != None and onlyOne:
                                return step
                    else:
                        i3 = i2 + 1
                        while i3 < maxIndex - anz + 3:
                            cell3 = int((cell2 | sudoku.getCell(self.tmpArr1[i3])))
                            if Sudoku2.ANZ_VALUES[cell3] > anz:
                                i3 += 1
                                continue 
                            if anz == 3:
                                if Sudoku2.ANZ_VALUES[cell3] == anz:
                                    step = createSubsetStep(self.tmpArr1[i1], self.tmpArr1[i2], self.tmpArr1[i3], -1, cell3, SolutionType.NAKED_TRIPLE, lockedOnly, nakedOnly)
                                    if step != None and onlyOne:
                                        return step
                            else:
                                i4 = i3 + 1
                                while i4 < maxIndex:
                                    cell4 = int((cell3 | sudoku.getCell(self.tmpArr1[i4])))
                                    if Sudoku2.ANZ_VALUES[cell4] > anz:
                                        i4 += 1
                                        continue 
                                    if Sudoku2.ANZ_VALUES[cell4] == anz:
                                        step = createSubsetStep(self.tmpArr1[i1], self.tmpArr1[i2], self.tmpArr1[i3], self.tmpArr1[i4], cell4, SolutionType.NAKED_QUADRUPLE, lockedOnly, nakedOnly)
                                        if step != None and onlyOne:
                                            return step
                                    i4 += 1
                            i3 += 1
                    i2 += 1
                i1 += 1
            entity += 1
        return None

    def findHiddenSingle(self):
        """ generated source for method findHiddenSingle """
        step = None
        free = sudoku.getFree()
        hsQueue = sudoku.getHsQueue()
        queueIndex = -1
        while (queueIndex = hsQueue.getSingle()) != -1:
            index = hsQueue.getIndex(queueIndex)
            value = hsQueue.getValue(queueIndex)
            if sudoku.getValue(index) == 0:
                i = 0
                while len(length):
                    if free[Sudoku2.CONSTRAINTS[index][i]][value] == 1:
                        step = SolutionStep(SolutionType.HIDDEN_SINGLE)
                        step.addValue(value)
                        step.addIndex(index)
                        break
                    i += 1
                break
        return step

    def findAllHiddenSingles(self):
        """ generated source for method findAllHiddenSingles """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        Arrays.fill(self.singleFound, False)
        free = sudoku.getFree()
        hsQueue = sudoku.getHsQueue()
        queueIndex = hsQueue.getFirstIndex()
        while queueIndex != -1:
            index = hsQueue.getIndex(queueIndex)
            value = hsQueue.getValue(queueIndex)
            if sudoku.getValue(index) == 0 and not self.singleFound[index]:
                i = 0
                while len(length):
                    if free[Sudoku2.CONSTRAINTS[index][i]][value] == 1:
                        step = SolutionStep(SolutionType.HIDDEN_SINGLE)
                        step.addValue(value)
                        step.addIndex(index)
                        step.setEntity(i)
                        self.steps.add(step)
                        self.singleFound[index] = True
                        break
                    i += 1
            queueIndex = hsQueue.getNextIndex()
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findAllHiddenXle(self):
        """ generated source for method findAllHiddenXle """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        tmpSteps = self.findAllHiddenSingles()
        self.steps.addAll(tmpSteps)
        i = 2
        while i <= 4:
            findHiddenXleInEntity(2 * Sudoku2.UNITS, Sudoku2.BLOCKS, i, False)
            findHiddenXleInEntity(0, Sudoku2.LINES, i, False)
            findHiddenXleInEntity(Sudoku2.UNITS, Sudoku2.COLS, i, False)
            i += 1
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findHiddenXle(self, anz):
        """ generated source for method findHiddenXle """
        SudokuUtil.clearStepList(self.steps)
        step = findHiddenXleInEntity(2 * Sudoku2.UNITS, Sudoku2.BLOCKS, anz, True)
        if step != None:
            return step
        step = findHiddenXleInEntity(0, Sudoku2.LINES, anz, True)
        if step != None:
            return step
        step = findHiddenXleInEntity(Sudoku2.UNITS, Sudoku2.COLS, anz, True)
        return step

    def findHiddenXleInEntity(self, constraintBase, indices, anz, onlyOne):
        """ generated source for method findHiddenXleInEntity """
        step = None
        entity = 0
        while len(indices):
            maxIndex = 0
            i = 0
            while len(length):
                if sudoku.getCell(indices[entity][i]) != 0:
                    maxIndex += 1
                i += 1
            if maxIndex <= anz:
                entity += 1
                continue 
            candMask = 0
            free = sudoku.getFree()
            i = 1
            while i <= 9:
                actFree = free[constraintBase + entity][i]
                if actFree != 0 and actFree <= anz:
                    candMask |= Sudoku2.MASKS[i]
                    self.ipcMask[i] = 0
                    j = 0
                    while j < Sudoku2.UNITS:
                        if (sudoku.getCell(indices[entity][j]) & Sudoku2.MASKS[i]) != 0:
                            self.ipcMask[i] |= Sudoku2.MASKS[j + 1]
                        j += 1
                i += 1
            if Sudoku2.ANZ_VALUES[candMask] < anz:
                entity += 1
                continue 
            candArr = Sudoku2.POSSIBLE_VALUES[candMask]
            i1 = 0
            while i1 < 1 + len(candArr):
                cand1 = Sudoku2.MASKS[candArr[i1]]
                cell1 = self.ipcMask[candArr[i1]]
                i2 = i1 + 1
                while i2 < 2 + len(candArr):
                    cand2 = int((cand1 | Sudoku2.MASKS[candArr[i2]]))
                    cell2 = int((cell1 | self.ipcMask[candArr[i2]]))
                    if anz == 2:
                        if Sudoku2.ANZ_VALUES[cell2] == anz:
                            tmp = Sudoku2.POSSIBLE_VALUES[cell2]
                            step = createSubsetStep(indices[entity][tmp[0] - 1], indices[entity][tmp[1] - 1], -1, -1, cand2, SolutionType.HIDDEN_PAIR, onlyOne, onlyOne)
                            if step != None and onlyOne:
                                return step
                    else:
                        i3 = i2 + 1
                        while i3 < 3 + len(candArr):
                            cand3 = int((cand2 | Sudoku2.MASKS[candArr[i3]]))
                            cell3 = int((cell2 | self.ipcMask[candArr[i3]]))
                            if anz == 3:
                                if Sudoku2.ANZ_VALUES[cell3] == anz:
                                    tmp = Sudoku2.POSSIBLE_VALUES[cell3]
                                    step = createSubsetStep(indices[entity][tmp[0] - 1], indices[entity][tmp[1] - 1], indices[entity][tmp[2] - 1], -1, cand3, SolutionType.HIDDEN_TRIPLE, onlyOne, onlyOne)
                                    if step != None and onlyOne:
                                        return step
                            else:
                                i4 = i3 + 1
                                while len(candArr):
                                    cand4 = int((cand3 | Sudoku2.MASKS[candArr[i4]]))
                                    cell4 = int((cell3 | self.ipcMask[candArr[i4]]))
                                    if Sudoku2.ANZ_VALUES[cell4] == anz:
                                        tmp = Sudoku2.POSSIBLE_VALUES[cell4]
                                        step = createSubsetStep(indices[entity][tmp[0] - 1], indices[entity][tmp[1] - 1], indices[entity][tmp[2] - 1], indices[entity][tmp[3] - 1], cand4, SolutionType.HIDDEN_QUADRUPLE, onlyOne, onlyOne)
                                        if step != None and onlyOne:
                                            return step
                                    i4 += 1
                            i3 += 1
                    i2 += 1
                i1 += 1
            entity += 1
        return None

    def findLockedCandidates(self, type_):
        """ generated source for method findLockedCandidates """
        SudokuUtil.clearStepList(self.steps)
        step = None
        if type_ == SolutionType.LOCKED_CANDIDATES or type_ == SolutionType.LOCKED_CANDIDATES_1:
            step = findLockedCandidatesInEntityN(18, Sudoku2.BLOCKS, True)
            if step != None:
                return step
        if type_ == SolutionType.LOCKED_CANDIDATES or type_ == SolutionType.LOCKED_CANDIDATES_2:
            step = findLockedCandidatesInEntityN(0, Sudoku2.LINES, True)
            if step != None:
                return step
            step = findLockedCandidatesInEntityN(9, Sudoku2.COLS, True)
            if step != None:
                return step
        return None

    def findAllLockedCandidates(self):
        """ generated source for method findAllLockedCandidates """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findLockedCandidatesInEntityN(18, Sudoku2.BLOCKS, False)
        findLockedCandidatesInEntityN(0, Sudoku2.LINES, False)
        findLockedCandidatesInEntityN(9, Sudoku2.COLS, False)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findLockedCandidatesInEntityN(self, constraintBase, indices, onlyOne):
        """ generated source for method findLockedCandidatesInEntityN """
        step = None
        free = sudoku.getFree()
        constr = 0
        while constr < Sudoku2.UNITS:
            cand = 1
            while cand <= 9:
                unitFree = free[constr + constraintBase][cand]
                if unitFree == 2 or unitFree == 3:
                    first = True
                    self.sameConstraint[0] = self.sameConstraint[1] = self.sameConstraint[2] = True
                    i = 0
                    while len(length):
                        index = indices[constr][i]
                        cell = sudoku.getCell(index)
                        if (cell & Sudoku2.MASKS[cand]) == 0:
                            i += 1
                            continue 
                        if first:
                            self.constraint[0] = Sudoku2.CONSTRAINTS[index][0]
                            self.constraint[1] = Sudoku2.CONSTRAINTS[index][1]
                            self.constraint[2] = Sudoku2.CONSTRAINTS[index][2]
                            first = False
                        else:
                            j = 0
                            while len(length):
                                if self.sameConstraint[j] and self.constraint[j] != Sudoku2.CONSTRAINTS[index][j]:
                                    self.sameConstraint[j] = False
                                j += 1
                        i += 1
                    skipConstraint = constraintBase + constr
                    aktConstraint = -1
                    if constraintBase == 18:
                        if self.sameConstraint[0] and free[self.constraint[0]][cand] > unitFree:
                            aktConstraint = self.constraint[0]
                        elif self.sameConstraint[1] and free[self.constraint[1]][cand] > unitFree:
                            aktConstraint = self.constraint[1]
                        else:
                            cand += 1
                            continue 
                        step = createLockedCandidatesStep(SolutionType.LOCKED_CANDIDATES_1, cand, skipConstraint, Sudoku2.ALL_UNITS[aktConstraint])
                        if onlyOne:
                            return step
                        else:
                            self.steps.add(step)
                    else:
                        if self.sameConstraint[2] and free[self.constraint[2]][cand] > unitFree:
                            step = createLockedCandidatesStep(SolutionType.LOCKED_CANDIDATES_2, cand, skipConstraint, Sudoku2.ALL_UNITS[self.constraint[2]])
                            if onlyOne:
                                return step
                            else:
                                self.steps.add(step)
                cand += 1
            constr += 1
        return None

    def createLockedCandidatesStep(self, type_, cand, skipConstraint, indices):
        """ generated source for method createLockedCandidatesStep """
        self.globalStep.reset()
        self.globalStep.setType(type_)
        self.globalStep.addValue(cand)
        self.globalStep.setEntity(Sudoku2.CONSTRAINT_TYPE_FROM_CONSTRAINT[skipConstraint])
        self.globalStep.setEntityNumber(Sudoku2.CONSTRAINT_NUMBER_FROM_CONSTRAINT[skipConstraint])
        i = 0
        while len(indices):
            index = indices[i]
            if (sudoku.getCell(index) & Sudoku2.MASKS[cand]) != 0:
                if Sudoku2.CONSTRAINTS[index][0] == skipConstraint or Sudoku2.CONSTRAINTS[index][1] == skipConstraint or Sudoku2.CONSTRAINTS[index][2] == skipConstraint:
                    self.globalStep.addIndex(index)
                else:
                    self.globalStep.addCandidateToDelete(index, cand)
            i += 1
        return self.globalStep.clone()

    @overloaded
    def createSubsetStep(self, i1, i2, i3, i4, cands, type_, lockedOnly, nakedOnly):
        """ generated source for method createSubsetStep """
        if i4 >= 0:
            self.indices4[0] = i1
            self.indices4[1] = i2
            self.indices4[2] = i3
            self.indices4[3] = i4
            return self.createSubsetStep(self.indices4, cands, type_, lockedOnly, nakedOnly)
        elif i3 >= 0:
            self.indices3[0] = i1
            self.indices3[1] = i2
            self.indices3[2] = i3
            return self.createSubsetStep(self.indices3, cands, type_, lockedOnly, nakedOnly)
        else:
            self.indices2[0] = i1
            self.indices2[1] = i2
            return self.createSubsetStep(self.indices2, cands, type_, lockedOnly, nakedOnly)

    @createSubsetStep.register(object, int, int, SolutionType, bool, bool)
    def createSubsetStep_0(self, indices, cands, type_, lockedOnly, nakedHiddenOnly):
        """ generated source for method createSubsetStep_0 """
        self.globalStep.reset()
        self.globalStep.setType(type_)
        self.sameConstraint[0] = self.sameConstraint[1] = self.sameConstraint[2] = True
        self.constraint[0] = Sudoku2.CONSTRAINTS[indices[0]][0]
        self.constraint[1] = Sudoku2.CONSTRAINTS[indices[0]][1]
        self.constraint[2] = Sudoku2.CONSTRAINTS[indices[0]][2]
        i = 1
        while len(indices):
            j = 0
            while len(length):
                if self.sameConstraint[j] and self.constraint[j] != Sudoku2.CONSTRAINTS[indices[i]][j]:
                    self.sameConstraint[j] = False
                j += 1
            i += 1
        anzFoundConstraints = 0
        if type_.isHiddenSubset():
            i = 0
            while len(indices):
                candsToDelete = int((sudoku.getCell(indices[i]) & ~cands))
                if candsToDelete == 0:
                    i += 1
                    continue 
                candArray = Sudoku2.POSSIBLE_VALUES[candsToDelete]
                k = 0
                while len(candArray):
                    self.globalStep.addCandidateToDelete(indices[i], candArray[k])
                    k += 1
                i += 1
        else:
            self.foundConstraint[0] = self.foundConstraint[1] = self.foundConstraint[2] = False
            i = 0
            while len(sameConstraint):
                if not self.sameConstraint[i]:
                    i += 1
                    continue 
                cells = Sudoku2.ALL_UNITS[self.constraint[i]]
                j = 0
                while len(cells):
                    skip = False
                    k = 0
                    while len(indices):
                        if cells[j] == indices[k]:
                            skip = True
                            break
                        k += 1
                    if skip:
                        j += 1
                        continue 
                    candsToDelete = int((sudoku.getCell(cells[j]) & cands))
                    if candsToDelete == 0:
                        j += 1
                        continue 
                    candArray = Sudoku2.POSSIBLE_VALUES[candsToDelete]
                    k = 0
                    while len(candArray):
                        self.globalStep.addCandidateToDelete(cells[j], candArray[k])
                        if not self.foundConstraint[i] and ((i == 2) or (Sudoku2.CONSTRAINTS[cells[j]][2] != self.constraint[2])):
                            self.foundConstraint[i] = True
                            anzFoundConstraints += 1
                        k += 1
                    j += 1
                i += 1
        if self.globalStep.getAnzCandidatesToDelete() == 0:
            return None
        isLocked = False
        if anzFoundConstraints > 1 and len(indices) and not type_.isHiddenSubset() and (self.sameConstraint[2] and self.sameConstraint[0] or self.sameConstraint[2] and self.sameConstraint[1]):
            isLocked = True
        if isLocked:
            if type_ == SolutionType.NAKED_PAIR:
                self.globalStep.setType(SolutionType.LOCKED_PAIR)
            if type_ == SolutionType.NAKED_TRIPLE:
                self.globalStep.setType(SolutionType.LOCKED_TRIPLE)
        i = 0
        while len(indices):
            self.globalStep.addIndex(indices[i])
            i += 1
        candArray = Sudoku2.POSSIBLE_VALUES[cands]
        i = 0
        while len(candArray):
            self.globalStep.addValue(candArray[i])
            i += 1
        step = self.globalStep.clone()
        if lockedOnly and not nakedHiddenOnly:
            if not isLocked:
                self.cachedSteps.add(step)
                step = None
        elif nakedHiddenOnly and not lockedOnly:
            if isLocked:
                self.cachedSteps.add(step)
                step = None
        elif not lockedOnly and not nakedHiddenOnly:
            self.steps.add(step)
        return step

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":0110:38:.1.57.4..7+521+4.6..........5.+2...1........+7.2..7562+839.2.+7......569214....4.7.....::319 329 338 378 388 398 819 829 837 838 848 878 888 898::")
        solver = SudokuSolverFactory.getDefaultSolverInstance()
        step = solver.getHint(sudoku, False)
        print(step)
        System.exit(0)


if __name__ == '__main__':
    import sys
    SimpleSolver.main(sys.argv)

