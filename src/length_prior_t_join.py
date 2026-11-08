"""Step 3 (the join) and the verdict table of queue 75.

    python3 src/length_prior_t_join.py runs/length-prior-t.json runs/lt-prior.json OUT.md

For each machine: delta_LP (the reader share of the prior conditional on finite terms, junk in the denominator; exact-member
lower bound and family-level lower bound) against delta* of series 2b (the length-prior-shaped law, projection onto T+);
the smallest tested (N, I) at which delta_LP >= delta* (none if delta* is above delta_LP everywhere); the extrapolation: the
founder copy count c* = I N delta* from the tested cells and the I N it would need at delta_LP.
"""
import sys, json, math


def point(d):
    if d['kind'] == 'bracket':
        return d['interp'] or math.sqrt(d['lower'] * d['upper'])
    return None


if __name__ == '__main__':
    rep = json.load(open(sys.argv[1])); pri = json.load(open(sys.argv[2]))
    out = ['# Step 3: the join (generated)', '', 'A projection of the length prior onto T+ (readers = exact-member lower bounds, no other conditionals), one-sided.', '']
    for mn in ('R0', 'R1'):
        h = pri['machines'][mn]['headline']
        dl, dlf = h['reader_exact_lower_bound_cond'], h['reader_family_lower_bound_cond']
        out.append('## %s: delta_LP >= %.3g (exact members), >= %.3g (family level); bully/reader ratio %.3g' % (mn, dl, dlf, h['beta_exact_lower_bound_ratio']))
        for N in (200, 400):
            d = rep['delta_star_2b'].get('%s|%d' % (mn, N))
            if not d:
                out.append('- N = %d, I = 64: no 2b result' % N); continue
            if d['kind'] == 'bracket':
                p = point(d)
                cstar = 64 * N * p
                need = cstar / dl
                out.append('- N = %d, I = 64: delta* in (%.3g, %.3g], ~%.3g; delta_LP/delta* = %.2g -> %s; c* = I N delta* ~ %.3g founder copies; extrapolation: I*N ~ %.3g needed at delta_LP (labelled extrapolation)' % (
                    N, d['lower'], d['upper'], p, dl / p, 'reached' if dl >= d['upper'] else 'not reached', cstar, need))
            elif d['kind'] == 'beyond_grid':
                out.append('- N = %d, I = 64: delta* beyond the feasible grid (> %.3g): no tested (N, I) reaches it; no c* law fitted' % (N, d['lower']))
            else:
                out.append('- N = %d, I = 64: delta* below the grid (< %.3g)' % (N, d['upper']))
        out.append('')
    open(sys.argv[3], 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))
