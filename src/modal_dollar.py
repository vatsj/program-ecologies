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
PPRIME_1 = one(1, 0, 4, 2)          # the PA + Con twins ("policy duplicates")
PPROG_1 = two(1, 0, 1, 4, 4, 4, 0, 2)


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


# ---------------------------------------------------------------- chains
def state_sets(d, ch):
    """per expanded state: efficient (>= 0.99 of encounters efficient), greedy (polymorphic with S5 >= 0.5), label."""
    from dollar_partitions import pop_outcome, label_of
    s5 = find(d, S['S5'])
    info = {}
    for key in ch.keys_list:
        ids, x, kind = ch.states[key]
        cnt = np.round(np.asarray(x) * ch.N).astype(int)
        o = pop_outcome(d, ids, cnt)
        xs5 = dict(zip(ids, x)).get(s5, 0.0)
        info[key] = dict(eff=o['eff'], effset=o['eff'] >= 0.99, greedy=(len(ids) > 1 and xs5 >= 0.5), label=label_of(o), xs5=xs5)
    return info


def set_rates(ch, info, which):
    """exit rate (per mutation event, from inside the set) and entry rate (per event, from outside) of a set of states."""
    pin = 0.0; pout = 0.0; fout = 0.0; fin = 0.0
    for key, p in zip(ch.keys_list, ch.pi):
        inside = info[key][which]
        if inside: pin += p
        else: pout += p
        for k2, pr in ch.trans[key].items():
            if k2 == key or k2 not in info: continue
            if inside and not info[k2][which]: fout += p * pr
            if not inside and info[k2][which]: fin += p * pr
    return dict(mass=pin, exit_rate=fout / pin if pin > 0 else None, entry_rate=fin / pout if pout > 0 else None, flux_out=fout, flux_in=fin)


def flux_by_mutant(d, ch, info, src_pred, dst_pred, top=12):
    """stationary flux from states satisfying src_pred to states satisfying dst_pred, decomposed by mutant class."""
    acc = defaultdict(float); tot = 0.0
    for key, p in zip(ch.keys_list, ch.pi):
        if not src_pred(info[key]): continue
        for k2, pr in ch.trans[key].items():
            if k2 == key or k2 not in info or not dst_pred(info[k2]): continue
            for q, v in ch.trans_mut[(key, k2)].items():
                acc[q] += p * v; tot += p * v
    rows = sorted(acc.items(), key=lambda kv: -kv[1])[:top]
    return dict(total=tot, by_mutant=[dict(q=d['names'][int(q)], flux=float(f), share=float(f / tot) if tot > 0 else 0.0) for q, f in rows])


def run_chain(arm, n, N, theta, aug=None, aug_mass=0.0, d=None, tag=''):
    from dollar_partitions import onepop_summary
    t0 = time.time()
    if d is None:
        d = data(arm, n, aug=aug, aug_mass=aug_mass)
    ch, prov = make_chain(d, N, theta=theta, max_states=30000, eager_poly=False)
    ch.explore()
    r = onepop_summary(d, ch, top=20)
    info = state_sets(d, ch)
    r['P_efficient'] = r['outcome']['eff']
    r['effset'] = set_rates(ch, info, 'effset')
    r['greedy'] = set_rates(ch, info, 'greedy')
    r['reentry_greedy_to_eff'] = flux_by_mutant(d, ch, info, lambda i: i['greedy'], lambda i: i['effset'])
    r['exit_eff_to_any'] = flux_by_mutant(d, ch, info, lambda i: i['effset'], lambda i: not i['effset'])
    r['exit_eff_to_greedy'] = flux_by_mutant(d, ch, info, lambda i: i['effset'], lambda i: i['greedy'])
    # top states with their efficient/greedy flags
    r['top_states'] = [dict(state=state_desc(d, ch, ch.keys_list[i]), pi=float(ch.pi[i]), **{k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k, v in info[ch.keys_list[i]].items()})
                       for i in np.argsort(-ch.pi)[:20]]
    r.update(arm=arm, n=n, N=N, theta=theta, K=d['K'], aug_mass=aug_mass, aug=[fsrc(f) for f in (aug or [])], time_s=time.time() - t0,
             n_expanded=len(ch.trans), tag=tag)
    return r, ch, d


def subdata(d, funcs):
    """the class data restricted to the classes of the given canonical functions (masses renormalized)."""
    cls = [find(d, f) for f in funcs]
    assert len(set(cls)) == len(cls), 'two named programs share a class'
    c = np.array(cls)
    sd = dict(d)
    sd['U'] = d['U'][np.ix_(c, c)]; sd['JA'] = d['JA'][np.ix_(c, c)]
    sd['mu'] = d['mu'][c] / d['mu'][c].sum()
    sd['names'] = [d['names'][i] for i in c]; sd['kinds'] = [d['kinds'][i] for i in c]
    sd['self_out'] = [d['self_out'][i] for i in c]; sd['K'] = len(c)
    sd['sizes'] = d['sizes'][c]; sd['members'] = [d['members'][i] for i in c]
    sd['fs'] = [d['fs'][d['rep'][i]] for i in c]; sd['cls_of'] = np.arange(len(c)); sd['rep'] = list(range(len(c)))
    return sd


def _job_chain(job):
    r, ch, d = run_chain(job['arm'], job['n'], job['N'], job['theta'], aug=job.get('aug'), aug_mass=job.get('aug_mass', 0.0), tag=job.get('tag', ''))
    fn = os.path.join(OUT, 'chain_%s_n%d_N%d_th%g%s.json' % (job['arm'], job['n'], job['N'], job['theta'], job.get('tag', '')))
    json.dump(r, open(fn, 'w'), indent=1, default=str)
    return dict(fn=fn, arm=job['arm'], N=job['N'], theta=job['theta'], tag=job.get('tag', ''), P_eff=r['P_efficient'],
                greedy=r['greedy']['mass'], effset=r['effset']['mass'], time_s=r['time_s'], cut=r['cut_flow'])


# ---------------------------------------------------------------- log-domain chain (closure of every reachable state)
@njit(cache=True)
def log_fixation(uqq, uqa, uaq, uaa, N, w, kstar):
    """log of chain.fixation (same formula), without underflow."""
    if kstar <= 1:
        return 0.0
    acc = 0.0; lmax = -1e300
    logs = np.empty(kstar - 1)
    for k in range(1, kstar):
        pq = (k - 1) / (N - 1) * uqq + (N - k) / (N - 1) * uqa
        pa = k / (N - 1) * uaq + (N - k - 1) / (N - 1) * uaa
        acc += w * (pa - pq)
        logs[k - 1] = acc
        if acc > lmax: lmax = acc
    ssum = 0.0
    for k in range(kstar - 1):
        ssum += np.exp(logs[k] - lmax)
    ls = lmax + np.log(ssum)
    if ls > 0:
        return -(ls + np.log1p(np.exp(-ls)))
    return -np.log1p(np.exp(ls))


@njit(cache=True)
def _lae(a, b):
    if a == -np.inf: return b
    if b == -np.inf: return a
    if a > b: return a + np.log1p(np.exp(b - a))
    return b + np.log1p(np.exp(a - b))


@njit(cache=True)
def gth_log(LA):
    """stationary distribution (log) of a chain with log off-diagonal weights LA (n x n, -inf = no edge), by GTH in
    the log domain (GTH has no subtractions, so log-sum-exp is exact up to rounding).  Row k is eliminated from n-1
    down; rows with an edge into k are updated."""
    n = LA.shape[0]
    A = LA.copy()
    for i in range(n):
        A[i, i] = -np.inf
    s = np.full(n, -np.inf)
    for k in range(n - 1, 0, -1):
        sk = -np.inf
        for j in range(k):
            sk = _lae(sk, A[k, j])
        if sk == -np.inf:
            sk = -1e300
        s[k] = sk
        for i in range(k):
            aik = A[i, k]
            if aik == -np.inf:
                continue
            f = aik - sk
            for j in range(k):
                if A[k, j] != -np.inf:
                    A[i, j] = _lae(A[i, j], f + A[k, j])
    x = np.full(n, -np.inf)
    x[0] = 0.0
    for k in range(1, n):
        v = -np.inf
        for i in range(k):
            if A[i, k] != -np.inf:
                v = _lae(v, x[i] + A[i, k])
        x[k] = v - s[k]
    m = x.max()
    return x - m


def twin_of(U, ids, q):
    """the resident r of the support ids of which q is a payoff twin (same payoffs against every other resident, in
    both directions, and U[q,q] = U[q,r] = U[r,q] = U[r,r]), or None."""
    for r in ids:
        if q == r: continue
        if not (abs(U[q, q] - U[r, r]) < 1e-9 and abs(U[q, r] - U[r, r]) < 1e-9 and abs(U[r, q] - U[r, r]) < 1e-9):
            continue
        ok = True
        for j in ids:
            if j == r: continue
            if abs(U[q, j] - U[r, j]) > 1e-9 or abs(U[j, q] - U[j, r]) > 1e-9:
                ok = False; break
        if ok:
            return r
    return None


def edge_logweights(d, ch, N, keys, twins=False):
    """log transition weights among the expanded states `keys` (recomputed from chain.Chain's fates and k*), plus the
    log inflow weights into unexpanded targets."""
    pos = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    mu = d['mu']; U = d['U']
    LA = np.full((n, n), -np.inf)
    out_un = defaultdict(list)
    cache = {}
    twin_done = set()
    for (k1, k2, q), (rho, kstar, tk) in ch.edge_rho.items():
        i = pos.get(k1)
        if i is None: continue
        if k1 not in cache:
            ids, x, kind = ch.states[k1]
            ids = list(ids); x = np.array(x)
            cache[k1] = (ids, x, float(x @ U[np.ix_(ids, ids)] @ x))
        ids, x, uaa = cache[k1]
        if twins and len(ids) > 1:
            r = twin_of(U, ids, q)
            if r is not None:
                # q is a payoff twin of resident r on the support: neutral drift inside r's compartment replaces r by q
                # with probability 1/(x_r N) (the chain's lumped-resident fixation would charge it a frequency penalty)
                if (k1, q) in twin_done: continue
                twin_done.add((k1, q))
                xr = x[ids.index(r)]
                ids2 = [q if j == r else j for j in ids]
                k3 = ch.add_state(ids2, x)
                lw = math.log(mu[q]) - math.log(max(xr * N, 1.0))
                j = pos.get(k3)
                if j is None:
                    out_un[k3].append((i, lw))
                else:
                    LA[i, j] = _lae(LA[i, j], lw)
                continue
        uqa = float(U[q, ids] @ x); uaq = float(U[ids, q] @ x); uqq = float(U[q, q])
        lr = log_fixation(uqq, uqa, uaq, uaa, N, W, int(kstar))
        tm = ch.trans_mut.get((k1, k2), {}).get(q, 0.0)
        share = tm / (mu[q] * rho) if rho > 1e-250 and tm > 0 else 1.0
        share = min(max(share, 0.0), 1.0)
        if share <= 0: continue
        lw = math.log(mu[q]) + math.log(share) + lr
        j = pos.get(k2)
        if j is None:
            out_un[k2].append((i, lw))
        else:
            LA[i, j] = _lae(LA[i, j], lw)
    return LA, out_un


def solve_log(LA):
    n = LA.shape[0]
    lex = np.array([np.logaddexp.reduce(LA[i][np.isfinite(LA[i])]) if np.isfinite(LA[i]).any() else -1e300 for i in range(n)])
    order = np.argsort(lex)
    lx = gth_log(LA[np.ix_(order, order)])
    lpi = np.empty(n); lpi[order] = lx
    return lpi - np.logaddexp.reduce(lpi), lex


def seeded_chain(d, N, extra_states=(), log_theta=math.log(1e-12), max_states=4000, max_rounds=80, verbose=False, twins=False):
    """Log-domain lazy chain: every monomorphic state and every state in extra_states ((ids, x) pairs, e.g. all deep
    polymorphisms) is expanded; then, round by round, every unexpanded target whose stationary inflow (log domain,
    relative to the total) exceeds log_theta is expanded; pi by log-domain GTH (reflecting boundary).  Returns the
    chain, keys, log pi and the log of the cut flow.  The criterion is relative inflow, so a deep state reached with a
    tiny flow is expanded whenever that flow beats theta; deep states are seeded explicitly so none can hide."""
    ch, prov = make_chain(d, N, theta=1.0, max_states=10**9, eager_poly=True)
    for c in range(d['K']):
        ch.expand(ch.mono(c))
    seeded = []
    for ids, x in extra_states:
        k = ch.add_state(ids, x); ch.expand(k); seeded.append(k)
    # one layer more: every target of a seeded state's exits, so a seeded state's exits are never cut
    for k in seeded:
        for k2 in list(ch.trans[k]):
            if k2 not in ch.trans:
                ch.expand(k2)
    for rnd in range(max_rounds):
        keys = list(ch.trans)
        LA, out_un = edge_logweights(d, ch, N, keys, twins=twins)
        lpi, lex = solve_log(LA)
        inflow = {k2: np.logaddexp.reduce([lpi[i] + lw for i, lw in lst]) for k2, lst in out_un.items()}
        cand = [k for k, f in inflow.items() if f > log_theta]
        small = [f for f in inflow.values() if f <= log_theta]
        lcut = np.logaddexp.reduce(small) if small else -np.inf
        if not np.isfinite(lcut): lcut = -1e300
        if verbose:
            print('  round %d: %d expanded, %d candidates, log10 cut %.1f' % (rnd, len(keys), len(cand), lcut / math.log(10)), flush=True)
        if not cand or len(keys) >= max_states:
            break
        for k in sorted(cand, key=lambda k: -inflow[k])[:max(1, max_states - len(keys))]:
            ch.expand(k)
    return dict(ch=ch, keys=keys, lpi=lpi, pi=np.exp(lpi), LA=LA, lexit=lex, n=len(keys), log10_cut=float(lcut / math.log(10)),
                rounds=rnd + 1, n_cand_left=len(cand))


def deep_states(d, max_types=3):
    """monomorphic and 2-/3-type interior rest points that are stable within their face and against which every
    outside mutant is deleterious at first order or first-order neutral with a frequency penalty (the chain's lumped
    resident): the states whose every exit has a barrier growing linearly in N."""
    import itertools
    from chain import replicator
    U, K = d['U'], d['K']

    def deep(ids, x):
        ids = np.asarray(ids); x = np.asarray(x)
        ub = x @ U[np.ix_(ids, ids)] @ x
        uq = U[:, ids] @ x
        uq[ids] = -9
        if (uq > ub + 1e-12).any(): return False
        for q in np.nonzero(np.abs(uq - ub) <= 1e-12)[0]:
            if (U[q, q] - uq[q]) - (U[ids, q] @ x - ub) >= -1e-12: return False
        return True
    out = []
    for i in range(K):
        if deep([i], [1.0]): out.append(([i], [1.0]))
    for i in range(K):
        for j in range(i + 1, K):
            a, b, c, e = U[i, i], U[i, j], U[j, i], U[j, j]
            if a < c - 1e-12 and e < b - 1e-12:
                x = (b - e) / ((b - e) + (c - a))
                if deep([i, j], [x, 1 - x]): out.append(([i, j], [x, 1 - x]))
    if max_types >= 3:
        T = np.array(list(itertools.combinations(range(K), 3)))
        for s in range(0, len(T), 200000):
            t = T[s:s + 200000]; n = len(t)
            A = np.zeros((n, 4, 4)); A[:, :3, :3] = U[t[:, :, None], t[:, None, :]]; A[:, :3, 3] = -1; A[:, 3, :3] = 1
            b = np.zeros((n, 4)); b[:, 3] = 1
            ok = np.abs(np.linalg.det(A)) > 1e-12
            X = np.full((n, 4), np.nan); X[ok] = np.linalg.solve(A[ok], b[ok][:, :, None])[:, :, 0]
            for r in np.nonzero(ok & (X[:, :3] > 1e-9).all(1))[0]:
                ids = t[r]; x = X[r, :3]
                if not deep(ids, x): continue
                Us = U[np.ix_(ids, ids)]; stable = True
                for pert in ([.02, -.01, -.01], [-.01, .02, -.01], [-.01, -.01, .02]):
                    xp = np.clip(x + np.array(pert), 1e-6, 1); xp /= xp.sum()
                    xr, st, _, _ = replicator(Us, xp, rest_tol=1e-10)
                    if st != 'rest' or np.abs(xr - x).max() > 1e-3: stable = False; break
                if stable: out.append((list(ids), list(x)))
    return out


def best_path(LA, src, dst_set):
    """max-weight (min -log w) path from src to any state of dst_set in the log-weight graph LA (Dijkstra)."""
    import heapq
    n = LA.shape[0]
    dist = np.full(n, np.inf); prev = -np.ones(n, int)
    dist[src] = 0.0
    h = [(0.0, src)]
    dst_set = set(dst_set)
    while h:
        dd, u = heapq.heappop(h)
        if dd > dist[u]: continue
        if u in dst_set:
            path = [u]
            while prev[path[-1]] >= 0: path.append(prev[path[-1]])
            return -dd, path[::-1]
        for v in np.nonzero(np.isfinite(LA[u]))[0]:
            nd = dd - LA[u, v]
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u; heapq.heappush(h, (nd, v))
    return -np.inf, []


def lazy_best_path(d, N, src_state, target_pred, twins=True, max_expand=3000):
    """max-weight path (in log weight per mutation event) from src_state ((ids, x)) to any state satisfying
    target_pred(info) with info = pop_outcome dict, by Dijkstra with on-demand expansion (twin moves included if
    twins).  Returns (log10 weight, path descriptions, expansions)."""
    import heapq
    from dollar_partitions import pop_outcome
    ch, prov = make_chain(d, N, theta=1.0, max_states=10**9, eager_poly=True)
    k0 = ch.add_state(*src_state)
    dist = {k0: 0.0}; prev = {k0: None}
    h = [(0.0, 0, k0)]; cnt = 0; tie = 1
    done = set()
    while h and cnt < max_expand:
        dd, _, k = heapq.heappop(h)
        if k in done: continue
        done.add(k)
        ids, x, kind = ch.states[k]
        o = pop_outcome(d, ids, np.round(np.array(x) * N).astype(int))
        if target_pred(o):
            path = [k]
            while prev[path[-1]] is not None: path.append(prev[path[-1]])
            return -dd / math.log(10), [state_desc(d, ch, p) for p in path[::-1]], cnt
        ch.expand(k); cnt += 1
        LA, out_un = edge_logweights(d, ch, N, [k], twins=twins)
        for k2, lst in out_un.items():
            lw = np.logaddexp.reduce([w_ for _, w_ in lst])
            nd = dd - lw
            if nd < dist.get(k2, np.inf):
                dist[k2] = nd; prev[k2] = k; heapq.heappush(h, (nd, tie, k2)); tie += 1
    return None, [], cnt


def limN_run(arm, N, log_theta, n=7, aug=None, aug_mass=0.0, deep=None, tag='', twins=False):
    """seeded log-domain chain at one N, with the summary statistics, the efficient set's and the deep set's
    entry/exit rates, and the best paths S3 -> deep set and deep set -> efficient set."""
    from dollar_partitions import pop_outcome, label_of
    t0 = time.time()
    d = data(arm, n, aug=aug, aug_mass=aug_mass)
    if deep is None:
        deep = deep_states(d, 3)
    F = seeded_chain(d, N, deep, log_theta=log_theta, twins=twins)
    ch, keys, pi, LA = F['ch'], F['keys'], F['pi'], F['LA']
    s5 = find(d, S['S5'])
    deepkeys = set(ch.add_state(ids, x) for ids, x in deep)
    info = []
    for k in keys:
        ids, x, kind = ch.states[k]
        o = pop_outcome(d, ids, np.round(np.array(x) * N).astype(int))
        xs5 = dict(zip(ids, x)).get(s5, 0.0)
        info.append(dict(eff=o['eff'], effset=o['eff'] >= 0.99, greedy=len(ids) > 1 and xs5 >= 0.5, deep=k in deepkeys, label=label_of(o),
                         mean=o['mean_pay'], E_max=o['E_max_pay']))
    P_eff = float(sum(p * i['eff'] for p, i in zip(pi, info)))
    res = dict(arm=arm, n=n, N=N, twins=twins, log10_theta=log_theta / math.log(10), aug_mass=aug_mass, aug=[fsrc(f) for f in (aug or [])], tag=tag,
               n_states=F['n'], log10_cut=F['log10_cut'], n_deep=len(deep), P_efficient=P_eff,
               E_max=float(sum(p * i['E_max'] for p, i in zip(pi, info))), mean_pay=float(sum(p * i['mean'] for p, i in zip(pi, info))))
    for nm_ in ('effset', 'greedy', 'deep'):
        mask = np.array([i[nm_] for i in info])
        lpi = F['lpi']
        m = float(pi[mask].sum())
        # exit / entry rates per mutation event in log10 (flux out of the set over its mass)
        if mask.any() and (~mask).any():
            lf_out = np.logaddexp.reduce((lpi[mask][:, None] + LA[np.ix_(mask, ~mask)]).ravel())
            lf_in = np.logaddexp.reduce((lpi[~mask][:, None] + LA[np.ix_(~mask, mask)]).ravel())
            lm_in = np.logaddexp.reduce(lpi[mask]); lm_out = np.logaddexp.reduce(lpi[~mask])
            res[nm_] = dict(mass=m, log10_mass=float(lm_in / math.log(10)), log10_exit_rate=float((lf_out - lm_in) / math.log(10)),
                            log10_entry_rate=float((lf_in - lm_out) / math.log(10)))
        else:
            res[nm_] = dict(mass=m)
    order = np.argsort(-pi)[:12]
    res['top_states'] = [dict(state=state_desc(d, ch, keys[i]), pi=float(pi[i]), log10_pi=float(F['lpi'][i] / math.log(10)), **info[i]) for i in order]
    # best paths
    i3 = keys.index(ch.mono(find(d, S['S3'])))
    dset = [i for i, x in enumerate(info) if x['deep']]
    eset = [i for i, x in enumerate(info) if x['effset']]
    lw, path = best_path(LA, i3, dset)
    res['path_S3_to_deep'] = dict(log10_w=float(lw / math.log(10)), path=[state_desc(d, ch, keys[i]) for i in path])
    top = int(order[0])
    if info[top]['deep']:
        lw, path = best_path(LA, top, eset)
        res['path_top_to_eff'] = dict(log10_w=float(lw / math.log(10)), path=[state_desc(d, ch, keys[i]) for i in path])
    res['time_s'] = time.time() - t0
    return res


def cmd_limN(a):
    jobs = [dict(arm=arm, N=N, lt=th) for arm in a.arm for N in a.N for th in a.theta]
    if a.aug:
        AUG = dict(P=[PPROG, PPROG_1], Pp=[PPRIME, PPRIME_1], both=[PPROG, PPROG_1, PPRIME, PPRIME_1])[a.aug]
        jobs = [dict(j, aug=AUG, aug_mass=m, tag='_aug%s%g' % (a.aug, m)) for j in jobs for m in a.aug_mass]
    if a.shard is not None:
        i, m = a.shard
        jobs = jobs[i::m]
    deep_cache = {}
    for j in jobs:
        key = (j['arm'], j.get('aug_mass', 0.0), a.aug)
        if key not in deep_cache:
            deep_cache[key] = deep_states(data(j['arm'], 7, aug=j.get('aug'), aug_mass=j.get('aug_mass', 0.0)), 3)
        tg = j.get('tag', '') + ('_twins' if a.twins else '')
        r = limN_run(j['arm'], j['N'], math.log(j['lt']), aug=j.get('aug'), aug_mass=j.get('aug_mass', 0.0), deep=deep_cache[key], tag=tg, twins=a.twins)
        fn = os.path.join(OUT, 'limN_%s_n7_N%d_th%g%s.json' % (j['arm'], j['N'], j['lt'], tg))
        json.dump(r, open(fn, 'w'), indent=1, default=str)
        print('%s N=%d th=%g %s: P(eff) %.4f effset %.3g (log10 %.1f) deep %.4f greedy %.3g | states %d cut 1e%.1f | top %s (%.3f) | S3->deep 1e%.1f (%.0fs)' % (
            j['arm'], j['N'], j['lt'], tg, r['P_efficient'], r['effset']['mass'], r['effset'].get('log10_mass', 0), r['deep']['mass'],
            r['greedy']['mass'], r['n_states'], r['log10_cut'], r['top_states'][0]['state'], r['top_states'][0]['pi'],
            r['path_S3_to_deep']['log10_w'], r['time_s']), flush=True)


def full_chain(d, N, max_states=6000, verbose=False):
    """The chain over the closure of every state reachable from the monomorphic states (no flow pruning), with
    every edge weight recomputed in the log domain, and the stationary distribution by log-domain GTH.  The edge
    targets, fates and k* are chain.Chain's (eager_poly irrelevant: everything is expanded).  Exact up to the
    chain's own approximations at any N, and immune to the underflow that makes a linear-domain chain at large N
    treat a deep state as absorbing."""
    ch, prov = make_chain(d, N, theta=-1.0, max_states=max_states, max_rounds=400, eager_poly=True)
    ch.explore()
    keys = list(ch.trans)
    n = len(keys)
    pos = {k: i for i, k in enumerate(keys)}
    mu = d['mu']; U = d['U']
    LA = np.full((n, n), -np.inf)
    unexpanded = set()
    for (k1, k2, q), (rho, kstar, tk) in ch.edge_rho.items():
        if k1 not in pos: continue
        if k2 not in pos:
            unexpanded.add(k2); continue
        ids, x, kind = ch.states[k1]
        ids = list(ids); x = np.array(x)
        uaa = float(x @ U[np.ix_(ids, ids)] @ x)
        uqa = float(U[q, ids] @ x); uaq = float(U[ids, q] @ x); uqq = float(U[q, q])
        lr = log_fixation(uqq, uqa, uaq, uaa, N, W, int(kstar))
        tm = ch.trans_mut.get((k1, k2), {}).get(q, 0.0)
        share = tm / (mu[q] * rho) if rho > 1e-250 and tm > 0 else 1.0
        share = min(max(share, 0.0), 1.0)
        if share <= 0: continue
        LA[pos[k1], pos[k2]] = _lae(LA[pos[k1], pos[k2]], math.log(mu[q]) + math.log(share) + lr)
    # order: put the states with the smallest total exit last-eliminated (index 0 side) for accuracy
    lex = np.array([np.logaddexp.reduce(LA[i][np.isfinite(LA[i])]) if np.isfinite(LA[i]).any() else -1e300 for i in range(n)])
    order = np.argsort(lex)
    LAo = LA[np.ix_(order, order)]
    lx = gth_log(LAo)
    lpi = np.empty(n); lpi[order] = lx
    lpi -= np.logaddexp.reduce(lpi)
    return dict(ch=ch, keys=keys, lpi=lpi, pi=np.exp(lpi), LA=LA, lexit=lex, n=n, unexpanded=len(unexpanded))


# ---------------------------------------------------------------- fixed roles: lazy version of dollar_partitions.fixed_chain
def fixed_chain_lazy(d, N, w=W, theta=1e-12, rel_drop=1e-25, max_states=5000, verbose=False):
    """dollar_partitions.fixed_chain's chain (joint monomorphic slot configurations, constant-selection Moran
    fixation per slot, embedded jump chain, pi(s) = pi_jump(s)/R(s)) solved by GTH on a lazily grown state set:
    start from the 25 constant pairs, add every unexpanded state whose stationary inflow exceeds theta (reflecting
    boundary), until none does.  Returns the same dict as fixed_chain (pi over all K^2 pairs, zero off the set) plus
    the cut flow and the set size.  K^2 = 42,025 at modal n = 7 does not fit the dense K^2 x K^2 solve."""
    from dollar_partitions import lrho_vec, gth_linear
    U, mu, K = d['U'], d['mu'], d['K']
    lmu = np.log(0.5 * mu)
    du1 = U.T[None, :, :] - U[:, :, None]
    du2 = U.T[:, None, :] - U.T[:, :, None]
    L1 = lrho_vec(du1, N, w) + lmu[None, None, :]
    L2 = lrho_vec(du2, N, w) + lmu[None, None, :]
    del du1, du2
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    mm = np.maximum(L1.max(axis=2), L2.max(axis=2))
    R = mm + np.log(np.exp(L1 - mm[:, :, None]).sum(axis=2) + np.exp(L2 - mm[:, :, None]).sum(axis=2))
    P1 = np.exp(L1 - R[:, :, None]); P2 = np.exp(L2 - R[:, :, None])
    del L1, L2
    P1[P1 < rel_drop] = 0.0; P2[P2 < rel_drop] = 0.0
    const = [c for c in range(K) if d['kinds'][c] == 'constant']
    E = [a * K + b for a in const for b in const]
    for rnd in range(200):
        pos = {s: i for i, s in enumerate(E)}
        n = len(E)
        P = np.zeros((n, n))
        inflow = defaultdict(float)
        rows_out = []
        for i, s0 in enumerate(E):
            a, b = divmod(s0, K)
            for q in range(K):
                for pr, t in ((P1[a, b, q], q * K + b), (P2[a, b, q], a * K + q)):
                    if pr <= 0: continue
                    j = pos.get(t)
                    if j is None:
                        rows_out.append((i, t, pr))
                    else:
                        P[i, j] += pr
        # reflecting boundary: dropped mass stays (self-loop)
        for i in range(n):
            P[i, i] += max(0.0, 1.0 - P[i].sum())
        xj = gth_linear(P)
        for i, t, pr in rows_out:
            inflow[t] += xj[i] * pr
        cand = [t for t, f in inflow.items() if f > theta]
        cut = float(sum(f for t, f in inflow.items() if f <= theta))
        if verbose:
            print('  round %d: %d states, %d candidates, cut %.2e' % (rnd, n, len(cand), cut), flush=True)
        if not cand or n >= max_states:
            cut = float(sum(inflow.values()))      # every unexpanded target's inflow, truncated candidates included
            break
        cand.sort(key=lambda t: -inflow[t])
        E = E + cand[:max(1, max_states - n)]
    lpi = np.full(K * K, -np.inf)
    lpi[E] = np.log(np.maximum(xj, 1e-320)) - R.ravel()[E]
    lpi -= lpi.max()
    pi = np.exp(lpi); pi /= pi.sum()
    return dict(pi=pi.reshape(K, K), logR=R, P1=P1, P2=P2, cut=cut, n_states=len(E), rounds=rnd + 1)


def fixed_chain_full(d, N, w=W, method='sparse'):
    """The fixed-role chain over all K^2 joint states: jump chain from dollar_partitions.fixed_chain's rates (no
    dropping), stationary by a sparse direct solve ('sparse') or dense GTH ('gth', K^2 <= ~6000); pi(s) =
    pi_jump(s)/R(s) in log space.  Returns the fixed_chain dict."""
    import scipy.sparse as sp_
    import scipy.sparse.linalg as spl
    from dollar_partitions import lrho_vec, gth_linear
    U, mu, K = d['U'], d['mu'], d['K']
    lmu = np.log(0.5 * mu)
    L1 = lrho_vec(U.T[None, :, :] - U[:, :, None], N, w) + lmu[None, None, :]
    L2 = lrho_vec(U.T[:, None, :] - U.T[:, :, None], N, w) + lmu[None, None, :]
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    mm = np.maximum(L1.max(axis=2), L2.max(axis=2))
    R = mm + np.log(np.exp(L1 - mm[:, :, None]).sum(axis=2) + np.exp(L2 - mm[:, :, None]).sum(axis=2))
    P1 = np.exp(L1 - R[:, :, None]); P2 = np.exp(L2 - R[:, :, None])
    del L1, L2
    S_ = K * K
    a_, b_ = np.divmod(np.arange(S_), K)
    rows = np.concatenate([np.repeat(np.arange(S_), K), np.repeat(np.arange(S_), K)])
    cols = np.concatenate([(idx[None, :] * K + b_[:, None]).ravel(), (a_[:, None] * K + idx[None, :]).ravel()])
    vals = np.concatenate([P1.reshape(S_, K).ravel(), P2.reshape(S_, K).ravel()])
    keep = vals > 0
    P = sp_.csr_matrix((vals[keep], (rows[keep], cols[keep])), shape=(S_, S_))
    if method == 'gth':
        xj = gth_linear(P.toarray())
    else:
        A = (sp_.identity(S_, format='csr') - P).T.tolil()
        A[S_ - 1, :] = np.ones(S_)
        bvec = np.zeros(S_); bvec[-1] = 1.0
        xj = spl.spsolve(A.tocsc(), bvec)
        xj = np.maximum(xj, 0.0); xj /= xj.sum()
    lpi = np.log(np.maximum(xj, 1e-320)) - R.ravel()
    lpi -= lpi.max()
    pi = np.exp(lpi); pi /= pi.sum()
    return dict(pi=pi.reshape(K, K), logR=R, P1=P1, P2=P2, cut=0.0, n_states=S_, xjump=xj.reshape(K, K))


def fixed_chain_poly(d, N, w=W, log_cut=-60.0):
    """Large-N fixed-role chain: keep only edges with log weight > log_cut (strict and neutral moves; deleterious
    fixations are exp(-Theta(N)) and dropped), find the closed communicating classes of what remains, and solve the
    stationary distribution inside each (sparse).  With a single closed class this is the N -> infinity support at
    this N; with several, their relative weights need the dropped (exponential) edges and are not computed."""
    import scipy.sparse as sp_
    import scipy.sparse.linalg as spl
    import scipy.sparse.csgraph as csg_
    from dollar_partitions import lrho_vec
    U, mu, K = d['U'], d['mu'], d['K']
    lmu = np.log(0.5 * mu)
    L1 = lrho_vec(U.T[None, :, :] - U[:, :, None], N, w) + lmu[None, None, :]
    L2 = lrho_vec(U.T[:, None, :] - U.T[:, :, None], N, w) + lmu[None, None, :]
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    S_ = K * K
    a_, b_ = np.divmod(np.arange(S_), K)
    rows = np.concatenate([np.repeat(np.arange(S_), K), np.repeat(np.arange(S_), K)])
    cols = np.concatenate([(idx[None, :] * K + b_[:, None]).ravel(), (a_[:, None] * K + idx[None, :]).ravel()])
    lv = np.concatenate([L1.reshape(S_, K).ravel(), L2.reshape(S_, K).ravel()])
    keep = lv > log_cut
    rows, cols, lv = rows[keep], cols[keep], lv[keep]
    G = sp_.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(S_, S_))
    ncomp, lab = csg_.connected_components(G, directed=True, connection='strong')
    out_edge = np.zeros(ncomp, bool)
    out_edge[lab[rows][lab[rows] != lab[cols]]] = True
    closed = [c for c in range(ncomp) if not out_edge[c]]
    pi = np.zeros(S_)
    classes = []
    vals = np.exp(lv)
    for c in closed:
        mem = np.nonzero(lab == c)[0]
        pos = -np.ones(S_, int); pos[mem] = np.arange(len(mem))
        m = (lab[rows] == c) & (lab[cols] == c)
        Q = sp_.csr_matrix((vals[m], (pos[rows[m]], pos[cols[m]])), shape=(len(mem), len(mem)))
        Q = Q - sp_.diags(np.asarray(Q.sum(axis=1)).ravel())
        n = len(mem)
        if n == 1:
            x = np.ones(1)
        else:
            A = Q.T.tolil(); A[n - 1, :] = np.ones(n)
            bvec = np.zeros(n); bvec[-1] = 1.0
            x = spl.spsolve(A.tocsc(), bvec); x = np.maximum(x, 0); x /= x.sum()
        classes.append(dict(size=n, members=mem, pi=x))
    return dict(closed=classes, n_closed=len(closed), ncomp=ncomp, K=K)


def cmd_fixed_poly(a):
    from dollar_partitions import slot_outcome, olabel_of
    out = {}
    for arm in a.arm:
        d = data(arm, 7)
        K = d['K']; nm = d['names']
        for N in a.N:
            r = fixed_chain_poly(d, N)
            rec = dict(arm=arm, N=N, n_closed=r['n_closed'], classes=[])
            for c in r['closed']:
                lab = defaultdict(float); eff = 0.0; top = []
                for s, p in zip(c['members'], c['pi']):
                    aa, bb = divmod(int(s), K)
                    o = slot_outcome(d, aa, bb)
                    lab[olabel_of(o)] += p; eff += p * o['eff']
                order = np.argsort(-c['pi'])[:8]
                top = [('%s | %s' % (nm[divmod(int(c['members'][i]), K)[0]], nm[divmod(int(c['members'][i]), K)[1]]), float(c['pi'][i])) for i in order]
                rec['classes'].append(dict(size=c['size'], eff=eff, labels=dict(lab), top=top))
            out['%s_%d' % (arm, N)] = rec
            print(arm, N, 'closed classes', r['n_closed'], [(c['size'], round(c['eff'], 4), {k: round(v, 3) for k, v in c['labels'].items() if v > 1e-3}) for c in rec['classes']][:6], flush=True)
    json.dump(out, open(os.path.join(OUT, 'fixed_poly.json'), 'w'), indent=1, default=str)


def cmd_fixed(a):
    from dollar_partitions import fixed_summary
    for arm in a.arm:
        d = data(arm, 7)
        for N in a.N:
            t0 = time.time()
            ch = fixed_chain_full(d, N, method='gth') if d['K'] <= 80 else fixed_chain_lazy(d, N, theta=a.theta[0], max_states=a.max_states, verbose=True)
            r = fixed_summary(d, ch)
            r.update(arm=arm, n=7, N=N, theta=a.theta[0], n_states=ch['n_states'], time_s=time.time() - t0, K=d['K'])
            fn = os.path.join(OUT, 'fixed_%s_n7_N%d_th%g.json' % (arm, N, a.theta[0]))
            json.dump(r, open(fn, 'w'), indent=1, default=str)
            o = r['outcome']
            print('%s fixed N=%d: %s | eff %.4f Emax %.3f; const pairs %.3f; states %d; cut %.1e (%.0fs)' % (
                arm, N, ', '.join('%s %.4f' % (k, v) for k, v in sorted(r['ordered_label_mass'].items()) if v > 1e-3),
                o['eff'], o['E_max_pay'], r['mass_constant_pairs'], ch['n_states'], ch['cut'], r['time_s']), flush=True)


# ---------------------------------------------------------------- lotteries (dollar_partitions' kernel and stop rule)
def _job_lottery(job):
    import dollar_partitions as DP
    marm = job['marm']
    DP.data = lambda game, n, arm, _m=marm, _n=job['n']: data(_m, _n)
    r = DP.run_islands(dict(job, game='dollar5', arm='norole'))
    r.update(marm=marm, I=job['I'], N=job['N'], mN=job['mN'], run=job['run'])
    return r


def cmd_lottery(a):
    jobs = []
    for marm in a.arm:
        for (N, I) in a.cells:
            for mN in a.mN:
                for r in range(a.runs):
                    # identical initialization seeds across the two arms (the multinomial draw is over each arm's own
                    # classes, so 'identical' means identical seeds and stopping rules)
                    seed = (7919 * I + 31 * N + int(mN * 1000) * 13 + r) % (2**31 - 1)
                    jobs.append(dict(marm=marm, n=7, I=I, N=N, mN=mN, gens=a.gens, seed=seed, run=r, thr=0.95))
    if a.shard is not None:
        i, m = a.shard
        jobs = jobs[i::m]
    out = defaultdict(list)
    fn = os.path.join(OUT, 'lottery_%s.json' % (a.tag or 'all'))
    for j in jobs:
        r = _job_lottery(j)
        out['%s|%d|%d|%g' % (r['marm'], r['N'], r['I'], r['mN'])].append(r)
        json.dump(out, open(fn, 'w'), default=str)
        labs = Counter(r['labels'])
        print('%s (%d,%d) mN=%g run %d: %s closed_at %s censored %s (%.0fs)' % (r['marm'], r['N'], r['I'], r['mN'], r['run'],
              dict(labs.most_common(4)), r['closed_at'], r['censored'], r['time_s']), flush=True)


def cmd_proofs(a):
    """certificates for the representative encounters -> notes/modal-dollar.md (derivation section) + json."""
    th = Theory5()
    ms = GP.MinSearch(th)
    F = {"P'": PPRIME, 'A5': ACC5, 'P': PPROG, 'S5': S['S5'], 'S3': S['S3'], "P'1": PPRIME_1,
         'C3': one(0, 2, 2, 0),      # C3 = if(BOX(S3), S3, S1): the 'concede unless provably fair' accommodator
         'X': one(0, 0, 0, 3), 'Z': one(1, 2, 2, 1), 'V': one(1, 3, 1, 3), 'S4': S['S4']}   # the deep polymorphism's members
    pairs = [("P'", "P'"), ("P'", 'A5'), ("P'", 'P'), ('P', 'S5'), ('A5', 'S5'), ('A5', 'A5'), ('P', 'P'), ('P', 'A5'),
             ("P'", 'S5'), ("P'", 'C3'), ("P'1", 'A5'), ('C3', 'S5'),
             ('X', 'X'), ('X', 'Z'), ('X', 'V'), ('Z', 'Z'), ('Z', 'V'), ('V', 'V'), ('Z', 'S3'), ('X', 'S4')]
    names = {th.prog(f): k for k, f in F.items()}
    nat, atL, atA, tab = to_arrays([F[k] for k in F])
    keys = list(F)
    out = np.zeros(2, np.int64)
    recs = []
    lines = ['## Certificates (GLS+Def, five-valued definitional constants)', '',
             'P^a[x,y] reads "x demands S_a against y"; its definition is x\'s source read against y (a disjunction over the',
             'atom valuations whose table entry is a). An atom BOX_L(THEM = S_b) of x read against y is [](~[]^L F -> P^b[y,x]).',
             'For each encounter: every box atom of each side, its provability (the terminating GL decision procedure of',
             '`src/gl_proofs.py`; "not provable" is the exhaustive search failing, so the atom is false at the stable world),',
             'the certified minimal derivation (size in sequents, Löb steps) of each provable atom, and the evaluator\'s play.', '']
    for x, y in pairs:
        r = certify_pair(th, F[x], F[y], ms=ms, want_render=True, names=names)
        eval_modal2(nat, atL, atA, tab, keys.index(x), keys.index(y), out)
        ev = [SNAME[o] for o in out]
        recs.append(dict(x=x, y=y, x_src=fsrc(F[x]), y_src=fsrc(F[y]), plays=r['plays'], evaluator=ev, agree=r['plays'] == ev,
                         atoms=[[{k: v for k, v in s.items() if k != 'derivation'} for s in side] for side in r['sides']]))
        lines.append('### %s = `%s` vs %s = `%s`: plays (%s, %s); evaluator (%s, %s)' % (x, fsrc(F[x]), y, fsrc(F[y]), *r['plays'], *ev))
        lines.append('')
        for who, side in zip((x, y), r['sides']):
            for s_ in side:
                if s_['provable']:
                    lines.append('- %s\'s atom %s: **provable**, %d sequents, %d Löb step(s)%s' % (
                        who, s_['atom'], s_['size'], s_['loeb'], '' if s_['certified'] else ' (upper bound, uncertified)'))
                    if s_.get('derivation'):
                        lines += ['', '```', s_['derivation'], '```', '']
                else:
                    lines.append('- %s\'s atom %s: not provable' % (who, s_['atom']))
        lines.append('')
    open(os.path.join(OUT, 'certificates.md'), 'w').write('\n'.join(lines) + '\n')
    json.dump(recs, open(os.path.join(OUT, 'certificates.json'), 'w'), indent=1)
    for r in recs:
        print(r['x'], r['y'], r['plays'], r['evaluator'], r['agree'])


def cmd_static(a):
    out = {}
    for arm in ('modal', 'weak'):
        r, d = static_checkpoint(arm)
        out[arm] = r
    json.dump(out, open(os.path.join(OUT, 'static.json'), 'w'), default=str)
    print('wrote static.json')


def cmd_chain(a):
    from multiprocessing import Pool
    jobs = [dict(arm=arm, n=n, N=N, theta=th, tag=a.tag) for arm in a.arm for n in a.n for N in a.N for th in a.theta]
    if a.aug:
        AUG = dict(P=[PPROG, PPROG_1], Pp=[PPRIME, PPRIME_1], both=[PPROG, PPROG_1, PPRIME, PPRIME_1])[a.aug]
        jobs = [dict(j, aug=AUG, aug_mass=m, tag='%s_aug%s%g' % (a.tag, a.aug, m)) for j in jobs for m in a.aug_mass]
    jobs.sort(key=lambda j: -j['N'])
    if a.shard is not None:
        i, m = a.shard
        jobs = jobs[i::m]
    for r in map(_job_chain, jobs):
            print('%s N=%d theta=%g %s: P(eff) %.4f effset %.4f greedy %.4f cut %.1e (%.0fs)' % (
                r['arm'], r['N'], r['theta'], r['tag'], r['P_eff'], r['effset'], r['greedy'], r['cut'], r['time_s']), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--n', type=int, nargs='+', default=[7])
    ap.add_argument('--arm', nargs='+', default=['modal', 'weak'])
    ap.add_argument('--N', type=int, nargs='+', default=[100, 1000, 10000, 30000, 100000])
    ap.add_argument('--theta', type=float, nargs='+', default=[1e-7, 1e-9])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--tag', default='')
    ap.add_argument('--aug', default=None)
    ap.add_argument('--shard', type=int, nargs=2, default=None)
    ap.add_argument('--twins', action='store_true')
    ap.add_argument('--max_states', type=int, default=8000)
    ap.add_argument('--cells', type=lambda s: tuple(int(x) for x in s.split(',')), nargs='+', default=[(100, 64), (400, 16)])
    ap.add_argument('--mN', type=float, nargs='+', default=[0.0, 0.1])
    ap.add_argument('--runs', type=int, default=40)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--aug_mass', type=float, nargs='+', default=[1e-4, 1e-3, 1e-2])
    a = ap.parse_args()
    if a.cmd == 'classes':
        for n in a.n:
            for arm in a.arm:
                t0 = time.time()
                d = data(arm, n)
                print('%s n=%d: a(s)=%s, %d canonical functions, %d payoff classes, classes with mixed joint actions %d (%.1fs)' % (
                    arm, n, [int(x) for x in d['a_counts']], d['n_funcs'], d['K'], d['mixed_actions'], time.time() - t0), flush=True)
    elif a.cmd == 'chain':
        cmd_chain(a)
    elif a.cmd == 'limN':
        cmd_limN(a)
    elif a.cmd == 'lottery':
        cmd_lottery(a)
    elif a.cmd == 'fixed_poly':
        cmd_fixed_poly(a)
    elif a.cmd == 'fixed':
        cmd_fixed(a)
    elif a.cmd == 'proofs':
        cmd_proofs(a)
    elif a.cmd == 'static':
        cmd_static(a)
