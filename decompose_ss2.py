import os
import sys
import re
from rna_ss import *

def decompose_ss(ss):
    l = len(ss)
    seq = 'X' * l
    rs = residues(seq, ss)

    hairpins = []
    stack = []
    for i in range(l):
        stack.append(rs[i])
        if i == l-1 or (ss[i] == ')' and ss[i+1] != ')'):
            extract_hairpin(hairpins, stack)
#    if len(stack) != 0:
#        hairpins.append(GHairpin(stack))
    for hp in hairpins:
        print 'Helix:',rs_seq(hp.helix),rs_ss(hp.helix),rs_nums_str(hp.helix)
        print 'Loop:',rs_seq(hp.loop),rs_ss(hp.loop),rs_nums_str(hp.loop)

def extract_hairpin(hairpins, stack):
#    print 'stack',rs_ss(stack)

    l_r = sum(r.ss == ')' for r in stack)
    # There is no parenthesis
    if l_r == 0:
        hairpins.append(GHairpin(stack))
        for i in range(len(stack)):
            stack.pop()
        return

    # stack => stack2
    n = 0
    stack2 = []
    for i in range(len(stack)):
        stack2.insert(0, stack.pop())
        if stack2[0].ss == '(':
            n += 1
            if n == l_r or (len(stack) > 0 and stack[-1].ss != '('):
                break

#    print 'stack2',rs_ss(stack2)

    # stack3 <= stack2
    l_l = sum(r.ss == '(' for r in stack2)
    stack3 = []
    n = 0
    for i in range(len(stack2)):
        stack3.append(stack2.pop(0))
        if stack3[-1].ss == ')':
            n += 1
            if n == l_l:
                break

#    print 'stack3',rs_ss(stack3)

    hairpins.append(GHairpin(stack3))
    stack.append(Residue(stack3[0].num, stack3[0].seq, '+'))
    stack.append(Residue(stack3[-1].num, stack3[-1].seq, '-'))

    # stack => stack2
    if len(stack2) != 0:
        l_r = sum(r.ss == ')' for r in stack2)
        n = 0
        for i in range(len(stack)):
            stack2.insert(0, stack.pop())
            if stack2[0].ss == '(':
                n += 1
                if n == l_r:
                    break


        hairpins.append(GHairpin(stack2))
        stack.append(Residue(stack2[0].num, stack2[0].seq, '+'))
        stack.append(Residue(stack2[-1].num, stack2[-1].seq, '-'))

#    print 'stack',rs_ss(stack)

if __name__ == '__main__':
    par = {}
    key = ''
    for i in sys.argv[1:]:
        if i[0] == '-':
            key = i[1:]
            par[key] = []
        else:
            par[key].append(i)

#    ss = '(.((((((((..((((((......[[.))))))[.....)]((((((]].....))))))..))))))).)'
    ss = par["ss"][0]

    decompose_ss(ss)


