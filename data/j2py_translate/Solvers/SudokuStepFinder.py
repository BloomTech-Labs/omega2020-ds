#!/usr/bin/env python
""" generated source for module SudokuStepFinder_no_german """
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
#  * This class has two purposes:
#  * <ol>
#  * <li>It holds all configuration data for the specializes solvers and
#  * handles lazy initialization</li>
#  * <li>It caches data needed by more than one solver (e.g. ALS and RCs)</li>
#  * <li>It exposes the public API of the specialized solvers to the
#  * rest of the program.</li>
#  * </ol>
#  *
#  * @author hobiwan
#  
class SudokuStepFinder(object):
    """ generated source for class SudokuStepFinder """
    #  The specialized solver for Singles, Intersections and Subsets. 
    simpleSolver = None

    #  The specialized solver for all kinds of Fish. 
    fishSolver = None

    #  The specialized solver for single digit patterns. 
    singleDigitPatternSolver = None

    #  The specialized solver for all kinds of Uniqueness techniques. 
    uniquenessSolver = None

    #  The specialized solver for Wings. 
    wingSolver = None

    #  The specialized solver for Coloring. 
    coloringSolver = None

    #  The specialized solver for simple chains. 
    chainSolver = None

    #  The specialized solver for ALS moves. 
    alsSolver = None

    #  The specialized solver for SDC. 
    miscellaneousSolver = None

    #  The specialized solver for complicated chains. 
    tablingSolver = None

    #  The specialized solver for Templates. 
    templateSolver = None

    #  The specialized solver for guessing. 
    bruteForceSolver = None

    #  The specialized solver for Incomplete Solutions. 
    incompleteSolver = None

    #  The specialized solver for giving up. 
    giveUpSolver = None

    #  An array for all specialized solvers. Makes finding steps easier. 
    solvers = []

    #  The sudoku for which steps should be found. 
    sudoku = None

    #  The step configuration for searches. 
    stepConfigs = []

    #  A status counter that changes every time a new step has been found. Specialized
    #      *  solvers can use this counter to use cached steps instead of searching for them
    #      *  if no step was found since the last search.
    #      
    stepNumber = 0

    #  for timing 
    templateNanos = long()

    #  for timing 
    templateAnz = int()

    #  Lazy initialization: The solvers are only created when they are used. 
    initialized = False

    #  If set to <code>true</code>, the StepFinder contains only one {@link SimpleSolver} instance. 
    simpleOnly = False

    #  Data that is used by more than one specialized solver
    #  One set with all positions left for each candidate. 
    candidates = [None] * 10

    #  Dirty flag for candidates. 
    candidatesDirty = True

    #  One set with all set cells for each candidate. 
    positions = [None] * 10

    #  Dirty flag for positions. 
    positionsDirty = True

    #  One set with all cells where a candidate is still possible 
    candidatesAllowed = [None] * 10

    #  Dirty flag for candidatesAllowed. 
    candidatesAllowedDirty = True

    #  A set for all cells that are not set yet 
    emptyCells = SudokuSet()

    #  One template per candidate with all positions that can be set immediately. 
    setValueTemplates = [None] * 10

    #  One template per candidate with all positions from which the candidate can be eliminated immediately. 
    delCandTemplates = [None] * 10

    #  The lists with all valid templates for each candidate. 
    candTemplates = None

    #  Dirty flag for templates (without refinements). 
    templatesDirty = True

    #  Dirty flag for templates (with refinements). 
    templatesListDirty = True

    #  Cache for ALS entries (only ALS with more than one cell). 
    alsesOnlyLargerThanOne = None

    #  Step number for which {@link #alsesOnlyLargerThanOne} was computed. 
    alsesOnlyLargerThanOneStepNumber = -1

    #  Cache for ALS entries (ALS with one cell allowed). 
    alsesWithOne = None

    #  Step number for which {@link #alsesWithOne} was computed. 
    alsesWithOneStepNumber = -1

    #  Cache for RC entries. 
    restrictedCommons = None

    #  start indices into {@link #restrictedCommons} for all ALS. 
    startIndices = None

    #  end indices into {@link #restrictedCommons} for all ALS. 
    endIndices = None

    #  Overlap status at last RC search. 
    lastRcAllowOverlap = bool()

    #  Step number for which {@link #restrictedCommons} was computed. 
    lastRcStepNumber = -1

    #  ALS list for which RCs were calculated. 
    lastRcAlsList = None

    #  Was last RC search only for forward references? 
    lastRcOnlyForward = True

    #  Collect RCs for forward search only 
    rcOnlyForward = True

    #  temporary varibles for calculating ALS and RC
    #  Temporary set for recursion: all cells of each try 
    indexSet = SudokuSet()

    #  Temporary set for recursion: all numbers contained in {@link #indexSet}. 
    candSets = [None] * 10

    #  statistics: total time for all calls 
    alsNanos = long()

    #  statistics: number of calls 
    anzAlsCalls = int()

    #  statistics: number of ALS found 
    anzAls = int()

    #  statistics: number of ALS found more than once 
    doubleAls = int()

    #  All candidates common to two ALS. 
    possibleRestrictedCommonsSet = 0

    #  Holds all buddies of all candidate cells for one RC (including the candidate cells themselves). 
    restrictedCommonBuddiesSet = SudokuSet()

    #  All cells containing a specific candidate in two ALS. 
    restrictedCommonIndexSet = SudokuSet()

    #  Contains the indices of all overlapping cells in two ALS. 
    intersectionSet = SudokuSet()

    #  statistics: total time for all calls 
    rcNanos = long()

    #  statistics: number of calls 
    rcAnzCalls = int()

    #  statistics: number of RCs found 
    anzRcs = int()

    # 
    #      * Creates an instance of the class.
    #      
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        self.__init__(False)

    # 
    #      * Creates an instance of the class.
    #      * @param simpleOnly If set, the StepFinder contains only an instance of SimpleSolver
    #      
    @__init__.register(object, bool)
    def __init___0(self, simpleOnly):
        """ generated source for method __init___0 """
        self.simpleOnly = simpleOnly
        self.initialized = False

    def initialize(self):
        """ generated source for method initialize """
        if self.initialized:
            return
        #  Create all Sets
        i = 0
        while len(candidates):
            self.candidates[i] = SudokuSet()
            self.positions[i] = SudokuSet()
            self.candidatesAllowed[i] = SudokuSet()
            i += 1
        #  Create all templates
        self.candTemplates = ArrayList(10)
        i = 0
        while len(setValueTemplates):
            self.setValueTemplates[i] = SudokuSet()
            self.delCandTemplates[i] = SudokuSet()
            self.candTemplates.add(i, LinkedList())
            i += 1
        #  Create the solvers
        self.simpleSolver = SimpleSolver(self)
        if not self.simpleOnly:
            self.fishSolver = FishSolver(self)
            self.singleDigitPatternSolver = SingleDigitPatternSolver(self)
            self.uniquenessSolver = UniquenessSolver(self)
            self.wingSolver = WingSolver(self)
            self.coloringSolver = ColoringSolver(self)
            self.chainSolver = ChainSolver(self)
            self.alsSolver = AlsSolver(self)
            self.miscellaneousSolver = MiscellaneousSolver(self)
            self.tablingSolver = TablingSolver(self)
            self.templateSolver = TemplateSolver(self)
            self.bruteForceSolver = BruteForceSolver(self)
            self.incompleteSolver = IncompleteSolver(self)
            self.giveUpSolver = GiveUpSolver(self)
            self.solvers = [None] * 
        else:
            self.solvers = [None] * 
        self.initialized = True

    # 
    #      * Calls the {@link AbstractSolver#cleanUp() } method for every
    #      * specialized solver. This method is called from an extra
    #      * thread from within {@link SudokuSolverFactory}. No synchronization
    #      * is done here to speed things up, if the functionality is not used.<br>
    #      *
    #      * Specialized solvers, that use cleanup, have to implement synchronization
    #      * themselves.
    #      
    def cleanUp(self):
        """ generated source for method cleanUp """
        if self.solvers == None:
            return
        for solver in solvers:
            solver.cleanUp()

    # 
    #      * Gets the next step of type <code>type</code>.
    #      * @param type
    #      * @return
    #      
    def getStep(self, type_):
        """ generated source for method getStep """
        self.initialize()
        result = None
        i = 0
        while len(solvers):
            if (result = self.solvers[i].getStep(type_)) != None:
                self.stepNumber += 1
                return result
            i += 1
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        self.initialize()
        i = 0
        while len(solvers):
            if self.solvers[i].doStep(step):
                setSudokuDirty()
                return
            i += 1
        raise RuntimeException("Invalid solution step in doStep() (" + step.getType() + ")")

    def setSudokuDirty(self):
        """ generated source for method setSudokuDirty """
        self.candidatesDirty = True
        self.candidatesAllowedDirty = True
        self.positionsDirty = True
        self.templatesDirty = True
        self.templatesListDirty = True
        self.stepNumber += 1

    def setSudoku(self, sudoku):
        """ generated source for method setSudoku """
        if sudoku != None and self.sudoku != sudoku:
            self.sudoku = sudoku
        self.setSudokuDirty()

    def getSudoku(self):
        """ generated source for method getSudoku """
        return self.sudoku

    def setStepConfigs(self, stepConfigs):
        """ generated source for method setStepConfigs """
        self.stepConfigs = stepConfigs

    def getTablingSolver(self):
        """ generated source for method getTablingSolver """
        return self.tablingSolver

    def findAllFullHouses(self, newSudoku):
        """ generated source for method findAllFullHouses """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllFullHouses()
        self.setSudoku(oldSudoku)
        return steps

    def findAllNakedSingles(self, newSudoku):
        """ generated source for method findAllNakedSingles """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllNakedSingles()
        self.setSudoku(oldSudoku)
        return steps

    def findAllNakedXle(self, newSudoku):
        """ generated source for method findAllNakedXle """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllNakedXle()
        self.setSudoku(oldSudoku)
        return steps

    def findAllHiddenSingles(self, newSudoku):
        """ generated source for method findAllHiddenSingles """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllHiddenSingles()
        self.setSudoku(oldSudoku)
        return steps

    def findAllHiddenXle(self, newSudoku):
        """ generated source for method findAllHiddenXle """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllHiddenXle()
        self.setSudoku(oldSudoku)
        return steps

    def findAllLockedCandidates(self, newSudoku):
        """ generated source for method findAllLockedCandidates """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllLockedCandidates()
        self.setSudoku(oldSudoku)
        return steps

    def findAllLockedCandidates1(self, newSudoku):
        """ generated source for method findAllLockedCandidates1 """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllLockedCandidates()
        self.setSudoku(oldSudoku)
        resultList = ArrayList()
        for step in steps:
            if step.getType() == SolutionType.LOCKED_CANDIDATES_1:
                resultList.add(step)
        return resultList

    def findAllLockedCandidates2(self, newSudoku):
        """ generated source for method findAllLockedCandidates2 """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.simpleSolver.findAllLockedCandidates()
        self.setSudoku(oldSudoku)
        resultList = ArrayList()
        for step in steps:
            if step.getType() == SolutionType.LOCKED_CANDIDATES_2:
                resultList.add(step)
        return resultList

    def getAllFishes(self, newSudoku, minSize, maxSize, maxFins, maxEndoFins, dlg, forCandidate, type_):
        """ generated source for method getAllFishes """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.fishSolver.getAllFishes(minSize, maxSize, maxFins, maxEndoFins, dlg, forCandidate, type_)
        self.setSudoku(oldSudoku)
        return steps

    def getAllKrakenFishes(self, newSudoku, minSize, maxSize, maxFins, maxEndoFins, dlg, forCandidate, type_):
        """ generated source for method getAllKrakenFishes """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.fishSolver.getAllKrakenFishes(minSize, maxSize, maxFins, maxEndoFins, dlg, forCandidate, type_)
        self.setSudoku(oldSudoku)
        return steps

    def findAllEmptyRectangles(self, newSudoku):
        """ generated source for method findAllEmptyRectangles """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.singleDigitPatternSolver.findAllEmptyRectangles()
        self.setSudoku(oldSudoku)
        return steps

    def findAllSkyScrapers(self, newSudoku):
        """ generated source for method findAllSkyScrapers """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.singleDigitPatternSolver.findAllSkyscrapers()
        self.setSudoku(oldSudoku)
        return steps

    def findAllTwoStringKites(self, newSudoku):
        """ generated source for method findAllTwoStringKites """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.singleDigitPatternSolver.findAllTwoStringKites()
        self.setSudoku(oldSudoku)
        return steps

    def getAllUniqueness(self, newSudoku):
        """ generated source for method getAllUniqueness """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.uniquenessSolver.getAllUniqueness()
        self.setSudoku(oldSudoku)
        return steps

    def getAllWings(self, newSudoku):
        """ generated source for method getAllWings """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.wingSolver.getAllWings()
        self.setSudoku(oldSudoku)
        return steps

    def findAllSimpleColors(self, newSudoku):
        """ generated source for method findAllSimpleColors """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.coloringSolver.findAllSimpleColors()
        self.setSudoku(oldSudoku)
        return steps

    def findAllMultiColors(self, newSudoku):
        """ generated source for method findAllMultiColors """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.coloringSolver.findAllMultiColors()
        self.setSudoku(oldSudoku)
        return steps

    def getAllChains(self, newSudoku):
        """ generated source for method getAllChains """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.chainSolver.getAllChains()
        self.setSudoku(oldSudoku)
        return steps

    def getAllAlses(self, newSudoku, doXz, doXy, doChain):
        """ generated source for method getAllAlses """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.alsSolver.getAllAlses(doXz, doXy, doChain)
        self.setSudoku(oldSudoku)
        return steps

    def getAllDeathBlossoms(self, newSudoku):
        """ generated source for method getAllDeathBlossoms """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.alsSolver.getAllDeathBlossoms()
        self.setSudoku(oldSudoku)
        return steps

    def getAllSueDeCoqs(self, newSudoku):
        """ generated source for method getAllSueDeCoqs """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.miscellaneousSolver.getAllSueDeCoqs()
        self.setSudoku(oldSudoku)
        return steps

    def getAllNiceLoops(self, newSudoku):
        """ generated source for method getAllNiceLoops """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.tablingSolver.getAllNiceLoops()
        self.setSudoku(oldSudoku)
        return steps

    def getAllGroupedNiceLoops(self, newSudoku):
        """ generated source for method getAllGroupedNiceLoops """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.tablingSolver.getAllGroupedNiceLoops()
        self.setSudoku(oldSudoku)
        return steps

    def getAllForcingChains(self, newSudoku):
        """ generated source for method getAllForcingChains """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.tablingSolver.getAllForcingChains()
        self.setSudoku(oldSudoku)
        return steps

    def getAllForcingNets(self, newSudoku):
        """ generated source for method getAllForcingNets """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.tablingSolver.getAllForcingNets()
        self.setSudoku(oldSudoku)
        return steps

    def getAllTemplates(self, newSudoku):
        """ generated source for method getAllTemplates """
        self.initialize()
        oldSudoku = self.getSudoku()
        self.setSudoku(newSudoku)
        steps = self.templateSolver.getAllTemplates()
        self.setSudoku(oldSudoku)
        return steps

    def getCandidates(self):
        """ generated source for method getCandidates """
        if self.candidatesDirty:
            initCandidates()
        return self.candidates

    def getPositions(self):
        """ generated source for method getPositions """
        if self.positionsDirty:
            initPositions()
        return self.positions

    def initCandidates(self):
        """ generated source for method initCandidates """
        if self.candidatesDirty:
            i = 1
            while len(candidates):
                self.candidates[i].clear()
                i += 1
            cells = self.sudoku.getCells()
            i = 0
            while len(cells):
                cands = Sudoku2.POSSIBLE_VALUES[cells[i]]
                j = 0
                while len(cands):
                    self.candidates[cands[j]].add(i)
                    j += 1
                i += 1
            self.candidatesDirty = False

    def initPositions(self):
        """ generated source for method initPositions """
        if self.positionsDirty:
            i = 1
            while len(positions):
                self.positions[i].clear()
                i += 1
            values = self.sudoku.getValues()
            i = 0
            while len(values):
                if values[i] != 0:
                    self.positions[values[i]].add(i)
                i += 1
            self.positionsDirty = False

    def getCandidatesAllowed(self):
        """ generated source for method getCandidatesAllowed """
        if self.candidatesAllowedDirty:
            initCandidatesAllowed()
        return self.candidatesAllowed

    def getEmptyCells(self):
        """ generated source for method getEmptyCells """
        if self.candidatesAllowedDirty:
            initCandidatesAllowed()
        return self.emptyCells

    def initCandidatesAllowed(self):
        """ generated source for method initCandidatesAllowed """
        if self.candidatesAllowedDirty:
            self.emptyCells.setAll()
            i = 1
            while len(candidatesAllowed):
                self.candidatesAllowed[i].setAll()
                i += 1
            values = self.sudoku.getValues()
            i = 0
            while len(values):
                if values[i] != 0:
                    self.candidatesAllowed[values[i]].andNot(Sudoku2.buddies[i])
                    self.emptyCells.remove(i)
                i += 1
            i = 1
            while len(candidatesAllowed):
                self.candidatesAllowed[i].and_(self.emptyCells)
                i += 1
            self.candidatesAllowedDirty = False

    def getDelCandTemplates(self, initLists):
        """ generated source for method getDelCandTemplates """
        if (initLists and self.templatesListDirty) or (not initLists and self.templatesDirty):
            initCandTemplates(initLists)
        return self.delCandTemplates

    def getSetValueTemplates(self, initLists):
        """ generated source for method getSetValueTemplates """
        if (initLists and self.templatesListDirty) or (not initLists and self.templatesDirty):
            initCandTemplates(initLists)
        return self.setValueTemplates

    def initCandTemplates(self, initLists):
        """ generated source for method initCandTemplates """
        self.templateAnz += 1
        nanos = System.nanoTime()
        if (initLists and self.templatesListDirty) or (not initLists and self.templatesDirty):
            allowedPositions = self.getCandidates()
            setPositions = self.getPositions()
            templates = Sudoku2.templates
            forbiddenPositions = [None] * 10
            i = 1
            while i <= 9:
                self.setValueTemplates[i].setAll()
                self.delCandTemplates[i].clear()
                self.candTemplates.get(i).clear()
                forbiddenPositions[i] = SudokuSetBase()
                forbiddenPositions[i].set(setPositions[i])
                forbiddenPositions[i].or_(allowedPositions[i])
                forbiddenPositions[i].not_()
                i += 1
            i = 0
            while len(templates):
                j = 1
                while j <= 9:
                    if not setPositions[j].andEquals(templates[i]):
                        j += 1
                        continue 
                    if not forbiddenPositions[j].andEmpty(templates[i]):
                        j += 1
                        continue 
                    self.setValueTemplates[j].and_(templates[i])
                    self.delCandTemplates[j].or_(templates[i])
                    if initLists:
                        self.candTemplates.get(j).add(templates[i])
                    j += 1
                i += 1
            if initLists:
                removals = 0
                while True:
                    removals = 0
                    j = 1
                    while j <= 9:
                        self.setValueTemplates[j].setAll()
                        self.delCandTemplates[j].clear()
                        it = self.candTemplates.get(j).listIterator()
                        while it.hasNext():
                            template = it.next()
                            removed = False
                            k = 1
                            while k <= 9:
                                if k != j and not template.andEmpty(self.setValueTemplates[k]):
                                    it.remove()
                                    removed = True
                                    removals += 1
                                    break
                                k += 1
                            if not removed:
                                self.setValueTemplates[j].and_(template)
                                self.delCandTemplates[j].or_(template)
                        j += 1
                    if not ((removals > 0)):
                        break
            i = 1
            while i <= 9:
                self.delCandTemplates[i].not_()
                i += 1
            self.templatesDirty = False
            if initLists:
                self.templatesListDirty = False
        self.templateNanos += System.nanoTime() - nanos

    def getStepNumber(self):
        """ generated source for method getStepNumber """
        return self.stepNumber

    @overloaded
    def getAlses(self):
        """ generated source for method getAlses """
        return self.getAlses(False)

    @getAlses.register(object, bool)
    def getAlses_0(self, onlyLargerThanOne):
        """ generated source for method getAlses_0 """
        if onlyLargerThanOne:
            if self.alsesOnlyLargerThanOneStepNumber == self.stepNumber:
                return self.alsesOnlyLargerThanOne
            else:
                self.alsesOnlyLargerThanOne = doGetAlses(onlyLargerThanOne)
                self.alsesOnlyLargerThanOneStepNumber = self.stepNumber
                return self.alsesOnlyLargerThanOne
        else:
            if self.alsesWithOneStepNumber == self.stepNumber:
                return self.alsesWithOne
            else:
                self.alsesWithOne = doGetAlses(onlyLargerThanOne)
                self.alsesWithOneStepNumber = self.stepNumber
                return self.alsesWithOne

    def doGetAlses(self, onlyLargerThanOne):
        """ generated source for method doGetAlses """
        actNanos = System.nanoTime()
        alses = ArrayList(300)
        alses.clear()
        i = 0
        while len(length):
            j = 0
            while len(length):
                self.indexSet.clear()
                self.candSets[0] = 0
                checkAlsRecursive(0, j, Sudoku2.ALL_UNITS[i], alses, onlyLargerThanOne)
                j += 1
            i += 1
        for als in alses:
            als.computeFields(self)
        self.alsNanos += (System.nanoTime() - actNanos)
        self.anzAlsCalls += 1
        return alses

    def checkAlsRecursive(self, anzahl, startIndex, indexe, alses, onlyLargerThanOne):
        """ generated source for method checkAlsRecursive """
        anzahl += 1
        if anzahl > len(indexe):
            return
        i = startIndex
        while len(indexe):
            houseIndex = indexe[i]
            if self.sudoku.getValue(houseIndex) != 0:
                i += 1
                continue 
            self.indexSet.add(houseIndex)
            self.candSets[anzahl] = int((self.candSets[anzahl - 1] | self.sudoku.getCell(houseIndex)))
            if Sudoku2.ANZ_VALUES[self.candSets[anzahl]] - anzahl == 1:
                if not onlyLargerThanOne or len(self.indexSet) > 1:
                    self.anzAls += 1
                    newAls = Als(self.indexSet, self.candSets[anzahl])
                    if not alses.contains(newAls):
                        alses.add(newAls)
                    else:
                        self.doubleAls += 1
            self.checkAlsRecursive(anzahl, i + 1, indexe, alses, onlyLargerThanOne)
            self.indexSet.remove(houseIndex)
            i += 1

    def getAlsStatistics(self):
        """ generated source for method getAlsStatistics """
        return "Statistic for getAls(): number of calls: " + self.anzAlsCalls + ", total time: " + (self.alsNanos / 1000) + "us, average: " + (self.alsNanos / self.anzAlsCalls / 1000) + "us\r\n" + "    anz: " + self.anzAls + "/" + (self.anzAls / self.anzAlsCalls) + ", double: " + self.doubleAls + "/" + (self.doubleAls / self.anzAlsCalls) + " res: " + (self.anzAls - self.doubleAls) + "/" + ((self.anzAls - self.doubleAls) / self.anzAlsCalls)

    def getRestrictedCommons(self, alses, allowOverlap):
        """ generated source for method getRestrictedCommons """
        if self.lastRcStepNumber != self.stepNumber or self.lastRcAllowOverlap != allowOverlap or self.lastRcAlsList != alses or self.lastRcOnlyForward != self.rcOnlyForward:
            if self.startIndices == None or len(startIndices):
                self.startIndices = [None] * int((len(alses) * 1.5))
                self.endIndices = [None] * int((len(alses) * 1.5))
            self.restrictedCommons = doGetRestrictedCommons(alses, allowOverlap)
            self.lastRcStepNumber = self.stepNumber
            self.lastRcAllowOverlap = allowOverlap
            self.lastRcOnlyForward = self.rcOnlyForward
            self.lastRcAlsList = alses
        return self.restrictedCommons

    def getStartIndices(self):
        """ generated source for method getStartIndices """
        return self.startIndices

    def getEndIndices(self):
        """ generated source for method getEndIndices """
        return self.endIndices

    def setRcOnlyForward(self, rof):
        """ generated source for method setRcOnlyForward """
        self.rcOnlyForward = rof

    def isRcOnlyForward(self):
        """ generated source for method isRcOnlyForward """
        return self.rcOnlyForward

    def doGetRestrictedCommons(self, alses, withOverlap):
        """ generated source for method doGetRestrictedCommons """
        self.rcAnzCalls += 1
        actNanos = 0
        actNanos = System.nanoTime()
        self.lastRcOnlyForward = self.rcOnlyForward
        rcs = ArrayList(2000)
        i = 0
        while i < len(alses):
            als1 = alses.get(i)
            self.startIndices[i] = len(rcs)
            start = 0
            if self.rcOnlyForward:
                start = i + 1
            j = start
            while j < len(alses):
                if i == j:
                    j += 1
                    continue 
                als2 = alses.get(j)
                self.intersectionSet.set(als1.indices)
                self.intersectionSet.and_(als2.indices)
                if not withOverlap and not self.intersectionSet.isEmpty():
                    j += 1
                    continue 
                self.possibleRestrictedCommonsSet = als1.candidates
                self.possibleRestrictedCommonsSet &= als2.candidates
                if self.possibleRestrictedCommonsSet == 0:
                    j += 1
                    continue 
                rcAnz = 0
                newRC = None
                prcs = Sudoku2.POSSIBLE_VALUES[self.possibleRestrictedCommonsSet]
                k = 0
                while len(prcs):
                    cand = prcs[k]
                    self.restrictedCommonIndexSet.set(als1.indicesPerCandidat[cand])
                    self.restrictedCommonIndexSet.or_(als2.indicesPerCandidat[cand])
                    if not self.restrictedCommonIndexSet.andEmpty(self.intersectionSet):
                        k += 1
                        continue 
                    self.restrictedCommonBuddiesSet.setAnd(als1.buddiesAlsPerCandidat[cand], als2.buddiesAlsPerCandidat[cand])
                    if self.restrictedCommonIndexSet.andEquals(self.restrictedCommonBuddiesSet):
                        if rcAnz == 0:
                            newRC = RestrictedCommon(i, j, cand)
                            rcs.add(newRC)
                            self.anzRcs += 1
                        else:
                            newRC.setCand2(cand)
                        rcAnz += 1
                    k += 1
                if rcAnz > 0:
                j += 1
            self.endIndices[i] = len(rcs)
            i += 1
        actNanos = System.nanoTime() - actNanos
        self.rcNanos += actNanos
        return rcs

    def getRCStatistics(self):
        """ generated source for method getRCStatistics """
        return "Statistic for getRestrictedCommons(): number of calls: " + self.rcAnzCalls + ", total time: " + (self.rcNanos / 1000) + "us, average: " + (self.rcNanos / self.rcAnzCalls / 1000) + "us\r\n" + "    anz: " + self.anzRcs + "/" + (self.anzRcs / self.rcAnzCalls)

    def printStatistics(self):
        """ generated source for method printStatistics """

