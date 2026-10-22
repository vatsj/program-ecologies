"""Diagnostic re-run of one counted run (deterministic: same seeds) to a given generation, dumping the response-signature histogram
and the most common types with their fills.  python3 tools/beh_diag.py CELL REP GENS [OUT.md]   (a diagnostic, not a counted cell)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh_run as R
import hooks_beh_kern as K
import hooks_w2 as H

cell, rep, gens = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
lines = []


def sig_str(s):
    return ''.join('CD'[1 - ((s >> k) & 1)] for k in range(6)) + '|' + 'CD'[1 - ((s >> 6) & 1)]


def post(d):
    S = d['S']; T = d['T']; ev = d['ev']
    Tb, Tl, Tf, Tn, Tg, Ts0 = T[0], T[1], T[2], T[3], T[4], T[5]
    pres, cnt, npres, rec = d['pres'], d['cnt'], d['npres'], d['rec']
    eff = rec[:, 0] >= 0.95
    sigs = {}; types = {}
    for i in range(pres.shape[0]):
        for s in range(int(npres[i])):
            t = int(pres[i, s]); c = int(cnt[i, s])
            sg = int(K._sigspec(S.LA, S.KA, ev, S.Lx.iC, S.Lx.iD, int(Tb[t]), int(Ts0[t]), S.PANb, S.PANs))
            key = (sg, bool(eff[i]))
            sigs[key] = sigs.get(key, 0) + c
            desc = R.type_desc(S, T, t)
            nm = desc['base'] + ' ' + ' '.join(f.replace('behaviour:', '') for f in desc['fills'])
            types[nm] = types.get(nm, 0) + c
    lines.append('# diagnostic: %s rep %d to generation %d\n' % (cell, rep, gens))
    lines.append('islands efficient: %d of %d; panel order: %s then a stranger copy\n' % (eff.sum(), len(eff), S.panel_order))
    tot = sum(sigs.values())
    for w in (True, False):
        sub = sorted(((n, sg) for (sg, e), n in sigs.items() if e == w), reverse=True)
        tt = sum(n for n, _ in sub)
        lines.append('\n## response signatures on %s islands (%d individuals)\n' % ('efficient' if w else 'non-efficient', tt))
        for n, sg in sub[:12]:
            cls = K._class_of(sg, S.cref)
            lines.append('- %s  %d (%.3f)  class %s' % (sig_str(sg), n, n / max(tt, 1), R.CLASS_NAMES[cls]))
    lines.append('\n## most common types (base, fills as scope:origin:action:key:tag)\n')
    for nm, n in sorted(types.items(), key=lambda x: -x[1])[:25]:
        lines.append('- %d  %s' % (n, nm))


row = R.run_one(cell, rep, gens=gens, post=post)
lines.append('\nuniversal_open %s, efficient islands %.3f, wall %.0f s' % (row['universal_open'], row['eff_islands'], row['wall']))
txt = '\n'.join(lines)
print(txt)
if out:
    open(out, 'w').write(txt)
