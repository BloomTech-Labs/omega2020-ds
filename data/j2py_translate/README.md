This is a work in progress for translating the open source human techniques on HoDoKu from java into python3.

We are using a python2 package named java2python to attempt to translate some of them into python2, and then to python3 with hopes of implementing into our ai.py code.

***

12 Working No issues

4 Partially Worked (perhaps no issue but error raised)

4 Not Working (but similar error for 4 of them)

***

Worked with no issues:

AIs.py

GiveUpSolver.py

GroupNode.py 

IncompleteSolver.py

SudokuSolverFactory.py

TableEntry.py

BruteForceSolver.py

MiscellaneousSolver.py

SudokuStepFinder.py

TablingSolver.py

TemplateSolver.py

UniquenessSolver.py

WingSolver.py


***

Partially Worked:

ColoringSolver.py

Error:
```
# WARNING runTransform: Generated source has invalid syntax. invalid syntax (<string>, line 43)
```

RestrictedCommon.py

Error:
```
# WARNING runTransform: Generated source has invalid syntax. expected an indented block (<string>, line 135)
```

SimpleSolver.py

Error:
```
# WARNING runTransform: Generated source has invalid syntax. invalid syntax (<string>, line 39)
```

SingleDigitPatternSolver.py

Error:
```
# WARNING runTransform: Generated source has invalid syntax. invalid syntax (<string>, line 76)
```

***

Did not work:

AIsSolver.py

Error:

```
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 259, in <module>
    sys.exit(runMain(configScript(sys.argv[1:])))
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 57, in runMain
    return runOneOrMany(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 83, in runOneOrMany
    return runTransform(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 135, in runTransform
    module.walk(tree)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 483, in acceptIf
    ifBlock.walk(node.children[1], memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 668, in nodeOpExpr
    self.zipWalk(node.children, visitors, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 99, in zipWalk
    visitor.walk(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 700, in acceptPreformatted
    self.zipWalk(node.children, vs, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 99, in zipWalk
    visitor.walk(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 743, in acceptPrePost
    name = node.firstChildOfType(tokens.IDENT).text
AttributeError: 'NoneType' object has no attribute 'text'
```

ChainSolver.py

Error:

```
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 259, in <module>
    sys.exit(runMain(configScript(sys.argv[1:])))
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 57, in runMain
    return runOneOrMany(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 83, in runOneOrMany
    return runTransform(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 135, in runTransform
    module.walk(tree)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 625, in acceptWhile
    whileStat.walk(blkNode, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 223, in acceptVarDeclaration
    assgnExp.walk(declExp, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 700, in acceptPreformatted
    self.zipWalk(node.children, vs, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 99, in zipWalk
    visitor.walk(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 743, in acceptPrePost
    name = node.firstChildOfType(tokens.IDENT).text
AttributeError: 'NoneType' object has no attribute 'text'
```

FishSolver.py

Error:

```
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 259, in <module>
    sys.exit(runMain(configScript(sys.argv[1:])))
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 57, in runMain
    return runOneOrMany(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 83, in runOneOrMany
    return runTransform(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 135, in runTransform
    module.walk(tree)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 625, in acceptWhile
    whileStat.walk(blkNode, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 86, in walk
    visitor.walk(child, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 668, in nodeOpExpr
    self.zipWalk(node.children, visitors, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 99, in zipWalk
    visitor.walk(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 83, in walk
    visitor = self.accept(tree, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 43, in accept
    return call(node, memo)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/visitor.py", line 743, in acceptPrePost
    name = node.firstChildOfType(tokens.IDENT).text
AttributeError: 'NoneType' object has no attribute 'text'

```

SudokuSolver.py

Error:
```
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 259, in <module>
    sys.exit(runMain(configScript(sys.argv[1:])))
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 57, in runMain
    return runOneOrMany(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 83, in runOneOrMany
    return runTransform(options)
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 128, in runTransform
    transformAST(tree, config)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 37, in transformAST
    call(node, config)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/mod/transform.py", line 97, in lengthToLen
    expr.children.remove(method)
ValueError: list.remove(x): x not in list
```
