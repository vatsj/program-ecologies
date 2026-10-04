"""Writes runs/conjecture4.md from runs/conjecture4.json (src/moat_static_big.py) and the sibling checks
(src/conj4.py).  specs/2026-10-04-conjecture4.md, Task 2.

    python3 src/conj4_report.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = 'BOX(THEM(ME))'
M_FB = 1.0 / 324          # unnormalized mass of the 3-node program BOX(THEM(ME))


def main():
    res = json.load(open(os.path.join(ROOT, 'runs', 'conjecture4.json')))
    ns = sorted(int(k) for k in res if k.isdigit())
    out = ['# Conjecture 4: static map at n = 6–13 and the sibling check', '',
           'Written by `src/conj4_report.py` from `runs/conjecture4.json` (`src/moat_static_big.py`) and `src/conj4.py`. '
           'Spec `specs/2026-10-04-conjecture4.md`; predictions `predictions/2026-10-04-conjecture4.md`; proof `notes/conjecture4.md`. '
           'Free modal arm, PD, boxes at PA and PA + Con(PA) (`modal.build`). Masses normalized over L_n unless marked unnormalized. '
           'n ≤ 11 reproduce `runs/drift_closure_static.json` exactly (class counts, frontier names, μ and leak to machine precision).', '',
           '## Per n', '',
           '| n | programs | canonical functions | classes | worlds | self-cooperating | suckerable self-coop. | components of G | closed | max drift distance | unsuckerable | FairBot leak/μ | min leak/μ (class) | time (s) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for n in ns:
        o = res[str(n)]
        fb = [r for r in o['frontier'] if r['name'] == FB][0]
        mn = o['frontier'][0]
        progs = sum(b['programs'] for b in o['by_size'])
        out.append('| %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %.4f | %.4f (`%s`) | %.0f |' % (
            n, progs, o['canon'], o['classes'], o['worlds'], o['self_coop'], o['n_suckerable_selfcoop'], o['n_components'],
            o['n_closed'], o['max_drift'], len(o['frontier']), fb['ratio'], mn['ratio'], mn['name'], o['t_total']))
    # runner-up
    out += ['', '**FairBot against the runner-up** (leak/μ):', '', '| n | FairBot | runner-up | runner-up / FairBot − 1 |', '|---|---|---|---|']
    for n in ns:
        f = res[str(n)]['frontier']
        fb = [r for r in f if r['name'] == FB][0]
        ru = [r for r in f if r['name'] != FB][0]
        out.append('| %d | %.5f | %.5f (`%s`) | %.2e |' % (n, fb['ratio'], ru['ratio'], ru['name'], ru['ratio'] / fb['ratio'] - 1))
    # shells
    nmax = ns[-1]; o = res[str(nmax)]
    fb = [r for r in o['frontier'] if r['name'] == FB][0]
    out += ['', '## Shells of FairBot\'s direct leak (n = %d; unnormalized mass, and contribution to leak/μ)' % nmax, '',
            'Shell s = programs of size exactly s. Shell s has total prior mass 1/(2s²). Leak membership is evaluated at '
            'cutoff n = %d. The contribution to leak/μ divides by FairBot\'s unnormalized class mass.' % nmax, '',
            '| s | shell mass 1/(2s²) | leak mass in shell | fraction of shell | FairBot-class mass in shell | Δ(leak/μ) | ratio to shell s−1 |',
            '|---|---|---|---|---|---|---|']
    mu_fb_un = sum(fb['mu_shell'])
    prev = None
    for s in range(1, nmax + 1):
        lm = fb['leak_shell'][s]; sm = 1.0 / (2 * s * s)
        r = (lm / prev) if prev else float('nan')
        out.append('| %d | %.4g | %.4g | %.4f | %.3g | %.3f | %s |' % (s, sm, lm, lm / sm, fb['mu_shell'][s], lm / mu_fb_un,
                   '%.3f' % r if prev else ''))
        prev = lm if lm > 0 else prev
    # shells across cutoffs (membership may change with n)
    out += ['', '**FairBot\'s leak by shell at each cutoff** (unnormalized leak mass in shell s, evaluated at cutoff n):', '',
            '| n | ' + ' | '.join('s=%d' % s for s in range(3, nmax + 1)) + ' |', '|---|' + '---|' * (nmax - 2)]
    for n in ns:
        f = [r for r in res[str(n)]['frontier'] if r['name'] == FB][0]
        out.append('| %d | ' % n + ' | '.join(('%.3g' % f['leak_shell'][s]) if s <= n else '' for s in range(3, nmax + 1)) + ' |')
    # program counts by size and depth
    out += ['', '## Program counts and prior mass by size and box-nesting depth (n = %d)' % nmax, '',
            '| size | programs | ' + ' | '.join('depth %d' % d for d in range(0, 5)) + ' |', '|---|---|' + '---|' * 5]
    massd = [0.0] * 6
    for b in o['by_size']:
        s = b['size']; tot = b['programs']
        out.append('| %d | %d | ' % (s, tot) + ' | '.join(str(b['by_depth'].get(str(d), b['by_depth'].get(d, 0))) for d in range(0, 5)) + ' |')
        for d, m in b['by_depth'].items():
            massd[int(d)] += m / tot / (2 * s * s)
    Z = sum(massd)
    out += ['', 'Prior mass by box-nesting depth (normalized over L_%d): ' % nmax + ', '.join('depth %d: %.4f' % (d, m / Z) for d, m in enumerate(massd) if m > 0) + '.']
    # frontier tables
    for n in ns:
        f = res[str(n)]['frontier']
        out += ['', '## Unsuckerable classes, n = %d (%d)' % (n, len(f)), '',
                '| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |', '|---|---|---|---|---|---|---|---|---|']
        for r in f:
            out.append('| `%s` | %.3e | %.3e | %.5g | %.3g | %.3f | %s | %s | %s |' % (
                r['name'], r['mu'], r['leak'], r['ratio'], r['closure_leak'], r['universality'], r['coop_FB'], r['coop_ALLC'],
                ', '.join('`%s`' % t for t in r['top_leaks'][:2])))
    # sibling checks
    sib = res.get('sibling')
    if sib:
        out += ['', '## Sibling check (Theorem 1 of `notes/conjecture4.md`)', '',
                'For every self-cooperating canonical function x of L_n (boxes up to lmax) that defects on D: y = or(x, ψ_K), '
                'ψ_K = and(not(BOX_K(THEM(^D))), not(BOXD_K(THEM(^D)))), z = BOX_K(THEM(^D)), K = max settle(P, D) over P in F(x). '
                'Checked in `modal_lv` (y, z added to the language): y–x mutual C, y self-C, y cooperates with z, z defects on y. '
                'Plus agreement of the independent evaluator in `src/conj4.py` with `modal_lv` on random pairs.', '',
                '| n / lmax | canonical functions | self-cooperating | cooperate with D | K histogram | failures | pairs compared | disagreements |',
                '|---|---|---|---|---|---|---|---|']
        for r in sib['crosschecks']:
            out.append('| %d / %d | %d | %d | %d | %s | %d | %d | %d |' % (r['n'], r['lmax'], r['classes'], r['self_coop'], r['coop_D'],
                       ', '.join('K=%s: %s' % kv for kv in r['K_hist'].items()), r['n_fail'], r['sample'], r['disagreements']))
        out += ['', '| x | size | K | sibling y (size) | faker z | ok |', '|---|---|---|---|---|---|']
        for r in sib['ladder']:
            if 'K' in r:
                out.append('| `%s` | %d | %d | `%s` (%d) | `%s` | %s |' % (r['x'], r['size'], r['K'], r['y'], r['y_size'], r['z'], r['ok']))
            else:
                out.append('| `%s` | %d | | %s | | |' % (r['x'], r['size'], r['note']))
    open(os.path.join(ROOT, 'runs', 'conjecture4.md'), 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
