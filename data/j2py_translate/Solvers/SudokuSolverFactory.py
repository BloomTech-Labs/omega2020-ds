#!/usr/bin/env python
""" generated source for module SudokuSolverFactory """
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
#  * HoDoKu uses one instance of class {@link SudokuSolver} from within the
#  * GUI. This instance is called the <b>defaultSolver</b>. For use in background
#  * threads an arbitrary number of additional solver instances can be gotten
#  * from this factory.<br>
#  * Solvers have to be released after they are used.
#  * 
#  * @author hobiwan
#  
class SudokuSolverFactory(object):
    """ generated source for class SudokuSolverFactory """
    #  The <b>defaultSolver</b> for use by the GUI. 
    defaultSolver = SudokuSolver()

    #  All SudokuSolver instances created by this factory. 
    instances = ArrayList()

    #  A background thread that cleans up unused SudokuSolver instances. 
    thread = Thread(Runnable())

    @SuppressWarnings("SleepWhileInLoop")
    def run(self):
        """ generated source for method run """
        while True:
            with lock_for_object(self.thread):
                self.defaultSolver.getStepFinder().cleanUp()
                iterator = self.instances.iterator()
                while iterator.hasNext():
                    act = iterator.next()
                    if act.inUse == False and (System.currentTimeMillis() - act.lastUsedAt) > SOLVER_TIMEOUT:
                        iterator.remove()
                    else:
                        act.instance_.getStepFinder().cleanUp()
            try:
                Thread.sleep(SOLVER_TIMEOUT)
            except InterruptedException as ex:
                pass

    #  The default cleanup time for SudokuSolver instances. 
    SOLVER_TIMEOUT = 5 * 60 * 1000

    # 
    #      * One entry in {@link #instances}.
    #      
    class SolverInstance(object):
        """ generated source for class SolverInstance """
        #  The solver held in this entry. 
        instance_ = None

        #  <code>true</code>, if the solver has been handed out by the factory. 
        inUse = True

        #  Last time the solver was returned to the factory. 
        lastUsedAt = -1

        # 
        #          * Create a new entry for {@link #instances}.
        #          * @param instance
        #          
        def __init__(self, instance_):
            """ generated source for method __init__ """
            self.instance_ = instance_

    #  Start the thread 
    # 
    #      * This class is a utility class that cannot be instantiated.
    #      
    def __init__(self):
        """ generated source for method __init__ """
        #  class cannot be instantiated! 

    #  Get the {@link #defaultSolver}.
    #      * @return 
    #      
    @classmethod
    def getDefaultSolverInstance(cls):
        """ generated source for method getDefaultSolverInstance """
        return cls.defaultSolver

    # 
    #      * Hand out an ununsed solver or create a new one if necessary.
    #      * @return
    #      
    @classmethod
    def getInstance(cls):
        """ generated source for method getInstance """
        ret = None
        with lock_for_object(cls.thread):
            for act in instances:
                if act.inUse == False:
                    act.inUse = True
                    ret = act.instance_
                    break
            if ret == None:
                ret = SudokuSolver()
                cls.instances.add(cls.SolverInstance(ret))
        return ret

    # 
    #      * Gives a solver back to the factory.
    #      * @param solver
    #      
    @classmethod
    def giveBack(cls, solver):
        """ generated source for method giveBack """
        with lock_for_object(cls.thread):
            for act in instances:
                if act.instance_ == solver:
                    act.inUse = False
                    act.lastUsedAt = System.currentTimeMillis()
                    break

