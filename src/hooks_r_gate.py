"""The gate of hooks Part R (notes/hooks-r.md §2): the gene-site check at the term level and in the host replay.

  (g1) conservativeness: sampled stored checks have the same value and step count under the hook library;
  (g2) the battery: hooked carriers with interacting fills against opponents; the term's CHKH, the host replay's
       CHKH and the host-side conflict rule agree on every gene site, and the actual play follows them;
  (g3) soundness: every accepted certificate (CHKS at the partner, ⌜C⌝, ⌜D⌝ and self roots) states the actual play;
       a production C script stops validating after a D fill covers the partner (re-checking after a write);
  (g4) costs: steps of a gene-site check by list length and scope (the cost model's inputs).
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import carrier_populations as CP
import detectors as DT
import hooks_r as H

K, V = H.K, H.V
A_S = lambda nm: ('A', nm)


def at(p, q, a):
    return ('A', (0, p, q, a))


PROGS = {
    'HC': ('H', 1, 'C'),
    'HD': ('H', 1, 'D'),
    'FBh': ('if', at('them', 'me', 'C'), ('H', 1, 'C'), ('D',)),               # FairBot with a hooked C branch
    'FBh2': ('if', at('them', 'me', 'C'), ('H', 1, 'C'), ('H', 2, 'D')),        # two gene sites
    'PBh': ('if', at('them', 'me', 'C'), ('if', at('them', 'D', 'D'), ('H', 1, 'C'), ('D',)), ('D',)),
    'DETh': ('if', at('them', 'them', 'D'), ('D',), ('H', 1, 'C')),
}
P_PROGS = {
    'FB': ('if', at('them', 'me', 'C'), ('C',), ('D',)),
    'PB': ('if', at('them', 'me', 'C'), ('if', at('them', 'D', 'D'), ('C',), ('D',)), ('D',)),
    'CB': ('C',),
    'DB': ('D',),
}


class Bare:
    """Bare sources of the battery's programs (the marked hooked body)."""

    def __init__(self):
        self.enc = {}

    def __call__(self, name):
        return self.enc[name]


def make_prog(sx, fills, bare, cseq=(), dseq=(), marker='H'):
    """fills: [(tag, scope, key, act)] with spelling keys as program names (resolved by bare)."""
    ents = []
    for (t, sc, key, act) in fills:
        if sc in (H.SC_HIST, H.SC_SRC):
            kd = H.SELF_TOK if key == 'SELF' else bare(key)
        elif sc in (H.SC_NONE, H.SC_ROLE):
            kd = 0
        else:
            kd = int(key)
        ents.append((act, H.fill_script(t, sc, kd)))
    return H.hooked_carrier(sx, cseq, dseq, ents, marker)


def resolve_host(fills, tag, kind, opp_name, opp_cls, own_name, recency=False):
    """The host-side conflict rule on named keys (kind: 0 C, 1 D, 2 self, 3 other)."""
    fl = []
    for (t, sc, key, act) in fills:
        k = key
        if sc in (H.SC_HIST, H.SC_SRC):
            k = H.SELF_KEY if key == 'SELF' else key
        fl.append((t, sc, k, 1 if act == 'C' else 0, 0))
    w = H.winner([(t, sc, (k if not isinstance(k, str) else hash(k)), a, s) for (t, sc, k, a, s) in fl], tag, kind,
                 hash(opp_name) if opp_name is not None else -1, opp_cls, hash(own_name), recency=recency)
    if w < 0: return None
    return 'C' if fl[w][3] == 1 else 'D'


def term_hook(x, m, a, tag):
    """The gene-site check by the term (the library's CHKH core under capk)."""
    n = L.LIBIDX['CCH']
    arg = H.hook_arg(V, ('quote', x), ('quote', m), a, K, tag)
    v, steps = L.evaluate(('capk', C.N(V), ('lib', n), arg))
    return ('T' if v == 'T' else 'F' if v == 'F' else 'TO'), steps


def gate(log=print):
    t0 = time.time()
    out = {}
    H.install_hook_library(recency=False)
    hh = H.HostH()
    bare = Bare()
    names = list(PROGS) + list(P_PROGS)

    def body_of(nm):
        return PROGS[nm] if nm in PROGS else P_PROGS[nm]
    for nm in names:
        bare.enc[nm] = L.canon_term(DT.bare(make_prog(body_of(nm), [], bare)))
    # ---- (g2) battery: fill lists on hooked programs against opponents
    cases = [
        ('HD', [(1, H.SC_SRC, 'FB', 'C')]),
        ('HD', [(1, H.SC_SRC, 'FB', 'C'), (1, H.SC_NONE, 0, 'D')]),
        ('HC', [(1, H.SC_NONE, 0, 'D'), (1, H.SC_SRC, 'FB', 'C')]),
        ('HC', [(1, H.SC_BEH, 1, 'D'), (1, H.SC_HIST, 'FB', 'C')]),
        ('HC', [(1, H.SC_HIST, 'FB', 'C'), (1, H.SC_BEH, 1, 'D')]),
        ('HC', [(1, H.SC_NONE, 0, 'D'), (1, H.SC_NONE, 0, 'C')]),
        ('HD', [(1, H.SC_SRC, 'SELF', 'C')]),
        ('HD', [(1, H.SC_SRC, 'SELF', 'C'), (1, H.SC_SRC, 'HD', 'D')]),
        ('HC', [(1, H.SC_ROOT, H.RK_D, 'D')]),
        ('HC', [(1, H.SC_ROOT, H.RK_SELF, 'D'), (1, H.SC_ROOT, H.RK_C, 'D')]),
        ('HD', [(1, H.SC_ROOT, H.RK_OTHER, 'C'), (1, H.SC_ROLE, 0, 'D')]),
        ('HD', [(1, H.SC_BEH, 0, 'C')]),
        ('HD', [(1, H.SC_BEH, 1, 'C'), (1, H.SC_BEH, 0, 'C')]),
        ('FBh', [(1, H.SC_HIST, 'PB', 'D')]),
        ('FBh', [(1, H.SC_ROOT, H.RK_D, 'D'), (1, H.SC_NONE, 0, 'D'), (1, H.SC_SRC, 'PB', 'C')]),
        ('FBh2', [(1, H.SC_NONE, 0, 'D'), (2, H.SC_SRC, 'FB', 'C'), (2, H.SC_ROOT, H.RK_D, 'D')]),
        ('FBh2', [(2, H.SC_BEH, 5, 'C'), (1, H.SC_HIST, 'CB', 'D')]),
        ('PBh', [(1, H.SC_SRC, 'DB', 'C'), (1, H.SC_BEH, 1, 'D')]),
        ('DETh', [(1, H.SC_HIST, 'FB', 'D'), (1, H.SC_ROLE, 0, 'C')]),
        ('HC', [(2, H.SC_NONE, 0, 'D')]),                                    # a fill for a tag the program lacks
        ('HC', [(1, H.SC_SRC, 'PB', 'D')]),                                  # a key that holds nowhere below
    ]
    prod = C.Producer(host=H.HostHE())

    def produced(sx, fl):
        """A program with milestone 4's two-pass production (D step against ⌜D⌝, then C scripts against the
        listed FairBot and PrudentBot with their own lists), its fills in place during production."""
        x0 = make_prog(sx, fl, bare)
        sD = prod.produce(0, x0, L.PROG_D, 'D', K, V)
        ds = [sD] if sD else []
        x1 = make_prog(sx, fl, bare, dseq=ds)
        cs = []
        for o in probes:
            s = prod.produce(0, x1, o, 'C', K, V)
            if s is not None and s not in cs: cs.append(s)
        return make_prog(sx, fl, bare, cseq=cs, dseq=ds)
    probes = []
    for nm in ('FB', 'PB'):
        probes.append(make_prog(P_PROGS[nm], [], bare))
    probes = [produced(P_PROGS['FB'], []), produced(P_PROGS['PB'], [])]
    opps = {nm: produced(body_of(nm), []) for nm in names}
    rows = []
    n_disagree = 0
    n_false = 0
    n_acc = 0
    cls_cache = {}

    def cls_of(prog):
        k = id(prog)
        if k not in cls_cache: cls_cache[k] = hh.bclass(prog, V, K)
        return cls_cache[k]
    for ci, (xn, fl) in enumerate(cases):
        x = produced(PROGS[xn], fl)
        targets = [(nm, opps[nm]) for nm in names] + [('^C', L.PROG_C), ('^D', L.PROG_D), ('self', x)]
        tags = sorted(set(t for t, _ in H.hook_leaves(PROGS[xn])))
        for on, o in targets:
            kind = 0 if on == '^C' else 1 if on == '^D' else 2 if on == 'self' else 3
            oc = 0 if on in ('^C', '^D') else cls_of(o)
            for tag in tags:
                exp = resolve_host(fl, tag, kind, None if kind < 2 else (xn if kind == 2 else on), oc, xn)
                for a in ('C', 'D'):
                    hv = hh.hook_check(x, o, a, tag)
                    tv, steps = term_hook(x, o, a, tag)
                    ev = 'T' if exp == a else 'F'
                    ok = (hv == tv == ev)
                    if not ok: n_disagree += 1
                    rows.append((ci, xn, on, tag, a, ev, hv, tv, steps))
            # (g3) soundness of top-level certificates and the actual play
            pl = C.play(x, o, K)[0] if on != 'self' else C.play(x, x, K)[0]
            for a in ('C', 'D'):
                v = hh.check(C.ID['CHKS'], C.mk_arg(V, x, o, a, K))
                if v == 'T':
                    n_acc += 1
                    if pl != a: n_false += 1
    out['g2'] = dict(cases=len(cases), gene_site_checks=len(rows), disagreements=n_disagree)
    out['g3'] = dict(accepted=n_acc, false_atoms=n_false)
    log('g2: %d cases, %d gene-site checks (term, host, rule), %d disagreements' % (len(cases), len(rows), n_disagree))
    # ---- (g3b) re-checking after a write: FBh produces its C script against FB (no fills), then a D fill keyed to PB
    x1 = produced(PROGS['FBh'], [])
    lst = C.h_getcerts(x1)
    ents = C.uncons(lst) if lst else []
    cs = [e[1] for e in ents if e[0] == 'C']
    ds = [DT.unkey(e[1]) for e in ents if e[0] == 'D']
    x2 = make_prog(PROGS['FBh'], [(1, H.SC_HIST, 'FB', 'D')], bare, cseq=cs, dseq=ds)
    h2 = H.HostH()
    r = dict(scripts=[C.show_script(s) for s in cs],
             before_vs_FB=h2.check(C.ID['CHKS'], C.mk_arg(V, x1, opps['FB'], 'C', K)),
             after_vs_FB=h2.check(C.ID['CHKS'], C.mk_arg(V, x2, opps['FB'], 'C', K)),
             after_vs_PB=h2.check(C.ID['CHKS'], C.mk_arg(V, x2, opps['PB'], 'C', K)),
             play_before=(C.play(x1, opps['FB'], K)[0], C.play(opps['FB'], x1, K)[0]),
             play_after=(C.play(x2, opps['FB'], K)[0], C.play(opps['FB'], x2, K)[0]))
    out['g3_recheck'] = r
    log('g3: %d accepted certificates, %d false atoms; re-check after a D fill: %s' % (n_acc, n_false, r))
    # ---- forged and misplaced fills
    forg = []
    x_forge = H.hooked_carrier(PROGS['HC'], (), (), [('D', C.node(C.HYP, 0)), ('D', (H.FILL, ((2, (0, 0)),
                                                                                              C.cons([C.node(C.HYP, 0)]))))])
    forg.append(('bare Hyp and other-tag fill on HOOK(1,C)', hh.hook_check(x_forge, opps['FB'], 'D', 1),
                 C.play(x_forge, opps['FB'], K)[0]))
    p_with_fill = C.carrier(CP.body_term(P_PROGS['FB'], V, K), C.cons([('D', H.fill_script(1, 0, 0))]))
    forg.append(('a Fill entry in FairBot (no gene site)', hh.check(C.ID['CHKS'], C.mk_arg(V, p_with_fill, opps['FB'],
                                                                                             'D', K)),
                 C.play(p_with_fill, opps['FB'], K)[0]))
    out['forged'] = forg
    log('forged: %s' % forg)
    # ---- (g1) conservativeness: sampled stored checks under the base (world K key) library and the hook library
    S_ = H.statics()
    U = S_['U']
    rng = np.random.default_rng(7)
    O = np.nonzero(S_['inO'])[0]
    samp = []
    CHC, CHD = S_['CHC'], S_['CHD']
    while len(samp) < 60:
        u, v = int(rng.choice(O)), int(rng.choice(O))
        for a, CH in (('C', CHC), ('D', CHD)):
            if CH[u, v] >= 0 and u != v:
                samp.append((u, v, a))
    res = {}
    for which in ('key', 'hooks'):
        if which == 'key':
            H.leave_hook_library('key')
        else:
            H.install_hook_library(recency=False)
        L.CACHE.clear()
        vals = []
        for (u, v, a) in samp:
            tu = DT.key_term_K(U, U.units[u], 'H'); tv = DT.key_term_K(U, U.units[v], 'H')
            vals.append(C.check_value(0, V, tu, tv, a, K))
        res[which] = vals
    nd = sum(1 for x, y in zip(res['key'], res['hooks']) if x != y)
    stored_ok = sum(1 for (u, v, a), (val, st_) in zip(samp, res['hooks'])
                    if {'T': 1, 'F': 0, 'TO': 2}[val] == (CHC if a == 'C' else CHD)[u, v])
    out['g1'] = dict(sampled=len(samp), differences=nd, equal_to_stored_table=stored_ok)
    log('g1: %d sampled checks, %d value/step differences between libraries; %d equal the stored table' % (
        len(samp), nd, stored_ok))
    # ---- (g4) costs of a gene-site check by list length and scope (term steps)
    cost = {}
    for sc in range(6):
        for n in (1, 2, 4):
            key = {H.SC_NONE: 0, H.SC_ROLE: 0, H.SC_BEH: 1, H.SC_HIST: 'PB', H.SC_SRC: 'PB', H.SC_ROOT: 3}[sc]
            fl = [(1, sc, key, 'C')] * n
            x = make_prog(PROGS['HD'], fl, bare)
            tv, steps = term_hook(x, opps['FB'], 'C', 1)
            cost['%s_%d' % (H.SCOPES[sc], n)] = steps
    x = make_prog(PROGS['HD'], [], bare)
    cost['empty'] = term_hook(x, opps['FB'], 'C', 1)[1]
    out['g4_steps'] = cost
    log('g4: gene-site check steps %s' % cost)
    out['rows'] = rows
    out['time_s'] = time.time() - t0
    out['go'] = (n_disagree == 0 and n_false == 0 and nd == 0 and r['after_vs_FB'] != 'T')
    log('GATE: %s (%.0fs)' % ('GO' if out['go'] else 'NO-GO', out['time_s']))
    return out


# ------------------------------------------------------------------------------------------------ Lemma H audit
def _cont(nd):
    """A premise that continues the run (EvR* first), as opposed to one closed by Run/RunNeg/Hyp/Ax."""
    return nd[0] == C.EVS


def translate(nd, tree, a, tagdef):
    """A baked script (P skeleton over the resolved tree) -> the true hooked program's script: at the leaf a
    continuing branch reaches, a hook leaf (tag t, default a0) needs a ChkR on the gene-site call, Run on its box
    when the script's outcome a is not a0 (the hook returned T), RunNeg when it is a0.  tree: dt_leaf of the hooked
    sexpr (leaves 0 or the tag), tagdef: {leaf object id: default} via a parallel tree with defaults."""
    rule, (j, ps) = nd
    ps = C.uncons(ps)
    if rule == C.EVS:
        nxt = ps[0]
        if isinstance(tree, tuple) and not isinstance(tree[0], str) and len(tree) == 3 and not _is_leaf(tree):
            return C.node(C.EVS, j, translate(nxt, tree, a, tagdef))
        # the evaluation reaches a leaf of the tree
        if _is_leaf(tree) and tree[1] > 0:
            a0 = tree[2]
            if nxt[0] != C.AX: return nd
            if a != a0:      # the gene site returned T: ρ_T continues to the value
                hk = C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.RUN, 0))
            else:
                hk = C.node(C.CHKR, 0, C.node(C.RUNNEG, 0), C.node(C.EVS, 1, C.node(C.AX, 0)))
            return C.node(C.EVS, j, hk)
        return nd
    if rule == C.CHKR:
        p1, p2 = ps[0], ps[1]
        if _is_leaf(tree): return nd
        tT, tF = tree[1], tree[2]
        q1 = translate(p1, tT, a, tagdef) if _cont(p1) else p1
        q2 = translate(p2, tF, a, tagdef) if _cont(p2) else p2
        return C.node(C.CHKR, j, q1, q2)
    return nd


def _is_leaf(t):
    return isinstance(t, tuple) and len(t) == 3 and t[0] == 'L'


def leaf_tree(x):
    """dt with leaves ('L', tag or 0, default)."""
    if x[0] == 'H': return ('L', x[1], x[2])
    if x[0] in ('C', 'D'): return ('L', 0, x[0])
    return CP._bt(x[1], leaf_tree(x[2]), leaf_tree(x[3]))


def audit(R, n_pairs=200, seed=0, log=print):
    """Lemma H on a live run R (hooks_r.HRun): sampled pairs of distinct co-resident types, at least one hooked;
    the kernel's plays against the executed plays of the true hooked carriers (fills as Fill entries, the kernel's
    baked scripts translated), and the kernel's behaviour classes against the true host classes."""
    import hooks_r as H
    H.install_hook_library(recency=bool(R.c['recency']))
    S_ = H.statics()
    gh = S_['gh']; U = S_['U']
    rng = np.random.default_rng(seed)
    cache_bare = {}

    def bare_sp(sp):
        if sp not in cache_bare:
            cache_bare[sp] = L.canon_term(DT.bare(H.hooked_carrier(gh.sexprs[sp], (), (), [])))
        return cache_bare[sp]

    def true_carrier(k):
        sp = int(R.tsp[k]); x = gh.sexprs[sp]
        lt = leaf_tree(x)
        cs = [U.scripts[s][1] for s in R.BKC[R.tblk[k]] if s >= 0]
        ds = [U.scripts[s][1] for s in R.BKD[R.tblk[k]] if s >= 0]
        cs = [translate(s, lt, 'C', None) for s in cs]
        ds = [translate(s, lt, 'D', None) for s in ds]
        f = R.tfl[k]; fl = []
        for q in range(R.FN[f]):
            p = int(R.FP[f, q])
            t, sc, act, src, key = p & 3, (p >> 2) & 7, (p >> 5) & 1, (p >> 6) & 3, (p >> 8) - 3
            if R.inert[src, sc]: continue          # an inert fill is held but never applied: not in the true list
            kd = H.SELF_TOK if (sc == H.SC_SRC and key == H.SELF_KEY) else (
                bare_sp(key) if sc in (H.SC_HIST, H.SC_SRC) else (0 if sc <= 1 else key))
            fl.append(('C' if act == 1 else 'D', H.fill_script(t, sc, kd)))
        return H.hooked_carrier(x, cs, ds, fl)
    audit.true_carrier = true_carrier
    pairs = []
    for i in range(R.I):
        ks = R.pres[i, :R.npres[i]]
        for a_ in ks:
            for b_ in ks:
                if a_ < b_ and (R.tsp[a_] >= gh.NP or R.tsp[b_] >= gh.NP): pairs.append((int(a_), int(b_)))
    if len(pairs) > n_pairs:
        pairs = [pairs[q] for q in rng.choice(len(pairs), n_pairs, replace=False)]
    hh = H.HostH()
    n0 = C.ID['CHKS']

    def ideal_play(z, x, m):
        """The true hooked program's action on the ideal table: its run tree with every atom a host check of the
        true quotes and every gene site the host's CHKH."""
        t = leaf_tree(gh.sexprs[int(R.tsp[z])])
        while not _is_leaf(t):
            e, pp, qq, a = t[0]
            who = x if pp == 'me' else m
            opp = {'me': x, 'them': m, 'C': L.PROG_C, 'D': L.PROG_D}[qq]
            v = hh.check(n0, C.mk_arg(V, who, opp, a, K)) == 'T'
            t = t[1] if v else t[2]
        _, tag, a0 = t
        if tag == 0: return a0
        na = 'D' if a0 == 'C' else 'C'
        return na if hh.hook_check(x, m, na, tag) == 'T' else a0
    bad = []; n_ok = 0; n_cls_bad = 0; n_cls = 0; n_exec = 0; n_exec_bad = 0
    terms = {}
    for (k, j) in pairs:
        for z in (k, j):
            if z not in terms: terms[z] = true_carrier(z)
        xk, xj = terms[k], terms[j]
        ak, aj = R.acts(k, j)
        pk = ideal_play(k, xk, xj); pj = ideal_play(j, xj, xk)
        ok = (pk == ('C' if ak == 1 else 'D')) and (pj == ('C' if aj == 1 else 'D'))
        if ok: n_ok += 1
        else: bad.append((k, j, int(R.tsp[k]), int(R.tsp[j]), int(ak), int(aj), pk, pj))
        if n_exec < 40:
            n_exec += 1
            ek = C.play(xk, xj, K)[0]; ej = C.play(xj, xk, K)[0]
            if (ek, ej) != (pk, pj): n_exec_bad += 1
    for z in list(terms)[:100]:
        n_cls += 1
        if hh.bclass(terms[z], V, K) != int(R.tcls[z]): n_cls_bad += 1
    out = dict(g=int(R.g), pairs=len(pairs), agree=n_ok, disagree=len(bad), bad=bad[:20], classes=n_cls,
               class_disagree=n_cls_bad, executed=n_exec, executed_differs_from_ideal=n_exec_bad)
    log('audit at %d: %d / %d pairs agree; classes %d / %d agree; executed plays differ from ideal in %d / %d' % (
        R.g, n_ok, len(pairs), n_cls - n_cls_bad, n_cls, n_exec_bad, n_exec))
    return out
