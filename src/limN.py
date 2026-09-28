"""lim_N of the attractor chain: entry into and exits from all-THEM(^C), split
into shadow / faker / other mutants, with pi-weighted P(C,C).

    python3 src/limN.py --game pd --w 0.1 0.3 1 --N 100 300 1000 3000 10000 30000

Shadow: a mutant q on-path identical to R = THEM(^C) (u(q,R) = u(R,q) = u(q,q)
= u(R,R)).  Faker: u(q,R) > u(R,R).  Rates are shares of mutation events
(sum over mutants of mu(q) * rho), as in the chain's transition matrix.
Writes runs/limN_<game>.md and .json.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from run import run_cell, ROOT
from game import Game
from abm import load_or_evaluate


def analyse(ch, prov, lang, game):
    # class-level P(C,C) from the ABM cache (same language and classes)
    _, ids, reps, members, _, _, PCC, _, _, _ = load_or_evaluate(game, lang.n, verbose=False)
    cls = {}
    for c, mem in enumerate(members):
        for a in mem:
            cls[int(ids[a])] = c
    pcc_pi = 0.0; poly_pi = 0.0
    key_of = {}
    for key, w in zip(ch.keys_list, ch.pi):
        sid, x, kind = ch.states[key]
        x = np.asarray(x); cs = [cls[int(p)] for p in sid]
        pcc_pi += w * float(x @ PCC[np.ix_(cs, cs)] @ x)
        if len(sid) > 1: poly_pi += w
        else: key_of[lang.src(int(sid[0]))] = key
    kR, kD = key_of.get('THEM(^C)'), key_of.get('D')
    out = dict(pcc=pcc_pi, poly_pi=poly_pi,
               pi_R=float(ch.pi[ch.keys_list.index(kR)]) if kR is not None else 0.0,
               pi_D=float(ch.pi[ch.keys_list.index(kD)]) if kD is not None else 0.0)
    # entry D -> R
    out['entry'] = float(ch.trans.get(kD, {}).get(kR, 0.0)) if kD is not None and kR is not None else 0.0
    rho = [v[0] for (a, b, q), v in ch.edge_rho.items() if a == kD and b == kR]
    out['rho_enter'] = float(max(rho)) if rho else 0.0
    # exits from R, by mutant type
    ex = dict(shadow=0.0, faker=0.0, other=0.0); by_mut = {}
    if kR is not None:
        r = int(ch.states[kR][0][0])
        for b, wgt in ch.trans.get(kR, {}).items():
            if b == kR: continue
            for q, mw in ch.trans_mut[(kR, b)].items():
                Uq = prov.U([int(q), r])
                uqq, uqr, urq, urr = Uq[0, 0], Uq[0, 1], Uq[1, 0], Uq[1, 1]
                if max(abs(uqr - urr), abs(urq - urr), abs(uqq - urr)) < 1e-9: t = 'shadow'
                elif uqr > urr + 1e-9: t = 'faker'
                else: t = 'other'
                ex[t] += mw; by_mut[lang.src(int(q))] = by_mut.get(lang.src(int(q)), 0.0) + mw
    tot = sum(ex.values())
    out.update(exit_total=tot, **{'exit_' + k: v for k, v in ex.items()},
               faker_share=ex['faker'] / tot if tot else float('nan'),
               shadow_share=ex['shadow'] / tot if tot else float('nan'),
               top_exits=sorted(by_mut.items(), key=lambda kv: -kv[1])[:5])
    return out


def main(a):
    rows = []
    for w in a.w:
        for N in a.N:
            t = time.time()
            row, md, ch, prov, lang = run_cell('weak', 6, os.path.join(ROOT, 'games', a.game + '.yaml'), N, w=w, verbose=False)
            game = Game.load(os.path.join(ROOT, 'games', a.game + '.yaml'))
            r = dict(w=w, N=N, time_s=time.time() - t, support=row['support'][:6], indeterminate=row['indeterminate'],
                     cut_flow=row['cut_flow'], poly_flow=row['poly_flow'], mean_payoff=row['mean_payoff'])
            r.update(analyse(ch, prov, lang, game))
            rows.append(r)
            print('w=%g N=%d: pi(R) %.4f pi(D) %.4f P(C,C) %.4f rho_enter %.2e entry %.2e exit %.2e (shadow %.2f faker %.2f) poly %.1e (%.0fs)' % (
                w, N, r['pi_R'], r['pi_D'], r['pcc'], r['rho_enter'], r['entry'], r['exit_total'], r['shadow_share'], r['faker_share'], r['poly_pi'], r['time_s']), flush=True)
            json.dump(rows, open(os.path.join(ROOT, 'runs', 'limN_%s.json' % a.game), 'w'), indent=1, default=str)
    L = ['# lim_N of the attractor chain: %s, weak L_6 with ROLE, f = exp(w·payoff)' % a.game, '',
         'Exits from all-`THEM(^C)` as shares of mutation events; shadow = on-path identical to `THEM(^C)`, faker = earns more against it than it earns against itself.', '',
         '| w | N | π(all-D) | π(all-`THEM(^C)`) | P(C,C) | ρ_enter | entry | exit | shadow share | faker share | π polymorphic | support (top 4) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %g | %d | %.4f | %.4f | %.4f | %.2e | %.2e | %.2e | %.2f | %.2f | %.1e | %s |' % (
            r['w'], r['N'], r['pi_D'], r['pi_R'], r['pcc'], r['rho_enter'], r['entry'], r['exit_total'], r['shadow_share'], r['faker_share'], r['poly_pi'],
            '; '.join('%s %.4f' % (s, p) for s, p in r['support'][:4])))
    L += ['', 'Top exit mutants from all-`THEM(^C)` (share of mutation events):', '']
    for r in rows:
        L.append('- w=%g N=%d: %s' % (r['w'], r['N'], ', '.join('`%s` %.2e' % kv for kv in r['top_exits'])))
    open(os.path.join(ROOT, 'runs', 'limN_%s.md' % a.game), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--w', type=float, nargs='+', default=[0.1, 0.3, 1.0])
    ap.add_argument('--N', type=int, nargs='+', default=[100, 300, 1000, 3000, 10000, 30000])
    main(ap.parse_args())
