"""Queue 81: concrete islands for the report (stage-1 cells).  Positive migrant regret (resident, better variant,
separating migrant) and costly threats carried with zero regret.

    python3 src/tbr_examples.py > runs/tbr/examples.txt
"""
import glob, gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    import tbr
    A = {a: tbr.Tri(a) for a in ('T', 'M')}
    import tbr_p as TP
    d = TP._d()

    def nm(arm, s, k):
        if arm == 'T':
            return A['T'].names[k]
        if arm == 'M':
            from churn_primary import get_cat
            return '%d:%s' % (k, A['M'].fam_names[A['M'].fam[s, k]])
        return d['names'][k]
    print('== positive migrant regret (settled, zero native regret, T-weighted) ==')
    for arm, pat in (('T', 'T_*_100_1.json.gz'), ('M', 'M_*_100_1.json.gz')):
        n = 0; seen = set()
        for f in sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'tm', pat))):
            r = json.load(gzip.open(f, 'rt'))
            for c in r['snaps']['100']['cases']:
                if c.get('ex') and c['set08'] and not c['natpos'] and n < 4:
                    e = c['ex']
                    key = (c['j'], c['p'], e['better'], e['sep_migrant'])
                    if key in seen:
                        continue
                    seen.add(key)
                    o1, o2 = tbr.OTHERS[c['j']]
                    prof = e['profile']
                    print('%s N=%d run %d island %d slot %d: profile %s; resident %s, better %s (sigma %.2f); '
                          'separating migrant %s in slot %d (Delta %+.3f, share of migrants %.2f, T_q %.1f)' % (
                              arm, r['N'], r['run'], c['i'], c['j'], [nm(arm, s, prof[s]) for s in range(3)],
                              nm(arm, c['j'], c['p']), nm(arm, c['j'], e['better']), e['sigma'],
                              nm(arm, e['sep_slot'], e['sep_migrant']), e['sep_slot'], e['delta'], e['a_q'], e['T_q']))
                    n += 1
    n = 0; seen = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'p', '*_1.091_*.json.gz'))):
        r = json.load(gzip.open(f, 'rt'))
        for c in r['snaps']['100']['cases']:
            if c.get('ex') and c['set08'] and not c['natpos'] and n < 6:
                e = c['ex']
                key = (e['resident'], e['better'], e['sep_migrant'])
                if key in seen:
                    continue
                seen.add(key)
                print('P %s run %d island %d: resident %s, better %s (sigma %.2f); separating migrant %s (Delta %+.1f, '
                      'share %.2f, T_q %.1f)' % ((r['rival'] or 'natural')[:44], r['run'], c['i'], e['resident'], e['better'],
                                               e['sigma'], e['sep_migrant'], e['delta'], e['a_q'], e['T_q']))
                n += 1
    print('\n== costly threats carried with zero migrant regret (T, M; settled, zero native regret) ==')
    for arm, pat in (('T', 'T_*_100_1.json.gz'), ('M', 'M_*_100_1.json.gz')):
        n = 0; tot = 0; withthr = 0; seen = set()
        for f in sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'tm', pat))):
            r = json.load(gzip.open(f, 'rt'))
            for c in r['snaps']['100']['cases']:
                if not (c['set08'] and not c['natpos'] and not c['vacE'] and c['regT'] <= 1e-9):
                    continue
                tot += 1
                th = c.get('threat')
                if th:
                    withthr += 1
                    key = (c['j'], c['p'], th['variant'], th['tester'])
                    if n < 4 and key not in seen and r['snaps']['100']['world']['diverse']:
                        seen.add(key)
                        print('%s N=%d run %d island %d slot %d: resident %s carries a threat against prior tester %s in '
                              'slot %d (prior mass %.3g): variant %s would earn %+.3f more against it, the tester earns '
                              '%+.3f more against the variant; world diverse: %s' % (
                                  arm, r['N'], r['run'], c['i'], c['j'], nm(arm, c['j'], c['p']), nm(arm, th['slot'], th['tester']),
                                  th['slot'], th['pi'], nm(arm, c['j'], th['variant']), th['gain'], th['hurt'],
                                  r['snaps']['100']['world']['diverse']))
                        n += 1
        print('%s: zero-regret residents %d, of which carrying a costly threat against some prior tester %d (%.2f)' % (
            arm, tot, withthr, withthr / tot if tot else 0))


if __name__ == '__main__':
    main()
