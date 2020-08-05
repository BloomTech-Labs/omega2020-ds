#!/usr/bin/env python
""" generated source for module RestrictedCommon """
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
#  * Describes Restriced Commons (RCs) between two ALS; since we only
#  * handle ALS and not AALS or greater a maximum of 2 RCs between
#  * any ALS pair can exist.<br>
#  * 
#  * If only one RC exists for the pair, the second is 0.<br>
#  * 
#  * The references to the ALS are stored as indices into a <code>List&lt;{@link Als}&gt;</code>,
#  * they are therefore meaningless outside the scope of the list for which they were
#  * created.
#  * 
#  * @author hobiwan
#  
class RestrictedCommon(Comparable, RestrictedCommon, Cloneable):
    """ generated source for class RestrictedCommon """
    #  Index of first ALS (index into a <code>List&lt;{@link Als}&gt;</code> stored elsewhere) 
    als1 = int()

    #  Index of the second ALS (index into a <code>List&lt;{@link Als}&gt;</code> stored elsewhere) 
    als2 = int()

    #  First RC, must be != 0. 
    cand1 = int()

    #  Second rc; if <code>cand2 == 0</code> only one rc exists between als1 and als2 
    cand2 = int()

    #  Used for propagation checks in ALS-Chains (see {@link AlsSolver#getAlsXYChain()} for details). 
    #      * 0: none, 1: cand1 only, 2: cand2 only, 3: both.
    #      
    actualRC = int()

    # 
    #      * Creates a new instance of <code>RestricteCommon</code>.
    #      
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(RestrictedCommon, self).__init__()

    # 
    #      * Creates a new instance of <code>RestricteCommon</code> for two singly linked ALS.
    #      * @param als1 
    #      * @param als2 
    #      * @param cand1
    #      
    @__init__.register(object, int, int, int)
    def __init___0(self, als1, als2, cand1):
        """ generated source for method __init___0 """
        super(RestrictedCommon, self).__init__()
        self.als1 = als1
        self.als2 = als2
        self.cand1 = cand1
        self.cand2 = 0

    # 
    #      * Creates a new instance of <code>RestricteCommon</code> for two doubly linked ALS.
    #      * @param als1 
    #      * @param cand2
    #      * @param als2
    #      * @param cand1
    #      
    @__init__.register(object, int, int, int, int)
    def __init___1(self, als1, als2, cand1, cand2):
        """ generated source for method __init___1 """
        super(RestrictedCommon, self).__init__()
        self.__init__(als1, als2, cand1)
        self.cand2 = cand2

    # 
    #      * Creates a new instance of <code>RestricteCommon</code> for two ALS
    #      * and specifies the actual RC.
    #      * @param als1 
    #      * @param als2 
    #      * @param cand2
    #      * @param cand1
    #      * @param actualRC
    #      
    @__init__.register(object, int, int, int, int, int)
    def __init___2(self, als1, als2, cand1, cand2, actualRC):
        """ generated source for method __init___2 """
        super(RestrictedCommon, self).__init__()
        self.__init__(als1, als2, cand1, cand2)
        self.actualRC = actualRC

    # 
    #      * New propagation rules for ALS-Chains: the actual RCs of parameter
    #      * <code>rc</code> are excluded from <code>this</code>,
    #      * <code>this.actualRC</code> is adjusted as necessary;
    #      * if <code>this.actualRC</code> is greater than <code>0</code> the
    #      * chain can be continued and
    #      * true is returned, else false is returned.<br><br>
    #      * 
    #      * If a chain starts with a doubly linked RC (<code>rc == null</code>, <code>cand2 != 0</code>),
    #      * one of the RCs can be chosen freely; this results in two different
    #      * tries for the chain search.
    #      * 
    #      * @param rc RC of the previous link in a chain
    #      * @param firstTry Only used, if <code>rc == null</code>: if set, <code>cand1</code> is used else <code>cand2</code>
    #      * @return true if an actual RC remains, false otherwise
    #      
    def checkRC(self, rc, firstTry):
        """ generated source for method checkRC """
        self.actualRC = 1 if self.cand2 == 0 else 3
        #  rc is not provided
        if rc == None:
            #  start of chain: pick your RC
            if self.cand2 != 0:
                self.actualRC = 1 if firstTry else 2
            return self.actualRC != 0
        if rc.actualRC == 0:
            #  already done
        elif rc.actualRC == 1:
            self.actualRC = checkRCInt(rc.cand1, 0, self.cand1, self.cand2)
        elif rc.actualRC == 2:
            self.actualRC = checkRCInt(rc.cand2, 0, self.cand1, self.cand2)
        elif rc.actualRC == 3:
            self.actualRC = checkRCInt(rc.cand1, rc.cand1, self.cand1, self.cand2)
        else:
        return self.actualRC != 0

    # 
    #      * Checks duplicates (all possible combinations); 
    #      * <code>c12</code> and <code>c22</code>
    #      * can be 0 (meaning: to be ignored).
    #      * 
    #      * @param c11 First ARC of first link
    #      * @param c12 Second ARC of first link (may be 0)
    #      * @param c21 First PRC of second link
    #      * @param c22 Second PRC of second link (may be 0)
    #      * @return
    #      
    def checkRCInt(self, c11, c12, c21, c22):
        """ generated source for method checkRCInt """
        if c12 == 0:
            #  one ARC
            if c22 == 0:
                #  one ARC one PRC
                if c11 == c21:
                    return 0
                else:
                    return 1
            else:
                #  one ARC two PRCs
                if c11 == c22:
                    return 1
                elif c11 == c21:
                    return 2
                else:
                    return 3
        else:
            #  two ARCs
            if c22 == 0:
                #  two ARCs one PRC
                if c11 == c21 or c12 == c21:
                    return 0
                else:
                    return 1
            else:
                #  two ARCs two PRCs
                if (c11 == c21 and c12 == c22) or (c11 == c22 and c12 == c21):
                    return 0
                elif c11 == c22 or c12 == c22:
                    return 1
                elif c11 == c21 or c12 == c21:
                    return 2
                else:
                    return 3

    # 
    #      * Returns a string representation of <code>this</code>.
    #      * @return
    #      
    def __str__(self):
        """ generated source for method toString """
        return "RC(" + self.als1 + "/" + self.als2 + "/" + self.cand1 + "/" + self.cand2 + "/" + self.actualRC + ")"

    # 
    #      * Compares two RCs.
    #      * @param r
    #      * @return
    #      
    def compareTo(self, r):
        """ generated source for method compareTo """
        result = self.als1 - r.als1
        if result == 0:
            result = self.als2 - r.als2
            if result == 0:
                result = self.cand1 - r.cand1
                if result == 0:
                    result = self.cand2 - r.cand2
        return result

    # 
    #      * Returns a shallow copy of <code>this</code>. Since the class holds only
    #      * base types, this is sufficient.
    #      * 
    #      * @return
    #      
    def clone(self):
        """ generated source for method clone """
        try:
            newRC = super(RestrictedCommon, self).clone()
            return newRC
        except CloneNotSupportedException as ex:
            Logger.getLogger(getClass().__name__).log(Level.SEVERE, "Error while cloning (RC)", ex)
            return None

    # 
    #      * Getter for {@link #als1}.
    #      * @return
    #      
    def getAls1(self):
        """ generated source for method getAls1 """
        return self.als1

    # 
    #      * Setter for {@link #als1}.
    #      * @param als1
    #      
    def setAls1(self, als1):
        """ generated source for method setAls1 """
        self.als1 = als1

    # 
    #      * Getter for {@link #als2}.
    #      * @return
    #      
    def getAls2(self):
        """ generated source for method getAls2 """
        return self.als2

    # 
    #      * Setter for {@link #als2}.
    #      * @param als2
    #      
    def setAls2(self, als2):
        """ generated source for method setAls2 """
        self.als2 = als2

    # 
    #      * Getter for {@link #cand1}.
    #      * @return
    #      
    def getCand1(self):
        """ generated source for method getCand1 """
        return self.cand1

    # 
    #      * Setter for {@link #cand1}.
    #      * @param cand1
    #      
    def setCand1(self, cand1):
        """ generated source for method setCand1 """
        self.cand1 = cand1

    # 
    #      * Getter for {@link #cand2}.
    #      * @return
    #      
    def getCand2(self):
        """ generated source for method getCand2 """
        return self.cand2

    # 
    #      * Setter for {@link #cand2}.
    #      * @param cand2
    #      
    def setCand2(self, cand2):
        """ generated source for method setCand2 """
        self.cand2 = cand2

    # 
    #      * Getter for {@link #actualRC}.
    #      * @return
    #      
    def getActualRC(self):
        """ generated source for method getActualRC """
        return self.actualRC

    # 
    #      * Setter for {@link #actualRC}.
    #      * @param actualRC
    #      
    def setActualRC(self, actualRC):
        """ generated source for method setActualRC """
        self.actualRC = actualRC

