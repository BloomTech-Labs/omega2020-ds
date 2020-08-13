#!/usr/bin/env python
""" generated source for module TablingSolver_no_german """
from __future__ import print_function
from functools import wraps
from threading import RLock

def lock_for_object(obj, locks={}):
    return locks.setdefault(id(obj), RLock())

def synchronized(call):
    assert call.__code__.co_varnames[0] in ['self', 'cls']
    @wraps(call)
    def inner(*args, **kwds):
        with lock_for_object(args[0]):
            return call(*args, **kwds)
    return inner

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
#  * Implements Trebors Tables for finding Nice Loops, AICs, Forcing Chains and
#  * Forcing Nets. Also called by the {@link FishSolver} for finding suitable
#  * chains for Kraken Fish.<br><br>
#  *
#  * The idea of tabling is simple: For all possible premises ("candidate n is set
#  * in/eliminated from cell x") all possible outcomes are logged. The result is
#  * then checked for contradictions or verities. For chains only direct outcomes
#  * are stored, for nets every possible outcome triggers a new round of starting
#  * conditions (up to a maximum recursion depth). For every premise a separate
#  * table is used.<br><br>
#  *
#  * After the initial round all tables are expanded: For every possible outcome
#  * all other outcomes from the other table are added. This results in a matrix
#  * holding all possible conclusions. The method is simple but it uses a lot of
#  * memory and computation time.<br><br>
#  *
#  * The real problem with Trebors Tables is to reconstruct the chains/nets that
#  * led to the result.<br><br>
#  *
#  * Some tests currently implemented (every table holds an array with sets for
#  * all cells than can be set to a certain candidate - onSets - and with set for
#  * cell where that candidate can be eliminated - offSets): <ol> <li>only one
#  * chain:<ul> <li>two values set in the same cell (AND onSets) -> premise was
#  * wrong </li> <li>same value set twice in one house -> premise was wrong</li>
#  * <li>all candidates deleted from a cell -> premise was wrong</li>
#  * <li>candidate cand be set in and deleted from a cell simultaneously ->
#  * premise was wrong</li> <li>all candidates are deleted from a cell -> premise
#  * was wrong</li></ul></li> <li>two chains for the same start candidate
#  * (candidate set and deleted):<ul> <li>both chains lead to the same value in
#  * onSets -> value can be set</li> <li>both chains lead to the same value in
#  * offSets -> candidate can be deleted</li></ul></li> <li>chains for all
#  * candidates in one house/cell set:<ul> <li>both chains lead to the same value
#  * in onSets -> value can be set</li> <li>both chains lead to the same value in
#  * offSets -> candidate can be deleted</li></ul></li> </ol>
#  *
#  * 20081013: AIC added (combined with Nice Loops)<br><br> For every Nice Loop
#  * that starts with a strong inference out of the start cell and ends with a
#  * weak inference into the start cell the AIC (start cell - last strong
#  * inference) is checked. If it gives more than one elimination, it is stored as
#  * AIC instead of as Nice Loop. The check is done for discontinuous loops
#  * only.<br><br>
#  *
#  * AIC eliminations: <ul> <li>if the candidates of the endpoints are equal, all
#  * candidates can be eliminated that see both endpoints</li> <li>if the
#  * candidates are not equal, cand A can be eliminated in cell b and vice
#  * versa</li> </ul>
#  *
#  * @author hobiwan
#  
class TablingSolver(AbstractSolver):
    """ generated source for class TablingSolver """
    CLEANUP_INTERVAL = 5 * 60 * 1000

    # 
    #      * Enable additional output for debugging.
    #      
    DEBUG = False

    # 
    #      * Maximum recursion depth in buildung the tables.
    #      
    MAX_REC_DEPTH = 50

    # 
    #      * A special comparator for comparing chains and nets.
    #      
    tablingComparator = None

    # 
    #      * A list with steps found in the current run.
    #      
    steps = None

    #  gefundene Losungsschritte
    # 
    #      * One global step for optimization.
    #      
    globalStep = SolutionStep(SolutionType.HIDDEN_SINGLE)

    # 
    #      * All chains already found: eliminations + index in {@link #steps}.
    #      
    deletesMap = TreeMap()

    # 
    #      * Search only for chains, not for nets.
    #      
    chainsOnly = True

    # 
    #      * Include group nodes in search.
    #      
    withGroupNodes = False

    # 
    #      * Include ALS nodes in search.
    #      
    withAlsNodes = False

    # 
    #      * Accept steps only if they contain group nodes/ALS nodes.
    #      
    onlyGroupedNiceLoops = False

    # 
    #      * One table for every premise. Indices are in format "nnm" with "nn" the
    #      * index of the cell and "m" the candidate. This table holds all entries for
    #      * "candidate m set in cell nn".
    #      
    onTable = None

    # 
    #      * One table for every premise. Indices are in format "nnm" with "nn" the
    #      * index of the cell and "m" the candidate. This table holds all entries for
    #      * "candidate m deleted from cell nn".
    #      
    offTable = None

    # 
    #      * A list of all table entries for e specific candidate in a house or for
    #      * all candidates in a cell respectively. Used for Forcing chain/Net checks.
    #      
    entryList = ArrayList(10)

    # 
    #      * For temporary checks.
    #      
    tmpSet = SudokuSet()

    # 
    #      * For temporary checks.
    #      
    tmpSet1 = SudokuSet()

    # 
    #      * For temporary checks.
    #      
    tmpSet2 = SudokuSet()

    # 
    #      * For buildung chains.
    #      
    tmpSetC = SudokuSet()

    # 
    #      * Used to check if all candidates in a house or cell set lead to the same
    #      * value in a cell.
    #      
    tmpOnSets = [None] * 10

    # 
    #      * Used to check if all candidates in a house or cell deleted lead to the
    #      * same canddiate deleted from a cell.
    #      
    tmpOffSets = [None] * 10

    # 
    #      * Map containing the new indices of all alses, that have already been
    #      * written to globalStep. They key is the old index into {@link #alses}, the
    #      * value is the new index of the ALS stored in the {@link SolutionStep}.
    #      
    chainAlses = TreeMap()
    savedSudoku = None

    #  Sudoku2 im Ausgangszustand (fur Erstellen der Tables)
    retIndices = [None] * MAX_REC_DEPTH

    #  indices ermitteln
    #     private int[][] retIndices1 = new int[MAX_REC_DEPTH][5]; // indices ermitteln
    groupNodes = None

    #  a list with all group nodes for a given sudoku
    alses = None

    #  a list with all available ALS for a given sudoku
    #     private SudokuSet alsBuddies = new SudokuSet(); // cells that can see all the cells of the als
    alsEliminations = [None] * 10

    #  all cells with elminations for an als, sorted by candidate
    simpleFinder = None
    singleSteps = ArrayList()

    #  fur Naked und Hidden Singles
    chain = [None] * Options.getInstance().getMaxTableEntryLength()

    #  globale chain fur buildChain()
    chainIndex = 0

    #  Index des nachsten Elements in chain[]
    mins = [None] * 200

    #  globale chains fur networks
    minIndexes = [None] * 

    #  Indexe der nachsten Elemente in mins[]
    actMin = 0

    #  derzeit aktuelles min
    tmpChain = [None] * Options.getInstance().getMaxTableEntryLength()

    #  globale chain fur addChain()
    tmpChains = [None] * 9
    tmpChainsIndex = 0
    lassoSet = SudokuSet()

    #  fur addChain: enthalt alle Zellen-Indices der Chain
    extendedTable = None

    #  Tables for group nodes, ALS, AUR...
    extendedTableMap = None

    #  entry -> index in extendedTable
    extendedTableIndex = 0

    #  current index in extendedTable
    initialized = False
    lastUsed = -1

    # 
    #      * Creates a new instance of TablingSolver
    #      *
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(TablingSolver, self).__init__(finder)
        self.simpleFinder = SudokuStepFinder(True)
        i = 0
        while len(tmpOnSets):
            self.tmpOnSets[i] = SudokuSet()
            self.tmpOffSets[i] = SudokuSet()
            i += 1
        self.steps = ArrayList()
        if self.tablingComparator == None:
            self.tablingComparator = TablingComparator()
        i = 0
        while len(tmpChains):
            self.tmpChains[i] = Chain()
            self.tmpChains[i].setChain([None] * Options.getInstance().getMaxTableEntryLength())
            i += 1
        i = 0
        while len(alsEliminations):
            self.alsEliminations[i] = SudokuSet()
            i += 1

    def initialize(self):
        """ generated source for method initialize """
        if not self.initialized:
            self.onTable = [None] * 810
            self.offTable = [None] * 810
            i = 0
            while len(onTable):
                self.onTable[i] = TableEntry()
                self.offTable[i] = TableEntry()
                i += 1
            self.extendedTable = ArrayList()
            self.extendedTableMap = TreeMap()
            self.extendedTableIndex = 0
            self.initialized = True
        self.lastUsed = System.currentTimeMillis()

    def cleanUp(self):
        """ generated source for method cleanUp """
        with lock_for_object(self):
            if self.initialized and (System.currentTimeMillis() - self.lastUsed) > self.CLEANUP_INTERVAL:
                i = 0
                while len(onTable):
                    self.onTable[i] = None
                    self.offTable[i] = None
                    i += 1
            self.onTable = None
            self.offTable = None
            if self.extendedTable != None:
                i = 0
                while i < self.extendedTableIndex:
                    self.extendedTable.set(i, None)
                    i += 1
                self.extendedTable = None
            if self.extendedTableMap != None:
                self.extendedTableMap.clear()
                self.extendedTableMap = None
            self.extendedTableIndex = 0
            self.initialized = False

    def resetTmpChains(self):
        """ generated source for method resetTmpChains """
        i = 0
        while len(tmpChains):
            self.tmpChains[i].reset()
            i += 1
        self.tmpChainsIndex = 0

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == NICE_LOOP:
            pass
        elif type_ == CONTINUOUS_NICE_LOOP:
            pass
        elif type_ == DISCONTINUOUS_NICE_LOOP:
            pass
        elif type_ == AIC:
            self.withGroupNodes = False
            self.withAlsNodes = False
            result = getNiceLoops()
        elif type_ == GROUPED_NICE_LOOP:
            pass
        elif type_ == GROUPED_CONTINUOUS_NICE_LOOP:
            pass
        elif type_ == GROUPED_DISCONTINUOUS_NICE_LOOP:
            pass
        elif type_ == GROUPED_AIC:
            self.withGroupNodes = True
            self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
            result = getNiceLoops()
        elif type_ == FORCING_CHAIN:
            pass
        elif type_ == FORCING_CHAIN_CONTRADICTION:
            pass
        elif type_ == FORCING_CHAIN_VERITY:
            self.steps.clear()
            self.withGroupNodes = True
            self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
            getForcingChains()
            if len(self.steps) > 0:
                Collections.sort(self.steps, self.tablingComparator)
                result = self.steps.get(0)
        elif type_ == FORCING_NET:
            pass
        elif type_ == FORCING_NET_CONTRADICTION:
            pass
        elif type_ == FORCING_NET_VERITY:
            self.steps.clear()
            self.withGroupNodes = True
            self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
            getForcingNets()
            if len(self.steps) > 0:
                Collections.sort(self.steps, self.tablingComparator)
                result = self.steps.get(0)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == NICE_LOOP:
            pass
        elif step.getType() == CONTINUOUS_NICE_LOOP:
            pass
        elif step.getType() == DISCONTINUOUS_NICE_LOOP:
            pass
        elif step.getType() == AIC:
            pass
        elif step.getType() == GROUPED_NICE_LOOP:
            pass
        elif step.getType() == GROUPED_CONTINUOUS_NICE_LOOP:
            pass
        elif step.getType() == GROUPED_DISCONTINUOUS_NICE_LOOP:
            pass
        elif step.getType() == GROUPED_AIC:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        elif step.getType() == FORCING_CHAIN:
            pass
        elif step.getType() == FORCING_CHAIN_CONTRADICTION:
            pass
        elif step.getType() == FORCING_CHAIN_VERITY:
            pass
        elif step.getType() == FORCING_NET:
            pass
        elif step.getType() == FORCING_NET_CONTRADICTION:
            pass
        elif step.getType() == FORCING_NET_VERITY:
            if step.getValues().size() > 0:
                i = 0
                while i < step.getValues().size():
                    value = step.getValues().get(i)
                    index = step.getIndices().get(i)
                    sudoku.setCell(index, value)
                    i += 1
            else:
                for cand in step.getCandidatesToDelete():
                    sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    @synchronized
    def getAllNiceLoops(self):
        """ generated source for method getAllNiceLoops """
        self.initialize()
        sudoku = finder.getSudoku()
        ticks = System.currentTimeMillis()
        self.steps = ArrayList()
        self.withGroupNodes = False
        self.withAlsNodes = False
        doGetNiceLoops()
        Collections.sort(self.steps)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("getAllNiceLoops() gesamt: " + ticks + "ms")
        return self.steps

    @synchronized
    def getAllGroupedNiceLoops(self):
        """ generated source for method getAllGroupedNiceLoops """
        self.initialize()
        sudoku = finder.getSudoku()
        ticks = System.currentTimeMillis()
        self.steps = ArrayList()
        self.withGroupNodes = True
        self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
        self.onlyGroupedNiceLoops = True
        doGetNiceLoops()
        self.onlyGroupedNiceLoops = False
        Collections.sort(self.steps)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("getAllGroupedNiceLoops() gesamt: " + ticks + "ms")
        return self.steps

    @synchronized
    def getAllForcingChains(self):
        """ generated source for method getAllForcingChains """
        self.initialize()
        sudoku = finder.getSudoku()
        oldSteps = self.steps
        self.steps = ArrayList()
        millis1 = System.currentTimeMillis()
        self.withGroupNodes = True
        self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
        getForcingChains()
        Collections.sort(self.steps, self.tablingComparator)
        millis1 = System.currentTimeMillis() - millis1
        if self.DEBUG:
            print("getAllForcingChains() gesamt: " + millis1 + "ms")
        result = self.steps
        self.steps = oldSteps
        return result

    @synchronized
    def getAllForcingNets(self):
        """ generated source for method getAllForcingNets """
        self.initialize()
        sudoku = finder.getSudoku()
        oldSteps = self.steps
        self.steps = ArrayList()
        millis1 = System.currentTimeMillis()
        self.withGroupNodes = True
        self.withAlsNodes = Options.getInstance().isAllowAlsInTablingChains()
        getForcingNets()
        Collections.sort(self.steps, self.tablingComparator)
        millis1 = System.currentTimeMillis() - millis1
        if self.DEBUG:
            print("getAllForcingNets() gesamt: " + millis1 + "ms")
        result = self.steps
        self.steps = oldSteps
        return result

    def initForKrakenSearch(self):
        """ generated source for method initForKrakenSearch """
        self.initialize()
        sudoku = finder.getSudoku()
        self.deletesMap.clear()
        ticks = System.currentTimeMillis()
        self.chainsOnly = True
        fillTables()
        fillTablesWithGroupNodes()
        if Options.getInstance().isAllowAlsInTablingChains():
            fillTablesWithAls()
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("fillTables(): " + ticks + "ms")
        printTableAnz()
        ticks = System.currentTimeMillis()
        expandTables(self.onTable)
        expandTables(self.offTable)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("expandTables(): " + ticks + "ms")
        printTableAnz()

    def checkKrakenTypeOne(self, fins, index, candidate):
        """ generated source for method checkKrakenTypeOne """
        i = 0
        while i < len(fins):
            tableIndex = fins.get(i) * 10 + candidate
            if not self.onTable[tableIndex].offSets[candidate].contains(index):
                return False
            i += 1
        return True

    def checkKrakenTypeTwo(self, indices, result, startCandidate, endCandidate):
        """ generated source for method checkKrakenTypeTwo """
        result.set(finder.getCandidates()[endCandidate])
        result.andNot(indices)
        i = 0
        while i < len(indices):
            tableIndex = indices.get(i) * 10 + startCandidate
            result.and_(self.onTable[tableIndex].offSets[endCandidate])
            i += 1
        return not result.isEmpty()

    def getKrakenChain(self, startIndex, startCandidate, endIndex, endCandidate):
        """ generated source for method getKrakenChain """
        self.globalStep.reset()
        self.resetTmpChains()
        addChain(self.onTable[startIndex * 10 + startCandidate], endIndex, endCandidate, False)
        return self.globalStep.getChains().get(0)

    @synchronized
    def getNiceLoops(self):
        """ generated source for method getNiceLoops """
        self.initialize()
        self.steps = ArrayList()
        doGetNiceLoops()
        if len(self.steps) > 0:
            Collections.sort(self.steps)
            return self.steps.get(0)
        return None

    @synchronized
    def getForcingChains(self):
        """ generated source for method getForcingChains """
        self.initialize()
        self.chainsOnly = True
        doGetForcingChains()

    @synchronized
    def getForcingNets(self):
        """ generated source for method getForcingNets """
        self.initialize()
        self.chainsOnly = False
        doGetForcingChains()

    def doGetNiceLoops(self):
        """ generated source for method doGetNiceLoops """
        self.deletesMap.clear()
        ticks = System.currentTimeMillis()
        self.chainsOnly = True
        fillTables()
        if self.withGroupNodes:
            fillTablesWithGroupNodes()
        if self.withAlsNodes:
            fillTablesWithAls()
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("fillTables(): " + ticks + "ms")
        printTableAnz()
        ticks = System.currentTimeMillis()
        expandTables(self.onTable)
        expandTables(self.offTable)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("expandTables(): " + ticks + "ms")
        printTableAnz()
        ticks = System.currentTimeMillis()
        checkNiceLoops(self.onTable)
        checkNiceLoops(self.offTable)
        checkAics(self.offTable)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("checkNiceLoops(): " + ticks + "ms")

    def doGetForcingChains(self):
        """ generated source for method doGetForcingChains """
        self.deletesMap.clear()
        ticks = System.currentTimeMillis()
        fillTables()
        if self.withGroupNodes:
            fillTablesWithGroupNodes()
        if self.withAlsNodes:
            fillTablesWithAls()
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("fillTables(): " + ticks + "ms")
        printTableAnz()
        ticks = System.currentTimeMillis()
        expandTables(self.onTable)
        expandTables(self.offTable)
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("expandTables(): " + ticks + "ms")
        printTableAnz()
        ticks = System.currentTimeMillis()
        checkForcingChains()
        ticks = System.currentTimeMillis() - ticks
        if self.DEBUG:
            print("checkChains(): " + ticks + "ms")

    def checkForcingChains(self):
        """ generated source for method checkForcingChains """
        i = 0
        while len(onTable):
            checkOneChain(self.onTable[i])
            checkOneChain(self.offTable[i])
            i += 1
        i = 0
        while len(onTable):
            checkTwoChains(self.onTable[i], self.offTable[i])
            i += 1
        checkAllChainsForHouse(None)
        checkAllChainsForHouse(Sudoku2.LINE_TEMPLATES)
        checkAllChainsForHouse(Sudoku2.COL_TEMPLATES)
        checkAllChainsForHouse(Sudoku2.BLOCK_TEMPLATES)

    def checkAllChainsForHouse(self, houseSets):
        """ generated source for method checkAllChainsForHouse """
        if houseSets == None:
            i = 0
            while i < Sudoku2.LENGTH:
                if sudoku.getValue(i) != 0:
                    i += 1
                    continue 
                self.entryList.clear()
                cands = sudoku.getAllCandidates(i)
                j = 0
                while len(cands):
                    self.entryList.add(self.onTable[i * 10 + cands[j]])
                    j += 1
                checkEntryList(self.entryList)
                i += 1
        else:
            i = 0
            while len(houseSets):
                j = 1
                while len(length):
                    self.tmpSet.set(houseSets[i])
                    self.tmpSet.and_(finder.getCandidates()[j])
                    if not self.tmpSet.isEmpty():
                        self.entryList.clear()
                        k = 0
                        while k < len(self.tmpSet):
                            self.entryList.add(self.onTable[self.tmpSet.get(k) * 10 + j])
                            k += 1
                        checkEntryList(self.entryList)
                    j += 1
                i += 1

    def checkEntryList(self, entryList):
        """ generated source for method checkEntryList """
        i = 0
        while i < len(entryList):
            entry = entryList.get(i)
            j = 1
            while len(tmpOnSets):
                if i == 0:
                    self.tmpOnSets[j].set(entry.onSets[j])
                    self.tmpOffSets[j].set(entry.offSets[j])
                else:
                    self.tmpOnSets[j].and_(entry.onSets[j])
                    self.tmpOffSets[j].and_(entry.offSets[j])
                j += 1
            i += 1
        j = 1
        while len(tmpOnSets):
            if not self.tmpOnSets[j].isEmpty():
                k = 0
                while k < self.tmpOnSets[j].size():
                    if self.DEBUG and k > 0:
                        print("More than one chein/net found 1")
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_VERITY)
                    self.globalStep.addIndex(self.tmpOnSets[j].get(k))
                    self.globalStep.addValue(j)
                    self.resetTmpChains()
                    l = 0
                    while l < len(entryList):
                        addChain(entryList.get(l), self.tmpOnSets[j].get(k), j, True)
                        l += 1
                    replaceOrCopyStep()
                    k += 1
            if not self.tmpOffSets[j].isEmpty():
                k = 0
                while k < self.tmpOffSets[j].size():
                    if self.DEBUG and k > 0:
                        print("More than one chein/net found 2")
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_VERITY)
                    self.globalStep.addCandidateToDelete(self.tmpOffSets[j].get(k), j)
                    self.resetTmpChains()
                    l = 0
                    while l < len(entryList):
                        addChain(entryList.get(l), self.tmpOffSets[j].get(k), j, False)
                        l += 1
                    replaceOrCopyStep()
                    k += 1
            j += 1

    def adjustType(self, step):
        """ generated source for method adjustType """
        if step.isNet():
            if step.getType() == SolutionType.FORCING_CHAIN_CONTRADICTION:
                step.setType(SolutionType.FORCING_NET_CONTRADICTION)
            if step.getType() == SolutionType.FORCING_CHAIN_VERITY:
                step.setType(SolutionType.FORCING_NET_VERITY)

    def adjustChains(self, step):
        """ generated source for method adjustChains """
        alsIndex = step.getAlses().size()
        self.chainAlses.clear()
        i = 0
        while i < step.getChainAnz():
            adjChain = step.getChains().get(i)
            j = adjChain.getStart()
            while j <= adjChain.getEnd():
                if Chain.getSNodeType(adjChain.getChain()[j]) == Chain.ALS_NODE:
                    which = Chain.getSAlsIndex(adjChain.getChain()[j])
                    if self.chainAlses.containsKey(which):
                        newIndex = self.chainAlses.get(which)
                        adjChain.replaceAlsIndex(j, newIndex)
                    else:
                        step.addAls(self.alses.get(which).indices, self.alses.get(which).candidates)
                        self.chainAlses.put(which, alsIndex)
                        adjChain.replaceAlsIndex(j, alsIndex)
                        alsIndex += 1
                j += 1
            i += 1

    def replaceStep(self, src, dest):
        """ generated source for method replaceStep """
        self.adjustType(src)
        dest.setType(src.getType())
        if src.getIndices().size() > 0:
            i = 0
            while i < src.getIndices().size():
                dest.getIndices().set(i, src.getIndices().get(i))
                dest.getValues().set(i, src.getValues().get(i))
                i += 1
        else:
            i = 0
            while i < src.getCandidatesToDelete().size():
                dest.getCandidatesToDelete().set(i, src.getCandidatesToDelete().get(i))
                i += 1
        if src.getAlses().size() > 0:
            dest.getAlses().clear()
            i = 0
            while i < src.getAlses().size():
                dest.addAls(src.getAlses().get(i))
                i += 1
        dest.getEndoFins().clear()
        i = 0
        while i < src.getEndoFins().size():
            dest.getEndoFins().add(src.getEndoFins().get(i))
            i += 1
        dest.setEntity(src.getEntity())
        dest.setEntityNumber(src.getEntityNumber())
        i = 0
        while i < src.getChains().size():
            localTmpChain = src.getChains().get(i)
            toShort = dest.getChains().size() > i and len(length)
            if i >= dest.getChains().size() or toShort:
                tmp = [None] * localTmpChain.getEnd() + 1
                j = 0
                while j <= localTmpChain.getEnd():
                    tmp[j] = localTmpChain.getChain()[j]
                    j += 1
                if toShort:
                    destChain = dest.getChains().get(i)
                    destChain.setChain(tmp)
                    destChain.setStart(localTmpChain.getStart())
                    destChain.setEnd(localTmpChain.getEnd())
                    destChain.resetLength()
                else:
                    dest.addChain(0, localTmpChain.getEnd(), tmp)
            else:
                destChain = dest.getChains().get(i)
                j = 0
                while j <= localTmpChain.getEnd():
                    destChain.getChain()[j] = localTmpChain.getChain()[j]
                    j += 1
                destChain.setStart(localTmpChain.getStart())
                destChain.setEnd(localTmpChain.getEnd())
                destChain.resetLength()
            i += 1
        while i < dest.getChains().size():
            dest.getChains().remove(i)

    def replaceOrCopyStep(self):
        """ generated source for method replaceOrCopyStep """
        self.adjustType(self.globalStep)
        if not self.chainsOnly and (self.globalStep.getType() == SolutionType.FORCING_CHAIN_CONTRADICTION or self.globalStep.getType() == SolutionType.FORCING_CHAIN_VERITY):
            return
        self.adjustChains(self.globalStep)
        del_ = None
        if Options.getInstance().isOnlyOneChainPerStep():
            if self.globalStep.getCandidatesToDelete().size() > 0:
                del_ = self.globalStep.getCandidateString()
            else:
                del_ = self.globalStep.getSingleCandidateString()
            oldIndex = self.deletesMap.get(del_)
            actStep = None
            if oldIndex != None:
                actStep = self.steps.get(oldIndex.intValue())
            if actStep != None:
                if actStep.getChainLength() > self.globalStep.getChainLength():
                    self.replaceStep(self.globalStep, actStep)
                return
        oldChains = self.globalStep.getChains()
        chainAnz = len(oldChains)
        oldChains.clear()
        i = 0
        while i < chainAnz:
            oldChains.add(self.tmpChains[i].clone())
            i += 1
        self.steps.add(self.globalStep.clone())
        if del_ != None:
            self.deletesMap.put(del_, len(self.steps) - 1)

    def printEntryList(self, entryList):
        """ generated source for method printEntryList """
        tmp = StringBuilder()
        i = 0
        while i < len(entryList):
            if i != 0:
                tmp.append(", ")
            tmp.append(printTableEntry(entryList.get(i).entries[0]))
            i += 1
        return tmp.__str__()

    def checkTwoChains(self, on, off):
        """ generated source for method checkTwoChains """
        if on.index == 0 or off.index == 0:
            return
        i = 1
        while len(length):
            self.tmpSet.set(on.onSets[i])
            self.tmpSet.and_(off.onSets[i])
            self.tmpSet.remove(on.getCellIndex(0))
            if not self.tmpSet.isEmpty():
                j = 0
                while j < len(self.tmpSet):
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_VERITY)
                    self.globalStep.addIndex(self.tmpSet.get(j))
                    self.globalStep.addValue(i)
                    self.resetTmpChains()
                    addChain(on, self.tmpSet.get(j), i, True)
                    addChain(off, self.tmpSet.get(j), i, True)
                    self.replaceOrCopyStep()
                    j += 1
            i += 1
        i = 1
        while len(length):
            self.tmpSet.set(on.offSets[i])
            self.tmpSet.and_(off.offSets[i])
            self.tmpSet.remove(on.getCellIndex(0))
            if not self.tmpSet.isEmpty():
                j = 0
                while j < len(self.tmpSet):
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_VERITY)
                    self.globalStep.addCandidateToDelete(self.tmpSet.get(j), i)
                    self.resetTmpChains()
                    addChain(on, self.tmpSet.get(j), i, False)
                    addChain(off, self.tmpSet.get(j), i, False)
                    self.replaceOrCopyStep()
                    j += 1
            i += 1

    def checkOneChain(self, entry):
        """ generated source for method checkOneChain """
        if entry.index == 0:
            return
        if (entry.isStrong(0) and entry.offSets[entry.getCandidate(0)].contains(entry.getCellIndex(0))) or (not entry.isStrong(0) and entry.onSets[entry.getCandidate(0)].contains(entry.getCellIndex(0))):
            self.globalStep.reset()
            self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
            if entry.isStrong(0):
                self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
            else:
                self.globalStep.addIndex(entry.getCellIndex(0))
                self.globalStep.addValue(entry.getCandidate(0))
            self.globalStep.setEntity(Sudoku2.CELL)
            self.globalStep.setEntityNumber(self.tmpSet.get(0))
            self.resetTmpChains()
            addChain(entry, entry.getCellIndex(0), entry.getCandidate(0), not entry.isStrong(0))
            self.replaceOrCopyStep()
        i = 0
        while len(length):
            self.tmpSet.set(entry.onSets[i])
            self.tmpSet.and_(entry.offSets[i])
            if not self.tmpSet.isEmpty():
                self.globalStep.reset()
                self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
                if entry.isStrong(0):
                    self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
                else:
                    self.globalStep.addIndex(entry.getCellIndex(0))
                    self.globalStep.addValue(entry.getCandidate(0))
                self.globalStep.setEntity(Sudoku2.CELL)
                self.globalStep.setEntityNumber(self.tmpSet.get(0))
                self.resetTmpChains()
                addChain(entry, self.tmpSet.get(0), i, False)
                addChain(entry, self.tmpSet.get(0), i, True)
                self.replaceOrCopyStep()
            i += 1
        i = 1
        while len(length):
            j = i + 1
            while len(length):
                self.tmpSet.set(entry.onSets[i])
                self.tmpSet.and_(entry.onSets[j])
                if not self.tmpSet.isEmpty():
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
                    if entry.isStrong(0):
                        self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
                    else:
                        self.globalStep.addIndex(entry.getCellIndex(0))
                        self.globalStep.addValue(entry.getCandidate(0))
                    self.globalStep.setEntity(Sudoku2.CELL)
                    self.globalStep.setEntityNumber(self.tmpSet.get(0))
                    self.resetTmpChains()
                    addChain(entry, self.tmpSet.get(0), i, True)
                    addChain(entry, self.tmpSet.get(0), j, True)
                    self.replaceOrCopyStep()
                j += 1
            i += 1
        checkHouseSet(entry, Sudoku2.LINE_TEMPLATES, Sudoku2.LINE)
        checkHouseSet(entry, Sudoku2.COL_TEMPLATES, Sudoku2.COL)
        checkHouseSet(entry, Sudoku2.BLOCK_TEMPLATES, Sudoku2.BLOCK)
        self.tmpSet.setAll()
        i = 1
        while len(length):
            self.tmpSet1.set(entry.offSets[i])
            self.tmpSet1.orNot(finder.getCandidates()[i])
            self.tmpSet.and_(self.tmpSet1)
            i += 1
        i = 0
        while len(length):
            self.tmpSet.andNot(entry.onSets[i])
            i += 1
        self.tmpSet2.clear()
        i = 1
        while len(length):
            self.tmpSet2.or_(finder.getPositions()[i])
            i += 1
        self.tmpSet.andNot(self.tmpSet2)
        if not self.tmpSet.isEmpty():
            i = 0
            while i < len(self.tmpSet):
                self.globalStep.reset()
                self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
                if entry.isStrong(0):
                    self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
                else:
                    self.globalStep.addIndex(entry.getCellIndex(0))
                    self.globalStep.addValue(entry.getCandidate(0))
                self.globalStep.setEntity(Sudoku2.CELL)
                self.globalStep.setEntityNumber(self.tmpSet.get(i))
                self.resetTmpChains()
                cands = sudoku.getAllCandidates(self.tmpSet.get(i))
                j = 0
                while len(cands):
                    addChain(entry, self.tmpSet.get(i), cands[j], False)
                    j += 1
                if entry.isStrong(0):
                    self.replaceOrCopyStep()
                else:
                    self.replaceOrCopyStep()
                i += 1
        checkHouseDel(entry, Sudoku2.LINE_TEMPLATES, Sudoku2.LINE)
        checkHouseDel(entry, Sudoku2.COL_TEMPLATES, Sudoku2.COL)
        checkHouseDel(entry, Sudoku2.BLOCK_TEMPLATES, Sudoku2.BLOCK)

    def checkHouseDel(self, entry, houseSets, entityTyp):
        """ generated source for method checkHouseDel """
        i = 1
        while len(length):
            j = 0
            while len(houseSets):
                self.tmpSet.set(houseSets[j])
                self.tmpSet.and_(finder.getCandidatesAllowed()[i])
                if not self.tmpSet.isEmpty() and self.tmpSet.andEquals(entry.offSets[i]):
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
                    if entry.isStrong(0):
                        self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
                    else:
                        self.globalStep.addIndex(entry.getCellIndex(0))
                        self.globalStep.addValue(entry.getCandidate(0))
                    self.globalStep.setEntity(entityTyp)
                    self.globalStep.setEntityNumber(j)
                    self.resetTmpChains()
                    k = 0
                    while k < len(self.tmpSet):
                        addChain(entry, self.tmpSet.get(k), i, False)
                        k += 1
                    if entry.isStrong(0):
                        self.replaceOrCopyStep()
                    else:
                        self.replaceOrCopyStep()
                j += 1
            i += 1

    def checkHouseSet(self, entry, houseSets, entityTyp):
        """ generated source for method checkHouseSet """
        i = 1
        while len(length):
            j = 0
            while len(houseSets):
                self.tmpSet.setAnd(houseSets[j], entry.onSets[i])
                if len(self.tmpSet) > 1:
                    self.globalStep.reset()
                    self.globalStep.setType(SolutionType.FORCING_CHAIN_CONTRADICTION)
                    if entry.isStrong(0):
                        self.globalStep.addCandidateToDelete(entry.getCellIndex(0), entry.getCandidate(0))
                    else:
                        self.globalStep.addIndex(entry.getCellIndex(0))
                        self.globalStep.addValue(entry.getCandidate(0))
                    self.globalStep.setEntity(entityTyp)
                    self.globalStep.setEntityNumber(j)
                    self.resetTmpChains()
                    k = 0
                    while k < len(self.tmpSet):
                        addChain(entry, self.tmpSet.get(k), i, True)
                        k += 1
                    if entry.isStrong(0):
                        self.replaceOrCopyStep()
                    else:
                        self.replaceOrCopyStep()
                j += 1
            i += 1

    def checkNiceLoops(self, tables):
        """ generated source for method checkNiceLoops """
        i = 0
        while len(tables):
            startIndex = tables[i].getCellIndex(0)
            j = 1
            while j < tables[i].index:
                if tables[i].getNodeType(j) == Chain.NORMAL_NODE and tables[i].getCellIndex(j) == startIndex:
                    checkNiceLoop(tables[i], j)
                j += 1
            i += 1

    def checkAics(self, tables):
        """ generated source for method checkAics """
        i = 0
        while len(tables):
            startIndex = tables[i].getCellIndex(0)
            startCandidate = tables[i].getCandidate(0)
            buddies = Sudoku2.buddies[startIndex]
            j = 1
            while j < tables[i].index:
                if tables[i].getNodeType(j) != Chain.NORMAL_NODE or not tables[i].isStrong(j) or tables[i].getCellIndex(j) == startIndex:
                    j += 1
                    continue 
                if startCandidate == tables[i].getCandidate(j):
                    self.tmpSet.set(buddies)
                    self.tmpSet.and_(Sudoku2.buddies[tables[i].getCellIndex(j)])
                    self.tmpSet.and_(finder.getCandidates()[startCandidate])
                    if not self.tmpSet.isEmpty() and len(self.tmpSet) >= 2:
                        checkAic(tables[i], j)
                else:
                    if not buddies.contains(tables[i].getCellIndex(j)):
                        j += 1
                        continue 
                    if sudoku.isCandidate(tables[i].getCellIndex(j), startCandidate) and sudoku.isCandidate(startIndex, tables[i].getCandidate(j)):
                        checkAic(tables[i], j)
                j += 1
            i += 1

    def checkNiceLoop(self, entry, entryIndex):
        """ generated source for method checkNiceLoop """
        if entry.getDistance(entryIndex) <= 2:
            return
        self.globalStep.reset()
        self.globalStep.setType(SolutionType.DISCONTINUOUS_NICE_LOOP)
        self.resetTmpChains()
        addChain(entry, entry.getCellIndex(entryIndex), entry.getCandidate(entryIndex), entry.isStrong(entryIndex), True)
        if self.globalStep.getChains().isEmpty():
            return
        localTmpChain = self.globalStep.getChains().get(0)
        if localTmpChain.getCellIndex(0) == localTmpChain.getCellIndex(1):
            return
        nlChain = localTmpChain.getChain()
        nlChainIndex = localTmpChain.getEnd()
        nlChainLength = localTmpChain.getLength()
        firstLinkStrong = entry.isStrong(1)
        lastLinkStrong = entry.isStrong(entryIndex)
        startCandidate = entry.getCandidate(0)
        endCandidate = entry.getCandidate(entryIndex)
        startIndex = entry.getCellIndex(0)
        if not firstLinkStrong and not lastLinkStrong and startCandidate == endCandidate:
            self.globalStep.addCandidateToDelete(startIndex, startCandidate)
        elif firstLinkStrong and lastLinkStrong and startCandidate == endCandidate:
            cands = sudoku.getAllCandidates(startIndex)
            i = 0
            while len(cands):
                if cands[i] != startCandidate:
                    self.globalStep.addCandidateToDelete(startIndex, cands[i])
                i += 1
        elif firstLinkStrong != lastLinkStrong and startCandidate != endCandidate:
            if not firstLinkStrong:
                self.globalStep.addCandidateToDelete(startIndex, startCandidate)
            else:
                self.globalStep.addCandidateToDelete(startIndex, endCandidate)
        elif (not firstLinkStrong and not lastLinkStrong and sudoku.getAnzCandidates(startIndex) == 2 and startCandidate != endCandidate) or (firstLinkStrong and lastLinkStrong and startCandidate != endCandidate) or (firstLinkStrong != lastLinkStrong and startCandidate == endCandidate):
            self.globalStep.setType(SolutionType.CONTINUOUS_NICE_LOOP)
            i = 0
            while i <= nlChainIndex:
                if (i == 0 and (firstLinkStrong and lastLinkStrong)) or (i > 0 and (Chain.isSStrong(nlChain[i]) and i <= nlChainIndex - 2 and Chain.getSCellIndex(nlChain[i - 1]) != Chain.getSCellIndex(nlChain[i]))):
                    if i == 0 or (not Chain.isSStrong(nlChain[i + 1]) and Chain.getSCellIndex(nlChain[i]) == Chain.getSCellIndex(nlChain[i + 1]) and Chain.isSStrong(nlChain[i + 2]) and Chain.getSCellIndex(nlChain[i + 1]) != Chain.getSCellIndex(nlChain[i + 2])):
                        c1 = Chain.getSCandidate(nlChain[i])
                        c2 = Chain.getSCandidate(nlChain[i + 2])
                        if i == 0:
                            c1 = startCandidate
                            c2 = endCandidate
                        cands = sudoku.getAllCandidates(Chain.getSCellIndex(nlChain[i]))
                        j = 0
                        while len(cands):
                            if cands[j] != c1 and cands[j] != c2:
                                self.globalStep.addCandidateToDelete(Chain.getSCellIndex(nlChain[i]), cands[j])
                            j += 1
                if (i > 0) and (not Chain.isSStrong(nlChain[i]) and Chain.getSCellIndex(nlChain[i - 1]) != Chain.getSCellIndex(nlChain[i])):
                    actCand = Chain.getSCandidate(nlChain[i])
                    Chain.getSNodeBuddies(nlChain[i - 1], actCand, self.alses, self.tmpSet)
                    Chain.getSNodeBuddies(nlChain[i], actCand, self.alses, self.tmpSet1)
                    self.tmpSet.and_(self.tmpSet1)
                    self.tmpSet.andNot(self.tmpSetC)
                    self.tmpSet.remove(startIndex)
                    self.tmpSet.and_(finder.getCandidates()[actCand])
                    if not self.tmpSet.isEmpty():
                        j = 0
                        while j < len(self.tmpSet):
                            self.globalStep.addCandidateToDelete(self.tmpSet.get(j), actCand)
                            j += 1
                    if Chain.getSNodeType(nlChain[i]) == Chain.ALS_NODE:
                        isForceExit = i < nlChainIndex and Chain.isSStrong(nlChain[i + 1])
                        nextCellIndex = Chain.getSCellIndex(nlChain[i + 1])
                        self.tmpSet2.clear()
                        if isForceExit:
                            forceCand = Chain.getSCandidate(nlChain[i + 1])
                            sudoku.getCandidateSet(nextCellIndex, self.tmpSet2)
                            self.tmpSet2.remove(forceCand)
                        else:
                            if i < nlChainIndex:
                                self.tmpSet2.add(Chain.getSCandidate(nlChain[i + 1]))
                        als = self.alses.get(Chain.getSAlsIndex(nlChain[i]))
                        j = 1
                        while len(length):
                            if j == actCand or self.tmpSet2.contains(j) or als.buddiesPerCandidat[j] == None:
                                j += 1
                                continue 
                            self.tmpSet.set(als.buddiesPerCandidat[j])
                            self.tmpSet.and_(finder.getCandidates()[j])
                            if not self.tmpSet.isEmpty():
                                k = 0
                                while k < len(self.tmpSet):
                                    self.globalStep.addCandidateToDelete(self.tmpSet.get(k), j)
                                    k += 1
                            j += 1
                        if isForceExit:
                            self.tmpSet1.set(Sudoku2.buddies[nextCellIndex])
                            j = 0
                            while j < len(self.tmpSet2):
                                actExitCand = self.tmpSet2.get(j)
                                self.tmpSet.set(als.buddiesPerCandidat[actExitCand])
                                self.tmpSet.and_(self.tmpSet1)
                                self.tmpSet.and_(finder.getCandidates()[actExitCand])
                                if not self.tmpSet.isEmpty():
                                    k = 0
                                    while k < len(self.tmpSet):
                                        self.globalStep.addCandidateToDelete(self.tmpSet.get(k), actExitCand)
                                        k += 1
                                j += 1
                i += 1
        if self.globalStep.getCandidatesToDelete().size() > 0:
            grouped = False
            newChain = self.globalStep.getChains().get(0)
            i = newChain.getStart()
            while i <= newChain.getEnd():
                if Chain.getSNodeType(newChain.getChain()[i]) != Chain.NORMAL_NODE:
                    grouped = True
                    break
                i += 1
            if grouped:
                if self.globalStep.getType() == SolutionType.DISCONTINUOUS_NICE_LOOP:
                    self.globalStep.setType(SolutionType.GROUPED_DISCONTINUOUS_NICE_LOOP)
                if self.globalStep.getType() == SolutionType.CONTINUOUS_NICE_LOOP:
                    self.globalStep.setType(SolutionType.GROUPED_CONTINUOUS_NICE_LOOP)
                if self.globalStep.getType() == SolutionType.AIC:
                    self.globalStep.setType(SolutionType.GROUPED_AIC)
            if self.onlyGroupedNiceLoops and not grouped:
                return
            del_ = self.globalStep.getCandidateString()
            oldIndex = self.deletesMap.get(del_)
            if oldIndex != None and self.steps.get(oldIndex.intValue()).getChainLength() <= nlChainLength:
                return
            self.deletesMap.put(del_, len(self.steps))
            newChain = self.globalStep.getChains().get(0).clone()
            self.globalStep.getChains().clear()
            self.globalStep.getChains().add(newChain)
            self.adjustChains(self.globalStep)
            self.steps.add(self.globalStep.clone())

    def checkAic(self, entry, entryIndex):
        """ generated source for method checkAic """
        if entry.getDistance(entryIndex) <= 2:
            return
        self.globalStep.reset()
        self.globalStep.setType(SolutionType.AIC)
        startCandidate = entry.getCandidate(0)
        endCandidate = entry.getCandidate(entryIndex)
        startIndex = entry.getCellIndex(0)
        endIndex = entry.getCellIndex(entryIndex)
        if startCandidate == endCandidate:
            self.tmpSet.set(Sudoku2.buddies[startIndex])
            self.tmpSet.and_(Sudoku2.buddies[endIndex])
            self.tmpSet.and_(finder.getCandidates()[startCandidate])
            if len(self.tmpSet) > 1:
                i = 0
                while i < len(self.tmpSet):
                    if self.tmpSet.get(i) != startIndex:
                        self.globalStep.addCandidateToDelete(self.tmpSet.get(i), startCandidate)
                    i += 1
        else:
            if sudoku.isCandidate(startIndex, endCandidate):
                self.globalStep.addCandidateToDelete(startIndex, endCandidate)
            if sudoku.isCandidate(endIndex, startCandidate):
                self.globalStep.addCandidateToDelete(endIndex, startCandidate)
        if self.globalStep.getAnzCandidatesToDelete() == 0:
            return
        self.resetTmpChains()
        addChain(entry, entry.getCellIndex(entryIndex), entry.getCandidate(entryIndex), entry.isStrong(entryIndex), False, True)
        if self.globalStep.getChains().isEmpty():
            return
        grouped = False
        newChain = self.globalStep.getChains().get(0)
        i = newChain.getStart()
        while i <= newChain.getEnd():
            if Chain.getSNodeType(newChain.getChain()[i]) != Chain.NORMAL_NODE:
                grouped = True
                break
            i += 1
        if grouped:
            if self.globalStep.getType() == SolutionType.DISCONTINUOUS_NICE_LOOP:
                self.globalStep.setType(SolutionType.GROUPED_DISCONTINUOUS_NICE_LOOP)
            if self.globalStep.getType() == SolutionType.CONTINUOUS_NICE_LOOP:
                self.globalStep.setType(SolutionType.GROUPED_CONTINUOUS_NICE_LOOP)
            if self.globalStep.getType() == SolutionType.AIC:
                self.globalStep.setType(SolutionType.GROUPED_AIC)
        if self.onlyGroupedNiceLoops and not grouped:
            return
        del_ = self.globalStep.getCandidateString()
        oldIndex = self.deletesMap.get(del_)
        if oldIndex != None and self.steps.get(oldIndex.intValue()).getChainLength() <= self.globalStep.getChains().get(0).getLength():
            return
        self.deletesMap.put(del_, len(self.steps))
        newChain = self.globalStep.getChains().get(0).clone()
        self.globalStep.getChains().clear()
        self.globalStep.getChains().add(newChain)
        self.adjustChains(self.globalStep)
        self.steps.add(self.globalStep.clone())

    def fillTables(self):
        """ generated source for method fillTables """
        i = 0
        while len(onTable):
            self.onTable[i].reset()
            self.offTable[i].reset()
            i += 1
        self.extendedTableMap.clear()
        self.extendedTableIndex = 0
        if self.chainsOnly:
            i = 0
            while len(length):
                if sudoku.getValue(i) != 0:
                    i += 1
                    continue 
                j = 1
                while j <= 9:
                    if not sudoku.isCandidate(i, j):
                        j += 1
                        continue 
                    cand = j
                    self.onTable[i * 10 + cand].addEntry(i, cand, True)
                    self.offTable[i * 10 + cand].addEntry(i, cand, False)
                    cands = sudoku.getAllCandidates(i)
                    k = 0
                    while len(cands):
                        otherCand = cands[k]
                        if otherCand == cand:
                            k += 1
                            continue 
                        self.onTable[i * 10 + cand].addEntry(i, otherCand, False)
                        if len(cands):
                            self.offTable[i * 10 + cand].addEntry(i, otherCand, True)
                        k += 1
                    self.tmpSet1.set(finder.getCandidates()[cand])
                    self.tmpSet1.remove(i)
                    constrIndex = 0
                    while len(length):
                        constr = Sudoku2.CONSTRAINTS[i][constrIndex]
                        anzCands = sudoku.getFree()[constr][cand]
                        if anzCands < 2:
                            constrIndex += 1
                            continue 
                        self.tmpSet.set(self.tmpSet1)
                        self.tmpSet.and_(Sudoku2.ALL_CONSTRAINTS_TEMPLATES[constr])
                        if self.tmpSet.isEmpty():
                            constrIndex += 1
                            continue 
                        k = 0
                        while k < len(self.tmpSet):
                            self.onTable[i * 10 + cand].addEntry(self.tmpSet.get(k), cand, False)
                            k += 1
                        if anzCands == 2:
                            self.offTable[i * 10 + cand].addEntry(self.tmpSet.get(0), cand, True)
                        constrIndex += 1
                    j += 1
                i += 1
        else:
            self.savedSudoku = sudoku.clone()
            self.simpleFinder.setSudoku(self.savedSudoku)
            i = 0
            while len(length):
                if self.savedSudoku.getValue(i) != 0:
                    i += 1
                    continue 
                cands = self.savedSudoku.getAllCandidates(i)
                j = 0
                while len(cands):
                    cand = cands[j]
                    sudoku.set(self.savedSudoku)
                    self.simpleFinder.setSudoku(sudoku)
                    getTableEntry(self.onTable[i * 10 + cand], i, cand, True)
                    sudoku.set(self.savedSudoku)
                    self.simpleFinder.setSudoku(sudoku)
                    getTableEntry(self.offTable[i * 10 + cand], i, cand, False)
                    j += 1
                i += 1
            sudoku.set(self.savedSudoku)

    def fillTablesWithGroupNodes(self):
        """ generated source for method fillTablesWithGroupNodes """
        self.groupNodes = GroupNode.getGroupNodes(finder)
        i = 0
        while i < len(self.groupNodes):
            gn = self.groupNodes.get(i)
            onEntry = getNextExtendedTableEntry(self.extendedTableIndex)
            onEntry.addEntry(gn.index1, gn.index2, gn.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
            self.extendedTableMap.put(onEntry.entries[0], self.extendedTableIndex)
            self.extendedTableIndex += 1
            offEntry = getNextExtendedTableEntry(self.extendedTableIndex)
            offEntry.addEntry(gn.index1, gn.index2, gn.index3, Chain.GROUP_NODE, gn.cand, False, 0, 0, 0, 0, 0, 0)
            self.extendedTableMap.put(offEntry.entries[0], self.extendedTableIndex)
            self.extendedTableIndex += 1
            self.tmpSet.set(finder.getCandidates()[gn.cand])
            self.tmpSet.and_(gn.buddies)
            if not self.tmpSet.isEmpty():
                j = 0
                while j < len(self.tmpSet):
                    index = self.tmpSet.get(j)
                    onEntry.addEntry(index, gn.cand, False)
                    tmp = self.onTable[index * 10 + gn.cand]
                    tmp.addEntry(gn.index1, gn.index2, gn.index3, Chain.GROUP_NODE, gn.cand, False, 0, 0, 0, 0, 0, 0)
                    j += 1
                self.tmpSet1.set(self.tmpSet)
                self.tmpSet1.and_(Sudoku2.BLOCK_TEMPLATES[gn.block])
                if not self.tmpSet1.isEmpty() and len(self.tmpSet1) == 1:
                    offEntry.addEntry(self.tmpSet1.get(0), gn.cand, True)
                    tmp = self.offTable[self.tmpSet1.get(0) * 10 + gn.cand]
                    tmp.addEntry(gn.index1, gn.index2, gn.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
                self.tmpSet1.set(self.tmpSet)
                if gn.line != -1:
                    self.tmpSet1.and_(Sudoku2.LINE_TEMPLATES[gn.line])
                else:
                    self.tmpSet1.and_(Sudoku2.COL_TEMPLATES[gn.col])
                if not self.tmpSet1.isEmpty() and len(self.tmpSet1) == 1:
                    offEntry.addEntry(self.tmpSet1.get(0), gn.cand, True)
                    tmp = self.offTable[self.tmpSet1.get(0) * 10 + gn.cand]
                    tmp.addEntry(gn.index1, gn.index2, gn.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
            lineAnz = 0
            line1Index = -1
            colAnz = 0
            col1Index = -1
            blockAnz = 0
            block1Index = -1
            gn2 = None
            j = 0
            while j < len(self.groupNodes):
                gn2 = self.groupNodes.get(j)
                if j == i:
                    j += 1
                    continue 
                if gn.cand != gn2.cand:
                    j += 1
                    continue 
                self.tmpSet2.set(gn.indices)
                if not self.tmpSet2.andEmpty(gn2.indices):
                    j += 1
                    continue 
                if gn.line != -1 and gn.line == gn2.line:
                    lineAnz += 1
                    if lineAnz == 1:
                        line1Index = j
                    onEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, False, 0, 0, 0, 0, 0, 0)
                if gn.col != -1 and gn.col == gn2.col:
                    colAnz += 1
                    if colAnz == 1:
                        col1Index = j
                    onEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, False, 0, 0, 0, 0, 0, 0)
                if gn.block == gn2.block:
                    blockAnz += 1
                    if blockAnz == 1:
                        block1Index = j
                    onEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, False, 0, 0, 0, 0, 0, 0)
                j += 1
            if lineAnz == 1:
                gn2 = self.groupNodes.get(line1Index)
                self.tmpSet.set(Sudoku2.LINE_TEMPLATES[gn.line])
                self.tmpSet.and_(finder.getCandidates()[gn.cand])
                self.tmpSet.andNot(gn.indices)
                self.tmpSet.andNot(gn2.indices)
                if self.tmpSet.isEmpty():
                    offEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
            if colAnz == 1:
                gn2 = self.groupNodes.get(col1Index)
                self.tmpSet.set(Sudoku2.COL_TEMPLATES[gn.col])
                self.tmpSet.and_(finder.getCandidates()[gn.cand])
                self.tmpSet.andNot(gn.indices)
                self.tmpSet.andNot(gn2.indices)
                if self.tmpSet.isEmpty():
                    offEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
            if blockAnz == 1:
                gn2 = self.groupNodes.get(block1Index)
                self.tmpSet.set(Sudoku2.BLOCK_TEMPLATES[gn.block])
                self.tmpSet.and_(finder.getCandidates()[gn.cand])
                self.tmpSet.andNot(gn.indices)
                self.tmpSet.andNot(gn2.indices)
                if self.tmpSet.isEmpty():
                    offEntry.addEntry(gn2.index1, gn2.index2, gn2.index3, Chain.GROUP_NODE, gn.cand, True, 0, 0, 0, 0, 0, 0)
            i += 1

    def fillTablesWithAls(self):
        """ generated source for method fillTablesWithAls """
        self.alses = finder.getAlses(True)
        i = 0
        while i < len(self.alses):
            als = self.alses.get(i)
            if len(als.indices) == 1:
                i += 1
                continue 
            j = 1
            while j <= 9:
                if als.indicesPerCandidat[j] == None or als.indicesPerCandidat[j].isEmpty():
                    j += 1
                    continue 
                eliminationsPresent = False
                k = 1
                while k <= 9:
                    self.alsEliminations[k].clear()
                    if k == j:
                        k += 1
                        continue 
                    if als.indicesPerCandidat[k] != None:
                        self.alsEliminations[k].set(finder.getCandidates()[k])
                        self.alsEliminations[k].and_(als.buddiesPerCandidat[k])
                        if not self.alsEliminations[k].isEmpty():
                            eliminationsPresent = True
                    k += 1
                if not eliminationsPresent:
                    j += 1
                    continue 
                entryIndex = als.indicesPerCandidat[j].get(0)
                offEntry = None
                if (offEntry = getAlsTableEntry(entryIndex, i, j)) == None:
                    offEntry = getNextExtendedTableEntry(self.extendedTableIndex)
                    offEntry.addEntry(entryIndex, i, Chain.ALS_NODE, j, False, 0)
                    self.extendedTableMap.put(offEntry.entries[0], self.extendedTableIndex)
                    self.extendedTableIndex += 1
                self.tmpSet.set(finder.getCandidates()[j])
                self.tmpSet.and_(als.buddiesPerCandidat[j])
                alsEntry = Chain.makeSEntry(entryIndex, i, j, False, Chain.ALS_NODE)
                k = 0
                while k < len(self.tmpSet):
                    actIndex = self.tmpSet.get(k)
                    tmp = self.onTable[actIndex * 10 + j]
                    tmp.addEntry(entryIndex, i, Chain.ALS_NODE, j, False, 0)
                    l = 0
                    while l < len(self.groupNodes):
                        gAct = self.groupNodes.get(l)
                        if gAct.cand == j and gAct.indices.contains(actIndex):
                            self.tmpSet1.set(als.indices)
                            if not self.tmpSet1.andEmpty(gAct.indices):
                                l += 1
                                continue 
                            self.tmpSet1.set(als.indicesPerCandidat[j])
                            if not self.tmpSet1.andEquals(gAct.buddies):
                                l += 1
                                continue 
                            entry = Chain.makeSEntry(gAct.index1, gAct.index2, gAct.index3, j, True, Chain.GROUP_NODE)
                            gTmp = self.extendedTable.get(self.extendedTableMap.get(entry))
                            if gTmp.indices.containsKey(alsEntry):
                                l += 1
                                continue 
                            gTmp.addEntry(entryIndex, i, Chain.ALS_NODE, j, False, 0)
                        l += 1
                    k += 1
                k = 1
                while k <= 9:
                    if self.alsEliminations[k].isEmpty():
                        k += 1
                        continue 
                    l = 0
                    while l < self.alsEliminations[k].size():
                        offEntry.addEntry(self.alsEliminations[k].get(l), k, als.getChainPenalty(), False)
                        l += 1
                    l = 0
                    while l < len(self.groupNodes):
                        gAct = self.groupNodes.get(l)
                        if gAct.cand != k:
                            l += 1
                            continue 
                        self.tmpSet1.set(gAct.indices)
                        if not self.tmpSet1.andEquals(self.alsEliminations[k]):
                            l += 1
                            continue 
                        offEntry.addEntry(gAct.index1, gAct.index2, gAct.index3, Chain.GROUP_NODE, k, False, 0, 0, 0, 0, 0, als.getChainPenalty())
                        l += 1
                    k += 1
                k = 0
                while k < len(self.alses):
                    if k == i:
                        k += 1
                        continue 
                    tmpAls = self.alses.get(k)
                    self.tmpSet1.set(als.indices)
                    if not self.tmpSet1.andEmpty(tmpAls.indices):
                        k += 1
                        continue 
                    l = 1
                    while l <= 9:
                        if self.alsEliminations[l] == None or self.alsEliminations[l].isEmpty() or tmpAls.indicesPerCandidat[l] == None or tmpAls.indicesPerCandidat[l].isEmpty():
                            l += 1
                            continue 
                        self.tmpSet1.set(self.alsEliminations[l])
                        if not self.tmpSet1.contains(tmpAls.indicesPerCandidat[l]):
                            l += 1
                            continue 
                        tmpAlsIndex = tmpAls.indicesPerCandidat[l].get(0)
                        if getAlsTableEntry(tmpAlsIndex, k, l) == None:
                            tmpAlsEntry = getNextExtendedTableEntry(self.extendedTableIndex)
                            tmpAlsEntry.addEntry(tmpAlsIndex, k, Chain.ALS_NODE, l, False, 0)
                            self.extendedTableMap.put(tmpAlsEntry.entries[0], self.extendedTableIndex)
                            self.extendedTableIndex += 1
                        offEntry.addEntry(tmpAlsIndex, k, Chain.ALS_NODE, l, False, als.getChainPenalty())
                        l += 1
                    k += 1
                k = 0
                while k < len(als.buddies):
                    cellIndex = als.buddies.get(k)
                    if sudoku.getValue(cellIndex) != 0 or sudoku.getAnzCandidates(cellIndex) == 2:
                        k += 1
                        continue 
                    sudoku.getCandidateSet(cellIndex, self.tmpSet1)
                    l = 1
                    while l <= 9:
                        if self.alsEliminations[l] != None and self.alsEliminations[l].contains(cellIndex):
                            self.tmpSet1.remove(l)
                        l += 1
                    if len(self.tmpSet1) == 1:
                        offEntry.addEntry(cellIndex, self.tmpSet1.get(0), als.getChainPenalty() + 1, True)
                    k += 1
                j += 1
            i += 1

    def getAlsTableEntry(self, entryCellIndex, alsIndex, cand):
        """ generated source for method getAlsTableEntry """
        entry = Chain.makeSEntry(entryCellIndex, alsIndex, cand, False, Chain.ALS_NODE)
        if self.extendedTableMap.containsKey(entry):
            return self.extendedTable.get(self.extendedTableMap.get(entry))
        return None

    def getNextExtendedTableEntry(self, tableIndex):
        """ generated source for method getNextExtendedTableEntry """
        entry = None
        if tableIndex >= len(self.extendedTable):
            entry = TableEntry()
            self.extendedTable.add(entry)
        else:
            entry = self.extendedTable.get(tableIndex)
            entry.reset()
        return entry

    def getTableEntry(self, entry, cellIndex, cand, set):
        """ generated source for method getTableEntry """
        if set:
            setCell(cellIndex, cand, entry, False, False)
        else:
            sudoku.delCandidate(cellIndex, cand)
            entry.addEntry(cellIndex, cand, False, 0)
            if sudoku.getAnzCandidates(cellIndex) == 1:
                setCand = sudoku.getAllCandidates(cellIndex)[0]
                setCell(cellIndex, setCand, entry, False, True)
        j = 0
        while j < Options.getInstance().getAnzTableLookAhead():
            self.singleSteps.clear()
            dummyList = self.simpleFinder.findAllNakedSingles(sudoku)
            self.singleSteps.addAll(dummyList)
            dummyList = self.simpleFinder.findAllHiddenSingles(sudoku)
            self.singleSteps.addAll(dummyList)
            i = 0
            while i < len(self.singleSteps):
                step = self.singleSteps.get(i)
                index = step.getIndices().get(0)
                setCell(index, step.getValues().get(0), entry, True, step.getType() == SolutionType.NAKED_SINGLE)
                i += 1
            j += 1

    def setCell(self, cellIndex, cand, entry, getRetIndices, nakedSingle):
        """ generated source for method setCell """
        self.tmpSet.set(finder.getCandidates()[cand])
        self.tmpSet.remove(cellIndex)
        self.tmpSet.and_(Sudoku2.buddies[cellIndex])
        cands = sudoku.getAllCandidates(cellIndex)
        entityType = Sudoku2.LINE
        entityNumberFree = sudoku.getFree()[Sudoku2.CONSTRAINTS[cellIndex][0]][cand]
        dummy = sudoku.getFree()[Sudoku2.CONSTRAINTS[cellIndex][1]][cand]
        if dummy < entityNumberFree:
            entityType = Sudoku2.COL
            entityNumberFree = dummy
        dummy = sudoku.getFree()[Sudoku2.CONSTRAINTS[cellIndex][2]][cand]
        if dummy < entityNumberFree:
            entityType = Sudoku2.BLOCK
            entityNumberFree = dummy
        sudoku.setCell(cellIndex, cand)
        retIndex = entry.index
        if getRetIndices:
        __ri_0 = ri
        ri += 1
            i = 0
            while len(length):
                self.retIndices[0][i] = 0
                i += 1
            if nakedSingle:
                cellCands = self.savedSudoku.getAllCandidates(cellIndex)
                if len(cellCands):
                    Logger.getLogger(getClass().__name__).log(Level.WARNING, "Too many candidates (setCell() - Naked Single")
                ri = 0
                i = 0
                while ri < self.retIndices[0].length and len(cellCands):
                    if cellCands[i] == cand:
                        i += 1
                        continue 
                    self.retIndices[0][__ri_0] = entry.getEntryIndex(cellIndex, False, cellCands[i])
                    i += 1
            else:
                if entityType == Sudoku2.LINE:
                    getRetIndicesForHouse(cellIndex, cand, Sudoku2.LINE_TEMPLATES[Sudoku2.getLine(cellIndex)], entry)
                elif entityType == Sudoku2.COL:
                    getRetIndicesForHouse(cellIndex, cand, Sudoku2.COL_TEMPLATES[Sudoku2.getCol(cellIndex)], entry)
                else:
                    getRetIndicesForHouse(cellIndex, cand, Sudoku2.BLOCK_TEMPLATES[Sudoku2.getBlock(cellIndex)], entry)
            entry.addEntry(cellIndex, cand, True, self.retIndices[0][0], self.retIndices[0][1], self.retIndices[0][2], self.retIndices[0][3], self.retIndices[0][4])
        else:
            entry.addEntry(cellIndex, cand, True)
        i = 0
        while i < len(self.tmpSet):
            entry.addEntry(self.tmpSet.get(i), cand, False, retIndex)
            i += 1
        i = 0
        while len(cands):
            if cands[i] != cand:
                entry.addEntry(cellIndex, cands[i], False, retIndex)
            i += 1

    def getRetIndicesForHouse(self, cellIndex, cand, houseSet, entry):
        """ generated source for method getRetIndicesForHouse """
        self.tmpSet1.set(finder.getCandidates()[cand])
        self.tmpSet1.remove(cellIndex)
        self.tmpSet1.and_(houseSet)
        if len(self.tmpSet1) > len(length):
            Logger.getLogger(getClass().__name__).log(Level.WARNING, "Too many candidates (setCell() - Hidden Single")
        ri = 0
        i = 0
        while i < len(self.tmpSet1) and len(length):
        __ri_1 = ri
        ri += 1
            self.retIndices[0][__ri_1] = entry.getEntryIndex(self.tmpSet1.get(i), False, cand)
            i += 1

    def expandTables(self, table):
        """ generated source for method expandTables """
        i = 0
        while len(table):
            if table[i].index == 0:
                i += 1
                continue 
            dest = table[i]
            isFromOnTable = False
            isFromExtendedTable = False
            j = 1
            while len(length):
                if dest.entries[j] == 0:
                    break
                if dest.isFull():
                    Logger.getLogger(getClass().__name__).log(Level.WARNING, "TableEntry full!")
                    break
                src = None
                srcTableIndex = dest.getCellIndex(j) * 10 + dest.getCandidate(j)
                isFromExtendedTable = False
                isFromOnTable = False
                if Chain.getSNodeType(dest.entries[j]) != Chain.NORMAL_NODE:
                    tmpSI = self.extendedTableMap.get(dest.entries[j])
                    if tmpSI == None:
                        Logger.getLogger(getClass().__name__).log(Level.WARNING, "Table for {0} not found!", printTableEntry(dest.entries[j]))
                        j += 1
                        continue 
                    srcTableIndex = tmpSI.intValue()
                    src = self.extendedTable.get(srcTableIndex)
                    isFromExtendedTable = True
                else:
                    if dest.isStrong(j):
                        src = self.onTable[srcTableIndex]
                    else:
                        src = self.offTable[srcTableIndex]
                    isFromOnTable = dest.isStrong(j)
                if src.index == 0:
                    tmpBuffer = StringBuilder()
                    tmpBuffer.append("TableEntry for ").append(dest.entries[j]).append(" not found!\r\n")
                    tmpBuffer.append("i == ").append(i).append(", j == ").append(j).append(", dest.entries[j] == ").append(dest.entries[j]).append(": ")
                    tmpBuffer.append(printTableEntry(dest.entries[j]))
                    Logger.getLogger(getClass().__name__).log(Level.WARNING, tmpBuffer.__str__())
                    j += 1
                    continue 
                srcBaseDistance = dest.getDistance(j)
                k = 1
                while k < src.index:
                    if src.isExpanded(k):
                        k += 1
                        continue 
                    srcDistance = src.getDistance(k)
                    if dest.indices.containsKey(src.entries[k]):
                        orgIndex = dest.getEntryIndex(src.entries[k])
                        if dest.isExpanded(orgIndex) and (dest.getDistance(orgIndex) > (srcBaseDistance + srcDistance) or dest.getDistance(orgIndex) == (srcBaseDistance + srcDistance) and dest.getNodeType(orgIndex) > src.getNodeType(k)):
                            dest.retIndices[orgIndex] = TableEntry.makeSRetIndex(srcTableIndex, 0, 0, 0, 0)
                            dest.setExpanded(orgIndex)
                            if isFromExtendedTable:
                                dest.setExtendedTable(orgIndex)
                            elif isFromOnTable:
                                dest.setOnTable(orgIndex)
                            dest.setDistance(orgIndex, srcBaseDistance + srcDistance)
                    else:
                        srcCellIndex = src.getCellIndex(k)
                        srcCand = src.getCandidate(k)
                        srcStrong = src.isStrong(k)
                        if Chain.getSNodeType(src.entries[k]) == Chain.NORMAL_NODE:
                            dest.addEntry(srcCellIndex, srcCand, srcStrong, srcTableIndex)
                        else:
                            tmp = src.entries[k]
                            dest.addEntry(Chain.getSCellIndex(tmp), Chain.getSCellIndex2(tmp), Chain.getSCellIndex3(tmp), Chain.getSNodeType(tmp), srcCand, srcStrong, srcTableIndex, 0, 0, 0, 0, 0)
                        dest.setExpanded(dest.index - 1)
                        if isFromExtendedTable:
                            dest.setExtendedTable(dest.index - 1)
                        elif isFromOnTable:
                            dest.setOnTable(dest.index - 1)
                        dest.setDistance(dest.index - 1, srcBaseDistance + srcDistance)
                    k += 1
                j += 1
            i += 1

    @overloaded
    def addChain(self, entry, cellIndex, cand, set):
        """ generated source for method addChain """
        self.addChain(entry, cellIndex, cand, set, False)

    @addChain.register(object, TableEntry, int, int, bool, bool)
    def addChain_0(self, entry, cellIndex, cand, set, isNiceLoop):
        """ generated source for method addChain_0 """
        self.addChain(entry, cellIndex, cand, set, isNiceLoop, False)

    @addChain.register(object, TableEntry, int, int, bool, bool, bool)
    def addChain_1(self, entry, cellIndex, cand, set, isNiceLoop, isAic):
        """ generated source for method addChain_1 """
        buildChain(entry, cellIndex, cand, set)
        j = 0
        if isNiceLoop or isAic:
            self.lassoSet.clear()
            if isNiceLoop and Chain.getSCellIndex(self.chain[0]) == Chain.getSCellIndex(self.chain[1]):
                return
        lastCellIndex = -1
        lastCellEntry = -1
        firstCellIndex = Chain.getSCellIndex(self.chain[self.chainIndex - 1])
        i = self.chainIndex - 1
        while i >= 0:
        __j_2 = j
        j += 1
        __j_3 = j
        j += 1
        __j_4 = j
        j += 1
            oldEntry = self.chain[i]
            newCellIndex = Chain.getSCellIndex(oldEntry)
            if isNiceLoop or isAic:
                if self.lassoSet.contains(newCellIndex):
                    return
                if lastCellIndex != -1 and (lastCellIndex != firstCellIndex or isAic):
                    self.lassoSet.add(lastCellIndex)
                    if Chain.getSNodeType(lastCellEntry) == Chain.GROUP_NODE:
                        tmp = Chain.getSCellIndex2(lastCellEntry)
                        if tmp != -1:
                            self.lassoSet.add(tmp)
                        tmp = Chain.getSCellIndex3(lastCellEntry)
                        if tmp != -1:
                            self.lassoSet.add(tmp)
                    elif Chain.getSNodeType(lastCellEntry) == Chain.ALS_NODE:
                        self.lassoSet.or_(self.alses.get(Chain.getSAlsIndex(lastCellEntry)).indices)
            lastCellIndex = newCellIndex
            lastCellEntry = oldEntry
            self.tmpChain[__j_2] = oldEntry
            k = 0
            while k < self.actMin:
                if self.mins[k][self.minIndexes[k] - 1] == oldEntry:
                    l = self.minIndexes[k] - 2
                    while l >= 0:
                        self.tmpChain[__j_3] = -self.mins[k][l]
                        l -= 1
                    self.tmpChain[__j_4] = Integer.MIN_VALUE
                k += 1
            i -= 1
        if j > 0:
            System.arraycopy(self.tmpChain, 0, self.tmpChains[self.tmpChainsIndex].getChain(), 0, j)
            self.tmpChains[self.tmpChainsIndex].setStart(0)
            self.tmpChains[self.tmpChainsIndex].setEnd(j - 1)
            self.tmpChains[self.tmpChainsIndex].resetLength()
            self.globalStep.addChain(self.tmpChains[self.tmpChainsIndex])
            self.tmpChainsIndex += 1

    @overloaded
    def buildChain(self, entry, cellIndex, cand, set):
        """ generated source for method buildChain """
        self.chainIndex = 0
        chainEntry = Chain.makeSEntry(cellIndex, cand, set)
        index = -1
        i = 0
        while len(length):
            if entry.entries[i] == chainEntry:
                index = i
                break
            i += 1
        if index == -1:
            Logger.getLogger(getClass().__name__).log(Level.WARNING, "No chain entry for {0}/{1}/{2}/{3}", [None] * )
            return
        self.actMin = 0
        i = 0
        while len(minIndexes):
            self.minIndexes[i] = 0
            i += 1
        self.tmpSetC.clear()
        self.chainIndex = self.buildChain(entry, index, self.chain, False, self.tmpSetC)
        minIndex = 0
        while minIndex < self.actMin:
            self.minIndexes[minIndex] = self.buildChain(entry, entry.getEntryIndex(self.mins[minIndex][0]), self.mins[minIndex], True, self.tmpSetC)
            minIndex += 1

    @buildChain.register(object, TableEntry, int, int, bool, SudokuSet)
    def buildChain_0(self, entry, entryIndex, actChain, isMin, chainSet):
        """ generated source for method buildChain_0 """
        actChainIndex = 0
        __actChainIndex_5 = actChainIndex
        actChainIndex += 1
        actChain[__actChainIndex_5] = entry.entries[entryIndex]
        firstEntryIndex = entryIndex
        expanded = False
        orgEntry = entry
        __actChainIndex_6 = actChainIndex
        actChainIndex += 1
        __actMin_7 = actMin
        actMin += 1
        while firstEntryIndex != 0 and len(actChain):
            if entry.isExpanded(firstEntryIndex):
                if entry.isExtendedTable(firstEntryIndex):
                    entry = self.extendedTable.get(orgEntry.getRetIndex(firstEntryIndex, 0))
                elif entry.isOnTable(firstEntryIndex):
                    entry = self.onTable[orgEntry.getRetIndex(firstEntryIndex, 0)]
                else:
                    entry = self.offTable[orgEntry.getRetIndex(firstEntryIndex, 0)]
                expanded = True
                firstEntryIndex = entry.getEntryIndex(orgEntry.entries[firstEntryIndex])
            tmpEntryIndex = firstEntryIndex
            i = 0
            while i < 5:
                entryIndex = entry.getRetIndex(tmpEntryIndex, i)
                if i == 0:
                    firstEntryIndex = entryIndex
                    actChain[__actChainIndex_6] = entry.entries[entryIndex]
                    if not isMin:
                        chainSet.add(entry.getCellIndex(entryIndex))
                        if Chain.getSNodeType(entry.entries[entryIndex]) == Chain.GROUP_NODE:
                            tmp = Chain.getSCellIndex2(entry.entries[entryIndex])
                            if tmp != -1:
                                chainSet.add(tmp)
                            tmp = Chain.getSCellIndex3(entry.entries[entryIndex])
                            if tmp != -1:
                                chainSet.add(tmp)
                        elif Chain.getSNodeType(entry.entries[entryIndex]) == Chain.ALS_NODE:
                            if Chain.getSAlsIndex(entry.entries[entryIndex]) == -1:
                                Logger.getLogger(getClass().__name__).log(Level.WARNING, "INVALID ALS_NODE: {0}", Chain.toString(entry.entries[entryIndex]))
                            chainSet.or_(self.alses.get(Chain.getSAlsIndex(entry.entries[entryIndex])).indices)
                    else:
                        if chainSet.contains(entry.getCellIndex(entryIndex)):
                            j = 0
                            while j < self.chainIndex:
                                if self.chain[j] == entry.entries[entryIndex]:
                                    return actChainIndex
                                j += 1
                else:
                    if entryIndex != 0 and not isMin:
                        self.mins[self.actMin][0] = entry.entries[entryIndex]
                        self.minIndexes[__actMin_7] = 1
                i += 1
            if expanded and firstEntryIndex == 0:
                retEntry = entry.entries[0]
                entry = orgEntry
                firstEntryIndex = entry.getEntryIndex(retEntry)
                expanded = False
        return actChainIndex

    def printTable(self, title, entry):
        """ generated source for method printTable """
        print(title + ": ")
        anz = 0
        tmp = StringBuilder()
        i = 0
        while i < entry.index:
            if not entry.isStrong(i):
            tmp.append(printTableEntry(entry.entries[i]))
            j = 0
            while j < entry.getRetIndexAnz(i):
                retIndex = entry.getRetIndex(i, j)
                tmp.append(" (")
                if entry.isExpanded(i):
                    tmp.append("EX:").append(retIndex).append(":").append(entry.isExtendedTable(i)).append("/").append(entry.isOnTable(i)).append("/")
                else:
                    tmp.append(retIndex).append("/").append(printTableEntry(entry.entries[retIndex])).append(")")
                j += 1
            tmp.append(" ")
            anz += 1
            if (anz % 5) == 0:
                tmp.append("\r\n")
            i += 1
        print(tmp.__str__())

    def printTableEntry(self, entry):
        """ generated source for method printTableEntry """
        index = Chain.getSCellIndex(entry)
        candidate = Chain.getSCandidate(entry)
        set = Chain.isSStrong(entry)
        cell = SolutionStep.getCellPrint(index, False)
        if Chain.getSNodeType(entry) == Chain.GROUP_NODE:
            cell = SolutionStep.getCompactCellPrint(index, Chain.getSCellIndex2(entry), Chain.getSCellIndex3(entry))
        elif Chain.getSNodeType(entry) == Chain.ALS_NODE:
            cell = "ALS:" + SolutionStep.getAls(self.alses.get(Chain.getSAlsIndex(entry)))
        if set:
            return cell + "=" + candidate
        else:
            return cell + "<>" + candidate

    def printTableAnz(self):
        """ generated source for method printTableAnz """
        if not self.DEBUG:
            return
        onAnz = 0
        offAnz = 0
        entryAnz = 0
        maxEntryAnz = 0
        i = 0
        while len(onTable):
            if self.onTable[i] != None:
                onAnz += 1
                entryAnz += self.onTable[i].index
                if self.onTable[i].index > maxEntryAnz:
                    maxEntryAnz = self.onTable[i].index
            if self.offTable[i] != None:
                offAnz += 1
                entryAnz += self.offTable[i].index
                if self.offTable[i].index > maxEntryAnz:
                    maxEntryAnz = self.offTable[i].index
            i += 1
        print("Tables: " + onAnz + " onTableEntries, " + offAnz + " offTableEntries, " + entryAnz + " Implikationen (" + maxEntryAnz + " max)")

    class TablingComparator(Comparator, SolutionStep):
        """ generated source for class TablingComparator """
        def compare(self, o1, o2):
            """ generated source for method compare """
            sum1 = 0
            sum2 = 0
            if o1.getIndices().size() > 0 and o2.getIndices().isEmpty():
                return -1
            if o1.getIndices().isEmpty() and o2.getIndices().size() > 0:
                return +1
            if o1.getIndices().size() > 0:
                result = o2.getIndices().size() - o1.getIndices().size()
                if result != 0:
                    return result
                if not o1.isEquivalent(o2):
                    sum1 = o1.getSumme(o1.getIndices())
                    sum2 = o1.getSumme(o2.getIndices())
                    return 1 if sum1 == sum2 else sum1 - sum2
                result = o1.getChainLength() - o2.getChainLength()
                if result != 0:
                    return result
            else:
                result = o2.getCandidatesToDelete().size() - o1.getCandidatesToDelete().size()
                if result != 0:
                    return result
                if not o1.isEquivalent(o2):
                    result = o1.compareCandidatesToDelete(o2)
                    if result != 0:
                        return result
                result = o1.getChainLength() - o2.getChainLength()
                if result != 0:
                    return result
            return 0

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        finder = SudokuStepFinder()
        TablingSolver.DEBUG = True
        sudoku = Sudoku2()
        sudoku.setSudoku(":0000:x:9...6..2............1.893.......65..41.8...96..24.......352.1..1.........8..1...5:316 716 221 521 621 721 325 725 326 726 741 344 744 944 345 348 748 848 349 749 849 361 861 362 365 366 384 784 985 394 794::")
        sudoku.setSudoku(":0709:1234679:5.81...6.....9.4...39.8..7..6...5.....27.95....58...2..8..5134..51.3.....9...8651:221 224 231 743 445 349 666 793:122 128 131 141 147 151 161 167 219 229 341 348 441 451 461 624 761 769 919 947 967 987::11")
        sudoku.setSudoku(":0711-4:59:...65+4+328+2458.31.+6+63+8....+459+7+31+4+5+86+2+42+1+38+6..+9+8+56..74+13.84.....7.......+8..6...+8.3.:175 275 975 185 285 785 985:578 974::7")
        sudoku.setSudoku(":0000:x:.......123......6+4+1...4..+8+59+1...+45+2......1+67..2....+1+4....35+64+9+1..14..8.+6.6....+2.+7:::")
        finder.setSudoku(sudoku)
        steps = None
        ticks = System.currentTimeMillis()
        anzLoops = 1
        i = 0
        while i < anzLoops:
            steps = finder.getAllForcingChains(sudoku)
            i += 1
        ticks = System.currentTimeMillis() - ticks
        print("Dauer: " + (ticks / anzLoops) + "ms")
        print("Anzahl Steps: " + len(steps))
        i = 0
        while i < len(steps):
            print(steps.get(i).toString(2))
            i += 1

