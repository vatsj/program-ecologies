"""Step 0 of queue 79 (spec specs/2026-11-15-certified-offers.md): exact invasion assays for the certified families (C1 tables).

    python3 src/certified_offers_step0.py OUT.json OUT.md

Every edge is the exact fixation probability of one invader copy in one slot of a named resident triple (the other two slots monomorphic),
N = 200, w = 0.3, A_f charges (P_fail = 0.1): rho = (1 - 1/r) / (1 - 1/r^N), r = exp(w (pi_x - pi_res)) (queue 76's rho_exact; the
10^4-trial jump chain and the full kernel are checks).  rho * N = 1 is neutral.  Per-mutant fixation is reported separately from the
prior-weighted rate per arrival into that slot (fixation x the invader's arrival mass under the main law FcOcRc, delta = 0.03, beta = 3,
phi = 1/2, gamma = 1).

 item 1  Rc (and Rcs; queue 78's R as comparator) into the victim's slot of every simulating-bully-held unequal island (Bn / Bp on 2/3 with a
         1/3 constant C0 / C3 / C6, any program in the excluded slot, all rotations); split by orientation and by whether e's certificate
         points at the victim (active) and by e's class.
 item 2  Rc resident as the matched victim (the resident still unequal): every program into e, by class; and with each offerer class
         resident in e (Oc, Fc, the 1/2 constant naming v, Bc, any reader): Rc into v.
 item 3  reverse edges: the bullies, Bc, the 2/3 demanders C2 C5 C8 and the 1/3 constants into every slot of fair carrier islands
         ((Rc, Oc), (Fc, Fc), (Rcs, 1/2 constant), (Fc, Bc); third slot any non-carrier); Bc into fair simulating-reader islands (queue 76's
         FI and FC classes); every carrier into those islands.
 item 4  Bc's own unequal island (Bc on 2/3 with a 1/3 constant, any e): items 1 and 2's entries.
"""
import os, sys, json, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import certified_offers as CO
import migration_window as MW
import majority_tail as MT
from bully_resist_step0 import rho_exact, mc_fixation, summarize, resident_sets, N0

PFAIL = 0.1
CAT = ['F', 'U', 'G', 'W', 'D']


class Ctx:
    def __init__(self):
        import certified_offers_dyn as D
        tb = D.tabs(os.path.join(ROOT, 'runs', '_cache'))
        self.tb = tb
        self.names = tb.names; self.idx = tb.cat.idx
        self.NET = tb.payoff(PFAIL, PFAIL); self.GROSS = tb.GROSS
        self.OUT = tb.VEC[tb.JT]; self.CLS = MW.CATMAP[self.OUT]
        fam = tb.fam
        g = lambda *fs: [i for i in range(tb.K) if fam[i] in fs]
        self.FR = g('single', 'two'); self.CST = g('const'); self.BUL = g('bully'); self.BC = g('c_bully')
        self.RC = g('c_acc'); self.RCS = g('c_accs'); self.R78 = [self.idx['Rnn'], self.idx['Rpn']]
        self.OC = g('c_open'); self.FC = g('c_firm'); self.PC = g('c_prud')
        self.CAR = [i for i in range(tb.K) if tb.cat.meta[i]['cert'] is not None]
        self.third_all = [self.idx['C0'], self.idx['C3'], self.idx['C6']]
        self.ref_law = D.law_arm('FcOcRc', 0.03, 3.0, 0.5, 1.0)

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
                'junk_r': 'J', 'accepter': 'R', 'c_open': 'Oc', 'c_firm': 'Fc', 'c_acc': 'Rc', 'c_accs': 'Rcs', 'c_bully': 'Bc', 'c_prud': 'Pc'}[f]

    def points(self, x, sx, sy):
        c = self.tb.cat.meta[x]['cert']
        if c is None:
            return False
        return (c[0] if (sx + 1) % 3 == sy else c[1]) == 1


def edge(ctx, res, s, x, **extra):
    d = ctx.pay_in(res, s, x) - ctx.pay_in(res, s, res[s])
    dg = ctx.pay_in(res, s, x, False) - ctx.pay_in(res, s, res[s], False)
    t = list(res); t[s] = x
    o = int(ctx.OUT[tuple(t)])
    rho = rho_exact(d)
    sh = MW.X[o]
    row = dict(res=[ctx.names[v] for v in res], s=s, x=ctx.names[x], xg=ctx.group(x), dnet=round(d, 9), dgross=round(dg, 9), rhoN=rho * N0,
               rate=rho * float(ctx.ref_law[x]), mass=float(ctx.ref_law[x]), out_if_fixed=CAT[int(MW.CATMAP[o])], shares_if_fixed=[int(v) for v in sh],
               x_nto=int(ctx.tb.NTO[t[0], t[1], t[2], s]))
    row.update(extra)
    return row


def unequal_held(ctx, bullies, victims):
    """unequal triples with a program of `bullies` on 2/3 and one of `victims` on 1/3, any third slot: (triple, b, v, e)."""
    out = []
    K = ctx.tb.K
    for b in bullies:
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


def orient(ctx, r, sv, se):
    """matched: the accepter in slot sv offers toward the excluded slot se."""
    return 'matched' if ctx.points(r, sv, se) else 'mismatched'


def eclass(ctx, x, se, sv):
    """class of the excluded-slot program relative to the victim's seat: active carrier (points at v), inactive carrier, 1/2 constant
    naming v, other constant, simulating reader, other."""
    f = ctx.tb.fam[x]
    if ctx.tb.cat.meta[x]['cert'] is not None:
        return 'carrier-active' if ctx.points(x, se, sv) else 'carrier-inactive'
    if f == 'const':
        code = int(ctx.tb.code[x, 0, 0])
        if code % 3 == 1 and code // 3 < 2 and ((se + 1) % 3 if code // 3 == 0 else (se - 1) % 3) == sv:
            return 'half-naming-v'
        return 'const-other'
    if f in ('single', 'two', 'opener', 'prudent', 'prudent_a', 'single2', 'accepter', 'exploit', 'bully'):
        return 'sim-reader'
    return 'other'


def items_unequal(ctx, bullies, tag):
    nm = ctx.names
    UB = unequal_held(ctx, bullies, ctx.third_all)
    acc = ctx.RC + ctx.RCS + ctx.R78
    rows1 = []
    for (t, sb, sv, se) in UB:
        for r in acc:
            rows1.append(edge(ctx, t, sv, r, item='%s1' % tag, R=nm[r], Rg=ctx.group(r), orient=orient(ctx, r, sv, se) if r not in ctx.R78 else
                              ('matched' if (nm[r][1] == 'n') == ((sv + 1) % 3 == se) else 'mismatched'),
                              ecls=eclass(ctx, t[se], se, sv), third=nm[t[se]], third_g=ctx.group(t[se]), bully=nm[t[sb]], victim=nm[t[sv]], rot=sb))
    # item 2: Rc (matched) resident as victim, still unequal
    UBR = []
    for (t, sb, sv, se) in UB:
        for r in ctx.RC + ctx.RCS:
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
            rows2.append(edge(ctx, t, se, x, item='%s2' % tag, R=nm[t[sv]], Rg=ctx.group(t[sv]), resident_third=nm[t[se]],
                              ecls=eclass(ctx, x, se, sv), bully=nm[t[sb]], rot=sb))
    # item 2b: offerer resident in e (the island still unequal with the 1/3 constant as victim), Rc into v
    rows2b = []
    for (t, sb, sv, se) in UB:
        if t[se] not in ctx.OC + ctx.FC + ctx.BC + ctx.PC + ctx.FR + [ctx.idx['C1'], ctx.idx['C4']]:
            continue
        for r in acc:
            rows2b.append(edge(ctx, t, sv, r, item='%s2b' % tag, R=nm[r], Rg=ctx.group(r), orient=orient(ctx, r, sv, se) if r not in ctx.R78 else
                               ('matched' if (nm[r][1] == 'n') == ((sv + 1) % 3 == se) else 'mismatched'),
                               offerer=nm[t[se]], offerer_g=ctx.group(t[se]), ecls=eclass(ctx, t[se], se, sv), victim=nm[t[sv]], bully=nm[t[sb]], rot=sb))
    # item 1c: every program into e of the unequal island with the 1/3 constant as victim (no accepter anywhere)
    rows1c = []
    for (t, sb, sv, se) in UB:
        for x in range(ctx.tb.K):
            if x == t[se]:
                continue
            rows1c.append(edge(ctx, t, se, x, item='%s1c' % tag, ecls=eclass(ctx, x, se, sv), at_b=bool(ctx.points(x, se, sb)),
                               bully=nm[t[sb]], victim=nm[t[sv]], resident_third=nm[t[se]], rot=sb))
    return UB, UBR, rows1, rows2, rows2b, rows1c


def run(out, md=None):
    t0 = time.time()
    ctx = Ctx(); nm = ctx.names
    res = {}
    UB, UBR, r1, r2, r2b, r1c = items_unequal(ctx, ctx.BUL, 'i')
    res['item1c'] = r1c
    res['item1_n_residents'] = len(UB); res['item2_n_residents'] = len(UBR)
    res['item1'] = r1; res['item2'] = r2; res['item2b'] = r2b
    UBc, UBRc, r4_1, r4_2, r4_2b, r4_1c = items_unequal(ctx, ctx.BC, 'iv')
    res['item4_1c'] = r4_1c
    res['item4_n_residents'] = [len(UBc), len(UBRc)]
    res['item4_1'] = r4_1; res['item4_2'] = r4_2; res['item4_2b'] = r4_2b
    # ---------------------------------------------------------------- item 3: fair carrier islands
    noncar = [i for i in range(ctx.tb.K) if ctx.tb.cat.meta[i]['cert'] is None]
    half = [ctx.idx['C1'], ctx.idx['C4']]
    pairs = (('Rc,Oc', ctx.RC, ctx.OC), ('Fc,Fc', ctx.FC, ctx.FC), ('Rcs,half', ctx.RCS, half), ('Fc,Bc', ctx.FC, ctx.BC))
    ent = ctx.BUL + ctx.BC + [ctx.idx[c] for c in ('C2', 'C5', 'C8', 'C0', 'C3', 'C6')]
    rows3 = []
    nres = {}
    for lab, A, B in pairs:
        cnt = 0
        for a in A:
            for b in B:
                for sa in range(3):
                    for sb_ in range(3):
                        if sa == sb_:
                            continue
                        sz = 3 - sa - sb_
                        for z in noncar:
                            t = [0, 0, 0]; t[sa] = a; t[sb_] = b; t[sz] = z; t = tuple(t)
                            if ctx.CLS[t] != 0:
                                continue
                            sh = ctx.share(t)
                            if not (sh[sa] > 0 and sh[sb_] > 0):
                                continue
                            cnt += 1
                            for s in range(3):
                                for x in ent:
                                    if x == t[s]:
                                        continue
                                    rows3.append(edge(ctx, t, s, x, item='3', island=lab, role=('pair' if sh[s] > 0 else 'out')))
        nres[lab] = cnt
    res['item3_n_residents'] = nres
    # Bc and carriers into fair simulating-reader islands (queue 76's FI and FC classes over the firm readers)
    class _C:
        pass
    c2 = _C(); c2.CLS = ctx.CLS; c2.OUT = ctx.OUT; c2.CST = ctx.CST; c2.BUL = ctx.BUL; c2.third_all = ctx.third_all; c2.share = ctx.share
    rs = resident_sets(c2, ctx.FR)
    rows3b = []
    for k in ('FI', 'FC'):
        for t in rs[k]:
            sh = ctx.share(t)
            for s in range(3):
                for x in ctx.CAR:
                    rows3b.append(edge(ctx, t, s, x, item='3b', cls=k, role=('pair' if sh[s] > 0 else 'out')))
    res['item3b_n_residents'] = {k: len(rs[k]) for k in ('FI', 'FC')}
    res['item3'] = rows3; res['item3b'] = rows3b
    # ---------------------------------------------------------------- checks
    rng = np.random.default_rng(79)
    allr = r1 + r2 + r2b + r4_2
    nonneutral = [r for r in allr if abs(r['rhoN'] - 1) > 1e-6]
    mc = []
    for j in rng.choice(len(nonneutral), size=min(60, len(nonneutral)), replace=False):
        r = nonneutral[int(j)]
        p = rho_exact(r['dnet'])
        f, per = mc_fixation(r['dnet'], trials=10000, seed=int(3000 + j))
        mc.append(dict(exact=p, mc=f, z=float((f - p) / max(np.sqrt(p * (1 - p) / 10000), 1e-9))))
    res['mc_check'] = dict(n=len(mc), max_abs_z=float(max(abs(m['z']) for m in mc)) if mc else None)
    res['kernel_check'] = kernel_check(ctx, allr)
    res['summary'] = summaries(res)
    res['wall'] = round(time.time() - t0, 1)
    keep = ('Oc', 'Fc', 'Bc', 'Pc', 'Rc', 'Rcs', 'C1', 'C4', 'B')
    slim = {k: v for k, v in res.items() if k not in ('item2', 'item4_2', 'item3', 'item3b', 'item1c', 'item4_1c')}
    slim['item1c'] = [r for r in res['item1c'] if r['xg'] in keep]
    slim['item4_1c'] = [r for r in res['item4_1c'] if r['xg'] in keep]
    slim['item2'] = [r for r in res['item2'] if r['xg'] in keep]
    slim['item4_2'] = [r for r in res['item4_2'] if r['xg'] in keep]
    slim['note'] = 'item2 / item4_2 rows kept for the offerer classes only; item3 / item3b as summaries'
    import gzip
    with gzip.open(out, 'wt') as f:
        json.dump(slim, f)
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


def _count(rows, key):
    c = {}
    for r in rows:
        c[r[key]] = c.get(r[key], 0) + 1
    return c


def summaries(res):
    S = {}
    for tag, k1, k2, k2b in (('item1', 'item1', 'item2', 'item2b'), ('item4', 'item4_1', 'item4_2', 'item4_2b')):
        grp = {}
        for r in res[k1]:
            grp.setdefault('%s|accepter into v|%s|%s|e=%s' % (tag, r['Rg'], r['orient'], r['ecls']), []).append(r)
        grp2 = {}
        for r in res[k1]:
            if r['orient'] == 'matched':
                grp2.setdefault('%s|accepter into v (matched)|%s|e class %s' % (tag, r['Rg'], r['third_g']), []).append(r)
        for r in res[k2]:
            grp.setdefault('%s|into e, %s resident|%s|%s' % (tag, r['Rg'], r['xg'], r['ecls']), []).append(r)
        for r in res[k2b]:
            grp.setdefault('%s|accepter into v, offerer resident|%s|%s|%s|%s' % (tag, r['Rg'], r['orient'], r['offerer_g'], r['ecls']), []).append(r)
        for k, sel in sorted(grp.items()):
            S[k] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
        for k, sel in sorted(grp2.items()):
            S[k] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
    for tag, k in (('item1c', 'item1c'), ('item4c', 'item4_1c')):
        grp = {}
        for r in res[k]:
            grp.setdefault('%s|into e, 1/3-constant victim|%s|%s|points at b=%s' % (tag, r['xg'], r['ecls'], r['at_b']), []).append(r)
        for kk, sel in sorted(grp.items()):
            S[kk] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
    grp = {}
    for r in res['item3']:
        grp.setdefault('item3|%s|%s|%s' % (r['island'], r['role'], r['xg']), []).append(r)
    for r in res['item3b']:
        grp.setdefault('item3b|%s|%s|%s' % (r['cls'], r['role'], r['xg']), []).append(r)
    for k, sel in sorted(grp.items()):
        S[k] = dict(_s(sel), out_if_fixed=_count(sel, 'out_if_fixed'))
    return S


def report_md(res):
    Lx = ['# Queue 79 step 0: exact invasion assays (rho * N, N = 200, w = 0.3, A_f charges; 1 = neutral; C1 tables)', '',
          'Residents: item 1 (simulating-bully unequal) %d, item 2 (Rc / Rcs matched victim) %d; item 4 (Bc unequal) %s; item 3 fair carrier '
          'islands %s; item 3b fair reader islands %s' % (res['item1_n_residents'], res['item2_n_residents'], res['item4_n_residents'],
                                                         res['item3_n_residents'], res['item3b_n_residents']),
          'Checks: jump chain (10^4 trials, %d non-neutral assays) max |z| %s; kernel (%d assays, 3,000 islands) max |z| %s' % (
              res['mc_check']['n'], ('%.2f' % res['mc_check']['max_abs_z']) if res['mc_check']['max_abs_z'] is not None else '-',
              res['kernel_check']['n'], ('%.2f' % res['kernel_check']['max_abs_z']) if res['kernel_check']['max_abs_z'] is not None else '-'), '',
          'Rate = rho x the invader\'s arrival mass under the main law (FcOcRc, delta 0.03, beta 3, phi 1/2).', '',
          '| group | n | median | min | max | share <= 1 | share > 3 | mean rate per arrival | outcome if fixed |', '|---|---|---|---|---|---|---|---|---|']
    for k, s in res['summary'].items():
        if s.get('n', 0) == 0:
            continue
        Lx.append('| %s | %d | %.4g | %.3g | %.3g | %.2f | %.2f | %.3g | %s |' % (k, s['n'], s['median'], s['min'], s['max'], s['share_le_1'], s['share_gt3'],
                                                                          s.get('rate_mean', 0), s.get('out_if_fixed')))
    return Lx


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
