import re


seq = '(...((((....))))..)'
# seq = '((((..([[(..((..(((((...((((....))))..)))))..))..)]])..))))'
# seq = '((..[[..{{..))..]]..}}'

# print(seq[::-1])
# Res
# Searching everything except . and parenthesis
conversion = re.compile('[^\.\(\)]')
# Searching IL in reversed seq
iloop = re.compile('\)\.+\)')
# Searching helices in reversed seq
# helix = re.compile('\(+')
# Searching hairpins in reversed seq
hairpin = re.compile('\(\.+\)')


def convert_to_par(seq):
    seq = conversion.sub('.', seq)
    return seq


def is_hairpin(seq):
    """Find whether given representation of sequence forms hairpin"""
    if seq.startswith('(') and seq.endswith(')'):
        return True
    return False


def is_helix(seq):
    """Find whether given representation of sequence forms helix"""
    if not seq.startswith('(.') and seq.endswith('('):
        return True
    return False


def is_iloop(seq):
    """Find whether given representation of sequence forms internal loop"""
    if seq.startswith('(.') and seq.endswith('('):
        return True
    return False



seq = convert_to_par(seq)
rev = seq[::-1]
length = len(seq)

# List with indices of points where something starts or finishes up to left part of final motif
rep_points = []
# List with indices of points where something starts or finishes from end to the first right part of motifs
back_points = []
# pieces = []

for (ind1, el1), (ind2, el2) in zip(enumerate(seq), enumerate(seq[1:], 1)):
    if el1 != el2 and el1 == '(':
        rep_points.append(ind1)
    elif el1 != el2 and el2 == '(':
        rep_points.append(ind2)
    elif el1 != el2 and el2 == ')':
        rep_points.append(ind2)
        break

for (ind1, el1), (ind2, el2) in zip(enumerate(seq), enumerate(seq[1:], 1)):
    if el1 != el2 and el1 == ')':
        back_points.append(length - ind1 - 1)
    elif el1 != el2 and el2 == ')':
        back_points.append(length - ind2 - 1)
    # if seq[-1] == ')' and 0 not in back_points:
    #     back_points.append(0)
back_points.append(back_points[-1])
# Delete duplicates, perhaps it is redundant
# rep_points = list(sorted(set(rep_points)))
# back_points = list(sorted(back_points, reverse=True))
# print(rep_points, back_points)

pieces = [(seq[i:j + 1], i, j, len(seq[i:j + 1])) for i, j in zip(rep_points, rep_points[1:])]
# Not good
if seq[0] == '(' and seq[1] == '.':
    pieces.insert(0, ('(', 0, 0, 1))

print(rep_points, back_points, pieces, length, sep='\n')


for piece, bind in zip(pieces, back_points[::-1]):
    if is_helix(piece[0]):

        pat = re.compile('\){{{}}}'.format(piece[3]))
        fin = pat.search(rev, min(piece[1], bind))
        print(piece[1], piece[2], piece[0], fin.group().replace('(', ')'), length - fin.span()[1], length - fin.span()[0] - 1)
        print(piece[1], bind, '\n')
    elif is_iloop(piece[0]):
        fin = iloop.search(rev, bind)
        print(piece[1], piece[2], piece[0], fin.group()[::-1], length - fin.span()[1], length - fin.span()[0] - 1)
    elif is_hairpin(piece[0]):
        print(piece[1], piece[0], piece[2])

    # Determine of which structure is a piece
    # Find it complement
    # Return results


quit()

# seq = '((((..([[(..((..(((((...((((....))))..)))))..))..)]])..))))'
# seq = '((..(((((...((((....))))....)))))..))'
#      01  4   8   12 15   20 23   28  32 35
# seq = '((..[[..{{..))..]]..}}'
# seq = '(...((((....))))..)'
    # '0  3  611  11  1   1   1  1    1  1  1   1  11  111  1111' hel pos


# Make 2 separate lists for 1st parts of motifs and for 2nd parts by dividing conditions in heloops function DONE
# Indices in 2nd list perhaps should be in a form of len(seq) - i DONE
# Go by re.search in reverse direction, pass index in it from 2nd list, and reverse pattern sequence (cause you reverse all sequence)


# Searching IL in reversed seq
iloop = re.compile('\(\.+\(')
# Searching helices in reversed seq
helix = re.compile('\(+')
# Searching hairpins in reversed seq
hairpin = re.compile('\(\.+\)')

def loop_elems(seq):
    # Initialize list of loop elements positions
    rep_points = [0]
    # Add positions of loop elements
    for (ind1, el1), (ind2, el2), (ind3, el3) in zip(enumerate(seq[1:], 1), enumerate(seq[2:], 2), enumerate(seq[3:], 3)):
        if el1 == el2 == el3:
            continue
        elif el1 in ['(', ')'] and el2 == '.':
            rep_points.append(ind1)
        elif el1 == el2 != el3 and el2 in ['(', ')']:
            rep_points.append(ind2)
        elif el2 in ['(', ')'] and el3 not in ['(', ')']:
            rep_points.append(ind2)

        elif el1 == el2 != el3 and el3 in ['(', ')']:
            rep_points.append(ind3)
    # Add last value
    if seq[-1] == ')':
        rep_points.append(len(seq) - 1)

    # Delete duplicates which were added in uneffecrive cycle
    result = list(sorted(set(rep_points)))

    return result


# Alternative variant, seems better
def finding_heloops(seq):
    """
    Find indices in sequence where helices and loops start and finish
    :param seq: string - 2d representation of rna with ., (, [ and {
    :return: list - indices
    """
    # Data modification
    seq = seq.replace('[', '.')
    seq = seq.replace(']', '.')
    seq = seq.replace('{', '.')
    seq = seq.replace('}', '.')
    # Initialize list of loop elements positions
    length = len(seq) - 1
    rep_points = []
    backward = []
    if seq[0] == '(':
        rep_points.append(0)

    # Add indices of elements starting or ending loop or helix
    for (ind1, el1), (ind2, el2) in zip(enumerate(seq[1:], 1), enumerate(seq[2:], 2)):
        if el1 != el2 and el1 == '(':
            rep_points.append(ind1)
        elif el1 != el2 and el1 == ')':
            backward.append(length - ind1)
        elif el1 != el2 and el2 == '(':
            rep_points.append(ind2)
        elif el1 != el2 and el2 == ')':
            backward.append(length - ind2)
    # Add last index
    rep_points.append(length - backward[0])
    if seq[-1] == ')' and 0 not in backward:
        backward.append(0)
    # Delete duplicates
    forward = list(sorted(set(rep_points)))
    backward = list(sorted(set(backward)))

    return forward, backward





def anti_seq(piece, rev, finish, brpieces):
    """
    Find the other half of motif
    :param piece: string - representation of motif part
    :param rev: string - whole reversed representation of sequence
    :param finish: int - index where part of motif ends
    :return: tuple of int, int, string - indices of start and end of second part of motif and entire motif from given and found parts
    """
    # -1 means not implemented here
    if is_loop(piece):
        compl = iloop.search(rev, finish)
    elif is_hairpin(piece):
        compl = hairpin.search(rev, finish)
    else:
        compl = helix.search(rev, finish)

    inds = compl.span(0)
    compl = compl.group(0)
    print(compl, brpieces)

    brpieces.remove(compl)

    return inds[0], inds[1], piece + compl


def decomposition(seq):

    motifs = []
    fpieces = []
    bpieces = []
    # brpieces = []
    rev = seq[::-1]

    forward, backward = finding_heloops(seq)
    print(forward, backward, sep='\n')
    for i, j in zip(forward, forward[1:]):
        fpieces.append(seq[i:j + 1])
    for k, z in zip(backward, backward[1:]):
        bpieces.append(rev[k:z + 1])


    print(fpieces, bpieces, sep='\n')
    print("\n\nRepart\n")


    # print(list(zip(pieces, zip(worep, worep[1:]))))

    for piece, (start, finish) in zip(fpieces, zip(forward, backward[1:])):
        motif = anti_seq(piece, rev, finish, brpieces)
        if motif:
            motifs.append((start, finish, motif))

    return motifs



a = decomposition(seq)
# for i in a:
#     print(i)



