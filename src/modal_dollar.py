"""The modal arm on two-player divide-the-dollar, one population (spec specs/2026-10-05-modal-dollar.md, reviewed by
gpt-6.1-sol; predictions predictions/2026-10-05-modal-dollar.md).

Game.  `dollar5` (demands S1..S5 = 1/6..5/6, stored as action indices 0..4; paid iff the two demands sum to <= 1).

Grammar: the two-slot restriction of src/dollar3.py's grammar,

    A ::= a                       5 constants, 1 node
        | if(B, A, A)             1 + |B| + |A| + |A|
    B ::= BOX_L(THEM = a)         3 nodes; a one of the opponent's 5 demands, L in {PA, PA + Con}
        | not B | and B B | or B B

Programs are merged into canonical functions (essential atoms, action table) exactly as in dollar3.Lang; mu of a
canonical function is the sum over its spellings of size <= n of 2^-bits, bits = log2 a(|p|) + 2 log2 |p| + 1.

Two arms share this grammar and this prior (the E1 matched-control design):
  modal  BOX_L is provability in PA (L = 0) or PA + Con(PA) (L = 1) on the linear GL Kripke chain over the encounter
         (dollar3.eval_modal's semantics, restricted to two players: an atom is true at world n iff the opponent
         played a at every world m with L <= m < n; the stable value is the outcome);
  weak   the atom is evaluated by simulating the opponent in the current encounter (budget iteration from bottom,
         dollar3.eval_weak's semantics); the level is ignored (simulation has no levels, so a level-1 atom is the
         level-0 atom: the grammar and the prior stay identical); a program still bottom at the fixed point diverges
         and plays the game's minimax action S1 (games/dollar5.yaml, as in the published weak dollar5 arm).

Classes are payoff-equivalence classes (identical payoff rows and columns), the chain's lumping relation.

    python3 src/modal_dollar.py classes --n 7 11
    python3 src/modal_dollar.py static
    python3 src/modal_dollar.py proofs
    python3 src/modal_dollar.py chain --arm modal weak --n 7 --N 100 1000 ...
"""
import argparse, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'modal_dollar')
os.makedirs(OUT, exist_ok=True)
W = 0.3
K_ACT = 5
SNAME = ['S1', 'S2', 'S3', 'S4', 'S5']
DEM = np.array([1, 2, 3, 4, 5], np.int64)       # demands in sixths
MINIMAX = 0                                      # S1 (games/dollar5.yaml minimax_action)


# ---------------------------------------------------------------- language (two-player restriction of dollar3.Lang)
class Lang2:
    """Canonical functions (atoms tuple sorted, table tuple of own actions over 2^k valuations, bit t = atom t true);
    an abstract atom is (L, a): BOX_L(THEM = S_{a+1})."""

    def __init__(self, n, levels=(0, 1)):
        self.n, self.levels = n, tuple(levels)
        self.atoms = [(L, a) for L in self.levels for a in range(K_ACT)]
        self.cntB = [defaultdict(int) for _ in range(n + 1)]
        self.cntA = [defaultdict(int) for _ in range(n + 1)]
        self._enumerate(n)
        self.a = np.array([0] + [sum(self.cntA[s].values()) for s in range(1, n + 1)], float)

    _reduce = None   # set below (dollar3.Lang._reduce, which is arity-agnostic)
    _expand = None

    def _enumerate(self, n):
        R, E = self._reduce, self._expand
        for a in self.atoms:
            if n >= 3:
                self.cntB[3][((a,), (0, 1))] += 1
        for s in range(4, n + 1):
            for f, m in self.cntB[s - 1].items():
                g = R(f[0], tuple(1 - v for v in f[1])); self.cntB[s][g] += m
            for i in range(3, s - 3):
                j = s - 1 - i
                for fa, ma in self.cntB[i].items():
                    for fb, mb in self.cntB[j].items():
                        U = sorted(set(fa[0]) | set(fb[0]))
                        ta, tb = E(fa, U), E(fb, U)
                        self.cntB[s][R(U, [x & y for x, y in zip(ta, tb)])] += ma * mb
                        self.cntB[s][R(U, [x | y for x, y in zip(ta, tb)])] += ma * mb
        for l in range(K_ACT):
            self.cntA[1][((), (l,))] += 1
        for s in range(2, n + 1):
            for ib in range(3, s - 2):
                for ia in range(1, s - ib - 1):
                    ic = s - 1 - ib - ia
                    if ic < 1: continue
                    for fb, mb in self.cntB[ib].items():
                        for fa, ma in self.cntA[ia].items():
                            for fc, mc in self.cntA[ic].items():
                                U = sorted(set(fb[0]) | set(fa[0]) | set(fc[0]))
                                tb, ta, tc = E(fb, U), E(fa, U), E(fc, U)
                                self.cntA[s][R(U, [x if c else y for c, x, y in zip(tb, ta, tc)])] += mb * ma * mc

    def canon(self, n=None):
        n = self.n if n is None else n
        mu = defaultdict(float); cnt = defaultdict(int); size = {}
        for s in range(1, n + 1):
            if self.a[s] == 0: continue
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for f, m in self.cntA[s].items():
                mu[f] += m * 2.0 ** (-b); cnt[f] += m; size[f] = min(size.get(f, 99), s)
        fs = sorted(mu, key=lambda f: (size[f], len(f[0]), f))
        return fs, np.array([mu[f] for f in fs]), np.array([cnt[f] for f in fs]), np.array([size[f] for f in fs])


from dollar3 import Lang as _L3
Lang2._reduce = staticmethod(_L3._reduce)
Lang2._expand = staticmethod(_L3._expand)


def fsrc(f):
    """readable source of a canonical function."""
    atoms, tab = f
    if not atoms:
        return SNAME[tab[0]]
    def at(t):
        L, a = atoms[t]
        return 'BOX%s(%s)' % ('1' if L else '', SNAME[a])
    if len(atoms) == 1:
        return 'if(%s,%s,%s)' % (at(0), SNAME[tab[1]], SNAME[tab[0]])
    if len(atoms) == 2:
        # table index bit0 = atom0, bit1 = atom1
        return '{%s,%s: TT %s, TF %s, FT %s, FF %s}' % (at(0), at(1), SNAME[tab[3]], SNAME[tab[1]], SNAME[tab[2]], SNAME[tab[0]])
    return 'f%s:%s' % (atoms, tab)


def to_arrays(fs, kmax=2):
    K = len(fs)
    nat = np.zeros(K, np.int64); atL = np.zeros((K, kmax), np.int64); atA = np.zeros((K, kmax), np.int64)
    tab = np.zeros((K, 1 << kmax), np.int64)
    for x, (atoms, t) in enumerate(fs):
        assert len(atoms) <= kmax
        nat[x] = len(atoms)
        for i, (L, a) in enumerate(atoms):
            atL[x, i] = L; atA[x, i] = a
        for v, l in enumerate(t):
            tab[x, v] = l
    return nat, atL, atA, tab


# ---------------------------------------------------------------- evaluators (dollar3's, two players)
VAC, BROKEN = -2, -1


@njit(cache=True)
def eval_modal2(nat, atL, atA, tab, x0, x1, out):
    """Stable actions of (x0, x1) on the linear GL chain; returns the world at which the play stabilized (or -1)."""
    hist = np.full((2, 2), VAC, np.int64)
    val = np.zeros(2, np.int64)
    for n in range(64):
        for s in range(2):
            x = x0 if s == 0 else x1
            idx = 0
            for t in range(nat[x]):
                h = hist[atL[x, t], 1 - s]
                if h == VAC or h == atA[x, t]:
                    idx |= 1 << t
            val[s] = tab[x, idx]
        changed = False
        for L in range(2):
            if n < L:
                continue
            for s in range(2):
                h = hist[L, s]
                if h == VAC:
                    hist[L, s] = val[s]; changed = True
                elif h >= 0 and h != val[s]:
                    hist[L, s] = BROKEN; changed = True
        if not changed and n >= 2:
            out[0] = val[0]; out[1] = val[1]
            return n
    out[0] = -1; out[1] = -1
    return -1


@njit(cache=True)
def eval_weak2(nat, atL, atA, tab, x0, x1, out):
    """Least fixed point by budget iteration from bottom; bottom -> MINIMAX (S1).  Returns 1 if divergent."""
    val = -np.ones(2, np.int64)
    new = np.empty(2, np.int64)
    for it in range(8):
        for s in range(2):
            x = x0 if s == 0 else x1
            k = nat[x]
            if k == 0:
                new[s] = tab[x, 0]; continue
            v = val[1 - s]
            if v < 0:
                new[s] = -1; continue
            idx = 0
            for t in range(k):
                if v == atA[x, t]:
                    idx |= 1 << t
            new[s] = tab[x, idx]
        same = True
        for s in range(2):
            if new[s] != val[s]:
                same = False
            val[s] = new[s]
        if same:
            break
    div = 0
    for s in range(2):
        if val[s] < 0:
            val[s] = 0; div = 1
        out[s] = val[s]
    return div


@njit(cache=True)
def play_matrix(arm, nat, atL, atA, tab):
    """A[i, j] = i's action against j (and the stabilization world / divergence flag)."""
    K = nat.shape[0]
    A = np.empty((K, K), np.int8); S = np.empty((K, K), np.int8)
    out = np.empty(2, np.int64)
    for i in range(K):
        for j in range(i, K):
            if arm == 0:
                st = eval_modal2(nat, atL, atA, tab, i, j, out)
            else:
                st = eval_weak2(nat, atL, atA, tab, i, j, out)
            A[i, j] = out[0]; A[j, i] = out[1]; S[i, j] = st; S[j, i] = st
    return A, S


def payoff_of(Ai, Aj):
    """payoff (in units of the dollar) of action Ai against Aj."""
    di = DEM[Ai]; dj = DEM[Aj]
    return np.where(di + dj <= 6, di / 6.0, 0.0)


# ---------------------------------------------------------------- class data
_DCACHE = {}


def build_lang(n, extra=()):
    """canonical functions of L_n plus `extra` named canonical functions (augmentation; their mass set separately)."""
    L = Lang2(n, (0, 1))
    fs, mu, cnt, size = L.canon()
    return L, list(fs), mu, cnt, size


def data(arm='modal', n=7, aug=None, aug_mass=0.0):
    """class data dict in the shape src/dollar_partitions.py's chain, summary and lottery code expect.
    arm: 'modal' or 'weak'.  aug: list of canonical functions added (if absent) at total syntax mass aug_mass
    (fraction of the final prior, split equally), identical in both arms."""
    key = (arm, n, tuple(aug) if aug else None, aug_mass)
    if key in _DCACHE:
        return _DCACHE[key]
    fpath = os.path.join(OUT, 'classes_%s_n%d%s.npz' % (arm, n, '' if not aug else '_aug%g' % aug_mass))
    L, fs, mu, cnt, size = build_lang(n)
    mu = mu / mu.sum()
    if aug:
        add = [f for f in aug]
        idx = {f: i for i, f in enumerate(fs)}
        mu = mu * (1 - aug_mass)
        for f in add:
            if f in idx:
                mu[idx[f]] += aug_mass / len(add)
            else:
                fs.append(f); mu = np.append(mu, aug_mass / len(add)); size = np.append(size, 99); cnt = np.append(cnt, 0)
                idx[f] = len(fs) - 1
    nat, atL, atA, tab = to_arrays(fs)
    A, St = play_matrix(0 if arm == 'modal' else 1, nat, atL, atA, tab)
    assert (A >= 0).all(), 'unstable modal play'
    # payoff classes: identical rows and columns (payoffs in sixths, int8)
    D8 = DEM.astype(np.int8)
    DA = D8[A]
    Ur = np.where(DA + DA.T <= 6, DA, np.int8(0)).astype(np.int8)
    del DA
    keyrows = {}
    cls_of = np.empty(len(fs), np.int64)
    reps = []
    for i in range(len(fs)):
        k = (Ur[i].tobytes(), Ur[:, i].tobytes())
        c = keyrows.get(k)
        if c is None:
            c = len(reps); keyrows[k] = c; reps.append(i)
        cls_of[i] = c
    K = len(reps)
    members = [[] for _ in range(K)]
    for i in range(len(fs)):
        members[cls_of[i]].append(i)
    cmu = np.array([mu[m].sum() for m in members])
    # representative: the heaviest member (names), but every member checked for an identical joint-action row
    rep = [max(m, key=lambda i: (mu[i], -size[i])) for m in members]
    mixed_actions = 0
    for c, m in enumerate(members):
        r = rep[c]
        for i in m:
            if not (np.array_equal(A[i, rep], A[r, rep]) and np.array_equal(A[rep, i], A[rep, r])):
                mixed_actions += 1; break
    R = np.array(rep)
    U = Ur[np.ix_(R, R)].astype(float) / 6.0
    del Ur
    JA = np.zeros((K, K, K_ACT, K_ACT))
    for a in range(K):
        for b in range(K):
            JA[a, b, A[R[a], R[b]], A[R[b], R[a]]] = 1.0
    names = []
    for c in range(K):
        nm = fsrc(fs[rep[c]])
        names.append(nm)
    kinds = ['constant' if len(fs[rep[c]][0]) == 0 else 'reader' for c in range(K)]
    from dollar_partitions import outcome_of
    values = DEM / 6.0
    self_out = [outcome_of(JA[c, c], values) for c in range(K)]

    class _G:
        actions = SNAME
        k = 5
    d = dict(game=_G(), gname='dollar5', n=n, arm='norole', modal_arm=arm, fs=fs, fmu=mu, fsize=size, cls_of=cls_of, A=A,
             stab=St, K=K, U=U, JA=JA, mu=cmu, names=names, sizes=np.array([len(m) for m in members], float), members=members,
             rep=rep, kinds=kinds, values=values, self_out=self_out, mixed_actions=mixed_actions, n_funcs=len(fs),
             a_counts=L.a.tolist())
    _DCACHE[key] = d
    return d


def find(d, f):
    """class index of canonical function f (atoms tuple, table tuple) in d, or None."""
    try:
        i = d['fs'].index(f)
    except ValueError:
        return None
    return int(d['cls_of'][i])


def act(f, *_):
    return f


# named programs (canonical functions).  Atom (L, a); table bit t = atom t true.
S = {nm: ((), (i,)) for i, nm in enumerate(SNAME)}
def one(L, a, yes, no):
    return (((L, a),), (no, yes))
ACC5 = one(0, 4, 0, 2)              # if(BOX(THEM=S5), S1, S3): the one-atom accommodating shadow (concedes to S5)
PPRIME = one(0, 0, 4, 2)            # P' = if(BOX(THEM=S1), S5, S3) (canonical form of the spec's 11-node spelling)
def two(L1, a1, L2, a2, tt, tf, ft, ff):
    """{atom1, atom2} with atom1 < atom2 in sort order; tt = both true, tf = atom1 true atom2 false, ..."""
    atoms = ((L1, a1), (L2, a2))
    assert atoms[0] < atoms[1]
    return (atoms, (ff, tf, ft, tt))
# P = if(BOX(THEM=S1), S5, if(BOX(THEM=S5), S1, S3)): atoms (0,0) [S1] and (0,4) [S5]
PPROG = two(0, 0, 0, 4, 4, 4, 0, 2)


# ---------------------------------------------------------------- GLS+Def certificates for multi-valued box atoms
import gl_proofs as GP


class Theory5(GP.Theory):
    """GLS+Def (src/gl_proofs.py) with five-valued definitional constants P^a_{xy} = "x demands S_{a+1} against y".
    The definition of P^a_{xy} is x's source read against y: the disjunction, over the atom valuations v with
    table[v] = a, of the conjunction of x's box atoms (true where v says so, negated otherwise); the atom
    BOX_L(THEM = S_b) read against y is [](~[]^L F -> P^b_{yx}).  A constant c: P^a_{cy} is T if a = c else F.
    The definitions of P^0..P^4 for one pair partition the valuations, so 'plays exactly one demand' is propositional
    and needs no axiom."""

    def __init__(self):
        super().__init__()
        self.fun = []            # program id -> canonical function
        self.fun_id = {}

    def prog(self, f):
        i = self.fun_id.get(f)
        if i is None:
            i = len(self.fun); self.fun_id[f] = i; self.fun.append(f)
        return i

    def P(self, x, y, a=None):
        return self.f((GP.FP, x, y, a))

    def atom(self, x, y, t):
        L, b = self.fun[x][0][t]
        s = self.P(y, x, b)
        if L: s = self.con_guard(L, s)
        return self.box(s)

    def phi(self, x, y, a):
        atoms, tab = self.fun[x]
        k = len(atoms)
        disj = []
        for v in range(1 << k):
            if tab[v] != a: continue
            lits = []
            for t in range(k):
                at = self.atom(x, y, t)
                lits.append(at if (v >> t) & 1 else self.neg(at))
            if not lits:
                c = self.TOP
            else:
                c = lits[0]
                for l in lits[1:]:
                    c = self.f((GP.FAND, c, l))
            disj.append(c)
        if not disj:
            return self.BOT
        out = disj[0]
        for c in disj[1:]:
            out = self.f((GP.FOR, out, c))
        return out

    def unfold(self, pf):
        d = self.defn.get(pf)
        if d is None:
            _, x, y, a = self.forms[pf]
            d = self.phi(x, y, a); self.defn[pf] = d
        return d

    def show(self, i, names=None):
        t = self.forms[i]
        if t[0] == GP.FP:
            nm = names or {}
            return 'P%s[%s,%s]' % (SNAME[t[3]], nm.get(t[1], 'p%d' % t[1]), nm.get(t[2], 'p%d' % t[2]))
        k = t[0]
        if k == GP.FBOT: return 'F'
        if k == GP.FTOP: return 'T'
        if k == GP.FNOT: return '~' + self.show(t[1], names)
        if k == GP.FBOX: return '[]' + self.show(t[1], names)
        return '(%s %s %s)' % (self.show(t[1], names), GP.KNAME[k], self.show(t[2], names))


def atom_root(th, x, y, t):
    """the provability root of x's atom t read against y: |- P^b_{yx} (L = 0) or |- ~[]F -> P^b_{yx} (L = 1)."""
    L, b = th.fun[x][0][t]
    p = th.P(y, x, b)
    if L:
        p = th.con_guard(L, p)
    return (frozenset(), frozenset([p]))


def certify_pair(th, fx, fy, ms=None, want_render=False, names=None, minimize=True):
    """For the encounter (fx, fy): every box atom of each side, its GLS+Def provability (decision procedure), and for
    provable atoms a certified minimal derivation (size, Loeb count).  Returns the plays implied by provability (the
    stable-world plays: an atom is true in the standard model iff it is provable) and the certificates."""
    x = th.prog(fx); y = th.prog(fy)
    ms = ms or GP.MinSearch(th)
    out = dict(sides=[])
    plays = []
    for me, op in ((x, y), (y, x)):
        atoms, tab = th.fun[me]
        idx = 0; recs = []
        for t in range(len(atoms)):
            root = atom_root(th, me, op, t)
            pv = ms.oracle.prov(root)
            rec = dict(atom='BOX%s(THEM=%s)' % ('1' if atoms[t][0] else '', SNAME[atoms[t][1]]), provable=bool(pv))
            if pv:
                idx |= 1 << t
                if minimize:
                    r = ms.minimize(root)
                    rec.update(size=r['c'][0], loeb=r['c'][1], certified=r['certified'])
                    if want_render and r['certified']:
                        rec['derivation'] = ms.render(root, names)
            recs.append(rec)
        plays.append(tab[idx])
        out['sides'].append(recs)
    out['plays'] = [SNAME[p] for p in plays]
    out['play_idx'] = plays
    return out


# ---------------------------------------------------------------- static checkpoint
def make_chain(d, N, theta=1e-7, **kw):
    from chain import Chain
    from dollar_partitions import ClassProvider
    prov = ClassProvider(d['U'], d['mu'])
    return Chain(prov, N=N, w=W, theta=theta, **kw), prov


def exits_of(d, ch, key):
    """expand a state and return its per-mutant exits: list of dict(mutant, target, rho, flow = mu*rho, kind)."""
    ch.expand(key)
    ids, x, kind = ch.states[key]
    out = []
    for (k1, k2, q), (rho, kstar, tk) in ch.edge_rho.items():
        if k1 != key: continue
        out.append(dict(q=int(q), target=k2, rho=float(rho), flow=float(d['mu'][q] * rho), kstar=kstar, tkind=tk))
    return out


def state_desc(d, ch, key):
    ids, x, kind = ch.states[key]
    return ' + '.join('%s:%.3f' % (d['names'][i], xi) for i, xi in zip(ids, x))


def poly_state(d, ch, ids, x0=None):
    """rest point of the replicator on the classes ids (from x0, default uniform), as a chain state key."""
    from chain import replicator
    ids = np.asarray(ids)
    Us = d['U'][np.ix_(ids, ids)]
    x0 = np.ones(len(ids)) / len(ids) if x0 is None else np.asarray(x0, float)
    xf, st, _, _ = replicator(Us, x0, rest_tol=1e-10)
    return ch.add_state(ids, xf), xf, st


def classify_exit(d, src_ids, src_x, q):
    """strict / neutral / deleterious at first order for mutant q against the resident mix."""
    ids = np.asarray(src_ids); x = np.asarray(src_x)
    uqa = d['U'][q, ids] @ x
    uaa = x @ d['U'][np.ix_(ids, ids)] @ x
    if uqa > uaa + 1e-9: return 'strict', float(uqa - uaa)
    if uqa < uaa - 1e-9: return 'deleterious', float(uqa - uaa)
    return 'neutral', 0.0


def self_eff(d, c):
    return abs(d['U'][c, c] - 0.5) < 1e-9


def static_checkpoint(arm, n=7, Ns=(1000, 10000), aug=(PPROG,), aug_mass=1e-4):
    """The spec's static go/no-go table.  P (two atoms, minimal spelling 11 nodes) is added to L_7 as a named class at
    a token mass so that its invasion numbers exist; rho does not depend on its mass."""
    from dollar_partitions import rho1
    from chain import fixation
    d = data(arm, n, aug=list(aug), aug_mass=aug_mass)
    U, mu, nm, K = d['U'], d['mu'], d['names'], d['K']
    s5 = find(d, S['S5']); a5 = find(d, ACC5)
    cands = [c for c in range(K) if self_eff(d, c)]
    res = dict(arm=arm, n=n, K=K, n_funcs=d['n_funcs'], n_self_efficient=len(cands), mass_self_efficient=float(mu[cands].sum()),
               named=dict(S3=find(d, S['S3']), S5=s5, A5=a5, Pprime=find(d, PPRIME), P=find(d, PPROG)), names=nm, mu=mu.tolist())
    rows = []
    gpoly = {}
    for N in Ns:
        ch, _ = make_chain(d, N)
        gkey, gx, gst = poly_state(d, ch, [s5, a5], [0.5, 0.5])
        gids, gxx, _ = ch.states[gkey]
        gids = list(gids); gxx = np.array(gxx)
        gmean = float(gxx @ U[np.ix_(gids, gids)] @ gxx)
        gex = exits_of(d, ch, gkey)
        gpoly[N] = dict(state=state_desc(d, ch, gkey), mean=gmean, exits=[dict(q=nm[e['q']], rho=e['rho'], flow=e['flow'],
                        target=state_desc(d, ch, e['target']), target_self_eff=all(self_eff(d, i) for i in ch.states[e['target']][0]) and len(ch.states[e['target']][0]) == 1,
                        first_order=classify_exit(d, gids, gxx, e['q'])) for e in sorted(gex, key=lambda e: -e['flow'])[:40]])
        gpoly[N]['reentry_flow_efficient'] = float(sum(e['flow'] for e in gex if len(ch.states[e['target']][0]) == 1 and self_eff(d, ch.states[e['target']][0][0])))
        gpoly[N]['total_exit_flow'] = float(sum(e['flow'] for e in gex))
        rho_in = {}
        for e in gex:
            rho_in[e['q']] = e
        for c in cands:
            key = ch.mono(c)
            ex = exits_of(d, ch, key)
            agg = defaultdict(float)
            for e in ex:
                agg[classify_exit(d, [c], [1.0], e['q'])[0]] += e['flow']
            # constants
            consts = []
            for i, snm in enumerate(SNAME):
                q = find(d, S[snm])
                if q == c: continue
                consts.append(dict(c=snm, u_qE=float(U[q, c]), u_Eq=float(U[c, q]), u_qq=float(U[q, q]),
                                   kind=classify_exit(d, [c], [1.0], q)[0], rho=float(rho1(U, q, c, N))))
            # neutral neighbours and the strict invaders of each (two-step exits)
            neigh = [q for q in range(K) if q != c and abs(U[q, c] - .5) < 1e-9 and abs(U[c, q] - .5) < 1e-9 and abs(U[q, q] - .5) < 1e-9]
            two = defaultdict(float)
            for q in neigh:
                kq = ch.mono(q)
                exq = exits_of(d, ch, kq)
                totq = sum(e['flow'] for e in exq)
                for e in exq:
                    if classify_exit(d, [q], [1.0], e['q'])[0] == 'strict':
                        tg = ch.states[e['target']][0]
                        lab = 'efficient' if (len(tg) == 1 and self_eff(d, tg[0])) else 'inefficient'
                        two[lab] += mu[q] / N * e['flow'] / totq
            gi = rho_in.get(c)
            row = dict(N=N, cls=c, name=nm[c], mu=float(mu[c]), exits=dict(agg), consts=consts,
                       strict_const_invaders=[x['c'] for x in consts if x['kind'] == 'strict'],
                       n_neutral=len(neigh), neutral_mass=float(mu[neigh].sum()), two_step=dict(two),
                       u_vs_G=float(U[c, gids] @ gxx), G_mean=gmean, u_vs_G_weakcomp=float(U[c, s5] * 0.8 + U[c, a5] * 0.2),
                       G_mean_weakcomp=float(np.array([.8, .2]) @ U[np.ix_([s5, a5], [s5, a5])] @ np.array([.8, .2])),
                       rho_into_G=(gi['rho'] if gi else None), target_from_G=(state_desc(d, ch, gi['target']) if gi else None),
                       rho_neutral=1.0 / N)
            rows.append(row)
    res['rows'] = rows
    res['G'] = gpoly
    return res, d


def audit(fs, pairs, th=None):
    """GLS+Def provability of every box atom in each encounter against the evaluator's stable plays.  Returns
    (n_pairs, n_atoms checked, disagreements list)."""
    th = th or Theory5()
    ms = GP.MinSearch(th)
    nat, atL, atA, tab = to_arrays(fs)
    out = np.zeros(2, np.int64)
    bad = []; natoms = 0
    for i, j in pairs:
        eval_modal2(nat, atL, atA, tab, i, j, out)
        r = certify_pair(th, fs[i], fs[j], ms=ms, minimize=False)
        natoms += len(fs[i][0]) + len(fs[j][0])
        if r['play_idx'][0] != out[0] or r['play_idx'][1] != out[1]:
            bad.append((i, j, r['plays'], [SNAME[o] for o in out]))
    return len(pairs), natoms, bad


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--n', type=int, nargs='+', default=[7])
    ap.add_argument('--arm', nargs='+', default=['modal', 'weak'])
    a = ap.parse_args()
    if a.cmd == 'classes':
        for n in a.n:
            for arm in a.arm:
                t0 = time.time()
                d = data(arm, n)
                print('%s n=%d: a(s)=%s, %d canonical functions, %d payoff classes, classes with mixed joint actions %d (%.1fs)' % (
                    arm, n, [int(x) for x in d['a_counts']], d['n_funcs'], d['K'], d['mixed_actions'], time.time() - t0), flush=True)
