import re


# seq = '((((..([[(..((..(((((...((((....))))..)))))..))..)]])..))))'
seq = '((..(((((...((((....))))....)))))..))'
# seq = '((..[[..{{..))..]]..}}'
# seq = '(...((((....))))..)'
    # '0  3  611  11  1   1   1  1    1  1  1   1  11  111  1111' hel pos


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
    rep_points = []
    if seq[0] == '(':
        rep_points.append(0)

    # Add indices of elements starting or ending loop or helix
    for (ind1, el1), (ind2, el2) in zip(enumerate(seq[1:], 1), enumerate(seq[2:], 2)):
        if el1 != el2 and el1 in ['(', ')']:
            rep_points.append(ind1)
        elif el1 != el2 and el2 in ['(', ')']:
            rep_points.append(ind2)
    # Add last index
    if len(seq) - 1 == ')' and len(seq) - 1 not in rep_points:
        rep_points.append(len(seq) - 1)
    # Delete duplicates
    result = list(sorted(set(rep_points)))

    return result


def is_hairpin(seq):
    """Find whether given representation of sequence forms hairpin"""
    if seq.startswith('(') and seq.endswith(')'):
        return True
    return False


def is_loop(seq):
    """Find whether given representation of sequence forms internal loop"""
    if seq.startswith('(.') and seq.endswith('('):
        return True
    return False


def anti_seq(piece, pattern, seq, finish):
    """
    Find the other half of motif
    :param piece: string - representation of motif part
    :param pattern: re.compiled pattern to look for, defined in upper scope
    :param seq: string - whole representation of sequence
    :param finish: int - index where part of motif ends
    :return: string - entire motif from given and found parts
    """
    if is_loop(piece):
        compl = pattern.search(seq, finish).group(0)
        return piece + compl
    elif is_hairpin(piece):
        return piece
    elif piece.endswith(')'):
        return ''
    else:
        return piece + piece.replace('(', ')')


def decomposition(seq):

    motifs = []
    pieces = []

    worep = finding_heloops(seq)
    # print(worep)
    for i, j in zip(worep, worep[1:]):
            pieces.append(seq[i:j + 1])

    pattern=re.compile('\)\.+\)')
    # print(list(zip(pieces, zip(worep, worep[1:]))))

    for piece, (start, finish) in zip(pieces, zip(worep, worep[1:])):
        motif = anti_seq(piece, pattern, seq, finish)
        if motif:
            motifs.append((start, finish, motif))

    return motifs



a = decomposition(seq)
for i in a:
    print(i)

