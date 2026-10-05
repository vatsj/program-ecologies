"""Incentive-compatible enforcement in the union game (specs/2026-10-05-enforcement.md).

Extends src/union.py.  The game, grammar, atoms and prior are the union run's;
only the evaluator changes.

Extensive form of one encounter.  Stage 1: the boss's wage s is committed (its
program output).  Stage 2: the workers' strike/work and the boss's whack policy
are each either committed (program output) or ex-post rational, per arm:

    CC  both committed (the union run's game)
    RC  boss's whack ex-post rational, workers committed
    CR  boss's whack committed, workers ex-post rational
    RR  both ex-post rational

crossed with the replacement pool (a whacked striker is replaced by an outside
scab whose product 1 - s the boss recovers; the boss pays the scab s).

Override, applied inside the per-world evaluation.  At world n each slot's
recommendation is computed from its box atoms; then
  * a rational boss keeps its wage and whacks each striker iff whacking raises its
    payoff in this encounter: with the pool the gain is (1 - s) - c, without it
    -c.  A working worker is never whacked by a rational boss (gain -c, or
    (1 - s) - c - (1 - s) = -c if replaced).  The implemented whack policy is then
    'strike' (whack strikers) or 'none'.  At the exact boundary 1 - s = c the
    rational boss whacks (tie = 'whack', the spec's declaration) or not
    (tie = 'nowhack', the alternative report);
  * a rational worker best-responds to the implemented boss action (s, h'), with
    the complete payoff table: work gives s - L [whacked if working], strike gives
    -L [whacked if striking]; whacked if working iff h' = source and the worker is
    tagged; whacked if striking iff h' = strike, or h' = source and tagged.  A
    worker's payoff does not depend on the other worker, so there is no
    circularity.  Indifference resolves to the program's recommendation.
Boxes refer to implemented actions: the flags are updated with the implemented
joint code, so values stay per-world, boxes stay "true at every earlier world",
monotonicity and stabilization are unchanged (the implemented play at a world is
a deterministic function of the flags), and Lemma 0 (soundness at the stable
world) goes through.  The box audit (audit_* below) re-derives every encounter
from the play history with an independent evaluator and checks it.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from abm import njit
import union as U

ARMS = {'CC': (0, 0), 'RC': (1, 0), 'CR': (0, 1), 'RR': (1, 1)}   # (boss rational, workers rational)
TIES = {'whack': 0, 'nowhack': 1}
WAGES = U.WAGES
LW = 1.0


# ---------------------------------------------------------------- override
@njit(cache=True)
def override(bi, a1, a2, t1, t2, rb, rw, pool, c, tie):
    """Implemented (boss action, a1, a2) from the recommendations."""
    si = bi // 3; h = bi % 3
    s = 0.25 * si
    if rb:
        g = (1.0 - s - c) if pool else -c
        if g > 1e-12:
            h = 0
        elif g < -1e-12:
            h = 1
        else:
            h = 0 if tie == 0 else 1
    if rw:
        out = [a1, a2]
        tg = (t1, t2)
        for i in range(2):
            wW = 1.0 if (h == 2 and tg[i] == 1) else 0.0
            wS = 1.0 if (h == 0 or (h == 2 and tg[i] == 1)) else 0.0
            uW = s - LW * wW
            uS = -LW * wS
            if uW > uS + 1e-12:
                out[i] = 0
            elif uS > uW + 1e-12:
                out[i] = 1
        a1 = out[0]; a2 = out[1]
    return 3 * si + h, a1, a2


@njit(cache=True)
def encounter_e(nat, atP, atL, tab, TT, xb, x1, x2, flag, tagw, rb, rw, pool, c, tie):
    """As union.encounter, with the per-world override; boxes read implemented play."""
    xs = (xb, x1, x2)
    for t in range(flag.shape[1]):
        flag[0, t] = True; flag[1, t] = True
    val = np.zeros(3, np.int64)
    t1 = tagw[x1]; t2 = tagw[x2]
    for n in range(64):
        for s in range(3):
            x = xs[s]; idx = 0
            for t in range(nat[s, x]):
                if flag[atL[s, x, t], atP[s, x, t]]:
                    idx |= 1 << t
            val[s] = tab[s, x, idx]
        b2, i1, i2 = override(val[0], val[1], val[2], t1, t2, rb, rw, pool, c, tie)
        j = 4 * b2 + 2 * i1 + i2
        changed = False
        for s in range(3):
            x = xs[s]
            for t in range(nat[s, x]):
                L = atL[s, x, t]; p = atP[s, x, t]
                if n >= L and flag[L, p] and not TT[p, j]:
                    flag[L, p] = False; changed = True
        if not changed and n >= 2:
            return j
    return -1


@njit(cache=True)
def tensor_e(nat, atP, atL, tab, TT, KB, KW, tagw, rb, rw, pool, c, tie):
    J = np.empty((KB, KW, KW), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    for b in range(KB):
        for x in range(KW):
            for y in range(KW):
                J[b, x, y] = encounter_e(nat, atP, atL, tab, TT, b, x, y, flag, tagw, rb, rw, pool, c, tie)
    return J


@njit(cache=True)
def tensor_sub(nat, atP, atL, tab, TT, Bs, Ws, tagw, rb, rw, pool, c, tie):
    """J over index lists Bs x Ws x Ws."""
    J = np.empty((Bs.shape[0], Ws.shape[0], Ws.shape[0]), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    for i in range(Bs.shape[0]):
        for k in range(Ws.shape[0]):
            for l in range(Ws.shape[0]):
                J[i, k, l] = encounter_e(nat, atP, atL, tab, TT, Bs[i], Ws[k], Ws[l], flag, tagw, rb, rw, pool, c, tie)
    return J


# ---------------------------------------------------------------- payoffs
def payoff_table_e(c, pool, Lw=LW):
    """PAY[j, t1, t2] = (u_B, u_1, u_2) for implemented joint code j and tags;
    REP[j, t1, t2] = number of replaced strikers (each brings an outside scab paid s,
    whose product 1 - s goes to the boss).  Without the pool this is U.payoff_table."""
    PAY = np.zeros((36, 2, 2, 3)); REP = np.zeros((36, 2, 2))
    for j in range(36):
        b, a1, a2 = j // 4, (j // 2) % 2, j % 2
        s = WAGES[b // 3]; h = b % 3
        for t1 in range(2):
            for t2 in range(2):
                uB = 0.0; u = [0.0, 0.0]; rep = 0
                for w, (a, tg) in enumerate(((a1, t1), (a2, t2))):
                    whacked = (h == 0 and a == 1) or (h == 2 and tg == 1)
                    if a == 0:
                        u[w] += s; uB += 1 - s
                    if whacked:
                        u[w] -= Lw; uB -= c
                        if pool and a == 1:
                            uB += 1 - s; rep += 1
                PAY[j, t1, t2] = (uB, u[0], u[1]); REP[j, t1, t2] = rep
    return PAY, REP


def surplus(j, t1, t2, PAY, REP):
    """Realized total surplus: the three slots plus the outside scabs' wages
    (production minus whack costs and losses)."""
    s = WAGES[(j // 4) // 3]
    return PAY[j, t1, t2].sum() + s * REP[j, t1, t2]


# ---------------------------------------------------------------- independent evaluator (box audit)
def _override_py(bi, a1, a2, t1, t2, rb, rw, pool, c, tie):
    si, h = divmod(bi, 3); s = 0.25 * si
    if rb:
        g = (1 - s - c) if pool else -c
        h = 0 if g > 1e-12 else (1 if g < -1e-12 else (0 if tie == 0 else 1))
    a = [a1, a2]
    if rw:
        for i, tg in enumerate((t1, t2)):
            uW = s - LW * (h == 2 and tg == 1)
            uS = -LW * (h == 0 or (h == 2 and tg == 1))
            if uW > uS + 1e-12: a[i] = 0
            elif uS > uW + 1e-12: a[i] = 1
    return 3 * si + h, a[0], a[1]


def trace(P, xb, x1, x2, rb=0, rw=0, pool=0, c=0.5, tie=0, K=10, tagw=None):
    """History-based evaluation (no flags): world by world, every atom's truth
    recomputed from the implemented joint codes of earlier worlds.  Returns a list
    of dicts per world: rec (boss, a1, a2), imp (code), atoms per slot [(L, p, truth)]."""
    tagw = P.tag.astype(int) if tagw is None else tagw
    hist = []; out = []
    xs = (xb, x1, x2)
    for n in range(K):
        vals = []; atv = []
        for s in range(3):
            x = xs[s]; idx = 0; av = []
            for t in range(P.nat[s, x]):
                L = int(P.atL[s, x, t]); p = int(P.atP[s, x, t])
                tv = all(U.TT[p, hist[m]] for m in range(L, n))
                av.append((L, p, tv))
                if tv: idx |= 1 << t
            vals.append(int(P.tab[s, x, idx])); atv.append(av)
        b2, i1, i2 = _override_py(vals[0], vals[1], vals[2], int(tagw[x1]), int(tagw[x2]), rb, rw, pool, c, tie)
        j = 4 * b2 + 2 * i1 + i2
        hist.append(j)
        out.append(dict(n=n, rec=tuple(vals), imp=j, atoms=atv))
    return out


def audit_one(P, xb, x1, x2, j_eval, rb, rw, pool, c, tie, K=10):
    """Returns a list of violation strings (empty = pass):
    (i) the play is constant from some world n* <= K - 3 on and equals j_eval;
    (ii) box monotonicity: no atom goes false -> true;
    (iii) Lemma 0 at the stable world: every true box's proposition holds in the stable play;
    (iv) incentive check: a rational slot's implemented stage-2 move is a best response at the stable world."""
    tr = trace(P, xb, x1, x2, rb, rw, pool, c, tie, K)
    v = []
    js = [w['imp'] for w in tr]
    if js[-1] != j_eval or js[-2] != js[-1] or js[-3] != js[-1]:
        v.append('stable play mismatch %s vs %d' % (js, j_eval))
    for s in range(3):
        for t in range(len(tr[0]['atoms'][s])):
            seq = [w['atoms'][s][t][2] for w in tr]
            if any((not seq[m]) and seq[m + 1] for m in range(K - 1)):
                v.append('non-monotone atom slot %d t %d' % (s, t))
    jst = js[-1]
    for s in range(3):
        for (L, p, tv) in tr[-1]['atoms'][s]:
            if tv and not U.TT[p, jst]:
                v.append('unsound box slot %d prop %d' % (s, p))
    # incentive check at the stable world
    PAY, _ = payoff_table_e(c, pool)
    b, a1, a2 = jst // 4, (jst // 2) % 2, jst % 2
    t1, t2 = int(P.tag[x1]), int(P.tag[x2])
    if rb:
        si = b // 3
        for h in (0, 1):
            alt = 4 * (3 * si + h) + 2 * a1 + a2
            if PAY[alt, t1, t2, 0] > PAY[jst, t1, t2, 0] + 1e-12:
                v.append('boss not best-responding: h=%d better' % h)
        if b % 3 == 2:
            v.append('rational boss source-targets')
    if rw:
        for i in (1, 2):
            a = [a1, a2]; a[i - 1] = 1 - a[i - 1]
            alt = 4 * b + 2 * a[0] + a[1]
            if PAY[alt, t1, t2, i] > PAY[jst, t1, t2, i] + 1e-12:
                v.append('worker %d not best-responding' % i)
    return v


# ---------------------------------------------------------------- language helpers
def worker_fn(atoms, fn):
    """Canonical worker function from absolute atom labels (L, kind) and a python
    predicate fn(dict atom->bool) -> action (0 work, 1 strike)."""
    from dollar3 import Lang
    atoms = sorted(atoms)
    tab = []
    for idx in range(1 << len(atoms)):
        tv = {a: bool((idx >> t) & 1) for t, a in enumerate(atoms)}
        tab.append(fn(tv))
    return Lang._reduce(atoms, tab)


def boss_fn(atoms, fn):
    from dollar3 import Lang
    atoms = sorted(atoms)
    tab = [fn({a: bool((idx >> t) & 1) for t, a in enumerate(atoms)}) for idx in range(1 << len(atoms))]
    return Lang._reduce(atoms, tab)


KFAIR = 3                     # worker atom kind 's in {1/2}' (mask 4)
KLOW = 2                      # 's in {0,1/4}' (mask 3)
KOS = 13                      # OTHER = strike


def minus_programs():
    """Part A worker programs: militant-_a = if(not(BOX_a(s = 1/2)), strike, work);
    union-_{a,b} = if(and(not(BOX_a(s = 1/2)), BOX_b(OTHER = strike)), strike, work)."""
    out = {}
    for a in (0, 1):
        fa = (a, KFAIR)
        out['militant-%s' % ('' if a == 0 else '[BOX1 wage]')] = worker_fn([fa], lambda tv, fa=fa: int(not tv[fa]))
        for b in (0, 1):
            ob = (b, KOS)
            name = 'union-%d%s' % (b, '' if a == 0 else ' [BOX1 wage]')
            out[name] = worker_fn([fa, ob], lambda tv, fa=fa, ob=ob: int((not tv[fa]) and tv[ob]))
    return out


# ---------------------------------------------------------------- shared setup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'enforcement')
NAMED_W = ['scab', 'militant', 'union']
WORK = ['both work', 'one strikes', 'both strike']


def load_base():
    """The union run's language (quorum arm, boss n = 6, workers n = 10, level 0)
    and its CC class lumping (class masses are the union run's, frozen across arms)."""
    os.makedirs(OUT, exist_ok=True)
    d = U.build()
    f = os.path.join(OUT, 'classes_CC.npz')
    if os.path.exists(f):
        z = np.load(f); C = {k: z[k] for k in z.files}
        for k in ('KcW', 'KcB'): C[k] = int(C[k])
    else:
        C = U.classes(d); C.pop('J'); np.savez(f, **C)
    P = d['P']
    nmw_f = U.named(P); nmb_f = U.named_boss(P)
    return d, C, nmw_f, nmb_f


def named_lists(d, C, nmw_f, nmb_f):
    """Function indices and frozen class masses of the reduced chain's programs."""
    Bn = [U.bname(b) for b in range(U.NB)]
    Bf = np.array([nmb_f[k] for k in Bn], np.int64)
    Wf = np.array([nmw_f[k] for k in NAMED_W], np.int64)
    mB = C['massB'][C['cb'][Bf]]; mW = C['massW'][C['cw'][Wf]]
    return Bn, Bf, Wf, mB, mW


def reduced_J(d, Bf, Wf, arm, pool, c, tie):
    P = d['P']; rb, rw = ARMS[arm]
    return tensor_sub(*P.arrays(), U.TT, Bf, Wf, P.tag.astype(np.int64), rb, rw, pool, c, TIES[tie])


def _decode(j):
    b = j // 4
    return b // 3, b % 3, (j // 2) % 2, j % 2      # wage index, implemented whack, a1, a2


def threat_stats(j, t1, t2, PAY, arm, c, pool):
    """Committed threats in a state with implemented code j: per committed
    enforcement move that is executed, its payoff advantage over the feasible
    deviation (the boss: whack nobody; a worker: work), and the boss's 'if called'
    value of a committed strike-targeting threat that nobody triggers."""
    rb, rw = ARMS[arm]
    si, h, a1, a2 = _decode(j)
    out = {}
    if not rb:
        whacks = [(h == 0 and a == 1) or (h == 2 and tg == 1) for a, tg in ((a1, t1), (a2, t2))]
        if any(whacks):
            alt = 4 * (3 * si + 1) + 2 * a1 + a2
            out['boss_exec'] = PAY[j, t1, t2, 0] - PAY[alt, t1, t2, 0]
        if h == 0 and not (a1 or a2):
            out['boss_if_called'] = -c + ((1 - WAGES[si]) if pool else 0.0)
    if not rw:
        for i, a in ((1, a1), (2, a2)):
            if a == 1:
                aa = [a1, a2]; aa[i - 1] = 0
                alt = 4 * (3 * si + h) + 2 * aa[0] + aa[1]
                out['w%d_exec' % i] = PAY[j, t1, t2, i] - PAY[alt, t1, t2, i]
    return out


def chain_stats(st, lpi, A, js, t1, t2, PAY, REP, arm, c, pool, name, top_trans=6):
    """Summaries, support and transitions of a dense chain over states st."""
    pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
    n = len(st)
    pay = np.array([PAY[js[k], t1[k], t2[k]] for k in range(n)])
    sur = np.array([surplus(js[k], t1[k], t2[k], PAY, REP) for k in range(n)])
    summ = np.array([U.summary(js[k], t1[k], t2[k]) for k in range(n)])
    dec = [_decode(j) for j in js]
    striker = np.array([bool(a1 or a2) for (_, _, a1, a2) in dec])
    whacked_striker = np.array([bool((h == 0 and (a1 or a2)) or (h == 2 and ((a1 and t1[k]) or (a2 and t2[k]))))
                                for k, (_, h, a1, a2) in enumerate(dec)])
    any_whack = np.array([bool((h == 0 and (a1 or a2)) or (h == 2 and (t1[k] or t2[k]))) for k, (_, h, a1, a2) in enumerate(dec)])
    out = {}
    out['summary'] = {U.SUMM[k]: float(pi[summ == k].sum()) for k in range(7)}
    out['wage_dist'] = {U.WNAME[s]: float(sum(pi[k] for k in range(n) if dec[k][0] == s)) for s in range(3)}
    out['strike_incidence'] = float(pi[striker].sum())
    ps = pi[striker].sum()
    out['repression_given_strike'] = float(pi[whacked_striker].sum() / ps) if ps > 0 else None
    out['realized_repression'] = float(pi[any_whack].sum())
    out['mean_payoff'] = dict(zip(['boss', 'W1', 'W2'], (pi @ pay).tolist()))
    out['efficiency_slots'] = float(pi @ pay.sum(1))
    out['total_surplus'] = float(pi @ sur)
    out['implemented_whack_dist'] = {U.HNAME[h]: float(sum(pi[k] for k in range(n) if dec[k][1] == h)) for h in range(3)}
    th = {}
    for k in range(n):
        for key, v in threat_stats(js[k], t1[k], t2[k], PAY, arm, c, pool).items():
            th.setdefault(key, []).append((pi[k], v))
    out['threats'] = {key: dict(mass=float(sum(p for p, _ in L)),
                                mean_adv=float(sum(p * v for p, v in L) / max(sum(p for p, _ in L), 1e-300)),
                                mass_negative=float(sum(p for p, v in L if v < -1e-12)))
                      for key, L in th.items()}
    order = np.argsort(-pi)
    out['support'] = [dict(pi=float(pi[k]), state=name(k), play=U.joint_name(int(js[k])), summary=U.SUMM[summ[k]],
                           pay=np.round(pay[k], 3).tolist()) for k in order[:12]]
    out['support_size_99'] = int(np.searchsorted(np.cumsum(pi[order]), 0.99) + 1)
    with np.errstate(over='ignore', invalid='ignore'):
        F = np.exp(np.log(pi + 1e-300)[:, None] + A)
    F[~np.isfinite(F)] = 0
    cur = {}
    for a_ in range(7):
        for b_ in range(7):
            if a_ != b_:
                v = float(F[np.ix_(summ == a_, summ == b_)].sum())
                if v > 0: cur[U.SUMM[a_] + '>' + U.SUMM[b_]] = v
    out['currents'] = cur
    trans = []
    for k in order[:top_trans]:
        mv = []
        for k2 in range(n):
            if k2 != k and A[k, k2] > -np.inf:
                diff = [i for i in range(3) if st[k][i] != st[k2][i]]
                s_ = diff[0]
                du = pay[k2][s_] - pay[k][s_]
                mv.append(dict(p=float(np.exp(A[k, k2])), to=name(k2), to_summary=U.SUMM[summ[k2]], slot=['B', 'W1', 'W2'][s_],
                               kind='strict' if du > 1e-12 else ('deleterious' if du < -1e-12 else 'neutral')))
        mv.sort(key=lambda e: -e['p'])
        trans.append(dict(state=name(k), pi=float(pi[k]), summary=U.SUMM[summ[k]], exit_total=float(sum(e['p'] for e in mv)),
                          by_kind={kk: float(sum(e['p'] for e in mv if e['kind'] == kk)) for kk in ('strict', 'neutral', 'deleterious')},
                          top=mv[:5]))
    out['transitions'] = trans
    return out, pi


def reduced_cell(base, arm, pool, c, tie, prior, N, w=0.3):
    """One reduced canonical chain cell; exact dense log-GTH over 9 x 3 x 3 states."""
    from union_chain import dense_chain
    d, C, Bn, Bf, Wf, mB, mW = base
    P = d['P']
    Jr = reduced_J(d, Bf, Wf, arm, pool, c, tie)
    tg = P.tag[Wf].astype(np.int64)
    PAY, REP = payoff_table_e(c, pool)
    mb = np.ones(len(Bf)) if prior == 'uniform' else mB
    mw = np.ones(len(Wf)) if prior == 'uniform' else mW
    st, lpi, A = dense_chain(Jr, tg, PAY, list(range(len(Bf))), list(range(len(Wf))), mb, mw, float(N), w)
    js = np.array([int(Jr[b, x, y]) for (b, x, y) in st])
    t1 = tg[[x for (_, x, _) in st]]; t2 = tg[[y for (_, _, y) in st]]
    name = lambda k: '%s %s %s' % (Bn[st[k][0]], NAMED_W[st[k][1]], NAMED_W[st[k][2]])
    out, pi = chain_stats(st, lpi, A, js, t1, t2, PAY, REP, arm, c, pool, name)
    out.update(arm=arm, pool=pool, c=c, tie=tie, prior=prior, N=N)
    out['zero_strike_boss_mass'] = float(sum(pi[k] for k, (b, x, y) in enumerate(st) if b == U.bact(0, 0)))
    out['pi_all'] = {name(k): float(pi[k]) for k in range(len(st))}
    return out


def reduced_static(base, arm, pool, c, tie):
    """Static table of the reduced chain's named triples: implemented play, payoffs,
    and every move with its payoff change (the ε-free per-mutant quantities)."""
    from union_chain import log_rho
    d, C, Bn, Bf, Wf, mB, mW = base
    P = d['P']
    Jr = reduced_J(d, Bf, Wf, arm, pool, c, tie)
    tg = P.tag[Wf].astype(np.int64)
    PAY, REP = payoff_table_e(c, pool)
    rows = []
    for b in range(len(Bf)):
        for x in range(len(Wf)):
            for y in range(x, len(Wf)):
                j = int(Jr[b, x, y]); r = PAY[j, tg[x], tg[y]]
                mov = []
                for s in range(3):
                    K = len(Bf) if s == 0 else len(Wf)
                    for q in range(K):
                        t = [b, x, y]
                        if t[s] == q: continue
                        t[s] = q
                        j2 = int(Jr[t[0], t[1], t[2]]); u = PAY[j2, tg[t[1]], tg[t[2]]]
                        du = float(u[s] - r[s])
                        mov.append(dict(slot=['B', 'W1', 'W2'][s], mutant=(Bn[q] if s == 0 else NAMED_W[q]), du=du,
                                        rhoN={str(N): float(np.exp(log_rho(0.3 * du, float(N)))) * N for N in (100, 1000)},
                                        to=U.joint_name(j2), to_summary=U.SUMM[U.summary(j2, tg[t[1]], tg[t[2]])]))
                rows.append(dict(boss=Bn[b], W1=NAMED_W[x], W2=NAMED_W[y], play=U.joint_name(j),
                                 summary=U.SUMM[U.summary(j, tg[x], tg[y])], pay=r.round(3).tolist(),
                                 surplus=float(surplus(j, tg[x], tg[y], PAY, REP)), moves=mov))
    return rows


def part_a(nB=6, levels=(0, 1), K=10):
    """Part A: the unfakeable-polarity union, static only, committed play (CC).
    Every boss function at n = nB with box levels `levels` against every ordered pair
    of the six militant-/union- variants (plus scab and the union run's union for
    reference)."""
    LB = U.RoleLang(nB, U.boss_atoms(levels), U.NB)
    fb, mb, cb, sb = LB.canon()
    mb = mb / mb.sum()
    mp = minus_programs()
    names = list(mp.keys())
    fw = [mp[k] for k in names]
    P = U.Programs(fb, fw)
    Wn = len(fw)
    res = dict(boss_functions=len(fb), levels=list(levels), nB=nB, programs={k: str(v) for k, v in mp.items()})
    # per ordered pair: classify every boss function
    pairs = {}
    audit_viol = 0; audit_n = 0
    lemma0 = 0
    stable = {}
    for x in range(Wn):
        for y in range(Wn):
            cat = {}
            rows = []
            for b in range(len(fb)):
                tr = trace(P, b, x, y, 0, 0, 0, 0.5, 0, K)
                js = [w['imp'] for w in tr]
                j = js[-1]
                v = audit_one(P, b, x, y, j, 0, 0, 0, 0.5, 0, K)
                audit_n += 1
                if v: audit_viol += 1
                si, h, a1, a2 = _decode(j)
                s0 = _decode(js[0])[0]
                # Lemma 0 on the wage boxes: a worker judging the boss fair (BOX_a(s = 1/2) true at the stable world) while it pays low
                for slot in (1, 2):
                    for (L, p, tv) in tr[-1]['atoms'][slot]:
                        if p == KFAIR and tv and si != 2:
                            lemma0 += 1
                fair = si == 2
                strike = bool(a1 or a2)
                key = ('fair' if fair else 'low') + (' struck' if strike else ' worked')
                if not fair and not strike and s0 == 2:
                    key = 'low worked (faker: fair at world 0)'
                cat.setdefault(key, [0, 0.0]); cat[key][0] += 1; cat[key][1] += float(mb[b])
                stable[(b, x, y)] = (j, s0)
            pairs['%s | %s' % (names[x], names[y])] = {k: dict(n=v[0], mass=v[1]) for k, v in sorted(cat.items())}
    res['pairs'] = pairs
    res['audit'] = dict(encounters=audit_n, violations=audit_viol, lemma0_counterexamples=lemma0)
    # activation rule of each self-pair (S8): strikes iff s(world 0) < 1/2 ?
    act = {}
    for x in range(Wn):
        cnt = dict(strike_w0low=0, work_w0low=0, strike_w0fair=0, work_w0fair=0)
        for b in range(len(fb)):
            j, s0 = stable[(b, x, x)]
            st = bool(_decode(j)[2] or _decode(j)[3])
            cnt[('strike' if st else 'work') + ('_w0fair' if s0 == 2 else '_w0low')] += 1
        act[names[x]] = cnt
    res['self_pair_activation'] = act
    # constant low bosses against union- self-pairs
    const = {}
    for x in range(Wn):
        for si in range(3):
            for hi in range(3):
                b = P.index_b[((), (U.bact(si, hi),))]
                j, _ = stable[(b, x, x)]
                const.setdefault(names[x], {})[U.bname(U.bact(si, hi))] = U.joint_name(j)
    res['constants'] = const
    # named bosses: world-by-world traces
    W1w, W1s = (0, 0), (0, 1)
    nb_ = {
        '(0,none)': ((), (U.bact(0, 1),)),
        '(1/4,none)': ((), (U.bact(1, 1),)),
        '(1/2,none)': ((), (U.bact(2, 1),)),
        'union-run faker if(BOX(W1=work),(1/2,none),(0,none))': boss_fn([(0, 0)], lambda tv: U.bact(2, 1) if tv[(0, 0)] else U.bact(0, 1)),
        'bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none))': boss_fn([(0, 1)], lambda tv: U.bact(2, 1) if tv[(0, 1)] else U.bact(0, 1)),
        'level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none))': boss_fn([(1, 1)], lambda tv: U.bact(2, 1) if tv[(1, 1)] else U.bact(0, 1)),
        'low-then-fair if(BOX(W1=work),(0,none),(1/2,none))': boss_fn([(0, 0)], lambda tv: U.bact(0, 1) if tv[(0, 0)] else U.bact(2, 1)),
        'low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none))': boss_fn([(1, 0)], lambda tv: U.bact(0, 1) if tv[(1, 0)] else U.bact(2, 1)),
        'low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none))': boss_fn([(0, 1)], lambda tv: U.bact(0, 1) if tv[(0, 1)] else U.bact(2, 1)),
    }
    pair_list = [(0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (3, 3), (2, 0), (1, 0), (2, 5), (2, 4)]
    traces = {}
    for bn, f in nb_.items():
        b = P.index_b.get(f)
        if b is None:
            continue
        for (x, y) in pair_list:
            tr = trace(P, b, x, y, 0, 0, 0, 0.5, 0, 6)
            rowsT = []
            for w in tr:
                si, h, a1, a2 = _decode(w['imp'])
                boxes = []
                for slot in (1, 2):
                    for (L, p, tv) in w['atoms'][slot]:
                        lab = ('BOX%s(%s)' % ('1' if L else '', 's=1/2' if p == KFAIR else 'OTHER=strike'))
                        boxes.append('W%d:%s=%s' % (slot, lab, 'T' if tv else 'F'))
                rowsT.append('w%d: s=%s %s%s  [%s]' % (w['n'], U.WNAME[si], 'WS'[a1], 'WS'[a2], ', '.join(boxes)))
            traces['%s || %s | %s' % (bn, names[x], names[y])] = rowsT
    res['traces'] = traces
    res['boss_mass'] = dict(constants=float(sum(mb[i] for i, f in enumerate(fb) if not f[0])),
                            conditionals=float(sum(mb[i] for i, f in enumerate(fb) if f[0])))
    return res


def make_base():
    d, C, nmw_f, nmb_f = load_base()
    Bn, Bf, Wf, mB, mW = named_lists(d, C, nmw_f, nmb_f)
    return (d, C, Bn, Bf, Wf, mB, mW)
