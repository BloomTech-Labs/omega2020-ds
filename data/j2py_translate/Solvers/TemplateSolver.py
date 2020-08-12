#!/usr/bin/env python
""" generated source for module TemplateSolver_no_german """
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
#  * Verboten sind alle Templates, die keine 1 an einer der bereits gesetzten Positionen haben:
#  *    (positions & template) != positions
#  * Verboten sind alle Templates, die eine 1 an einer nicht mehr erlaubten Position haben:
#  *    (~(positions | allowedPositions) & template) != 0
#  * Verboten sind alle Templates, die eine 1 an einer Position eines Templates haben, das aus
#  *    allen verundeten Templates eines anderen Kandidaten gebildet wurde
#  * Verboten sind alle Templates, die keine einzige uberlappungsfreie Kombination mit wenigstens
#  *    einem Template einer anderen Ziffer haben
#  *
#  * Wenn die Templates bekannt sind:
#  *    alle Templates OR: Alle Kandidaten, die nicht enthalten sind, konnen geloscht werden
#  *    alle Templates AND: Alle Positionen, die ubrig bleiben, konnen gesetzt werden
#  *    alle gultigen Kombinationen aus Templates zweier Ziffern bilden (OR), alle Ergebnisse
#  *           AND: An allen verbliebenen Positionen konnen alle Kandidaten, die nicht zu einer dieser
#  *           Ziffern gehoren, eliminiert werden.
#  *
#  * @author hobiwan
#  
class TemplateSolver(AbstractSolver):
    """ generated source for class TemplateSolver """
    steps = None

    #  gefundene Losungsschritte
    globalStep = SolutionStep(SolutionType.HIDDEN_SINGLE)

    #  Creates a new instance of TemplateSolver
    #      * @param finder
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(TemplateSolver, self).__init__(finder)

    def getStep(self, type_):
        """ generated source for method getStep """
        result = None
        sudoku = finder.getSudoku()
        if type_ == TEMPLATE_SET:
            getTemplateSet(True)
            if len(self.steps) > 0:
                result = self.steps.get(0)
        elif type_ == TEMPLATE_DEL:
            getTemplateDel(True)
            if len(self.steps) > 0:
                result = self.steps.get(0)
        return result

    def doStep(self, step):
        """ generated source for method doStep """
        handled = True
        sudoku = finder.getSudoku()
        if step.getType() == TEMPLATE_SET:
            value = step.getValues().get(0)
            for index in step.getIndices():
                sudoku.setCell(index, value)
        elif step.getType() == TEMPLATE_DEL:
            for cand in step.getCandidatesToDelete():
                sudoku.delCandidate(cand.getIndex(), cand.getValue())
        else:
            handled = False
        return handled

    def getAllTemplates(self):
        """ generated source for method getAllTemplates """
        sudoku = finder.getSudoku()
        oldSteps = self.steps
        self.steps = ArrayList()
        millis1 = System.currentTimeMillis()
        getTemplateSet(False)
        getTemplateDel(False)
        millis1 = System.currentTimeMillis() - millis1
        Logger.getLogger(getClass().__name__).log(Level.FINE, "getAllTemplates() gesamt: {0}ms", millis1)
        result = self.steps
        self.steps = oldSteps
        return result

    def getTemplateSet(self, initSteps):
        """ generated source for method getTemplateSet """
        if initSteps:
            self.steps = ArrayList()
        #  konnen Zellen gesetzt werden?
        setSet = SudokuSet()
        i = 1
        while i <= 9:
            setSet.set(finder.getSetValueTemplates(True)[i])
            setSet.andNot(finder.getPositions()[i])
            if not setSet.isEmpty():
                #  Zellen konnen gesetzt werden
                self.globalStep.reset()
                self.globalStep.setType(SolutionType.TEMPLATE_SET)
                self.globalStep.addValue(i)
                j = 0
                while j < len(setSet):
                    self.globalStep.addIndex(setSet.get(j))
                    j += 1
                self.steps.add(self.globalStep.clone())
            i += 1

    def getTemplateDel(self, initSteps):
        """ generated source for method getTemplateDel """
        if initSteps:
            self.steps = ArrayList()
        #  konnen Kandidaten geloscht werden?
        setSet = SudokuSet()
        i = 1
        while i <= 9:
            setSet.set(finder.getDelCandTemplates(True)[i])
            setSet.and_(finder.getCandidates()[i])
            if not setSet.isEmpty():
                #  Kandidaten konnen geloscht werden
                self.globalStep.reset()
                self.globalStep.setType(SolutionType.TEMPLATE_DEL)
                self.globalStep.addValue(i)
                j = 0
                while j < len(setSet):
                    self.globalStep.addCandidateToDelete(setSet.get(j), i)
                    j += 1
                self.steps.add(self.globalStep.clone())
            i += 1

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        # Sudoku2 sudoku = new Sudoku2(true);
        sudoku = Sudoku2()
        # sudoku.setSudoku(":0361:4:..5.132673268..14917...2835..8..1.262.1.96758.6..283...12....83693184572..723.6..:434 441 442 461 961 464 974:411:r7c39 r6c1b9 fr3c3");
        sudoku.setSudoku(":0000:x:7.2.34.8.........2.8..51.74.......51..63.27..29.......14.76..2.8.........2.51.8.7:::")
        #         for (int i = 1; i <= 9; i++) {
        #             print("allowedPositions[" + i + "]: " + sudoku.getCandidates()[i]);
        #             print("positions[" + i + "]: " + sudoku.getPositions()[i]);
        #         }
        ts = TemplateSolver(None)
        millis = System.currentTimeMillis()
        i = 0
        while i < 1:
            steps = ts.getAllTemplates()
            i += 1
        millis = System.currentTimeMillis() - millis
        print("Zeit: " + (millis / 100) + "ms")

