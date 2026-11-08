"""Diagnostic (not the object): the idealized uncapped behavioural table of the 55-program catalogue of bully_resist.py (spec:
"an idealized uncapped behavioural table for P and O, to separate strategic failure from timeout-induced behaviour").

Reading a partner in the capped evaluator times out whenever the partner reads back (the regress lemma), so readers read readers as
TO.  The idealization removes the caps by level iteration (the budget iteration from bottom of the DSL's weak arm): level 0 returns TO for every
read; level m + 1 evaluates each program with its reads replaced by the level-m outputs of the partner in the profile the read would run (a read
of next b in (a, b, c) is b's output in (b, c, a); of prev c it is c's output in (c, a, b); a probe replaces the third slot by the constant of
code 3 (dir n) or 0 (dir p)).  A fixed point is the table where reads are answered by what the partner would do; profiles that cycle are
reported and keep their last level.  No read times out and no charge is levied (the A_f charges are zero), so this table separates what the
programs would do with perfect reading from what the cap makes them do.

  python3 src/bully_resist_ideal.py [OUT.json]       builds the table, reports convergence and the agreement with the capped table on
                                                      profiles whose capped evaluation had no timeout
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist as BR

TO = 9


def _acc(r, val, to_y):
    a = (r == val)
    return a | (r == TO) if to_y else a


def level(tb, X, ixC3, ixC0):
    K = tb.K
    Rn = X.transpose(2, 0, 1); Rp = X.transpose(1, 2, 0)
    # probes: Pn[a, b, c] = X[b, C3, a] (c free); Pp[a, b, c] = X[c, a, C0] (b free)
    Pn = np.broadcast_to(X[:, ixC3, :].T[:, :, None], (K, K, K))          # X[b, C3, a] indexed [a, b]
    # Pp[a, b, c] = X[c, a, C0]
    Pp = np.empty((K, K, K), X.dtype)
    M = X[:, :, ixC0]                                  # M[c, a]
    for a in range(K):
        Pp[a, :, :] = M[:, a][None, :]
    out = np.empty((K, K, K), np.int64)
    for a, (nm, fm) in enumerate(zip(tb.names, tb.fam)):
        rn, rp = Rn[a], Rp[a]
        if fm == 'const':
            out[a] = int(nm[1:])
        elif fm in ('junk_f', 'junk_r'):
            out[a] = 8
        elif fm == 'single':
            d, fb, to = nm[1], nm[2], nm[3]
            r = rn if d == 'n' else rp
            go, other = (1, 4) if d == 'n' else (4, 1)
            f = {'o': other, 'z': 8, 'q': go}[fb]
            out[a] = np.where(_acc(r, 4 if d == 'n' else 1, to == 'y'), go, f)
        elif fm == 'two':
            first, fb, to = nm[1], nm[2], nm[3]
            y = to == 'y'
            g1, g2 = (1, 4) if first == 'n' else (4, 1)
            f = {'f': g1, 'z': 8}[fb]
            r1, r2 = (rn, rp) if first == 'n' else (rp, rn)
            v1, v2 = (4, 1) if first == 'n' else (1, 4)
            out[a] = np.where(_acc(r1, v1, y), g1, np.where(_acc(r2, v2, y), g2, f))
        elif fm == 'exploit':
            if nm[1] == 'n':
                out[a] = np.where(rn == 3, 2, np.where(rn == 4, 1, 8))
            else:
                out[a] = np.where(rp == 0, 5, np.where(rp == 1, 4, 8))
        elif fm == 'bully':
            if nm == 'Bn':
                out[a] = np.where(rn == 3, 2, 4)
            else:
                out[a] = np.where(rp == 0, 5, 1)
        elif fm in ('prudent', 'prudent_a', 'single2'):
            d, fb, to = nm[1], nm[2], nm[3]
            r = rn if d == 'n' else rp
            q = Pn[a] if d == 'n' else Pp[a]
            go, other, ex = (1, 4, 2) if d == 'n' else (4, 1, 5)
            f = {'o': other, 'z': 8}[fb]
            acc = _acc(r, 4 if d == 'n' else 1, to == 'y')
            if fm == 'single2':
                out[a] = np.where(acc, go, f)
            else:
                bad = (q == ex) if fm == 'prudent_a' else ((q == ex) | (q == TO))
                out[a] = np.where(acc, np.where(bad, f, go), f)
        elif fm == 'opener':
            first, fb, to = nm[1], nm[2], nm[3]
            y = to == 'y'
            g1, g2 = (1, 4) if first == 'n' else (4, 1)
            f = {'f': g1, 'z': 8}[fb]
            a_, b_ = rn, rp
            r1, r2 = (a_, b_) if first == 'n' else (b_, a_)
            v1, v2 = (4, 1) if first == 'n' else (1, 4)
            dpart = np.where(_acc(r1, v1, y), g1, np.where(_acc(r2, v2, y), g2, f))
            out[a] = np.where((a_ == 2) & (b_ == 3), 4, np.where((b_ == 5) & (a_ == 0), 1, dpart))
        else:
            raise ValueError(fm)
    return out


def build(tb, max_levels=30, rounds=8):
    """level iteration from the all-TO bottom.  Cells that still change after max_levels levels (reads that depend on each other with no
    fixed point reached from below) are frozen at the default action 8 (the timeout action: a read that diverges makes the reader diverge) and
    the iteration is repeated until nothing changes.  Returns (table, frozen mask, history of (round, changing cells))."""
    K = tb.K
    ixC3, ixC0 = tb.names.index('C3'), tb.names.index('C0')
    X = np.full((K, K, K), TO, np.int64)
    frozen = np.zeros((K, K, K), bool)
    hist = []
    for rd in range(rounds):
        converged = False
        for m in range(max_levels):
            Y = level(tb, X, ixC3, ixC0)
            Y[frozen] = 8
            diff = int((Y != X).sum())
            X = Y
            if diff == 0:
                converged = True
                break
        hist.append((rd, diff, int(frozen.sum())))
        if converged:
            break
        Y = level(tb, X, ixC3, ixC0)
        Y[frozen] = 8
        newly = (Y != X) & ~frozen
        frozen |= newly
        X[frozen] = 8
    return X, frozen, hist


def ideal_tabs(cache_dir=None):
    """a TabsBR-like object with the idealized codes, no steps, no timeouts, no forfeits, no charges."""
    import copy
    tb = BR.TabsBR(cache_dir=cache_dir or os.path.join(ROOT, 'runs', '_cache'))
    X, cyc, hist = build(tb)
    ib = copy.copy(tb)
    ib.code = X.astype(np.int8)
    ib.steps = np.zeros_like(tb.steps); ib.nto = np.zeros_like(tb.nto); ib.fo = np.zeros_like(tb.fo)
    ib._joint()
    ib.cycling = cyc; ib.hist = hist
    return ib, tb


if __name__ == '__main__':
    ib, tb = ideal_tabs()
    X = ib.code.astype(np.int64)
    cap = tb.code.astype(np.int64)
    # profiles where the capped evaluation of a had no timeout and the partners' own capped evaluations had none either
    clean = (tb.nto == 0) & (tb.fo == 0)
    agree_clean = float((X[clean] == cap[clean]).mean())
    res = dict(rounds=len(ib.hist), history=ib.hist, frozen_profiles=int(ib.cycling.sum()), profiles=int(X.size),
               clean_profiles=int(clean.sum()), agreement_on_clean_profiles=agree_clean,
               agreement_all=float((X == cap).mean()))
    # per family: share of profiles where the idealized output differs from the capped one
    fam = np.array(tb.fam)
    res['differs_by_family'] = {f: float((X[fam == f] != cap[fam == f]).mean()) for f in sorted(set(tb.fam))}
    # mutual compatibility under the ideal table: share of (a in slot 0, b in slot 1, third c over the 29) forming a fair pair on slots 0, 1
    import migration_window as MW
    OUT = ib.VEC[ib.JT]
    names = tb.names; idx = {n: i for i, n in enumerate(names)}
    def pair01(A, B):
        n = t = 0
        for a in A:
            for b in B:
                for c in range(29):
                    o = int(OUT[a, b, c]); sh = MW.X[o]
                    t += 1; n += (MW.T.cat[o] == 'fair' and sh[0] > 0 and sh[1] > 0)
        return n / t
    sets = dict(Pz=[idx[x] for x in BR.NAMES_P if x[2] == 'z'], O=[idx[x] for x in BR.NAMES_O], F=[i for i in range(29) if tb.fam[i] in ('single', 'two')],
                half=[idx['C1'], idx['C4']], Bn=[idx['Bn']], Bp=[idx['Bp']])
    res['compat_ideal'] = {'%s x %s' % (a, b): pair01(sets[a], sets[b]) for a, b in (('Pz', 'Pz'), ('Pz', 'F'), ('F', 'F'), ('O', 'O'), ('O', 'F'), ('Pz', 'Bn'), ('Pz', 'Bp'), ('F', 'Bn'), ('F', 'Bp'), ('O', 'Bn'), ('O', 'Bp'))}
    if len(sys.argv) > 1:
        json.dump(res, open(sys.argv[1], 'w'), indent=1)
    print(json.dumps(res, indent=1))
