#!/usr/bin/env python
""" generated source for module GroupNode """
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
class GroupNode(object):
    """ generated source for class GroupNode """
    indices = SudokuSet()

    #  indices as bit mask
    buddies = SudokuSet()

    #  all buddies that can see all cells in the group node
    cand = int()

    #  candidate for grouped link
    line = -1

    #  row (index in Sudoku2.ROWS), -1 if not applicable
    col = -1

    #  col (index in Sudoku2.COLS), -1 if not applicable
    block = int()

    #  block (index in Sudoku2.BLOCKS)
    index1 = int()

    #  index of first cell
    index2 = int()

    #  index of second cell
    index3 = int()

    #  index of third cell or -1, if grouped node consists only of two cells
    candInHouse = SudokuSet()

    #  all positions for a given candidate in a given house
    tmpSet = SudokuSet()

    #  for check with blocks
    # 
    #      * Creates a new instance of GroupNode
    #      * @param cand
    #      * @param indices  
    #      
    def __init__(self, cand, indices):
        """ generated source for method __init__ """
        self.cand = cand
        self.indices.set(indices)
        self.index1 = indices.get(0)
        self.index2 = indices.get(1)
        self.index3 = -1
        if len(indices) > 2:
            self.index3 = indices.get(2)
        self.block = Sudoku2.getBlock(self.index1)
        if Sudoku2.getLine(self.index1) == Sudoku2.getLine(self.index2):
            self.line = Sudoku2.getLine(self.index1)
        if Sudoku2.getCol(self.index1) == Sudoku2.getCol(self.index2):
            self.col = Sudoku2.getCol(self.index1)
        #  calculate the buddies
        self.buddies.set(Sudoku2.buddies[self.index1])
        self.buddies.and_(Sudoku2.buddies[self.index2])
        if self.index3 >= 0:
            self.buddies.and_(Sudoku2.buddies[self.index3])

    def __str__(self):
        """ generated source for method toString """
        return "GroupNode: " + self.cand + " - " + SolutionStep.getCompactCellPrint(self.index1, self.index2, self.index3) + "  - " + self.index1 + "/" + self.index2 + "/" + self.index3 + " (" + self.line + "/" + self.col + "/" + self.block + ")"

    # 
    #      * Gets all group nodes from the given sudoku and puts them in an ArrayList.
    #      *
    #      * For all candidates in all lines and all cols do:
    #      *   - check if they have a candidate left
    #      *   - if so, check if an intersection of line/col and a block contains
    #      *     more than one candidate; if yes -> group node found
    #      * @param finder
    #      * @return  
    #      
    @classmethod
    def getGroupNodes(cls, finder):
        """ generated source for method getGroupNodes """
        groupNodes = ArrayList()
        getGroupNodesForHouseType(groupNodes, finder, Sudoku2.LINE_TEMPLATES)
        getGroupNodesForHouseType(groupNodes, finder, Sudoku2.COL_TEMPLATES)
        return groupNodes

    @classmethod
    def getGroupNodesForHouseType(cls, groupNodes, finder, houses):
        """ generated source for method getGroupNodesForHouseType """
        i = 0
        while len(houses):
            cand = 1
            while cls.cand <= 9:
                cls.candInHouse.set(houses[i])
                cls.candInHouse.and_(finder.getCandidates()[cls.cand])
                if cls.candInHouse.isEmpty():
                    #  no candidates left in this house -> proceed
                    cls.cand += 1
                    continue 
                #  candidates left in house -> check blocks
                j = 0
                while len(length):
                    cls.tmpSet.set(cls.candInHouse)
                    cls.tmpSet.and_(Sudoku2.BLOCK_TEMPLATES[j])
                    if cls.tmpSet.isEmpty():
                        #  no candidates in this house -> proceed with next block
                        j += 1
                        continue 
                    else:
                        #  rather complicated for performance reasons (isEmpty() is much faster than size())
                        if len(cls.tmpSet) >= 2:
                            #  group node found
                            groupNodes.add(GroupNode(cls.cand, cls.tmpSet))
                    j += 1
                cls.cand += 1
            i += 1

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        sudoku = Sudoku2()
        sudoku.setSudoku(":0000:x:.4..1..........5.6......3.15.38.2...7......2..........6..5.7....2.....1....3.14..:211 213 214 225 235 448 465 366 566 468 469::")
        ticks = System.currentTimeMillis()
        groupNodes = GroupNode.getGroupNodes(None)
        ticks = System.currentTimeMillis() - ticks
        print("getGroupNodes(): " + ticks + "ms, " + len(groupNodes) + " group nodes")
        for node in groupNodes:
            print("  " + node)


if __name__ == '__main__':
    import sys
    GroupNode.main(sys.argv)

