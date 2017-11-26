import sys
import math

class Atom(list):
    def __init__(self, name, num, x, y, z):
        self.name = name
        self.num = num
        self.extend([x, y, z])

class Residue(list):
    def __init__(self, name, num, atoms):
        self.name = name
        self.num = num
        self.extend(atoms)

class Chain(list):
    def __init__(self, name, residues):
        self.name = name
        self.extend(residues)

class Model(list):
    def __init__(self, name, chains):
        self.name = name
        self.extend(chains)

class ParsedLine:
    def __init__(self, line):
        self.atom_name = line[12:16].strip()
        self.res_name = line[17:20].strip()
        self.chain_name = line[20:22].strip()
        self.atom_num = int(line[6:11].strip())
        self.res_num = int(line[22:26].strip())
        self.x = float(line[30:38].strip())
        self.y = float(line[38:46].strip())
        self.z = float(line[46:54].strip())

def read_model(file_name):
    atoms = []
    residues = []
    chains = []
    old_line = ''
    i = 0
    for line in open(file_name):
        if (line[0:4] == "ATOM"):
            line = ParsedLine(line)
            if i > 0:
                if line.res_num != old_line.res_num or line.res_name != old_line.res_name:
                    residues.append(Residue(old_line.res_name, old_line.res_num, atoms))
                    atoms = []
                if line.chain_name != old_line.chain_name:
                    chains.append(Chain(old_line.chain_name, residues))
                    residues = []
            atoms.append(Atom(line.atom_name, line.atom_num, line.x, line.y, line.z))
            old_line = line
            i += 1
    residues.append(Residue(old_line.res_name, old_line.res_num, atoms))
    chains.append(Chain(old_line.chain_name, residues))
    return Model(file_name, chains)

def print_model(model):
    num_atom = 1
    num_residue = 1
    for chain in model:
        for residue in chain:
            for atom in residue:
                print "ATOM%7i  %-4s%3s%2s%4i%12.3lf%8.3lf%8.3lf%6.2f%6.2f%12c  " % \
                    (num_atom, atom.name , residue.name , chain.name , residue.num, atom[0], atom[1], atom[2] , 1.00 , 0.00, atom.name[0])
                num_atom += 1
            num_residue += 1
 
def center(res):
    c = [0, 0, 0]
    for atom in res:
        for i in range(0, 3):
            c[i] += atom[i]
    for i in range(0, 3):
        c[i] /= 3.0
    return c

def distance(c1, c2):
    n = 0
    for i in range(0, 3):
        n += (c1[i] - c2[i]) ** 2
    return math.sqrt(n)

def min_distance(r1, r2):
    min = 999
    for atom1 in r1:
        for atom2 in r2:
            d = distance(atom1, atom2)
            if d < min:
                min = d
    return min

def ca_distance(r1, r2):
    for atom1 in r1:
        if atom1.name == "CA":
            for atom2 in r2:
                if atom2.name == "CA":
                    return distance(atom1, atom2)

def contacts(model, cutoff, k):
    num_res1 = 0
    for chain1 in model:
        for res1 in chain1:
            num_res2 = 0
            for chain2 in model:
                for res2 in chain2:
                    if num_res2 - num_res1 > k:
                        d = ca_distance(res1, res2)
                        if d < cutoff:
                            print chain1.name, '-', res1.num, '-', res1.name, " : ", chain2.name, '-', res2.num, '-', res2.name, ':', d
                    num_res2 += 1
            num_res1 += 1

if __name__ == '__main__':
    par = {}
    key = ''
    for i in sys.argv[1:]:
        if i[0] == '-':
            key = i[1:]
            par[key] = []
        else:
            par[key].append(i)
    model = read_model(par["pdb"][0])
    cutoff = 7
    if "cutoff" in par:
        cutoff = float(par["cutoff"][0])
    k = 0
    if "k" in par:
        k = int(par["k"][0])
    contacts(model, cutoff, k)

