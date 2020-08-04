This is a work in progress for translating the open source human techniques on HoDoKu from java into python3.

We are using a python2 package named java2python to attempt to translate some of them into python2, and then to python3 with hopes of implementing into our ai.py code.

***

6 Working No issues

4 Partially Worked (perhaps no issue but error raised)

11 Not Working (but similar error for all in hex)

***

Worked with no issues:

AIs.py

GiveUpSolver.py

GroupNode.py 

IncompleteSolver.py 

SudokuSolverFactory.py 

TableEntry.py


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
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 62550: ordinal not in range(128)
```


BruteForceSolver.py

Error:

```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 2061: ordinal not in range(128)
```

ChainSolver.py

Error:

```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 32528: ordinal not in range(128)
```

FishSolver.py

Error:

```
j2py FishSolver.java > FishSolver.py
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 1425: ordinal not in range(128)
```

MiscellaneousSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 1845: ordinal not in range(128)
```

SudokuSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 7713: ordinal not in range(128)
```

SudokuStepFinder.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 33929: ordinal not in range(128)
```

TablingSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 4692: ordinal not in range(128)
```

TemplateSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 1519: ordinal not in range(128)
```

UniquenessSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 13237: ordinal not in range(128)
```

WingSolver.py

Error:
```
# ERROR runTransform: exception while parsing
Traceback (most recent call last):
  File "/home/ivan/anaconda3/envs/py2/bin/j2py", line 120, in runTransform
    tree = buildAST(source)
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/java2python/compiler/__init__.py", line 15, in buildAST
    lexer = Lexer(StringStream(source))
  File "/home/ivan/anaconda3/envs/py2/lib/python2.7/site-packages/antlr_python_runtime-3.1.3-py2.7.egg/antlr3/streams.py", line 336, in __init__
    self.strdata = unicode(data)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 4777: ordinal not in range(128)
```
