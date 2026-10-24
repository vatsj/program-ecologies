"""Deriving immigrant rejection for stable sets on islands: Step 0 machinery (notes/immigrant-rejection.md).

Runs the migration-window object (three-player majority division in sixths, length prior, Moran w = 0.3, eps = 0,
N = 100, I = 64 islands in one connected component) through `immigrant_rejection_kernels.fkern_ir`, a generated copy of
`farsighted_refusal.fkern` with per-generation records, freeze vetoes of births at member islands and immigrant-fate
counters, and computes the flip statistics, the contract accounting and the coverage statistics of Step 0.  Also holds
the reference (pure Python) tie rules of the candidates.  Importable without side effects; the drivers are in
immigrant_rejection_run.py.  No existing file of src/ is edited.
"""
import os, sys, time, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import dollar3 as D
import farsighted_refusal as F
import farsighted_refusal_run as FR
import migration_window as MW
import immigrant_rejection_kernels as IK

T = MW.T
X = MW.X
V = MW.V                                    # outcome ids of the three fair pairs
NOUT = MW.NOUT
HELD = 25
H0 = 10000
N0 = 100
I0 = 64
BASE = 'L1'
CS, CD, CACT = F.CS_, F.CD_, F.CACT_

# excluded slot of each fair-pair outcome (the slot with zero payoff), -1 elsewhere
EXCL = np.full(NOUT, -1, np.int64)
for _z in V:
    EXCL[_z] = [s for s in range(3) if X[_z][s] == 0][0]
PARTNER = np.asarray(D.PARTNER, np.int64)
FAIR33 = np.array([bool(CD[k, 0] == 3 and CD[k, 1] == 3) for k in range(CS.shape[0])], np.bool_)


# ---------------------------------------------------------------- arms
# fr = (excluded-slot offers, included-slot partner, immigrant fiat, track fates); modes 1 all births, 2 local, 3 migrant
ARMS = {
    'B':    dict(nu=0.0, guards=['g0'], assign=None, fr=(0, 0, 0)),
    'FX':   dict(nu=0.0, guards=['g0'], assign=None, fr=(1, 0, 0)),
    'FP':   dict(nu=0.0, guards=['g0'], assign=None, fr=(0, 1, 0)),
    'FXP':  dict(nu=0.0, guards=['g0'], assign=None, fr=(1, 1, 0)),
    'FI':   dict(nu=0.0, guards=['g0'], assign=None, fr=(0, 0, 1)),
    'FPL':  dict(nu=0.0, guards=['g0'], assign=None, fr=(0, 2, 0)),
    'g0':   dict(nu=0.1, guards=['g0'], assign=None, fr=(0, 0, 0)),
    'gV':   dict(nu=0.1, guards=['g0', 'gV'], assign=('bit', 1.0, 1), fr=(0, 0, 0)),
    'gVs':  dict(nu=0.1, guards=['g0', 'gVs'], assign=('bit', 1.0, 1), fr=(0, 0, 0)),
    'gKRw': dict(nu=0.1, guards=['g0', 'gKRw'], assign=('bit', 1.0, 1), fr=(0, 0, 0)),
    'gKR':  dict(nu=0.1, guards=['g0', 'gKR0.99'], assign=('bit', 1.0, 1), fr=(0, 0, 0)),
}
MNS = (0.01, 0.1, 1)


def table_gVs():
    """strict veto: every contract is refused at a fair pair (gV without the (3, 3) exemption)."""
    T_ = F.table_gV().copy()
    for y in V:
        T_[y, :, :] = False
    return T_


def table_gKRw():
    """the default gKR(0.99) value function W with consent if not worse (indifference accepts)."""
    Tk, d, W, acc = FR.kr_table('0.99')
    Tw = np.zeros_like(Tk)
    for y in range(F.NX):
        for k in range(F.NCON):
            x = F.CX[k]
            for z in range(2):
                i = int(CS[k, z])
                Tw[y, k, z] = W[x, i] >= W[y, i] - 1e-9
    return Tw


def guard_arrays_ir(names):
    """FR.guard_arrays extended by the two new static guards 'gVs' and 'gKRw'."""
    known = [n for n in names if n not in ('gVs', 'gKRw')]
    ga = FR.guard_arrays([n if n not in ('gVs', 'gKRw') else 'g0' for n in names])
    for g, n in enumerate(names):
        if n == 'gVs':
            ga['GTAB'][g] = table_gVs()
        elif n == 'gKRw':
            ga['GTAB'][g] = table_gKRw()
    return ga


# ---------------------------------------------------------------- flips
def flips(modal, L=HELD):
    """debounced changes of each island's modal outcome: list over islands of (g, from, to), g the first generation of
    the new value (accepted if it persists for L generations or to the end of the horizon)."""
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


def flip_summary(fl, installs, H):
    """counts of debounced changes by class (m->m, m->o, o->m, o->o), the contract-mediated subset, and m->m by window.
    installs: array of (generation, island) of installed contracts."""
    inst = {}
    for g, i in installs:
        inst.setdefault(int(i), []).append(int(g))
    ismem = np.zeros(NOUT, bool); ismem[V] = True
    out = dict(mm=0, mo=0, om=0, oo=0, mm_med=0, mo_med=0, om_med=0, oo_med=0)
    win = np.zeros(10, np.int64)
    pairs = {}
    for i, ch in enumerate(fl):
        gs = inst.get(i, [])
        for g, a, b in ch:
            k = ('m' if ismem[a] else 'o') + ('m' if ismem[b] else 'o')
            out[k] += 1
            med = any(g - 3 <= gc <= g for gc in gs)
            if med:
                out[k + '_med'] += 1
            if k == 'mm':
                win[min(9, g * 10 // H)] += 1
                pairs['%s>%s' % (MW.OLAB[a], MW.OLAB[b])] = pairs.get('%s>%s' % (MW.OLAB[a], MW.OLAB[b]), 0) + 1
    out['mm_win'] = win.tolist()
    out['mm_pairs'] = pairs
    return out


def install_summary(cev):
    """installs and refusals on member / other islands, split by (3, 3) fair-to-fair contracts.  cev rows: generation,
    island, contract, status (1 refused, 2 installed), modal class index at the event is column 5."""
    ismem = np.zeros(NOUT, bool); ismem[V] = True
    out = dict(inst_mem_fair33=0, inst_mem_other=0, inst_oth_fair33=0, inst_oth_other=0,
               ref_mem_fair33=0, ref_mem_other=0, ref_oth_fair33=0, ref_oth_other=0)
    if len(cev) == 0:
        return out, np.zeros((0, 2), np.int64)
    st = cev[:, 3].astype(int)
    mem = ismem[cev[:, 5].astype(int)]
    f33 = FAIR33[cev[:, 2].astype(int)]
    for code, pre in ((2, 'inst'), (1, 'ref')):
        sel = st == code
        for m_, mn in ((True, 'mem'), (False, 'oth')):
            for f_, fn in ((True, 'fair33'), (False, 'other')):
                out['%s_%s_%s' % (pre, mn, fn)] = int((sel & (mem == m_) & (f33 == f_)).sum())
    inst = cev[st == 2][:, [0, 1]].astype(np.int64)
    return out, inst


# ---------------------------------------------------------------- one run
def run_arm(arm, mN, r, H=H0, N=N0, I=I0, base=BASE, cevcap=400000):
    """one run of an arm at migration mN; returns the compact record (no arrays)."""
    t0 = time.time()
    p = ARMS[arm]
    names = p['guards']
    init, _ = MW.founders(base, r, I, N)
    loc, U = SS.compress(init)
    st = F.Setup(loc, U, len(names), assign=p['assign'], rng=None)
    ga = guard_arrays_ir(names)
    seed = MW.comp_seed(base, r, 0, I, True)
    fr = np.array(list(p['fr']) + [1], np.int64)
    nu = float(p['nu'])
    res, modal, effm, fairm, fate, tdesc = IK.fkern_ir(
        st.J, T.PAY, T.VEC, T.ISMEM, T.TOT, st.tc0, st.TK, st.TO, st.TG, st.TPC, st.TMAP, st.ntypes, st.Kmax, st.NG, N,
        SS.W, mN / N, seed, H, 10, np.zeros(0, np.int64), nu, CS, CD, CACT, F.CX, ga['GKIND'], ga['GTAB'], ga['KRTAB'],
        F.PROPM, F.UPAY, float(ga['rdelta']), nu == 0.0, 50, 1000, cevcap, fr, EXCL, PARTNER)
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, gfreq, refby, nsolve, pcount = res
    wall_k = time.time() - t0
    arr = dict(cls=cls, modal=modal, effm=effm, fairm=fairm)
    meta = dict(status=[int(status)], stop=[int(stop)], nmig=int(nmig), nev=int(nev))
    rec, _ = MW.analyse(arr, [(0, I)], meta, H)
    isum, inst = install_summary(cev)
    fl = flips(modal)
    fs = flip_summary(fl, inst, H)
    alive = np.zeros((2, 2, 2), np.int64)
    for i in range(I):
        for s in range(3):
            for pc in np.nonzero(tdesc[i, s] > 0)[0]:
                d_ = int(tdesc[i, s, pc]) - 1
                alive[d_ // 4, (d_ // 2) % 2, d_ % 2] += 1
    out = dict(arm=arm, mN=mN, run=r, status=int(status), stop=int(stop), nmig=int(nmig), ncev=int(ncev),
               ncev_overflow=bool(ncev > cevcap), snap=rec['snap'], tc=rec['t_clear'], ge=rec['g_est'],
               tl=rec['t_lost'], lw=rec['last_waste'], ep_ts=rec['ep_ts'], ep_tv=rec['ep_tv'],
               flips=fs, inst=isum, fate=fate.tolist(), alive=alive.tolist(),
               cnt=[int(v) for v in cnt.sum(0)], wall=round(time.time() - t0, 1), wall_kernel=round(wall_k, 1),
               rss_gb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 2))
    return out


# ---------------------------------------------------------------- candidates: reference tie rules (pure Python)
# A tie for slot s: both other slots' base actions name s as partner and each demand completes a pair at s's base
# demand.  Actions are (partner slot, demand in sixths); ALL = 3.
ALL = 3


def is_tie(s, base_action, act_b, act_c):
    """slots b < c are the two others of s; act_* are (partner, demand) base actions."""
    others = [t for t in range(3) if t != s]
    ab, ac = (act_b, act_c)
    ds = base_action[1]
    return (ab[0] == s and ac[0] == s and ab[1] + ds <= 6 and ac[1] + ds <= 6), others


def loyal_choice(s, base_action, act_b, act_c, memory, k):
    """LOYAL-k: memory is the list of the last up to k partners (slot or None); returns the program's action."""
    tie, others = is_tie(s, base_action, act_b, act_c)
    if not tie:
        return base_action
    mem = memory[-k:]
    if k == 1:
        h = mem[-1] if mem else None
    else:
        cnt = {}
        for q in mem:
            if q is not None:
                cnt[q] = cnt.get(q, 0) + 1
        h = None
        for q, c in cnt.items():
            if 2 * c > len(mem):                 # strict majority of the remembered encounters
                h = q
    if h in others:
        return (h, base_action[1])
    return base_action


def sq_choice(s, base_action, act_b, act_c, island_pair):
    """SQ-direct: at a tie keep the partner of the island's current pair (None if s is not in it)."""
    tie, others = is_tie(s, base_action, act_b, act_c)
    if not tie or island_pair is None or s not in island_pair:
        return base_action
    j = [t for t in island_pair if t != s][0]
    return (j, base_action[1])


def valued_tie_choice(Q):
    """SQ-valued: Q maps candidate partner -> value W_i(x_j) - eps [coal(x_j) != incumbent]; the argmax if strict,
    None (fall back to drift) on an exact tie."""
    items = sorted(Q.items())
    best = max(v for _, v in items)
    arg = [j for j, v in items if abs(v - best) < 1e-12]
    return arg[0] if len(arg) == 1 else None


def sq_valued_choice(s, base_action, act_b, act_c, W_by_partner, incumbent_partner, eps):
    tie, others = is_tie(s, base_action, act_b, act_c)
    if not tie:
        return base_action
    Q = {j: W_by_partner[j] - (eps if j != incumbent_partner else 0.0) for j in others}
    j = valued_tie_choice(Q)
    return (j, base_action[1]) if j is not None else base_action


def conf_update(s, previous, sample_pair):
    """CONF: observe one completed encounter; if it formed a fair pair containing s, play the part (name the partner at
    3 sixths); otherwise keep the previous choice.  sample_pair: tuple of the two slots of the observed fair pair or None."""
    if sample_pair is not None and s in sample_pair:
        j = [t for t in sample_pair if t != s][0]
        return (j, 3)
    return previous
