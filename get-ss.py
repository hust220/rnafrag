import os
from coparser import RnaviewParser, RnaViewParseError, is_canonical
from operator import itemgetter


def main():
    """
    Parse output files from RNAview, write Secondary Structure of RNA in files
    :return:
    """
    # Create directory for file with SS annotations
    os.makedirs('rnaview_ss', exist_ok=True)

    # Take all files from rnaview_annotations directory with annotations from rnaview
    files = os.scandir('rnaview_annotations')

    # Iterate over files, try to parse them and write result to new file in created directory
    # Essentially it parses all files from rnaview without errors except for the file with base pair statistic
    for file in files:
        with open(file.path, 'r') as source:

            try:
                summary = RnaviewParser(source)
                # Extract # of pairs, if it 0, don`t create file
                np = summary['NP']['NUM_PAIRS']
                if not np:
                    print('no bp')
                    continue

                # Extract base pair information
                bp = summary['BP']
                # Choose canonical bp - standard WC GC, AU or wobble GU
                canonical_bp = bp.select(is_canonical)
                # Don`t create file if there is no canonical bp
                if not canonical_bp:
                    print('no canonical bp')
                    continue

                # Create lists with bases position in bp
                find = [int(x.Up.ResId) for x in canonical_bp]
                sind = [int(x.Down.ResId) for x in canonical_bp]
                # Find boundaries of SS which will be written
                both = find + sind
                min_pos = min(both)
                max_pos = max(both)
                # first = [(x.Up.ResName, int(x.Up.ResId)) for x in canonical_bp]
                # second = [(x.Down.ResName, int(x.Down.ResId)) for x in canonical_bp]
                # print(first, second, min_pos, max_pos, find, sind, len(first), sep='\n')

                with open(os.path.join('rnaview_ss', file.name[3:7] + '.ss'), 'w') as dest:
                    # Iterate over bases positions, add '(' or ')' to scheme if base in Secondary Structure, '.' otherwise
                    for i in range(min_pos, max_pos + 1):
                        if i in find:
                            dest.write('(')
                        elif i in sind:
                            dest.write(')')
                        else:
                            dest.write('.')

            except RnaViewParseError:
                print('!')


if __name__ == '__main__':
    main()


# Parser dictionary
'''
FN - filename
pdb/pdb1a4d.ent
<class 'str'>

PC - dictionary with # of different pairs
{'WH-tran': 4, 'HS-tran': 2, 'HS--cis': 0, 'WW-tran': 0, 'WS-tran': 0, 'SS-tran': 0, 'HH-tran': 0, 'WH--cis': 0, 'HH--cis': 0, 'SS--cis': 0, 'Standard': 9, 'WS--cis': 0, 'WW--cis': 2}
<class 'coparser.PairCounts'>

UC - uncanonical bp?
{}
<class 'dict'>

NP - dictionary with # of pairs and bases
{'NUM_PAIRS': 17, 'NUM_BASES': 41}
<class 'dict'>

BM - base multiplets?

<class 'coparser.BaseMultiplets'>

BP - table with bp?
===================================================================
Bases: Up -- Down; Annotation: Edges -- Orient. -- Conf. -- Saenger
===================================================================
Bases: A 68 G -- B 108 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 69 G -- B 107 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 70 C -- B 106 G; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 71 C -- B 105 G; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 72 G -- B 104 A; Annotation: S/H -- tran -- None -- XI;
Bases: A 73 A -- B 103 U; Annotation: H/W -- tran -- None -- XXIV;
Bases: A 74 U -- B 102 G; Annotation: H/W -- tran -- None -- n/a;
Bases: A 76 G -- B 100 G; Annotation: W/H -- tran -- None -- VII;
Bases: A 77 U -- B 99 A; Annotation: W/H -- tran -- None -- XXIV;
Bases: A 78 A -- B 98 G; Annotation: H/S -- tran -- None -- XI;
Bases: A 79 G -- B 97 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 80 U -- B 96 G; Annotation: W/W -- cis -- None -- XXVIII;
Bases: A 81 G -- B 95 U; Annotation: W/W -- cis -- None -- XXVIII;
Bases: A 82 U -- B 94 A; Annotation: -/- -- cis -- None -- XX;
Bases: A 83 G -- B 93 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 84 G -- B 92 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: A 85 G -- B 91 C; Annotation: +/+ -- cis -- None -- XIX;
Bases: B 93 C -- B 94 A; Annotation: stacked -- None -- None -- None;
Bases: B 94 A -- B 95 U; Annotation: stacked -- None -- None -- None;
Bases: B 96 G -- B 97 C; Annotation: stacked -- None -- None -- None;
Bases: B 103 U -- B 104 A; Annotation: stacked -- None -- None -- None;
Bases: A 75 G -- B 101 A; Annotation: H/W -- cis -- None -- !1H(b_b).;
Bases: A 86 G -- B 90 C; Annotation: W/W -- cis -- None -- !1H(b_b).;
<class 'coparser.BasePairs'>
'''
