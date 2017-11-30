import re


seq = '(...((((....))))..(())..)'
#seq = '(...((((....))))..)'
# seq = '((((..([[(..((..(((((...((((....))))..)))))..))..)]])..))))'
# seq = '((..[[..{{..))..]]..}}'


# Res
# Searching everything except . and parenthesis
conversion = re.compile('[^\.\(\)]')

# Searching IL in reversed seq
iloop = re.compile('\)\.+\)')

# Searching hairpins in reversed seq
hairpin = re.compile('\(\.+\)')


def convert_to_par(seq):
    """Convert everything in structure to parenthesis and dots"""
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

# Populate rep_points
for (ind1, el1), (ind2, el2) in zip(enumerate(seq), enumerate(seq[1:], 1)):
    if el1 != el2 and el1 == '(':
        rep_points.append(ind1)
    elif el1 != el2 and el2 == '(':
        rep_points.append(ind2)
    elif el1 != el2 and el2 == ')':
        rep_points.append(ind2)
        break
if seq[0] == '(' and 0 not in rep_points:
    rep_points.append(0)

# Populate back_points
for (ind1, el1), (ind2, el2) in zip(enumerate(seq), enumerate(seq[1:], 1)):
    if el1 != el2 and el1 == ')':
        back_points.append(length - ind1 - 1)
    elif el1 != el2 and el2 == ')':
        back_points.append(length - ind2 - 1)
if seq[-1] == ')' and 0 not in back_points:
    back_points.append(0)

# Sort lists with points
rep_points = sorted(rep_points)
back_points = sorted(back_points, reverse=True)

# Create list with information about left motifs part
pieces = [(seq[i:j + 1], i, j, len(seq[i:j + 1])) for i, j in zip(rep_points, rep_points[1:])]

# print(rep_points, back_points, pieces, length, sep='\n')

# Find complement of each motif part
for piece, bind in zip(pieces, back_points[::-1]):
    # If we have a helix
    if is_helix(piece[0]):
        pat = re.compile('\){{{}}}'.format(piece[3]))
        fin = pat.search(rev, min(piece[1], bind))
        print(piece[0] + fin.group().replace('(', ')'),
              '-'.join(map(str, list(range(piece[1], piece[2] + 1)) +
                           list(range(length - fin.span()[1], length - fin.span()[0])))))
    # Internal loop
    elif is_iloop(piece[0]):
        fin = iloop.search(rev, bind)
        print(piece[0] + fin.group().replace('(', ')'),
              '-'.join(map(str, list(range(piece[1], piece[2] + 1)) +
                           list(range(length - fin.span()[1], length - fin.span()[0])))))
    # Or hairpin
    elif is_hairpin(piece[0]):
        print(piece[0], '-'.join(map(str, list(range(piece[1], piece[2] + 1)))))



