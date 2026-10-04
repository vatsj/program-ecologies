"""Conjecture 4 (THEORY §9.2): an independent trace evaluator for single modal programs, and the sibling
construction of notes/conjecture4.md checked against it and against src/modal_lv.py.

Programs are parsed from the evaluator's source syntax: C, D, not(A), and(A,B), or(A,B), BOX[L](App), BOXD[L](App)
with App = THEM(ME) | THEM(THEM) | THEM(^A).  BOX_L(p plays C vs q) holds at world n iff p plays C against q at every
world m with L <= m < n (src/modal_lv.py).  The stable value is the outcome.

    python3 src/conj4.py        (prints the checks; used by runs/conjecture4.md)
"""
import re, sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def parse(s):
    s = s.replace(' ', '')
    pos = [0]

    def expr():
        if s.startswith('not(', pos[0]):
            pos[0] += 4; a = expr(); eat(')'); return ('not', a)
        for op in ('and', 'or'):
            if s.startswith(op + '(', pos[0]):
                pos[0] += len(op) + 1; a = expr(); eat(','); b = expr(); eat(')'); return (op, a, b)
        m = re.compile(r'BOX(D?)(\d*)\(THEM\(').match(s, pos[0])
        if m:
            pos[0] = m.end(); kind = 1 if m.group(1) else 0; lev = int(m.group(2) or 0)
            if s.startswith('ME))', pos[0]):
                pos[0] += 4; return ('box', kind, lev, 'ME', None)
            if s.startswith('THEM))', pos[0]):
                pos[0] += 6; return ('box', kind, lev, 'THEM', None)
            eat('^'); a = expr(); eat('))'); return ('box', kind, lev, 'ARG', a)
        if s.startswith('C', pos[0]):
            pos[0] += 1; return ('C',)
        if s.startswith('D', pos[0]):
            pos[0] += 1; return ('D',)
        raise ValueError('parse error at %d in %s' % (pos[0], s))

    def eat(t):
        if not s.startswith(t, pos[0]):
            raise ValueError('expected %r at %d in %s' % (t, pos[0], s))
        pos[0] += len(t)
    out = expr()
    assert pos[0] == len(s), s
    return out


def src(p):
    t = p[0]
    if t in ('C', 'D'): return t
    if t == 'not': return 'not(%s)' % src(p[1])
    if t in ('and', 'or'): return '%s(%s,%s)' % (t, src(p[1]), src(p[2]))
    _, kind, lev, form, arg = p
    inner = {'ME': 'THEM(ME)', 'THEM': 'THEM(THEM)'}.get(form) or 'THEM(^%s)' % src(arg)
    return 'BOX%s%s(%s)' % ('D' if kind else '', lev if lev else '', inner)


def size(p):
    t = p[0]
    if t in ('C', 'D'): return 1
    if t == 'not': return 1 + size(p[1])
    if t in ('and', 'or'): return 1 + size(p[1]) + size(p[2])
    return 3 + (size(p[4]) if p[3] == 'ARG' else 0)


def args(p, acc=None):
    """F(p): p and every fixed argument inside it, recursively."""
    if acc is None: acc = set()
    if p in acc: return acc
    acc.add(p)

    def walk(f):
        t = f[0]
        if t == 'not': walk(f[1])
        elif t in ('and', 'or'): walk(f[1]); walk(f[2])
        elif t == 'box' and f[3] == 'ARG': args(f[4], acc)
    walk(p)
    return acc


@lru_cache(maxsize=None)
def play(p, q, n):
    """1 if p plays C against q at world n."""
    def ev(f):
        t = f[0]
        if t == 'C': return 1
        if t == 'D': return 0
        if t == 'not': return 1 - ev(f[1])
        if t == 'and': return ev(f[1]) and ev(f[2])
        if t == 'or': return ev(f[1]) or ev(f[2])
        _, kind, lev, form, arg = f
        a, b = (q, p) if form == 'ME' else (q, q) if form == 'THEM' else (q, arg)
        want = 0 if kind else 1
        return int(all(play(a, b, m) == want for m in range(lev, n)))
    return ev(p)


def trace(p, q, W=40):
    return [play(p, q, m) for m in range(W)]


def stable(p, q, W=40):
    t = trace(p, q, W)
    assert len(set(t[W // 2:])) == 1, ('not settled by world %d' % (W // 2), src(p), src(q), t)
    return t[-1]


def settle(p, q, W=40):
    t = trace(p, q, W); s = W - 1
    while s > 0 and t[s - 1] == t[-1]: s -= 1
    assert s < W // 2
    return s


D_ = ('D',)


def sibling(x, W=40):
    """y = or(x, psi_K), z = BOX_K(THEM(^D)), K = max settle(P, D) over P in F(x)."""
    K = max(settle(P, D_, W) for P in args(x))
    psi = parse('and(not(BOX{0}(THEM(^D))),not(BOXD{0}(THEM(^D))))'.format(K if K else ''))
    y = ('or', x, psi)
    z = parse('BOX{0}(THEM(^D))'.format(K if K else ''))
    return K, y, z


def check(xsrc, W=40):
    x = parse(xsrc)
    r = dict(x=xsrc, size=size(x), self_coop=stable(x, x, W), coop_D=stable(x, D_, W))
    if not r['self_coop']:
        r['note'] = 'not self-cooperating'; return r
    if r['coop_D']:
        r['note'] = 'suckerable by D (distance 0)'; return r
    K, y, z = sibling(x, W)
    r.update(K=K, y=src(y), y_size=size(y), z=src(z),
             y_vs_x=stable(y, x, W), x_vs_y=stable(x, y, W), y_vs_y=stable(y, y, W),
             y_vs_z=stable(y, z, W), z_vs_y=stable(z, y, W),
             mimic=all(trace(y, P, W) == trace(x, P, W) and trace(P, y, W) == trace(P, x, W)
                       for P in args(x) | {D_}) and trace(y, y, W) == trace(x, x, W))
    r['ok'] = bool(r['y_vs_x'] and r['x_vs_y'] and r['y_vs_y'] and r['y_vs_z'] and not r['z_vs_y'] and r['mimic'])
    return r


CASES = [
    'BOX(THEM(ME))',                                            # FairBot
    'BOX1(THEM(ME))',
    'and(BOX(THEM(ME)),BOXD1(THEM(^D)))',                       # PrudentBot
    'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))',                   # P*
    'and(BOX1(THEM(ME)),not(BOX(THEM(^C))))',                   # P2
    'and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))',   # P12b
    'and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))',   # P*1b
    'and(and(BOX2(THEM(ME)),not(BOX1(THEM(^C)))),BOXD2(THEM(^D)))',  # P2D2
    'and(BOX(THEM(ME)),BOXD2(THEM(^D)))',                       # PB2
    'BOX(THEM(THEM))',
    'C',
]

# ---------------------------------------------------------------- cross-check against src/modal_lv.py
def max_level(p):
    t = p[0]
    if t in ('C', 'D'): return -1
    if t == 'not': return max_level(p[1])
    if t in ('and', 'or'): return max(max_level(p[1]), max_level(p[2]))
    return max(p[2], max_level(p[4]) if p[3] == 'ARG' else -1)


def to_op(L, p):
    import modal as M
    t = p[0]
    if t in ('C', 'D'): return L.op(t)
    if t == 'not': return L.op('not', to_op(L, p[1]))
    if t in ('and', 'or'): return L.op(t, to_op(L, p[1]), to_op(L, p[2]))
    _, kind, lev, form, arg = p
    f = {'ME': M.TM, 'THEM': M.TT, 'ARG': M.TL}[form]
    return L.op((kind, lev, f), to_op(L, arg) if form == 'ARG' else None)


def crosscheck(n, lmax, W=40, sample=3000, seed=0):
    """Every self-cooperating class of L_n (boxes up to level lmax): build its sibling and faker, add them to the
    modal_lv language, evaluate everything with modal_lv, and check (a) the sibling property there, (b) agreement of
    this file's evaluator with modal_lv on a random sample of pairs."""
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import numpy as np, modal as M, modal_lv as LV
    kinds = tuple((k, l) for l in range(lmax + 1) for k in (M.KC, M.KD))
    L = LV.ModalLanguageLv(n, kinds)
    K0 = len(L.funcs)
    reps = {c: parse(L.rep[c]) for c in range(K0) if L.count_canon[c] > 0}
    sc = [c for c, p in reps.items() if stable(p, p, W) == 1]
    jobs = []
    for c in sc:
        x = reps[c]
        if stable(x, D_, W):
            jobs.append((c, None, None, None)); continue
        K, y, z = sibling(x, W)
        jobs.append((c, K, to_op(L, y), to_op(L, z)))
    nlev = max(L.atoms[a][1] for a in range(len(L.atoms))) + 1
    val, worlds = LV._evaluate_lv(*L.arrays(), nlev, 400)
    assert worlds >= 0
    iD = L.op('D')
    bad = []; Ks = []
    for c, K, cy, cz in jobs:
        if K is None:
            ok = val[c, iD] == 1
        else:
            Ks.append(K)
            ok = val[cy, c] == 1 and val[c, cy] == 1 and val[cy, cy] == 1 and val[cy, cz] == 1 and val[cz, cy] == 0
        if not ok: bad.append(L.rep[c])
    rng = np.random.default_rng(seed); cl = list(reps); dis = 0
    for _ in range(sample):
        a, b = rng.choice(cl, 2)
        if stable(reps[a], reps[b], W) != val[a, b]: dis += 1
    return dict(n=n, lmax=lmax, classes=len(reps), self_coop=len(sc), coop_D=sum(1 for j in jobs if j[1] is None),
                K_hist={k: Ks.count(k) for k in sorted(set(Ks))}, n_fail=len(bad), failures=bad[:10],
                sample=sample, disagreements=dis)


if __name__ == '__main__':
    for c in CASES:
        print(check(c))
    for n, lmax in [(int(a.split('/')[0]), int(a.split('/')[1])) for a in sys.argv[1:]]:
        print(crosscheck(n, lmax), flush=True)
