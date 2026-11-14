"""Gates of queue 78 (spec specs/2026-11-14-patient-accepters.md, section Programs): V2, the action gate, the reference check, the
mutual-read gate and the nested-read report.

    python3 src/patient_accepter_validate.py OUT.json [OUT.md]

 V2    the 55 x 55 x 55 block of the extended table equals queue 76's (bully_resist.TabsBR) on code, steps, timeouts, forfeits and the
       joint code, and its 31-block equals T+'s.
 ACT   for every R variant and every (next, prev) of the 59-program catalogue: R's read evaluated in R's own frame (value: a code, TO, or
       other); R's action equals its 1/3 constant's (C3 for Rn*, C0 for Rp*) wherever the read does not return an offer of 1/2 (a timed-out
       read is no offer for `n`, an offer for `y`) and names the read partner at 1/2 wherever it does.  Read status and A_f charges are
       tabulated beside the actions (they differ from the constant's wherever the read times out).
 REF   R against an explicit reference built from the partner's own table (queue 76's REF rule: conclusive at <= 395 steps, timeout above 405).
 MUT   the mutual-read gate: R (matched orientation, victim seat) with each family in the read slot (O, F singles, F twos, F2, P, Q, bullies,
       the 1/2 constant naming R, other constants, R itself) and each family in the current slot: read completes / times out, R's action,
       charges; and the decisive question: in the unequal configuration (bully, R as victim, X in the excluded slot), which X turn the
       island fair (does O or F trigger R, or only non-reading 1/2 constants?).
 NEST  the (R u O u F u B)^3 sub-table: timeouts, forfeits, A_f charges, outcome classes; R with R, R with O, R with a bully in the read slot.
"""
import os, sys, json, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import patient_accepter as PA
import bully_resist as BR
import tplus as TP
import migration_window as MW
import lt_code as L

CAP_OK, CAP_TO = 395, 405
PFAIL = 0.1
CLS = ['F', 'U', 'G', 'W', 'D']


def fam_group(tb, i):
    n, f = tb.names[i], tb.fam[i]
    if f == 'const':
        return n
    if f == 'prudent':
        return 'Pz' if n[2] == 'z' else 'Po'
    return {'single': 'Fs', 'two': 'Ft', 'single2': 'F2', 'prudent_a': 'Q', 'opener': 'O', 'bully': 'B', 'exploit': 'X', 'junk_f': 'J', 'junk_r': 'J',
            'accepter': 'R'}[f]


def ref_read(tb, j, nxt, prv):
    st = int(tb.steps[j, nxt, prv])
    if st <= CAP_OK:
        return int(tb.code[j, nxt, prv]) if not tb.fo[j, nxt, prv] else None
    if st > CAP_TO:
        return 'TO'
    return None


def ref_accepter(tb, me, nxt, prv, dirn, to):
    if dirn == 'n':
        r = ref_read(tb, nxt, prv, me); accv, go, dflt = 4, 1, 3
    else:
        r = ref_read(tb, prv, me, nxt); accv, go, dflt = 1, 4, 0
    if r is None:
        return None
    return go if (r == accv or (to == 'y' and r == 'TO')) else dflt


def main(out, md=None):
    t0 = time.time()
    cache = os.path.join(ROOT, 'runs', '_cache')
    tb = PA.TabsPA(cache_dir=cache)
    ob = BR.TabsBR(cache_dir=cache)
    tp = TP.TabsPlus(cache_dir=cache)
    names = tb.names; idx = {x: i for i, x in enumerate(names)}; K = tb.K
    res = {}
    n = 55
    res['V2'] = {a: bool((getattr(tb, a)[:n, :n, :n] == getattr(ob, a)).all()) for a in ('code', 'steps', 'nto', 'fo', 'JT')}
    res['V2_tplus'] = {a: bool((getattr(tb, a)[:31, :31, :31] == getattr(tp, a)).all()) for a in ('code', 'steps', 'nto', 'fo', 'JT')}
    cat = tb.cat
    # ---- ACT: R's read evaluated in R's frame
    act = {}
    readv = {}
    for nm in PA.NAMES_R:
        me = idx[nm]; d, to = nm[1], nm[2]
        cst = idx[PA.DEFAULT_CONST[nm]]
        go = 1 if d == 'n' else 4; accv = 4 if d == 'n' else 1
        cnt = dict(profiles=0, read_code=0, read_TO=0, read_other=0, offer=0, action_ok=0, action_bad=0, equal_const_action=0,
                   equal_const_charge=0, charge_differs_TO=0, forfeit=0)
        bad = []
        rv = np.empty((K, K), object)
        for b in range(K):
            for c in range(K):
                v, st, nto = L.run_big(PA.read_value, None, cat.terms[me], d, cat.terms[b], cat.terms[c])
                if isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8:
                    status = 'code'; cnt['read_code'] += 1
                elif v == 'TO':
                    status = 'TO'; cnt['read_TO'] += 1
                else:
                    status = 'other'; cnt['read_other'] += 1
                rv[b, c] = v if status != 'other' else repr(v)
                offer = (status == 'code' and v == accv) or (to == 'y' and status == 'TO')
                cnt['offer'] += offer
                expect = go if offer else int(tb.code[cst, b, c])
                got = int(tb.code[me, b, c])
                cnt['profiles'] += 1
                cnt['forfeit'] += int(tb.fo[me, b, c])
                if got == expect:
                    cnt['action_ok'] += 1
                else:
                    cnt['action_bad'] += 1
                    if len(bad) < 8:
                        bad.append((names[b], names[c], str(v), expect, got))
                if not offer and got == int(tb.code[cst, b, c]):
                    cnt['equal_const_action'] += 1
                    if int(tb.nto[me, b, c]) == 0 and int(tb.fo[me, b, c]) == 0:
                        cnt['equal_const_charge'] += 1
                    elif status == 'TO':
                        cnt['charge_differs_TO'] += 1
        cnt['examples_bad'] = bad
        act[nm] = cnt
        readv[nm] = rv
    res['ACT'] = act
    # ---- REF
    ref = {}
    for nm in PA.NAMES_R:
        me = idx[nm]
        agree = dis = amb = 0; bad = []
        for j in range(K):
            for k in range(K):
                r = ref_accepter(tb, me, j, k, nm[1], nm[2])
                got = int(tb.code[me, j, k])
                if r is None or tb.fo[me, j, k]:
                    amb += 1
                elif r == got:
                    agree += 1
                else:
                    dis += 1
                    if len(bad) < 6:
                        bad.append((names[j], names[k], r, got))
        ref[nm] = dict(agree=agree, disagree=dis, ambiguous_or_forfeit=amb, examples=bad)
    res['REF'] = ref
    # ---- MUT: R in its matched orientation with each family in the read slot and the current slot
    groups = {}
    for i in range(K):
        groups.setdefault(fam_group(tb, i), []).append(i)
    mut = {}
    for nm in PA.NAMES_R:
        me = idx[nm]; d = nm[1]
        tab = {}
        for gr, ids_r in groups.items():               # family in the read slot
            for gc, ids_c in groups.items():           # family in the current slot
                st = dict(n=0, read_code=0, read_TO=0, offer_read=0, plays_half_to_read=0, plays_third_to_current=0, other_action=0, nto_sum=0, fo=0)
                for x in ids_r:
                    for y in ids_c:
                        b, c = (x, y) if d == 'n' else (y, x)
                        v = readv[nm][b, c]
                        st['n'] += 1
                        if v == 'TO':
                            st['read_TO'] += 1
                        elif isinstance(v, int):
                            st['read_code'] += 1
                            st['offer_read'] += int(v == (4 if d == 'n' else 1))
                        a = int(tb.code[me, b, c])
                        if a == (1 if d == 'n' else 4):
                            st['plays_half_to_read'] += 1
                        elif a == (3 if d == 'n' else 0):
                            st['plays_third_to_current'] += 1
                        else:
                            st['other_action'] += 1
                        st['nto_sum'] += int(tb.nto[me, b, c]); st['fo'] += int(tb.fo[me, b, c])
                st['mean_charge'] = PFAIL * (st['nto_sum'] + st['fo']) / st['n']
                tab['%s|%s' % (gr, gc)] = st
        mut[nm] = tab
    res['MUT'] = mut
    # ---- the decisive question: unequal island (bully on 2/3, victim R in its matched orientation, X in the excluded slot)
    OUT = tb.VEC[tb.JT]
    trig = {}
    rows = []
    for bn in ('Bn', 'Bp'):
        for nm in PA.NAMES_R:
            for x in range(K):
                for rot in range(3):
                    # victim R in slot v; bully in v-1 (prev of R) for Rn* (R reads next = e), in v+1 for Rp*
                    v = rot
                    if nm[1] == 'n':
                        sb, se = (v - 1) % 3, (v + 1) % 3
                    else:
                        sb, se = (v + 1) % 3, (v - 1) % 3
                    t = [0, 0, 0]; t[v] = idx[nm]; t[sb] = idx[bn]; t[se] = x
                    o = int(OUT[tuple(t)]); sh = MW.X[o]
                    # the same triple with R replaced by its 1/3 constant: is it the bully-held unequal island?
                    t0_ = list(t); t0_[v] = idx[PA.DEFAULT_CONST[nm]]
                    o0 = int(OUT[tuple(t0_)]); sh0 = MW.X[o0]
                    base_unequal = (MW.CATMAP[o0] == 1 and sh0[sb] == 4 and sh0[v] == 2)
                    rows.append(dict(bully=bn, R=nm, x=names[x], xg=fam_group(tb, x), rot=rot, base_unequal=bool(base_unequal),
                                     cls=CLS[int(MW.CATMAP[o])], R_share=int(sh[v]), x_share=int(sh[se]), b_share=int(sh[sb]),
                                     R_nto=int(tb.nto[t[0], t[1], t[2]] if False else tb.NTO[t[0], t[1], t[2], v]),
                                     x_nto=int(tb.NTO[t[0], t[1], t[2], se])))
    summ = {}
    for r in rows:
        if not r['base_unequal']:
            continue
        k = '%s|%s' % (r['R'], r['xg'])
        s = summ.setdefault(k, dict(n=0, fair_R_x=0, fair_b_x=0, fair_R_b=0, unequal=0, other=0, other_cls={}, R_TO=0, members=set()))
        s['n'] += 1
        if r['cls'] == 'F' and r['R_share'] > 0 and r['x_share'] > 0:
            s['fair_R_x'] += 1; s['members'].add(r['x'])
        elif r['cls'] == 'F' and r['b_share'] > 0 and r['x_share'] > 0:
            s['fair_b_x'] += 1
        elif r['cls'] == 'F' and r['b_share'] > 0 and r['R_share'] > 0:
            s['fair_R_b'] += 1
        elif r['cls'] == 'U':
            s['unequal'] += 1
        else:
            s['other'] += 1; s['other_cls'][r['cls']] = s['other_cls'].get(r['cls'], 0) + 1
        s['R_TO'] += int(r['R_nto'] > 0)
    for s in summ.values():
        s['members'] = sorted(s['members'])
    trig['by_R_and_excluded_family'] = summ
    trig['triggers_n_variants'] = sorted({r['x'] for r in rows if r['base_unequal'] and r['R'][2] == 'n' and r['cls'] == 'F' and r['R_share'] > 0 and r['x_share'] > 0})
    trig['triggers_y_variants'] = sorted({r['x'] for r in rows if r['base_unequal'] and r['R'][2] == 'y' and r['cls'] == 'F' and r['R_share'] > 0 and r['x_share'] > 0})
    res['TRIGGER'] = trig
    # ---- NEST: (R u O u F u B)^3
    S = [i for i in range(K) if tb.fam[i] in ('accepter', 'opener', 'single', 'two', 'bully')]
    nest = {}
    for a, b, c in itertools.product(S, S, S):
        ga, gb, gc = fam_group(tb, a), fam_group(tb, b), fam_group(tb, c)
        key = '|'.join(sorted([ga, gb, gc]))
        st = nest.setdefault(key, dict(n=0, nto=0, fo=0, charge=0.0, cls=[0] * 5, profiles_with_TO=0))
        nto = tb.NTO[a, b, c]; fo = tb.FO[a, b, c]
        st['n'] += 1; st['nto'] += int(nto.sum()); st['fo'] += int(fo.sum()); st['charge'] += PFAIL * float(nto.sum() + fo.sum())
        st['cls'][int(MW.CATMAP[int(OUT[a, b, c])])] += 1
        st['profiles_with_TO'] += int(nto.sum() > 0)
    for st in nest.values():
        st['mean_charge_per_profile'] = st['charge'] / st['n']; st['share_TO'] = st['profiles_with_TO'] / st['n']
    res['NEST'] = nest
    # R with R, R with O, R with a bully in the read slot: pair-level summaries from MUT
    res['NEST_focus'] = {nm: {k: mut[nm][k] for k in mut[nm] if k.split('|')[0] in ('R', 'O', 'B', 'Fs', 'Ft')} for nm in PA.NAMES_R}
    res['max_steps'] = int(tb.steps.max())
    res['wall'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'), indent=1, default=str)
    if md:
        open(md, 'w').write('\n'.join(report_md(res)) + '\n')
    return res


def report_md(res):
    Lx = ['# Queue 78 gates (src/patient_accepter_validate.py)', '']
    Lx.append('V2 (first 55 programs equal queue 76): %s; T+ block: %s' % (res['V2'], res['V2_tplus']))
    Lx.append('')
    Lx.append('| R | profiles | read code | read TO | offers | action = rule | action != rule | no-offer profiles with the constant\'s action | ... and its charge | ... charge differs (TO) |')
    Lx.append('|---|---|---|---|---|---|---|---|---|---|')
    for nm, c in res['ACT'].items():
        Lx.append('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d |' % (nm, c['profiles'], c['read_code'], c['read_TO'], c['offer'], c['action_ok'], c['action_bad'],
                                                                     c['equal_const_action'], c['equal_const_charge'], c['charge_differs_TO']))
    Lx.append('')
    Lx.append('REF: ' + '; '.join('%s agree %d disagree %d ambiguous %d' % (k, v['agree'], v['disagree'], v['ambiguous_or_forfeit']) for k, v in res['REF'].items()))
    Lx.append('')
    Lx.append('Mutual-read gate (R in its matched victim seat; read slot family | current slot family): read completes / times out, R names the read slot at 1/2, R names the current slot at 1/3')
    Lx.append('')
    for nm in ('Rnn', 'Rny'):
        Lx.append('%s:' % nm)
        Lx.append('')
        Lx.append('| read slot | current slot | n | read code | read TO | offers read | R -> read 1/2 | R -> current 1/3 | mean charge |')
        Lx.append('|---|---|---|---|---|---|---|---|---|')
        for k, st in sorted(res['MUT'][nm].items()):
            gr, gc = k.split('|')
            if gc not in ('B', 'C3', 'C0', 'C8', 'R', 'O', 'Fs'):
                continue
            if gr not in ('O', 'Fs', 'Ft', 'F2', 'Pz', 'Po', 'Q', 'B', 'C4', 'C1', 'C8', 'R', 'X'):
                continue
            Lx.append('| %s | %s | %d | %d | %d | %d | %d | %d | %.3f |' % (gr, gc, st['n'], st['read_code'], st['read_TO'], st['offer_read'], st['plays_half_to_read'],
                                                                      st['plays_third_to_current'], st['mean_charge']))
        Lx.append('')
    Lx.append('Who turns a bully-held unequal island fair when R is the victim (X in the excluded slot; base = the same triple with R\'s 1/3 constant is unequal, bully on 2/3):')
    Lx.append('')
    Lx.append('| R | excluded family | triples | fair (R, X) | fair (bully, X) | fair (R, bully) | still unequal | other (classes) | R read timed out |')
    Lx.append('|---|---|---|---|---|---|---|---|---|')
    for k, s in sorted(res['TRIGGER']['by_R_and_excluded_family'].items()):
        R_, g = k.split('|')
        Lx.append('| %s | %s | %d | %d | %d | %d | %d | %d %s | %d |' % (R_, g, s['n'], s['fair_R_x'], s['fair_b_x'], s['fair_R_b'], s['unequal'], s['other'], s['other_cls'], s['R_TO']))
    Lx.append('')
    Lx.append('Triggers (n variants): %s' % res['TRIGGER']['triggers_n_variants'])
    Lx.append('Triggers (y variants): %s' % res['TRIGGER']['triggers_y_variants'])
    Lx.append('')
    Lx.append('Nested reads over (R u O u F u B)^3 (unordered family multiset): profiles, share with a timeout, mean A_f charge per profile (all three slots), outcome classes F/U/G/W/D')
    Lx.append('')
    Lx.append('| families | profiles | share with TO | mean charge | F | U | G | W | D |')
    Lx.append('|---|---|---|---|---|---|---|---|---|')
    for k, st in sorted(res['NEST'].items()):
        Lx.append('| %s | %d | %.3f | %.3f | %s |' % (k, st['n'], st['share_TO'], st['mean_charge_per_profile'], ' | '.join(str(x) for x in st['cls'])))
    return Lx


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
