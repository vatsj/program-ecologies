"""Certificates-only arm: lim_N of the eps->0 chain in the PD
(predictions/2026-10-01-certificates.md).

    python3 src/certificates_limN.py --static      # single-edge rates only (pre-registration)
    python3 src/certificates_limN.py               # the chain cells
Writes runs/certificates.md/json (chain) or prints the static tables.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import certificates as CE
import modal as M
from chain import Chain, fixation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 0.3
NS = (100, 1000, 10000, 30000)
TOL = 1e-13
TOL_ALT = 1e-11                    # threshold-sensitivity check
ORDER = ['tag', 'tageq', 'lfp', 'gfp', 'lob', 'lob1']
CELLS = [(v, n) for n in (10, 11) for v in ('tag', 'tageq', 'lfp', 'gfp', 'lob')] + [('lob1', 10)]
TT_NAME = {'gfp': 'IMP(THEM(THEM))', 'lfp': 'IMP(THEM(THEM))', 'lob': 'BOX(THEM(THEM))', 'lob1': 'BOX1(THEM(THEM))'}


def exit_kind(U, q, a):
    """Type of mutant q in the monomorphic world of a (PD, deterministic)."""
    uaa = U[a, a]
    if U[q, a] > uaa + 1e-9:
        return 'faker'              # strict first-order invader: a cooperates with q, q defects on a
    if max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-9:
        return 'neutral'
    if abs(U[q, a] - uaa) < 1e-9 and U[q, q] > U[a, q] + 1e-9:
        return 'strict'             # neutral against the resident, favoured among its own kind
    return 'other'                  # deleterious (fixation against selection)


def log_fixation(uqq, uqa, uaq, uaa, N, w):
    """log of the Moran fixation probability (kstar = N), stable for tiny values."""
    k = np.arange(1, N)
    pq = (k - 1) / (N - 1) * uqq + (N - k) / (N - 1) * uqa
    pa = k / (N - 1) * uaq + (N - k - 1) / (N - 1) * uaa
    logs = np.cumsum(w * (pa - pq))
    ls = np.logaddexp.reduce(logs)
    return -np.logaddexp(0.0, ls)


def coverage(cv, nodes, wts):
    """Weighted share of ordered pairs (a, b), a != b, among nodes that cooperate mutually."""
    nodes = list(nodes); w = np.array([wts[k] for k in nodes], float)
    if len(nodes) < 2: return float('nan')
    M_ = np.array([[1.0 if (a != b and cv[a, b] and cv[b, a]) else 0.0 for b in nodes] for a in nodes])
    off = np.outer(w, w); np.fill_diagonal(off, 0.0)
    return float((M_ * off).sum() / off.sum())


def setup(variant, n):
    L, val, info, prov = CE.build(n, variant)
    cv = CE.class_val(prov, val); mu = np.array([c[2] for c in prov.classes]); names = prov.names
    iD = names.index('D')
    cc = [x for x in range(len(names)) if cv[x, x] and not cv[x, iD]]
    return L, val, info, prov, cv, mu, names, cc


# ------------------------------------------------------------------ static (single-edge) estimates
def static(variant, n, ablate_tt=True):
    L, val, info, prov, cv, mu, names, cc = setup(variant, n)
    U = prov.Ufull; K = len(names)
    iD, iC = names.index('D'), names.index('C')
    iF = max(cc, key=lambda c: mu[c])              # main conditional cooperator (largest mu; all enter neutrally)
    comps = CE.coop_components(cv, cc)
    comps.sort(key=lambda g: -mu[g].sum())
    out = dict(variant=variant, n=n, programs=L.n_programs, classes=K, info=info, mu_C=mu[iC], mu_D=mu[iD],
               main=names[iF], mu_main=mu[iF], n_cc=len(cc), mu_cc=mu[cc].sum(), cc_components=len(comps),
               top_components=[(len(g), float(mu[g].sum()), names[g[0]]) for g in comps[:5]],
               cc_coverage_mu=coverage(cv, cc, mu),
               main_mutual=sum(1 for x in cc if x != iF and cv[x, iF] and cv[iF, x]))
    kinds = {}
    for q in range(K):
        if q == iF: continue
        kinds.setdefault(exit_kind(U, q, iF), []).append(q)
    out['main_world'] = {k: (len(v), float(mu[v].sum()), [names[q] for q in sorted(v, key=lambda q: -mu[q])[:4]]) for k, v in kinds.items()}
    out['shadow_mu'] = float(sum(mu[q] for q in kinds.get('neutral', []) if cv[q, iD]))
    iTT = names.index(TT_NAME[variant]) if variant in TT_NAME and TT_NAME[variant] in names else None
    rates = []
    for N in NS:
        r_in = fixation(U[iF, iF], U[iF, iD], U[iD, iF], U[iD, iD], N, W, N)
        ex = {k: float(sum(mu[q] * fixation(U[q, q], U[q, iF], U[iF, q], U[iF, iF], N, W, N) for q in v)) for k, v in kinds.items()}
        P = np.zeros((K, K))
        for a in range(K):
            for b in range(K):
                if a != b:
                    P[a, b] = mu[b] * fixation(U[b, b], U[b, a], U[a, b], U[a, a], N, W, N)
            P[a, P[a] < TOL] = 0.0          # as floor_transitions in the chain cells
            P[a, a] = 0.0; P[a, a] = 1 - P[a].sum()
        pi, closed = stat(P, mu)
        pcc = float(sum(pi[x] * cv[x, x] for x in range(K)))
        cc_flux = float(sum(mu[c] * fixation(U[c, c], U[c, iD], U[iD, c], U[iD, iD], N, W, N) for c in cc))
        r = dict(N=N, rho_main_D=r_in, entry_flux=mu[iF] * r_in, cc_flux=cc_flux, exits=ex, pcc_static=pcc, pi_D_static=float(pi[iD]),
                 pi_main_static=float(pi[iF]), closed_classes=closed,
                 static_support=[(names[x], float(pi[x])) for x in np.argsort(-pi)[:5]])
        if iTT is not None and cv[iTT, iTT]:
            r['pi_TT_static'] = float(pi[iTT])
            if ablate_tt:                    # mechanism diagnostic: suppress the faker edges out of the probe's world
                P2 = P.copy()
                for q in range(K):
                    if q != iTT and exit_kind(U, q, iTT) == 'faker':
                        P2[iTT, iTT] += P2[iTT, q]; P2[iTT, q] = 0.0
                pi2, _ = stat(P2, mu)
                r['pcc_ablated'] = float(sum(pi2[x] * cv[x, x] for x in range(K)))
                r['pi_TT_ablated'] = float(pi2[iTT])
        rates.append(r)
    out['rates'] = rates
    return out


def stat(P, mu):
    """Stationary distribution of the embedded chain; with several closed
    classes, the absorption lottery from the mu-weighted start (rule 5)."""
    import scipy.sparse.csgraph as csg, scipy.sparse as sp
    K = P.shape[0]
    off = P.copy(); np.fill_diagonal(off, 0.0)
    nc, lab = csg.connected_components(sp.csr_matrix(off > 0), directed=True, connection='strong')
    closed = [c for c in range(nc) if not (off[np.ix_(lab == c, lab != c)] > 0).any()]
    pi = np.zeros(K)
    trans = [i for i in range(K) if lab[i] not in closed]
    if trans:
        Q = P[np.ix_(trans, trans)]
        Ninv = np.linalg.inv(np.eye(len(trans)) - Q)
    for c in closed:
        mem = [i for i in range(K) if lab[i] == c]
        if len(mem) == 1: s = np.array([1.0])
        else:
            G = off[np.ix_(mem, mem)]; G = G - np.diag(G.sum(1))          # generator: exact diagonal
            Am = G.T.copy(); Am[-1] = 1; bb = np.zeros(len(mem)); bb[-1] = 1
            s = np.clip(np.linalg.solve(Am, bb), 0, None); s /= s.sum()
        w = sum(mu[i] for i in mem)
        if trans:
            R = P[np.ix_(trans, mem)].sum(1)
            w += float(mu[trans] @ (Ninv @ R))
        pi[mem] += w * s
    return pi / pi.sum(), len(closed)


# ------------------------------------------------------------------ chain cells
def floor_transitions(ch, tol=TOL):
    """Drop transition probabilities below tol (relative to the row) and
    recompute pi.  Exits of order e^(-cN) (deleterious fixation, e.g. out of a
    clique) are below double precision next to a self-loop of 1 - O(e^(-cN)),
    so the stationary solve cannot resolve them; dropping them makes such states
    closed, and pi becomes an absorption lottery from the seeds (rule 5).
    Returns the largest stationary flow dropped."""
    pi0 = dict(zip(ch.keys_list, ch.pi)); dropped = 0.0
    for a, row in ch.trans.items():
        small = [b for b, v in row.items() if b != a and v < tol]
        if not small: continue
        dropped = max(dropped, pi0.get(a, 0.0) * sum(row[b] for b in small))
        for b in small:
            row[a] = row.get(a, 0.0) + row.pop(b)
    ch.stationary()
    return dropped


def summarize(ch, P):
    pcc = 0.0; poly = 0.0; pis = {}; key_of = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if len(ids) > 1: poly += wgt
        else: pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
    return pcc, poly, pis, key_of


def cell(job):
    variant, n, N = job
    L, val, info, prov, cv, mu, names, cc = setup(variant, n)
    U, P = prov.Ufull, prov.PCC
    lang = M.ClassLang(prov)
    t = time.time()
    ch = Chain(prov, N=N, w=W, verbose=False, eager_poly=False).explore()
    trans0 = {a: dict(row) for a, row in ch.trans.items()}
    floored = floor_transitions(ch)
    iD, iC = names.index('D'), names.index('C')
    iF = CE.class_of(prov, L, CE.fb_name(variant))
    pcc, poly, pis, key_of = summarize(ch, P)
    poly_states = [(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-4) if ch.states[k][2] == 'poly'][:4]
    coop = sorted([(p, k) for k, p in pis.items() if cv[k, k]], reverse=True)
    iMain = coop[0][1] if coop else iF
    out = dict(variant=variant, n=n, N=N, w=W, classes=len(names), programs=L.n_programs, eval_info=info, pcc=pcc, poly=poly, poly_states=poly_states,
               pi_D=pis.get(iD, 0.0), pi_C=pis.get(iC, 0.0), pi_FB=pis.get(iF, 0.0), main=names[iMain], pi_main=pis.get(iMain, 0.0),
               cut_flow=ch.cut_flow, floored_flow=floored, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), absorb_error=float(getattr(ch, 'absorb_error', 0.0)),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:8])
    # entry into all-D and exits by type, for the main cooperator and the FairBot form
    for tag, i in (('main', iMain), ('FB', iF)):
        kD, kA = key_of.get(iD), key_of.get(i)
        rho = [v[0] for (a, b, q), v in ch.edge_rho.items() if a == kD and b == kA and q == i]
        ex = dict(faker=0.0, strict=0.0, neutral=0.0, other=0.0); shadow = 0.0; dest = {}
        if kA is not None:
            for b, v in ch.trans.get(kA, {}).items():
                if b == kA: continue
                for q, mw in ch.trans_mut[(kA, b)].items():
                    k = exit_kind(U, q, i); ex[k] += mw
                    if k == 'neutral' and cv[q, iD]: shadow += mw
                    dest[names[q]] = dest.get(names[q], 0.0) + mw
        out[tag] = dict(name=names[i], self_coop=bool(cv[i, i]), pi=pis.get(i, 0.0), mu=float(mu[i]), rho_enter=float(max(rho)) if rho else 0.0,
                        rho_enter_static=float(fixation(U[i, i], U[i, iD], U[iD, i], U[iD, iD], N, W, N)),
                        exit_total=sum(ex.values()), **{'exit_' + k: v for k, v in ex.items()}, exit_shadow=shadow,
                        top_exits=sorted(dest.items(), key=lambda kv: -kv[1])[:4])
    # mutual-cooperation graph over the pi-weighted cooperative support
    sup = [k for k, p in pis.items() if p > 1e-5 and cv[k, k]]
    comps = CE.coop_components(cv, sup)
    comps.sort(key=lambda g: -sum(pis[k] for k in g))
    cross = []
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            pairs = [(a, b) for a in comps[i] for b in comps[j]]
            cross.append('mutual D' if all(not cv[a, b] and not cv[b, a] for a, b in pairs) else 'one-way C')
    coop_mass = sum(pis[k] for k in sup)
    out['graph'] = dict(n_states=len(sup), coop_mass=coop_mass, n_components=len(comps),
                        components=[(len(g), float(sum(pis[k] for k in g)), [names[k] for k in sorted(g, key=lambda k: -pis[k])[:3]]) for g in comps[:6]],
                        largest_share=(sum(pis[k] for k in comps[0]) / coop_mass) if comps else float('nan'),
                        cross=dict((c, cross.count(c)) for c in set(cross)),
                        coverage_pi=coverage(cv, sup, pis),
                        cc_coverage_mu=coverage(cv, cc, mu),
                        main_mutual_cc=(sum(1 for x in cc if x != iMain and cv[x, iMain] and cv[iMain, x]), len([x for x in cc if x != iMain])))
    # verdict 8 (gfp): pi-weighted faker flux out of self-cooperating states; the loop-only part is where the
    # resident cooperates with the faker only through a loop, i.e. lfp says it defects, weighted over the
    # canonical members of both classes by mu
    if variant == 'gfp':
        Ll = CE.CertLanguage(n, 'lfp'); vl, _ = CE.evaluate(Ll)
        mc = L.mu_canon
        def loop_frac(a, q):
            ma, mq = prov.members[a], prov.members[q]
            w = np.outer(mc[ma], mc[mq])
            return float((w * (vl[np.ix_(ma, mq)] == 0)).sum() / w.sum())
        fk = dict(FB=0.0, other=0.0); fk_loop = dict(FB=0.0, other=0.0); loop_pairs = {}
        for a, pa in pis.items():
            if not cv[a, a] or a not in key_of: continue
            kA = key_of[a]; grp = 'FB' if a == iF else 'other'
            for b, v in ch.trans.get(kA, {}).items():
                if b == kA: continue
                for q, mw in ch.trans_mut[(kA, b)].items():
                    if exit_kind(U, q, a) != 'faker': continue
                    fk[grp] += pa * mw
                    lf = loop_frac(a, q)
                    if lf > 0:
                        fk_loop[grp] += pa * mw * lf
                        loop_pairs[(names[a], names[q])] = loop_pairs.get((names[a], names[q]), 0.0) + pa * mw * lf
        out['faker_flux'] = fk; out['faker_flux_loop_only'] = fk_loop
        out['loop_only_pairs'] = sorted(loop_pairs.items(), key=lambda kv: -kv[1])[:6]
    from priced_limN import hitting_time
    cc_keys = [key_of[k] for k in key_of if k in cc]
    out['hit_cc_from_D'] = hitting_time(ch, key_of.get(iD), cc_keys)
    # tags: effective inter-clique split, pi_A proportional to lottery_A / escape_A, escape in log space
    if variant in ('tag', 'tageq'):
        closed = []
        for c in ch.terminal:
            mem = np.nonzero(ch.labels == c)[0]
            if len(mem) != 1: continue
            ids = ch.states[ch.keys_list[mem[0]]][0]
            if len(ids) != 1: continue
            a = ids[0]
            if not cv[a, a]: continue
            lr = np.logaddexp.reduce([np.log(mu[q]) + log_fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, W) for q in range(len(names)) if q != a])
            closed.append((a, ch.absorb.get(c, 0.0), lr))
        if closed:
            lw = np.array([np.log(max(p, 1e-300)) - lr for a, p, lr in closed])
            sh = np.exp(lw - np.logaddexp.reduce(lw))
            out['clique_split'] = sorted([(names[a], float(p), float(lr / np.log(10)), float(s)) for (a, p, lr), s in zip(closed, sh)], key=lambda r: -r[3])[:5]
    # threshold sensitivity
    for a, row in trans0.items(): ch.trans[a] = dict(row)
    floor_transitions(ch, TOL_ALT)
    out['pcc_tol_alt'] = summarize(ch, P)[0]
    # mechanism ablation: suppress faker transitions out of the probe's monomorphic world
    iTT = names.index(TT_NAME[variant]) if variant in TT_NAME and TT_NAME[variant] in names else None
    if iTT is not None and cv[iTT, iTT] and iTT in key_of:
        for a, row in trans0.items(): ch.trans[a] = dict(row)
        floor_transitions(ch)
        kT = key_of[iTT]; row = ch.trans[kT]
        for b in list(row):
            if b == kT: continue
            fake = sum(mw for q, mw in ch.trans_mut[(kT, b)].items() if exit_kind(U, q, iTT) == 'faker')
            if fake > 0:
                row[b] -= fake; row[kT] = row.get(kT, 0.0) + fake
        ch.stationary()
        pc2, _, pis2, _ = summarize(ch, P)
        out['ablated'] = dict(pcc=pc2, pi_TT=pis2.get(iTT, 0.0), pi_FB=pis2.get(iF, 0.0))
        out['pi_TT'] = pis.get(iTT, 0.0)
    out['time_s'] = time.time() - t
    return out


def main_static(a):
    for variant, n in a.cells:
        s = static(variant, n)
        print('\n== %s n=%d: %d programs, %d classes, eval %s' % (variant, n, s['programs'], s['classes'], s['info']))
        print('   mu(C) %.4f mu(D) %.4f main %s mu %.5f; conditional cooperators %d (mu %.4f) in %d components; main mutual with %d others; mu-coverage %.3f; top %s' % (
            s['mu_C'], s['mu_D'], s['main'], s['mu_main'], s['n_cc'], s['mu_cc'], s['cc_components'], s['main_mutual'], s['cc_coverage_mu'], s['top_components']))
        print('   mutants in the all-main world:', s['main_world'], 'shadow mu %.4f' % s['shadow_mu'])
        for r in s['rates']:
            extra = ''
            if 'pi_TT_static' in r:
                extra = ' pi(TT) %.4f' % r['pi_TT_static']
                if 'pcc_ablated' in r: extra += ' | ablated P(C,C) %.4f pi(TT) %.4f' % (r['pcc_ablated'], r['pi_TT_ablated'])
            print('   N=%6d rho(main|D) %.4g entry flux %.3g (all CC %.3g, 1/flux %.3g) exits %s | static P(C,C) %.4f pi(D) %.4f pi(main) %.4f closed %d%s support %s' % (
                r['N'], r['rho_main_D'], r['entry_flux'], r['cc_flux'], 1 / r['cc_flux'], {k: '%.3g' % v for k, v in r['exits'].items()}, r['pcc_static'], r['pi_D_static'],
                r['pi_main_static'], r['closed_classes'], extra, [(nm, round(p, 4)) for nm, p in r['static_support']]))


def main(a):
    from multiprocessing import Pool
    jobs = sorted([(v, n, N) for v, n in a.cells for N in NS], key=lambda j: (-j[2], -j[1]))
    rows = []
    path = os.path.join(ROOT, 'runs', 'certificates.json')
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(cell, jobs):
            rows.append(r)
            m = r['main']
            print('%s n=%d N=%d: P(C,C) %.4f pi(D) %.4f main %s pi %.4f rho_in %.4g exits faker %.2e neutral %.2e other %.2e; graph %d comps (largest %.2f, coverage %.3f) poly %.1e cut %.1e terminal %d%s (%.0fs)' % (
                r['variant'], r['n'], r['N'], r['pcc'], r['pi_D'], m['name'], m['pi'], m['rho_enter'], m['exit_faker'],
                m['exit_neutral'], m['exit_other'], r['graph']['n_components'], r['graph']['largest_share'], r['graph']['coverage_pi'], r['poly'], r['cut_flow'],
                r['n_terminal'], (' ablated %.4f' % r['ablated']['pcc']) if 'ablated' in r else '', r['time_s']), flush=True)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
    rows.sort(key=lambda r: (r['n'], ORDER.index(r['variant']), r['N']))
    json.dump(rows, open(path, 'w'), indent=1, default=str)
    write_md(rows)


def write_md(rows):
    L = ['# Certificates-only arm: eps->0 chain (PD, w = 0.3, f = exp(w·payoff), `eager_poly=False`)', '',
         'Predictions: `predictions/2026-10-01-certificates.md`. Variants: tag (EQ, propositional equivalence), tageq (EQ with equality axioms), '
         'lfp (D-seeded IMP), gfp (C-seeded IMP), lob (PA provability, = M0), lob1 (PA + Con(PA) provability). Transitions below 1e-13 dropped (see brief).', '',
         '| variant | n | classes | N | P(C,C) | π(all-D) | main cooperator | π(main) | ρ(main \\| all-D) | exits from main: faker / strict / neutral (shadow) / other | cooperative support: states, components, largest share, π-coverage, between-component | polymorphic π | terminal | cut / dropped flow | P(C,C) at tol 1e-11 | ablated P(C,C) (π probe) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        m, g = r['main'], r['graph']
        ab = ('%.4f (%.3f; was %.3f)' % (r['ablated']['pcc'], r['ablated']['pi_TT'], r['pi_TT'])) if 'ablated' in r else '—'
        L.append('| %s | %d | %d | %d | %.4f | %.4f | `%s` | %.4f | %.4g | %.2e / %.2e / %.2e (%.2e) / %.2e | %d, %d, %.3f, %.3f, %s | %.1e | %d | %.1e / %.1e | %.4f | %s |' % (
            r['variant'], r['n'], r['classes'], r['N'], r['pcc'], r['pi_D'], m['name'], m['pi'], m['rho_enter'], m['exit_faker'], m['exit_strict'], m['exit_neutral'],
            m['exit_shadow'], m['exit_other'], g['n_states'], g['n_components'], g['largest_share'], g['coverage_pi'], g['cross'], r['poly'], r['n_terminal'],
            r['cut_flow'], r['floored_flow'], r['pcc_tol_alt'], ab))
    L += ['', '## Support, components, hitting times, faker accounting', '']
    for r in rows:
        s = '- **%s n=%d N=%d**: support %s; components %s; main mutual with %d of %d other conditional cooperators (μ-coverage among them %.3f); top exits from main %s; hitting time all-D → a conditional cooperator %.3g mutation events' % (
            r['variant'], r['n'], r['N'], '; '.join('%s %.3f' % sp for sp in r['support'][:6]),
            r['graph']['components'][:4], r['graph']['main_mutual_cc'][0], r['graph']['main_mutual_cc'][1], r['graph']['cc_coverage_mu'],
            [(k, '%.2e' % v) for k, v in r['main']['top_exits']], r['hit_cc_from_D'])
        if 'faker_flux' in r:
            s += '; π-weighted faker flux FB %.2e / others %.2e, loop-only FB %.2e / others %.2e, top loop-only pairs %s' % (
                r['faker_flux']['FB'], r['faker_flux']['other'], r['faker_flux_loop_only']['FB'], r['faker_flux_loop_only']['other'],
                [(a, b, '%.1e' % v) for (a, b), v in r['loop_only_pairs'][:3]])
        if 'clique_split' in r:
            s += '; cliques (lottery, log10 escape, effective share) %s' % [(a, '%.4f' % p, '%.1f' % le, '%.4f' % sh) for a, p, le, sh in r['clique_split']]
        if r['poly_states']:
            s += '; polymorphic states %s' % r['poly_states']
        L.append(s)
    open(os.path.join(ROOT, 'runs', 'certificates.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--static', action='store_true')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--cells', type=lambda s: (s.split(':')[0], int(s.split(':')[1])), nargs='+', default=CELLS)
    a = ap.parse_args()
    main_static(a) if a.static else main(a)
