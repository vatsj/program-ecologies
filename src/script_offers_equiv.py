"""Queue 80: behavioural equivalence of programs in the world-S tables.  Two programs x, y are table-equivalent on a support U if
replacing x by y in any slot of any triple over U (x's other occurrences unchanged) leaves every slot's action code, failed-read count
and forfeit unchanged.  Checked for (a) every spelling against its family's canonical spelling (on A2's support at phi = 1/2), and
(b) the + versions against the plain ones (on A3's support at phi = 1/2, where no program requires S_nx).  If (a) holds, A2's law is
A1's law with each canonical program split into identical copies: the two arms differ only in sampling.

    python3 src/script_offers_equiv.py OUT.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script_offers_dyn as D


def equivalent(tb, x, y, U):
    U = list(U)
    for arr in (tb.code, tb.nto, tb.fo):
        # x as the root program against all (n, p) in U
        if not np.array_equal(arr[x][np.ix_(U, U)], arr[y][np.ix_(U, U)]):
            return False
        # x as the next / prev partner of every root program in U
        if not np.array_equal(arr[np.ix_(U, [x], U)], arr[np.ix_(U, [y], U)]):
            return False
        if not np.array_equal(arr[np.ix_(U, U, [x])], arr[np.ix_(U, U, [y])]):
            return False
    return True


if __name__ == '__main__':
    tb = D.tabs('S')
    out = dict(spellings={}, plus={})
    U2 = np.nonzero(D.law_arm('A2', 0.03, 3.0, 0.5))[0]
    for i in U2:
        nm = tb.names[i]
        if '.' in nm and not nm.endswith('.canon'):
            c = tb.names.index(nm.split('.')[0] + '.canon')
            out['spellings'][nm] = equivalent(tb, i, c, U2)
    U3 = np.nonzero(D.law_arm('A3', 0.03, 3.0, 0.5))[0]
    for i in U3:
        nm = tb.names[i]
        if '+' in nm:
            plain = nm.replace('+', '')
            j = tb.names.index(plain)
            U = sorted(set(U3) | {j})
            out['plus'][nm] = equivalent(tb, i, j, [u for u in U if u != j] + [])
    out['all_spellings_equivalent'] = all(out['spellings'].values())
    out['all_plus_equivalent'] = all(out['plus'].values())
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(out['all_spellings_equivalent'], sum(out['spellings'].values()), len(out['spellings']),
          out['all_plus_equivalent'], sum(out['plus'].values()), len(out['plus']))
