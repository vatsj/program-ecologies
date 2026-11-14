"""Step 0 of queue 78 (spec specs/2026-11-14-patient-accepters.md): exact invasion assays for the patient accepter R.

    python3 src/patient_accepter_step0.py OUT.json [OUT.md]

Every edge is the exact fixation probability of one invader copy in one slot of a named resident triple (the other two slots monomorphic),
N = 200, w = 0.3, A_f charges included (P_fail = 0.1): with the other slots monomorphic the invader's and the resident's payoffs in the
invaded slot are constant, so the island chain is a birth-death chain and rho = (1 - 1/r) / (1 - 1/r^N), r = exp(w * (pi_x - pi_res))
(queue 76's bully_resist_step0.rho_exact; the 10^4-trial jump chain and the full kernel are checks).  rho * N = 1 is neutral.  Per-mutant
fixation is reported separately from prior-weighted establishment rates per arrival into that slot (fixation x the invader's arrival mass
under the reference law F+R, delta = 0.03, beta = 3, gamma = 1).

 item 1  R into the victim's slot of every bully-held unequal island (a bully on 2/3 with a 1/3 constant, any third-slot program; both
         bullies, all three role rotations, both R orientations and both timeout variants), split by R's read class in the invaded triple
         (completes / times out), by orientation (matched: R reads the excluded slot) and by whether the third slot offers the victim 1/2.
 item 2  R resident as the victim (matched orientation; the resident triple is still unequal): every program of the catalogue into the
         excluded slot, with the outcome when it fixes.
 item 3  the offerer resident in the excluded slot (a 1/2 constant naming the victim; also any reader that leaves the island unequal): R into
         the victim's slot.
 item 4  reverse: (a) bullies and 2/3-demanders into every slot of fair islands whose pair holds R; (b) R into every slot of fair firm-reader
         islands (queue 76's FI and FC classes).
"""
import os, sys, json, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import patient_accepter as PA
import migration_window as MW
import majority_tail as MT
from bully_resist_step0 import rho_exact, mc_fixation, summarize, resident_sets, N0

PFAIL = 0.1
CAT = ['F', 'U', 'G', 'W', 'D']


class Ctx:
    def __init__(self):
        tb = PA.TabsPA(cache_dir=os.path.join(ROOT, 'runs', '_cache'))
        self.tb = tb
        self.names = tb.names; self.idx = {n: i for i, n in enumerate(tb.names)}
        self.NET = tb.payoff(PFAIL, PFAIL); self.GROSS = tb.GROSS
        self.OUT = tb.VEC[tb.JT]; self.CLS = MW.CATMAP[self.OUT]
        fam = tb.fam
        self.FR = [i for i in range(tb.K) if fam[i] in ('single', 'two')]
        self.CST = [i for i in range(tb.K) if fam[i] == 'const']
        self.BUL = [i for i in range(tb.K) if fam[i] == 'bully']
        self.R = [i for i in range(tb.K) if fam[i] == 'accepter']
        self.third = [self.idx['C0'], self.idx['C3']]
        self.third_all = self.third + [self.idx['C6']]
        import patient_accepter_dyn as D
        self.ref_law = D.law_arm('FR', 0.03, 3.0, 1.0)

    def share(self, t):
        return MW.X[int(self.OUT[tuple(t)])]

    def pay_in(self, res, s, x, net=True):
        t = list(res); t[s] = x
        return float((self.NET if net else self.GROSS)[t[0], t[1], t[2]][s])

    def group(self, i):
        n, f = self.names[i], self.tb.fam[i]
        if f == 'const':
            return n
        if f == 'prudent':
            return 'Pz' if n[2] == 'z' else 'Po'
        return {'single': 'Fs', 'two': 'Ft', 'single2': 'F2', 'prudent_a': 'Q', 'opener': 'O', 'bully': 'B', 'exploit': 'X', 'junk_f': 'J',
                'junk_r': 'J', 'accepter': 'R'}[f]


def edge(ctx, res, s, x, **extra):
    d = ctx.pay_in(res, s, x) - ctx.pay_in(res, s, res[s])
    dg = ctx.pay_in(res, s, x, False) - ctx.pay_in(res, s, res[s], False)
    t = list(res); t[s] = x
    o = int(ctx.OUT[tuple(t)])
    rho = rho_exact(d)
    row = dict(res=[ctx.names[v] for v in res], s=s, x=ctx.names[x], xg=ctx.group(x), dnet=round(d, 9), dgross=round(dg, 9), rhoN=rho * N0,
               rate=rho * float(ctx.ref_law[x]), mass=float(ctx.ref_law[x]), out_if_fixed=CAT[int(MW.CATMAP[o])], shares_if_fixed=[int(v) for v in MW.X[o]],
               x_nto=int(ctx.tb.NTO[t[0], t[1], t[2], s]))
    row.update(extra)
    return row


def unequal_bully(ctx, victims):
    """bully-held unequal triples (bully on 2/3, a program of `victims` as the 1/3 victim, any third slot): (triple, b, v, e)."""
    out = []
    K = ctx.tb.K
    for b in ctx.BUL:
        for v in victims:
            for x in range(K):
                for sb in range(3):
                    for sv in range(3):
                        if sv == sb:
                            continue
                        se = 3 - sb - sv
                        t = [0, 0, 0]; t[sb] = b; t[sv] = v; t[se] = x
                        o = int(ctx.OUT[tuple(t)]); sh = MW.X[o]
                        if MW.CATMAP[o] == 1 and sh[sb] == 4 and sh[sv] == 2:
                            out.append((tuple(t), sb, sv, se))
    return sorted(set(out))


_RV = {}


def read_status(ctx, r, t, sv):
    """R's own read in triple t with R in slot sv: 'complete' or 'TO' (evaluated in R's frame)."""
    b, c = t[(sv + 1) % 3], t[(sv - 1) % 3]
    key = (r, b, c)
    if key not in _RV:
        import lt_code as L
        cat = ctx.tb.cat
        v, st, nto = L.run_big(PA.read_value, None, cat.terms[r], ctx.names[r][1], cat.terms[b], cat.terms[c])
        _RV[key] = 'TO' if v == 'TO' else ('complete' if isinstance(v, int) and not isinstance(v, bool) else 'other')
    return _RV[key]


def orient(ctx, r, sv, se):
    """matched: R in slot sv reads the excluded slot se (Rn* reads next = sv + 1)."""
    d = ctx.names[r][1]
    reads = (sv + 1) % 3 if d == 'n' else (sv - 1) % 3
    return 'matched' if reads == se else 'mismatched'


def offers(ctx, t, se, sv):
    """does the third-slot program name the victim at 1/2 in triple t?"""
    code = int(ctx.tb.code[t[se], t[(se + 1) % 3], t[(se - 1) % 3]])
    tgt = (se + 1) % 3 if code // 3 == 0 else ((se - 1) % 3 if code // 3 == 1 else -1)
    return code % 3 == 1 and tgt == sv


def run(out, md=None):
    t0 = time.time()
    ctx = Ctx(); nm = ctx.names
    res = {}
    # ---------------------------------------------------------------- item 1
    UB = unequal_bully(ctx, ctx.third_all)
    rows1 = []
    for (t, sb, sv, se) in UB:
        for r in ctx.R:
            rows1.append(edge(ctx, t, sv, r, item=1, R=nm[r], to=nm[r][2], orient=orient(ctx, r, sv, se), offer=offers(ctx, t, se, sv),
                              read=read_status(ctx, r, tuple(t[:sv]) + (r,) + tuple(t[sv + 1:]), sv),
                              third=nm[t[se]], third_g=ctx.group(t[se]), bully=nm[t[sb]], victim=nm[t[sv]], rot=sb))
    res['item1_n_residents'] = len(UB)
    res['item1'] = rows1
    # ---------------------------------------------------------------- item 2: R resident as victim (matched), resident still unequal
    UBR = []
    for (t, sb, sv, se) in UB:
        for r in ctx.R:
            if orient(ctx, r, sv, se) != 'matched':
                continue
            tt = list(t); tt[sv] = r; tt = tuple(tt)
            o = int(ctx.OUT[tt]); sh = MW.X[o]
            if MW.CATMAP[o] == 1 and sh[sb] == 4 and sh[sv] == 2 and (tt, sb, sv, se) not in UBR:
                UBR.append((tt, sb, sv, se))
    rows2 = []
    for (t, sb, sv, se) in UBR:
        for x in range(ctx.tb.K):
            if x == t[se]:
                continue
            rows2.append(edge(ctx, t, se, x, item=2, R=nm[t[sv]], resident_third=nm[t[se]], bully=nm[t[sb]], rot=sb))
    res['item2_n_residents'] = len(UBR)
    res['item2'] = rows2
    # ---------------------------------------------------------------- item 3: offerer resident in e, R into v
    rows3 = []
    for (t, sb, sv, se) in UB:
        if not (offers(ctx, t, se, sv) or ctx.tb.fam[t[se]] in ('single', 'two', 'opener', 'single2', 'prudent')):
            continue
        for r in ctx.R:
            rows3.append(edge(ctx, t, sv, r, item=3, R=nm[r], to=nm[r][2], orient=orient(ctx, r, sv, se), offerer=nm[t[se]], offerer_g=ctx.group(t[se]),
                              offer=offers(ctx, t, se, sv), victim=nm[t[sv]], bully=nm[t[sb]], rot=sb))
    res['item3'] = rows3
    # ---------------------------------------------------------------- item 4a: fair islands whose pair holds R
    pool = ctx.R + ctx.CST + ctx.BUL + ctx.FR
    FR_ = []
    for t in itertools.product(pool, repeat=3):
        if not any(v in ctx.R for v in t):
            continue
        o = int(ctx.OUT[t])
        if MW.CATMAP[o] != 0:
            continue
        sh = MW.X[o]
        if any(sh[s] > 0 and t[s] in ctx.R for s in range(3)) and sum(1 for v in t if v in ctx.FR) <= 1:
            FR_.append(t)
    two3 = [ctx.idx[c] for c in ('C2', 'C5', 'C8')] + ctx.BUL
    rows4 = []
    for t in FR_:
        sh = ctx.share(t)
        for s in range(3):
            for x in two3:
                if x == t[s]:
                    continue
                rows4.append(edge(ctx, t, s, x, item='4a', role=('pair' if sh[s] > 0 else 'out'), slot_is_R=t[s] in ctx.R))
    res['item4a_n_residents'] = len(FR_)
    res['item4a'] = rows4
    # ---------------------------------------------------------------- item 4b: R into fair firm-reader islands
    rs = resident_sets(ctx, ctx.FR)
    rows4b = []
    for k in ('FI', 'FC'):
        for t in rs[k]:
            sh = ctx.share(t)
            for s in range(3):
                for r in ctx.R:
                    rows4b.append(edge(ctx, t, s, r, item='4b', cls=k, role=('pair' if sh[s] > 0 else 'out'), R=nm[r]))
    res['item4b_n_residents'] = {k: len(rs[k]) for k in ('FI', 'FC')}
    res['item4b'] = rows4b
    # ---------------------------------------------------------------- checks: jump chain and the real kernel
    rng = np.random.default_rng(78)
    mc = []
    allr = rows1 + rows2 + rows3
    for j in rng.choice(len(allr), size=60, replace=False):
        r = allr[int(j)]
        p = rho_exact(r['dnet'])
        f, per = mc_fixation(r['dnet'], trials=10000, seed=int(2000 + j))
        mc.append(dict(exact=p, mc=f, z=float((f - p) / max(np.sqrt(p * (1 - p) / 10000), 1e-9))))
    res['mc_check'] = dict(n=len(mc), max_abs_z=float(max(abs(m['z']) for m in mc)))
    res['kernel_check'] = kernel_check(ctx, rows1 + rows2 + rows3)
    res['summary'] = summaries(res)
    res['wall'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'))
    if md:
        open(md, 'w').write('\n'.join(report_md(res)) + '\n')
    return res


def kernel_check(ctx, rows, n_assay=16, islands=3000, N=N0):
    import majority_tail_kern as MK
    J, PAY, VEC, ISMEM, TOT = ctx.tb.charged_tables(PFAIL, MT.T)
    rng = np.random.default_rng(7)
    pool = [r for r in rows if 0.05 < r['rhoN'] < 30 and abs(r['rhoN'] - 1) > 1e-9]
    out = []
    z0 = np.zeros(0, np.int64)
    for j in rng.choice(len(pool), size=min(n_assay, len(pool)), replace=False):
        r = pool[int(j)]
        res_ = [ctx.idx[v] for v in r['res']]; x = ctx.idx[r['x']]; s = r['s']
        init = np.zeros((islands, 3, ctx.tb.K), np.int64)
        for q in range(3):
            init[:, q, res_[q]] = N
        init[:, s, res_[s]] = N - 1; init[:, s, x] = 1
        o = MK.kern_mt(J, PAY, VEC, ISMEM, TOT, init, N, MT.W, 0.0, int(900 + j), 400 * N, 10, np.zeros(0, np.int64), z0, z0, z0,
                       np.zeros(0), z0, 4000, 4000)
        counts = o[2]
        fixed = int((counts[:, s, x] == N).sum())
        p = rho_exact(r['dnet'], N)
        out.append(dict(res=r['res'], s=s, x=r['x'], exact=p, kernel=fixed / islands, z=float((fixed / islands - p) / max(np.sqrt(p * (1 - p) / islands), 1e-9))))
    return dict(n=len(out), max_abs_z=float(max(abs(o['z']) for o in out)) if out else None, rows=out)


def _s(rows):
    s = summarize(rows)
    if rows:
        s['rate_mean'] = float(np.mean([r['rate'] for r in rows]))
        s['rate_median'] = float(np.median([r['rate'] for r in rows]))
    return s


def summaries(res):
    S = {}
    r1 = res['item1']
    for to in 'ny':
        for ori in ('matched', 'mismatched'):
            for rd in ('complete', 'TO', 'other'):
                for off in (False, True):
                    sel = [r for r in r1 if r['to'] == to and r['orient'] == ori and r['read'] == rd and r['offer'] == off]
                    if sel:
                        S['item1|%s|%s|%s|offer=%s' % (to, ori, rd, off)] = dict(_s(sel), third=sorted({r['third_g'] for r in sel}),
                                                                              out_if_fixed=_count(sel, 'out_if_fixed'))
    r2 = res['item2']
    for to in 'ny':
        for g in sorted({r['xg'] for r in r2}):
            sel = [r for r in r2 if r['R'][2] == to and r['xg'] == g]
            if sel:
                S['item2|%s|%s' % (to, g)] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'),
                                                  out_if_fixed_gt3=_count([r for r in sel if r['rhoN'] > 3], 'out_if_fixed'))
    r3 = res['item3']
    for to in 'ny':
        for ori in ('matched', 'mismatched'):
            for g in sorted({r['offerer_g'] for r in r3}):
                sel = [r for r in r3 if r['to'] == to and r['orient'] == ori and r['offerer_g'] == g]
                if sel:
                    S['item3|%s|%s|%s' % (to, ori, g)] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
    for k in ('item4a', 'item4b'):
        rr = res[k]
        keyf = (lambda r: '%s|%s|%s' % (r['xg'], r['role'], 'Rslot' if r['slot_is_R'] else 'other')) if k == 'item4a' else (lambda r: '%s|%s|%s' % (r['cls'], r['role'], r['R'][2]))
        grp = {}
        for r in rr:
            grp.setdefault(keyf(r), []).append(r)
        for kk, sel in sorted(grp.items()):
            S['%s|%s' % (k, kk)] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
    # the spec's first and selected steps on the decisive triple (Bn, C3, C8) and its offerer variant
    return S


def _count(rows, key):
    c = {}
    for r in rows:
        c[r[key]] = c.get(r[key], 0) + 1
    return c


def report_md(res):
    Lx = ['# Queue 78 step 0: exact invasion assays (rho * N, N = 200, w = 0.3, A_f charges; 1 = neutral)', '',
          'item 1 residents: %d bully-held unequal triples; item 2 residents (R as matched victim): %d; item 4a residents: %d; item 4b: %s' % (
              res['item1_n_residents'], res['item2_n_residents'], res['item4a_n_residents'], res['item4b_n_residents']),
          'Monte Carlo check (jump chain, 10^4 trials, 60 assays): max |z| %.2f; kernel check (%d assays, 3,000 islands): max |z| %s' % (
              res['mc_check']['max_abs_z'], res['kernel_check']['n'], ('%.2f' % res['kernel_check']['max_abs_z']) if res['kernel_check']['max_abs_z'] is not None else '-'), '',
          '| group | n | median | min | max | share <= 1 | share > 3 | mean prior-weighted rate | outcome if fixed |', '|---|---|---|---|---|---|---|---|---|']
    for k, s in res['summary'].items():
        if s.get('n', 0) == 0:
            continue
        Lx.append('| %s | %d | %.3g | %.3g | %.3g | %.2f | %.2f | %.3g | %s |' % (k, s['n'], s['median'], s['min'], s['max'], s['share_le_1'], s['share_gt3'],
                                                                         s.get('rate_mean', 0), s.get('out_if_fixed')))
    return Lx


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
