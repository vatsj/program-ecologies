"""Does churn among the fair pairs happen in the primary object? (spec specs/2026-10-25-churn-primary.md; notes
notes/churn-primary.md; predictions predictions/2026-10-25-churn-primary.md.)

The primary object is the eps = 0 seed lottery of programs that read each other and play encounter by encounter, with
no contracts and no veto: three slot populations per island, mean-field expected payoffs, Moran birth-death with
fitness weight exp(w * payoff), migration m = mN / N per birth.  The kernel is the stored baseline's
(migration_window_kernels.kern_mw, imported, not edited); what changes between the arms is the catalogue of programs
and the joint table that says what each triple of programs plays:

  E, E'   the standing DSL of dollar3 at n = 10 (modalPA evaluator = E, weak evaluator = E'), length prior;
  B6w/m   the same at n = 6 (the stored baseline, rerun);
  E-min   the n <= 6 catalogue plus the explicit two-partner reader family, doses lo / main / hi;
  T       the arm-T library of churn_primary_t.py (programs of L_T^code reading each other by capped simulation).

Importable without side effects; the drivers are in churn_primary_run.py.
"""
import json, os, sys, time, zlib, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dollar3 as D
import stable_sets as SS
import stable_sets_run as SR
import migration_window as MW
import migration_window_kernels as MK

ROOT = SS.ROOT
T = MW.T
V = MW.V
W = SS.W
HELD = 25
NOUT = MW.NOUT
CATMAP = MW.CATMAP
ISFAIR = np.zeros(NOUT, bool)
ISFAIR[V] = True
MNS = (0, 0.01, 0.1, 1)
SNAPS = (1000, 2000, 5000, 10000)


def run_seed(base, r):
    return SR.run_seed(base, r)


# ====================================================================== the DSL catalogues
class DSLCat:
    """A catalogue of canonical functions of the dollar3 DSL (the weak / modalPA grammar), an evaluator and a seed law.

    name     label
    n        grammar size bound
    evalr    'modalPA' or 'weak'
    dose     None for the plain length prior; (w_single, w_two) for E-min (n <= 6 plus the explicit readers)
    """
    kind = 'dsl'

    def __init__(self, name, n=6, evalr='modalPA', dose=None):
        self.name = name; self.n = n; self.evalr = evalr; self.armi = D.ARM[evalr]; self.dose = dose
        L, S0, mu, cnt, size = D.build('modalPA', n)
        self.size0 = size
        if dose is None:
            self.S = S0; self.mu = mu
            self.K0 = len(mu); self.extra = {}
        else:
            self.K0 = len(mu)
            extra = {}
            forms = []
            for s in range(3):
                for key, f in reader_forms(s).items():
                    if key.startswith('R2'):
                        extra[(s, key)] = self.K0 + len(forms); forms.append(f)
            self.S = D.Slots(list(S0.fs) + forms)
            self.mu = np.concatenate([mu, np.zeros(len(forms))])
            self.extra = extra
        S = self.S
        self.K = len(self.mu)
        self.is_reader = (S.nat > 0)            # (3, K): non-constant classes
        self.idx = {}                            # name -> class index per slot, for the named readers
        if dose is not None:
            for s in range(3):
                for key, f in reader_forms(s).items():
                    if key.startswith('R2'):
                        self.idx[(s, key)] = self.extra[(s, key)]
                    else:
                        self.idx[(s, key)] = S.index[s][f]

    def law(self, s):
        if self.dose is None:
            return self.mu / self.mu.sum()
        wS, wD = self.dose
        p = np.zeros(self.K)
        p[:self.K0] = (1 - wS - wD) * self.mu[:self.K0] / self.mu[:self.K0].sum()
        singles = [self.idx[(s, k)] for k in ('Sj', 'Sk', 'Zj', 'Zk')]
        twos = [self.idx[(s, k)] for k in ('R2jf', 'R2jz', 'R2kf', 'R2kz')]
        for x in singles:
            p[x] += wS / 4
        for x in twos:
            p[x] += wD / 4
        return p

    def make_J(self, U, price=0.0):
        Kmax = max(len(u) for u in U)
        Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
        S = self.S
        J = SS._joint_table(self.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, Up[0], Up[1], Up[2])
        return J, T.PAY, T.VEC

    def src(self, s, x):
        return self.S.src(s, x)

    def reader_mask(self, s):
        return self.is_reader[s]


def reader_forms(s):
    """Canonical forms (atoms, table) of the explicit reader families of slot s (notes 1.4).  Keys: Sj, Sk (fair
    switchers: accept that partner's half offer, otherwise name the other at 1/2), Zj, Zk (single readers with null
    fallback), R2{j,k}{f,z} (two-partner readers: first partner j or k, fallback stay-with-first or null)."""
    j, k = D.others(s)
    aj = (0, 0, D.local_of(j, s, 1)); ak = (0, 1, D.local_of(k, s, 1))
    sj = D.local_of(s, j, 1); sk = D.local_of(s, k, 1)
    R = D.Lang._reduce
    out = {
        'Sj': R([aj], [sk, sj]), 'Sk': R([ak], [sj, sk]),
        'Zj': R([aj], [D.NULL_LOCAL, sj]), 'Zk': R([ak], [D.NULL_LOCAL, sk]),
    }
    for first, fb in (('j', 'f'), ('j', 'z'), ('k', 'f'), ('k', 'z')):
        st1 = sj if first == 'j' else sk
        fbv = st1 if fb == 'f' else D.NULL_LOCAL
        tab = []
        for v in range(4):
            a0 = bool(v & 1); a1 = bool(v & 2)
            if first == 'j':
                tab.append(sj if a0 else (sk if a1 else fbv))
            else:
                tab.append(sk if a1 else (sj if a0 else fbv))
        out['R2%s%s' % (first, fb)] = R([aj, ak], tab)
    return out


_CATS = {}
_TBASE = None


class TView:
    """One dose of the arm-T library, sharing the execution tables of the single TCat."""
    kind = 'lt'

    def __init__(self, tcat, dose, name):
        self.t = tcat; self.dose = dose; self.name = name

    def __getattr__(self, k):
        return getattr(self.t, k)

    def make_J(self, U, price=0.0):
        return self.t.make_J(U, price, T.PAY, T.VEC)


def get_cat(spec, cache_dir=None):
    """spec: 'B6w', 'B6m', 'E10m', 'E10w', 'Emin-{lo,main,hi}-{m,w}', 'T-{lo,main,hi}'."""
    if spec in _CATS:
        return _CATS[spec]
    if spec == 'B6w':
        c = DSLCat(spec, 6, 'weak')
    elif spec == 'B6m':
        c = DSLCat(spec, 6, 'modalPA')
    elif spec == 'E10m':
        c = DSLCat(spec, 10, 'modalPA')
    elif spec == 'E10w':
        c = DSLCat(spec, 10, 'weak')
    elif spec.startswith('Emin-'):
        _, dose, ev = spec.split('-')
        wS, wD = EMIN_DOSE[dose]
        c = DSLCat(spec, 6, 'modalPA' if ev == 'm' else 'weak', dose=(wS, wD))
    elif spec.startswith('T-'):
        import churn_primary_t as CT
        global _TBASE
        if _TBASE is None:
            _TBASE = CT.TCat(cache_dir=cache_dir)
        c = TView(_TBASE, spec.split('-')[1], spec)
    else:
        raise ValueError(spec)
    _CATS[spec] = c
    return c


EMIN_DOSE = {'lo': (0.087, 0.003), 'main': (0.06, 0.03), 'hi': (0.06, 0.10)}


def cat_law(cat, s):
    if cat.kind == 'dsl':
        return cat.law(s)
    w = cat.law(cat.dose)
    return w / w.sum()


def is_reader_class(cat, s, x):
    if cat.kind == 'dsl':
        return bool(cat.is_reader[s, x])
    return bool(cat.is_reader[x])


# ====================================================================== founders and one run
def founders(cat, base, r, I=64, N=100):
    """init counts (I, 3, K) and the run's kernel seed.  B6w uses the migration-window founders exactly."""
    rng = np.random.default_rng(run_seed(base, r))
    laws = [cat_law(cat, s) for s in range(3)]
    init = SS.draw_seeds(rng, I, N, laws)
    return init, run_seed(base, r) % (2 ** 31)


def prepare(cat, base, r, I=64, N=100, price=0.0):
    init, seed = founders(cat, base, r, I, N)
    loc, U = SS.compress(init)
    J, PAY, VEC = cat.make_J(U, price)
    return dict(cat=cat, loc=loc, U=U, J=J, PAY=PAY, VEC=VEC, seed=seed, N=N, I=I)


def kernel(prep, mN, H, seed=None, evcap=200000):
    out = MK.kern_mw(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, prep['loc'], prep['N'], W, mN / prep['N'],
                     prep['seed'] if seed is None else seed, H, 10, np.zeros(0, np.int64), evcap)
    status, stop, counts, cls, eff, dist, ev, nev, nmig, modal, effm, fairm = out
    return dict(status=int(status), stop=int(stop), counts=counts, cls=cls, ev=ev, nev=int(nev), nmig=int(nmig),
                modal=modal, effm=effm, fairm=fairm)


# ====================================================================== statistics
def flips(modal, L=HELD):
    """debounced changes of each island's modal outcome (as immigrant_rejection.flips): per island a list of
    (g, from, to), g the first generation of the new value, accepted if it persists L generations or to the end."""
    G, I = modal.shape
    out = []
    for i in range(I):
        s = modal[:, i]
        cands = np.nonzero(s[1:] != s[:-1])[0] + 1
        last = s[0]; ch = []; j = 0
        while j < len(cands):
            g = int(cands[j])
            if s[g] != last and (g + L > G or (s[g:g + L] == s[g]).all()):
                ch.append((g, int(last), int(s[g]))); last = s[g]
                j = int(np.searchsorted(cands, g + L))
            else:
                j += 1
        out.append(ch)
    return out


def flip_counts(fl, modal, stop):
    """m->m, m->o, o->m, o->o counts, the fair-pair island-generations at risk up to the stop generation, m->m by
    pair type and by tenth of the horizon."""
    G = modal.shape[0] - 1
    c = dict(mm=0, mo=0, om=0, oo=0)
    pairs = {}
    win = np.zeros(10, np.int64)
    for i, ch in enumerate(fl):
        for g, a, b in ch:
            if g > stop:
                continue
            k = ('m' if ISFAIR[a] else 'o') + ('m' if ISFAIR[b] else 'o')
            c[k] += 1
            if k == 'mm':
                key = '%s>%s' % (MW.OLAB[a], MW.OLAB[b])
                pairs[key] = pairs.get(key, 0) + 1
                win[min(9, g * 10 // max(G, 1))] += 1
    expo = int(ISFAIR[modal[:stop + 1]].sum())
    c.update(expo=expo, pairs=pairs, win=win.tolist())
    return c


def flip_routes(fl, ev, nev, evcap, loc_U, cat, stop, window=30):
    """For each m->m flip: 'redirect' (no majority-class change on the island within +-window generations),
    'resident' (a majority-class change occurred and every dominant class at the flip is a constant), 'reader' (a
    majority-class change occurred and at least one slot's dominant class is a reader).  ev rows: gen, island, slot,
    old, new (local class index), intro, t10, dpay.  Returns counts and the number of events (overflow flag)."""
    out = dict(redirect=0, resident=0, reader=0, overflow=bool(nev > evcap))
    if ev is None or len(ev) == 0:
        ev = np.zeros((0, 8))
    byisl = {}
    for e in ev:
        byisl.setdefault(int(e[1]), []).append(e)
    for i, ch in enumerate(fl):
        evs = byisl.get(i, [])
        for g, a, b in ch:
            if g > stop or not (ISFAIR[a] and ISFAIR[b]):
                continue
            near = [e for e in evs if g - window <= e[0] <= g + window and e[0] > 0]
            if not near:
                out['redirect'] += 1
                continue
            dom = [-1, -1, -1]
            for e in evs:
                if e[0] <= g:
                    dom[int(e[2])] = int(e[4])
            anyr = False
            for s in range(3):
                if dom[s] >= 0 and is_reader_class(cat, s, int(loc_U[s][dom[s]])):
                    anyr = True
            out['reader' if anyr else 'resident'] += 1
    return out


def summarize(prep, res, mN, H):
    """compact per-(run, mN) record."""
    cat = prep['cat']
    modal, effm, fairm, cls = res['modal'], res['effm'], res['fairm'], res['cls']
    G1, I = modal.shape
    stop = res['stop']
    ser = MW.target_series(modal, effm, fairm)
    nm, nf = ser['nm'], ser['nf']
    cat_ = ser['cat']
    inef = 1.0 - effm.mean(1)
    snaps = {}
    for g in SNAPS:
        if g > H:
            continue
        mg = modal[g]
        snaps[str(g)] = dict(nm=int(nm[g]), F=int(nf[g]), U=int((cat_[g] == 1).sum()), Gr=int((cat_[g] == 2).sum()),
                             Wa=int((cat_[g] == 3).sum()), Dd=int((cat_[g] == 4).sum()), cons=int((mg == mg[0]).all()),
                             ts=int(ser['ts'][g]), tv=int(ser['tv'][g]), inef=round(float(inef[g]), 5),
                             pres=[int((mg == v).any()) for v in V],
                             lab={MW.OLAB[int(k)]: int(c) for k, c in zip(*np.unique(mg, return_counts=True))})
    fl = flips(modal)
    fc = flip_counts(fl, modal, stop)
    routes = flip_routes(fl, res['ev'], res['nev'], 200000, prep['U'], cat, stop)
    lo = min(5000, H)
    cov_avg = float((nm[lo:] == 3).mean())
    # first generation at which all three fair pairs are present / the last at which they are
    cov = nm == 3
    g_first = int(np.argmax(cov)) if cov.any() else -1
    g_last = int(np.nonzero(cov)[0][-1]) if cov.any() else -1
    rec = dict(mN=mN, status=res['status'], stop=stop, nmig=res['nmig'], nev=res['nev'], snap=snaps, flips=fc, routes=routes,
               cov_avg=round(cov_avg, 4), g_first=g_first, g_last=g_last, mean_inef=round(float(inef.mean()), 5),
               fair_share_end=round(float(ISFAIR[modal[H]].mean()), 4), eff_end=round(float(effm[H].mean()), 4))
    return rec


def run_cell_run(spec, r, mNs=MNS, H=10000, base=None, price=0.0, N=100, I=64, cache_dir=None):
    """one run (one set of founders) of a cell at every mN; returns a list of records."""
    t0 = time.time()
    cat = get_cat(spec, cache_dir)
    base = base or founder_base(spec)
    prep = prepare(cat, base, r, I, N, price)
    t1 = time.time() - t0
    recs = []
    for mN in mNs:
        t2 = time.time()
        res = kernel(prep, mN, H)
        rec = summarize(prep, res, mN, H)
        rec.update(run=r, spec=spec, price=price, wall=round(time.time() - t2, 1))
        recs.append(rec)
    for rec in recs:
        rec['prep_wall'] = round(t1, 1); rec['rss_gb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 2)
        rec['K'] = [len(u) for u in prep['U']]
    return recs


def founder_base(spec):
    """founder base name: B6w / B6m use the stored L1 founders (the migration-window baseline); E10m and E10w share a
    base (paired); every other arm has its own."""
    if spec in ('B6w', 'B6m'):
        return 'L1'
    if spec in ('E10m', 'E10w'):
        return 'CP-E10'
    if spec.startswith('Emin-'):
        return 'CP-Emin-' + spec.split('-')[1]            # modal and weak evaluators share founders
    if spec.startswith('T-'):
        return 'CP-' + spec
    raise ValueError(spec)
