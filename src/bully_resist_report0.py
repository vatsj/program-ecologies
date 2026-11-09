"""Report of step 0 of queue 76 (assays and holding configurations).

    python3 src/bully_resist_report0.py ASSAYS.json[.gz] HOLD.json OUT.json OUT.md
"""
import sys, json, gzip, collections


def load(p):
    return json.load(gzip.open(p, 'rt')) if p.endswith('.gz') else json.load(open(p))


def fmt(x):
    if x is None:
        return '-'
    if x != 0 and (abs(x) < 1e-3 or abs(x) >= 1e4):
        return '%.2g' % x
    return '%.3g' % x


def hold_stats(hold):
    CL = 'FUGWD'
    out = {}
    for beta in ('1.0', '3.0'):
        cells = [c for c in hold['cells'] if c['spec'].split(':b=')[1] == beta]
        nI = 0; endU = 0; endU_bully = 0; endU_third = 0; endU_bully_third = 0; endU_none = 0; endU_U30 = 0
        endF = 0; endF_reader = 0; endF_bully = 0
        t = collections.Counter(); topU = collections.Counter(); topFU = collections.Counter(); topF = collections.Counter()
        for c in cells:
            for (c30, c120, d30, d120) in c['islands']:
                nI += 1
                t[(CL[c30], CL[c120])] += 1
                has_b = any(x in ('Bn', 'Bp') for x in d120)
                has_t = any(x in ('C0', 'C3') for x in d120)
                if c120 == 1:
                    endU += 1; endU_bully += has_b; endU_third += has_t; endU_bully_third += (has_b and has_t)
                    endU_none += (not has_b); endU_U30 += (c30 == 1)
                    topU[tuple(d120)] += 1
                    if c30 == 0:
                        topFU[tuple(d120)] += 1
                if c120 == 0:
                    endF += 1
                    topF[tuple(d120)] += 1
                    endF_reader += any(x[0] in 'SDXPO' for x in d120)
                    endF_bully += has_b
        out[beta] = dict(islands=nI, transitions={'%s>%s' % k: v for k, v in sorted(t.items())}, end_unequal=endU,
                         share_with_bully=endU / max(endU, 1) and endU_bully / max(endU, 1), share_with_third_constant=endU_third / max(endU, 1),
                         share_bully_and_third=endU_bully_third / max(endU, 1), share_constants_only=endU_none / max(endU, 1),
                         share_already_unequal_at_30N=endU_U30 / max(endU, 1), fair_to_unequal=sum(topFU.values()),
                         end_fair=endF, end_fair_share_with_reader=endF_reader / max(endF, 1), end_fair_share_with_bully=endF_bully / max(endF, 1),
                         top_unequal=topU.most_common(12), top_fair_to_unequal=topFU.most_common(6), top_fair=topF.most_common(8))
    out['v_check'] = dict(cells=len(hold['cells']), mismatches=sum(1 for c in hold['cells'] if c['stored_vstar'] is None or abs(c['vstar'] - c['stored_vstar']) > 1e-9))
    return out


def md_assays(A):
    L = []
    S = A['item2_summary']
    L.append('### Items 2, 4, 5: exact invasion assays (rho * N; 1 = neutral; scoring statistic = exact value)')
    L.append('')
    L.append('| family | class | resident triples | assays | median | share <= 1 | neutral share [0.5, 3] | share > 3 | max |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    names = {'FI': 'FI (bully into fair reader islands)', 'FC': 'FC (bully into pair + constant)', 'UB': 'UB (reader into bully-held unequal)',
             'BF': 'BF (1/3 constants into bully-held fair)'}
    for fam in ('firm', 'firm_single', 'firm_two', 'Pz', 'Po', 'Q', 'O'):
        for k in ('FI', 'FC', 'UB', 'BF'):
            v = S[fam][k]; a = v['all']
            if a['n'] == 0:
                continue
            L.append('| %s | %s | %d | %d | %s | %.2f | %.2f | %.2f | %s |' % (fam, names[k], v['n_resident'], a['n'], fmt(a['median']), a['share_le_1'],
                                                                           a['share_neutral'], a['share_gt3'], fmt(a['max'])))
    L.append('')
    L.append('By slot role of the invasion (pair = a member of the resident outcome, out = the unpaired slot), medians of rho * N [share > 3]:')
    L.append('')
    L.append('| family | class | pair slot | unpaired slot |')
    L.append('|---|---|---|---|')
    for fam in ('firm', 'firm_single', 'firm_two', 'Pz', 'Po', 'Q', 'O'):
        for k in ('FI', 'FC', 'UB', 'BF'):
            v = S[fam][k]
            if v['all']['n'] == 0:
                continue
            br = v['by_role']
            cell = lambda r: ('%s [%.2f]' % (fmt(br[r]['median']), br[r]['share_gt3'])) if r in br else '-'
            L.append('| %s | %s | %s | %s |' % (fam, k, cell('pair'), cell('out')))
    return L


def verdicts0(A):
    S = A['item2_summary']
    med = lambda f, k: S[f][k]['all'].get('median')
    shr = lambda f, k: S[f][k]['all'].get('share_gt3')
    v = {}
    v['RE1_clauseA_fires_FI'] = med('firm', 'FI') > 3
    v['RE1_clauseA_fires_FC'] = med('firm', 'FC') > 3
    v['RE1_clauseB_fires'] = med('firm', 'UB') > 3
    v['RE1_UB_median_le_1'] = med('firm', 'UB') <= 1
    v['RE1_holds'] = (not v['RE1_clauseA_fires_FI']) and (not v['RE1_clauseA_fires_FC']) and (not v['RE1_clauseB_fires']) and v['RE1_UB_median_le_1']
    v['RE1_mixed_shares_gt3'] = dict(FI=shr('firm', 'FI'), FC=shr('firm', 'FC'), UB=shr('firm', 'UB'))
    v['RE1_mixed'] = v['RE1_holds'] and any(x > 0.10 for x in v['RE1_mixed_shares_gt3'].values())
    v['argon_a'] = (0.5 <= med('firm', 'FI') <= 3) and v['RE1_UB_median_le_1']
    # sol (b): medians or shares differ across invader family or slot role by > 3x, or neutrality and persistence both present
    roles = S['firm']['FC']['by_role']
    meds = [roles[r]['median'] for r in roles]
    fam_meds = [S['firm_single']['FI']['all']['median'], S['firm_two']['FI']['all']['median'], S['firm_single']['FC']['all']['median'], S['firm_two']['FC']['all']['median']]
    ratio_role = max(meds) / max(min(meds), 1e-300)
    ratio_fam = max(fam_meds) / max(min(fam_meds), 1e-300)
    neutral_present = S['firm']['FI']['all']['share_neutral'] > 0.5
    persistence = S['firm']['UB']['all']['share_le_1'] > 0.9
    v['sol_b'] = dict(role_ratio=ratio_role, family_ratio=ratio_fam, neutrality_and_persistence=neutral_present and persistence,
                      value=(ratio_role > 3 or ratio_fam > 3 or (neutral_present and persistence)))
    v['E1a_UB_share_le_1'] = S['firm']['UB']['all']['share_le_1']
    v['E1b_FI_share_neutral'] = S['firm']['FI']['all']['share_neutral']
    v['E1_holds'] = v['E1a_UB_share_le_1'] >= 0.9 and v['E1b_FI_share_neutral'] >= 0.6
    return v


def md_hold(H):
    L = ['### Item 3: holding configurations (rerun of queue 75, N = 200, I = 64, delta in {1e-3, 1e-2, 1e-1}, 20 runs per cell; V* identical to the stored rows in %d of %d cells)' % (
        H['v_check']['cells'] - H['v_check']['mismatches'], H['v_check']['cells']), '']
    for b in ('1.0', '3.0'):
        h = H[b]
        L.append('beta = %s: %d islands; transitions (class at 30N > class at 120N) %s' % (b, h['islands'], h['transitions']))
        L.append('- islands ending unequal: %d; with a bully in the dominant triple %.3f, with a 1/3-naming constant (C0, C3) %.3f, with both %.3f, constants only %.3f; already unequal at 30N: %.3f; fair at 30N and unequal at 120N: %d' % (
            h['end_unequal'], h['share_with_bully'], h['share_with_third_constant'], h['share_bully_and_third'], h['share_constants_only'],
            h['share_already_unequal_at_30N'], h['fair_to_unequal']))
        L.append('- most frequent dominant triples (slot 0, 1, 2) on islands ending unequal: ' + '; '.join('%s x%d' % ('/'.join(t), n) for t, n in h['top_unequal'][:8]))
        L.append('- fair at 30N and unequal at 120N: ' + '; '.join('%s x%d' % ('/'.join(t), n) for t, n in h['top_fair_to_unequal']))
        L.append('- islands ending fair: %d, with a reader in the dominant triple %.3f, with a bully %.3f; most frequent: %s' % (
            h['end_fair'], h['end_fair_share_with_reader'], h['end_fair_share_with_bully'], '; '.join('%s x%d' % ('/'.join(t), n) for t, n in h['top_fair'][:5])))
        L.append('')
    return L


if __name__ == '__main__':
    A = load(sys.argv[1]); Hh = load(sys.argv[2])
    H = hold_stats(Hh)
    V = verdicts0(A)
    out = dict(hold=H, verdicts=V, item1_counts=A['item1_counts'], item1_unequal=dict(n=A['item1_unequal_bully_on_2_3']['n'], by_victim=A['item1_unequal_bully_on_2_3']['by_victim']),
               item1_fair=dict(n=A['item1_fair_pair_bully_and_reader']['n'], by_reader_family=A['item1_fair_pair_bully_and_reader']['by_reader_family']),
               item2_summary=A['item2_summary'], mc_check=A['mc_check'], neutral_twin=A['neutral_twin'], kernel_check={k: v for k, v in A['kernel_check'].items() if k != 'rows'})
    json.dump(out, open(sys.argv[3], 'w'), default=str)
    L = ['## Step 0', '', '### Item 1: outcome table over (bully, firm reader, constant), all slot orders (%s triples)' % sum(A['item1_counts'].values()), '']
    L.append('classes by (bully, reader family): ' + '; '.join('%s %d' % (k.replace('|', ' / '), v) for k, v in A['item1_counts'].items()))
    L.append('')
    L.append('Triples with the bully on an unequal pair at 2/3: %d (victim: %s). Triples with the bully and a firm reader on a fair pair: %d (%s).' % (
        A['item1_unequal_bully_on_2_3']['n'], A['item1_unequal_bully_on_2_3']['by_victim'], A['item1_fair_pair_bully_and_reader']['n'], A['item1_fair_pair_bully_and_reader']['by_reader_family']))
    L.append('')
    L += md_assays(A)
    L.append('')
    mc = A['mc_check']; nt = A['neutral_twin']; kc = A['kernel_check']
    L.append('Checks: jump-chain Monte Carlo (10^4 trials) of %d assays, max |z| %.2f, share above 3 %.4f, no persisting trial; neutral twin fixation %.5f +- %.5f against 1/N = %.3f; full kernel on %d non-neutral assays (3,000 islands each) max |z| %.2f.' % (
        mc['n'], mc['max_abs_z'], mc['share_abs_z_gt3'], nt['fixation_mean'], nt['fixation_se'], nt['one_over_N'], kc['n'], kc['max_abs_z']))
    L.append('')
    L += md_hold(H)
    L.append('')
    L.append('### Scoring (rules fixed in the predictions file)')
    L.append('')
    L.append('```')
    L.append(json.dumps(V, indent=1, default=str))
    L.append('```')
    open(sys.argv[4], 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))
