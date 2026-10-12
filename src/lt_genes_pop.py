"""Certificates as genes: the population tables over units (notes/certificates-as-genes.md §1.8, §1.11).

A unit is (τ, Cseq, Dseq): a run tree of milestone 2's P catalogue (n <= 7; in P a τ-type is a run tree, since the
frozen lists are functions of the run tree) and the two blocks of its certificate list, scripts by global id.  Every
check value, play, adoption and production is a function of the units involved and of whether the two sides are the
same quote (Lemma T with inventories).  Representatives: the τ's first spelling with the H mode marker; the twin
instance is the same spelling with the C marker (a distinct quote with the same unit).

Tables (host replay checker without step limit, `IdealCheck`: milestone 2's ideal table; the executable term is
compared on samples):
  CH[a][t, m]  chk_a(t, m) for distinct units, diagonal = the twin instance (int8: -1 unknown, 0 F, 1 T, 2 TO);
  UVt[u, k]    self (same quote), vs ⌜C⌝, vs ⌜D⌝ values per unit and outcome;
  A[x, y]      x's action against y (diagonal = twin play); selfa[x] the self-play action;
  SINGLE[τ, s] the single-entry unit (τ, [s]) when s fits τ's run (wildcard screen), else -1;
  APP[u, s]    u with s appended to its block;  PRODC[τ, code], PRODD[τ, code] the tactic's script by signature;
  PD[u]        u after the S step's D production.
"""
import os
import pickle
import sys
import time
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import lt_genes as G
import carrier_populations as CP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'lt_genes')
os.makedirs(OUT, exist_ok=True)
K_DEF = 10 ** 6
QC, QD = L.PROG_C, L.PROG_D
VCODE = {'F': 0, 'T': 1, 'TO': 2}
UVK = [('C', 'self'), ('D', 'self'), ('C', '^C'), ('D', '^C'), ('C', '^D'), ('D', '^D')]
UVI = {k: i for i, k in enumerate(UVK)}

# atom kinds for signatures: (kind, a, q) with kind 0 S, 1 R, 2 yself, 3 xself, 4 y^q, 5 x^q; a 0 C 1 D; q 0 C 1 D
KIND = {'S': 0, 'R': 1, 'yself': 2, 'xself': 3, 'y^': 4, 'x^': 5}


def atom_box_kind(at):
    """(e, p, q, a) -> (kind, a, q) of the box the atom builds in a run against an opponent."""
    e, p, q, a = at
    ai = 0 if a == 'C' else 1
    if p == 'them' and q == 'me': return (0, ai, 0)
    if p == 'me' and q == 'them': return (1, ai, 0)
    if p == 'them' and q == 'them': return (2, ai, 0)
    if p == 'me' and q == 'me': return (3, ai, 0)
    qi = 0 if q == 'C' else 1
    if p == 'them': return (4, ai, qi)
    return (5, ai, qi)


class Universe:
    """The script registry, the units and their representative terms."""

    def __init__(self, K=K_DEF, P=None, verbose=False):
        self.K, self.V = K, K // 4
        self.P = K // 4 if P is None else P
        t0 = time.time()
        self.cat = cat = CP.Catalogue(7, 'P', K)
        self.T = cat.T
        self.tau_dt = cat.tau_dt
        self.tau_atoms = [sorted(CP.dt_atoms(d)) for d in cat.tau_dt]
        self.tau_kinds = [[atom_box_kind(at) for at in ats] for ats in self.tau_atoms]
        assert max(len(a) for a in self.tau_atoms) <= 2
        self.rep_sp = [cat.members[t][0] for t in range(cat.T)]
        self.bodies = [CP.body_term(cat.sexprs[cat.spell[k]['i']], self.V, K) for k in self.rep_sp]
        self.scripts = []            # (a, script data)
        self.sid = {}
        self.sorigin = {}            # sid -> 'host' | 'search' (first origin)
        self.units = []              # (τ, cseq tuple of sids, dseq tuple of sids)
        self.uid = {}
        self.H_unit = np.zeros(cat.T, np.int64)
        self.E_unit = np.zeros(cat.T, np.int64)
        for t in range(cat.T):
            cs, ds = G.split_list(cat.tau_list[t])
            self.H_unit[t] = self.unit(t, [self.script('C', s, 'host') for s in cs], [self.script('D', s, 'host') for s in ds])
        for t in range(cat.T):
            self.E_unit[t] = self.unit(t, (), ())
        self.n_base_units = len(self.units)
        self._terms = {}
        if verbose:
            print('universe base: %d run trees, %d units, %d scripts (%.1fs)' % (cat.T, len(self.units), len(self.scripts), time.time() - t0), flush=True)

    def script(self, a, s, origin='host'):
        k = (a, s)
        i = self.sid.get(k)
        if i is None:
            i = len(self.scripts); self.sid[k] = i; self.scripts.append(k); self.sorigin[i] = origin
        return i

    def unit(self, t, cs, ds):
        k = (int(t), tuple(int(x) for x in cs), tuple(int(x) for x in ds))
        u = self.uid.get(k)
        if u is None:
            u = len(self.units); self.uid[k] = u; self.units.append(k)
        return u

    def has_entry(self, u, a):
        t, cs, ds = self.units[u]
        return bool(cs) if a == 'C' else bool(ds)

    def append(self, u, sid):
        t, cs, ds = self.units[u]
        if self.scripts[sid][0] == 'C':
            return u if sid in cs else self.unit(t, cs + (sid,), ds)
        return u if sid in ds else self.unit(t, cs, ds + (sid,))

    def single_unit(self, t, sid):
        a = self.scripts[sid][0]
        return self.unit(t, (sid,) if a == 'C' else (), (sid,) if a == 'D' else ())

    def term(self, u, marker='H'):
        key = (u, marker)
        tm = self._terms.get(key)
        if tm is None:
            tm = key_term(self, self.units[u], marker)
            self._terms[key] = tm
        return tm


def key_term(U, key, marker):
    t, cs, ds = key
    body = G.marked_body(U.bodies[t], marker)
    return C.carrier(body, G.canon_list([U.scripts[i][1] for i in cs], [U.scripts[i][1] for i in ds]))


# ----------------------------------------------------------------------------------------------------------------
# Screening: wildcard validity (an upper bound on adoption: every Run/RunNeg on a runnable box accepted, no partner
# validation).  Exact on the run's structure (EvR*, ChkR, Hyp, Ax), notes §1.11.
# ----------------------------------------------------------------------------------------------------------------
class Wild(CP.IdealCheck):
    def cchk(self, mode, Rb, Sb, V, nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
        except Exception:
            return 0
        if rule in (C.RUN, C.RUNNEG):
            lst = Rf if rule == C.RUN else Lf
            b = lst[j] if isinstance(j, int) and 0 <= j < len(lst) else None
            if b is None or b[0] != 'cbox' or b == Rb or b == Sb: return 0
            Vb = C.parse_carg(b[2])
            return 1 if (Vb is not None and Vb >= V) else 0
        return CP.IdealCheck.cchk(self, mode, Rb, Sb, V, nd, Lf, Rf)


# ----------------------------------------------------------------------------------------------------------------
# Workers (units and scripts synced through versioned pickles; terms cached per worker)
# ----------------------------------------------------------------------------------------------------------------
_W = {}
SYNC = os.path.join(OUT, 'sync')


def _winit(K, P, sync_dir=None):
    sys.setrecursionlimit(1000000)
    _W['U'] = Universe(K, P)
    _W['chk'] = CP.Checker('ideal', K // 4, K, memo_cap=400000)
    _W['prod'] = C.Producer(host=CP.ExactHost())
    _W['ver'] = -1
    _W['terms'] = {}
    _W['sync'] = sync_dir or SYNC


def _sync(ver):
    if _W['ver'] == ver: return
    import pickle
    with open(os.path.join(_W['sync'], 'v%d.pkl' % ver), 'rb') as f:
        scripts, units = pickle.load(f)
    U = _W['U']
    for i in range(len(U.scripts), len(scripts)):
        U.script(scripts[i][0], scripts[i][1])
    assert U.scripts == scripts[:len(U.scripts)]
    U.units = list(units)
    U.uid = {k: i for i, k in enumerate(U.units)}
    _W['ver'] = ver


def _term(u, marker):
    tm = _W['terms'].get((u, marker))
    if tm is None:
        tm = key_term(_W['U'], _W['U'].units[u], marker)
        _W['terms'][(u, marker)] = tm
    return tm


def _pair_terms(t, m, rel):
    if rel == 's':
        x = _term(t, 'H'); return x, x
    if rel == 'w':
        return _term(t, 'H'), _term(t, 'C')
    return _term(t, 'H'), _term(m, 'H')


def _chk_job(job):
    """job = (ver, a, t, [m, ...]) -> (a, t, [(m, val)], secs); m == t is the twin instance."""
    ver, a, t, ms = job
    _sync(ver)
    chk = _W['chk']
    t0 = time.time()
    out = []
    for m in ms:
        tt, mm = _pair_terms(t, m, 'w' if m == t else 'd')
        v, _ = chk(0, tt, mm, a)
        out.append((m, VCODE[v]))
    return a, t, out, time.time() - t0


def _uv_job(job):
    """job = (ver, [units]) -> [(u, k index, val)] for a in C, D and opp in self, ^C, ^D."""
    ver, us = job
    _sync(ver)
    chk = _W['chk']
    U = _W['U']
    out = []
    for u in us:
        key = U.units[u]
        x = _term(u, 'H')
        for a in ('C', 'D'):
            has = bool(key[1]) if a == 'C' else bool(key[2])
            for opp, q in (('self', x), ('^C', QC), ('^D', QD)):
                if not has:
                    out.append((u, UVI[(a, opp)], 0)); continue
                v, _ = chk(0, x, q, a)
                out.append((u, UVI[(a, opp)], VCODE[v]))
    return out


def _prod_job(job):
    """job = (ver, [(tag, key, u, v or None, rel, a)]) -> [(tag, key, script data or None)].  The host Producer
    (the frozen tactic); the term PCORE is validated equal on samples."""
    ver, items = job
    _sync(ver)
    prod = _W['prod']
    U = _W['U']
    out = []
    for tag, key, u, v, rel, a in items:
        if v is None:
            xt = _term(u, 'H'); yt = QD
        else:
            xt, yt = _pair_terms(u, v, rel)
        prod.host.clear()
        s = prod.produce(0, xt, yt, a, U.K, U.V)
        out.append((tag, key, s))
    return out


def _wild_job(job):
    ver, items, dummy = job
    _sync(ver)
    U = _W['U']
    w = _W.setdefault('wild', Wild())
    dm = _term(dummy, 'H')
    out = []
    n = C.ID['CHKS']
    for t, sid in items:
        a, s = U.scripts[sid]
        xs = key_term(U, (t, (sid,) if a == 'C' else (), (sid,) if a == 'D' else ()), 'C')
        q = dm if a == 'C' else QD
        v = C.mk_arg(U.V, xs, q, a, U.K)
        Rb = ('cbox', n, v); Sb = ('cbox', n, C.swap_arg(v))
        w.clear()
        ok, usesS, _ = w.vone(0, v, Rb, Sb)
        out.append((t, sid, bool(ok), bool(usesS)))
    return out


# ----------------------------------------------------------------------------------------------------------------
# Main side: dense tables over units
# ----------------------------------------------------------------------------------------------------------------
class Tables:
    """CH[a] (cap x cap int8), UVt (cap x 6 int8), wild screen, production memos."""

    def __init__(self, U, pool, verbose=True, chunk=2500, sync_dir=None):
        self.U, self.pool, self.verbose, self.chunk = U, pool, verbose, chunk
        self.sync_dir = sync_dir or SYNC
        self.cap = 0
        self.CH = {'C': np.zeros((0, 0), np.int8), 'D': np.zeros((0, 0), np.int8)}
        self.UVt = np.zeros((0, 6), np.int8)
        self.wild = {}               # (τ, sid) -> (ok, usesS)
        self.prodC = {}              # (τ, code) -> sid or -1
        self.prodD = {}              # (τ, code) -> sid or -1
        self.prod_rep = {}           # memo key -> representative (u, v, rel)
        self.n_checks = 0
        self.t_checks = 0.0
        self._grow()

    def _grow(self):
        n = len(self.U.units)
        if n <= self.cap: return
        cap = max(n, int(self.cap * 1.3) + 256)
        for a in ('C', 'D'):
            old = self.CH[a]
            new = np.full((cap, cap), -1, np.int8)
            new[:old.shape[0], :old.shape[1]] = old
            self.CH[a] = new
        old = self.UVt
        new = np.full((cap, 6), -1, np.int8); new[:old.shape[0]] = old
        self.UVt = new
        self.cap = cap

    def uvv(self, u, a, opp):
        if not self.U.has_entry(u, a): return 0
        return int(self.UVt[u, UVI[(a, opp)]])

    def publish(self):
        """Write the current scripts and units for the workers (a new version when either grew)."""
        import pickle
        U = self.U
        state = (len(U.scripts), len(U.units))
        if getattr(self, '_pub', None) == state: return self.ver
        self.ver = getattr(self, 'ver', -1) + 1
        os.makedirs(self.sync_dir, exist_ok=True)
        tmp = os.path.join(self.sync_dir, 'v%d.tmp' % self.ver)
        with open(tmp, 'wb') as f:
            pickle.dump((list(U.scripts), list(U.units)), f)
        os.replace(tmp, os.path.join(self.sync_dir, 'v%d.pkl' % self.ver))
        self._pub = state
        return self.ver

    def ensure_uv(self, units):
        self._grow()
        todo = [int(u) for u in units if self.UVt[u, 0] < 0]
        if not todo: return
        ver = self.publish()
        jobs = [(ver, todo[i:i + 200]) for i in range(0, len(todo), 200)]
        t0 = time.time()
        for res in self.pool.imap_unordered(_uv_job, jobs):
            for u, k, v in res:
                self.UVt[u, k] = v
        if self.verbose: print('    uv: %d units (%.0fs)' % (len(todo), time.time() - t0), flush=True)

    def ensure_pairs(self, a, ts, ms, label=''):
        """Fill CH[a] at the pairs (ts[i], ms[i]) (numpy arrays; t == m is the twin instance).  Targets without an
        a-entry are F without running (the code's empty selection)."""
        self._grow()
        U = self.U
        CH = self.CH[a]
        ts = np.asarray(ts, np.int64); ms = np.asarray(ms, np.int64)
        if len(ts) == 0: return 0
        keep = CH[ts, ms] < 0
        ts, ms = ts[keep], ms[keep]
        n = len(U.units)
        has = np.array([U.has_entry(u, a) for u in range(n)])
        noent = ~has[ts]
        CH[ts[noent], ms[noent]] = 0
        ts, ms = ts[~noent], ms[~noent]
        if len(ts) == 0: return 0
        order = np.lexsort((ms, ts))
        ts, ms = ts[order], ms[order]
        keys, starts = np.unique(ts, return_index=True)
        ends = np.append(starts[1:], len(ts))
        ver = self.publish()
        jobs = []
        for t, s0, s1 in zip(keys.tolist(), starts.tolist(), ends.tolist()):
            mm = np.unique(ms[s0:s1])
            for i in range(0, len(mm), self.chunk):
                jobs.append((ver, a, t, mm[i:i + self.chunk].tolist()))
        tot = int(sum(len(j[3]) for j in jobs))
        t0 = time.time()
        done = 0
        if self.verbose: print('    %s pair checks %s: %d in %d jobs' % (a, label, tot, len(jobs)), flush=True)
        for a_, t, out, secs in self.pool.imap_unordered(_chk_job, jobs, chunksize=1):
            for m, v in out:
                CH[t, m] = v
            done += len(out)
            if self.verbose and done // 2000000 != (done - len(out)) // 2000000:
                print('      %d / %d (%.0fs)' % (done, tot, time.time() - t0), flush=True)
        self.n_checks += tot; self.t_checks += time.time() - t0
        if self.verbose: print('    %s pair checks %s done: %d (%.0fs)' % (a, label, tot, time.time() - t0), flush=True)
        return tot

    def ensure_wild(self, items, dummy_unit):
        todo = sorted({it for it in items if it not in self.wild})
        if not todo: return
        ver = self.publish()
        jobs = [(ver, todo[i:i + 500], int(dummy_unit)) for i in range(0, len(todo), 500)]
        for res in self.pool.imap_unordered(_wild_job, jobs):
            for t, sid, ok, uS in res:
                self.wild[(t, sid)] = (ok, uS)

    def uv_arrays(self):
        """{(a, opp): raw value array over units (0 F, 1 T, 2 TO; 0 without an a-entry)} and has-entry arrays."""
        U = self.U
        n = len(U.units)
        has = {a: np.array([U.has_entry(u, a) for u in range(n)]) for a in ('C', 'D')}
        out = {}
        for (a, opp), i in UVI.items():
            v = self.UVt[:n, i].astype(np.int64)
            out[(a, opp)] = np.where(has[a] & (v >= 0), v, 0)
        return out, has

    def sig_codes_C(self, u, vs, relc, UVA, has):
        """Signature codes of PROD(u, v, C) for the opponents vs (relc: 0 distinct, 1 twin, 2 same quote).
        Per atom: 0 F, 1 T, 4 TO (a box value; TO matters because a regressing nested check exhausts the
        production cap in the executable producer), 2 the root's R, 3 its S; code = 25 * self + 5 * c0 + c1."""
        U = self.U
        t = U.units[u][0]
        n = len(vs)
        selfm = relc == 2
        code = selfm.astype(np.int64) * 25
        for i, (k, ai, qi) in enumerate(U.tau_kinds[t]):
            a = 'C' if ai == 0 else 'D'
            q = '^C' if qi == 0 else '^D'
            if k == 0:
                c = 3 if a == 'C' else val3(np.where(has['D'][vs], self.CH['D'][vs, u], 0))
            elif k == 1:
                c = 2 if a == 'C' else (val3(self.CH['D'][u, vs]) if has['D'][u] else 0)
            elif k == 2:
                c = val3(UVA[(a, 'self')][vs])
            elif k == 3:
                c = val3(UVA[(a, 'self')][u])
            elif k == 4:
                c = val3(UVA[(a, q)][vs])
            else:
                c = val3(UVA[(a, q)][u])
            c = np.broadcast_to(np.asarray(c, np.int64), (n,)).copy()
            if k in (0, 1, 2, 3):
                c[selfm] = 2 if a == 'C' else int(val3(UVA[('D', 'self')][u]))
            if k == 4:
                c[selfm] = int(val3(UVA[(a, q)][u]))
            code += c * (5 if i == 0 else 1)
        return code

    def sig_code_D(self, u):
        """Signature code of PROD(u, ⌜D⌝, D) (codes as sig_codes_C)."""
        U = self.U
        t = U.units[u][0]
        code = 0
        for i, (k, ai, qi) in enumerate(U.tau_kinds[t]):
            a = 'C' if ai == 0 else 'D'
            if k == 0: c = 3 if a == 'D' else 0
            elif k == 1: c = 2 if a == 'D' else int(val3(self.uvv(u, 'C', '^D')))
            elif k == 2: c = 0
            elif k == 3: c = int(val3(self.uvv(u, a, 'self')))
            elif k == 4: c = 0
            else:
                if qi == 1 and a == 'D': c = 2
                else: c = int(val3(self.uvv(u, a, '^C' if qi == 0 else '^D')))
            code += c * (5 if i == 0 else 1)
        return code

    def run_productions(self, items):
        """items: [(memo, key, u, v or None, rel, a)]; computes the memo entries not yet present (one
        representative pair per signature)."""
        U = self.U
        todo = {}
        for memo, key, u, v, rel, a in items:
            tag = 'C' if memo is self.prodC else 'D'
            if key in memo or (tag, key) in todo: continue
            todo[(tag, key)] = (tag, key, int(u), (None if v is None else int(v)), rel, a)
        if not todo: return
        for (tag, key), it in todo.items():
            self.prod_rep[(tag, key)] = it[2:5]
        ver = self.publish()
        lst = list(todo.values())
        jobs = [(ver, lst[i:i + 40]) for i in range(0, len(lst), 40)]
        t0 = time.time()
        for res in self.pool.imap_unordered(_prod_job, jobs):
            for tag, key, s in res:
                memo = self.prodC if tag == 'C' else self.prodD
                memo[key] = -1 if s is None else U.script(tag, s, 'search')
        if self.verbose: print('    productions: %d (%.0fs)' % (len(lst), time.time() - t0), flush=True)


# ----------------------------------------------------------------------------------------------------------------
# The closure of the unit universe under the modes' transitions, and the final tables
# ----------------------------------------------------------------------------------------------------------------
LMAX = 6


def blocks(U, n):
    """Padded blocks BL[a][u, k] (sid or -1) for units 0..n-1."""
    BL = {a: np.full((n, LMAX), -1, np.int64) for a in ('C', 'D')}
    for u in range(n):
        t, cs, ds = U.units[u]
        assert len(cs) <= LMAX and len(ds) <= LMAX
        BL['C'][u, :len(cs)] = cs
        BL['D'][u, :len(ds)] = ds
    return BL


class Closure:
    """Reachable units by mode: H fixed at H lists; S, C, CS start from every E and H unit (the empty and the
    identical-inventory starts) and close under the transitions against every reachable unit."""

    def __init__(self, Tb, verbose=True):
        self.Tb, self.U, self.verbose = Tb, Tb.U, verbose
        U = self.U
        base = set(U.H_unit.tolist()) | set(U.E_unit.tolist())
        self.reach = {m: set(base) for m in ('S', 'C', 'CS')}
        self.reach['H'] = set(U.H_unit.tolist())
        self.single = {}            # (τ, sid) -> unit id of the single-entry unit (when wild-compatible)
        self.trC = {}               # u -> dict v -> u' (only changes), for u reachable in C or CS
        self.dummy = int(U.H_unit[0])

    def O(self):
        return sorted(set().union(*self.reach.values()))

    def run(self, max_rounds=12):
        Tb, U = self.Tb, self.U
        for rnd in range(max_rounds):
            t0 = time.time()
            n_before = sum(len(v) for v in self.reach.values())
            O = self.O()
            Tb._grow()
            Tb.ensure_uv(O)
            # D values for signatures (and composition): rows of R_D askers, columns of S_D askers
            rowsD = [u for u in O if any(k == (1, 1, 0) for k in U.tau_kinds[U.units[u][0]]) and U.has_entry(u, 'D')]
            colsD = [u for u in O if any(k == (0, 1, 0) for k in U.tau_kinds[U.units[u][0]])]
            self._ensure_sub('D', rowsD, colsD, O)
            # wild screen for every (τ, script) carried by a reachable unit
            sids = sorted({s for u in O for s in U.units[u][1] + U.units[u][2]})
            Tb.ensure_wild([(t, s) for t in range(U.T) for s in sids], self.dummy)
            for (t, s), (ok, _) in Tb.wild.items():
                if ok and (t, s) not in self.single:
                    self.single[(t, s)] = U.single_unit(t, s)
            Tb._grow()
            # adoption checks: singles (C) against every reachable donor carrying the script; singles (D) vs ⌜D⌝
            donors = defaultdict(list)
            for u in O:
                for s in U.units[u][1]: donors[s].append(u)
            tl, ml = [], []
            compat = defaultdict(list)
            for (t, s_) in self.single:
                compat[t].append(s_)
            ac_units = set()
            for u in sorted(self.reach['C'] | self.reach['CS']):
                t, cs, ds = U.units[u]
                for s_ in compat.get(t, []):
                    a_ = U.scripts[s_][0]
                    if (a_ == 'C' and cs) or (a_ == 'D' and ds): continue
                    xs = U.append(u, s_)
                    ac_units.add(xs)
                    if a_ == 'C' and donors.get(s_):
                        d = np.asarray(donors[s_], np.int64)
                        tl.append(np.full(len(d), xs, np.int64)); ml.append(d)
            Tb._grow()
            Tb.ensure_uv(sorted(set(self.single.values()) | ac_units))
            if tl: Tb.ensure_pairs('C', np.concatenate(tl), np.concatenate(ml), label='(adoption)')
            # C successors
            new = defaultdict(set)
            cu = sorted(self.reach['C'] | self.reach['CS'])
            succC = self.successors_C(cu, O)
            self.trC = succC
            for u, (vs_, u2s) in succC.items():
                us2 = set(u2s.tolist())
                if u in self.reach['C']: new['C'] |= us2
                if u in self.reach['CS']: new['CS'] |= us2
            # S successors (gate rows first: S/CS-reachable units with a C entry, against every reachable unit)
            su = set(self.reach['S'])
            cs_units = set(self.reach['CS'])
            for u in self.reach['CS']:
                if u in succC: cs_units |= set(succC[u][1].tolist())
            su_all = sorted(su | cs_units)
            Tb._grow()
            Tb.ensure_uv(su_all)
            rowsD2 = [u for u in su_all if any(k == (1, 1, 0) for k in U.tau_kinds[U.units[u][0]]) and U.has_entry(u, 'D')]
            colsD2 = [u for u in su_all if any(k == (0, 1, 0) for k in U.tau_kinds[U.units[u][0]])]
            self._ensure_sub('D', rowsD2, colsD2, O)

            succS = self.successors_S(su_all, O)
            for u, outs in succS.items():
                if u in su: new['S'] |= outs
                if u in cs_units: new['CS'] |= outs
            for m in ('S', 'C', 'CS'):
                self.reach[m] |= new[m]
            n_after = sum(len(v) for v in self.reach.values())
            if self.verbose:
                print('  closure round %d: reach %s, units %d, scripts %d (%.0fs)' % (
                    rnd, {m: len(v) for m, v in self.reach.items()}, len(U.units), len(U.scripts), time.time() - t0), flush=True)
            if n_after == n_before:
                return rnd
        raise RuntimeError('closure did not converge')

    def _ensure_sub(self, a, rows, cols, O):
        """CH[a] restricted to reachable opponents: rows x O and O x cols."""
        Tb = self.Tb
        CH = Tb.CH[a]
        Oa = np.asarray(O, np.int64)
        tl, ml = [], []
        for u in rows:
            miss = Oa[CH[u, Oa] < 0]
            if len(miss): tl.append(np.full(len(miss), u, np.int64)); ml.append(miss)
        for u in cols:
            miss = Oa[CH[Oa, u] < 0]
            if len(miss): tl.append(miss); ml.append(np.full(len(miss), u, np.int64))
        if not tl: return
        Tb.ensure_pairs(a, np.concatenate(tl), np.concatenate(ml), label='(%d rows, %d cols)' % (len(rows), len(cols)))

    def single_array(self):
        U = self.U
        S = np.full((U.T, len(U.scripts)), -1, np.int64)
        for (t, sid), xs in self.single.items():
            S[t, sid] = xs
        return S

    def successors_C(self, units, O):
        """For each u, (vs, u2s): the reachable opponents v that change u, and the unit u becomes (distinct
        quotes; self-play changes nothing).  First valid entry per outcome in the donor's order."""
        Tb, U = self.Tb, self.U
        Oa = np.asarray(O)
        n = len(U.units)
        BL = blocks(U, n)
        SINGLE = self.single_array()
        CHC = Tb.CH['C']
        UVDD = Tb.UVt[:, UVI[('D', '^D')]]
        out = {}
        for u in units:
            t, cs, ds = U.units[u]
            R = {}
            for a, held in (('C', cs), ('D', ds)):
                Ra = np.full(len(Oa), -1, np.int64)
                heldA = np.array(held, np.int64)
                if len(held):           # rule 'lack': an outcome with an entry is not copied for
                    R[a] = Ra
                    continue
                for k in range(LMAX):
                    sk = BL[a][Oa, k]
                    cand = (sk >= 0) & (Ra < 0)
                    if not cand.any(): continue
                    if len(heldA): cand &= ~np.isin(sk, heldA)
                    xs = np.where(cand, SINGLE[t, np.where(sk >= 0, sk, 0)], -1)
                    valid = xs >= 0
                    if not valid.any(): continue
                    # the adoption check reads the would-be self u + s (notes §1.15); the single-entry unit is the screen
                    xs = xs.copy()
                    for j in np.nonzero(valid)[0].tolist():
                        xs[j] = U.append(u, int(sk[j]))
                    ok = np.zeros(len(Oa), bool)
                    if a == 'C':
                        vals = CHC[xs[valid], Oa[valid]]
                        assert (vals >= 0).all(), 'adoption check not computed'
                        ok[valid] = vals == 1
                    else:
                        ok[valid] = UVDD[xs[valid]] == 1
                    Ra[ok] = sk[ok]
                R[a] = Ra
            ch = np.nonzero((R['C'] >= 0) | (R['D'] >= 0))[0]
            if len(ch):
                memo = {}
                u2s = np.empty(len(ch), np.int64)
                for i, j in enumerate(ch.tolist()):
                    key = (int(R['C'][j]), int(R['D'][j]))
                    u2 = memo.get(key)
                    if u2 is None:
                        u2 = u
                        if key[0] >= 0: u2 = U.append(u2, key[0])
                        if key[1] >= 0: u2 = U.append(u2, key[1])
                        memo[key] = u2
                    u2s[i] = u2
                out[u] = (Oa[ch].copy(), u2s)
        Tb._grow()
        return out

    def successors_S(self, units, O):
        """For each u, the set of units the S step can produce against the reachable opponents and itself (gate
        from CH; production by signature; then the D production if the list has no D entry)."""
        Tb, U = self.Tb, self.U
        Oa = np.asarray(O)
        UVA, has = Tb.uv_arrays()
        items = []
        plan = {}
        for u in units:
            t = U.units[u][0]
            vs = np.concatenate([Oa, [u]])
            relc = np.where(vs == u, 1, 0); relc[-1] = 2
            if has['C'][u]:             # rule 'lack': a C entry ends the C production
                need = np.zeros(len(vs), bool)
            else:
                need = np.ones(len(vs), bool)
            if not need.any():
                plan[u] = []
                continue
            codes = Tb.sig_codes_C(u, vs, relc, UVA, has)
            uc, first = np.unique(codes[need], return_index=True)
            idx = np.nonzero(need)[0][first]
            plan[u] = [int(c) for c in uc]
            for c, j in zip(uc.tolist(), idx.tolist()):
                rel = 's' if relc[j] == 2 else ('w' if relc[j] == 1 else 'd')
                items.append((Tb.prodC, (t, c), u, int(vs[j]), rel, 'C'))
        Tb.run_productions(items)
        out = {}
        for u, codes in plan.items():
            outs = {u}
            for c in codes:
                s = Tb.prodC[(U.units[u][0], c)]
                if s >= 0: outs.add(U.append(u, s))
            out[u] = outs
        Tb._grow()
        allo = sorted({x for v in out.values() for x in v})
        Tb.ensure_uv(allo)
        ditems = []
        for u2 in allo:
            if not U.has_entry(u2, 'D'):
                ditems.append((Tb.prodD, (U.units[u2][0], Tb.sig_code_D(u2)), u2, None, 'D', 'D'))
        Tb.run_productions(ditems)
        final = {}
        for u, outs in out.items():
            fo = set()
            for u2 in outs:
                if not U.has_entry(u2, 'D'):
                    s = Tb.prodD[(U.units[u2][0], Tb.sig_code_D(u2))]
                    fo.add(U.append(u2, s) if s >= 0 else u2)
                else:
                    fo.add(u2)
            final[u] = fo
        Tb._grow()
        return final


def val3(x):
    """Raw check value (0 F, 1 T, 2 TO) -> signature digit (0, 1, 4)."""
    x = np.asarray(x)
    return np.where(x == 1, 1, np.where(x == 2, 4, 0))


def has_kind(U, u, kind):
    return any(k == kind for k in U.tau_kinds[U.units[u][0]])


def finalize(cl, verbose=True):
    """After the closure: composition needs, the action table, self-play actions, split units, and the kernel's
    transition arrays.  Returns a dict of arrays (global unit ids; entries for unreachable units unused)."""
    Tb, U = cl.Tb, cl.U
    t0 = time.time()
    O = cl.O()
    Oa = np.asarray(O, np.int64)
    # composition needs: R_a askers' rows, S_a askers' columns, over the reachable units
    for a, ai in (('C', 0), ('D', 1)):
        rows = [u for u in O if has_kind(U, u, (1, ai, 0)) and U.has_entry(u, a)]
        cols = [u for u in O if has_kind(U, u, (0, ai, 0))]
        cl._ensure_sub(a, rows, cols, O)
    Tb.ensure_uv(O)
    n = len(U.units)
    UVR, has = Tb.uv_arrays()
    UVA = {k: v == 1 for k, v in UVR.items()}
    CHC, CHD = Tb.CH['C'][:n, :n], Tb.CH['D'][:n, :n]
    CHv = {'C': CHC, 'D': CHD}
    A = np.full((n, n), -1, np.int8)
    selfa = np.full(n, -1, np.int8)
    sub = np.ix_(Oa, Oa)
    for x in O:
        t = U.units[x][0]

        def val(at, x=x):
            k, ai, qi = atom_box_kind(at)
            a = 'C' if ai == 0 else 'D'
            q = '^C' if qi == 0 else '^D'
            if k == 0:
                v = CHv[a][Oa, x]; assert (v >= 0).all(); return (v == 1) & has[a][Oa]
            if k == 1:
                if not has[a][x]: return np.zeros(len(Oa), bool)
                v = CHv[a][x, Oa]; assert (v >= 0).all(); return v == 1
            if k == 2: return UVA[(a, 'self')][Oa]
            if k == 3: return np.full(len(Oa), bool(UVA[(a, 'self')][x]))
            if k == 4: return UVA[(a, q)][Oa]
            return np.full(len(Oa), bool(UVA[(a, q)][x]))

        r = CP.eval_dt(U.tau_dt[t], val)
        if not isinstance(r, np.ndarray): r = np.full(len(Oa), r)
        A[x, Oa] = r.astype(np.int8)

        def sval(at, x=x):
            k, ai, qi = atom_box_kind(at)
            a = 'C' if ai == 0 else 'D'
            q = '^C' if qi == 0 else '^D'
            if k in (0, 1, 2, 3): return bool(UVA[(a, 'self')][x])
            return bool(UVA[(a, q)][x])
        selfa[x] = CP.eval_dt(U.tau_dt[t], sval)
    # split units: the twin play differs from the self play (as an action pair)
    split = np.zeros(n, bool)
    for x in O:
        split[x] = (A[x, x] != selfa[x])
    # kernel arrays
    utau = np.array([U.units[u][0] for u in range(n)], np.int64)
    BL = blocks(U, n)
    ns = len(U.scripts)
    SINGLE = cl.single_array()
    APP = np.full((n, ns), -1, np.int64)
    for u in range(n):
        t, cs, ds = U.units[u]
        for sid in range(ns):
            if U.scripts[sid][0] == 'C':
                k = (t, cs, ds) if sid in cs else (t, cs + (sid,), ds)
            else:
                k = (t, cs, ds) if sid in ds else (t, cs, ds + (sid,))
            APP[u, sid] = U.uid.get(k, -1)
    PRODC = np.full((U.T, 64), -2, np.int64)
    for (t, c), sid in Tb.prodC.items():
        PRODC[t, c] = sid
    PD = np.arange(n, dtype=np.int64)
    PDCODE = np.full(n, -1, np.int64)
    pd_missing = 0
    for u in range(n):
        if U.has_entry(u, 'D'): continue
        if Tb.UVt[u, 0] < 0: continue
        key = (U.units[u][0], Tb.sig_code_D(u))
        PDCODE[u] = key[1]
        sid = Tb.prodD.get(key)
        if sid is None:
            pd_missing += 1; PD[u] = -2; continue
        if sid >= 0:
            PD[u] = APP[u, sid]
    KIND = np.full((U.T, 2, 3), -1, np.int64)
    NAT = np.zeros(U.T, np.int64)
    for t in range(U.T):
        NAT[t] = len(U.tau_kinds[t])
        for i, kk in enumerate(U.tau_kinds[t]):
            KIND[t, i] = kk
    reach = {m: np.array(sorted(v), np.int64) for m, v in cl.reach.items()}
    if verbose:
        print('finalize: reachable units %d, split %d, PD missing %d, checks %d (%.0fs)' % (
            len(O), int(split[Oa].sum()), pd_missing, Tb.n_checks, time.time() - t0), flush=True)
    return dict(A=A, selfa=selfa, split=split, utau=utau, BLC=BL['C'], BLD=BL['D'], SINGLE=SINGLE, APP=APP,
                PRODC=PRODC, PD=PD, PDCODE=PDCODE, KIND=KIND, NAT=NAT, O=Oa, CHC=CHC.copy(), CHD=CHD.copy(),
                UVt=Tb.UVt[:n].copy(), **{'reach_' + m: v for m, v in reach.items()})


def save_static(st, U, Tb, cl, path):
    """Arrays as separate .npy files in the directory `path` (loaded memory-mapped by the lottery workers)."""
    os.makedirs(path, exist_ok=True)
    for k, v in st.items():
        if isinstance(v, np.ndarray):
            np.save(os.path.join(path, k + '.npy'), v)
    meta = dict(scripts=U.scripts, units=U.units, sorigin=U.sorigin, prodC=Tb.prodC, prodD=Tb.prodD,
                prod_rep=Tb.prod_rep, wild=Tb.wild, single=cl.single, n_checks=Tb.n_checks, t_checks=Tb.t_checks,
                H_unit=U.H_unit, E_unit=U.E_unit, time_s=st.get('time_s'))
    with open(os.path.join(path, 'meta.pkl'), 'wb') as f:
        pickle.dump(meta, f)


def load_static(path, mmap=True):
    st = {}
    for fn in os.listdir(path):
        if fn.endswith('.npy'):
            st[fn[:-4]] = np.load(os.path.join(path, fn), mmap_mode='r' if mmap else None)
    with open(os.path.join(path, 'meta.pkl'), 'rb') as f:
        meta = pickle.load(f)
    return st, meta
