iff = "<=>"
ifthen = ["=>","<="]
ampersand = "&"
negation = "!"
disjunction = "|"
par = "()"


def check_negation(char):
    return char == negation

def check_openpar(char):
    return char == par[0]

def check_closepar(char):
    return char == par[1]

def check_iff(string):
    return string == iff

def check_if(string):
    return string == ifthen[0] or string == ifthen[1]

def check_or(char):
    return char == disjunction

def check_and(char):
    return char == ampersand

def parenthesize(string):
    return par[0] + string + par[1]

def replace(string,start,end,replacement):
    return string[:start] + replacement + string[end:]

def endpar(line,idx):
    count = 0
    for i in range(idx,len(line)):
        if check_openpar(line[i]):
            count += 1
        elif check_closepar(line[i]):
            count -= 1
            if count == 0:
                return i

def replace_get_endidx(string,start,end,replacement):
    line = replace(string,start,end,replacement)
    return line,start + len(replacement),len(line)

def get_terms_ops(line):
    line = remove_extraneous_pars(line)
    terms = []
    ops = []
    i = 0
    while i < len(line):
        if check_openpar(line[i]):
            idx = i
            i = endpar(line,i) + 1
            terms.append([idx,i])
            continue
        elif notop(line[i]):
            atomend = untilop(line,i)
            terms.append([i,atomend])
            i = atomend
            continue
        else: # must be op
            ops.append(line[i])
        i += 1
    return terms,ops

def recurse_pars(line,fxn_to_recurse):
    i = 0
    lenline = len(line)
    while i < lenline:
        if check_openpar(line[i]):
            idx = i + 1
            i = endpar(line,i)
            line,i,lenline = replace_get_endidx(line,idx,i,fxn_to_recurse(line[idx:i]))
            continue
        i += 1
    return line

def check_parenthesize(*args): # if multiple terms in a or b, then a and/or b needs to be parenthesized to preserve order of ops
    returnvals = list(args)
    for i in range(len(returnvals)):
        if len(get_terms_ops(returnvals[i])[0]) > 1:
            returnvals[i] = parenthesize(returnvals[i])
    if len(returnvals) == 1:
        returnvals = returnvals[0] # return only element in returnvals
    return returnvals

def next_occurence(find,instr,startingidx,offset): # find "find" in "instr[startingidx+offset:]" and if not found, then return len(instr)
    nextfind = None
    try:
        nextfind = instr.index(find,startingidx + offset)
    except ValueError:
        nextfind = len(instr)
    return nextfind

def remove_iffs(line):
    iffs = line.count(iff) # assume only top level <=>
    if iffs != 0:
        line = recurse_pars(line,remove_iffs)
    alastidx = 0
    for i in range(iffs):
        alastidx = line.index(iff,alastidx + len(iff)) if alastidx != 0 else line.index(iff)
        a = line[:alastidx]
        b = None
        nextiff = next_occurence(iff,line,alastidx,len(iff))
        b = line[alastidx + len(iff):nextiff]
        # intermediate step:
        # line = par[0] + a + ifthen + b + par[1] + ampersand + par[0] + b + ifthen + a + par[1]
        a,b = check_parenthesize(a,b)
        line = parenthesize(negation + a + disjunction + b) + ampersand + parenthesize(negation + b + disjunction + a) + line[nextiff:]
    return line

def remove_ifs(line):
    totalifs = line.count(ifthen[0]) + line.count(ifthen[1]) # assume only top level ifs
    if totalifs != 0:
        line = recurse_pars(line,remove_ifs)
    totalifs = line.count(ifthen[0]) + line.count(ifthen[1]) # assume only top level ifs
    alastidx = 0
    for i in range(totalifs):
        forwardarrow = None
        # ifindices = [line.index(ifthen[0],alastidx + len(ifthen[0])),line.index(ifthen[0],alastidx + len(ifthen[0]))] if alastidx != 0 else\
        #     [line.index(ifthen[0]),line.index(ifthen[0])]
        # ifindices stores 1st occurence of "=>" after alastidx at idx 0, and 1st occurence of "<=" after alastidx at idx 1
        ifindices = None
        if alastidx != 0: # if not first run, look starting from last occurence
            ifindices = [next_occurence(ifthen[0],line,alastidx,len(ifthen[0])),next_occurence(ifthen[1],line,alastidx,len(ifthen[1]))]
        else: # first run so look starting from 0
            ifindices = [next_occurence(ifthen[0],line,0,0),next_occurence(ifthen[1],line,0,0)]
        alastidx = min(ifindices)
        if alastidx == ifindices[0]:
            forwardarrow = True
        else:
            forwardarrow = False
        a = line[:alastidx]
        b = None
        # think of this as nextif=min(nextbackwardifidx,nextforwardifidx)
        nextif = min(next_occurence(ifthen[0],line,alastidx,len(ifthen[0])),next_occurence(ifthen[1],line,alastidx,len(ifthen[1])))
        b = line[alastidx + len(ifthen[0]):nextif]
        a,b = check_parenthesize(a,b)
        if forwardarrow:
            line = parenthesize(negation + a + disjunction + b) + line[nextif:]
        else:
            line = parenthesize(negation + b + disjunction + a) + line[nextif:]
    return line

def notop(char): # dont need to check for iffs and ifs bc already gotten rid of and we consider ! part of the literals
    if check_and(char):
        return False
    if check_or(char):
        return False
    return True

def untilop(line,i):
    while i < len(line) and notop(line[i]):
        i += 1
    return i

def validpars(line):
    sum = 0
    for i in line:
        if sum < 0:
            return False
        if check_openpar(i):
            sum += 1
        elif check_closepar(i):
            sum -= 1
    return True

def remove_extraneous_pars(line):
    if check_openpar(line[0]) and check_closepar(line[-1]) and validpars(line[1:-1]):
        line = line[1:-1]
    return line

def flip(char):
    if check_and(char):
        return disjunction
    return ampersand

def negate(line):
    i = 0
    lenline = len(line)
    while i < lenline:
        if notop(line[i]):
            if check_openpar(line[i]):
                epidx = endpar(line,i)
                line,i,lenline = replace_get_endidx(line,i,epidx + 1,check_parenthesize(negate(line[i + 1:epidx])))
            elif check_negation(line[i]):
                endidx = None
                if check_openpar(line[i + 1]):
                    endidx = endpar(line,i)
                    line,i,lenline = replace_get_endidx(line,i,endidx + 1,check_parenthesize(line[i + 2:endidx]))
                else:
                    endidx = untilop(line,i)
                    line,i,lenline = replace_get_endidx(line,i,endidx,check_parenthesize(line[i + 1:endidx]))
            else:
                atomend = untilop(line,i)
                line,i,lenline = replace_get_endidx(line,i,atomend,negation + line[i:atomend])
        else:
            line,i,lenline = replace_get_endidx(line,i,i + 1,flip(line[i]))
    return line

def propagatenegations(line):
    i = 0
    lenline = len(line)
    while i < lenline:
        if check_negation(line[i]) and check_openpar(line[i + 1]):
            epidx = endpar(line,i)
            line,i,lenline = replace_get_endidx(line,i,epidx + 1,check_parenthesize(negate(line[i + 2:epidx])))
            continue
        i += 1
    return line

def pushnegations(line):
    return propagatenegations(line)

def combine_ors(t1,t2):
    if not check_openpar(t1[0]) and not check_openpar(t2[0]):
        return t1 + disjunction + t2
    t1 = remove_extraneous_pars(t1)
    t2 = remove_extraneous_pars(t2)
    terms1,ops1 = get_terms_ops(t1)
    terms2,ops2 = get_terms_ops(t2)
    if len(get_terms_ops(t2)[0]) == 1 or check_or(ops2[0]): # only 1 term or has ors only at top level
        tmp = t1
        t1 = t2
        t2 = tmp
        tmp = terms1
        terms1 = terms2
        terms2 = tmp
        tmp = ops1
        ops1 = ops2
        ops2 = tmp
    line = ""
    if len(terms1) == 1 or check_or(ops1[0]): # can be handled in 1 demorgan move
        if len(terms2) == 1 or check_or(ops2[0]):
            if check_openpar(t1[0]):
                t1 = t1[1:]
            else:
                t1 = t1 + par[1]
            if check_openpar(t2[0]):
                t2 = t2[:-1]
            else:
                t2 = par[0] + t2
            return t2 + disjunction + t1
        for i in range(len(terms2)):
            ith1term = remove_extraneous_pars(t2[terms2[i][0]:terms2[i][1]])
            for j in range(len(terms1)):
                ith1term += disjunction + remove_extraneous_pars(t1[terms1[j][0]:terms1[j][1]])
            line += parenthesize(ith1term) + ampersand
        line = line[:-1] # remove last and
        return line
    # ands in both args
    for i in range(len(terms1)):
        line += remove_extraneous_pars(combine_ors(t1[terms1[i][0]:terms1[i][1]],parenthesize(t2))) + ampersand
    line = line[:-1]
    return line

def demorgan(line):
    line = remove_extraneous_pars(recurse_pars(line,demorgan))
    terms,op = get_terms_ops(line)
    if len(terms) > 2:
        return line
    op = op[0]
    left = line[terms[0][0]:terms[0][1]]
    right = line[terms[1][0]:terms[1][1]]
    if check_and(op):
        # next few lines are probably overcareful checks to make sure the right thing is being done
        _,ops = get_terms_ops(left)
        if len(ops) > 0 and check_and(ops[0]):
            left = remove_extraneous_pars(left)
        if validpars(left[1:-1]) and check_closepar(left[-1]) and check_and(ops[0]):
            left = left[:-1]
        _,ops = get_terms_ops(right)
        if len(ops) > 0 and check_and(ops[0]):
            right = remove_extraneous_pars(right)
        if validpars(right[1:-1]) and check_openpar(right[0]) and check_and(ops[0]):
            right = right[1:]
        return left + ampersand + right
    return remove_extraneous_pars(combine_ors(left,right))

def group_ands(line):
    line = recurse_pars(line,group_ands)
    terms,ops = get_terms_ops(line)
    for i in range(len(ops) - 1,-1,-1):
        if check_and(ops[i]):
            line,_,_ = replace_get_endidx(line,terms[i][0],terms[i + 1][1],parenthesize(line[terms[i][0]:terms[i + 1][1]]))
    return line

def groupsof2(line):
    line = recurse_pars(line,groupsof2)
    terms,ops = get_terms_ops(line)
    if len(terms) == 2:
        return line
    numands = 0
    for i in range(len(ops) - 1,-1,-1): # going in backwards order to not deal with weird indexing
        if check_and(ops[i]):
            line,_,_ = replace_get_endidx(line,terms[i][0],terms[i + 1][1],parenthesize(line[terms[i][0]:terms[i + 1][1]]))
            numands += 1
    if numands < len(ops):
        terms,ops = get_terms_ops(line) # now every op is or
        for i in range(len(ops) - 1,0,-1):
            line,_,_ = replace_get_endidx(line,terms[i][0],terms[i + 1][1],parenthesize(line[terms[i][0]:terms[i + 1][1]]))
    return remove_extraneous_pars(line)

def group_ands(line):
    line = recurse_pars(line,group_ands)
    terms,ops = get_terms_ops(line)
    for i in range(len(ops) - 1,-1,-1):
        if check_and(ops[i]):
            line,_,_ = replace_get_endidx(line,terms[i][0],terms[i + 1][1],parenthesize(line[terms[i][0]:terms[i + 1][1]]))
    return line

def simple_str(line):
    return remove_extraneous_pars(demorgan(groupsof2(pushnegations(group_ands(remove_ifs(remove_iffs(line)))))))

def separate_into_sentences(line):
    lines = []
    latest = []
    i = 0
    while i < len(line):
        if check_and(line[i]):
            lines.append(latest)
            latest = []
        elif not check_openpar(line[i]) and not check_closepar(line[i]) and not check_or(line[i]):
            op = untilop(line,i)
            if check_closepar(line[op - 1]):
                op -= 1
            latest.append(line[i:op])
            i = op
            continue
        i += 1
    lines.append(latest)
    return lines

def get_cnf(line):
    return separate_into_sentences(simple_str(line.replace(" ","")))

def get_cnf_sentences(lines):
    lst = []
    for line in lines:
        lst += get_cnf(line)
    for line in lst:
        for atom in line:
            print(atom,end=" ")
        print()
    print()
    return lst

def separate_sentences(fname): # make each separate sentence an element of a list and return list
    f = open(fname,'r').read()
    sentences = []
    latest = ""
    for i in range(len(f)):
        if f[i] == '\n':
            if latest != "":
                sentences.append(latest)
            latest = ""
            continue
        latest += f[i]
    if latest != "":
        sentences.append(latest)
    return sentences

def from_cnf(fname): # input is cnf, just need to put in list form
    f = open(fname,'r').read()
    sentences = []
    latest = []
    latestelement = ""
    for i in range(len(f)):
        if f[i] == "\n":
            if latestelement != "":
                latest.append(latestelement)
            if latest != []:
                sentences.append(latest)
            latest = []
            latestelement = ""
            continue
        if f[i] == " ":
            latest.append(latestelement)
            latestelement = ""
            continue
        latestelement += f[i]
    if latestelement != "":
        latest.append(latestelement)
    if latest != []:
        sentences.append(latest)
    return sentences