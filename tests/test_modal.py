"""Reference check for the modal arm: enumerate actual syntax trees up to n,
evaluate every pair by direct recursion over Kripke worlds (no canonical
forms), and compare with the canonical-function evaluator."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import modal as M


def trees(n):
    by = {1: [('C',), ('D',)]}
    for s in range(2, n + 1):
        out = [('not', t) for t in by[s - 1]]
        for i in range(1, s - 1):
            for a in by[i]:
                for b in by[s - 1 - i]:
                    out += [('and', a, b), ('or', a, b)]
        for kind in (0, 1):
            for lvl in (0, 1):
                if s == 3:
                    out += [('box', kind, lvl, 'ME'), ('box', kind, lvl, 'THEM')]
                if s >= 4:
                    out += [('box', kind, lvl, a) for a in by[s - 3]]
        by[s] = out
    return [t for s in range(1, n + 1) for t in by[s]]


def run_ref(n, W=12):
    T = trees(n)
    memo = {}
    def val(p, q, w):          # p's action against q at world w (True = C)
        key = (p, q, w)
        if key in memo: return memo[key]
        def ev(t):
            op = t[0]
            if op == 'C': return True
            if op == 'D': return False
            if op == 'not': return not ev(t[1])
            if op == 'and': return ev(t[1]) and ev(t[2])
            if op == 'or': return ev(t[1]) or ev(t[2])
            kind, lvl, arg = t[1], t[2], t[3]
            other = p if arg == 'ME' else (q if arg == 'THEM' else arg)
            want = (kind == 0)
            return all(val(q, other, m) == want for m in range(lvl, w))
        r = ev(p); memo[key] = r
        return r
    return T, val, W


def test_against_canonical(n=5):
    T, val, W = run_ref(n)
    L = M.ModalLanguage(n)
    V, _ = M.evaluate(L)
    # canonical id of each tree via the language's op table
    def canon(t):
        op = t[0]
        if op in ('C', 'D'): return L.op(op)
        if op == 'not': return L.op('not', canon(t[1]))
        if op in ('and', 'or'): return L.op(op, canon(t[1]), canon(t[2]))
        kind, lvl, arg = t[1], t[2], t[3]
        form = M.TM if arg == 'ME' else (M.TT if arg == 'THEM' else M.TL)
        return L.op((kind, lvl, form), canon(arg) if form == M.TL else None)
    cs = [canon(t) for t in T]
    assert len(T) == L.n_programs
    bad = 0
    for i, p in enumerate(T):
        for j, q in enumerate(T):
            if val(p, q, W) != bool(V[cs[i], cs[j]]):
                bad += 1
    assert bad == 0, bad
    return len(T)


if __name__ == '__main__':
    print('pairs checked for n=5: %d programs, all agree' % test_against_canonical(5))
