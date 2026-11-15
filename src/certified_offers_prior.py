"""Step 1 of queue 79 (spec specs/2026-11-15-certified-offers.md): length-prior mass of the certified families (exact-member lower bounds
from canonical spellings; no Monte Carlo), under the three measures fixed in notes/certified-offers.md section 1.6:

  C1          R1's tags plus one arity-2 tag `carry(c, B)`: the skeleton with certificate code c = fn + 2 fp + 4 pref and fallback lam^3 B
  R1-written  R1's tags; the skeleton spelled with `lib CARRY`, the certificate a literal pair, the fallback lam^3 B
  C0-written  R0's tags; the skeleton with CARRY's and CHK's library bodies inlined (no library), reads written out

Comparators (re-weighed in each machine): the fair single readers (the eight S), the bullies (Bn, Bp), queue 78's R (Rnn, Rpn).  Every
canonical spelling is checked against the catalogue program's play on a sample of (next, prev) profiles before its mass is counted.

    python3 src/certified_offers_prior.py OUT.json OUT.md
"""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
NLIB_M3 = len(L.LIB)                     # milestone 3's library, before this queue's entries
import certified_offers as CO
import lt_prior as P
import tplus as TP

P.ARITY['carry'] = 2
NLIB_ALL = len(L.LIB)
C1M = P.Machine('C1', P.R1.tags + ['carry'])


def q_of(m):
    return m.extinction()


def mass(t, mach, nlib=NLIB_ALL):
    """prior mass of the body t (P.term_mass with the library size and the carry tag)."""
    pt = 1.0 / mach.T
    tag = t[0]
    if tag == 'lib':
        return pt / nlib
    if tag == 'carry':
        return pt * mass(t[1], mach, nlib) * mass(t[2], mach, nlib)
    if tag in ('v', 'nat', 'con', 'readn', 'readp'):
        return P.term_mass(t, mach)
    if tag == 'op':
        return pt / 7 * mass(t[2], mach, nlib) * mass(t[3], mach, nlib)
    m = pt
    for c in t[1:]:
        m *= mass(c, mach, nlib)
    return m


def log10mass(t, mach, nlib=NLIB_ALL):
    """log10 of the prior mass (no underflow), the same per-node rule as `mass`."""
    lt = -math.log10(mach.T)
    tag = t[0]
    if tag == 'lib':
        return lt - math.log10(nlib)
    if tag in ('v', 'nat'):
        return lt + math.log10(P.elias(t[1]))
    if tag == 'con':
        return lt - math.log10(5)
    if tag in ('readn', 'readp'):
        return lt
    if tag == 'op':
        return lt - math.log10(7) + log10mass(t[2], mach, nlib) + log10mass(t[3], mach, nlib)
    if tag == 'sim':
        return lt + math.log10(P.elias(t[1])) + log10mass(t[2], mach, nlib)
    return lt + sum(log10mass(c, mach, nlib) for c in t[1:])


def nodes(t):
    if t[0] == 'carry':
        return 1 + nodes(t[1]) + nodes(t[2])
    return P.node_count(t)


# ---------------------------------------------------------------- canonical bodies (R1 syntax; readn / readp are R1 tags)
RN, RP = ('readn',), ('readp',)


def acc(r, dirn, to):
    t = ('eq', r, ('nat', 4 if dirn == 'n' else 1))
    return ('if', t, ('con', 'T'), ('eq', r, ('con', 'TO'))) if to == 'y' else t


def one_read(dirn, to, go, dflt):
    """if the read partner names me at 1/2: go, else dflt.  n: the read inline (one use); y: let-bound (two uses)."""
    rd = RN if dirn == 'n' else RP
    if to == 'n':
        return ('if', acc(rd, dirn, to), ('nat', go), ('nat', dflt))
    return ('app', ('lam', ('if', acc(('v', 0), dirn, to), ('nat', go), ('nat', dflt))), rd)


def two_read(first, fb, to):
    d2 = 'p' if first == 'n' else 'n'
    g1 = 1 if first == 'n' else 4
    g2 = 4 if first == 'n' else 1
    f = {'f': g1, 'z': 8}[fb]
    inner = one_read(d2, to, g2, f)
    if to == 'n':
        return ('if', acc(RN if first == 'n' else RP, first, to), ('nat', g1), inner)
    # let-bound first read; inner at depth +1 (its own read is a tag, depth-free; no free variables)
    return ('app', ('lam', ('if', acc(('v', 0), first, to), ('nat', g1), inner)), RN if first == 'n' else RP)


def body_of(name):
    """canonical R1 body of a base program (constants, singles, twos, bullies, R)."""
    if name[0] == 'C':
        return ('nat', int(name[1:]))
    if name[0] == 'S':
        d, fb, to = name[1], name[2], name[3]
        go = 1 if d == 'n' else 4
        other = 4 if d == 'n' else 1
        return one_read(d, to, go, {'o': other, 'z': 8}[fb])
    if name[0] == 'D':
        return two_read(name[1], name[2], name[3])
    if name in ('Bn', 'Bp'):
        rd = RN if name == 'Bn' else RP
        return ('if', ('eq', rd, ('nat', 3 if name == 'Bn' else 0)), ('nat', 2 if name == 'Bn' else 5), ('nat', 4 if name == 'Bn' else 1))
    if name in ('Rnn', 'Rpn'):
        return one_read(name[1], 'n', 1 if name[1] == 'n' else 4, 3 if name[1] == 'n' else 0)
    if name[0] == 'P':                    # prudent readers (strict probe, fallback z): written with the probe read spelled out
        return None
    raise ValueError(name)


def cert_code(c):
    return c[0] + 2 * c[1] + 4 * c[2]


def carrier_bodies(tb):
    """{carrier name: {'C1': body, 'R1w': body}} for the carriers whose fallback has a canonical body."""
    out = {}
    for i, nm in enumerate(tb.names):
        m = tb.cat.meta[i]
        if m['cert'] is None:
            continue
        B = body_of(m['fb'])
        if B is None:
            continue
        c = m['cert']
        out[nm] = dict(C1=('carry', ('nat', cert_code(c)), B),
                       R1w=('app', ('app', ('app', ('app', ('app', ('lib', CO.ID_CARRY), CO.cert_term(*c)), ('lam', ('lam', ('lam', B)))),
                                             ('v', 2)), ('v', 1)), ('v', 0)))
    return out


# ---------------------------------------------------------------- expansions to executable terms
def expand_carry(t, d=0):
    """C1 syntax -> L_T: carry(c, B) -> the skeleton (at binder depth d inside the body: me n p are v(d+2) v(d+1) v(d))."""
    tag = t[0]
    if tag == 'carry':
        c = t[1][1]
        cert = (c & 1, (c >> 1) & 1, (c >> 2) & 1)
        B = P.expand(t[2], 0)
        return ('app', ('app', ('app', ('app', ('app', ('lib', CO.ID_CARRY), CO.cert_term(*cert)), ('lam', ('lam', ('lam', B)))),
                                ('v', d + 2)), ('v', d + 1)), ('v', d))
    return P.expand(t, d)


def expand_r1w(t):
    """R1-written: the lib skeleton already explicit; expand the fallback's reads (inside lam^3, their own frame)."""
    return _exp_reads_under(t)


def _exp_reads_under(t):
    tag = t[0]
    if tag == 'lam' and t[1][0] == 'lam' and t[1][1][0] == 'lam':
        return ('lam', ('lam', ('lam', P.expand(t[1][1][1], 0))))
    if tag in ('v', 'nat', 'con', 'lib'):
        return t
    if tag in ('lam', 'fix'):
        return (tag, _exp_reads_under(t[1]))
    return (tag,) + tuple(_exp_reads_under(c) for c in t[1:])


def inline_lib(t, ids, depth_guard=0):
    """replace ('lib', i) for i in ids by the library term (recursively): the C0-written spelling with no library."""
    tag = t[0]
    if tag == 'lib' and t[1] in ids:
        assert depth_guard < 50
        return inline_lib(L.LIB[t[1]], ids, depth_guard + 1)
    if tag in ('v', 'nat', 'con', 'lib'):
        return t
    if tag in ('lam', 'fix', 'fst', 'snd', 'quote', 'libsrc'):
        return (tag, inline_lib(t[1], ids, depth_guard))
    if tag == 'op':
        return ('op', t[1], inline_lib(t[2], ids, depth_guard), inline_lib(t[3], ids, depth_guard))
    if tag == 'sim':
        return ('sim', t[1], inline_lib(t[2], ids, depth_guard))
    return (tag,) + tuple(inline_lib(c, ids, depth_guard) for c in t[1:])


def check_spelling(tb, name, prog_term, n_pairs=400, seed=0):
    """the spelled program's code equals the catalogue program's on a sample of (next, prev) profiles (C1 machine)."""
    CO.set_machine('C1')
    rng = np.random.default_rng(seed)
    p = tb.cat.idx[name]
    bad = 0
    for _ in range(n_pairs):
        n, v = int(rng.integers(tb.K)), int(rng.integers(tb.K))
        c = L.run_big(TP.f_eval, prog_term, tb.cat.terms[n], tb.cat.terms[v])[0]
        if c != int(tb.code[p, n, v]):
            bad += 1
    return bad


def main(out, md):
    import certified_offers_dyn as D
    tb = D.tabs(os.path.join(ROOT, 'runs', '_cache'))
    old = json.load(open(os.path.join(ROOT, 'runs', 'lt_prior', 'lt-prior.json')))
    qR0, qR1 = old['machines']['R0']['finite_mass_q'], old['machines']['R1']['finite_mass_q']
    qC1 = q_of(C1M)
    base = ['S%s%s%s' % (d, fb, to) for d in 'np' for fb in 'oz' for to in 'yn'] + ['Bn', 'Bp', 'Rnn', 'Rpn']
    car = carrier_bodies(tb)
    res = dict(q=dict(R0=qR0, R1=qR1, C1=qC1), T=dict(R0=P.R0.T, R1=P.R1.T, C1=C1M.T), nlib=dict(milestone3=NLIB_M3, with_queue79=NLIB_ALL),
               programs={})
    lib_ids = set(range(NLIB_M3, NLIB_ALL))
    for nm in base:
        B = body_of(nm)
        prog = P.frame(P.expand(B, 0))
        bad = check_spelling(tb, nm, prog)
        b0 = P.expand(B, 0)
        res['programs'][nm] = dict(nodes_R1=nodes(B), nodes_R0=nodes(b0), C1=mass(B, C1M) / qC1, R1=mass(B, P.R1) / qR1,
                                   R0=mass(b0, P.R0, NLIB_M3) / qR0, check_bad=bad, sexpr=P.to_sexpr(B))
    for nm, bd in car.items():
        t1 = P.frame(expand_carry(bd['C1']))
        bad1 = check_spelling(tb, nm, t1)
        tw = P.frame(expand_r1w(bd['R1w']))
        badw = check_spelling(tb, nm, tw)
        c0 = inline_lib(expand_r1w(bd['R1w']), lib_ids)
        bad0 = check_spelling(tb, nm, P.frame(c0), n_pairs=100)
        res['programs'][nm] = dict(nodes_C1=nodes(bd['C1']), nodes_R1w=nodes(bd['R1w']), nodes_C0w=nodes(c0),
                                   C1=mass(bd['C1'], C1M) / qC1, R1w=mass(bd['R1w'], P.R1) / qR1,
                                   C0w_log10=log10mass(c0, P.R0, NLIB_M3) - math.log10(qR0),
                                   check_bad=dict(C1=bad1, R1w=badw, C0w=bad0), sexpr_C1=str(bd['C1'])[:200])
    fam = lambda pref: [k for k in res['programs'] if k.startswith(pref)]
    G = {'single': [k for k in base if k[0] == 'S'], 'bully': ['Bn', 'Bp'], 'R': ['Rnn', 'Rpn'], 'Oc': fam('Oc'), 'Rc': ['Rcn', 'Rcp'],
         'Rcs': fam('Rcs'), 'Fc': fam('Fc'), 'Bc': fam('Bc')}
    sums = {}
    for g, mem in G.items():
        d = {}
        for meas in ('C1', 'R1', 'R1w', 'R0'):
            vals = [res['programs'][k].get(meas) for k in mem if res['programs'][k].get(meas) is not None]
            if vals:
                d[meas] = float(sum(vals))
        if g in ('Oc', 'Rc', 'Rcs', 'Fc', 'Bc'):
            d['C0w_log10_max'] = max(res['programs'][k]['C0w_log10'] for k in mem)
            d['shortest'] = dict(C1=min(res['programs'][k]['nodes_C1'] for k in mem), R1w=min(res['programs'][k]['nodes_R1w'] for k in mem),
                                 C0w=min(res['programs'][k]['nodes_C0w'] for k in mem))
        else:
            d['shortest'] = dict(R1=min(res['programs'][k]['nodes_R1'] for k in mem), R0=min(res['programs'][k]['nodes_R0'] for k in mem))
        sums[g] = d
    res['groups'] = sums
    # ratios: the certified family under C1 against the comparators in C1; under R1-written against R1
    rat = {}
    for g in ('Oc', 'Rc', 'Rcs', 'Fc', 'Bc'):
        rat[g] = dict(C1_to_single=sums[g]['C1'] / sums['single']['C1'], C1_to_bully=sums[g]['C1'] / sums['bully']['C1'],
                      C1_to_R=sums[g]['C1'] / sums['R']['C1'],
                      R1w_to_single=sums[g]['R1w'] / sums['single']['R1'], R1w_to_bully=sums[g]['R1w'] / sums['bully']['R1'],
                      R1w_to_R=sums[g]['R1w'] / sums['R']['R1'])
    res['ratios'] = rat
    json.dump(res, open(out, 'w'), indent=1)
    Lx = ['# Queue 79 step 1: length-prior mass of the certified families (canonical spellings; conditional on finite trees)', '',
          'Machines: C1 = R1 + `carry` (T = %d, q = %.4f); R1 (T = %d, q = %.4f; lib uniform over %d entries); R0 (T = %d, q = %.4f; the C0-written '
          'spelling has no library). Every spelling was checked against the catalogue program on sampled profiles (column "check": mismatches).' % (
              C1M.T, qC1, P.R1.T, qR1, NLIB_ALL, P.R0.T, qR0), '',
          '| group | C1 mass | R1 (written) mass | shortest C1 / R1 / R0 (C0-written) nodes | C0-written log10 mass (max) |', '|---|---|---|---|---|']
    for g, d in sums.items():
        sh = d['shortest']
        Lx.append('| %s | %.3g | %.3g | %s | %s |' % (g, d.get('C1', float('nan')), d.get('R1w', d.get('R1', float('nan'))),
                                                     ' / '.join(str(v) for v in sh.values()), ('%.1f' % d['C0w_log10_max']) if 'C0w_log10_max' in d else '-'))
    Lx += ['', '| family | C1 / single | C1 / bully | C1 / R | R1w / single | R1w / bully | R1w / R |', '|---|---|---|---|---|---|---|']
    for g, r in rat.items():
        Lx.append('| %s | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g |' % (g, r['C1_to_single'], r['C1_to_bully'], r['C1_to_R'], r['R1w_to_single'], r['R1w_to_bully'], r['R1w_to_R']))
    Lx += ['', '| program | nodes (C1 / R1w / C0w, or R1 / R0) | C1 | R1 or R1w | check mismatches |', '|---|---|---|---|---|']
    for k, v in res['programs'].items():
        if 'nodes_C1' in v:
            Lx.append('| %s | %d / %d / %d | %.3g | %.3g | %s |' % (k, v['nodes_C1'], v['nodes_R1w'], v['nodes_C0w'], v['C1'], v['R1w'], v['check_bad']))
        else:
            Lx.append('| %s | %d / %d | %.3g | %.3g | %d |' % (k, v['nodes_R1'], v['nodes_R0'], v['C1'], v['R1'], v['check_bad']))
    open(md, 'w').write('\n'.join(Lx) + '\n')
    print('\n'.join(Lx))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
