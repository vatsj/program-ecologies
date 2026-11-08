"""Builds the step-1 input of series 2b (runs/length_prior_t/step1.json) from runs/lt-prior.json for the machines given.

Per machine (conditional on finite terms): const = the nine constant-code masses (exhaustive + Monte Carlo estimate), junk_f /
junk_r = the junk classes (estimates), single / two / bully / exploit = LOWER BOUNDS on the exact-member classes (exhaustive
masses for sizes <= s0 plus targeted-search masses above), so the within-reader ratios are those of the spellings found.

    python3 src/lt_prior_step1_json.py runs/lt-prior.json OUT.json R0 [R1]
"""
import sys, json

if __name__ == '__main__':
    R = json.load(open(sys.argv[1]))
    out = dict(machines=sys.argv[3:], note='readers are lower bounds on exact-member class masses; constants and junk are estimates')
    for mn in sys.argv[3:]:
        r = R['machines'][mn]
        q = r['finite_mass_q']
        c = r['combined']
        out[mn] = dict(const=r['const_by_code_cond'], junk_f=r['estimate']['junk_f']['total_cond'],
                       junk_r=r['estimate']['junk_r']['total_cond'],
                       single=c['single']['lower_bound_exact_raw'] / q, two=c['two']['lower_bound_exact_raw'] / q,
                       bully=c['bully']['lower_bound_exact_raw'] / q, exploit=c['exploit']['lower_bound_exact_raw'] / q,
                       omitted=dict(other_cond=r['estimate']['other_cond']['total_cond'], const_read=r['estimate']['const_read']['total_cond'],
                                    yielder=c['yielder']['lower_bound_family_raw'] / q))
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
    print(json.dumps(out, indent=1))
