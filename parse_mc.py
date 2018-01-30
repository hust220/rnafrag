import sys
import re

def parse_graph(fn):
    edges = []
    flag = ''
    n = 0
    for line in open(fn):
        if re.search('^Base-pairs', line):
            flag = 'base-pairs'
        elif re.search('^Non-Adjacent stackings', line):
            flag = 'stackings'
        elif re.search('^Adjacent stackings', line):
            flag = 'stackings'
        elif re.search('^Residue conformations', line):
            flag = 'residues'
        elif flag == 'residues':
            g = re.search('^\s*(\D+)(\d+)\s*:.*$', line)
            n += 1
        elif flag == 'stackings':
            g = re.search('^\s*(\D+)(\d+)-(\D+)(\d+)\s*:.*$', line)
            if g:
                pair = (int(g.group(2)), int(g.group(4)))
                t = 14
                edges.append([pair[0], pair[1], t])
        elif flag == 'base-pairs':
            g = re.search('^\s*(\D+)(\d+)-(\D+)(\d+)\s*:\s*(\w+)-(\w+)\s*(.+)\s*pairing.*$', line)
            if g:
                pair = (int(g.group(2)), int(g.group(4)))
                pairing_edges = re.split('\s+', g.group(7))
                t = 13
                for edge in pairing_edges:
                    t = min(pairing_type(edge), t)
                if t != 13:
                    if re.search('cis', line):
                        t = t * 2 + 1
                    elif re.search('trans', line):
                        t = t * 2 + 2
                    else:
                        t = 13
                edges.append([pair[0], pair[1], t])
    return (n, edges)

def print_graph(n, edges):
    print n
    for edge in edges:
        for n in edge:
            print n,
        print

def pairing_type(s):
    g = re.match('([WHS])./([WHS]).', s)
    if g:
        edge = g.group(1) + '/' + g.group(2)
        if edge in ['W/W']:
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
        t = 13
    return t

if __name__ == '__main__':
    fn = sys.argv[1]
    n, edges = parse_graph(fn)
    print_graph(n, edges)

