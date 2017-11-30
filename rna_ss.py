import re

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

def is_parenthesis(c):
    return c == '(' or c == ')'

