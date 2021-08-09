import copy
import time


def remove_neg(atom): # returns atom and whether it had ! in front of it
    if atom[0] == "!":
        return atom[1:],True
    return atom,False

def sol_or_unsat(atom,atomval,res): # returns solution or false if unsatisfiable
    if res != False:
        return atom + "=" + str(atomval) + "," + res
    return res

def propagate(cnf,settotrue,atom):
    i = 0
    lencnf = len(cnf)
    while i < lencnf:
        j = 0
        lencnfi = len(cnf[i])
        while j < lencnfi:
            curr,negated = remove_neg(cnf[i][j])
            if curr == atom:
                if settotrue and not negated or negated and not settotrue:
                    cnf = cnf[:i] + cnf[i + 1:]
                    i -= 1
                    lencnf -= 1
                    break
                else:
                    cnf[i] = cnf[i][:j] + cnf[i][j + 1:]
                    j -= 1
                    lencnfi -= 1
            j += 1
        i += 1
    return cnf

def guess(cnf,atom,startingval=True,earlycutoff=False):
    newcnf = propagate(copy.deepcopy(cnf),startingval,atom)
    res = dpll(newcnf)
    atomval = startingval
    if earlycutoff:
        return atomval,res
    if res == False:
        cnf = propagate(cnf,not startingval,atom)
        res = dpll(cnf)
        atomval = not startingval
    return atomval,res

def easycase1(cnf):
    for i in range(len(cnf)):
        if len(cnf[i]) == 1:
            atom = remove_neg(cnf[i][0])[0]
            atomval,res = guess(cnf,atom)
            return sol_or_unsat(atom,atomval,res)
    return None

def easycase2(cnf):
    atomtable = {}
    for i in range(len(cnf)):
        curr = []
        for j in range(len(cnf[i])):
            atom = cnf[i][j]
            if atom not in curr:
                curr.append(atom)
                try:
                    atomtable[atom] += 1
                except KeyError:
                    atomtable[atom] = 1
    keys = atomtable.keys()
    for i in keys:
        if atomtable[i] == len(cnf):
            i,neg = remove_neg(i)
            val = True
            if neg:
                val = False
            atomval,res = guess(cnf,i,val,True)
            return sol_or_unsat(i,atomval,res)
    return None

def guess_smallest_lex(cnf):
    smallest = remove_neg(cnf[0][0])[0]
    for i in range(len(cnf)):
        for j in range(len(cnf[i])):
            atom,_ = remove_neg(cnf[i][j])
            if atom < smallest:
                smallest = atom
    atomval,res = guess(cnf,smallest)
    return sol_or_unsat(smallest,atomval,res)

def check_empty_clause(cnf):
    for i in range(len(cnf)):
        if len(cnf[i]) == 0:
            return True
    return None

def dpll(cnf):
    if len(cnf) == 0:
        return ""
    realcnf = copy.deepcopy(cnf)
    is_unsat = check_empty_clause(cnf)
    if is_unsat:
        return False
    res = easycase1(cnf)
    if res == None:
        cnf = copy.deepcopy(realcnf)
        res = easycase2(cnf)
    else:
        return res
    if res == None:
        a = guess_smallest_lex(cnf)
        return a
    return res

def dplldriver(cnf):
    vals = dpll(cnf)
    if vals == False:
        print("unsatisfiable")
        return
    for i in range(len(cnf)):
        for j in range(len(cnf[i])):
            if remove_neg(cnf[i][j])[0] not in (',' + vals):
                vals += "unbound:" + remove_neg(cnf[i][j])[0] + "=true,"
    print(vals[:-1])