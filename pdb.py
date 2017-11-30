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

def write_model(model, f = sys.stdout):
    num_atom = 1
    num_residue = 1
    for chain in model:
        for residue in chain:
            for atom in residue:
                f.write("ATOM%7i  %-4s%3s%2s%4i%12.3lf%8.3lf%8.3lf%6.2f%6.2f%12c  \n" % \
                    (num_atom, atom.name , residue.name , chain.name , residue.num, atom[0], atom[1], atom[2] , 1.00 , 0.00, atom.name[0]))
                num_atom += 1
            num_residue += 1
 
def model2residues(model):
    rs = []
    for chain in model:
        for res in chain:
            rs.append(res)
    return rs

