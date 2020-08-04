#!/usr/bin/env python
""" generated source for module ColoringSolver """
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
class ColoringSolver(AbstractSolver):
    """ generated source for class ColoringSolver """
    #  First color of a coloring pair. Index in {@link #sets} 
    C1 = 0

    #  Second color of a coloring pair. Index in {@link #sets} 
    C2 = 1

    #  Maximum number of color pairs. 
    MAX_COLOR = 20

    #  Sets containing the indices of colored cells for all candidates. sets[x]
    #      * contains the color pairs for candidate x, sets[x][y] contains one color pair for candidate x. 
    sets = [None] * 10

    #  Number of color pairs for each candidate. 
    anzColorPairs = [None] * 

    #  Step number of the sudoku for which coloring was calculated. -1 means "data invalid". 
    stepNumbers = [None] * 

    #  contains all candidates, that are part of at least one conjugate pair. 
    startSet = SudokuSet()

    #  Set for temporary calculations. 
    tmpSet1 = SudokuSet()

    #  Contains cells where a candidate can be eliminated. 
    deleteSet = SudokuSet()

    #  All steps found. 
    steps = ArrayList()

    #  One global step for optimization. 
    globalStep = SolutionStep()

    def __init__(self, finder):
        """ generated source for method __init__ """
        super(ColoringSolver, self).__init__(finder)
        #  create coloring sets
        i = 0
        while len(sets):
            j = 0
            while len(length):
                k = 0
                while len(length):
                    self.sets[i][j][k] = SudokuSet()
                    k += 1
                j += 1
            self.anzColorPairs[i] = 0
            self.stepNumbers[i] = -1
            i += 1

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == SIMPLE_COLORS:
            pass
        elif type_ == SIMPLE_COLORS_TRAP:
            pass
        elif type_ == SIMPLE_COLORS_WRAP:
            result = findSimpleColorStep(True)
        elif type_ == MULTI_COLORS:
            pass
        elif type_ == MULTI_COLORS_1:
            pass
        elif type_ == MULTI_COLORS_2:
            result = findMultiColorStep(True)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == SIMPLE_COLORS:
            pass
        elif step.getType() == SIMPLE_COLORS_TRAP:
            pass
        elif step.getType() == SIMPLE_COLORS_WRAP:
            pass
        elif step.getType() == MULTI_COLORS:
            pass
        elif step.getType() == MULTI_COLORS_1:
            pass
        elif step.getType() == MULTI_COLORS_2:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    def findAllSimpleColors(self):
        """ generated source for method findAllSimpleColors """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findSimpleColorSteps(False)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findAllMultiColors(self):
        """ generated source for method findAllMultiColors """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findMultiColorSteps(False)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findSimpleColorStep(self, onlyOne):
        """ generated source for method findSimpleColorStep """
        self.steps.clear()
        step = findSimpleColorSteps(onlyOne)
        if onlyOne and step != None:
            return step
        elif len(self.steps) > 0:
            Collections.sort(self.steps)
            return self.steps.get(0)
        return None

    def findSimpleColorSteps(self, onlyOne):
        """ generated source for method findSimpleColorSteps """
        i = 1
        while i <= 9:
            step = findSimpleColorStepsForCandidate(i, onlyOne)
            if onlyOne and step != None:
                return step
            i += 1
        return None

    def findSimpleColorStepsForCandidate(self, cand, onlyOne):
        """ generated source for method findSimpleColorStepsForCandidate """
        anzColors = doColoring(cand)
        i = 0
        while i < anzColors:
            set1 = self.sets[cand][i][self.C1]
            set2 = self.sets[cand][i][self.C2]
            self.globalStep.reset()
            if checkColorWrap(set1):
                j = 0
                while j < len(set1):
                    self.globalStep.addCandidateToDelete(set1.get(j), cand)
                    j += 1
            if checkColorWrap(set2):
                j = 0
                while j < len(set2):
                    self.globalStep.addCandidateToDelete(set2.get(j), cand)
                    j += 1
            if not self.globalStep.getCandidatesToDelete().isEmpty():
                self.globalStep.setType(SolutionType.SIMPLE_COLORS_WRAP)
                self.globalStep.addValue(cand)
                self.globalStep.addColorCandidates(set1, 0)
                self.globalStep.addColorCandidates(set2, 1)
                step = self.globalStep.clone()
                if onlyOne:
                    return step
                else:
                    self.steps.add(step)
            self.globalStep.reset()
            checkCandidateToDelete(set1, set2, cand)
            if not self.globalStep.getCandidatesToDelete().isEmpty():
                self.globalStep.setType(SolutionType.SIMPLE_COLORS_TRAP)
                self.globalStep.addValue(cand)
                self.globalStep.addColorCandidates(set1, 0)
                self.globalStep.addColorCandidates(set2, 1)
                step = self.globalStep.clone()
                if onlyOne:
                    return step
                else:
                    self.steps.add(step)
            i += 1
        return None

    def checkColorWrap(self, set):
        """ generated source for method checkColorWrap """
        i = 0
        while i < len(set) - 1:
            j = i + 1
            while j < len(set):
                if Sudoku2.buddies[set.get(i)].contains(set.get(j)):
                    return True
                j += 1
            i += 1
        return False

    def checkCandidateToDelete(self, set1, set2, cand):
        """ generated source for method checkCandidateToDelete """
        self.deleteSet.clear()
        i = 0
        while i < len(set1):
            j = 0
            while j < len(set2):
                self.tmpSet1.set(Sudoku2.buddies[set1.get(i)])
                self.tmpSet1.and_(Sudoku2.buddies[set2.get(j)])
                self.tmpSet1.and_(finder.getCandidates()[cand])
                self.deleteSet.or_(self.tmpSet1)
                j += 1
            i += 1
        if not self.deleteSet.isEmpty():
            i = 0
            while i < len(self.deleteSet):
                self.globalStep.addCandidateToDelete(self.deleteSet.get(i), cand)
                i += 1

    def findMultiColorStep(self, onlyOne):
        """ generated source for method findMultiColorStep """
        self.steps.clear()
        step = findMultiColorSteps(onlyOne)
        if onlyOne and step != None:
            return step
        elif len(self.steps) > 0:
            Collections.sort(self.steps)
            return self.steps.get(0)
        return None

    def findMultiColorSteps(self, onlyOne):
        """ generated source for method findMultiColorSteps """
        i = 1
        while i <= 9:
            step = findMultiColorStepsForCandidate(i, onlyOne)
            if onlyOne and step != None:
                return step
            i += 1
        return None

    def findMultiColorStepsForCandidate(self, cand, onlyOne):
        """ generated source for method findMultiColorStepsForCandidate """
        anzColors = doColoring(cand)
        i = 0
        while i < anzColors:
            j = 0
            while j < anzColors:
                if i == j:
                    j += 1
                    continue 
                set11 = self.sets[cand][i][self.C1]
                set12 = self.sets[cand][i][self.C2]
                set21 = self.sets[cand][j][self.C1]
                set22 = self.sets[cand][j][self.C2]
                self.globalStep.reset()
                if checkMultiColor1(set11, set21, set22):
                    k = 0
                    while k < len(set11):
                        self.globalStep.addCandidateToDelete(set11.get(k), cand)
                        k += 1
                if checkMultiColor1(set12, set21, set22):
                    k = 0
                    while k < len(set12):
                        self.globalStep.addCandidateToDelete(set12.get(k), cand)
                        k += 1
                if not self.globalStep.getCandidatesToDelete().isEmpty():
                    self.globalStep.setType(SolutionType.MULTI_COLORS_2)
                    self.globalStep.addValue(cand)
                    self.globalStep.addColorCandidates(set11, 0)
                    self.globalStep.addColorCandidates(set12, 1)
                    self.globalStep.addColorCandidates(set21, 2)
                    self.globalStep.addColorCandidates(set22, 3)
                    step = self.globalStep.clone()
                    if onlyOne:
                        return step
                    else:
                        self.steps.add(step)
                self.globalStep.reset()
                if checkMultiColor2(set11, set21):
                    self.checkCandidateToDelete(set12, set22, cand)
                if checkMultiColor2(set11, set22):
                    self.checkCandidateToDelete(set12, set21, cand)
                if checkMultiColor2(set12, set21):
                    self.checkCandidateToDelete(set11, set22, cand)
                if checkMultiColor2(set12, set22):
                    self.checkCandidateToDelete(set11, set21, cand)
                if not self.globalStep.getCandidatesToDelete().isEmpty():
                    self.globalStep.setType(SolutionType.MULTI_COLORS_1)
                    self.globalStep.addValue(cand)
                    self.globalStep.addColorCandidates(set11, 0)
                    self.globalStep.addColorCandidates(set12, 1)
                    self.globalStep.addColorCandidates(set21, 2)
                    self.globalStep.addColorCandidates(set22, 3)
                    step = self.globalStep.clone()
                    if onlyOne:
                        return step
                    else:
                        self.steps.add(step)
                j += 1
            i += 1
        return None

    def checkMultiColor1(self, set, s21, s22):
        """ generated source for method checkMultiColor1 """
        seeS21 = False
        seeS22 = False
        i = 0
        while i < len(set):
            self.tmpSet1.set(Sudoku2.buddies[set.get(i)])
            if not self.tmpSet1.andEmpty(s21):
                seeS21 = True
            if not self.tmpSet1.andEmpty(s22):
                seeS22 = True
            if seeS21 and seeS22:
                return True
            i += 1
        return False

    def checkMultiColor2(self, set1, set2):
        """ generated source for method checkMultiColor2 """
        i = 0
        while i < len(set1):
            j = 0
            while j < len(set2):
                if Sudoku2.buddies[set1.get(i)].contains(set2.get(j)):
                    return True
                j += 1
            i += 1
        return False

    def doColoring(self, cand):
        """ generated source for method doColoring """
        if self.stepNumbers[cand] == finder.getStepNumber():
            return self.anzColorPairs[cand]
        self.anzColorPairs[cand] = 0
        self.stepNumbers[cand] = finder.getStepNumber()
        self.startSet.set(finder.getCandidates()[cand])
        values = self.startSet.getValues()
        size = len(self.startSet)
        free = sudoku.getFree()
        i = 0
        while i < size:
            index = values[i]
            if free[Sudoku2.CONSTRAINTS[index][0]][cand] != 2 and free[Sudoku2.CONSTRAINTS[index][1]][cand] != 2 and free[Sudoku2.CONSTRAINTS[index][2]][cand] != 2:
                self.startSet.remove(values[i])
                i += 1
                continue 
            i += 1
        while not self.startSet.isEmpty():
            actSets = self.sets[cand][self.anzColorPairs[cand]]
            actSets[self.C1].clear()
            actSets[self.C2].clear()
            index = self.startSet.get(0)
            doColoringForColorRecursive(index, cand, True)
            if actSets[self.C1].isEmpty() or actSets[self.C2].isEmpty():
                actSets[self.C1].clear()
                actSets[self.C2].clear()
            else:
                self.anzColorPairs[cand] += 1
        return self.anzColorPairs[cand]

    def doColoringForColorRecursive(self, index, cand, on):
        """ generated source for method doColoringForColorRecursive """
        if index == -1 or not self.startSet.contains(index):
            return
        if on:
            self.sets[cand][self.anzColorPairs[cand]][self.C1].add(index)
        else:
            self.sets[cand][self.anzColorPairs[cand]][self.C2].add(index)
        self.startSet.remove(index)
        self.doColoringForColorRecursive(getConjugateIndex(index, cand, Sudoku2.CONSTRAINTS[index][0]), cand, not on)
        self.doColoringForColorRecursive(getConjugateIndex(index, cand, Sudoku2.CONSTRAINTS[index][1]), cand, not on)
        self.doColoringForColorRecursive(getConjugateIndex(index, cand, Sudoku2.CONSTRAINTS[index][2]), cand, not on)

    def getConjugateIndex(self, index, cand, constraint):
        """ generated source for method getConjugateIndex """
        if sudoku.getFree()[constraint][cand] != 2:
            return -1
        self.tmpSet1.set(finder.getCandidates()[cand])
        self.tmpSet1.and_(Sudoku2.ALL_CONSTRAINTS_TEMPLATES[constraint])
        result = self.tmpSet1.get(0)
        if result == index:
            result = self.tmpSet1.get(1)
        return result

