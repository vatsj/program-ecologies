"""Step-1 gates of queue 76 (spec specs/2026-11-08-bully-resistance.md): V2 and the behavioural validation of P, Q, O.

    python3 src/bully_resist_validate.py OUT.json

 V2   the 31 x 31 x 31 block of the extended table equals T+'s (queue 75) table; the same for the stored cap values.
 REF  P, Q and O against an explicit reference implementation built from the *table of the partner*: a read of partner j in a
      profile is conclusive when j's standalone root run completes within 395 steps (value = its code) and times out when it
      needs more than 405 steps; profiles in between are reported as ambiguous, not scored.
 BULLY P_z / P_o / Q: the actions on the 29 x 29 probe table (partners the 27 library programs + Bn, Bp): refusals of Bn / Bp,
      acceptance of fair readers and the 1/2 constants toward P, forfeits and charges.
 OPEN  O offers 1/2 to the 1/3-holder on every unequal-pair profile (j names k at 2/3 and k names j at 1/3), constants as j, k.
 NEST  the full (P u O u F u B)^3 sub-table: read timeouts, forfeits, A_f charges, self- and mutual compatibility.
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist as BR
import tplus as TP
import migration_window as MW

CAP_OK, CAP_TO = 395, 405
PFAIL = 0.1
TO = 'TO'


def read(tb, j, nxt, prv):
    """what the read of partner j (with j's next = nxt, prev = prv) returns: code, 'TO', or None (ambiguous)."""
    st = int(tb.steps[j, nxt, prv])
    if st <= CAP_OK:
        return int(tb.code[j, nxt, prv]) if not tb.fo[j, nxt, prv] else None
    if st > CAP_TO:
        return TO
    return None


def ref_prudent(tb, me, nxt, prv, dirn, fb, to, lenient):
    """reference action of the prudent reader `me` (index) with next nxt, prev prv; None when ambiguous."""
    C3, C0 = tb.names.index('C3'), tb.names.index('C0')
    if dirn == 'n':
        r1 = read(tb, nxt, prv, me); q = read(tb, nxt, C3, me); go, other, ex, accv = 1, 4, 2, 4
    else:
        r1 = read(tb, prv, me, nxt); q = read(tb, prv, me, C0); go, other, ex, accv = 4, 1, 5, 1
    f = {'o': other, 'z': 8}[fb]
    if r1 is None:
        return None
    acc = (r1 == accv) or (to == 'y' and r1 == TO)
    if not acc:
        return f
    if q is None:
        return None
    bad = (q == ex) if lenient else (q == ex or q == TO)
    return f if bad else go


def ref_opener(tb, me, nxt, prv, first, fb, to):
    a = read(tb, nxt, prv, me); b = read(tb, prv, me, nxt)
    if a is None or b is None:
        return None
    if a == 2 and b == 3:
        return 4
    if b == 5 and a == 0:
        return 1
    g1 = 1 if first == 'n' else 4
    g2 = 4 if first == 'n' else 1
    f = {'f': g1, 'z': 8}[fb]
    acc = lambda v, d: (v == (4 if d == 'n' else 1)) or (to == 'y' and v == TO)
    va, vb = (a, b) if first == 'n' else (b, a)
    d1, d2 = ('n', 'p') if first == 'n' else ('p', 'n')
    if acc(va, d1):
        return g1
    if acc(vb, d2):
        return g2
    return f


def main(out):
    t0 = time.time()
    cache = os.path.join(ROOT, 'runs', '_cache')
    tb = BR.TabsBR(cache_dir=cache)
    tp = TP.TabsPlus(cache_dir=cache)
    res = {}
    # ---- V2
    n = 31
    res['V2'] = dict(code=bool((tb.code[:n, :n, :n] == tp.code).all()), steps=bool((tb.steps[:n, :n, :n] == tp.steps).all()),
                     nto=bool((tb.nto[:n, :n, :n] == tp.nto).all()), fo=bool((tb.fo[:n, :n, :n] == tp.fo).all()),
                     jt=bool((tb.JT[:n, :n, :n] == tp.JT).all()))
    names = tb.names; idx = {x: i for i, x in enumerate(names)}
    K = tb.K
    # ---- REF
    ref = {}
    for nm, fm in zip(names, tb.fam):
        if fm not in ('prudent', 'prudent_a', 'opener'):
            continue
        me = idx[nm]
        agree = dis = amb = 0; bad = []
        for j in range(K):
            for k in range(K):
                if nm[0] in 'PQ':
                    r = ref_prudent(tb, me, j, k, nm[1], nm[2], nm[3], nm[0] == 'Q')
                else:
                    r = ref_opener(tb, me, j, k, nm[1], nm[2], nm[3])
                got = int(tb.code[me, j, k])
                if tb.fo[me, j, k]:
                    amb += 1; continue             # forfeit (root fuel): reference does not model it
                if r is None:
                    amb += 1
                elif r == got:
                    agree += 1
                else:
                    dis += 1
                    if len(bad) < 6:
                        bad.append((names[j], names[k], r, got))
        ref[nm] = dict(agree=agree, disagree=dis, ambiguous_or_forfeit=amb, examples=bad)
    res['REF'] = ref
    # ---- BULLY on the 29 x 29 probe table
    pr = {}
    B = [idx['Bn'], idx['Bp']]
    fairreaders = [i for i in range(29) if tb.fam[i] in ('single', 'two')]
    for nm, fm in zip(names, tb.fam):
        if fm not in ('prudent', 'prudent_a'):
            continue
        me = idx[nm]; dirn = nm[1]
        go = 1 if dirn == 'n' else 4
        jslot = 0 if dirn == 'n' else 1                # partner index axis in code[me, nxt, prv]
        rows = {}
        for lab, js in (('bullies', B), ('fair_readers', fairreaders), ('half_constants', [idx['C4'] if dirn == 'n' else idx['C1']])):
            acc = nacc = fo = tot = 0
            for j in js:
                for k in range(29):
                    nx, pv = (j, k) if dirn == 'n' else (k, j)
                    tot += 1
                    if tb.fo[me, nx, pv]:
                        fo += 1; continue
                    if int(tb.code[me, nx, pv]) == go:
                        acc += 1
                    else:
                        nacc += 1
            rows[lab] = dict(profiles=tot, accepts=acc, refuses=nacc, forfeits=fo)
        pr[nm] = rows
    res['BULLY'] = pr
    # fair readers: acceptance only when the cooperation read says the reader names P at 1/2
    fr = {}
    for nm, fm in zip(names, tb.fam):
        if fm != 'prudent':
            continue
        me = idx[nm]; dirn = nm[1]; go = 1 if dirn == 'n' else 4; accv = 4 if dirn == 'n' else 1
        a_naming = a_acc = refused_naming = 0
        for j in fairreaders + [idx['C4'] if dirn == 'n' else idx['C1']]:
            for k in range(29):
                nx, pv = (j, k) if dirn == 'n' else (k, j)
                if tb.fo[me, nx, pv]:
                    continue
                names_me = read(tb, j, k, me) if dirn == 'n' else read(tb, j, me, k)
                if names_me == accv:
                    a_naming += 1
                    if int(tb.code[me, nx, pv]) == go:
                        a_acc += 1
                    else:
                        refused_naming += 1
        fr[nm] = dict(profiles_where_partner_names_me_at_half=a_naming, accepted=a_acc, refused=refused_naming)
    res['FAIR_ACCEPT'] = fr
    # ---- OPEN: on every unequal-pair profile (j names k at 2/3, k names j at 1/3) O offers 1/2 to the 1/3-holder
    op = {}
    CC = [idx['C%d' % c] for c in range(9)]
    for nm, fm in zip(names, tb.fam):
        if fm != 'opener':
            continue
        me = idx[nm]
        n_prof = ok = 0; bad = []
        for a in range(K):
            for b in range(K):
                nx, pv = a, b                           # j = next, k = prev
                if tb.fo[me, nx, pv]:
                    continue
                av = read(tb, nx, pv, me); bv = read(tb, pv, me, nx)
                if av is None or bv is None:
                    continue
                if av == 2 and bv == 3:
                    n_prof += 1
                    if int(tb.code[me, nx, pv]) == 4:
                        ok += 1
                    elif len(bad) < 5:
                        bad.append((names[a], names[b], int(tb.code[me, nx, pv])))
                elif bv == 5 and av == 0:
                    n_prof += 1
                    if int(tb.code[me, nx, pv]) == 1:
                        ok += 1
                    elif len(bad) < 5:
                        bad.append((names[a], names[b], int(tb.code[me, nx, pv])))
        # constants as j and k (exact, no reads needed): j = C2-type names its next at 2/3 ...
        cc = {}
        for cj, ck, exp in (('C2', 'C3', 4), ('C0', 'C5', 1)):
            cc['%s,%s' % (cj, ck)] = [int(tb.code[me, idx[cj], idx[ck]]), exp]
        op[nm] = dict(unequal_profiles=n_prof, offered_half=ok, examples_not=bad, constants=cc)
    res['OPEN'] = op
    # ---- NEST: the (P u O u F u B)^3 sub-table
    sub = [i for i in range(K) if tb.fam[i] in ('prudent', 'prudent_a', 'opener', 'single', 'two', 'bully')]
    S = np.array(sub)
    ix = np.ix_(S, S, S)
    nto = tb.nto[ix]; fo = tb.fo[ix]; stp = tb.steps[ix]
    byfam = {}
    for fm in ('prudent', 'prudent_a', 'opener', 'single', 'two', 'bully'):
        slot0 = [t for t, i in enumerate(sub) if tb.fam[i] == fm]
        c = nto[slot0].astype(float) + fo[slot0]
        byfam[fm] = dict(mean_read_timeouts=float(nto[slot0].mean()), mean_forfeits=float(fo[slot0].mean()),
                         mean_Af_charge=float((PFAIL * c).mean()), forfeit_profiles=int(fo[slot0].sum()),
                         max_steps=int(stp[slot0].max()), profiles=int(nto[slot0].size))
    res['NEST_by_family_as_slot0'] = byfam
    res['NEST_total'] = dict(profiles=int(fo.size), forfeit_profiles=int(fo.sum()), max_steps=int(stp.max()))
    # compatibility: P_z with P_z, with F, with 1/2 constants; O with O.  A pair "forms" when a slot-0 program and a slot-1
    # program name each other at 1/2 (outcome = fair pair on slots 0,1), over the third slot in a set.
    X = MW.X
    JT, VEC = tb.JT, tb.VEC
    T = MW.T

    def pairs01(a, b, thirds):
        n = fm_ = 0
        for c in thirds:
            o = int(VEC[JT[a, b, c]])
            sh = X[o]
            if T.cat[o] == 'fair' and sh[0] > 0 and sh[1] > 0:
                n += 1
            fm_ += 1
        return n, fm_

    sets = dict(Pz=[idx[x] for x in BR.NAMES_P if x[2] == 'z'], Po=[idx[x] for x in BR.NAMES_P if x[2] == 'o'],
                Q=[idx[x] for x in BR.NAMES_Q], O=[idx[x] for x in BR.NAMES_O],
                F=[i for i in range(29) if tb.fam[i] in ('single', 'two')],
                half=[idx['C1'], idx['C4']], consts=CC)
    thirds_all = list(range(29))
    comp = {}
    for A, Bn_ in (('Pz', 'Pz'), ('Pz', 'F'), ('Pz', 'half'), ('F', 'Pz'), ('Po', 'Po'), ('Po', 'F'), ('Q', 'Q'), ('Q', 'F'),
                   ('O', 'O'), ('O', 'F'), ('F', 'F'), ('Pz', 'Bn'), ('Pz', 'Bp')):
        sa = sets[A]; sb = sets[Bn_] if Bn_ in sets else [idx[Bn_]]
        tot = n = 0
        for a in sa:
            for b in sb:
                x, y = pairs01(a, b, thirds_all)
                n += x; tot += y
        comp['%s x %s (slots 0,1; thirds over the 29)' % (A, Bn_)] = dict(fair_pair_on_01=n, profiles=tot, share=round(n / max(tot, 1), 4))
    res['COMPAT'] = comp
    res['wall'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res['V2']), 'wall', res['wall'])
    return res


if __name__ == '__main__':
    main(sys.argv[1])
