"""Verdict checks for predictions/2026-10-01-cert-pricing.md from runs/cert_pricing.json.

    python3 src/cert_verdicts.py   -> prints the checks and appends them to runs/cert_pricing.md
"""
import json, os, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, 'runs', 'cert_pricing.json')))
OLD = json.load(open(os.path.join(ROOT, 'runs', 'priced_limN.json')))
Ns = (100, 1000, 10000, 30000)


def get(p, n, c, N, theta=1e-6):
    for r in R:
        if r['pricing'] == p and r['n'] == n and abs(r['c'] - c) < 1e-12 and r['N'] == N and abs(r.get('theta', 1e-6) - theta) < 1e-12:
            return r


out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))

P('## Verdict checks (src/cert_verdicts.py)', '')
# 1 references
d = []
for o in OLD:
    if o['exp'] != 'exp1' or o['pricing'] not in ('lazy', 'atoms'): continue
    if o['pricing'] == 'atoms' and o['c'] != 0: continue
    r = get(o['pricing'], o['n'], o['c'], o['N'])
    if r: d.append(abs(r['pcc'] - o['pcc']))
P('- **V1** references vs runs/priced_limN.json: %d cells, max |ΔP(C,C)| = %.1e' % (len(d), max(d)))
# 2 n = 6
d = [(p, c, N, get(p, 6, c, N)['pcc'] - get('atoms', 6, 0.0, N)['pcc']) for p in ('cert0', 'cert1', 'certC') for c in (1e-3, 1e-2) for N in Ns]
P('- **V2** n = 6, cert variants minus c = 0: max |Δ| = %.4f' % max(abs(x[3]) for x in d))
# 3 renewal identity
P('- **V3** cert0 n = 8 vs renewal identity (P_c0 − p)/(1 − p), p = c = 0 P*-block π:')
for c in (1e-3, 1e-2):
    row = []
    for N in Ns + (100000,):
        r = get('cert0', 8, c, N); z = get('atoms', 8, 0.0, N)
        if not r or not z: continue
        p = z['pstar_block']; pred = (z['pcc'] - p) / (1 - p)
        row.append('N=%d: %.4f vs %.4f (Δ %+.4f; c=0 %.4f)' % (N, r['pcc'], pred, r['pcc'] - pred, z['pcc']))
    P('  - c = %g: ' % c + '; '.join(row))
# 4 networks
P('- **V4** networks (rival share at 1e-3 / 1e-4, X, top program cooperates with FairBot):')
for p, cs in (('cert0', (1e-3, 1e-2)), ('atoms', (0.0,)), ('lazy', (1e-3, 1e-2)), ('cert1', (1e-3, 1e-2)), ('cert0flat', (1e-3, 1e-2)), ('lazycert0', (1e-3, 1e-2)), ('cert0diag', (1e-3, 1e-2))):
    for c in cs:
        row = []
        for N in (1000, 10000, 30000, 100000):
            r = get(p, 8, c, N)
            if not r: continue
            top = r['blocks'][0] if r['blocks'] else None
            row.append('N=%d: %.3f / %.3f, X %.3f, %s%s' % (N, r['rival_share'], r['rival_share_1e4'], r['universality'],
                       top['top'] if top else '-', ' (coop FB)' if top and top['coops_with_FB'] else ' (defects on FB)'))
        P('  - %s c=%g: ' % (p, c) + '; '.join(row))
# 5 P* block and exits
P('- **V5** P* block π and P* / nBM exits under cert0:')
for c in (1e-3, 1e-2):
    for N in (10000, 30000):
        r = get('cert0', 8, c, N); z = get('atoms', 8, 0.0, N); l = get('lazy', 8, c, N)
        tot = r['pstar_exit_strict'] + r['pstar_exit_neutral'] + r['pstar_exit_other']
        nt = r['nbm_exit_strict'] + r['nbm_exit_neutral'] + r['nbm_exit_other']
        dshare = sum(v for s, t, v in r['nbm_dest'] if s == 'D') / nt if nt else float('nan')
        P('  - c=%g N=%d: π(P* block) %.4f (c=0 %.4f, lazy %.4f); P* exit %.2e, strict share %.3f; nBM exit strict share %.3f, D share of top-4 dest %.3f' % (
            c, N, r['pstar_block'], z['pstar_block'], l['pstar_block'], tot, r['pstar_exit_strict'] / tot, r['nbm_exit_strict'] / nt, dshare))
# 6 top state
P('- **V6** cert0 top cooperative state (n = 8):')
for c in (1e-3, 1e-2):
    P('  - c=%g: ' % c + '; '.join('N=%d %s strict %.1e neutral %.2e (c=0 %.2e) ALLC %.2f' % (
        N, get('cert0', 8, c, N)['top_coop'], get('cert0', 8, c, N)['top_exit_strict'], get('cert0', 8, c, N)['top_exit_neutral'],
        get('atoms', 8, 0.0, N)['top_exit_neutral'], get('cert0', 8, c, N)['allc_share']) for N in (1000, 10000, 30000)))
# 7 lottery / numerics
bad = [(r['pricing'], r['n'], r['c'], r['N'], r['n_terminal'], r['near_closed'], r['absorb_error']) for r in R
       if r['pricing'] in ('cert0', 'cert1', 'certC', 'mono') and (r['n_terminal'] != 1 or r['near_closed'] != 0 or r['absorb_error'] > 1e-6)]
P('- **V7** cert0/cert1/certC/mono cells with >1 terminal, near-closed, or absorb error > 1e-6: %s' % (bad or 'none'))
allbad = [(r['pricing'], r['n'], r['c'], r['N'], r['n_terminal'], r['near_closed']) for r in R if r['n_terminal'] != 1 or r['near_closed'] != 0]
P('  - any cell: %s' % (allbad or 'none'))
for p in ('cert0', 'lazy'):
    a, b = get(p, 8, 1e-2, 30000), get(p, 8, 1e-2, 30000, 1e-7)
    if a and b: P('  - θ check %s c=0.01 N=3e4: %.6f vs %.6f (Δ %.1e)' % (p, a['pcc'], b['pcc'], abs(a['pcc'] - b['pcc'])))
P('  - max cut flow %.1e; max polymorphic π %.1e' % (max(r['cut_flow'] for r in R), max(r['poly'] for r in R)))
# 8-13 differences
def maxdiff(p, q, key='pcc', ns=(6, 8), cs=(1e-3, 1e-2), qc=None):
    m = 0.0
    for n in ns:
        for c in cs:
            for N in Ns:
                a = get(p, n, c, N); b = get(q, n, qc if qc is not None else c, N)
                if a and b: m = max(m, abs(a[key] - b[key]))
    return m
P('- **V8** cert1 vs c = 0: max |ΔP(C,C)| %.4f, max |Δ rival share| %.4f' % (maxdiff('cert1', 'atoms', qc=0.0), maxdiff('cert1', 'atoms', 'rival_share', qc=0.0)))
P('- **V9** certC vs cert0: max |ΔP(C,C)| %.4f, max |Δ rival share| %.4f' % (maxdiff('certC', 'cert0'), maxdiff('certC', 'cert0', 'rival_share')))
P('- **V10** mono vs cert0: max |ΔP(C,C)| %.1e' % maxdiff('mono', 'cert0', ns=(8,)))
P('- **V11** cert0flat vs c = 0: max |ΔP(C,C)| %.4f; rival share %s' % (maxdiff('cert0flat', 'atoms', ns=(8,), qc=0.0),
  ', '.join('%g/%d %.3f' % (c, N, get('cert0flat', 8, c, N)['rival_share']) for c in (1e-3, 1e-2) for N in (10000, 30000))))
P('- **V12** lazycert0 vs lazy: max |ΔP(C,C)| %.4f' % maxdiff('lazycert0', 'lazy', ns=(8,)))
P('- **V13** cert0diag: ' + '; '.join('c=%g N=%d P(C,C) %.4f (cert0 %.4f) π(PB) %.4f top %s rival %.3f' % (
    c, N, get('cert0diag', 8, c, N)['pcc'], get('cert0', 8, c, N)['pcc'], get('cert0diag', 8, c, N)['pi_PB'], get('cert0diag', 8, c, N)['top_coop'],
    get('cert0diag', 8, c, N)['rival_share']) for c in (1e-3, 1e-2) for N in (10000, 30000)))
# 14 large N and slopes
def ratio(r): return r['coop_mass'] / r['pi_D'] if r['pi_D'] > 0 else float('inf')
row = []
for p, c in (('atoms', 0.0), ('cert0', 1e-2), ('lazy', 1e-2)):
    a, b = get(p, 8, c, 30000), get(p, 8, c, 100000)
    sl = math.log(ratio(b) / ratio(a)) / math.log(100000 / 30000) if a and b and ratio(a) < 1e12 and ratio(b) < 1e12 else float('nan')
    row.append('%s c=%g: P(C,C) %.4f at 1e5, log-slope of coop/D 3e4→1e5 %.3f' % (p, c, b['pcc'], sl))
P('- **V14** ' + '; '.join(row))
P('- local log-slopes of coop/D (n = 8): ' + '; '.join('%s c=%g: %s' % (p, c, ', '.join(
    '%.2f' % (math.log(ratio(get(p, 8, c, N2)) / ratio(get(p, 8, c, N1))) / math.log(N2 / N1)) for N1, N2 in ((1000, 10000), (10000, 30000))))
    for p, c in (('atoms', 0.0), ('cert0', 1e-3), ('cert0', 1e-2), ('cert1', 1e-2))))
# free-arm check requested by the lead after the chain fix (a49a007): priced cells above c = 0 at the same n, N
above = []
for r in R:
    if r['c'] == 0: continue
    z = get('atoms', r['n'], 0.0, r['N'])
    if z and r['pcc'] > z['pcc'] + 0.002:
        above.append('%s n=%d c=%g N=%d %.4f vs %.4f (top %s, poly %.1e)' % (r['pricing'], r['n'], r['c'], r['N'], r['pcc'], z['pcc'], r['top_coop'], r['poly']))
P('- **Free-arm check** (chain fix a49a007): priced cells above c = 0 at the same n and N by more than 0.002: %d' % len(above))
for x in above: P('  - ' + x)
txt = '\n'.join(out)
print(txt)
md = os.path.join(ROOT, 'runs', 'cert_pricing.md')
s = open(md).read()
if '## Verdict checks' in s:
    s = s[:s.index('## Verdict checks')]
open(md, 'w').write(s.rstrip('\n') + '\n\n' + txt + '\n')
