"""Independent pure-python scalar evaluator of the inspection-game programs (the semantics of notes/mixed2.md
plus the added inspector operators of notes/zero-tolerance.md section 1.0), one program pair at a time.  The reference of tests/test_zero_tolerance.py."""
import os, sys, functools, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import mixed2 as M

D = 12
PAY0 = np.array([[-1, -1], [0, -4]], float)       # inspector action x (I=0,N=1), inspectee y (C=0,K=1)
PAY1 = np.array([[0, -3], [0, 1]], float)         # [inspector action][inspectee action] -> inspectee payoff
T, FI0, FI1, FII0, FII1, FF = M.game_tensors('insp')
TIE = 1e-9

# AST: ('c0',) ('c1',) ('x',) ('coin', a, b) ('cr', a) ('zt', a) ('crs', a) ('zts', a) ('sr', k, a) ('srs', k, a)
#      ('if', Q, a, b) ('me',) ('up', B)
C0, C1, X = ('c0',), ('c1',), ('x',)
ME = ('me',)


def coin(a, b): return ('coin', a, b)
def cr(a): return ('cr', a)
def zt(a): return ('zt', a)
def crs(a): return ('crs', a)
def zts(a): return ('zts', a)
def sr(k, a): return ('sr', k, a)
def srs(k, a): return ('srs', k, a)
def ife(Q, a, b): return ('if', Q, a, b)
def up(B): return ('up', B)


def _br(tp, m0, m1, z):
    """conditional best response of a type-tp responder to a child distribution (m0, m1) with non-forfeit mass z: (P(act0), P(act1))."""
    u = []
    for a in range(2):
        u.append((m0 * T[tp, 0, a, 0, 0] + m1 * T[tp, 0, a, 0, 1]) / z)
    if abs(u[0] - u[1]) <= TIE:
        return 0.5, 0.5
    return (1.0, 0.0) if u[0] > u[1] else (0.0, 1.0)


@functools.lru_cache(maxsize=None)
def V(r, P, Q, d):
    """value (p0, p1, pf), expected cost E and depth M of program P (context role r) against Q (role 1 - r) at level d."""
    return _ev(r, P, P, Q, d, r)


def _ev(r, node, root, Q, d, t):
    o = node[0]
    if o == 'c0': return (1.0, 0.0, 0.0), 0.0, 0.0
    if o == 'c1': return (0.0, 1.0, 0.0), 0.0, 0.0
    if o == 'x': return (0.5, 0.5, 0.0), 0.0, 0.0
    if o == 'coin':
        a, ea, ma = _ev(r, node[1], root, Q, d, t); b, eb, mb = _ev(r, node[2], root, Q, d, t)
        return tuple(0.5 * (a[i] + b[i]) for i in range(3)), 0.5 * (ea + eb), max(ma, mb)
    if o in ('me', 'up'):
        if d == 0: return (0.0, 0.0, 1.0), 0.0, 0.0
        arg = root if o == 'me' else node[1]
        v, e, m = V(1 - r, Q, arg, d - 1)
        return v, 1.0 + e, 1.0 + m
    if o == 'if':
        q, eq, mq = _ev(r, node[1], root, Q, d, 1 - r)
        x, ex, mx = _ev(r, node[2], root, Q, d, t); y, ey, my = _ev(r, node[3], root, Q, d, t)
        p0, p1, pf = q
        v = (p0 * x[0] + p1 * y[0], p0 * x[1] + p1 * y[1], p0 * x[2] + p1 * y[2] + pf)
        return v, eq + p0 * ex + p1 * ey, mq + max(mx, my)
    # unary readers: responder of type r reads the child (type 1 - r)
    k = node[1] if o in ('sr', 'srs') else 0
    child = node[2] if o in ('sr', 'srs') else node[1]
    x, ex, mx = _ev(r, child, root, Q, d, 1 - t)
    m0, m1, pf = x
    z = 1.0 - pf
    if o in ('cr', 'zt', 'crs', 'zts'):
        susp = o in ('crs', 'zts')
        if z < 1e-15:
            v = (1.0, 0.0, 0.0) if susp else (0.0, 0.0, 1.0)      # suspicious: the default I; else forfeit
            
        else:
            if o in ('zt', 'zts'):
                q = m1 / z
                p0, p1 = (1.0, 0.0) if q > 1e-12 else (0.0, 1.0)      # inspector only
            else:
                p0, p1 = _br(t, m0, m1, z)
            if susp:
                v = (z * p0 + pf, z * p1, 0.0)
            else:
                v = (z * p0, z * p1, pf)
        return v, mx, mx
    if o in ('sr', 'srs'):
        pc = m0                      # compliant (completed) draw
        if abs(1.0 - pc) < 1e-15:
            nreads = float(k); PI = 0.0; PF = 0.0
        else:
            geo = (1.0 - pc ** k) / (1.0 - pc)
            nreads = geo
            PI = m1 * geo; PF = pf * geo
        PN = pc ** k
        if o == 'srs':
            v = (PI + PF, PN, 0.0)
        else:
            v = (PI, PN, PF)
        return v, ex * nreads, k * mx
    raise ValueError(node)


def payoffs(P, Q):
    """game payoffs (u0, u1) with the forfeit convention, forfeit probabilities, expected costs, for inspector P vs inspectee Q at level D."""
    g0, e0, _ = V(0, P, Q, D)
    g1, e1, _ = V(1, Q, P, D)
    u0 = u1 = 0.0
    f0, f1 = g0[2], g1[2]
    for x in range(2):
        for y in range(2):
            u0 += g0[x] * g1[y] * PAY0[x, y]; u1 += g0[x] * g1[y] * PAY1[x, y]
        u0 += g0[x] * f1 * FII0[0, x]; u1 += g0[x] * f1 * FII1[0, x]
    for y in range(2):
        u0 += f0 * g1[y] * FI0[0, y]; u1 += f0 * g1[y] * FI1[0, y]
    u0 += f0 * f1 * FF[0]; u1 += f0 * f1 * FF[1]
    return dict(u0=u0, u1=u1, g0=g0, g1=g1, f0=f0, f1=f1, e0=e0, e1=e1)


def name(P):
    o = P[0]
    if o == 'c0': return 'I/C'
    if o == 'c1': return 'N/K'
    if o == 'x': return 'X'
    if o == 'me': return 'THEM(ME)'
    if o == 'up': return 'THEM(^%s)' % name(P[1])
    if o == 'coin': return 'coin(%s,%s)' % (name(P[1]), name(P[2]))
    if o == 'if': return 'if(%s,%s,%s)' % (name(P[1]), name(P[2]), name(P[3]))
    if o in ('sr', 'srs'): return '%s%d(%s)' % (o, P[1], name(P[2]))
    return '%s(%s)' % (o, name(P[1]))
