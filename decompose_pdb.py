import os
import sys
import math
import re
from pdb import *

def decompose_pdb(pdb_fn, ghp_fn):
    name = os.path.splitext(os.path.basename(pdb_fn))[0]
    rs = model2residues(read_model(pdb_fn))
    loop_num = 0
    helix_num = 0
    for l in open(ghp_fn):
        v = re.split('\s+', l.strip())
        if len(v) == 4:
            if v[0] == 'Helix:':
                helix_num += 1
                fn = '%s-helix-%d.pdb' % (name, helix_num)
                chain = Chain("A", map(lambda s: rs[int(s)-1], re.split('-', v[3])))
            elif v[0] == 'Loop:':
                loop_num += 1
                fn = '%s-loop-%d.pdb' % (name, loop_num)
                chain = Chain("A", map(lambda s: rs[int(s)-1], re.split('-', v[3])))

            f = open(fn, 'w')
            model = Model(name, [chain])
            write_model(model, f)
            f.close()

if __name__ == '__main__':
    par = {}
    key = ''
    for i in sys.argv[1:]:
        if i[0] == '-':
            key = i[1:]
            par[key] = []
        else:
            par[key].append(i)

    pdb_fn = par["pdb"][0]
    ghp_fn = par["ghp"][0]

    decompose_pdb(pdb_fn, ghp_fn)

