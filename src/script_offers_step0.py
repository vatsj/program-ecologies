"""Step 0 of queue 80 (spec specs/2026-11-16-script-checked-offers.md): exact invasion assays on the world-S tables (S1) at (KR', cap').

Every edge: the exact fixation probability of one invader copy in one slot of a named resident triple (the other slots monomorphic), N = 200,
w = 0.3, A_f charges (P_fail = 0.1), rho * N (1 = neutral); rate per arrival = rho x the invader's mass under the reference law
(A2, delta = 0.03, beta = 3, phi = 1/2).  Resident triples range over every seat pattern; "beside c" ranges over the 59 non-carriers
for which the named pair is the island's outcome.

 s1  a carrier of one spelling into a pair slot of a fair island of a pointing carrier of another spelling (and of the same spelling)
 s2  the same carrier spellings as the second step of the accepter route: Rc (any spelling) into the victim's seat of a simulating-bully
     unequal island whose excluded slot holds a carrier (any spelling) pointing at v; and certified offerers (any spelling) into e with
     Rc (any spelling) in v
 b1  Bc into the pair slots and the excluded slot of (Fc+, Fc+) and (Pc+, Pc+) islands
 b2  Pc+ and Fc+ (and Fc, Oc+, Rc+) into the excluded slot of Bc's unequal island (Bc on 2/3 with a 1/3 constant)
 b3  the simulating bully into the pair slots of fair carrier islands (A2's and A4's families)
 b4  1/3 constants into the third slot of (Pc+, Pc+) and (Fc+, Bc)
 jc  jump chain: 10^4 trials on 60 non-neutral edges (|z| reported)

    python3 src/script_offers_step0.py OUTDIR
"""
import os, sys, json, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import migration_window as MW
from bully_resist_step0 import rho_exact, mc_fixation, N0
import script_offers_dyn as D

PFAIL = 0.1
XS = np.array(MW.X)


class Ctx:
    def __init__(self):
        tb = D.tabs('S')
        self.tb = tb
        self.names = tb.names; self.idx = {n: i for i, n in enumerate(tb.names)}
        self.NET = tb.payoff(PFAIL, PFAIL)
        self.OUT = tb.VEC[tb.JT]
        self.law = D.law_arm('A2', 0.03, 3.0, 0.5)
        self.non = [i for i in range(tb.K) if not tb.meta[i].get('carrier')]

    def fam(self, f, sp=None):
        return [i for i in range(self.tb.K) if self.tb.fam[i] == f and (sp is None or self.tb.spell[i] == sp)]


def edge(ctx, res, s, x):
    t = list(res); t[s] = x
    d = float(ctx.NET[t[0], t[1], t[2]][s] - ctx.NET[res[0], res[1], res[2]][s])
    rho = rho_exact(d)
    o = int(ctx.OUT[tuple(t)])
    return dict(rhoN=rho * N0, d=d, rate=rho * float(ctx.law[x]), out=int(MW.CATMAP[o]), sh=[int(v) for v in XS[o]])


def pair_islands(ctx, A, B, thirds=None):
    """fair triples where a in A and b in B form the pair (shares 3, 3), the third slot in `thirds` (default the non-carriers)."""
    out = []
    thirds = ctx.non if thirds is None else thirds
    for a in A:
        for b in B:
            for c in thirds:
                for perm in itertools.permutations(range(3)):
                    t = [0, 0, 0]; t[perm[0]] = a; t[perm[1]] = b; t[perm[2]] = c
                    o = int(ctx.OUT[tuple(t)])
                    if MW.CATMAP[o] == 0 and XS[o][perm[0]] == 3 and XS[o][perm[1]] == 3:
                        out.append((tuple(t), perm[0], perm[1], perm[2]))
    return sorted(set(out))


def unequal_islands(ctx, bullies, victims):
    out = []
    for b in bullies:
        for v in victims:
            for x in range(ctx.tb.K):
                for sb in range(3):
                    for sv in range(3):
                        if sv == sb:
                            continue
                        se = 3 - sb - sv
                        t = [0, 0, 0]; t[sb] = b; t[sv] = v; t[se] = x
                        o = int(ctx.OUT[tuple(t)])
                        if MW.CATMAP[o] == 1 and XS[o][sb] == 4 and XS[o][sv] == 2:
                            out.append((tuple(t), sb, sv, se))
    return sorted(set(out))


def summ(rows):
    if not rows:
        return dict(n=0)
    r = np.array([x['rhoN'] for x in rows])
    return dict(n=len(rows), median=float(np.median(r)), min=float(r.min()), max=float(r.max()), mean=float(r.mean()),
                share_gt3=float((r > 3).mean()), share_lt_third=float((r < 1 / 3).mean()),
                fixed_out=dict(zip(*[list(map(str, u)) if k == 0 else list(map(int, u)) for k, u in enumerate(np.unique([x['out'] for x in rows], return_counts=True))])))


def points(ctx, x, sx, sy):
    m = ctx.tb.meta[x]
    if not m.get('carrier'):
        return False
    return (m['fn'] if (sx + 1) % 3 == sy else m['fp']) == 1


def main(outdir):
    t0 = time.time()
    ctx = Ctx()
    out = {}
    allrows = []
    # s1: spellings pair
    s1 = {}
    for fa, fb in (('s_firm', 's_firm'), ('s_open', 's_acc'), ('s_firm', 's_open'), ('s_firm+', 's_firm+'), ('s_prud+', 's_prud+'),
                   ('s_prud+', 's_open+')):
        for spa in D.S.SPELLINGS:
            isl = pair_islands(ctx, ctx.fam(fa, spa), ctx.fam(fb, spa), thirds=[ctx.idx['C8'], ctx.idx['C2'], ctx.idx['Snzn']])
            for (t, sa, sb, sc) in isl:
                for spx in D.S.SPELLINGS:
                    for x in ctx.fam(fb):
                        if ctx.tb.spell[x] != spx or not (points(ctx, x, sb, sa)):
                            continue
                        e = edge(ctx, t, sb, x)
                        k = '%s<-%s|%s' % (fa, fb, 'same' if spx == spa else 'cross')
                        s1.setdefault(k, []).append(e); allrows.append(e)
    out['s1'] = {k: summ(v) for k, v in s1.items()}
    # s2: the accepter route across spellings
    bul = ctx.fam('bully')
    rc = ctx.fam('s_acc')
    s2 = {}
    third = [ctx.idx['C0'], ctx.idx['C3'], ctx.idx['C6']]
    for (t, sb, sv, se) in unequal_islands(ctx, bul, third):
        x_e = t[se]
        if ctx.tb.meta[x_e].get('carrier') and points(ctx, x_e, se, sv) and ctx.tb.fam[x_e] in ('s_firm', 's_open', 's_bully'):
            for r in rc:
                if points(ctx, r, sv, se):
                    e = edge(ctx, t, sv, r)
                    k = 'Rc into v, e = %s|%s' % (ctx.tb.fam[x_e], 'same' if ctx.tb.spell[r] == ctx.tb.spell[x_e] else 'cross')
                    s2.setdefault(k, []).append(e); allrows.append(e)
    for (t, sb, sv, se) in unequal_islands(ctx, bul, rc):
        if not points(ctx, t[sv], sv, se):
            continue
        for x in ctx.fam('s_firm') + ctx.fam('s_open'):
            if points(ctx, x, se, sv):
                e = edge(ctx, t, se, x)
                k = '%s into e, Rc in v|%s' % (ctx.tb.fam[x], 'same' if ctx.tb.spell[x] == ctx.tb.spell[t[sv]] else 'cross')
                s2.setdefault(k, []).append(e); allrows.append(e)
    out['s2'] = {k: summ(v) for k, v in s2.items()}
    # b1: Bc into (Fc+, Fc+) and (Pc+, Pc+)
    bc = ctx.fam('s_bully')
    b1 = {}
    for f in ('s_firm+', 's_prud+'):
        for (t, sa, sb, sc) in pair_islands(ctx, ctx.fam(f, 'canon'), ctx.fam(f)):
            for x in bc:
                for s, role in ((sa, 'pair'), (sc, 'excl')):
                    e = edge(ctx, t, s, x)
                    b1.setdefault('Bc into %s of (%s, %s)' % (role, f, f), []).append(e); allrows.append(e)
    out['b1'] = {k: summ(v) for k, v in b1.items()}
    # b2: into e of Bc's unequal island
    b2 = {}
    for (t, sb, sv, se) in unequal_islands(ctx, bc, third):
        for f in ('s_prud+', 's_firm+', 's_firm', 's_open+', 's_acc+', 's_open', 's_openR+'):
            for x in ctx.fam(f):
                if not points(ctx, x, se, sb) and f not in ('s_prud+',):
                    continue
                e = edge(ctx, t, se, x)
                b2.setdefault('%s into e of Bc on 2/3' % f, []).append(e); allrows.append(e)
    out['b2'] = {k: summ(v) for k, v in b2.items()}
    # b3: simulating bully into pair slots of fair carrier islands
    b3 = {}
    for fa, fb in (('s_firm', 's_firm'), ('s_open', 's_acc'), ('s_firm+', 's_firm+'), ('s_prud+', 's_prud+'), ('s_prud+', 's_acc+'),
                   ('s_firm', 's_bully')):
        for (t, sa, sb, sc) in pair_islands(ctx, ctx.fam(fa, 'canon'), ctx.fam(fb), thirds=[ctx.idx['C8'], ctx.idx['C2'], ctx.idx['C5']]):
            for x in bul:
                for s in (sa, sb):
                    e = edge(ctx, t, s, x)
                    b3.setdefault('B into pair of (%s, %s)' % (fa, fb), []).append(e); allrows.append(e)
    out['b3'] = {k: summ(v) for k, v in b3.items()}
    # b4: 1/3 constants into the third slot
    b4 = {}
    for fa, fb in (('s_prud+', 's_prud+'), ('s_firm+', 's_bully'), ('s_firm', 's_bully')):
        for (t, sa, sb, sc) in pair_islands(ctx, ctx.fam(fa), ctx.fam(fb), thirds=[ctx.idx['C8']]):
            for x in third:
                e = edge(ctx, t, sc, x)
                b4.setdefault('1/3 constants into third of (%s, %s)' % (fa, fb), []).append(e); allrows.append(e)
    out['b4'] = {k: summ(v) for k, v in b4.items()}
    # jump chain on non-neutral edges
    nn = [r for r in allrows if abs(r['d']) > 1e-9]
    rng = np.random.default_rng(5)
    pick = [nn[i] for i in rng.choice(len(nn), size=min(60, len(nn)), replace=False)] if nn else []
    zs = []
    for k, r in enumerate(pick):
        p, per = mc_fixation(r['d'], trials=10000, seed=100 + k)
        rho = r['rhoN'] / N0
        sd = np.sqrt(max(rho * (1 - rho), 1e-12) / 10000)
        zs.append((p - rho) / sd if rho > 1e-6 else 0.0)
    out['jump_chain'] = dict(n=len(pick), max_abs_z=float(np.max(np.abs(zs))) if zs else None)
    out['n_edges'] = len(allrows)
    out['wall'] = round(time.time() - t0)
    os.makedirs(outdir, exist_ok=True)
    json.dump(out, open(os.path.join(outdir, 'step0.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    r = main(sys.argv[1])
    print(json.dumps(r, indent=1)[:6000])
