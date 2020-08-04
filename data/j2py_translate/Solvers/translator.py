import os
import java2python

for filename in os.listdir('/home/ivan/Desktop/Lambda/Labs/j2p/Solvers'):
    if filename.endswith(".java"):
        print(java2python(filename))
