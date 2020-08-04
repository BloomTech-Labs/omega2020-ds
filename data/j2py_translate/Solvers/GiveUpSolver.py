#!/usr/bin/env python
""" generated source for module GiveUpSolver """
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
class GiveUpSolver(AbstractSolver):
    """ generated source for class GiveUpSolver """
    #  Creates a new instance of GiveUpSolver
    #      * @param finder 
    #      
    def __init__(self, finder):
        """ generated source for method __init__ """
        super(GiveUpSolver, self).__init__(finder)

    def getStep(self, type_):
        """ generated source for method getStep """
        if type_ == SolutionType.GIVE_UP:
            return SolutionStep(SolutionType.GIVE_UP)
        return None

    def doStep(self, step):
        """ generated source for method doStep """
        handled = False
        if step.getType() == GIVE_UP:
            handled = True
        else:
            handled = False
        return handled

