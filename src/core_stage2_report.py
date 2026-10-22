"""Tables and verdict digest for the core stage-2 run: reads runs/core_stage2/cell_*.json, rows_*.csv.gz and statics.json, writes
runs/core_stage2/tables.json and table_cells.csv, and prints the digest.

    python3 src/core_stage2_report.py
"""
import gzip, json, os, sys, csv, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core_auction as C
import core_stage2 as S
import core_stage2_run as R

OUT = S.OUT


def load(name):
    p = os.path.join(OUT, 'cell_%s.json' % name)
    if not os.path.exists(p):
        return None, None
    return json.load(open(p)), pd.read_csv(os.path.join(OUT, 'rows_%s.csv.gz' % name))


def frac_sd(df, col):
    g = df.groupby('run')[col].mean()
    return float(df[col].mean()), float(g.std())


def delta_of(k):
    return int(k) - S.F0 + 1


def split_table(inst, df):
    """islands with both item roles fixed on followers and the items winning outright (TX never wins): A's payment, exact reference classes."""
    d = df[(df.fixA == 1) & (df.fixB == 1) & (df.folA == 1) & (df.folB == 1) & (df.txwin < 1e-9) & (df.eff > 1 - 1e-9)]
    refs = R.reference_splits(inst)
    out = dict(n=int(len(d)), A_payment=d.bA.value_counts().sort_index().to_dict(), exact={'vn': 0, 'es': 0, 'ep': 0, 'other': 0})
    for _, r in d.iterrows():
        out['exact'][R.split_class(inst, int(r.bA), int(r.bB))] += 1
    out['mean_L1_to_nearest_ref'] = float(np.mean([min(abs(r.bA - ra) + abs(r.bB - rb) for ra, rb in refs.values()) for _, r in d.iterrows()])) if len(d) else None
    d2 = d[d.core == 1]
    out['n_core'] = int(len(d2))
    out['A_payment_core'] = d2.bA.value_counts().sort_index().to_dict()
    out['exact_core'] = {'vn': 0, 'es': 0, 'ep': 0, 'other': 0}
    for _, r in d2.iterrows():
        out['exact_core'][R.split_class(inst, int(r.bA), int(r.bB))] += 1
    # per-run plurality of the exact classes among core islands
    return out


def cell_table(name):
    d, df = load(name)
    if d is None:
        return None
    cell = d['cell']; inst = cell['inst']; v = C.INSTANCES[inst]; mr = C.min_revenue(v)
    out = dict(name=name, group=cell['group'], inst=inst, space=cell['space'], arm=cell['arm'], m=cell['m'], ptype=cell['ptype'], itype=cell['itype'],
               rain_kind=cell['rain_kind'], rain_roles=cell['rain_roles'], N=cell['N'], gens=cell['gens'], n_runs=d['n_runs'], n_islands=int(len(df)), min_revenue=mr)
    for col in ('core_enc', 'core', 'edge', 'eroded', 'eff', 'rev'):
        out[col], out[col + '_sd'] = frac_sd(df, col)
    out['core_gap_enc_minus_island'] = out['core_enc'] - out['core']
    out['rev_minus_min'] = out['rev'] - mr
    out['prior_mean_threat'] = d['prior_mean_threat']
    out['threat'], out['threat_sd_runs'] = frac_sd(df, 'threat')
    out['threat_shift'] = out['threat'] - d['prior_mean_threat']
    out['tx_share_P'] = float(df.txshP.mean()); out['fol_share_A'] = float(df.folshA.mean()); out['fol_share_B'] = float(df.folshB.mean())
    out['fixed_all'] = float(((df.fixP == 1) & (df.fixA == 1) & (df.fixB == 1)).mean())
    out['fixed_items'] = float(((df.fixA == 1) & (df.fixB == 1)).mean())
    out['txwin_end'] = float(df.txwin.mean())
    q = df[df.qual == 1]
    out['n_qual'] = int(len(q)); out['txwin_qual_end'] = float(q.txwin.mean()) if len(q) else None
    out['txwin_qual_post'] = float(q.txwin_post.mean()) if len(q) and q.txwin_post.notna().any() else None
    out['txwin_qual_pre'] = float(q.txwin_pre.mean()) if len(q) and q.txwin_pre.notna().any() else None
    out['txwin_pre_all'] = float(df.txwin_pre.mean()) if df.txwin_pre.notna().any() else None
    out['txwin_post_all'] = float(df.txwin_post.mean()) if df.txwin_post.notna().any() else None
    # complementary vs non-complementary follower pairs (fixed followers in both item roles and fixed TX in P)
    ff = df[(df.fixA == 1) & (df.fixB == 1) & (df.folA == 1) & (df.folB == 1) & (df.txP == 1) & (df.fixP == 1)]
    if len(ff):
        dsum = ff.kA.map(delta_of) + ff.kB.map(delta_of)
        comp = ff[dsum == 10]; nonc = ff[dsum != 10]
        out['ff_n'] = int(len(ff)); out['ff_comp_n'] = int(len(comp)); out['ff_comp_txwin'] = float(comp.txwin.mean()) if len(comp) else None
        out['ff_noncomp_n'] = int(len(nonc)); out['ff_noncomp_txwin'] = float(nonc.txwin.mean()) if len(nonc) else None
        out['ff_comp_core'] = float(comp.core_enc.mean()) if len(comp) else None
        out['ff_noncomp_core'] = float(nonc.core_enc.mean()) if len(nonc) else None
    fi = df.t_fix_items[df.t_fix_items >= 0]; fa = df.t_fix_all[df.t_fix_all >= 0]
    out['t_fix_items_median'] = float(fi.median()) if len(fi) else None; out['t_fix_items_frac'] = float((df.t_fix_items >= 0).mean())
    out['t_fix_all_median'] = float(fa.median()) if len(fa) else None; out['t_fix_all_frac'] = float((df.t_fix_all >= 0).mean())
    out['rrain_mean'] = float(df.rrain.mean()); out['rmig_mean'] = float(df.rmig.mean())
    out['split'] = split_table(inst, df)
    tp = float(df.tested_pop.sum()); xp = float(df.tx_pop.sum())
    out['bluff'] = dict(tx_pop=xp, tested_pop=tp, tested_bluff=float(df.tested_bluff_pop.sum()), untested_bluff=float(df.untested_bluff_pop.sum()),
                        bluff_pop=float(df.bluff_pop.sum()),
                        tested_bluff_share_of_tested=(float(df.tested_bluff_pop.sum()) / tp) if tp > 0 else None,
                        untested_bluff_share_of_untested=(float(df.untested_bluff_pop.sum()) / (xp - tp)) if xp - tp > 0 else None,
                        bluff_share_of_tx=(float(df.bluff_pop.sum()) / xp) if xp > 0 else None)
    sm = d['series_mean']; smp = d['samples']
    out['series_at'] = {str(t): dict(core_enc=sm['core_enc'][i], core=sm['core'][i], threat=sm['threat'][i], tx_share_P=sm['tx_share_P'][i], txwin=sm['txwin'][i],
                                     dTX=sm['dTX'][i], fixed_items=sm['fixed_items'][i], fol_A=sm['fol_share_A'][i], rev=sm['rev'][i], eff=sm['eff'][i])
                        for i, t in enumerate(smp) if t in (0, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000)}
    thp = np.array(d['threat_dist_prior']); the = np.array(d['threat_dist_end_pooled']); the = the / the.sum()
    out['threat_hist'] = dict(prior=[round(x, 4) for x in thp.tolist()], end=[round(x, 4) for x in the.tolist()])
    out['order_match'] = all(d['order_match'])
    out['seconds'] = d['seconds_total']
    return out


def main():
    stat = json.load(open(os.path.join(OUT, 'statics.json')))
    tabs = {}
    for name in R.CELLS:
        t = cell_table(name)
        if t is not None:
            tabs[name] = t
    json.dump(tabs, open(os.path.join(OUT, 'tables.json'), 'w'), indent=1, default=str)
    cols = ['name', 'inst', 'space', 'arm', 'm', 'ptype', 'itype', 'rain_kind', 'rain_roles', 'N', 'n_runs', 'core_enc', 'core', 'core_gap_enc_minus_island', 'edge', 'eroded',
            'eff', 'rev', 'threat', 'threat_shift', 'tx_share_P', 'fol_share_A', 'fol_share_B', 'fixed_all', 'fixed_items', 'txwin_end', 'n_qual', 'txwin_qual_end',
            't_fix_items_median', 't_fix_all_median', 'rrain_mean', 'rmig_mean', 'order_match']
    with open(os.path.join(OUT, 'table_cells.csv'), 'w') as f:
        w = csv.writer(f); w.writerow(cols)
        for t in tabs.values():
            w.writerow([round(t[c], 4) if isinstance(t.get(c), float) else t.get(c) for c in cols])
    # ------------------------------------------------------------------ digest
    def g(name):
        return tabs.get(name)
    print('cells', len(tabs))
    for name, t in tabs.items():
        print('%-34s core_enc %.3f core %.3f eroded %.3f eff %.3f rev %.2f threat %.2f (shift %+.2f) txP %.2f folA %.2f fixedAll %.2f qual %d txwin_q %s' % (
            name, t['core_enc'], t['core'], t['eroded'], t['eff'], t['rev'], t['threat'], t['threat_shift'], t['tx_share_P'], t['fol_share_A'], t['fixed_all'], t['n_qual'],
            ('%.4f' % t['txwin_qual_end']) if t['txwin_qual_end'] is not None else '-'))
    return tabs, stat


def verdicts(tabs, stat):
    """the numbers behind each registered prediction (printed; the verdict words are written in runs/core-stage2.md)."""
    g = tabs.get
    print('\n=== P1 statics')
    for k, v in stat['prediction1'].items():
        print(k, 'efficient complementary at t = vP:', v['n_efficient'], 'max offset', v['max_offset_efficient'], 'more than 2 off', v['n_efficient_more_than_2_off'],
              'ties', v['n_tie'], 'TX wins', v['n_txwin'])
    print('order check', {k: (v['python_order_mismatch'], v['numba_vs_python_mismatch'], v['tensor_B_equal']) for k, v in stat['order'].items()})
    print('\n=== P2 primary, threshold no-overbid eps = 0 m = 0.5')
    t = g('p_threshold_no-overbid_zero_m50'); c = g('vi_threshold_no-overbid_zero')
    if t and c:
        print('core_enc %.3f (sd %.3f) island-mean core %.3f ; shift %.2f (prior mean %.2f, end %.2f) ; matched shift %.2f (ratio %.2f)' % (
            t['core_enc'], t['core_enc_sd'], t['core'], t['threat_shift'], t['prior_mean_threat'], t['threat'], c['threat_shift'], c['threat_shift'] / t['threat_shift']))
    for n in ('p_threshold_no-overbid_zero_m20', 'p_threshold_unrestricted_zero_m50', 'p_asymmetric_no-overbid_zero_m50', 'p_skew_no-overbid_zero_m50', 'i_threshold_zero', 'ii_threshold_zero'):
        if g(n):
            print('  ', n, 'core_enc %.3f core %.3f shift %.2f' % (g(n)['core_enc'], g(n)['core'], g(n)['threat_shift']))
    print('\n=== P3 shadow (qualifying islands)')
    for n in [k for k in tabs if tabs[k]['arm'] in ('zero', 'ann3') and tabs[k]['group'] == 'primary' or k.startswith('vii_')]:
        t = tabs[n]
        print('  %-36s n_qual %5d txwin_end %s post %s pre %s | comp n %s txwin %s | noncomp n %s txwin %s' % (
            n, t['n_qual'], t['txwin_qual_end'], t['txwin_qual_post'], t['txwin_qual_pre'], t.get('ff_comp_n'), t.get('ff_comp_txwin'), t.get('ff_noncomp_n'), t.get('ff_noncomp_txwin')))
    print('\n=== P4 rain')
    for n in ('p_threshold_no-overbid_rain_m50', 'p_threshold_no-overbid_rain_m20', 'p_threshold_unrestricted_rain_m50', 'iv_threshold_m50', 'ivb_threshold_m50', 'ivp_P_threshold_m50',
              'ivp_items_threshold_m50', 'iii_threshold_no-overbid_rain', 'vi_threshold_rain', 'i_threshold_rain', 'ii_threshold_rain', 'iv_threshold_m20', 'ivb_threshold_m20',
              'ivp_P_threshold_m20', 'ivp_items_threshold_m20'):
        if g(n):
            t = g(n)
            print('  %-36s core(island-mean) %.3f core_enc %.3f (sd %.3f) eroded %.3f eff %.3f rev %.2f threat %.2f txP %.2f folA %.2f fixedAll %.2f txwin %.3f' % (
                n, t['core'], t['core_enc'], t['core_sd'], t['eroded'], t['eff'], t['rev'], t['threat'], t['tx_share_P'], t['fol_share_A'], t['fixed_all'], t['txwin_end']))
    print('\n=== P5 order-free dynamic check')
    bad = [n for n, t in tabs.items() if not t['order_match']]
    print('cells', len(tabs), 'order mismatch in', bad)
    print('\n=== P6 split (skew)')
    for n in [k for k in tabs if tabs[k]['inst'] == 'skew' and tabs[k]['group'] in ('primary', 'control_i', 'control_ii', 'control_vi')]:
        t = tabs[n]; sp = t['split']
        print('  %-34s n %5d exact %s A payments %s | core n %d exact %s' % (n, sp['n'], sp['exact'], dict(list(sp['A_payment'].items())[:15]), sp['n_core'], sp['exact_core']))
    print('\n=== P7 bluffs')
    for n in [k for k in tabs if tabs[k]['space'] == 'unrestricted']:
        b = tabs[n]['bluff']
        print('  %-36s tx_pop %.0f tested %.0f tested bluffs %.0f untested bluffs %.0f ; tested bluff share of tested %s ; bluff share of TX %s' % (
            n, b['tx_pop'], b['tested_pop'], b['tested_bluff'], b['untested_bluff'], b['tested_bluff_share_of_tested'], b['bluff_share_of_tx']))


if __name__ == '__main__':
    tabs, stat = main()
    verdicts(tabs, stat)
