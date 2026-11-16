"""Queue 80 gates (static; before RE 2-12 and the E-series are committed): G1-G4, V3 and the amendment's extra gates.

    python3 src/script_offers_gates.py OUTDIR      # writes OUTDIR/gates.json and OUTDIR/gates.md
"""
import os, sys, json, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import tplus as TP
import certified_offers as CO
import migration_window as MW
import script_offers as S
import script_offers_cat as SC
import script_offers_tables as ST

XS = np.array(MW.X)


class Tabs(TP.TabsPlus):
    def __init__(self, names, fam, code, steps, nto, fo):
        self.names, self.fam, self.K = names, fam, len(names)
        self.code, self.steps, self.nto, self.fo = code, steps, nto, fo
        self._joint()


def entry_params(term, kw):
    hb = S.host_body(term)
    if hb is None:
        return None
    l = hb[1]
    while l != 0:
        if l[0][0] == kw:
            return l[0][1][0]
        l = l[1]
    return None


# ---------------------------------------------------------------- G1
def g1(cat, code_by_machine, CHK):
    Kc = cat.Kc
    out = dict(false=dict(), checked=dict(), forgers=[], check_map_host_mismatch=0)
    # host reference against the S0 map (the S1 table is S0's map by construction)
    mism = []
    for i in range(cat.K):
        for c in range(1, 6):
            h = S.host_check(cat.terms[i], c)
            if bool(CHK[i, c - 1]) != h:
                mism.append((cat.names[i], c))
    out['check_map_host_mismatch'] = len(mism)
    out['check_map_host_examples'] = mism[:5]
    Cn = CHK[:Kc]
    for mach, code in code_by_machine.items():
        nf = 0; nck = 0; ex = []
        for i in range(cat.K):
            for c in range(1, 6):
                if not CHK[i, c - 1]:
                    continue
                a = code[i].astype(np.int64)                        # (n, p) over the catalogue
                if c == 5:
                    viol = np.isin(a, (2, 5, 8))
                else:
                    kw = 1 if c < 3 else 2
                    pr = entry_params(cat.terms[i], kw)
                    R, (H, (fn, (fp, pf))) = pr
                    en = (fn == 1) & (Cn[:, 3 + H - 1] == 1) & ((R == 0) | (Cn[:, 4] == 1))     # over n
                    ep = (fp == 1) & (Cn[:, 1 + H - 1] == 1) & ((R == 0) | (Cn[:, 4] == 1))     # over p
                    EN, EP = en[:, None], ep[None, :]
                    if kw == 1:
                        g = EN & ((pf == 0) | ~EP); viol = g & (a != 1)
                    else:
                        g = EP & ((pf == 1) | ~EN); viol = g & (a != 4)
                nck += a.size
                k = int(viol.sum())
                if k:
                    nf += k; ex.append((cat.names[i], c, k))
        out['false'][mach] = nf; out['checked'][mach] = nck; out['false_examples_' + mach] = ex[:10]
    for i in range(Kc, cat.K):
        acc = ''.join(str(c) for c in range(1, 6) if CHK[i, c - 1])
        out['forgers'].append(dict(name=cat.names[i], accepted=acc, allowed=cat.meta[i]['expected'], note=cat.meta[i]['note'],
                                   ok=set(acc) <= set(cat.meta[i]['expected'])))
    return out


# ---------------------------------------------------------------- G2 and the extra gates
def holds(m):
    """expected accepted codes of a carrier from its parameters."""
    s = set()
    if m['fn']:
        s |= {2} | ({1} if m['R'] == 0 else set())
    if m['fp']:
        s |= {4} | ({3} if m['R'] == 0 else set())
    if m['nx']:
        s.add(5)
    return s


def in_E(mx, my, side_y):
    """is y in E_x, from the parameters (truthful holdings): side_y = 'n' if y is x's next."""
    on = mx['fn'] if side_y == 'n' else mx['fp']
    y_offers = my['fp'] if side_y == 'n' else my['fn']          # y offers toward x (x is y's prev if y is x's next)
    return bool(on and y_offers and my['R'] <= mx['H'] and (mx['R'] == 0 or my['nx']))


def g2(cat, tb, CHK, cost, label):
    Kc = cat.Kc
    car = [i for i in range(Kc) if cat.meta[i]['carrier']]
    non = [i for i in range(Kc) if not cat.meta[i]['carrier']]
    out = dict(spellings=[], accept_mismatch=0)
    for i in car:
        m = cat.meta[i]
        acc = {c for c in range(1, 6) if CHK[i, c - 1]}
        ok = acc == holds(m)
        out['accept_mismatch'] += int(not ok)
        out['spellings'].append(dict(name=cat.names[i], fam=cat.fam[i], sp=cat.spell[i], accepted=''.join(map(str, sorted(acc))),
                                     expected=''.join(map(str, sorted(holds(m)))), script_nodes=m['script_nodes'],
                                     term_nodes=m['term_nodes'], s0_cost_max=int(max(cost[i, c - 1] for c in acc)) if acc else 0))
    # pairs beside non-carriers, every seat pattern
    VEC, JT, NTO = tb.VEC, tb.JT, tb.NTO
    fams = {}
    bad = []
    for a in car:
        for b in car:
            for c in non:
                for perm in itertools.permutations(range(3)):
                    slots = [None] * 3
                    slots[perm[0]], slots[perm[1]], slots[perm[2]] = a, b, c
                    sa, sb = perm[0], perm[1]
                    side_b = 'n' if (sa + 1) % 3 == sb else 'p'
                    side_a = 'n' if (sb + 1) % 3 == sa else 'p'
                    exp = in_E(cat.meta[a], cat.meta[b], side_b) and in_E(cat.meta[b], cat.meta[a], side_a)
                    o = int(VEC[JT[slots[0], slots[1], slots[2]]])
                    sh = XS[o]
                    pair = sh[sa] == 3 and sh[sb] == 3 and MW.CATMAP[o] == 0
                    to = int(NTO[slots[0], slots[1], slots[2], sa]) + int(NTO[slots[0], slots[1], slots[2], sb])
                    key = '%s|%s' % (cat.fam[a], cat.fam[b])
                    e = fams.setdefault(key, [0, 0, 0, 0, 0, 0])
                    e[0] += 1; e[1] += int(exp); e[2] += int(pair); e[3] += int(exp and not pair); e[4] += int(exp and to > 0)
                    e[5] += int(pair and not exp)
                    if exp and not pair and len(bad) < 20:
                        bad.append((cat.names[a], cat.names[b], cat.names[c], perm, exp, bool(pair)))
    out['pairs'] = {k: dict(triples=v[0], eligible=v[1], observed_pair=v[2], eligible_not_paired=v[3], eligible_timeouts=v[4],
                            fallback_pairs=v[5]) for k, v in fams.items()}
    out['pair_mismatch'] = sum(v[3] for v in fams.values())
    out['pair_timeouts'] = sum(v[4] for v in fams.values())
    out['pair_mismatch_examples'] = bad
    # three carriers: every ordered all-carrier triple, outcome class by family triple
    grp = {}
    for x in car:
        for y in car:
            for z in car:
                o = int(VEC[JT[x, y, z]])
                cl = int(MW.CATMAP[o])
                c0, c1, c2 = int(tb.code[x, y, z]), int(tb.code[y, z, x]), int(tb.code[z, x, y])
                cyc = (c0 == c1 == c2) and c0 in (1, 4)
                k = '|'.join(sorted((cat.fam[x], cat.fam[y], cat.fam[z])))
                e = grp.setdefault(k, [0, 0, 0, 0])
                e[0] += 1; e[1] += int(cl == 0); e[2] += int(cyc); e[3] += int(cl == 1)
    out['triples3'] = {k: dict(n=v[0], fair=v[1], cycle=v[2], unequal=v[3]) for k, v in sorted(grp.items())}
    return out


# ---------------------------------------------------------------- G3
def g3(catS, catK):
    acc = lambda t: CO.host_skel(t) is not None
    out = dict(K=[], S_accepted=[])
    for i in range(catK.Kc):
        if catK.meta[i]['carrier']:
            out['K'].append((catK.names[i], catK.spell[i], acc(catK.terms[i])))
    out['K_canon_accepted'] = sum(1 for n, s, a in out['K'] if s == 'canon' and a)
    out['K_noncanon_accepted'] = sum(1 for n, s, a in out['K'] if s != 'canon' and a)
    out['S_accepted'] = [catS.names[i] for i in range(catS.K) if acc(catS.terms[i])]
    return out


# ---------------------------------------------------------------- G4
def g4(catS, tbS):
    import patient_accepter as PA
    old = PA.TabsPA(cache_dir=os.path.join(ROOT, 'runs', '_cache'))
    n = 59
    newJ = tbS.VEC[tbS.JT[:n, :n, :n]]
    oldJ = old.VEC[old.JT]
    d = np.argwhere(newJ != oldJ)
    rd = np.array([f not in ('const', 'junk_f', 'junk_r') for f in old.fam[:n]])
    # reader-reader timeouts (root program a reader, at least one partner a reader) at both fuels
    ntoN = tbS.nto[:n, :n, :n]; ntoO = old.nto
    mask = rd[:, None, None] & (rd[None, :, None] | rd[None, None, :])
    out = dict(differ=int(len(d)), triples=int(n ** 3),
               to_old=int(((ntoO > 0) & mask).sum()), to_new=int(((ntoN > 0) & mask).sum()), rr_profiles=int(mask.sum()),
               to_persist=int(((ntoO > 0) & (ntoN > 0) & mask).sum()), to_vanish=int(((ntoO > 0) & (ntoN == 0) & mask).sum()),
               to_appear=int(((ntoO == 0) & (ntoN > 0) & mask).sum()))
    cls = {}
    for a, b, c in d:
        k = '%s>%s' % ('FUGWD'[MW.CATMAP[oldJ[a, b, c]]], 'FUGWD'[MW.CATMAP[newJ[a, b, c]]])
        cls[k] = cls.get(k, 0) + 1
    out['differ_classes'] = cls
    out['differ_examples'] = [(old.names[a], old.names[b], old.names[c], int(oldJ[a, b, c]), int(newJ[a, b, c])) for a, b, c in d[:15]]
    # carriers with simulating readers at the new fuel: timeouts by whom
    car = [i for i in range(catS.Kc) if catS.meta[i]['carrier']]
    rdS = [i for i in range(n) if rd[i]]
    sub = tbS.nto[np.ix_(rdS, car, list(range(catS.Kc)))]
    out['reader_vs_carrier_to_share'] = round(float((sub > 0).mean()), 4)
    sub2 = tbS.nto[np.ix_(car, rdS, list(range(catS.Kc)))]
    out['carrier_vs_reader_to_share'] = round(float((sub2 > 0).mean()), 4)
    return out


# ---------------------------------------------------------------- V3
def v3(catS, t0, t1):
    out = {}
    for nm, a, b in (('code', t0[0], t1[0]), ('steps', t0[1], t1[1]), ('nto', t0[2], t1[2]), ('fo', t0[3], t1[3])):
        out[nm + '_diff'] = int((a != b).sum())
    out['profiles'] = int(t0[0].size)
    # residual fuel: each tabulated check at root with fuel cost (one below what the body needs) and cost + 1, and inside a capk
    # frame with cap cost and cost + 1; S0 and S1 must agree in value and ticks
    s1 = ST.load_s1(catS)
    SC.install_s1(s1)
    nd = 0; n = 0; ex = []
    for i in range(catS.K):
        for c in range(1, 6):
            arg = ('pair', ('quote', catS.terms[i]), ('nat', c))
            cost = s1[(L.canon_term(catS.terms[i]), c)][1]
            for kind in ('root', 'capk'):
                for f in (cost, cost + 1):
                    if kind == 'root':
                        t, fuel = ('app', ('lib', S.ID_CCORE), arg), f
                    else:
                        t, fuel = ('capk', ('nat', f), ('lib', S.ID_CCORE), arg), 10 ** 7
                    r = []
                    for m in ('S0', 'S1'):
                        S.set_machine(m)
                        v, st = L.run_big(L.evaluate, t, fuel)
                        r.append((v if isinstance(v, str) else repr(v), st))
                    n += 1
                    if r[0] != r[1]:
                        nd += 1
                        if len(ex) < 5:
                            ex.append((catS.names[i], c, kind, f, r))
    S.set_machine('S1')
    out['residual_tests'] = n; out['residual_diff'] = nd; out['residual_examples'] = ex
    return out


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    TP.install_counter(); S.set_regress(True)
    res = {}
    cat1, c1, s1_, n1, f1 = ST.get_tables('S', 'S1', forg=True)
    cat0, c0, s0_, n0, f0 = ST.get_tables('S', 'S0', forg=True)
    catK, cK, sK, nK, fK = ST.get_tables('K', 'C1')
    CHK, cost = ST.chk_matrix(cat1)
    Kc = cat1.Kc
    res['fuel'] = dict(KCHK=S.KCHK, WCHK=S.WCHK, cap=S.CAPP, KR=S.KRP)
    res['kappa_S'] = int(max(cost[i, c] for i in range(cat1.K) for c in range(5) if CHK[i, c]))
    res['worst_any'] = int(cost.max())
    res['G1'] = g1(cat1, dict(S1=c1, S0=c0), CHK)
    tbS = Tabs(cat1.names[:Kc], cat1.fam[:Kc], c1[:Kc], s1_[:Kc], n1[:Kc], f1[:Kc])
    tb0 = Tabs(cat1.names[:Kc], cat1.fam[:Kc], c0[:Kc], s0_[:Kc], n0[:Kc], f0[:Kc])
    res['G2'] = g2(cat1, tbS, CHK, cost, 'S1')
    g2b = g2(cat1, tb0, CHK, cost, 'S0')
    res['G2']['S0_pair_mismatch'] = g2b['pair_mismatch']; res['G2']['S0_pair_timeouts'] = g2b['pair_timeouts']
    res['G2']['S0_triples3_equal'] = g2b['triples3'] == res['G2']['triples3']
    res['G3'] = g3(cat1, catK)
    res['G4'] = g4(cat1, tbS)
    res['V3'] = v3(cat1, (c0, s0_, n0, f0), (c1, s1_, n1, f1))
    res['wall'] = round(time.time() - t0)
    json.dump(res, open(os.path.join(outdir, 'gates.json'), 'w'), indent=1, default=str)
    return res


if __name__ == '__main__':
    r = main(sys.argv[1])
    print(json.dumps({k: v for k, v in r.items() if k not in ('G2',)}, default=str)[:4000])
