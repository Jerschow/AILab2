import to_CNF
import sys
from os import path
from dpll import dplldriver


print()
convert = None
fname = None
for i in range(len(sys.argv)):
    if sys.argv[i] == "-convert":
        if convert != None:
            print("Error: only 1 instance of either '-convert' or '-noconvert' allowed")
            exit(1)
        convert = True
    elif sys.argv[i] == "-noconvert":
        if convert != None:
            print("Error: only 1 instance of either '-convert' or '-noconvert' allowed")
            exit(1)
        convert = False
    elif sys.argv[i] == "main.py":
        continue
    else:
        if fname != None:
            print("Only 1 graph file allowed.")
            exit(1)
        if not path.isfile(sys.argv[i]):
            print("File does not exist: " + sys.argv[i])
            exit(1)
        fname = sys.argv[i]
if convert == None:
    print("Error: Need to specify '-convert' or '-noconvert' to determine if this is BNF that needs to be converted to CNF before solving")
    exit(1)
if fname == None:
    print("Error: Need to provide file")
    exit(1)
try:    
    if convert:
        dplldriver(to_CNF.get_cnf_sentences(to_CNF.separate_sentences(fname)))
    else:
        dplldriver(to_CNF.from_cnf(fname))
except:
    print("Error: file is not a txt file or a different error,listed above,occured")
    exit(1)
print()