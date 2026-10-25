"""The mechanism probe and the homogeneous-reader cell of the churn-in-the-primary-object experiment (spec
specs/2026-10-25-churn-primary.md; notes/churn-primary.md section 1.5; predictions' scoring rules).

An island sits on the fair pair {0, 1} (slot 2 excluded): slot 0 holds the pair's reader (or a constant), slot 1 a
constant that offers slot 0 a half, slot 2 either a constant that offers slot 0 a half (stratum a, "forced to a fair
offer toward a member") or a natural composition drawn from the catalogue's seed law (stratum b).  Single immigrants
(one of N) or a fraction of immigrants are injected into one slot, the island is run alone (I = 1, no migration, eps =
0, the stored kernel) for 30 N generations or until it closes, and the island's final modal outcome decides whether
it switched to another fair pair.

All plays come from the catalogues' own joint tables (DSL evaluators, or the executed arm-T programs).
"""
import os, sys, math, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dollar3 as D
import stable_sets as SS
import migration_window_kernels as MK
import churn_primary as CP

T = CP.T
V = CP.V
W = CP.W
ISFAIR = CP.ISFAIR
F01, F02, F12 = None, None, None
# fair-pair outcome ids by pair: V is the sorted list of the three fair outcome ids; find which is {0,1}, {0,2}, {1,2}
for _o in V:
    _x = T.R[_o]
    if _x[0] > 0 and _x[1] > 0:
        F01 = _o
    elif _x[0] > 0 and _x[2] > 0:
        F02 = _o
    else:
        F12 = _o


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ====================================================================== roles: the named residents of each grammar
def const_index(cat):
    if cat.kind == 'dsl':
        return {f[1][0]: x for x, f in enumerate(cat.S.fs) if not f[0]}
    return None


class Roles:
    """The named programs of a catalogue used by the probe: per slot the constant that names slot t at 1/2, the readers
    and their fallback-disabled twins, and the library of immigrant classes."""

    def __init__(self, cat):
        self.cat = cat
        lo = D.local_of
        if cat.kind == 'dsl':
            ci = const_index(cat)
            self.Cn = lambda s, t: ci[lo(s, t, 1)]                  # slot s names slot t at 1/2
            self.const = lambda s, a: ci[a]                           # constant with local action a
            self.switch = cat.idx[(0, 'Sj')]                          # accept slot 1's half offer, else name slot 2
            self.taker = cat.idx[(0, 'Sk')]                           # accept slot 2's half offer, else name slot 1
            self.two = cat.idx[(0, 'R2jf')]                           # slot 1 first, then slot 2, fallback stay with slot 1
            self.stub = {'switch': ci[lo(0, 1, 1)], 'two': ci[lo(0, 1, 1)], 'taker': ci[lo(0, 1, 1)]}
            self.lib = {s: self._dsl_lib(s, ci) for s in range(3)}
            self.hom = {'modal': (cat.idx[(0, 'R2jf')], cat.idx[(1, 'R2jf')], cat.idx[(2, 'R2jf')]),
                        'weak': (cat.idx[(0, 'Sj')], ci[lo(1, 0, 1)], cat.idx[(2, 'R2jf')])}
        else:
            ix = cat.idx
            # cyclic frame: slot 0's next is slot 1; code 1 = next at 1/2, 4 = prev at 1/2
            self.Cn = lambda s, t: ix['C1'] if (t - s) % 3 == 1 else ix['C4']
            self.const = lambda s, a: ix['C%d' % a]
            self.switch = ix['Snoy']; self.taker = None; self.two = ix['Dnfy']
            self.stub = {'switch': ix['Snqy'], 'two': ix['Snqy'], 'taker': None}
            lib = [x for x in range(cat.K) if cat.fam[x] in ('const', 'single', 'two', 'exploit')]
            self.lib = {s: lib for s in range(3)}
            self.hom = {'T': (ix['Dnfy'], ix['Dpfy'], ix['Dpfy'])}

    def _dsl_lib(self, s, ci):
        cat = self.cat
        out = [ci[a] for a in range(9)]
        for key in ('Sj', 'Sk', 'Zj', 'Zk', 'R2jf', 'R2jz', 'R2kf', 'R2kz'):
            out.append(cat.idx[(s, key)])
        return out

    def residents(self, kind, stratum):
        """(class of slot 0, slot 1, slot 2) for the monomorphic parts; slot 2 is None for the natural stratum (b)."""
        c = self.Cn
        i = {'const': c(0, 1), 'switch': self.switch, 'two': self.two, 'taker': self.taker}[kind]
        j = c(1, 0)
        if kind == 'taker':
            k = c(2, 1)                                   # excluded slot offers slot 1 (not the reader): no offer to slot 0
        elif stratum == 'a':
            k = c(2, 0)                                   # forced fair offer toward member slot 0
        else:
            k = None
        return i, j, k


# ====================================================================== the local island
def make_prep(cat, classes, price=0.0):
    """classes: list over slots of iterables of global class ids that can occur.  Returns the local universe, joint
    table and index maps."""
    U = [np.array(sorted(set(int(x) for x in cl)), np.int64) for cl in classes]
    J, PAY, VEC = cat.make_J(U, price)
    g2l = [{int(g): t for t, g in enumerate(u)} for u in U]
    return dict(cat=cat, U=U, J=J, PAY=PAY, VEC=VEC, g2l=g2l, Kmax=J.shape[0])


def init_local(prep, counts):
    """counts: list over slots of dict global class -> count; returns (1, 3, Kmax) int64."""
    init = np.zeros((1, 3, prep['Kmax']), np.int64)
    for s in range(3):
        for g, n in counts[s].items():
            init[0, s, prep['g2l'][s][int(g)]] += n
    return init


def run_island(prep, init, N, seed, H):
    out = MK.kern_mw(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, init, N, W, 0.0, seed, H, 10,
                     np.zeros(0, np.int64), 4000)
    status, stop, counts, cls, eff, dist, ev, nev, nmig, modal, effm, fairm = out
    return dict(status=int(status), stop=int(stop), counts=counts, ev=ev, nev=int(nev), modal=modal[:, 0],
                effm=effm[:, 0], fairm=fairm[:, 0])


def final_outcome(modal, stop, H, L=25):
    """the island's debounced final modal outcome: the value held through the last L generations (before stop), else
    -1 (unsettled)."""
    g1 = min(stop, H)
    seg = modal[max(0, g1 - L + 1):g1 + 1]
    return int(seg[0]) if (seg == seg[0]).all() else -1


def encounter_stats(prep, counts, N):
    """outcome distribution, mean payoffs per slot and the redirect share of slot 0 against its resident-only action,
    at a state `counts` (1, 3, Kmax)."""
    J = prep['J']; PAY = prep['PAY']; VEC = prep['VEC']
    c0 = counts[0, 0] / N; c1 = counts[0, 1] / N; c2 = counts[0, 2] / N
    a = np.nonzero(c0)[0]; b = np.nonzero(c1)[0]; c = np.nonzero(c2)[0]
    dist = np.zeros(len(T.R)); pay = np.zeros(3)
    codes = J[np.ix_(a, b, c)]
    P = c0[a][:, None, None] * c1[b][None, :, None] * c2[c][None, None, :]
    np.add.at(dist, VEC[codes.ravel()], P.ravel())
    for s in range(3):
        pay[s] = (PAY[codes, s] * P).sum()
    # redirect: slot 0's action against the modal resident configuration
    am = a[np.argmax(c0[a])]; bm = b[np.argmax(c1[b])]; cm = c[np.argmax(c2[c])]
    base_act = J[am, bm, cm] // 81
    act = codes // 81
    redirect = float((P * (act != base_act)).sum())
    return dist, pay, redirect


# ====================================================================== one probe configuration
def natural_k(cat, rng, N, i_c, j_c, nat_n=20, accept_mass=0.9, max_tries=2000):
    """compositions for slot 2 drawn from the catalogue's seed law and kept if, against the monomorphic residents of
    slots 0 and 1, the pair {0, 1} holds at least `accept_mass` of encounters (rejection sampling).  Returns the
    accepted compositions and the acceptance rate."""
    law = CP.cat_law(cat, 2)
    nat = []; tries = 0
    while len(nat) < nat_n and tries < max_tries:
        tries += 1
        comp = rng.multinomial(N, law)
        gs = np.nonzero(comp)[0]
        pr = make_prep(cat, [[i_c], [j_c], list(gs)])
        c2 = {int(g): int(comp[g]) for g in gs}
        dist, pay, red = encounter_stats(pr, init_local(pr, [{i_c: N}, {j_c: N}, c2]), N)
        if dist[F01] >= accept_mass:
            nat.append(c2)
    return nat, len(nat) / max(tries, 1)


def probe_core(cat, i_c, j_c, nat, libs, slots=(0, 1, 2), N=100, reps=100, mode='single', frac=None, control=None,
               H=None, seed_base='probe', price=0.0, nexamples=3):
    """Inject immigrants into an island with slot 0 = i_c, slot 1 = j_c, slot 2 = one of the compositions in `nat`.
    mode 'single' (one individual) or 'frac' (a fraction `frac` of the slot).  control None, 'sham' (a resident copy
    replaces a resident: nothing changes), or 'namepres' (only immigrants whose play against the residents equals the
    replaced resident's).  Returns rows[(slot, class)]."""
    H = H or 30 * N
    rng = np.random.default_rng(zlib.crc32(('%s|%d|%s|%s|%s|%s' % (seed_base, N, mode, frac, control, (i_c, j_c))).encode()))
    allk = set()
    for d in nat:
        allk |= set(d)
    cls_sets = [set([i_c]) | set(libs[0]), set([j_c]) | set(libs[1]), allk | set(libs[2])]
    prep = make_prep(cat, cls_sets, price)
    base_counts = [{i_c: N}, {j_c: N}, dict(nat[0])]
    base_init = init_local(prep, base_counts)
    base_code = None
    if control == 'namepres':
        # the resident play: modal composition codes
        pass
    rows = {}
    examples = []
    resident_ok = None
    for s in slots:
        cand = list(libs[s])
        if control == 'sham':
            cand = [(i_c, j_c, list(nat[0])[0])[s]]
        for q in cand:
            if control == 'namepres':
                res_cls = (i_c, j_c, max(nat[0], key=nat[0].get))
                if int(q) == res_cls[s]:
                    continue
                trial = list(res_cls); trial[s] = int(q)
                lt = [prep['g2l'][t][int(trial[t])] for t in range(3)]
                lr = [prep['g2l'][t][int(res_cls[t])] for t in range(3)]
                if prep['J'][lt[0], lt[1], lt[2]] != prep['J'][lr[0], lr[1], lr[2]]:
                    continue
            row = dict(n=0, sw=0, left=0, takeover=0, drift=0, redirect=0, unres=0, tsw=[], redir0=None, pay0=None)
            for rep in range(reps):
                counts = [dict(base_counts[0]), dict(base_counts[1]), dict(nat[rep % len(nat)])]
                ds = counts[s]
                if control == 'sham':
                    pass
                elif mode == 'single':
                    cl = list(ds); w = np.array([ds[x] for x in cl], float)
                    r_ = cl[int(rng.choice(len(cl), p=w / w.sum()))]
                    ds[r_] -= 1
                    if ds[r_] == 0:
                        del ds[r_]
                    ds[int(q)] = ds.get(int(q), 0) + 1
                else:
                    nin = int(round(frac * N))
                    cl = list(ds)
                    for _ in range(nin):
                        w = np.array([ds[x] for x in cl], float)
                        r_ = cl[int(rng.choice(len(cl), p=w / w.sum()))]
                        ds[r_] -= 1
                    ds[int(q)] = ds.get(int(q), 0) + nin
                    for x in [x for x in ds if ds[x] == 0]:
                        del ds[x]
                init = init_local(prep, counts)
                if rep == 0:
                    dist0, pay0, red0 = encounter_stats(prep, init, N)
                    row['redir0'] = red0; row['pay0'] = pay0.tolist()
                seed = int(rng.integers(0, 2 ** 31 - 1))
                res = run_island(prep, init, N, seed, H)
                m0 = int(res['modal'][0])
                if resident_ok is None:
                    resident_ok = (m0 == F01)
                fo = final_outcome(res['modal'], res['stop'], H)
                row['n'] += 1
                if res['status'] == 4:
                    row['unres'] += 1
                if fo >= 0 and ISFAIR[fo] and fo != F01:
                    row['sw'] += 1
                    mm = res['modal']
                    g = int(np.nonzero(mm != fo)[0][-1] + 1) if (mm != fo).any() else 0
                    row['tsw'].append(g)
                    if len(examples) < 4 * nexamples and row['sw'] <= 1:
                        examples.append(dict(key=(s, int(q)), counts=counts, seed=seed, g=g))
                if fo != F01:
                    row['left'] += 1
                changes = [e for e in res['ev'] if e[0] > 0]
                if changes:
                    qloc = prep['g2l'][s][int(q)]
                    if any(int(e[2]) == s and int(e[4]) == qloc for e in changes):
                        row['takeover'] += 1
                    else:
                        row['drift'] += 1
                elif fo != F01:
                    row['redirect'] += 1
            rows[(s, int(q))] = row
    traces = []
    for ex in examples[:12]:
        init = init_local(prep, ex['counts'])
        g = ex['g']
        rec = dict(key=ex['key'], g=g)
        for lab, h in (('before', max(g - 1, 1)), ('after', min(g + 30, H))):
            r2 = run_island(prep, init, N, ex['seed'], h)
            dist, pay, red = encounter_stats(prep, r2['counts'], N)
            c0 = r2['counts'][0, 0]
            rec[lab] = dict(h=h, outcome={T.labels[o]: round(float(dist[o]), 3) for o in np.nonzero(dist > 0.01)[0]},
                            pay=[round(float(x), 3) for x in pay], redirect=round(red, 3),
                            slot0={cat.label(prep['U'][0][t]) if hasattr(cat, 'label') else int(prep['U'][0][t]): int(c0[t])
                                   for t in np.nonzero(c0)[0]})
        traces.append(rec)
    return dict(rows=rows, resident_ok=resident_ok, N=N, H=H, mode=mode, frac=frac, control=control,
                resid=(i_c, j_c), traces=traces)


def probe_config(cat, kind, stratum, N=100, reps=100, slots=(0, 1, 2), mode='single', frac=None, control=None,
                 seed_base='probe', nat_n=20, price=0.0, H=None):
    """Run one configuration of the probe.  kind in {'const', 'switch', 'two', 'taker'}; stratum 'a' (excluded slot
    forced to a fair offer toward slot 0) or 'b' (natural composition); control None, 'sham', 'namepres', 'twin'
    (fallback-disabled twin residents).  Returns None where a control does not exist."""
    roles = Roles(cat)
    i_c, j_c, k_c = roles.residents(kind, stratum)
    if control == 'twin':
        i_c = roles.stub[kind]
        if i_c is None:
            return None
    rng = np.random.default_rng(zlib.crc32((seed_base + '|nat|%s|%s|%d' % (kind, stratum, N)).encode()))
    if k_c is None:
        nat, acc = natural_k(cat, rng, N, i_c, j_c, nat_n)
    else:
        nat, acc = [{k_c: N}], 1.0
    out = probe_core(cat, i_c, j_c, nat, roles.lib, slots, N, reps, mode, frac, control, H,
                     '%s|%s|%s' % (seed_base, kind, stratum), price)
    out.update(kind=kind, stratum=stratum, accept=acc)
    return out


def hom_cell(cat, key, N=100, fracs=(0.01, 0.05), reps=100, seed_base='hom', price=0.0):
    """The homogeneous-reader cell (notes 1.5): residents roles.hom[key], immigrants into slot 1."""
    roles = Roles(cat)
    r0, r1, r2 = roles.hom[key]
    outs = {}
    for f in fracs:
        outs[f] = probe_core(cat, r0, r1, [{r2: N}], roles.lib, slots=(1,), N=N, reps=reps, mode='frac', frac=f,
                             seed_base=seed_base, price=price)
    return outs


def pool(cfg, slots=None, classes=None):
    """pooled switching rate over (slot, class) rows (equal replicates per class)."""
    rows = cfg['rows']
    ks = [k for k in rows if (slots is None or k[0] in slots) and (classes is None or k[1] in classes)]
    n = sum(rows[k]['n'] for k in ks); sw = sum(rows[k]['sw'] for k in ks)
    left = sum(rows[k]['left'] for k in ks)
    return dict(n=n, sw=sw, left=left, rate=sw / n if n else float('nan'), ci=wilson(sw, n))


# ====================================================================== balanced start with resident readers (extension)
def pair_residents(cat, kind, a, b):
    """(class of slot a, class of slot b) for a pair {a < b} on kind in {'const', 'switch', 'two'}: the lower slot a holds
    the reader (or a constant) that reads/names b, the higher slot b the constant that names a at 1/2; the readers' fallback
    names the third slot (switch) or stays with b (two)."""
    if cat.kind == 'dsl':
        ci = const_index(cat)
        lo = D.local_of
        lower = D.others(a)[0] == b
        if kind == 'const':
            ca = ci[lo(a, b, 1)]
        elif kind == 'switch':
            ca = cat.idx[(a, 'Sj' if lower else 'Sk')]
        else:
            ca = cat.idx[(a, 'R2jf' if lower else 'R2kf')]
        return ca, ci[lo(b, a, 1)]
    ix = cat.idx
    nxt = (b - a) % 3 == 1
    if kind == 'const':
        ca = ix['C1'] if nxt else ix['C4']
    elif kind == 'switch':
        ca = ix['Snoy'] if nxt else ix['Spoy']
    else:
        ca = ix['Dnfy'] if nxt else ix['Dpfy']
    cb = ix['C1'] if (a - b) % 3 == 1 else ix['C4']
    return ca, cb


def prepare_balanced(cat, kind, base, r, I=60, N=100, price=0.0):
    """I islands, a third on each fair pair (pair slots monomorphic: the reader or constant of `kind` and its mate), the
    excluded slot drawn from the catalogue's seed law (the stored 'bal' start of the migration window, with readers)."""
    rng = np.random.default_rng(CP.run_seed(base, r))
    laws = [CP.cat_law(cat, s) for s in range(3)]
    K = len(laws[0])
    init = np.zeros((I, 3, K), np.int64)
    pairs = ((0, 1), (0, 2), (1, 2))
    for i in range(I):
        a, b = pairs[i % 3]
        c = 3 - a - b
        ca, cb = pair_residents(cat, kind, a, b)
        init[i, a, ca] = N; init[i, b, cb] = N
        init[i, c] = rng.multinomial(N, laws[c])
    loc, U = SS.compress(init)
    J, PAY, VEC = cat.make_J(U, price)
    return dict(cat=cat, loc=loc, U=U, J=J, PAY=PAY, VEC=VEC, seed=CP.run_seed(base, r) % (2 ** 31), N=N, I=I)


def run_balanced(spec, kind, r, mNs=(0.1, 1), H=10000, cache_dir=None):
    cat = CP.get_cat(spec, cache_dir)
    base = 'CP-bal-%s-%s' % (spec, kind)
    prep = prepare_balanced(cat, kind, base, r)
    recs = []
    for mN in mNs:
        res = CP.kernel(prep, mN, H)
        rec = CP.summarize(prep, res, mN, H)
        rec.update(run=r, spec=spec, kind=kind)
        recs.append(rec)
    return recs
