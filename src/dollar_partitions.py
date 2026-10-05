"""Divide-the-dollar partitions across islands, with `ROLE`, without `ROLE`, and with fixed slot roles.
Spec specs/2026-10-05-dollar-partitions.md (reviewed, reviews/2026-10-05-dollar-partitions-gpt-6.1-sol.md);
predictions predictions/2026-10-05-dollar-partitions.md.

Weak arm (simulation-based reading, THEM(^A) probes, X), one matched cutoff n for every arm.  Three role
structures (arms):
  role    one population, `ROLE` in the grammar (the environment's public correlating signal), role-averaged payoffs
  norole  one population, no `ROLE` (symmetric, no signal)
  fixed   two slot populations without `ROLE`; a match draws one program from each slot; N is per slot
Class data come from src/dollar.py (classes = identical rows and columns of the payoff matrix U over L_n).  The fixed
arm uses the norole evaluation: a slot-1 program i against a slot-2 program j earns U[i, j], and j earns U[j, i].

Outcomes.  For a pair of classes (a, b), JA[a, b] is the distribution over (a's demand level, b's demand level),
role-averaged when ROLE is on.  Definitions used throughout:
  demand            the level a program submits (1/6 ... 5/6 in dollar5)
  realized payoff   the demand if the two demands sum to at most 1, else 0
  normalized share  d_i / (d_i + d_j) of a compatible match (undefined for a clash)
  split             an efficient match (d_i + d_j = 1), unordered ('1/6-5/6') or ordered ('1/6|5/6', slot 1 first)
  ineff / clash     compatible with d_i + d_j < 1 / incompatible (both get 0)
  E[max share]      expected max realized payoff in an encounter (the three-player convention; clash counts 0)
  dwl               per-agent deadweight loss: 1/2 - mean realized payoff
With ROLE an encounter's ex post split is unequal on a ROLE convention while every program's ex ante payoff is 1/2;
both views are reported (ex ante max share = the largest class-mean payoff in the state).

    python3 src/dollar_partitions.py static [--game dollar5 --n 5]
    python3 src/dollar_partitions.py chain --arm role|norole|fixed --N 100 1000 10000
    python3 src/dollar_partitions.py validate          # joint two-slot simulation vs the fixed-role chain
    python3 src/dollar_partitions.py lottery --arm A --I 64 --N 100 --mN 0.1 [--runs 40]
    python3 src/dollar_partitions.py merge
    python3 src/dollar_partitions.py report
"""
import argparse, json, math, os, re, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")          # one thread per worker (3-worker budget)
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar as D
from dsl import CONST, X as OPX, ROLE as OPROLE, APP
from chain import fixation, replicator

ROOT = D.ROOT
OUT = os.path.join(ROOT, 'runs', 'dollar_partitions')
os.makedirs(OUT, exist_ok=True)
W = 0.3
ARMS = ('role', 'norole', 'fixed')
NDEF = 5


# ------------------------------------------------------------------ class data
_CACHE = {}


def data(game='dollar5', n=NDEF, arm='role'):
    key = (game, n, arm == 'role')
    if key in _CACHE:
        d = dict(_CACHE[key]); d['arm'] = arm
        return d
    E = D.load_or_evaluate(game, n, role=(arm == 'role'), verbose=False)
    g, L, ids = E['game'], E['L'], E['ids']
    K = len(E['reps'])
    v = g.values
    # kinds
    kinds = []
    for mem in E['members']:
        progs = sorted((int(ids[a]) for a in mem), key=lambda p: (L.size[p], p))
        if any(L.size[p] == 1 and L.op[p] == CONST for p in progs):
            kinds.append('constant'); continue
        blind = [p for p in progs if 'THEM' not in L.src(p)]
        if not blind:
            kinds.append('reader'); continue
        tok = set(re.findall(r'[A-Za-z0-9]+', L.src(blind[0])))
        kinds.append('coin' if 'X' in tok else ('role-split' if 'ROLE' in tok else 'blind'))
    JA = E['JA']
    self_out = [outcome_of(JA[c, c], v) for c in range(K)]
    d = dict(game=g, gname=game, n=n, arm=arm, L=L, ids=ids, K=K, U=E['U'], JA=JA, mu=E['mu'], names=E['names'],
             sizes=E['sizes'], members=E['members'], kinds=kinds, values=v, self_out=self_out, div=E['div'])
    _CACHE[key] = d
    return dict(d)


def const_index(d):
    """class index of each constant level."""
    out = {}
    for c in range(d['K']):
        nm = d['names'][c]
        if nm in d['game'].actions:
            out[nm] = c
    return out


# ------------------------------------------------------------------ outcomes
def labels(v):
    k = len(v)
    lab = np.empty((k, k), dtype=object); olab = np.empty((k, k), dtype=object)
    for i in range(k):
        for j in range(k):
            s = v[i] + v[j]
            if abs(s - 1) < 1e-9:
                lo = min(v[i], v[j])
                lab[i, j] = '%s-%s' % (D.frac(lo), D.frac(1 - lo))
                olab[i, j] = '%s|%s' % (D.frac(v[i]), D.frac(v[j]))
            elif s < 1:
                lab[i, j] = olab[i, j] = 'ineff'
            else:
                lab[i, j] = olab[i, j] = 'clash'
    return lab, olab


def split_names(v):
    lab, olab = labels(v)
    uns = sorted({x for x in lab.ravel() if '-' in x}, key=lambda s: eval(s.split('-')[0]))
    ords = sorted({x for x in olab.ravel() if '|' in x}, key=lambda s: eval(s.split('|')[0]))
    return uns, ords


def outcome_of(J, v):
    """Statistics of a (k, k) joint distribution over (i's level, j's level)."""
    lab, olab = labels(v)
    out = defaultdict(float)
    S = v[:, None] + v[None, :]
    pay_i = np.where(S <= 1 + 1e-9, v[:, None] + 0 * v[None, :], 0.0)
    pay_j = np.where(S <= 1 + 1e-9, v[None, :] + 0 * v[:, None], 0.0)
    k = len(v)
    for i in range(k):
        for j in range(k):
            p = J[i, j]
            if p <= 0: continue
            out[lab[i, j]] += p
            if '|' in olab[i, j]: out['o:' + olab[i, j]] += p
    out['eff'] = float(sum(p for kk, p in out.items() if '-' in kk))
    out['pay_i'] = float((J * pay_i).sum()); out['pay_j'] = float((J * pay_j).sum())
    out['mean_pay'] = 0.5 * (out['pay_i'] + out['pay_j'])
    out['dwl'] = 0.5 - out['mean_pay']
    out['E_max_pay'] = float((J * np.maximum(pay_i, pay_j)).sum())
    comp = S <= 1 + 1e-9
    sh = np.maximum(v[:, None], v[None, :]) / S
    pc = float(J[comp].sum())
    out['E_max_share_compat'] = float((J * sh * comp).sum() / pc) if pc > 0 else float('nan')
    return dict(out)


def label_of(o, thr=0.99):
    """dominant outcome label of an outcome dict (unordered), or 'mixed'."""
    best = max((kk for kk in o if ('-' in kk or kk in ('ineff', 'clash')) and not kk.startswith('o:')), key=lambda kk: o[kk])
    return best if o[best] >= thr else 'mixed'


def olabel_of(o, thr=0.99):
    cands = [kk for kk in o if kk.startswith('o:')] + [kk for kk in ('ineff', 'clash') if kk in o]
    if not cands: return 'mixed'
    best = max(cands, key=lambda kk: o[kk])
    return (best[2:] if best.startswith('o:') else best) if o[best] >= thr else 'mixed'


def pop_outcome(d, cls, cnt):
    """one population, counts cnt over classes cls, random matching without self-matching."""
    c = np.asarray(cnt, float); cls = np.asarray(cls)
    Wm = np.outer(c, c) - np.diag(c)
    if Wm.sum() <= 0:
        Wm = np.outer(c, c)
    Wm /= Wm.sum()
    J = np.einsum('ab,abij->ij', Wm, d['JA'][np.ix_(cls, cls)])
    o = outcome_of(J, d['values'])
    fit = d['U'][np.ix_(cls, cls)] @ (c / c.sum())
    o['exante_max'] = float(fit.max())
    return o


def slot_outcome(d, a, b):
    """fixed roles, monomorphic slots: slot 1 class a, slot 2 class b."""
    o = outcome_of(d['JA'][a, b], d['values'])
    o['exante_max'] = float(max(d['U'][a, b], d['U'][b, a]))
    o['slot1'] = float(d['U'][a, b]); o['slot2'] = float(d['U'][b, a])
    return o


# ------------------------------------------------------------------ static
def crossing(U, a, b):
    den = (U[b, b] - U[b, a]) - (U[a, b] - U[a, a])
    if abs(den) < 1e-12: return None
    x = (U[a, a] - U[b, a]) / den
    return float(x) if 0 < x < 1 else None


def rho1(U, q, a, N, w=W):
    return float(fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, w, N))


def log_rho_const(du, N, w=W):
    """log fixation probability of one mutant under constant selection, fitness ratio exp(w du)."""
    dw = w * du
    if abs(dw) < 1e-12: return -math.log(N)
    if dw > 0: return math.log(-math.expm1(-dw)) - math.log(-math.expm1(-N * dw))
    a = -dw
    return math.log(math.expm1(a)) - N * a - math.log(-math.expm1(-N * a))


def induced_prior(d):
    """prior mass by kind and by self-play outcome label."""
    mu = d['mu']; K = d['K']
    by_kind = defaultdict(float); by_self = defaultdict(float); cnt_kind = Counter()
    for c in range(K):
        by_kind[d['kinds'][c]] += mu[c]; cnt_kind[d['kinds'][c]] += 1
        by_self[label_of(d['self_out'][c], 0.999)] += mu[c]
    return dict(by_kind=dict(by_kind), n_kind=dict(cnt_kind), by_selfplay=dict(by_self))


def shadows_of(d, a):
    """classes on-path identical to a in a monomorphic all-a population (one population)."""
    U = d['U']
    return [c for c in range(d['K']) if c != a and abs(U[c, a] - U[a, a]) < 1e-9 and abs(U[a, c] - U[a, a]) < 1e-9
            and abs(U[c, c] - U[a, a]) < 1e-9]


def static_onepop(d, Ns=(100, 1000, 10000)):
    """contest table among the heaviest efficient conventions and the one- and two-step exits of each."""
    U, mu, names, K, v = d['U'], d['mu'], d['names'], d['K'], d['values']
    eff = [c for c in range(K) if d['self_out'][c]['eff'] > 1 - 1e-9]
    conv = {}
    for c in eff:
        conv.setdefault(label_of(d['self_out'][c]), []).append(c)
    top = []
    for lab, cs in sorted(conv.items()):
        cs = sorted(cs, key=lambda c: -mu[c])
        top += cs[:2]
    res = dict(conventions={lab: [(names[c], float(mu[c]), d['kinds'][c]) for c in sorted(cs, key=lambda c: -mu[c])[:6]] for lab, cs in conv.items()},
               conv_mass={lab: float(mu[cs].sum()) for lab, cs in conv.items()}, n_conv={lab: len(cs) for lab, cs in conv.items()})
    pw = []
    for q in top:
        for a in top:
            if q == a: continue
            pw.append(dict(q=names[q], a=names[a], uqa=float(U[q, a]), uaq=float(U[a, q]), uqq=float(U[q, q]), uaa=float(U[a, a]),
                           cross_q=crossing(U, a, q), rho=[rho1(U, q, a, N) for N in Ns]))
    res['pairwise'] = pw
    # exits of each top convention: direct (one step) and through a neutral entrant (two steps)
    ex = {}
    for a in top:
        row = {}
        for N in Ns:
            direct = defaultdict(float); twostep = defaultdict(float)
            for q in range(K):
                if q == a: continue
                r = rho1(U, q, a, N)
                lab = label_of(d['self_out'][q])
                if q in shadows_of(d, a):
                    # neutral entrant: from all-q, the strict exits of q weighted by mu*rho, as a share of all exits of all-q
                    tot = 0.0; strict = defaultdict(float)
                    for q2 in range(K):
                        if q2 in (q,): continue
                        r2 = rho1(U, q2, q, N)
                        tot += mu[q2] * r2
                        if U[q2, q] > U[q, q] + 1e-9:
                            strict[label_of(d['self_out'][q2])] += mu[q2] * r2
                    for lab2, wgt in strict.items():
                        twostep[lab2] += mu[q] * r * wgt / tot
                else:
                    direct[lab] += mu[q] * r
            row[N] = dict(direct=dict(direct), via_neutral=dict(twostep))
        ex[names[a]] = dict(label=label_of(d['self_out'][a]), mu=float(mu[a]), n_shadows=len(shadows_of(d, a)),
                            shadow_mass=float(mu[shadows_of(d, a)].sum()), exits=row)
    res['exits'] = ex
    return res


def static_fixed(d, Ns=(100, 1000, 10000)):
    """fixed roles: constant conventions (S_i | S_j) efficient, their adjacent moves (direct constant-to-constant and
    conceder paths), with prior-weighted entry and exit rates per mutation event (a mutation event picks a slot
    uniformly)."""
    U, mu, names, K, v = d['U'], d['mu'], d['names'], d['K'], d['values']
    ci = const_index(d)
    acts = d['game'].actions
    k = len(acts)
    convs = [(ci[acts[i]], ci[acts[j]]) for i in range(k) for j in range(k) if abs(v[i] + v[j] - 1) < 1e-9]
    out = {}
    for (a, b) in convs:
        lab = '%s|%s' % (D.frac(v[acts.index(names[a])]), D.frac(v[acts.index(names[b])]))
        rows = {}
        for N in Ns:
            # direct moves: a constant mutant in one slot fixes against the other slot's constant
            direct = defaultdict(float); conceder = defaultdict(float); neutral_mass = [0.0, 0.0]
            for s, (me, other) in enumerate(((a, b), (b, a))):
                for q in range(K):
                    if q == me: continue
                    du = U[q, other] - U[me, other]
                    lr = log_rho_const(du, N)
                    r = 0.5 * mu[q] * math.exp(lr)
                    o = slot_outcome(d, q, other) if s == 0 else slot_outcome(d, other, q)
                    nl = olabel_of(o)
                    if abs(du) < 1e-9:
                        neutral_mass[s] += mu[q]
                        # conceder path: from (q, other) [slot s now q], the other slot's strict improvements
                        tot = 0.0; strict = defaultdict(float)
                        st = (q, other) if s == 0 else (other, q)
                        for s2 in (0, 1):
                            me2, oth2 = (st[0], st[1]) if s2 == 0 else (st[1], st[0])
                            for q2 in range(K):
                                if q2 == me2: continue
                                du2 = U[q2, oth2] - U[me2, oth2]
                                r2 = 0.5 * mu[q2] * math.exp(log_rho_const(du2, N))
                                tot += r2
                                if du2 > 1e-9:
                                    nst = (q2, oth2) if s2 == 0 else (oth2, q2)
                                    strict[olabel_of(slot_outcome(d, *nst))] += r2
                        for l2, w2 in strict.items():
                            if l2 != lab:
                                conceder[l2] += r * w2 / tot
                    elif nl != lab:
                        direct[nl] += r
            rows[N] = dict(direct=dict(direct), conceder=dict(conceder), exit_total=float(sum(direct.values()) + sum(conceder.values())),
                           neutral_mass_slot=neutral_mass)
        out[lab] = dict(state=(names[a], names[b]), rows=rows)
    # entry rates: sum over sources of the two-step flux into each convention, read off the exit tables
    for N in Ns:
        ent = defaultdict(float)
        for lab, r in out.items():
            for kind in ('direct', 'conceder'):
                for l2, wgt in r['rows'][N][kind].items():
                    ent[l2] += wgt
        for lab in out:
            out[lab]['rows'][N]['entry_from_constant_conventions'] = float(ent.get(lab, 0.0))
    return out


def replicator2(U, x, y, steps=20000, h=0.5, tol=1e-10):
    """two-population replicator (slot 1 x, slot 2 y), exponential steps."""
    for t in range(steps):
        fx = U @ y; fy = U @ x
        xn = x * np.exp(h * (fx - x @ fx)); xn /= xn.sum()
        yn = y * np.exp(h * (fy - y @ fy)); yn /= yn.sum()
        if max(np.abs(xn - x).max(), np.abs(yn - y).max()) < tol:
            return xn, yn
        x, y = xn, yn
        x[x < 1e-12] = 0; y[y < 1e-12] = 0
        x /= x.sum(); y /= y.sum()
    return x, y


def static_basins(d, N=100, draws=400, seed=5):
    """deterministic replicator from multinomial(N) draws of the prior (one island's seed, no drift): the share of
    seeds whose rest point carries each outcome label (a static stand-in for the scramble; drift is ignored)."""
    rng = np.random.default_rng(seed)
    agg = Counter()
    for t in range(draws):
        if d['arm'] == 'fixed':
            x = rng.multinomial(N, d['mu']) / N; y = rng.multinomial(N, d['mu']) / N
            x, y = replicator2(d['U'], x.astype(float), y.astype(float))
            J = np.einsum('a,b,abij->ij', x, y, d['JA'])
            agg[olabel_of(outcome_of(J, d['values']), 0.95)] += 1
        else:
            x = rng.multinomial(N, d['mu']) / N
            xs, st, _, _ = replicator(d['U'], x.astype(float), rest_tol=1e-10, ext_tol=1e-8)
            agg[label_of(pop_outcome(d, np.arange(d['K']), xs * 1e6), 0.95)] += 1
    return {k: v / draws for k, v in agg.most_common()}


def cmd_static(a):
    res = {}
    lines = ['# Static tables: divide-the-dollar partitions (spec specs/2026-10-05-dollar-partitions.md)', '',
             'Weak arm, n = %d in every arm, w = %.1f.  Prior masses are in the cut unit (normalized over the classes of L_n).' % (a.n, W), '']
    for game in a.games:
        for arm in (a.arms or ARMS):
            if not os.path.exists(os.path.join(ROOT, 'runs', 'dollar_eval_%s_n%d%s.npz' % (game, a.n, '' if arm == 'role' else '_norole'))):
                lines += ['## %s, arm %s: not evaluated' % (game, arm), '']
                continue
            d = data(game, a.n, arm)
            K = d['K']
            ip = induced_prior(d)
            tag = '%s_%s' % (game, arm)
            res[tag] = dict(K=K, n_programs=len(d['ids']), div=d['div'], induced=ip)
            lines += ['## %s, arm %s: %d programs, %d classes, divergent pairs %.4f' % (game, arm, len(d['ids']), K, d['div']), '']
            lines.append('Induced prior by kind: ' + ', '.join('%s %.4f (%d classes)' % (k, m, ip['n_kind'][k]) for k, m in sorted(ip['by_kind'].items(), key=lambda kv: -kv[1])))
            lines.append('')
            lines.append('Induced prior by self-play outcome: ' + ', '.join('%s %.4f' % (k, m) for k, m in sorted(ip['by_selfplay'].items(), key=lambda kv: -kv[1])))
            lines.append('')
            bs = static_basins(d)
            res[tag]['basins_N100'] = bs
            lines.append('Deterministic replicator from 400 multinomial(100) seeds of the prior (%s; no drift; label at >= 0.95 of encounters): ' % (
                'two-population' if arm == 'fixed' else 'one population') + ', '.join('%s %.3f' % kv for kv in bs.items()))
            lines.append('')
            if arm == 'fixed':
                st = static_fixed(d)
                res[tag]['fixed'] = st
                lines += ['Adjacent moves of each constant convention (slot 1 | slot 2), rates per mutation event (a slot drawn '
                          'uniformly, then a mutant from its prior; constant-selection Moran fixation, N per slot). '
                          '*direct*: one mutant fixes and changes the ordered split; *conceder*: a neutral entrant fixes, then the '
                          'other slot\'s strict move (rate = neutral step x share of the strict move among all exits of the '
                          'intermediate state). Entry = flux into the convention from the other constant conventions by these moves.', '',
                          '| convention | N | exit total | direct (to) | conceder (to) | entry from constant conventions | neutral entrant mass slot 1 / slot 2 |',
                          '|---|---|---|---|---|---|---|']
                for lab, r in st.items():
                    for N, rr in r['rows'].items():
                        lines.append('| %s `%s|%s` | %d | %.3g | %s | %s | %.3g | %.3f / %.3f |' % (
                            lab, r['state'][0], r['state'][1], N, rr['exit_total'],
                            ', '.join('%s %.2g' % kv for kv in sorted(rr['direct'].items(), key=lambda kv: -kv[1])[:4]) or '-',
                            ', '.join('%s %.2g' % kv for kv in sorted(rr['conceder'].items(), key=lambda kv: -kv[1])[:4]) or '-',
                            rr['entry_from_constant_conventions'], *rr['neutral_mass_slot']))
                lines.append('')
            else:
                st = static_onepop(d)
                res[tag]['onepop'] = st
                lines.append('Efficient monomorphic conventions by split: ' + '; '.join(
                    '%s: %d classes, mass %.4f (top %s)' % (lab, st['n_conv'][lab], st['conv_mass'][lab],
                                                             ', '.join('`%s` %.4f %s' % t for t in st['conventions'][lab][:3]))
                    for lab in sorted(st['conv_mass'])))
                lines += ['', 'Pairwise contests (row q invades column a): u(q,a) / u(a,q), crossing frequency of q (q wins above it), '
                          'Moran fixation of one q at N = 100 / 1,000 / 10,000 (w = 0.3; neutral 1/N).', '',
                          '| q | a | u(q,a) / u(a,q) | crossing of q | rho N=100 | rho N=1000 | rho N=10000 |', '|---|---|---|---|---|---|---|']
                for p in st['pairwise']:
                    lines.append('| `%s` | `%s` | %.3f / %.3f | %s | %.3g | %.3g | %.3g |' % (
                        p['q'], p['a'], p['uqa'], p['uaq'], '%.3f' % p['cross_q'] if p['cross_q'] is not None else '-', *p['rho']))
                lines += ['', 'Exits of each convention by destination self-play outcome (mu * rho per mutation event): direct = a '
                          'non-neutral mutant; via neutral = a neutral entrant (on-path identical shadow, mu/N) followed by a strict '
                          'invader of the shadow (share of the shadow state\'s exits).', '',
                          '| convention | split | shadows (mass) | N | direct | via neutral |', '|---|---|---|---|---|---|']
                for nm, r in st['exits'].items():
                    for N, rr in r['exits'].items():
                        lines.append('| `%s` | %s | %d (%.3f) | %d | %s | %s |' % (
                            nm, r['label'], r['n_shadows'], r['shadow_mass'], N,
                            ', '.join('%s %.2g' % kv for kv in sorted(rr['direct'].items(), key=lambda kv: -kv[1])[:4]) or '-',
                            ', '.join('%s %.2g' % kv for kv in sorted(rr['via_neutral'].items(), key=lambda kv: -kv[1])[:4]) or '-'))
                lines.append('')
    json.dump(res, open(os.path.join(OUT, 'static_%s.json' % '_'.join(a.games)), 'w'), indent=1, default=str)
    open(os.path.join(OUT, 'static_%s.md' % '_'.join(a.games)), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


# ------------------------------------------------------------------ chains
from abm import njit


@njit(cache=True)
def gth_linear(P):
    """stationary distribution of a row-stochastic matrix P by GTH, linear domain (no subtractions)."""
    n = P.shape[0]
    A = P.copy()
    for i in range(n):
        A[i, i] = 0.0
    s = np.zeros(n)
    for k in range(n - 1, 0, -1):
        sk = 0.0
        for j in range(k):
            sk += A[k, j]
        if sk <= 0.0:
            sk = 1e-300
        s[k] = sk
        for i in range(k):
            aik = A[i, k]
            if aik == 0.0:
                continue
            f = aik / sk
            for j in range(k):
                A[i, j] += f * A[k, j]
    x = np.zeros(n)
    x[0] = 1.0
    for k in range(1, n):
        v = 0.0
        for i in range(k):
            v += x[i] * A[i, k]
        x[k] = v / s[k]
    return x / x.sum()


def lrho_vec(du, N, w=W):
    """vectorized log fixation probability under constant selection, fitness ratio exp(w du)."""
    dw = w * np.asarray(du, float)
    out = np.full(dw.shape, -math.log(N))
    pos = dw > 1e-12; neg = dw < -1e-12
    out[pos] = np.log(-np.expm1(-dw[pos])) - np.log(-np.expm1(-N * dw[pos]))
    a = -dw[neg]
    out[neg] = np.log(np.expm1(a)) - N * a - np.log(-np.expm1(-N * a))
    return out


def fixed_chain(d, N, w=W, rel_drop=1e-25):
    """eps -> 0 chain over joint monomorphic configurations (a, b) of the two slot populations (spec 'The fixed-role
    chain').  A mutation event picks a slot uniformly, draws q from the slot's prior; q fixes in that slot with the
    constant-selection Moran probability at per-slot size N (a slot's fitness depends only on the other slot's
    resident, so selection is frequency-independent within the slot).  Solved on the embedded jump chain (entries
    below rel_drop of a row's total are dropped and the dropped flow reported), then pi(s) = pi_jump(s) / R(s), R(s)
    the total exit rate per mutation event (log domain)."""
    U, mu, K = d['U'], d['mu'], d['K']
    lmu = np.log(0.5 * mu)
    du1 = U.T[None, :, :] - U[:, :, None]          # du1[a, b, q] = U[q, b] - U[a, b]   (slot-1 mutant q)
    du2 = U.T[:, None, :] - U.T[:, :, None]        # du2[a, b, q] = U[q, a] - U[b, a]   (slot-2 mutant q)
    L1 = lrho_vec(du1, N, w) + lmu[None, None, :]
    L2 = lrho_vec(du2, N, w) + lmu[None, None, :]
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    mm = np.maximum(L1.max(axis=2), L2.max(axis=2))
    R = mm + np.log(np.exp(L1 - mm[:, :, None]).sum(axis=2) + np.exp(L2 - mm[:, :, None]).sum(axis=2))
    P1 = np.exp(L1 - R[:, :, None]); P2 = np.exp(L2 - R[:, :, None])
    dropped = (P1 * (P1 < rel_drop)).sum(axis=2) + (P2 * (P2 < rel_drop)).sum(axis=2)
    P1[P1 < rel_drop] = 0.0; P2[P2 < rel_drop] = 0.0
    S = K * K
    P = np.zeros((S, S))
    for a in range(K):
        for b in range(K):
            s0 = a * K + b
            P[s0, idx * K + b] += P1[a, b]
            P[s0, a * K + idx] += P2[a, b]
    xj = gth_linear(P)
    lpi = np.log(np.maximum(xj, 1e-320)) - R.ravel()
    lpi -= lpi.max()
    pi = np.exp(lpi); pi /= pi.sum()
    return dict(pi=pi.reshape(K, K), logR=R, P1=P1, P2=P2, cut=float((xj.reshape(K, K) * dropped).sum()), xjump=xj.reshape(K, K))


def fixed_summary(d, ch, top=15):
    """outcomes, support and transition structure of a fixed-role chain."""
    K, pi, names, kinds, v = d['K'], ch['pi'], d['names'], d['kinds'], d['values']
    uns, ords = split_names(v)
    acc = defaultdict(float); lab_mass = defaultdict(float); olab_mass = defaultdict(float)
    slot_more = defaultdict(float)
    st_lab = np.empty((K, K), dtype=object)
    for a in range(K):
        for b in range(K):
            p = pi[a, b]
            o = slot_outcome(d, a, b)
            st_lab[a, b] = olabel_of(o)
            for kk in list(uns) + ['ineff', 'clash', 'eff', 'E_max_pay', 'dwl', 'mean_pay', 'exante_max', 'slot1', 'slot2'] + ['o:' + x for x in ords]:
                acc[kk] += p * o.get(kk, 0.0)
            if o.get('E_max_share_compat') == o.get('E_max_share_compat'):
                acc['_n'] += p * o['E_max_share_compat'] * (1 - o.get('clash', 0.0)); acc['_c'] += p * (1 - o.get('clash', 0.0))
            lab_mass[label_of(o)] += p; olab_mass[st_lab[a, b]] += p
            slot_more['slot1' if o['slot1'] > o['slot2'] + 1e-9 else ('slot2' if o['slot2'] > o['slot1'] + 1e-9 else 'equal')] += p
    acc['E_max_share_compat'] = acc.pop('_n') / max(acc.pop('_c'), 1e-300)
    order = np.argsort(-pi.ravel())[:top]
    support = []
    for s0 in order:
        a, b = divmod(int(s0), K)
        support.append(dict(state='%s | %s' % (names[a], names[b]), kinds=(kinds[a], kinds[b]), pi=float(pi[a, b]), label=st_lab[a, b]))
    const = [c for c in range(K) if kinds[c] == 'constant']
    mass_const_pair = float(pi[np.ix_(const, const)].sum())
    # lumped flux between ordered labels per unit time, and the share leaving from states with a non-constant slot
    flux = defaultdict(float); flux_nc = defaultdict(float)
    R = np.exp(ch['logR'] - ch['logR'].max())
    scale = float((pi * R).sum())
    for a in range(K):
        for b in range(K):
            p = pi[a, b]
            if p < 1e-14: continue
            la = st_lab[a, b]
            nc = not (kinds[a] == 'constant' and kinds[b] == 'constant')
            for q in range(K):
                for (pr, t) in ((ch['P1'][a, b, q], (q, b)), (ch['P2'][a, b, q], (a, q))):
                    if pr <= 0: continue
                    lb = st_lab[t]
                    if lb != la:
                        f = p * R[a, b] * pr / scale
                        flux[(la, lb)] += f
                        if nc: flux_nc[(la, lb)] += f
    trans = [dict(src=x, dst=y, flux=f, share_from_nonconstant_states=flux_nc[(x, y)] / f if f > 0 else 0.0,
                  rate_per_unit_mass=f / olab_mass[x] if olab_mass[x] > 0 else 0.0)
             for (x, y), f in sorted(flux.items(), key=lambda kv: -kv[1])[:40]]
    net = {}
    for (x, y), f in flux.items():
        if (y, x) in flux and x < y:
            net['%s -> %s' % (x, y)] = f - flux[(y, x)]
    return dict(outcome={k: float(v_) for k, v_ in acc.items()}, state_label_mass=dict(lab_mass), ordered_label_mass=dict(olab_mass),
                slot_more=dict(slot_more), mass_constant_pairs=mass_const_pair, support=support, transitions=trans, net_flux=net, cut=ch['cut'])


def fixed_generator(d, N, w=W):
    U, mu, K = d['U'], d['mu'], d['K']
    R1 = np.exp(lrho_vec(U.T[None, :, :] - U[:, :, None], N, w)) * 0.5 * mu[None, None, :]
    R2 = np.exp(lrho_vec(U.T[:, None, :] - U.T[:, :, None], N, w)) * 0.5 * mu[None, None, :]
    S = K * K
    Q = np.zeros((S, S)); idx = np.arange(K)
    for a in range(K):
        for b in range(K):
            r1 = R1[a, b].copy(); r1[a] = 0
            r2 = R2[a, b].copy(); r2[b] = 0
            Q[a * K + b, idx * K + b] += r1
            Q[a * K + b, a * K + idx] += r2
    np.fill_diagonal(Q, 0); np.fill_diagonal(Q, -Q.sum(1))
    return Q


def fixed_hitting(d, N, w=W):
    """convention-to-convention moves of the fixed-role chain: from each efficient constant pair, the distribution of
    the next *different* efficient constant pair hit (returns to the source allowed), the expected time to it (mutation
    events), and the exact exit time and exit distribution by ordered label (the first state of another label, often
    a transient conceder state)."""
    K = d['K']; acts = d['game'].actions; v = d['values']; ci = const_index(d)
    Q = fixed_generator(d, N, w)
    S = K * K
    lab = np.array([[olabel_of(slot_outcome(d, a, b)) for b in range(K)] for a in range(K)], dtype=object).ravel()
    conv = [(ci[acts[i]] * K + ci[acts[j]], '%s|%s' % (D.frac(v[i]), D.frac(v[j]))) for i in range(len(acts)) for j in range(len(acts)) if abs(v[i] + v[j] - 1) < 1e-9]
    cs = [c for c, _ in conv]
    out = {}
    for s0, name in conv:
        A = [c for c in cs if c != s0]
        rest = np.setdiff1d(np.arange(S), A)
        Qrr = Q[np.ix_(rest, rest)]
        H = np.linalg.solve(-Qrr, Q[np.ix_(rest, A)])
        T = np.linalg.solve(-Qrr, np.ones(len(rest)))
        p = int(np.searchsorted(rest, s0))
        nxt = {conv[cs.index(c)][1]: float(h) for c, h in zip(A, H[p])}
        X = np.nonzero(lab == lab[s0])[0]
        Qxx = Q[np.ix_(X, X)]
        tx = np.linalg.solve(-Qxx, np.ones(len(X)))
        outside = np.setdiff1d(np.arange(S), X)
        Hx = np.linalg.solve(-Qxx, Q[np.ix_(X, outside)])
        px = int(np.searchsorted(X, s0))
        ex = defaultdict(float)
        for o, h in zip(outside, Hx[px]):
            ex[lab[o]] += h
        out[name] = dict(next_convention=nxt, time_to_next=float(T[p]), exit_time=float(tx[px]), exit_to=dict(ex))
    return out


class ClassProvider:
    """chain.Chain provider over the class-level payoff matrix (classes are already deduplicated)."""
    def __init__(self, U, mu):
        self.Ufull = np.round(np.asarray(U, float), 9)
        K = len(mu)
        self.classes = sorted([(c, [c], float(mu[c])) for c in range(K)], key=lambda c: -c[2])
        self._R = np.array([c[0] for c in self.classes])
        self._b = {}

    def prepare(self, support):
        pass

    def U(self, ids, sup=None):
        ids = [int(p) for p in ids]
        return self.Ufull[np.ix_(ids, ids)]

    def mutant_classes(self, support):
        return self.classes

    def blocks_for(self, support):
        sup = tuple(int(p) for p in support)
        b = self._b.get(sup)
        if b is None:
            si = np.array(sup, int); R = self._R
            b = (self.Ufull[np.ix_(R, si)], self.Ufull[np.ix_(si, R)], self.Ufull[R, R], self.Ufull[np.ix_(si, si)])
            self._b[sup] = b
        return b


def onepop_chain(d, N, w=W, theta=1e-7, max_states=30000):
    from chain import Chain
    prov = ClassProvider(d['U'], d['mu'])
    ch = Chain(prov, N=N, w=w, theta=theta, max_states=max_states).explore()
    return ch, prov


def onepop_summary(d, ch, top=15):
    names, kinds = d['names'], d['kinds']
    uns, ords = split_names(d['values'])
    acc = defaultdict(float); lab_mass = defaultdict(float)
    st_lab = {}
    for key, p in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]
        cnt = np.round(np.asarray(x) * ch.N).astype(int)
        o = pop_outcome(d, ids, cnt)
        st_lab[key] = label_of(o)
        lab_mass[st_lab[key]] += p
        for kk in list(uns) + ['ineff', 'clash', 'eff', 'E_max_pay', 'dwl', 'mean_pay', 'exante_max'] + ['o:' + z for z in ords]:
            acc[kk] += p * o.get(kk, 0.0)
        if o.get('E_max_share_compat') == o.get('E_max_share_compat'):
            acc['_n'] += p * o['E_max_share_compat'] * (1 - o.get('clash', 0.0)); acc['_c'] += p * (1 - o.get('clash', 0.0))
    acc['E_max_share_compat'] = acc.pop('_n') / max(acc.pop('_c'), 1e-300)

    def desc(key):
        ids, x, kind = ch.states[key]
        return ' + '.join('%s:%.2f' % (names[i], xi) for i, xi in zip(ids, x))
    order = np.argsort(-ch.pi)[:top]
    support = [dict(state=desc(ch.keys_list[i]), kinds=[kinds[c] for c in ch.states[ch.keys_list[i]][0]], pi=float(ch.pi[i]),
                    label=st_lab[ch.keys_list[i]]) for i in order]
    mono_const = sum(p for key, p in zip(ch.keys_list, ch.pi) if len(ch.states[key][0]) == 1 and kinds[ch.states[key][0][0]] == 'constant')
    poly = sum(p for key, p in zip(ch.keys_list, ch.pi) if len(ch.states[key][0]) > 1)
    flux = defaultdict(float); flux_nc = defaultdict(float)
    for key, p in zip(ch.keys_list, ch.pi):
        if p < 1e-14: continue
        la = st_lab[key]
        ids = ch.states[key][0]
        nc = not (len(ids) == 1 and kinds[ids[0]] == 'constant')
        for k2, pr in ch.trans[key].items():
            if k2 == key or k2 not in st_lab: continue
            lb = st_lab[k2]
            if lb != la:
                flux[(la, lb)] += p * pr
                if nc: flux_nc[(la, lb)] += p * pr
    trans = [dict(src=x, dst=y, flux=f, share_from_nonconstant_states=flux_nc[(x, y)] / f, rate_per_unit_mass=f / lab_mass[x])
             for (x, y), f in sorted(flux.items(), key=lambda kv: -kv[1])[:40]]
    exits = []
    for i in order[:6]:
        key = ch.keys_list[i]
        row = []
        for wgt, k2, muts in ch.out_transitions(key, top=5):
            row.append(dict(to=desc(k2), label=st_lab.get(k2, '?'), p=float(wgt), mutants=[(names[int(q)], float(m)) for q, m in muts]))
        exits.append(dict(state=desc(key), exits=row))
    net = {}
    for (x, y), f in flux.items():
        if (y, x) in flux and x < y:
            net['%s -> %s' % (x, y)] = f - flux[(y, x)]
    return dict(outcome={k: float(v_) for k, v_ in acc.items()}, state_label_mass=dict(lab_mass), mass_mono_constant=mono_const,
                mass_polymorphic=poly, support=support, transitions=trans, top_exits=exits, net_flux=net, cut_flow=float(ch.cut_flow),
                poly_flow=float(ch.poly_flow), indeterminate=len(ch.indeterminate), n_states=len(ch.trans))


def cmd_chain(a):
    for N in a.N:
        t0 = time.time()
        d = data(a.game, a.n, a.arm)
        if a.arm == 'fixed':
            r = fixed_summary(d, fixed_chain(d, N))
            r['hitting'] = fixed_hitting(d, N)
        else:
            ch, prov = onepop_chain(d, N)
            r = onepop_summary(d, ch)
        r.update(game=a.game, n=a.n, arm=a.arm, N=N, w=W, K=d['K'], time_s=time.time() - t0)
        fn = os.path.join(OUT, 'chain_%s_n%d_%s_N%d.json' % (a.game, a.n, a.arm, N))
        json.dump(r, open(fn, 'w'), indent=1, default=str)
        o = r['outcome']
        print('%s n=%d %s N=%d: %s | eff %.4f Emax %.3f dwl %.4f (%.0fs)' % (
            a.game, a.n, a.arm, N, ', '.join('%s %.4f' % (k, o[k]) for k in sorted(o) if '-' in k or '|' in k or k in ('ineff', 'clash')),
            o['eff'], o['E_max_pay'], o['dwl'], r['time_s']), flush=True)
        print('   support:', '; '.join('%s %.4f (%s)' % (s['state'], s['pi'], s['label']) for s in r['support'][:8]), flush=True)


# ------------------------------------------------------------------ islands (eps = 0 lottery, merges, joint simulation)
@njit(cache=True)
def _draw(w_, tot):
    u = np.random.random() * tot
    acc = 0.0
    for t in range(w_.shape[0]):
        acc += w_[t]
        if u <= acc:
            return t
    return w_.shape[0] - 1


@njit(cache=True)
def _parent(counts, pay, U, pres, npres, j, s, S, N, w):
    """class of a parent drawn on (island j, slot s) with weight count * exp(w * fitness)."""
    n = npres[j, s]
    f = np.empty(n)
    m = -1e300
    for t in range(n):
        k = pres[j, s, t]
        if S == 1:
            f[t] = (pay[j, s, k] - U[k, k]) / (N - 1)
        else:
            f[t] = pay[j, s, k] / N
        if f[t] > m: m = f[t]
    tot = 0.0
    for t in range(n):
        f[t] = counts[j, s, pres[j, s, t]] * np.exp(w * (f[t] - m)); tot += f[t]
    return pres[j, s, _draw(f, tot)]


@njit(cache=True)
def _victim(counts, pres, npres, i, s, N):
    u = np.random.randint(N)
    acc = 0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        acc += counts[i, s, k]
        if u < acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def _add(counts, pay, U, pres, npres, ppos, poly, polypos, npoly, i, s, k, delta, S):
    """counts[i, s, k] += delta (delta = +1 or -1), with present lists, polymorphic list and payoff sums."""
    T = pres.shape[0] * S
    before = counts[i, s, k]
    counts[i, s, k] += delta
    so = s if S == 1 else 1 - s
    K = U.shape[0]
    for x in range(K):
        pay[i, so, x] += delta * U[x, k]
    if before == 0 and delta > 0:
        ppos[i, s, k] = npres[i, s]; pres[i, s, npres[i, s]] = k; npres[i, s] += 1
        if npres[i, s] == 2:
            p = i * S + s
            polypos[p] = npoly[0]; poly[npoly[0]] = p; npoly[0] += 1
    elif counts[i, s, k] == 0:
        t = ppos[i, s, k]; last = pres[i, s, npres[i, s] - 1]
        pres[i, s, t] = last; ppos[i, s, last] = t; npres[i, s] -= 1; ppos[i, s, k] = -1
        if npres[i, s] == 1:
            p = i * S + s
            t2 = polypos[p]; lastp = poly[npoly[0] - 1]
            poly[t2] = lastp; polypos[lastp] = t2; npoly[0] -= 1; polypos[p] = -1


@njit(cache=True)
def _island_dist(counts, pres, npres, JA, cat, ncat, i, S, N):
    """outcome-category distribution of island i (random matching; S = 1 without self-matching)."""
    out = np.zeros(ncat)
    k = JA.shape[2]
    if S == 1:
        z = N * (N - 1.0)
        for ta in range(npres[i, 0]):
            a = pres[i, 0, ta]
            for tb in range(npres[i, 0]):
                b = pres[i, 0, tb]
                wgt = counts[i, 0, a] * (counts[i, 0, b] - (1 if a == b else 0)) / z
                if wgt <= 0: continue
                for x in range(k):
                    for y in range(k):
                        out[cat[x, y]] += wgt * JA[a, b, x, y]
    else:
        z = float(N) * N
        for ta in range(npres[i, 0]):
            a = pres[i, 0, ta]
            for tb in range(npres[i, 1]):
                b = pres[i, 1, tb]
                wgt = counts[i, 0, a] * counts[i, 1, b] / z
                for x in range(k):
                    for y in range(k):
                        out[cat[x, y]] += wgt * JA[a, b, x, y]
    return out


@njit(cache=True)
def _closed(U, present1, present2, S):
    """verified closed: fitnesses equal for ever on this support.  S = 1: every pair of present classes has the same
    payoff (src/islands.py's rule; self-exclusion makes anything weaker insufficient).  S = 2: within each slot,
    every present class earns the same against every present class of the other slot."""
    if S == 1:
        lo = 1e300; hi = -1e300
        for a in present1:
            for b in present1:
                if U[a, b] < lo: lo = U[a, b]
                if U[a, b] > hi: hi = U[a, b]
        return hi - lo < 1e-9
    for b in present2:
        lo = 1e300; hi = -1e300
        for a in present1:
            if U[a, b] < lo: lo = U[a, b]
            if U[a, b] > hi: hi = U[a, b]
        if hi - lo > 1e-9: return False
    for a in present1:
        lo = 1e300; hi = -1e300
        for b in present2:
            if U[b, a] < lo: lo = U[b, a]
            if U[b, a] > hi: hi = U[b, a]
        if hi - lo > 1e-9: return False
    return True


@njit(cache=True)
def _sim(U, JA, cat, ncat, init, S, N, w, m, eps, mu_cdf, checks, seed, thr, stop_closed):
    """Island Moran process (src/islands.py's dynamics) with S slot populations per island and exact event skipping.
    A birth picks an island and a slot uniformly; with probability m the parent comes from a uniformly chosen other
    island (fitness evaluated there), else from the same island and slot; with probability eps the offspring is a fresh
    draw from mu; the victim is uniform on the island-slot.  A birth on a monomorphic island-slot without migration or
    mutation changes nothing, so the number of births to the next possibly-effective one is drawn geometrically.
    checks: generations (I*S*N births each) at which the state is inspected.  Returns per-check records and the
    final counts."""
    np.random.seed(seed)
    I = init.shape[0]; K = U.shape[0]
    T = I * S
    counts = np.zeros((I, S, K), np.int64)
    pay = np.zeros((I, S, K))
    pres = np.zeros((I, S, K), np.int64); npres = np.zeros((I, S), np.int64); ppos = -np.ones((I, S, K), np.int64)
    poly = np.zeros(T, np.int64); polypos = -np.ones(T, np.int64); npoly = np.zeros(1, np.int64)
    for i in range(I):
        for s in range(S):
            for k in range(K):
                for r in range(init[i, s, k]):
                    _add(counts, pay, U, pres, npres, ppos, poly, polypos, npoly, i, s, k, 1, S)
    nchk = checks.shape[0]
    gen_births = float(T) * N
    lab = -np.ones((nchk, I), np.int64)          # dominant category per island (>= thr), -1 mixed
    lclosed = np.zeros((nchk, I), np.bool_)      # island locally closed
    gclosed_at = -1.0
    acc_cat = np.zeros(ncat)                     # check-averaged global category distribution (for eps > 0)
    poly_checks = 0
    births = 0.0
    c = 0
    last_c = -1
    while c < nchk:
        A = npoly[0]
        p_poly = A / T
        p_eff = p_poly + (1.0 - p_poly) * (1.0 - (1.0 - m) * (1.0 - eps))
        if p_eff <= 0.0:
            skip = 1e300
        elif p_eff >= 1.0:
            skip = 1.0
        else:
            uu = np.random.random()
            skip = np.floor(np.log(1.0 - uu) / np.log(1.0 - p_eff)) + 1.0
        nb = births + skip
        # inspections at checkpoints passed before this event (state unchanged since the last event)
        while c < nchk and checks[c] * gen_births <= nb:
            # global support per slot
            g1 = np.zeros(K, np.bool_); g2 = np.zeros(K, np.bool_)
            for i in range(I):
                for t in range(npres[i, 0]): g1[pres[i, 0, pres.shape[2] * 0 + t]] = True
                if S == 2:
                    for t in range(npres[i, 1]): g2[pres[i, 1, t]] = True
                dist = _island_dist(counts, pres, npres, JA, cat, ncat, i, S, N)
                best = 0
                for q in range(ncat):
                    if dist[q] > dist[best]: best = q
                lab[c, i] = best if dist[best] >= thr else -1
                if eps > 0:
                    for q in range(ncat): acc_cat[q] += dist[q] / I
                p1 = pres[i, 0, :npres[i, 0]]
                p2 = pres[i, S - 1, :npres[i, S - 1]]
                lclosed[c, i] = _closed(U, p1, p2, S)
                for s in range(S):
                    if npres[i, s] > 1:
                        mx = 0
                        for t in range(npres[i, s]):
                            if counts[i, s, pres[i, s, t]] > mx: mx = counts[i, s, pres[i, s, t]]
                        if mx < 0.9 * N:
                            poly_checks += 1
            s1 = np.nonzero(g1)[0]; s2 = np.nonzero(g2)[0] if S == 2 else s1
            last_c = c
            if eps == 0.0 and _closed(U, s1, s2, S):
                gclosed_at = checks[c]
                if stop_closed:
                    for c2 in range(c + 1, nchk):
                        for i in range(I):
                            lab[c2, i] = lab[c, i]; lclosed[c2, i] = lclosed[c, i]
                    c = nchk
                    break
            c += 1
        if c >= nchk or skip > 1e299:
            if skip > 1e299:
                # nothing can ever change: fill the remaining checks
                for c2 in range(c, nchk):
                    for i in range(I):
                        lab[c2, i] = lab[c - 1, i] if c > 0 else -1
                        lclosed[c2, i] = True
                    last_c = c2
            break
        births = nb
        # which kind of effective birth
        if np.random.random() < p_poly / p_eff:
            p = poly[np.random.randint(A)]
        else:
            while True:
                p = np.random.randint(T)
                if npres[p // S, p % S] == 1: break
        i = p // S; s = p % S
        # birth type given effective: on a polymorphic pair any birth; on a monomorphic pair migration or mutation
        if npres[i, s] > 1:
            mig = np.random.random() < m
            mut = np.random.random() < eps
        else:
            pm = m / (1.0 - (1.0 - m) * (1.0 - eps))
            mig = np.random.random() < pm
            mut = (not mig) or (np.random.random() < eps)
            if not mig:
                mut = True
        if mut:
            k_new = 0
            uu = np.random.random()
            while k_new < K - 1 and mu_cdf[k_new] < uu: k_new += 1
        else:
            j = i
            if mig and I > 1:
                j = np.random.randint(I - 1)
                if j >= i: j += 1
            k_new = _parent(counts, pay, U, pres, npres, j, s, S, N, w)
        kv = _victim(counts, pres, npres, i, s, N)
        if kv != k_new:
            _add(counts, pay, U, pres, npres, ppos, poly, polypos, npoly, i, s, k_new, 1, S)
            _add(counts, pay, U, pres, npres, ppos, poly, polypos, npoly, i, s, kv, -1, S)
    return lab, lclosed, gclosed_at, counts, acc_cat, poly_checks, last_c


def checks_schedule(gens, step=None):
    if step is not None:
        return np.arange(step, gens + 1e-9, step, dtype=np.float64)
    c = list(range(5, min(gens, 2000) + 1, 5)) + list(range(2025, min(gens, 10000) + 1, 25)) + list(range(10100, gens + 1, 100))
    if not c or c[-1] != gens:
        c.append(gens)
    return np.array(c, np.float64)


def categories(d, ordered):
    """category id per (level, level) cell: efficient splits (ordered for fixed roles), ineff, clash."""
    v = d['values']; lab, olab = labels(v)
    L = olab if ordered else lab
    names = sorted({x for x in L.ravel() if x not in ('ineff', 'clash')}, key=lambda s_: eval(s_.replace('|', '-').split('-')[0])) + ['ineff', 'clash']
    k = len(v)
    cat = np.zeros((k, k), np.int64)
    for i in range(k):
        for j in range(k):
            cat[i, j] = names.index(L[i, j])
    return cat, names


def final_island(d, S, counts_i):
    """outcome statistics of one island from its final counts (S, K)."""
    if S == 1:
        cls = np.nonzero(counts_i[0])[0]
        o = pop_outcome(d, cls, counts_i[0][cls])
        hold = [d['names'][int(np.argmax(counts_i[0]))]]
    else:
        c1 = np.nonzero(counts_i[0])[0]; c2 = np.nonzero(counts_i[1])[0]
        x = counts_i[0][c1] / counts_i[0].sum(); y = counts_i[1][c2] / counts_i[1].sum()
        J = np.einsum('a,b,abij->ij', x, y, d['JA'][np.ix_(c1, c2)])
        o = outcome_of(J, d['values'])
        o['slot1'] = float(x @ d['U'][np.ix_(c1, c2)] @ y); o['slot2'] = float(y @ d['U'][np.ix_(c2, c1)] @ x)
        o['exante_max'] = max(o['slot1'], o['slot2'])
        hold = [d['names'][int(np.argmax(counts_i[0]))], d['names'][int(np.argmax(counts_i[1]))]]
    o['holder'] = hold
    o['kinds'] = [d['kinds'][d['names'].index(h)] for h in hold]
    o['npresent'] = [int((counts_i[s] > 0).sum()) for s in range(S)]
    return o


def run_islands(job):
    """one lottery run: job = dict(game, n, arm, I, N, mN, gens, seed, thr, init (optional))."""
    d = data(job['game'], job['n'], job['arm'])
    S = 2 if job['arm'] == 'fixed' else 1
    cat, cnames = categories(d, ordered=(S == 2))
    I, N = job['I'], job['N']
    m = job['mN'] / N
    rng = np.random.default_rng(job['seed'])
    if job.get('init') is not None:
        init = np.asarray(job['init'], np.int64)
    else:
        init = np.zeros((I, S, d['K']), np.int64)
        for i in range(I):
            for s in range(S):
                init[i, s] = rng.multinomial(N, d['mu'])
    checks = checks_schedule(job['gens'], job.get('step'))
    t0 = time.time()
    JA = np.ascontiguousarray(d['JA'])
    lab, lcl, gcl, counts, _, polyc, last_c = _sim(np.ascontiguousarray(d['U']), JA, cat, len(cnames), init, S, N, W, m, 0.0,
                                                    np.cumsum(d['mu']), checks, int(job['seed'] % (2**31 - 1)), job.get('thr', 0.95), True)
    gens_end = float(gcl) if gcl >= 0 else float(checks[-1])
    nchk = len(checks)
    # per-island establishment (first locally closed check), run-level partition-frozen time and escapes after it
    allc = lcl.all(axis=1)
    c_pf = int(np.argmax(allc)) if allc.any() else -1
    t_est = [float(checks[int(np.argmax(lcl[:, i]))]) if lcl[:, i].any() else None for i in range(I)]
    # escapes: an island locally closed on label A at one check and locally closed on label B != A at a later check
    # (transient migrant lineages, which make an island briefly 'mixed' or not closed, are not escapes); losses: an
    # efficient label held by some locally closed island at one check and by none at the next check at which every
    # island is again locally closed.  Both counted after the partition-frozen check.
    esc = 0; losses = 0; exposure = 0.0
    eff_cat = np.array([('-' in x or '|' in x) for x in cnames])
    if c_pf >= 0:
        cend = nchk if gcl < 0 else int(np.searchsorted(checks, gcl)) + 1
        cend = min(cend, nchk)
        last = lab[c_pf].copy()
        prevset = {int(x) for x in lab[c_pf] if x >= 0 and eff_cat[x]}
        for c in range(c_pf + 1, cend):
            ok = lcl[c] & (lab[c] >= 0)
            ch_ = ok & (lab[c] != last)
            esc += int(ch_.sum())
            last = np.where(ok, lab[c], last)
            if lcl[c].all():
                cur = {int(x) for x in lab[c] if x >= 0 and eff_cat[x]}
                losses += len(prevset - cur)
                prevset = cur
        exposure = (min(gens_end, float(checks[-1])) - float(checks[c_pf]))
    isl = [final_island(d, S, counts[i]) for i in range(I)]
    finlab = [cnames[x] if x >= 0 else 'mixed' for x in lab[min(last_c, nchk - 1)]]
    rec = dict(seed=job['seed'], closed_at=float(gcl), censored=bool(gcl < 0 and job['mN'] > 0), t_pf=float(checks[c_pf]) if c_pf >= 0 else None,
               escapes=esc, losses=losses, exposure_gens=exposure, t_est=t_est, labels=finlab,
               locally_closed=[bool(x) for x in lcl[min(last_c, nchk - 1)]],
               holders=[o['holder'] for o in isl], holder_kinds=[o['kinds'] for o in isl],
               eff=[o['eff'] for o in isl], dwl=[o['dwl'] for o in isl], E_max_pay=[o['E_max_pay'] for o in isl],
               exante_max=[o['exante_max'] for o in isl], time_s=time.time() - t0, poly_checks=int(polyc))
    if S == 2:
        rec['slot1'] = [o['slot1'] for o in isl]; rec['slot2'] = [o['slot2'] for o in isl]
    if job.get('keep_counts'):
        rec['counts'] = counts.tolist()
    return rec


def cmd_lottery(a):
    from multiprocessing import Pool
    jobs = []
    for arm in a.arms:
        for mN in a.mN:
            for r in range(a.runs):
                jobs.append(dict(game=a.game, n=a.n, arm=arm, I=a.I, N=a.N, mN=mN, gens=a.gens, seed=(a.salt * 1000003 + ARMS.index(arm) * 100003 + a.I * 1009 + a.N * 7 + int(mN * 1000) * 13 + r) % (2**31 - 1),
                                 keep_counts=a.keep_counts, run=r))
    t0 = time.time()
    with Pool(a.procs) as pool:
        recs = pool.map(run_islands, jobs, chunksize=1)
    out = defaultdict(list)
    for j, r in zip(jobs, recs):
        r['run'] = j['run']
        out['%s|%g' % (j['arm'], j['mN'])].append(r)
    fn = os.path.join(OUT, 'lottery_%s_n%d_I%d_N%d_%s.json' % (a.game, a.n, a.I, a.N, a.tag))
    old = json.load(open(fn)) if os.path.exists(fn) else {}
    old.update(out)
    json.dump(old, open(fn, 'w'), default=str)
    print('wrote %s (%.0fs)' % (fn, time.time() - t0))
    for k, rs in out.items():
        labs = Counter(l for r in rs for l in r['labels'])
        tot = sum(labs.values())
        print(k, ', '.join('%s %.3f' % (l, c / tot) for l, c in labs.most_common()), '| censored %d/%d' % (sum(r['censored'] for r in rs), len(rs)),
              '| mean time %.1fs' % np.mean([r['time_s'] for r in rs]), flush=True)


def run_joint(job):
    """joint two-slot Moran simulation at finite eps (validation of the fixed-role reduction)."""
    d = data(job['game'], job['n'], 'fixed')
    cat, cnames = categories(d, ordered=True)
    N = job['N']
    init = np.zeros((1, 2, d['K']), np.int64)
    ci = const_index(d)
    init[0, 0, ci['S3' if 'S3' in ci else d['game'].actions[len(d['game'].actions) // 2]]] = N
    init[0, 1, ci['S3' if 'S3' in ci else d['game'].actions[len(d['game'].actions) // 2]]] = N
    checks = checks_schedule(job['gens'], job['step'])
    t0 = time.time()
    lab, lcl, gcl, counts, acc, polyc, last_c = _sim(np.ascontiguousarray(d['U']), np.ascontiguousarray(d['JA']), cat, len(cnames), init, 2, N, W,
                                                     0.0, job['eps'], np.cumsum(d['mu']), checks, int(job['seed']), 0.99, False)
    nchk = len(checks)
    # occupancy by dominant ordered label (state view) and by encounter (acc)
    labs = Counter(lab[:, 0].tolist())
    return dict(seed=job['seed'], enc={cnames[q]: float(acc[q] / nchk) for q in range(len(cnames))},
                state={(cnames[q] if q >= 0 else 'mixed'): c / nchk for q, c in labs.items()},
                poly_frac=polyc / (2.0 * nchk), time_s=time.time() - t0)


def cmd_validate(a):
    from multiprocessing import Pool
    jobs = [dict(game=a.game, n=a.n, N=a.N, eps=a.eps, gens=a.gens, step=a.step, seed=a.salt + r) for r in range(a.seeds)]
    with Pool(a.procs) as pool:
        recs = pool.map(run_joint, jobs, chunksize=1)
    d = data(a.game, a.n, 'fixed')
    r = fixed_summary(d, fixed_chain(d, a.N))
    cat, cnames = categories(d, ordered=True)
    chain_enc = {c: r['outcome'].get('o:' + c, r['outcome'].get(c, 0.0)) for c in cnames}
    sim = {c: [x['enc'].get(c, 0.0) for x in recs] for c in cnames}
    out = dict(game=a.game, n=a.n, N=a.N, eps=a.eps, gens=a.gens, seeds=a.seeds, chain=chain_enc,
               sim_mean={c: float(np.mean(v)) for c, v in sim.items()}, sim_se={c: float(np.std(v, ddof=1) / math.sqrt(len(v))) for c, v in sim.items()},
               tv=float(0.5 * sum(abs(np.mean(sim[c]) - chain_enc[c]) for c in cnames)),
               poly_frac=[x['poly_frac'] for x in recs], state_view=[x['state'] for x in recs], time_s=[x['time_s'] for x in recs],
               chain_state_mass=r['ordered_label_mass'])
    json.dump(out, open(os.path.join(OUT, 'validate_%s_N%d_eps%g.json' % (a.game, a.N, a.eps)), 'w'), indent=1, default=str)
    for c in cnames:
        print('%-8s chain %.4f  sim %.4f +- %.4f' % (c, chain_enc[c], out['sim_mean'][c], out['sim_se'][c]))
    print('TV %.4f; polymorphic slot-checks (minority >= 10%%) %.4f; time %.0fs' % (out['tv'], np.mean(out['poly_frac']), np.mean(out['time_s'])))


def merge_one(job):
    """one merge: a single well-mixed population of size N seeded with job['init'] (K,), run to closure."""
    d = data(job['game'], job['n'], job['arm'])
    cat, cnames = categories(d, ordered=False)
    init = np.asarray(job['init'], np.int64).reshape(1, 1, -1)
    checks = checks_schedule(job.get('gens', 20000), 1.0)
    lab, lcl, gcl, counts, acc, polyc, last_c = _sim(np.ascontiguousarray(d['U']), np.ascontiguousarray(d['JA']), cat, len(cnames), init, 1, int(init.sum()), W,
                                                     0.0, 0.0, np.cumsum(d['mu']), checks, int(job['seed']), 0.99, True)
    o = final_island(d, 1, counts[0])
    return dict(label=label_of(o), holder=o['holder'][0], closed_at=float(gcl), share=job['share'], N=int(init.sum()), kind=job['kind'])


def cmd_merge(a):
    from multiprocessing import Pool
    d = data(a.game, a.n, 'role')
    ci = d['names'].index('S3'); cr = d['names'].index('ROLE')
    rng = np.random.default_rng(a.salt)
    jobs = []
    ends = None
    if a.ends:
        L = json.load(open(a.ends))
        fair = []; role = []
        for key, rs in L.items():
            if not key.startswith('role|0'): continue
            for r in rs:
                for i, lab in enumerate(r['labels']):
                    c = np.asarray(r['counts'][i][0])
                    if lab == '1/2-1/2': fair.append(c)
                    elif lab == '1/6-5/6': role.append(c)
        ends = (fair, role)
        print('end states: %d fair, %d 1/6-5/6' % (len(fair), len(role)))
    for N in a.N:
        for sh in a.shares:
            for r in range(a.reps):
                n3 = int(round(sh * N))
                init = np.zeros(d['K'], np.int64); init[ci] = n3; init[cr] = N - n3
                jobs.append(dict(game=a.game, n=a.n, arm='role', init=init, share=sh, kind='pure', seed=a.salt + len(jobs)))
                if ends is not None and ends[0] and ends[1]:
                    f = ends[0][rng.integers(len(ends[0]))]; g = ends[1][rng.integers(len(ends[1]))]
                    init = rng.multinomial(n3, f / f.sum()) + rng.multinomial(N - n3, g / g.sum())
                    jobs.append(dict(game=a.game, n=a.n, arm='role', init=init, share=sh, kind='sampled', seed=a.salt + len(jobs)))
    with Pool(a.procs) as pool:
        recs = pool.map(merge_one, jobs, chunksize=4)
    json.dump(recs, open(os.path.join(OUT, 'merge_%s.json' % a.game), 'w'), indent=1, default=str)
    tab = defaultdict(lambda: [0, 0])
    for r in recs:
        k = (r['kind'], r['N'], r['share'])
        tab[k][0] += r['label'] == '1/2-1/2'; tab[k][1] += 1
    for k in sorted(tab):
        print(k, '%d/%d fair wins' % tuple(tab[k]))


# ------------------------------------------------------------------ summaries of lottery cells (run-level intervals)
def tci(xs):
    """mean and 95% t-interval of run-level values."""
    xs = np.asarray([x for x in xs if x is not None], float)
    if len(xs) == 0: return (float('nan'),) * 3
    m = float(xs.mean())
    if len(xs) < 2: return m, m, m
    from scipy.stats import t as tdist
    h = float(tdist.ppf(0.975, len(xs) - 1) * xs.std(ddof=1) / math.sqrt(len(xs)))
    return m, m - h, m + h


def wilson(k, n):
    if n == 0: return (float('nan'),) * 3
    z = 1.96; p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return p, max(0.0, c - h), min(1.0, c + h)


def cell_summary(rs, fixed):
    labs = sorted({l for r in rs for l in r['labels']})
    out = dict(runs=len(rs))
    out['label_share'] = {l: tci([np.mean([x == l for x in r['labels']]) for r in rs]) for l in labs}
    if fixed:
        # unordered view of the ordered labels
        def un(l):
            if '|' not in l: return l
            a_, b_ = l.split('|'); lo = min(eval(a_), eval(b_))
            return '%s-%s' % (D.frac(lo), D.frac(1 - lo))
        ul = sorted({un(l) for l in labs})
        out['unordered_share'] = {l: tci([np.mean([un(x) == l for x in r['labels']]) for r in rs]) for l in ul}
        out['slot_diff'] = tci([np.mean(np.array(r['slot1']) - np.array(r['slot2'])) for r in rs])
        out['slot1_more'] = tci([np.mean(np.array(r['slot1']) > np.array(r['slot2']) + 1e-9) for r in rs])
        out['slot2_more'] = tci([np.mean(np.array(r['slot2']) > np.array(r['slot1']) + 1e-9) for r in rs])
        out['mean_slot_payoff'] = tci([np.mean((np.array(r['slot1']) + np.array(r['slot2'])) / 2) for r in rs])
    out['eff_islands'] = tci([np.mean(np.array(r['eff']) > 0.99) for r in rs])
    out['eff_encounters'] = tci([np.mean(r['eff']) for r in rs])
    out['dwl'] = tci([np.mean(r['dwl']) for r in rs])
    out['E_max_pay'] = tci([np.mean(r['E_max_pay']) for r in rs])
    out['exante_max'] = tci([np.mean(r['exante_max']) for r in rs])
    eff_labels = lambda r: {l for l in r['labels'] if ('-' in l or '|' in l)}
    out['n_conventions'] = tci([len(eff_labels(r)) for r in rs])
    k = sum(len(eff_labels(r)) >= 2 for r in rs)
    out['patchwork'] = wilson(k, len(rs))
    out['censored'] = wilson(sum(r['censored'] for r in rs), len(rs))
    out['closed'] = wilson(sum(r['closed_at'] >= 0 for r in rs), len(rs))
    tpf = [r['t_pf'] for r in rs if r['t_pf'] is not None]
    out['t_pf_median'] = float(np.median(tpf)) if tpf else None
    out['partition_frozen_runs'] = len(tpf)
    esc = sum(r['escapes'] for r in rs); expo = sum(r['exposure_gens'] for r in rs) * len(rs[0]['labels'])
    out['escape_rate_per_island_gen'] = esc / expo if expo > 0 else None
    out['escapes'] = esc
    los = sum(r['losses'] for r in rs); ex2 = sum(r['exposure_gens'] for r in rs)
    out['loss_hazard_per_gen'] = los / ex2 if ex2 > 0 else None
    out['losses'] = los
    te = [t for r in rs for t in r['t_est'] if t is not None]
    out['T_est_median'] = float(np.median(te)) if te else None
    out['not_established_islands'] = sum(t is None for r in rs for t in r['t_est'])
    hk = Counter(tuple(h) for r in rs for h in r['holder_kinds'])
    tot = sum(hk.values())
    out['holder_kinds'] = {'|'.join(k_): v / tot for k_, v in hk.most_common(6)}
    hh = Counter(' | '.join(h) for r in rs for h in r['holders'])
    out['holders'] = {k_: v / tot for k_, v in hh.most_common(8)}
    return out


def _f(x, p=3):
    if x is None or (isinstance(x, float) and x != x): return '-'
    return ('%.' + str(p) + 'f') % x


def _ci(t, p=3):
    return '%s [%s, %s]' % (_f(t[0], p), _f(t[1], p), _f(t[2], p))


def report_chains(game, lines, J):
    uns_all = None
    for arm in ARMS:
        rows = []
        for N in (100, 1000, 3000, 10000):
            fn = os.path.join(OUT, 'chain_%s_n%d_%s_N%d.json' % (game, NDEF, arm, N))
            if os.path.exists(fn):
                rows.append(json.load(open(fn)))
        if not rows: continue
        J.setdefault('chains', {})['%s_%s' % (game, arm)] = rows
        d = data(game, NDEF, arm)
        uns, ords = split_names(d['values'])
        lines += ['### %s, %s (%s)' % (game, arm, 'N per slot' if arm == 'fixed' else 'one population of N'), '',
                  'Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).', '',
                  '| N | ' + ' | '.join(ords) + ' | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \\| compatible] | dwl | cut |',
                  '|' + '---|' * (len(ords) + 9)]
        for r in rows:
            o = r['outcome']
            lines.append('| %d | ' % r['N'] + ' | '.join(_f(o.get('o:' + s, 0.0), 4) for s in ords) + ' | %s | %s | %s | %s | %s | %s | %s | %.1e |' % (
                _f(o['ineff'], 4), _f(o['clash'], 4), _f(o['eff'], 4), _f(o['E_max_pay']), _f(o['exante_max']), _f(o['E_max_share_compat']), _f(o['dwl'], 4),
                r.get('cut', r.get('cut_flow', 0.0))))
        lines += ['', 'Support (top states, π, label):', '']
        for r in rows:
            lines.append('- N = %d: ' % r['N'] + '; '.join('`%s` %.4f (%s)' % (s['state'], s['pi'], s['label']) for s in r['support'][:6]))
            if arm != 'fixed':
                lines[-1] += ' — polymorphic mass %.4f, monomorphic-constant mass %.4f, states %d, indeterminate %d' % (
                    r['mass_polymorphic'], r['mass_mono_constant'], r['n_states'], r['indeterminate'])
            else:
                lines[-1] += ' — constant pairs %.4f; slot 1 gets more %.4f, slot 2 %.4f, equal %.4f' % (
                    r['mass_constant_pairs'], r['slot_more'].get('slot1', 0), r['slot_more'].get('slot2', 0), r['slot_more'].get('equal', 0))
        lines += ['', 'Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; '
                  '"via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):', '']
        for r in rows:
            lines.append('- N = %d: ' % r['N'] + '; '.join('%s → %s %.3g (via %.2f)' % (t['src'], t['dst'], t['rate_per_unit_mass'], t['share_from_nonconstant_states'])
                                                         for t in r['transitions'][:8]))
        if arm == 'fixed':
            lines += ['', 'Convention-to-convention moves (exact, from the generator): from each efficient constant pair, the next different '
                      'efficient constant pair hit, the expected time to it, and the exact exit time from its label (mutation events).', '',
                      '| N | from | next convention hit | time to next | exit time from label | first label after exit |', '|---|---|---|---|---|---|']
            for r in rows:
                for nm, h in r.get('hitting', {}).items():
                    lines.append('| %d | %s | %s | %.3g | %.3g | %s |' % (r['N'], nm, ', '.join('%s %.2f' % kv for kv in sorted(h['next_convention'].items(), key=lambda kv: -kv[1])),
                                                                     h['time_to_next'], h['exit_time'], ', '.join('%s %.2f' % kv for kv in sorted(h['exit_to'].items(), key=lambda kv: -kv[1])[:4])))
        else:
            lines += ['', 'Top exits of the heaviest states (probability per mutation event; mutants):', '']
            for r in rows:
                for e in r['top_exits'][:3]:
                    lines.append('- N = %d, from `%s`: ' % (r['N'], e['state']) + '; '.join('`%s` (%s) %.2g by %s' % (x['to'], x['label'], x['p'], ', '.join('`%s`' % m for m, _ in x['mutants'][:2])) for x in e['exits'][:4]))
        lines.append('')


def report_lotteries(game, lines, J):
    import glob
    files = sorted(glob.glob(os.path.join(OUT, 'lottery_%s_n%d_I*_N*_main.json' % (game, NDEF))))
    for fn in files:
        L = json.load(open(fn))
        m_ = re.search(r'_I(\d+)_N(\d+)_', fn); I, N = int(m_.group(1)), int(m_.group(2))
        lines += ['### Lottery %s at (N, I) = (%d, %d)' % (game, N, I), '']
        lines += ['Island partition labels at the horizon (share of islands; mean over runs with run-level 95% t-intervals); fixed roles: '
                  'ordered slot 1 | slot 2, with the unordered view.', '']
        for key in sorted(L, key=lambda k: (ARMS.index(k.split('|')[0]), float(k.split('|')[1]))):
            arm, mN = key.split('|')
            rs = L[key]
            cs = cell_summary(rs, arm == 'fixed')
            J.setdefault('lotteries', {})['%s_I%d_N%d_%s_mN%s' % (game, I, N, arm, mN)] = cs
            lines.append('**%s, mN = %s** (%d runs): ' % (arm, mN, cs['runs']) + '; '.join('%s %s' % (l, _ci(t)) for l, t in sorted(cs['label_share'].items(), key=lambda kv: -kv[1][0])))
            if arm == 'fixed':
                lines.append('  unordered: ' + '; '.join('%s %s' % (l, _ci(t)) for l, t in sorted(cs['unordered_share'].items(), key=lambda kv: -kv[1][0]))
                             + '. Slot 1 gets more on %s of islands, slot 2 on %s; mean slot-1 minus slot-2 payoff %s; mean slot payoff %s.' % (
                                 _ci(cs['slot1_more']), _ci(cs['slot2_more']), _ci(cs['slot_diff']), _ci(cs['mean_slot_payoff'])))
            lines.append('  Efficient islands %s; encounter efficiency %s; dwl %s; E[max share] %s; ex ante max %s; conventions per run %s; '
                         'runs with ≥ 2 conventions %s; closed %s; censored %s; partition-frozen in %d runs (median generation %s); '
                         'escapes after it %d (%s per island-generation); label losses %d (%s per generation); island establishment median %s generations '
                         '(%d islands never locally closed); holders %s.' % (
                             _ci(cs['eff_islands']), _ci(cs['eff_encounters']), _ci(cs['dwl']), _ci(cs['E_max_pay']), _ci(cs['exante_max']), _ci(cs['n_conventions'], 2),
                             _ci(cs['patchwork']), _ci(cs['closed']), _ci(cs['censored']), cs['partition_frozen_runs'], _f(cs['t_pf_median'], 0), cs['escapes'],
                             '%.2g' % cs['escape_rate_per_island_gen'] if cs['escape_rate_per_island_gen'] is not None else '-', cs['losses'],
                             '%.2g' % cs['loss_hazard_per_gen'] if cs['loss_hazard_per_gen'] is not None else '-', _f(cs['T_est_median'], 0),
                             cs['not_established_islands'], ', '.join('`%s` %.2f' % kv for kv in list(cs['holders'].items())[:5])))
            lines.append('')


def merge_exact(N, k, w=W):
    """exact probability that k copies of S3 among N - k copies of ROLE fix (one population, Moran, exp fitness, no
    self-matching): mismatch payoffs u(S3,S3) = u(ROLE,ROLE) = 1/2, u(S3,ROLE) = 1/4, u(ROLE,S3) = 1/12."""
    logs = [0.0]
    acc = 0.0
    for i in range(1, N):
        fs = ((i - 1) * 0.5 + (N - i) * 0.25) / (N - 1)
        fr = (i * (1 / 12) + (N - i - 1) * 0.5) / (N - 1)
        acc += w * (fr - fs)
        logs.append(acc)
    logs = np.array(logs); m = logs.max()
    e = np.exp(logs - m)
    return float(e[:k].sum() / e.sum())


def report_merges(lines, J):
    fn = os.path.join(OUT, 'merge_dollar5.json')
    if not os.path.exists(fn): return
    recs = json.load(open(fn))
    tab = defaultdict(lambda: [0, 0, []])
    for r in recs:
        k = (r['kind'], r['N'], r['share'])
        tab[k][0] += r['label'] == '1/2-1/2'; tab[k][1] += 1; tab[k][2].append(r['label'])
    shares = sorted({k[2] for k in tab})
    lines += ['### Merges (`role` arm, one population, 50–50 share s; fraction ending on 1/2–1/2, Wilson 95%)', '',
              '| kind | N | ' + ' | '.join('s = %g' % s for s in shares) + ' |', '|---|---|' + '---|' * len(shares)]
    J['merges'] = {}
    for kind in ('pure', 'sampled'):
        for N in sorted({k[1] for k in tab}):
            if (kind, N, shares[0]) not in tab: continue
            cells = []
            for s in shares:
                k_, n_, labs = tab[(kind, N, s)]
                w_ = wilson(k_, n_); cells.append('%.2f [%.2f, %.2f]' % w_)
                J['merges']['%s_N%d_s%g' % (kind, N, s)] = dict(fair=k_, n=n_, other=Counter(labs).most_common())
            lines.append('| %s | %d | ' % (kind, N) + ' | '.join(cells) + ' |')
    for N in sorted({k[1] for k in tab}):
        ex = [merge_exact(N, int(round(s * N))) for s in shares]
        J['merges']['exact_N%d' % N] = ex
        lines.append('| exact (pure) | %d | ' % N + ' | '.join('%.2f' % x for x in ex) + ' |')
    lines.append('')


def cmd_report(a):
    J = {}
    lines = ['# Divide-the-dollar partitions across islands, with `ROLE`, without `ROLE`, and with fixed roles', '',
             'Spec `specs/2026-10-05-dollar-partitions.md`; predictions `predictions/2026-10-05-dollar-partitions.md`; code `src/dollar_partitions.py`. '
             'Weak arm, n = 5 in every arm, w = 0.3. Static tables: `runs/dollar_partitions/static_dollar5.md`, `static_dollar3.md`. '
             'Per-cell JSON under `runs/dollar_partitions/`.', '']
    for game in ('dollar5', 'dollar3'):
        lines += ['## ε → 0 chains: %s' % game, '']
        report_chains(game, lines, J)
    vfn = os.path.join(OUT, 'validate_dollar5_N50_eps0.001.json')
    if os.path.exists(vfn):
        V = json.load(open(vfn)); J['validate'] = V
        lines += ['## Validation of the fixed-role reduction (joint two-slot simulation, N = 50 per slot, ε = 10⁻³ per birth, %d seeds × %d generations)' % (V['seeds'], V['gens']), '',
                  '| category | chain | simulation (± s.e. over seeds) |', '|---|---|---|']
        for c in V['chain']:
            lines.append('| %s | %.4f | %.4f ± %.4f |' % (c, V['chain'][c], V['sim_mean'][c], V['sim_se'][c]))
        lines += ['', 'Total variation %.4f; slot-checks with the largest class below 0.9: %.4f (mean over seeds).' % (V['tv'], float(np.mean(V['poly_frac']))), '']
    for game in ('dollar5', 'dollar3'):
        lines += ['## ε = 0 lotteries: %s' % game, '']
        report_lotteries(game, lines, J)
    lines += ['## Merges', '']
    report_merges(lines, J)
    open(os.path.join(ROOT, 'runs', 'dollar-partitions.md'), 'w').write('\n'.join(lines) + '\n')
    json.dump(J, open(os.path.join(ROOT, 'runs', 'dollar-partitions.json'), 'w'), indent=1, default=str)
    print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static'); s.add_argument('--games', nargs='+', default=['dollar5']); s.add_argument('--n', type=int, default=NDEF); s.add_argument('--arms', nargs='+', default=None)
    c = sub.add_parser('chain'); c.add_argument('--game', default='dollar5'); c.add_argument('--n', type=int, default=NDEF)
    c.add_argument('--arm', default='fixed'); c.add_argument('--N', type=int, nargs='+', default=[100])
    l = sub.add_parser('lottery'); l.add_argument('--game', default='dollar5'); l.add_argument('--n', type=int, default=NDEF)
    l.add_argument('--arms', nargs='+', default=list(ARMS)); l.add_argument('--I', type=int, default=64); l.add_argument('--N', type=int, default=100)
    l.add_argument('--mN', type=float, nargs='+', default=[0.1]); l.add_argument('--runs', type=int, default=40); l.add_argument('--gens', type=int, default=100000)
    l.add_argument('--procs', type=int, default=3); l.add_argument('--salt', type=int, default=20261005); l.add_argument('--tag', default='main')
    l.add_argument('--keep_counts', action='store_true')
    v = sub.add_parser('validate'); v.add_argument('--game', default='dollar5'); v.add_argument('--n', type=int, default=NDEF)
    v.add_argument('--N', type=int, default=50); v.add_argument('--eps', type=float, default=1e-3); v.add_argument('--gens', type=int, default=2000000)
    v.add_argument('--step', type=float, default=10.0); v.add_argument('--seeds', type=int, default=10); v.add_argument('--procs', type=int, default=3)
    v.add_argument('--salt', type=int, default=777000)
    mg = sub.add_parser('merge'); mg.add_argument('--game', default='dollar5'); mg.add_argument('--n', type=int, default=NDEF)
    mg.add_argument('--N', type=int, nargs='+', default=[100, 400]); mg.add_argument('--shares', type=float, nargs='+', default=[0.25, 0.3, 0.35, 0.375, 0.4, 0.45, 0.5])
    mg.add_argument('--reps', type=int, default=100); mg.add_argument('--ends', default=None); mg.add_argument('--procs', type=int, default=3)
    mg.add_argument('--salt', type=int, default=4242)
    rp = sub.add_parser('report')
    a = ap.parse_args()
    if a.cmd == 'report':
        cmd_report(a)
    elif a.cmd == 'validate':
        cmd_validate(a)
    elif a.cmd == 'merge':
        cmd_merge(a)
    elif a.cmd == 'static':
        cmd_static(a)
    elif a.cmd == 'chain':
        cmd_chain(a)
    elif a.cmd == 'lottery':
        cmd_lottery(a)
