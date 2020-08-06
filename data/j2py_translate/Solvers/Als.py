#!/usr/bin/env python
""" generated source for module Als """
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
class Als(object):
    """ generated source for class Als """
    #  All indices that belong to the ALS 
    indices = None

    #  All numbers that are contained in the ALS (only the numbers, not the actual candidates!) 
    candidates = int()

    #  For every number contained in the ALS all cells containing that number as candidate 
    indicesPerCandidat = [None] * 10

    #  For every number contained in the ALS all cells outside the als that are buddies to all ALS cells holding that candidate 
    buddiesPerCandidat = [None] * 10

    #  Like {@link #buddiesPerCandidat} but including the ALS cells holding that candidate (for RC search). 
    buddiesAlsPerCandidat = [None] * 10

    #  All cells outside the als, that contain at least one candidate, that is a buddy to the ALS 
    buddies = None

    #  The penalty for the ALS (used when calculating chain length) 
    chainPenalty = -1

    # 
    #      * Creates a new ALS.<br><br>
    #      * <b>Note:</b> An ALS created with this constructor cannot be
    #      * used unless {@link #computeFields(solver.SudokuStepFinder) }
    #      * has been called.
    #      * @param indices
    #      * @param candidates
    #      
    def __init__(self, indices, candidates):
        """ generated source for method __init__ """
        self.indices = SudokuSet(indices)
        self.candidates = candidates

    # 
    #      * Computes all the additional fields; is done after the initial search
    #      * to optimize finding doubles.
    #      * 
    #      * @param finder
    #      
    def computeFields(self, finder):
        """ generated source for method computeFields """
        self.buddies = SudokuSet()
        i = 1
        while i <= 9:
            if (self.candidates & Sudoku2.MASKS[i]) != 0:
                sudokuCandidates = finder.getCandidates()[i]
                self.indicesPerCandidat[i] = SudokuSet(self.indices)
                self.indicesPerCandidat[i].and_(sudokuCandidates)
                self.buddiesPerCandidat[i] = SudokuSet()
                Sudoku2.getBuddies(self.indicesPerCandidat[i], self.buddiesPerCandidat[i])
                self.buddiesPerCandidat[i].andNot(self.indices)
                self.buddiesPerCandidat[i].and_(finder.getCandidates()[i])
                self.buddiesAlsPerCandidat[i] = SudokuSet(self.buddiesPerCandidat[i])
                self.buddiesAlsPerCandidat[i].or_(self.indicesPerCandidat[i])
                self.buddies.or_(self.buddiesPerCandidat[i])
            i += 1

    @classmethod
    @overloaded
    def getChainPenalty(cls, candSize):
        """ generated source for method getChainPenalty """
        if candSize == 0 or candSize == 1:
            return 0
        elif candSize == 2:
            return candSize - 1
        else:
            return (candSize - 1) * 2

    @getChainPenalty.register(object)
    def getChainPenalty_0(self):
        """ generated source for method getChainPenalty_0 """
        if self.chainPenalty == -1:
            self.chainPenalty = self.getChainPenalty(Sudoku2.ANZ_VALUES[self.candidates])
        return self.chainPenalty

    def equals(self, o):
        """ generated source for method equals """
        if o == None:
            return False
        if not (isinstance(o, (Als, ))):
            return False
        a = o
        return self.indices == a.indices

    def hashCode(self):
        """ generated source for method hashCode """
        hash = 7
        hash = 71 * hash + (self.indices.hashCode() if self.indices != None else 0)
        return hash

    def __str__(self):
        """ generated source for method toString """
        return "ALS: " + SolutionStep.getAls(self)

