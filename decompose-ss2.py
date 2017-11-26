import re


ss = '.(.(())((((....))))..(())..)'
#ss = '.(.(())((..((....))))..(())..)'

def is_parenthesis(c):
    return c == '(' or c == ')'

class Residue:
    def __init__(self, num, seq, ss):
        self.seq = seq
        self.ss = ss
        self.num = num

# Generalized hairpin
class GHairpin:
    def __init__(self, stack):
        self.helix = []
        self.loop = []
        for i in stack:
            if is_parenthesis(i.ss):
                self.helix.append(i)
            else:
                if i.ss == '+':
                    i.ss = '('
                elif i.ss == '-':
                    i.ss = ')'
                self.loop.append(i)
        if len(self.loop) != 0 and len(self.helix) != 0:
            l = len(self.helix)/2
            self.loop.insert(0, self.helix[l-1])
            self.loop.append(self.helix[l])

def decompose_ss(ss):
    l = len(ss)
    seq = 'X' * l
    rs = residues(seq, ss)

    hairpins = []
    stack = []
    for i in range(l-1):
        stack.append(rs[i])
        if ss[i] == ')' and ss[i+1] != ')':
            extract_hairpin(hairpins, stack)
    stack.append(rs[l-1])
    extract_hairpin(hairpins, stack)
    if len(stack) != 0:
        extract_hairpin(hairpins, stack)
    for hp in hairpins:
        print 'Helix:',rs_seq(hp.helix),rs_ss(hp.helix),rs_nums_str(hp.helix)
        print 'Loop:',rs_seq(hp.loop),rs_ss(hp.loop),rs_nums_str(hp.loop)

def rs_seq(rs):
    return ''.join(map(lambda i: i.seq, rs))

def rs_ss(rs):
    return ''.join(map(lambda i: i.ss, rs))

def rs_nums(rs):
    return map(lambda i: i.num, rs)

def rs_nums_str(rs):
    return '-'.join(map(lambda i: str(1+i.num), rs))

def residues(seq, ss):
    l = len(seq)
    rs = []
    for i in range(l):
        rs.append(Residue(i, seq[i], ss[i]))
    return rs

def extract_hairpin(hairpins, stack):
    stack2 = []
    l = len(stack)
    right = stack[l-1].num
    findOut = False
    for i in range(l-1,0,-1):
        stack2.insert(0, stack[i])
        if stack[i].ss == '(' and stack[i-1].ss != '(':
            hairpins.append(GHairpin(stack2))
            findOut = True
        stack.pop()
        if findOut:
            break
    if not findOut:
        stack2.insert(0, stack[0])
        hairpins.append(GHairpin(stack2))
        stack.pop()
    stack.append(Residue(stack2[0].num, stack2[0].seq, '+'))
    stack.append(Residue(stack2[-1].num, stack2[-1].seq, '-'))

print "Decomposing: %s\n" % ss
decompose_ss(ss)


