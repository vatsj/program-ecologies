"""Queue 80 step 0, post-hoc addition (labelled in step0.json as b3_all_thirds_posthoc; run after the registered step-0 pass): the
simulating bully into the pair slots of fair carrier islands with every non-carrier as the third slot (queue 79's form of the assay;
the registered pass used the 2/3-demanding constants C8, C2, C5 only), canonical spellings.

    python3 src/script_offers_step0x.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import script_offers_step0 as S0

if __name__ == '__main__':
    ctx = S0.Ctx()
    bul = ctx.fam('bully')
    out = {}
    for fa, fb in (('s_firm', 's_firm'), ('s_open', 's_acc'), ('s_firm+', 's_firm+'), ('s_prud+', 's_prud+'), ('s_prud+', 's_acc+'),
                   ('s_firm', 's_bully')):
        rows = []
        for (t, sa, sb, sc) in S0.pair_islands(ctx, ctx.fam(fa, 'canon'), ctx.fam(fb, 'canon')):
            for x in bul:
                for s in (sa, sb):
                    rows.append(S0.edge(ctx, t, s, x))
        out['B into pair of (%s, %s), every non-carrier third, canonical spellings' % (fa, fb)] = S0.summ(rows)
    p = os.path.join(ROOT, 'runs', 'script_offers', 'step0.json')
    d = json.load(open(p))
    d['b3_all_thirds_posthoc'] = out
    json.dump(d, open(p, 'w'), indent=1)
    for k, v in out.items():
        print(k, v['n'], round(v['median'], 4), round(v['max'], 3), v['share_lt_third'], v.get('fixed_out'))
