#!/usr/bin/env python
""" generated source for module SingleDigitPatternSolver """
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
# 
#  Dual Skyscraper?
#  |-----------+-----------+-----------|
#  |  .  .  .  |  .  .  .  |  3  .  3  |
#  |  .  .  3  |  .  .  .  |  .  .  .  |
#  |  .  .  .  |  .  3  .  |  .  .  .  |
#  |-----------+-----------+-----------|
#  |  .  .  .  |  .  .  .  |  .  3  .  |
#  |  .  3@ .  |  3@ .  .  |  .  .  .  |
#  |  3  .  .  |  .  .  3# |  .  .  .  |
#  |-----------+-----------+-----------|
#  |  3  .  .  |  3# .  .  |  .  .  3  |
#  |  3  .  .  |  .  .  .  |  3  .  3  |
#  |  3  3@ .  |  .  .  3# |  3  .  .  |
#  +-----------------------------------+ 
#  
# package: solver
# 
#  * Empty Rectangles:
#  * 
#  * Every box can hold nine different empty rectangles ('X' means 'candidate not 
#  * present', digits below are lines/cols):
#  * 
#  * + - - - +   + - - - +   + - - - +
#  * | X X . |   | X . X |   | . X X |
#  * | X X . |   | X . X |   | . X X |
#  * | . . . |   | . . . |   | . . . |
#  * + - - - +   + - - - +   + - - - +
#  *    2 2         2 1         2 0
#  * + - - - +   + - - - +   + - - - +
#  * | X X . |   | X . X |   | . X X |
#  * | . . . |   | . . . |   | . . . |
#  * | X X . |   | X . X |   | . X X |
#  * + - - - +   + - - - +   + - - - +
#  *    1 2         1 1         1 0
#  * + - - - +   + - - - +   + - - - +
#  * | . . . |   | . . . |   | . . . |
#  * | X X . |   | X . X |   | . X X |
#  * | X X . |   | X . X |   | . X X |
#  * + - - - +   + - - - +   + - - - +
#  *    0 2         0 1         0 0
#  * 
#  * The '.' cells must contain at least three candidates, at least one exclusively
#  * within the row/col (with two candidates the basic ER move degenerates into an 
#  * X-Chain, with all three candidates only in a row/col it doesn't work at all).
#  * 
#  * For easy comparison SudokuSets with all possible combinations of empty cells
#  * for all blocks are created at startup.
#  *
#  * @author hobiwan
#  
class SingleDigitPatternSolver(AbstractSolver):
    """ generated source for class SingleDigitPatternSolver """
    #  empty rectangles: all possible empty cells relative to cell 0 
    erOffsets = [None] * 

    #  empty rectangles: all possible ER lines relative to line 0, synchronized with {@link #erOffsets} 
    erLineOffsets = [None] * 

    #  empty rectangles: all possible ER cols relative to col 0, synchronized with {@link #erOffsets} 
    erColOffsets = [None] * 

    #  Bitmaps for all possible ERs for all blocks (all cells set except those that
    #      * have to be empty; if anded with the availble candidates in a block the result has to
    #      * be empty too) 
    erSets = [None] * 9

    #  All possible ER lines for all blocks, synchronized with {@link #erSets} 
    erLines = [None] * 9

    #  All possible ER cols for all blocks, synchronized with {@link #erSets} 
    erCols = [None] * 9

    #  All candidates in a block (for ER search) 
    blockCands = SudokuSet()

    #  A set for various checks 
    tmpSet = SudokuSet()

    #  A list with all steps found 
    steps = ArrayList()

    #  One global instance for optimization 
    globalStep = SolutionStep()

    #  For all entries in {@link #only2Constraints} the indices of the two cells 
    only2Indices = [None] * 2 * Sudoku2.UNITS

    #  A set to check for eliminations 
    firstUnit = SudokuSet()

    #  Creates a new instance of SimpleSolver
    #      * @param finder 
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(SingleDigitPatternSolver, self).__init__(finder)

    #  initialize erSets, erLines, erCols
    indexOffset = 0
    lineOffset = 0
    colOffset = 0
    i = 0
    j = 0

    #  on to the next block
    # 
    #      * Finds all Empty Rectangles
    #      * @return
    #      
    # 
    #      * Find a single ER. If {@link Options#allowDualsAndSiamese} is set, Dual ERs
    #      * are found as well.
    #      * @return
    #      
    # 
    #      * Finds all empty rectangles that provide eliminations (only simple case
    #      * with one conjugate pair). The search is actually delegated to
    #      * {@link #findEmptyRectanglesForCandidate(int)}.
    #      * @param onlyOne
    #      * @return
    #      
    # 
    #      * Try all blocks: for every block check whether all the cells in erSets[block][i]
    #      * don't have the candidate in question. If this is true neither the ER line nor
    #      * the ER col may be empty (without crossing point!) and at least one of them
    #      * has to hold at least two candidates.
    #      * 
    #      * For any ER try to find a conjugate pair with one candidate in the row/col
    #      * of the ER, and one single candidate in ther intersection of the second
    #      * ca didate of the conjugate pair and the col/row of the ER.
    #      * 
    #      * @param cand candidate for which the grid is searched
    #      * @param onlyOne
    #      * @return
    #      
    #  scan all blocks
    #  if the block holds less than two or more than five candidates,
    #  it cant be a ER
    #  impossible
    #  get all occurrencies for cand in block i
    #  check all possible ERs for that block
    #  are the correct cells empty?
    #  definitely not this type of ER
    #  now check the candidates in the lines
    #  not valid!
    #  and the candidates in the cols
    #  not valid!
    #  both row and col have only one candidate -> invalid
    #  empty rectangle found: erLine and erCol hold the lineNumbers
    #  try all cells in indices erLine; if a cell that is not part of the ER holds
    #  a candidate, check whether it forms a conjugate pair in the respective col
    # 
    #      * Checks possible eliminations for a given ER. The names of the parameters
    #      * are chosen for a conjugate pair search in the columns, but it works for
    #      * the lines too, if all indices/col parameters are exchanged in the
    #      * method call.
    #      * 
    #      * The method tries to find a conjugate pair in a column where one of the
    #      * candidates is in indices firstLine. If so all candidates in the indices of the
    #      * second cell of the conjugate pair are checked. If one of them lies in
    #      * column firstCol, it can be eliminated.
    #      * 
    #      * @param cand The candidate for which the check is made
    #      * @param block The index of the block holding the ER
    #      * @param blockCands All Candidates that comprise the ER
    #      * @param indices Indices of all cells in firstLine/firstCol
    #      * @param LINE_TEMPLATES Sudoku2.LINE_TEMPLATES/Sudoku2.COL_TEMPLATES
    #      * @param COL_TEMPLATES Sudoku2.COL_TEMPLATES/Sudoku2.LINE_TEMPLATES
    #      * @param firstCol Index of the col/indices of the ER
    #      * @param lineColReversed If <code>true</code>, all lines/columns are interchanged
    #      * @param onlyOne
    #      * @return
    #      
    #  cell already set
    #  cell part of the ER
    #  possible conjugate pair -> check
    #  conjugate pair found
    #  now check, whether a candidate in the row of index2
    #  sees the col of the ER
    #  cannot eliminate an ER candidate
    #  elimination found!
    #  only one elimination per conjugate pair possible
    # 
    #      * A dual Empty Rectangle consists of two ERs, that have the same candidates
    #      * in the ER box but lead to different eliminations.
    #      * 
    #      * Try all combinations of steps:
    #      *   - entity and entityNumber have to be the same
    #      *   - box candidiates have to be the same (fins!)
    #      *   - elimination has to be different
    #      * Create new step with indices/eliminations from both, fins from first, add to ers
    #      * 
    #      * @param kites All available 2-String-Kites
    #      
    #  do nothing
    #  read current size (list can be changed by DUALS)
    #  different boxes -> cant be a dual
    #  different number of candidates in box -> cant be a dual
    #                         print("  " + step1.getFins().get(k) + " - " + step2.getFins().get(k));
    #  not the same ER -> cant be a dual
    #  possible dual ER; different eliminations?
    #  same step twice -> no dual
    #  ok: dual!
    # 
    #      * Search for all Skyscrapers
    #      * @return
    #      
    # 
    #      * Search the grid for Skyscrapers
    #      * @return
    #      
    # 
    #      * Search for Skyscrapers in the lines or in the columns. Two calls are
    #      * necessary to get all possible steps.<br>
    #      * The search:
    #      * <ul>
    #      * <li>Iterate over all candidates</li>
    #      * <li>For each candidate look at all lines (cols) and check which have only two candidates left</li>
    #      * <li></li>
    #      * <li></li>
    #      * </ul>
    #      * @param lines
    #      * @param onlyOne
    #      * @return
    #      
    #  indices in free
    #  adjust for columns
    #  try every candidate
    #  get all constraints with only two candidates and the indices of the cells
    #  constraint has only two candidates left -> get the indices of the cells
    #  ok: now try all combinations of those constraints
    #  one end has to be in the same line/col
    #  must be in the same col
    #  must be in the same line
    #  invalid combination
    #  the "free ends" must not be in the same unit or it would be an X-Wing
    #  step is X-Wing -> ignore
    #  can something be eliminated?
    #  Skyscraper found!
    #                         if (onlyOne && ! Options.getInstance().isAllowDualsAndSiamese()) {
    # 
    #      * FIns all 2-String-Kites in the grid
    #      * @return
    #      
    # 
    #      * Find the next 2-String-Kite
    #      * @return
    #      
    # 
    #      * Search for 2-String-Kites: We need a strong link in a line and one in a col.
    #      * The two strong links must be connected by a box and the "free ends" must see
    #      * a candidate.
    #      * @param onlyOne
    #      * @return
    #      
    #  search for lines and columns with exactly two candidates
    #  try every candidate
    #  get all constraints with only two candidates and the indices of the cells
    #  all lines are in only2Indices[0 .. constr1Count - 1], all cols
    #  are in only2Indices[constr1Count .. constr2Count - 1]
    #  constraint has only two candidates left -> get the indices of the cells
    #  ok: now try all combinations of those constraints
    #  one end has to be in the same line/col, but: all 4 combinations are possible
    #  the indices in the same block end up in only2Indices[][0], the "free ends"
    #  in only2indices[][1]
    #  everything is as it should be -> do nothing
    #  nothing found -> continue with next column
    #  the indices within the connecting box could be the same -> not a 2-String-Kite
    #  invalid!
    #  ok: two strong links, connected in a box; can anything be deleted?
    #  valid 2-String-Kite!
    #  the candidates in the connecting block are added as fins (will be painted
    #  in a different color)
    # 
    #      * A dual 2-String-Kite consists of two kites, that have the same candidates
    #      * in the connecting box but lead to different eliminations.
    #      * 
    #      * Try all combinations of steps:
    #      *   - box candidates have to be the same (fins!)
    #      *   - elimination has to be different
    #      * Create new step with indices/eliminations from both, fins from first, add to kites
    #      * 
    #      * @param kites All available 2-String-Kites
    #      
    #  do nothing
    #  read current size (list can be changed by DUALS)
    #  possible dual kite; different eliminations?
    #  same step twice -> no dual
    #  ok: dual!
    #  2-String Kite: 3 in r2c1,r8c5 (verbunden durch r2c6,r3c5) => r8c1<>3
    #  2-String Kite: 3 in r2c3,r6c8 (verbunden durch r5c3,r6c1) => r2c8<>3
    k = 0
    j = 0

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == SKYSCRAPER:
            result = findSkyscraper()
        elif type_ == TWO_STRING_KITE:
            result = findTwoStringKite()
        elif type_ == EMPTY_RECTANGLE:
            result = findEmptyRectangle()
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == SKYSCRAPER:
            pass
        elif step.getType() == TWO_STRING_KITE:
            pass
        elif step.getType() == DUAL_TWO_STRING_KITE:
            pass
        elif step.getType() == EMPTY_RECTANGLE:
            pass
        elif step.getType() == DUAL_EMPTY_RECTANGLE:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    def findAllEmptyRectangles(self):
        """ generated source for method findAllEmptyRectangles """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findEmptyRectangles(False)
        findDualEmptyRectangles(self.steps)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    def findEmptyRectangle(self):
        """ generated source for method findEmptyRectangle """
        self.steps.clear()
        step = findEmptyRectangles(True)
        if step != None and not Options.getInstance().isAllowDualsAndSiamese():
            return step
        if len(self.steps) > 0 and Options.getInstance().isAllowDualsAndSiamese():
            findDualEmptyRectangles(self.steps)
            Collections.sort(self.steps)
            return self.steps.get(0)
        return None

    def findEmptyRectangles(self, onlyOne):
        """ generated source for method findEmptyRectangles """
        i = 1
        while i <= 9:
            step = findEmptyRectanglesForCandidate(i, onlyOne)
            if step != None and onlyOne and not Options.getInstance().isAllowDualsAndSiamese():
                return step
            i += 1
        return None

    def findEmptyRectanglesForCandidate(self, cand, onlyOne):
        """ generated source for method findEmptyRectanglesForCandidate """
        free = sudoku.getFree()
        i = 0
        while len(length):
            if free[18 + i][cand] < 2 or free[18 + i][cand] > 5:
                i += 1
                continue 
            self.blockCands.set(finder.getCandidates()[cand])
            self.blockCands.and_(Sudoku2.BLOCK_TEMPLATES[i])
            j = 0
            while len(length):
                erLine = 0
                erCol = 0
                notEnoughCandidates = True
                self.tmpSet.setAnd(self.blockCands, self.erSets[i][self.j])
                if not self.tmpSet.isEmpty():
                    self.j += 1
                    continue 
                self.tmpSet.setAnd(self.blockCands, Sudoku2.LINE_TEMPLATES[self.erLines[i][self.j]])
                if len(self.tmpSet) >= 2:
                    notEnoughCandidates = False
                self.tmpSet.andNot(Sudoku2.COL_TEMPLATES[self.erCols[i][self.j]])
                if self.tmpSet.isEmpty():
                    self.j += 1
                    continue 
                erLine = self.erLines[i][self.j]
                self.tmpSet.setAnd(self.blockCands, Sudoku2.COL_TEMPLATES[self.erCols[i][self.j]])
                if len(self.tmpSet) >= 2:
                    notEnoughCandidates = False
                self.tmpSet.andNot(Sudoku2.LINE_TEMPLATES[self.erLines[i][self.j]])
                if self.tmpSet.isEmpty():
                    self.j += 1
                    continue 
                erCol = self.erCols[i][self.j]
                if notEnoughCandidates and Options.getInstance().isAllowErsWithOnlyTwoCandidates() == False:
                    self.j += 1
                    continue 
                step = checkEmptyRectangle(cand, i, self.blockCands, Sudoku2.LINES[erLine], Sudoku2.LINE_TEMPLATES, Sudoku2.COL_TEMPLATES, erCol, False, onlyOne)
                if onlyOne and step != None and not Options.getInstance().isAllowDualsAndSiamese():
                    return step
                step = checkEmptyRectangle(cand, i, self.blockCands, Sudoku2.COLS[erCol], Sudoku2.COL_TEMPLATES, Sudoku2.LINE_TEMPLATES, erLine, True, onlyOne)
                if onlyOne and step != None and not Options.getInstance().isAllowDualsAndSiamese():
                    return step
                self.j += 1
            i += 1
        return None

    def checkEmptyRectangle(self, cand, block, blockCands, indices, lineTemplates, colTemplates, firstCol, lineColReversed, onlyOne):
        """ generated source for method checkEmptyRectangle """
        i = 0
        while len(indices):
            index = indices[i]
            if sudoku.getValue(index) != 0:
                i += 1
                continue 
            if Sudoku2.getBlock(index) == block:
                i += 1
                continue 
            if sudoku.isCandidate(index, cand):
                self.tmpSet.set(finder.getCandidates()[cand])
                actCol = Sudoku2.getCol(index)
                if lineColReversed:
                    actCol = Sudoku2.getLine(index)
                self.tmpSet.and_(colTemplates[actCol])
                if len(self.tmpSet) == 2:
                    index2 = self.tmpSet.get(0)
                    if index2 == index:
                        index2 = self.tmpSet.get(1)
                    actLine = Sudoku2.getLine(index2)
                    if lineColReversed:
                        actLine = Sudoku2.getCol(index2)
                    self.tmpSet.set(finder.getCandidates()[cand])
                    self.tmpSet.and_(lineTemplates[actLine])
                    j = 0
                    while self.j < len(self.tmpSet):
                        indexDel = self.tmpSet.get(self.j)
                        if Sudoku2.getBlock(indexDel) == block:
                            self.j += 1
                            continue 
                        colDel = Sudoku2.getCol(indexDel)
                        if lineColReversed:
                            colDel = Sudoku2.getLine(indexDel)
                        if colDel == firstCol:
                            self.globalStep.reset()
                            self.globalStep.setType(SolutionType.EMPTY_RECTANGLE)
                            self.globalStep.setEntity(Sudoku2.BLOCK)
                            self.globalStep.setEntityNumber(block + 1)
                            self.globalStep.addValue(cand)
                            self.globalStep.addIndex(index)
                            self.globalStep.addIndex(index2)
                            k = 0
                            while self.k < len(blockCands):
                                self.globalStep.addFin(blockCands.get(self.k), cand)
                                self.k += 1
                            self.globalStep.addCandidateToDelete(indexDel, cand)
                            step = self.globalStep.clone()
                            if onlyOne and not Options.getInstance().isAllowDualsAndSiamese():
                                return step
                            else:
                                self.steps.add(step)
                            break
                        self.j += 1
            i += 1
        return None

    def findDualEmptyRectangles(self, ers):
        """ generated source for method findDualEmptyRectangles """
        if not Options.getInstance().isAllowDualsAndSiamese():
            return
        maxIndex = len(ers)
        i = 0
        while i < maxIndex - 1:
            j = i + 1
            while self.j < maxIndex:
                step1 = ers.get(i)
                step2 = ers.get(self.j)
                if step1.getEntity() != step2.getEntity() or step1.getEntityNumber() != step2.getEntityNumber():
                    self.j += 1
                    continue 
                if step1.getFins().size() != step2.getFins().size():
                    self.j += 1
                    continue 
                finsEqual = True
                k = 0
                while self.k < step1.getFins().size():
                    if not step1.getFins().get(self.k) == step2.getFins(.get(self.k)):
                        finsEqual = False
                        break
                    self.k += 1
                if not finsEqual:
                    self.j += 1
                    continue 
                if step1.getCandidatesToDelete().get(0) == step2.getCandidatesToDelete(.get(0)):
                    self.j += 1
                    continue 
                dual = step1.clone()
                dual.setType(SolutionType.DUAL_EMPTY_RECTANGLE)
                dual.addIndex(step2.getIndices().get(0))
                dual.addIndex(step2.getIndices().get(1))
                dual.addCandidateToDelete(step2.getCandidatesToDelete().get(0))
                ers.add(dual)
                self.j += 1
            i += 1

    def findAllSkyscrapers(self):
        """ generated source for method findAllSkyscrapers """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findSkyscraper(True, False)
        findSkyscraper(False, False)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    @overloaded
    def findSkyscraper(self):
        """ generated source for method findSkyscraper """
        self.steps.clear()
        step = self.findSkyscraper(True, True)
        if step != None:
            return step
        return self.findSkyscraper(False, True)

    @findSkyscraper.register(object, bool, bool)
    def findSkyscraper_0(self, lines, onlyOne):
        """ generated source for method findSkyscraper_0 """
        cStart = 0
        cEnd = 9
        if not lines:
            cStart += 9
            cEnd += 9
        free = sudoku.getFree()
        cand = 1
        while cand <= 9:
        __candIndex_0 = candIndex
        candIndex += 1
            constrCount = 0
            constr = cStart
            while constr < cEnd:
                if free[constr][cand] == 2:
                    indices = Sudoku2.ALL_UNITS[constr]
                    candIndex = 0
                    i = 0
                    while len(indices):
                        if sudoku.isCandidate(indices[self.i], cand):
                            self.only2Indices[constrCount][__candIndex_0] = indices[self.i]
                            if candIndex >= 2:
                                break
                        self.i += 1
                    constrCount += 1
                constr += 1
            i = 0
            while self.i < constrCount:
                j = self.i + 1
                while self.j < constrCount:
                    found = False
                    otherIndex = 1
                    if lines:
                        if Sudoku2.getCol(self.only2Indices[self.i][0]) == Sudoku2.getCol(self.only2Indices[self.j][0]):
                            found = True
                        if not found and Sudoku2.getCol(self.only2Indices[self.i][1]) == Sudoku2.getCol(self.only2Indices[self.j][1]):
                            found = True
                            otherIndex = 0
                    else:
                        if Sudoku2.getLine(self.only2Indices[self.i][0]) == Sudoku2.getLine(self.only2Indices[self.j][0]):
                            found = True
                        if not found and Sudoku2.getLine(self.only2Indices[self.i][1]) == Sudoku2.getLine(self.only2Indices[self.j][1]):
                            found = True
                            otherIndex = 0
                    if not found:
                        self.j += 1
                        continue 
                    if lines and Sudoku2.getCol(self.only2Indices[self.i][otherIndex]) == Sudoku2.getCol(self.only2Indices[self.j][otherIndex]) or not lines and Sudoku2.getLine(self.only2Indices[self.i][otherIndex]) == Sudoku2.getLine(self.only2Indices[self.j][otherIndex]):
                        self.j += 1
                        continue 
                    self.firstUnit.setAnd(finder.getCandidates()[cand], Sudoku2.buddies[self.only2Indices[self.i][otherIndex]])
                    self.firstUnit.and_(Sudoku2.buddies[self.only2Indices[self.j][otherIndex]])
                    if not self.firstUnit.isEmpty():
                        step = SolutionStep(SolutionType.SKYSCRAPER)
                        step.addValue(cand)
                        if otherIndex == 0:
                            step.addIndex(self.only2Indices[self.i][0])
                            step.addIndex(self.only2Indices[self.j][0])
                            step.addIndex(self.only2Indices[self.i][1])
                            step.addIndex(self.only2Indices[self.j][1])
                        else:
                            step.addIndex(self.only2Indices[self.i][1])
                            step.addIndex(self.only2Indices[self.j][1])
                            step.addIndex(self.only2Indices[self.i][0])
                            step.addIndex(self.only2Indices[self.j][0])
                        k = 0
                        while self.k < len(self.firstUnit):
                            step.addCandidateToDelete(self.firstUnit.get(self.k), cand)
                            self.k += 1
                        if onlyOne:
                            return step
                        else:
                            self.steps.add(step)
                    self.j += 1
                self.i += 1
            cand += 1
        return None

    def findAllTwoStringKites(self):
        """ generated source for method findAllTwoStringKites """
        sudoku = finder.getSudoku()
        oldList = self.steps
        newList = ArrayList()
        self.steps = newList
        findTwoStringKite(False)
        if Options.getInstance().isAllowDualsAndSiamese():
            findDualTwoStringKites(self.steps)
        Collections.sort(self.steps)
        self.steps = oldList
        return newList

    @overloaded
    def findTwoStringKite(self):
        """ generated source for method findTwoStringKite """
        self.steps.clear()
        step = self.findTwoStringKite(True)
        if step != None and not Options.getInstance().isAllowDualsAndSiamese():
            return step
        findDualTwoStringKites(self.steps)
        if len(self.steps) > 0:
            Collections.sort(self.steps)
            return self.steps.get(0)
        else:
            return None

    @findTwoStringKite.register(object, bool)
    def findTwoStringKite_0(self, onlyOne):
        """ generated source for method findTwoStringKite_0 """
        free = sudoku.getFree()
        cand = 1
        while cand <= 9:
        __candIndex_1 = candIndex
        candIndex += 1
            constr1Count = 0
            constr2Count = 0
            constr = 0
            while constr < 18:
                if free[constr][cand] == 2:
                    indices = Sudoku2.ALL_UNITS[constr]
                    candIndex = 0
                    i = 0
                    while len(indices):
                        if sudoku.isCandidate(indices[self.i], cand):
                            self.only2Indices[constr1Count + constr2Count][__candIndex_1] = indices[self.i]
                            if candIndex >= 2:
                                break
                        self.i += 1
                    if constr < 9:
                        constr1Count += 1
                    else:
                        constr2Count += 1
                constr += 1
            i = 0
            while self.i < constr1Count:
                j = constr1Count
                while self.j < constr1Count + constr2Count:
                    if Sudoku2.getBlock(self.only2Indices[self.i][0]) == Sudoku2.getBlock(self.only2Indices[self.j][0]):
                    elif Sudoku2.getBlock(self.only2Indices[self.i][0]) == Sudoku2.getBlock(self.only2Indices[self.j][1]):
                        tmp = self.only2Indices[self.j][0]
                        self.only2Indices[self.j][0] = self.only2Indices[self.j][1]
                        self.only2Indices[self.j][1] = tmp
                    elif Sudoku2.getBlock(self.only2Indices[self.i][1]) == Sudoku2.getBlock(self.only2Indices[self.j][0]):
                        tmp = self.only2Indices[self.i][0]
                        self.only2Indices[self.i][0] = self.only2Indices[self.i][1]
                        self.only2Indices[self.i][1] = tmp
                    elif Sudoku2.getBlock(self.only2Indices[self.i][1]) == Sudoku2.getBlock(self.only2Indices[self.j][1]):
                        tmp = self.only2Indices[self.j][0]
                        self.only2Indices[self.j][0] = self.only2Indices[self.j][1]
                        self.only2Indices[self.j][1] = tmp
                        tmp = self.only2Indices[self.i][0]
                        self.only2Indices[self.i][0] = self.only2Indices[self.i][1]
                        self.only2Indices[self.i][1] = tmp
                    else:
                        self.j += 1
                        continue 
                    if self.only2Indices[self.i][0] == self.only2Indices[self.j][0] or self.only2Indices[self.i][0] == self.only2Indices[self.j][1] or self.only2Indices[self.i][1] == self.only2Indices[self.j][0] or self.only2Indices[self.i][1] == self.only2Indices[self.j][1]:
                        self.j += 1
                        continue 
                    crossIndex = Sudoku2.getIndex(Sudoku2.getLine(self.only2Indices[self.j][1]), Sudoku2.getCol(self.only2Indices[self.i][1]))
                    if sudoku.isCandidate(crossIndex, cand):
                        step = SolutionStep(SolutionType.TWO_STRING_KITE)
                        step.addValue(cand)
                        step.addIndex(self.only2Indices[self.i][1])
                        step.addIndex(self.only2Indices[self.j][1])
                        step.addIndex(self.only2Indices[self.i][0])
                        step.addIndex(self.only2Indices[self.j][0])
                        step.addCandidateToDelete(crossIndex, cand)
                        step.addFin(self.only2Indices[self.i][0], cand)
                        step.addFin(self.only2Indices[self.j][0], cand)
                        if onlyOne and not Options.getInstance().isAllowDualsAndSiamese():
                            return step
                        else:
                            self.steps.add(step)
                    self.j += 1
                self.i += 1
            cand += 1
        return None

    def findDualTwoStringKites(self, kites):
        """ generated source for method findDualTwoStringKites """
        if not Options.getInstance().isAllowDualsAndSiamese():
            return
        maxIndex = len(kites)
        i = 0
        while i < maxIndex - 1:
            j = i + 1
            while self.j < maxIndex:
                step1 = kites.get(i)
                step2 = kites.get(self.j)
                b11 = step1.getIndices().get(2)
                b12 = step1.getIndices().get(3)
                b21 = step2.getIndices().get(2)
                b22 = step2.getIndices().get(3)
                if (b11 == b21 and b12 == b22) or (b12 == b21 and b11 == b22):
                    if step1.getCandidatesToDelete().get(0) == step2.getCandidatesToDelete(.get(0)):
                        self.j += 1
                        continue 
                    dual = step1.clone()
                    dual.setType(SolutionType.DUAL_TWO_STRING_KITE)
                    dual.addIndex(step2.getIndices().get(0))
                    dual.addIndex(step2.getIndices().get(1))
                    dual.addIndex(step2.getIndices().get(2))
                    dual.addIndex(step2.getIndices().get(3))
                    dual.addCandidateToDelete(step2.getCandidatesToDelete().get(0))
                    kites.add(dual)
                self.j += 1
            i += 1

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":0401:3:+156+87+49+3+2.4+762.+18+528....+4+7+6....8.+5+9.73....618+8.5...+32.........+3.7.5...49....487.1::381::")
        sudoku.setSudoku(":0401:3:9.567.1..61.5+4...+9.849+3+15+6....8.39.....+2.+9....+987.4...+5+61.+9782.+8+7+9.+26.51..2+1857+96:249 261 165 367 369:328::")
        solver = SudokuSolverFactory.getDefaultSolverInstance()
        step = solver.getHint(sudoku, False)
        print(step)
        System.exit(0)


if __name__ == '__main__':
    import sys
    SingleDigitPatternSolver.main(sys.argv)

