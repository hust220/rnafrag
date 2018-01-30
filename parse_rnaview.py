import sys
import re

fn = sys.argv[1]

edges = []

flag = False
for line in open(fn):
    if re.search('^BEGIN_base-pair', line):
        flag = True
    elif re.search('^END_base-pair', line):
        flag = False
    else:
        g = re.search('The total base pairs =\s*(.+)\s*\(from\s*(.+)\s*bases\)', line)
        if g:
            n = int(g.group(2))
        elif flag:
            if not re.search('!', line):
                g = re.search('^\s*(\d+)_(\d+),\s*(\S+):\s*(\d+)\s*(\S+)-(\S+)\s*(\d+)\s*(\S+):\s*(\S+/\S+)\s*(\S+)\s*.*$', line)
                if g:
                    pair = (int(g.group(1)), int(g.group(2)))
                    edge = g.group(9)
                    chir = g.group(10)
                    if edge in ['+/+', '-/-', 'W/W']:
                        t = 0
                    elif edge in ['W/H', 'H/W']:
                        t = 1
                    elif edge in ['W/S', 'S/W']:
                        t = 2
                    elif edge in ['H/H']:
                        t = 3
                    elif edge in ['H/S', 'S/H']:
                        t = 4
                    elif edge in ['S/S']:
                        t = 5
                    else:
                        print edge
                    if chir == 'cis':
                        t = t * 2 + 1
                    else:
                        t = t * 2 + 2
                    edges.append([pair[0], pair[1], t])
                else:
                    g = re.search('^\s*(\d+)_(\d+),\s*(\S+):\s*(\d+)\s*(\S+)-(\S+)\s*(\d+)\s*(\S+):\s*stacked\s*$', line)
                    if g:
                        pair = (int(g.group(1)), int(g.group(2)))
                        t = 13
                        edges.append([pair[0], pair[1], t])

print n
for edge in edges:
    for n in edge:
        print n,
    print
