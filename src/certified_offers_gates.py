"""Gates of queue 79 (spec specs/2026-11-15-certified-offers.md, "Gates") and V3.

    python3 src/certified_offers_gates.py OUT.json OUT.md

 G1  soundness: the check map (C0 term, C1 primitive, host reference) on every catalogue program and forger, both sides; every forger
     rejected; for every accepted program and every (next, prev) of the catalogue, in both machines, its play equals S(t) (the certified
     branch exactly; the fallback branch compared with the fallback's standalone table, differences reported as fuel-reduced fallbacks).
 G2  reader-reader: Oc x Rc, Oc x Fc, Fc x Fc, Rc x Rc, Fc x Rc, Pc x Pc (and Rcs, Bc) in every seat pattern with every non-carrier in the
     third slot: outcome, the pair's own timed-out reads, the third slot's, charges; three-carrier triples (Fc)^3 over orientations: cycle
     share and mean payoff per slot.
 G3  legibility: a bully (Bn, Bp, Bcn, Bcp) with Rc (matched) as victim and each program in the excluded slot: does the bully's read
     complete; outcome. Comparators: queue 78's R (Rnn / Rpn) and the 1/3 constant as victim.
 G4  mixed worlds: triples with a carrier and a simulating reader (F, O, R, P, bullies): timed-out reads by side, split into regress
     (a re-entered read) and cap exhaustion; in particular the simulating bully against Fc and Bc against F.
 G5  the first 59 programs' tables equal queue 78's (code, steps, nto, fo, joint code).
 V3  C1's tables equal C0's (actions, timeouts, forfeits) on the catalogue cube; every disagreement classified.
"""
import os, sys, json, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import certified_offers as CO
import patient_accepter as PA
import migration_window as MW

PFAIL = 0.1
CLS = ['F', 'U', 'G', 'W', 'D']
CACHE = os.path.join(ROOT, 'runs', '_cache')


def load(machine):
    return CO.TabsCO(cache_dir=CACHE, machine=machine)


def expected(tb, p, n, v):
    """S(t) for carrier p with next n, prev v: ('cert', code) or ('fb', None)."""
    fn, fp, pr = tb.cat.meta[p]['cert']
    cn = tb.cat.meta[n]['cert']; cv = tb.cat.meta[v]['cert']
    en = fn == 1 and cn is not None and cn[1] == 1
    ep = fp == 1 and cv is not None and cv[0] == 1
    if en and ep:
        return ('cert', 1 if pr == 0 else 4)
    if en:
        return ('cert', 1)
    if ep:
        return ('cert', 4)
    return ('fb', None)


def gate1(tabs):
    out = {}
    cat = CO.CatalogueCO(extra=CO.forgers())
    rows = []
    agree = True
    for i, nm in enumerate(cat.names):
        t = cat.terms[i]
        hs = CO.host_skel(t)
        r = dict(name=nm, fam=cat.fam[i], host=hs)
        for m in ('C0', 'C1'):
            for w in (0, 1):
                v, st = CO.check_value(m, t, w)
                r['%s_w%d' % (m, w)] = v; r['%s_w%d_steps' % (m, w)] = int(st)
                hv = 'F' if hs is None else ('T' if (hs[0] if w == 0 else hs[1]) == 1 else 'F')
                agree &= (v == hv)
        rows.append(r)
    out['check_map'] = rows
    out['check_map_agree'] = bool(agree)
    out['accepted'] = [r['name'] for r in rows if r['host'] is not None]
    out['forgers_rejected'] = {r['name']: (r['host'] is None and all(r['%s_w%d' % (m, w)] == 'F' for m in ('C0', 'C1') for w in (0, 1)))
                               for r in rows if r['fam'] == 'forger'}
    out['meta_matches_host'] = all(cat.meta[i]['cert'] == CO.host_skel(cat.terms[i]) for i in range(len(cat.names)) if cat.fam[i] != 'forger')
    conf = {}
    for m, tb in tabs.items():
        K = tb.K
        carriers = [p for p in range(K) if tb.cat.meta[p]['cert'] is not None]
        n_cert = n_cert_false = n_fb = n_fb_diff = 0
        examples = []
        fbdiff = {}
        for p in carriers:
            fb = tb.cat.idx[tb.cat.meta[p]['fb']]
            for n in range(K):
                for v in range(K):
                    kind, code = expected(tb, p, n, v)
                    got = int(tb.code[p, n, v])
                    if kind == 'cert':
                        n_cert += 1
                        if got != code or tb.nto[p, n, v] or tb.fo[p, n, v]:
                            n_cert_false += 1
                            if len(examples) < 10:
                                examples.append((tb.names[p], tb.names[n], tb.names[v], got, code))
                    else:
                        n_fb += 1
                        if got != int(tb.code[fb, n, v]) or tb.nto[p, n, v] != tb.nto[fb, n, v] or tb.fo[p, n, v] != tb.fo[fb, n, v]:
                            n_fb_diff += 1
                            fbdiff[tb.names[p]] = fbdiff.get(tb.names[p], 0) + 1
        conf[m] = dict(carriers=len(carriers), profiles_certified=n_cert, false_certified=n_cert_false, examples=examples,
                       profiles_fallback=n_fb, fallback_differs_from_standalone=n_fb_diff, fallback_diff_by_program=fbdiff)
    out['conformance'] = conf
    return out


def families(tb):
    g = {}
    for i in range(tb.K):
        g.setdefault(tb.fam[i], []).append(i)
    return g


def gate2(tb):
    fam = families(tb)
    noncar = [i for i in range(tb.K) if tb.cat.meta[i]['cert'] is None]
    OUT = tb.VEC[tb.JT]
    NET = tb.payoff(PFAIL, PFAIL)
    pairs = [('c_open', 'c_acc'), ('c_open', 'c_firm'), ('c_firm', 'c_firm'), ('c_acc', 'c_acc'), ('c_firm', 'c_acc'), ('c_prud', 'c_prud'),
             ('c_open', 'c_open'), ('c_accs', 'c_open'), ('c_accs', 'c_firm'), ('c_bully', 'c_firm'), ('c_bully', 'c_open'), ('c_bully', 'c_acc'),
             ('c_bully', 'c_bully'), ('c_prud', 'c_firm')]
    res = {}
    for fa, fb in pairs:
        st = dict(pointing=0, fair_pair=0, pair_to=0, third_to=0, other_outcomes={}, nonpointing=0, nonpointing_fair_pair=0, charge_pair=0.0)
        for x in fam[fa]:
            for y in fam[fb]:
                for sx in range(3):
                    for sy in range(3):
                        if sx == sy:
                            continue
                        sz = 3 - sx - sy
                        # pointing: x's flag toward y and y's toward x
                        cx, cy = tb.cat.meta[x]['cert'], tb.cat.meta[y]['cert']
                        x_to_y = cx[0] if (sx + 1) % 3 == sy else cx[1]
                        y_to_x = cy[0] if (sy + 1) % 3 == sx else cy[1]
                        point = x_to_y == 1 and y_to_x == 1
                        for z in noncar:
                            t = [0, 0, 0]; t[sx] = x; t[sy] = y; t[sz] = z; t = tuple(t)
                            o = int(OUT[t]); sh = MW.X[o]
                            fairxy = MW.CATMAP[o] == 0 and sh[sx] > 0 and sh[sy] > 0
                            if point:
                                st['pointing'] += 1
                                st['fair_pair'] += int(fairxy)
                                st['pair_to'] += int(tb.NTO[t][sx] > 0 or tb.NTO[t][sy] > 0)
                                st['third_to'] += int(tb.NTO[t][sz] > 0)
                                st['charge_pair'] += float(tb.NTO[t][sx] + tb.NTO[t][sy] + tb.FO[t][sx] + tb.FO[t][sy]) * PFAIL
                                if not fairxy:
                                    k = '%s:%s' % (CLS[MW.CATMAP[o]], tb.names[z])
                                    st['other_outcomes'][k] = st['other_outcomes'].get(k, 0) + 1
                            else:
                                st['nonpointing'] += 1
                                st['nonpointing_fair_pair'] += int(fairxy)
        st['charge_pair'] = st['charge_pair'] / max(st['pointing'], 1)
        res['%s x %s' % (fa, fb)] = st
    # three-carrier triples: (Fc)^3, (Fc, Fc, Oc-pointing), (Pc)^3, (Bc, Fc, Fc)
    tri = {}
    for lab, A, B, C in (('Fc^3', 'c_firm', 'c_firm', 'c_firm'), ('Pc^3', 'c_prud', 'c_prud', 'c_prud'), ('Bc,Fc,Fc', 'c_bully', 'c_firm', 'c_firm')):
        n = cyc = 0; pay = []
        byor = {}
        for a in fam[A]:
            for b in fam[B]:
                for c in fam[C]:
                    t = (a, b, c)
                    o = int(OUT[t])
                    n += 1
                    g = tb.GROSS[t]
                    pay.append(float(np.mean(g)))
                    prefs = ''.join('np'[tb.cat.meta[q]['cert'][2]] for q in t)
                    e = byor.setdefault(prefs, [0, 0, 0.0])
                    e[0] += 1; e[1] += int(MW.CATMAP[o] != 0); e[2] += float(np.mean(g))
                    cyc += int(MW.CATMAP[o] != 0)
        tri[lab] = dict(n=n, non_fair_share=cyc / n, mean_payoff_per_slot=float(np.mean(pay)),
                        by_orientation={k: dict(n=v[0], non_fair=v[1] / v[0], mean_pay=v[2] / v[0]) for k, v in sorted(byor.items())})
    res['three_carrier'] = tri
    return res


def unequal_seats(bname):
    """bully in slot b; for n-bullies the victim is b+1 (its next), excluded b+2; for p-bullies the victim is b-1, excluded b+1."""
    out = []
    for b in range(3):
        if bname[-1] == 'n':
            out.append((b, (b + 1) % 3, (b + 2) % 3))
        else:
            out.append((b, (b - 1) % 3, (b + 1) % 3))
    return out


def gate3(tb):
    nm = tb.names; I = tb.cat.idx
    OUT = tb.VEC[tb.JT]
    res = {}
    for bully in ('Bn', 'Bp', 'Bcn', 'Bcp'):
        d = bully[-1]
        for vic in (('Rcn' if d == 'n' else 'Rcp'), ('Rnn' if d == 'n' else 'Rpn'), ('C3' if d == 'n' else 'C0'), ('Rcsn' if d == 'n' else 'Rcsp')):
            rows = {}
            for (sb, sv, se) in unequal_seats(bully):
                for x in range(tb.K):
                    t = [0, 0, 0]; t[sb] = I[bully]; t[sv] = I[vic]; t[se] = x; t = tuple(t)
                    o = int(OUT[t]); sh = MW.X[o]
                    cl = CLS[MW.CATMAP[o]]
                    if cl == 'F':
                        pr = ''.join(sorted('bve'[[sb, sv, se].index(s)] for s in range(3) if sh[s] > 0))
                        cl = 'F(%s)' % pr
                    elif cl == 'U':
                        cl = 'U(b%d,v%d)' % (sh[sb], sh[sv])
                    g = rows.setdefault(_grp(tb, x), dict(n=0, bully_read_to=0, victim_read_to=0, e_read_to=0, outcomes={}))
                    g['n'] += 1
                    g['bully_read_to'] += int(tb.NTO[t][sb] > 0)
                    g['victim_read_to'] += int(tb.NTO[t][sv] > 0)
                    g['e_read_to'] += int(tb.NTO[t][se] > 0)
                    g['outcomes'][cl] = g['outcomes'].get(cl, 0) + 1
            res['%s|%s' % (bully, vic)] = rows
    return res


def _grp(tb, i):
    f, n = tb.fam[i], tb.names[i]
    if f == 'const':
        return n
    return {'single': 'F(single)', 'two': 'F(two)', 'exploit': 'X', 'bully': 'B', 'junk_f': 'J', 'junk_r': 'J', 'prudent': 'P', 'prudent_a': 'Q',
            'opener': 'O', 'single2': 'F2', 'accepter': 'R', 'c_open': 'Oc', 'c_firm': 'Fc', 'c_acc': 'Rc', 'c_accs': 'Rcs', 'c_bully': 'Bc',
            'c_prud': 'Pc'}[f] + ('' if f.startswith('c_') or f in ('bully', 'accepter') else '')


SIMF = {'single': 'F', 'two': 'F', 'opener': 'O', 'accepter': 'R', 'prudent': 'P', 'prudent_a': 'P', 'bully': 'B', 'single2': 'F', 'exploit': 'X'}


def gate4(tb):
    """over all triples with >= 1 carrier and >= 1 simulating reader: per (carrier family, sim family) the share of profiles where
    the carrier's reads time out and where the reader's reads time out, split by regress vs cap."""
    K = tb.K
    carr = [i for i in range(K) if tb.cat.meta[i]['cert'] is not None]
    sims = [i for i in range(K) if tb.fam[i] in SIMF]
    res = {}
    for c in carr:
        for s in sims:
            key = '%s x %s' % (_grp(tb, c), SIMF[tb.fam[s]])
            e = res.setdefault(key, dict(n=0, carrier_to=0, carrier_to_regress=0, reader_to=0, reader_to_regress=0, reader_to_cap=0))
            for sc in range(3):
                for ss in range(3):
                    if ss == sc:
                        continue
                    sz = 3 - sc - ss
                    for z in range(K):
                        t = [0, 0, 0]; t[sc] = c; t[ss] = s; t[sz] = z; t = tuple(t)
                        e['n'] += 1
                        # the table of program a with next n, prev v: reg[a, n, v]
                        ct = tb.NTO[t][sc] > 0; rt = tb.NTO[t][ss] > 0
                        cr = _reg(tb, t, sc) > 0; rr = _reg(tb, t, ss) > 0
                        e['carrier_to'] += int(ct); e['carrier_to_regress'] += int(ct and cr)
                        e['reader_to'] += int(rt); e['reader_to_regress'] += int(rt and rr); e['reader_to_cap'] += int(rt and not rr)
    for e in res.values():
        n = e['n']
        for k in list(e):
            if k != 'n':
                e[k + '_share'] = round(e[k] / n, 4)
    return res


def scale_caps(t, f):
    """the term t with every literal simulation cap (first argument of capk / run) multiplied by f."""
    tag = t[0]
    if tag in ('capk', 'run'):
        k = t[1]
        k2 = ('nat', k[1] * f) if k[0] == 'nat' else scale_caps(k, f)
        return (tag, k2) + tuple(scale_caps(a, f) for a in t[2:])
    if tag in ('v', 'con', 'nat', 'lib'):
        return t
    if tag == 'quote':
        return ('quote', scale_caps(t[1], f))
    if tag in ('lam', 'fix'):
        return (tag, scale_caps(t[1], f))
    if tag == 'op':
        return ('op', t[1], scale_caps(t[2], f), scale_caps(t[3], f))
    if tag == 'sim':
        return ('sim', t[1] * f, scale_caps(t[2], f))
    return (tag,) + tuple(scale_caps(a, f) for a in t[1:])


def gate4b(tb, n_per=300, f=20, seed=79, zset=None):
    """operational split of timed-out reads: re-evaluate a sample of timed-out profiles with every cap (and the root fuel) x f; a read
    that still times out is a regress (mutual simulation that no cap ends), one that completes was cap exhaustion (checks plus fallback
    reads that do not fit one cap).  Groups: carrier family x reader class, the read by the reader of the carrier triple and the carrier's
    own fallback reads; in particular the simulating bully against Fc and Bc against F."""
    import tplus as TP
    import lt_code as L
    CO.set_machine(tb.machine)
    rng = np.random.default_rng(seed)
    K = tb.K
    big = [scale_caps(t, f) for t in tb.cat.terms]
    carr = [i for i in range(K) if tb.cat.meta[i]['cert'] is not None]
    sims = [i for i in range(K) if tb.fam[i] in SIMF]
    groups = {}
    for c in carr:
        for s in sims:
            groups.setdefault((_grp(tb, c), SIMF[tb.fam[s]]), []).append((c, s))
    res = {}
    for (gc, gs), lst in sorted(groups.items()):
        cand = []
        for c, s in lst:
            for who, a in (('reader', s), ('carrier', c)):
                # profiles of program a whose partners include the other: a with next / prev
                other = c if who == 'reader' else s
                for z in (range(K) if zset is None else zset):
                    for (n, v) in ((other, z), (z, other)):
                        if tb.nto[a, n, v] > 0:
                            cand.append((who, a, n, v))
        if not cand:
            continue
        pick = [cand[int(j)] for j in rng.choice(len(cand), size=min(n_per, len(cand)), replace=False)]
        e = dict(sampled=len(pick), timed_out_profiles=len(cand), reader=[0, 0], carrier=[0, 0])
        for who, a, n, v in pick:
            r = L.run_big(TP.f_eval, big[a], big[n], big[v], CO.CT.KR * f)
            still = r[2] > 0
            e[who][0] += 1; e[who][1] += int(still)
        res['%s x %s' % (gc, gs)] = e
    return res


def _reg(tb, t, s):
    a = t[s]; n = t[(s + 1) % 3]; v = t[(s - 1) % 3]
    return int(tb.reg[a, n, v])


def gate5(tb):
    old = PA.TabsPA(cache_dir=CACHE)
    n = 59
    return {a: bool((getattr(tb, a)[:n, :n, :n] == getattr(old, a)).all()) for a in ('code', 'steps', 'nto', 'fo', 'JT')}


def v3(t1, t0):
    K = t1.K
    d_code = t1.code != t0.code
    d_nto = t1.nto != t0.nto
    d_fo = t1.fo != t0.fo
    rows = {}
    for p in range(K):
        nd = int(d_code[p].sum())
        if nd or int(d_nto[p].sum()) or int(d_fo[p].sum()):
            rows[t1.names[p]] = dict(code=nd, nto=int(d_nto[p].sum()), fo=int(d_fo[p].sum()),
                                     code_with_nto_change=int((d_code[p] & d_nto[p]).sum()))
    J1 = t1.VEC[t1.JT]; J0 = t0.VEC[t0.JT]
    dj = J1 != J0
    involve = np.zeros((K, K, K), bool)
    car = np.array([t1.cat.meta[i]['cert'] is not None for i in range(K)])
    involve |= car[:, None, None] | car[None, :, None] | car[None, None, :]
    return dict(profiles=int(K ** 3), action_diff=int(d_code.sum()), nto_diff=int(d_nto.sum()), fo_diff=int(d_fo.sum()),
                action_diff_without_nto_change=int((d_code & ~d_nto).sum()), outcome_triples_diff=int(dj.sum()),
                outcome_triples_diff_without_carrier=int((dj & ~involve).sum()), by_program=rows,
                first59_identical=bool((~d_code[:59, :59, :59]).all() and (~d_nto[:59, :59, :59]).all()))


def main(out, md):
    t0 = time.time()
    tabs = {'C1': load('C1'), 'C0': load('C0')}
    tb = tabs['C1']
    res = dict(kappa=CO.KAPPA, K=tb.K)
    res['G1'] = gate1(tabs)
    res['G2'] = gate2(tb)
    res['G2_C0'] = gate2(tabs['C0'])
    res['G3'] = gate3(tb)
    res['G3_C0'] = gate3(tabs['C0'])
    res['G4'] = gate4(tb)
    res['G4b'] = gate4b(tb)
    res['G4b_const'] = gate4b(tb, zset=[i for i in range(tb.K) if tb.fam[i] == 'const'])
    res['G5'] = gate5(tb)
    res['V3'] = v3(tb, tabs['C0'])
    res['wall'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'), indent=1, default=str)
    open(md, 'w').write('\n'.join(report(res)) + '\n')


def report(res):
    g1 = res['G1']
    Lx = ['# Queue 79 gates (C1 tables unless marked; kappa = %d; K = %d)' % (res['kappa'], res['K']), '',
          '## G1 soundness', '',
          '- check map: C0 term = C1 primitive = host reference on all %d programs and forgers, both sides: **%s**' % (len(g1['check_map']), g1['check_map_agree']),
          '- accepted (%d): %s' % (len(g1['accepted']), ', '.join(g1['accepted'])),
          '- forgers rejected: %s' % g1['forgers_rejected'],
          '- catalogue certificates equal the host parse: %s' % g1['meta_matches_host']]
    for m, c in g1['conformance'].items():
        Lx.append('- %s: %d carriers; certified-branch profiles %d, **false %d**; fallback profiles %d, differing from the standalone fallback %d %s'
                  % (m, c['carriers'], c['profiles_certified'], c['false_certified'], c['profiles_fallback'], c['fallback_differs_from_standalone'],
                     c['fallback_diff_by_program'] if c['fallback_differs_from_standalone'] else ''))
    Lx += ['', '| program | C0 check steps (w=0 / w=1) | C1 |', '|---|---|---|']
    for r in g1['check_map']:
        Lx.append('| %s | %s %d / %s %d | %s %d |' % (r['name'], r['C0_w0'], r['C0_w0_steps'], r['C0_w1'], r['C0_w1_steps'], r['C1_w0'], r['C1_w0_steps']))
    for tag in ('G2', 'G2_C0'):
        Lx += ['', '## %s reader-reader (every seat pattern, every non-carrier third slot)' % tag, '',
               '| families | pointing triples | fair pair (x, y) | pair read timed out | third timed out | mean pair charge | non-pointing (fair pair) | other outcomes (pointing) |',
               '|---|---|---|---|---|---|---|---|']
        for k, s in res[tag].items():
            if k == 'three_carrier':
                continue
            oo = sorted(s['other_outcomes'].items(), key=lambda x: -x[1])[:4]
            Lx.append('| %s | %d | %d | %d | %d | %.3f | %d (%d) | %s |' % (k, s['pointing'], s['fair_pair'], s['pair_to'], s['third_to'], s['charge_pair'],
                                                                     s['nonpointing'], s['nonpointing_fair_pair'], oo))
        Lx += ['', 'Three-carrier triples:', '']
        for k, s in res[tag]['three_carrier'].items():
            Lx.append('- %s: %d triples, non-fair share %.3f, mean gross payoff per slot %.4f (cycle-free rule: 1/3); by preference orientation %s'
                      % (k, s['n'], s['non_fair_share'], s['mean_payoff_per_slot'],
                         {o: (round(v['non_fair'], 3), round(v['mean_pay'], 3)) for o, v in s['by_orientation'].items()}))
    for tag in ('G3', 'G3_C0'):
        Lx += ['', '## %s legibility (bully | victim; rows: the excluded-slot program class over all three rotations)' % tag, '',
               '| bully, victim | excluded | n | bully read TO | victim read TO | excluded read TO | outcomes |', '|---|---|---|---|---|---|---|']
        for k, rows in res[tag].items():
            for g, s in sorted(rows.items()):
                Lx.append('| %s | %s | %d | %d | %d | %d | %s |' % (k, g, s['n'], s['bully_read_to'], s['victim_read_to'], s['e_read_to'],
                                                                 dict(sorted(s['outcomes'].items(), key=lambda x: -x[1]))))
    Lx += ['', '## G4 mixed worlds (triples with a carrier and a simulating reader, third slot any program; shares of profiles)', '',
           '| carrier x reader | n | carrier TO (regress) | reader TO | reader TO by regress | reader TO by cap |', '|---|---|---|---|---|---|']
    for k, e in sorted(res['G4'].items()):
        Lx.append('| %s | %d | %.3f (%.3f) | %.3f | %.3f | %.3f |' % (k, e['n'], e['carrier_to_share'], e['carrier_to_regress_share'], e['reader_to_share'],
                                                              e['reader_to_regress_share'], e['reader_to_cap_share']))
    Lx += ['', '"by regress" above counts the evaluator\'s identical-key regress detector, which arm T\'s nested reads never trigger (their keys '
           'differ level by level); the operational split is G4b.', '',
           '## G4b timed-out reads re-evaluated with every cap and the root fuel x20 (sample per group): still timed out = regress, '
           'completed = cap exhaustion', '',
           '| carrier x reader | timed-out profiles | sampled | reader reads: n / still TO | carrier fallback reads: n / still TO |', '|---|---|---|---|---|']
    for tag in ('G4b', 'G4b_const'):
        if tag == 'G4b_const':
            Lx += ['', 'The same with the third slot restricted to constants (the only reads are between the carrier and the reader):', '',
                   '| carrier x reader | timed-out profiles | sampled | reader reads: n / still TO | carrier fallback reads: n / still TO |', '|---|---|---|---|---|']
        for k, e in res[tag].items():
            Lx.append('| %s | %d | %d | %d / %d | %d / %d |' % (k, e['timed_out_profiles'], e['sampled'], e['reader'][0], e['reader'][1],
                                                              e['carrier'][0], e['carrier'][1]))
    Lx += ['', '## G5 first 59 programs unchanged', '', '- %s' % res['G5'], '', '## V3 C1 vs C0', '']
    v = res['V3']
    Lx.append('- profiles %d; action differences %d (without a timeout change %d); timeout differences %d; forfeit differences %d; outcome triples '
              'differing %d (of which without any carrier %d); first-59 block identical: %s' % (
                  v['profiles'], v['action_diff'], v['action_diff_without_nto_change'], v['nto_diff'], v['fo_diff'], v['outcome_triples_diff'],
                  v['outcome_triples_diff_without_carrier'], v['first59_identical']))
    for k, r in sorted(v['by_program'].items(), key=lambda x: -x[1]['code'])[:40]:
        Lx.append('  - %s: %s' % (k, r))
    return Lx


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
