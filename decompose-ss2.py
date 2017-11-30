import re

ss = '.((.(())((..((....))))..(())..))...'

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
    for i in range(l):
        stack.append(rs[i])
        if i == l-1 or (ss[i] == ')' and ss[i+1] != ')'):
            extract_hairpin(hairpins, stack)
#    if len(stack) != 0:
#        hairpins.append(GHairpin(stack))
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

print "Decomposing: %s\n" % ss
decompose_ss(ss)
print


