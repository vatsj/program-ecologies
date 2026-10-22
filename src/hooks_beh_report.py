"""Behavioural hooks: summary tables and verdicts from runs/hooks_beh/* -> runs/hooks-beh.md and runs/hooks-beh.json
(predictions/2026-10-21-behavioural-hooks.md).  Every number is a finite-(N, I, horizon) lottery statistic at eps = 0, not pi."""
import os, sys, json, gzip, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import hooks_beh_run as R

OUT = R.OUT
CL = R.CLASS_NAMES
OR = R.ORIGIN_NAMES


def load(cell):
    p, pz = R._path(cell)
    if os.path.exists(pz):
        rows = json.load(gzip.open(pz))
    elif os.path.exists(p):
        rows = json.load(open(p))
    else:
        return []
    return sorted([r for r in rows if 'error' not in r], key=lambda r: r['rep'])


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def uo(rows):
    v = [bool(r['universal_open']) for r in rows]
    return sum(v), len(v)


def fmt_uo(rows):
    k, n = uo(rows)
    if n == 0:
        return 'not run'
    return '%d/%d = %.3f %s' % (k, n, k / n, wilson(k, n))


def mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else float('nan')


def paired_diff(a, b):
    """Run-level difference in the share of universal-open runs (paired by run index)."""
    da = {r['rep']: bool(r['universal_open']) for r in a}
    db = {r['rep']: bool(r['universal_open']) for r in b}
    reps = sorted(set(da) & set(db))
    if not reps:
        return None
    return float(np.mean([da[x] for x in reps]) - np.mean([db[x] for x in reps]))


def ts_at(row, gen):
    for t in row['ts']:
        if t['gen'] == gen:
            return t
    return None


def class_shares(rows, gen):
    """Run-averaged share of individuals per class at generation gen, and the origin split of the (class, origin) table."""
    cs = []; tabs = []
    for r in rows:
        t = ts_at(r, gen)
        if t is None or t.get('cls') is None:
            continue
        c = np.array(t['cls']); cs.append(c.sum(0) / c.sum())
        tabs.append(np.array(t['tab']))
    if not cs:
        return None, None
    return np.mean(cs, 0), np.sum(tabs, 0)


def win_class_counts(rows, gen):
    """Class counts on islands efficient at that generation (pcc >= 0.95 at the record), summed over runs."""
    tot = np.zeros(8, np.int64); nisl = 0
    for r in rows:
        t = ts_at(r, gen)
        if t is None or t.get('cls') is None:
            continue
        c = np.array(t['cls']); eff = np.array(t['isl_pcc']) >= 0.95
        tot += c[eff].sum(0); nisl += int(eff.sum())
    return tot, nisl


def prod5(rows):
    """Production (class-changing writes, copies and contracts into the class) and births of the two classes, summed over runs."""
    conv = np.sum([np.array(r['conv']) for r in rows], 0)
    prod = conv[:4].sum((0, 1, 2)).copy(); np.fill_diagonal(prod, 0)
    births = conv[4].sum((0, 1))
    return ('; production events into FairBot-eq %d, PrudentBot-eq %d; births with a FairBot-eq child %d, PrudentBot-eq child %d (births are the reproductive output; '
            'class shares by generation are in M1)' % (prod[:, 0].sum(), prod[:, 1].sum(), births[:, 0].sum(), births[:, 1].sum()))


def md_table(head, rows):
    out = '| ' + ' | '.join(head) + ' |\n|' + '---|' * len(head) + '\n'
    for r in rows:
        out += '| ' + ' | '.join(str(x) for x in r) + ' |\n'
    return out


def main():
    cells = {c: load(c) for c in R.CELLS}
    J = {}
    L = []
    P = L.append
    P('# Behavioural hooks: verdicts (run 2026-10-21)\n')
    P('Spec `specs/2026-10-21-behavioural-hooks.md`; predictions `predictions/2026-10-21-behavioural-hooks.md` (with the addendum of the '
      'gate); notes `notes/hooks-beh.md`. All numbers are finite-(N, I, horizon) lottery statistics at eps = 0 over runs paired by index, '
      'not pi. Universal-open = every island efficient (P(C,C) >= 0.95) and every pair of island-majority types cooperating as strangers; '
      'Wilson 95% intervals in brackets.\n')
    # ---------------------------------------------------------------- cell table
    rows = []
    for c, rr in cells.items():
        if not rr:
            continue
        rows.append([c, len(rr), fmt_uo(rr), '%.3f' % mean([r['eff_islands'] for r in rr]), '%.3f' % mean([r['pcc'] for r in rr]),
                     '%.3f' % mean([r['lineage_closed'] for r in rr]), '%.0f' % mean([r['wall'] for r in rr]),
                     sum(r['overflow'] for r in rr)])
        J[c] = dict(n=len(rr), universal_open=uo(rr), eff_islands=mean([r['eff_islands'] for r in rr]), pcc=mean([r['pcc'] for r in rr]))
    P('## Cells\n')
    P(md_table(['cell', 'runs', 'universal-open', 'efficient islands', 'P(C,C)', 'lineage-closed', 'wall s/run', 'overflow'], rows))
    V = {}

    def verdict(num, held, text, number):
        V[num] = (held, text, number)

    A = lambda c: cells.get(c, [])
    # ---------------------------------------------------------------- 2
    bm = A('beh-max')
    if bm:
        k, n = uo(bm); p = k / n
        inert = A('inert'); om_ = A('open-max')
        verdict(2, 'held' if p >= 0.75 else ('failed' if p < 0.5 else 'partial'), 'beh-max universal-open >= 0.75 [< 0.5]',
                '%d/%d = %.3f; same-geometry references: open-max %s, inert-hooks %s' % (k, n, p, fmt_uo(om_) if om_ else 'not run', fmt_uo(inert) if inert else 'not run'))
    # ---------------------------------------------------------------- 3
    if bm:
        thr = []; anyp = []
        for r in bm:
            t = np.array(r['final']['win_tab'])
            tot = t.sum()
            if tot:
                thr.append(t[[0, 1], 1:, :].sum() / tot); anyp.append(t[[0, 1]].sum() / tot)
        x = mean(thr)
        verdict(3, 'held' if x >= 0.5 else ('failed' if x < 0.3 else 'partial'),
                'FairBot/PrudentBot-equivalent through a fill on winning islands at the end >= 50% [< 30%]',
                '%.3f through a fill (%.3f counting unhooked FairBot-equivalents)' % (x, mean(anyp)))
    # ---------------------------------------------------------------- 4
    hs = {}
    for c in ('beh-max', 'beh-max-hostile'):
        rr = A(c)
        if rr:
            hs[c] = (mean([np.mean(r['hostile_founded']) for r in rr]), mean([r['final']['hostile_share'] for r in rr]),
                     mean([r['final']['hostile_share_win'] for r in rr]))
    if hs:
        ok_f = all(v[0] >= 0.9 for v in hs.values())
        ok_e = all(v[1] < 0.05 for v in hs.values())
        bad = hs.get('beh-max-hostile', (0, 0, 0))[1] >= 0.20
        verdict(4, 'held' if (ok_f and ok_e) else ('failed' if bad else 'partial'),
                'hostile keys founded on >= 90% of islands and held by < 5% at the end under both priors [>= 20% under the hostile prior]',
                '; '.join('%s: founded %.3f of islands, held at end %.4f (winning islands %.4f)' % (c, *v) for c, v in hs.items()))
    # ---------------------------------------------------------------- 5
    if bm:
        tot, nisl = win_class_counts(bm, 200)
        fb, pb, cb, tb = int(tot[0]), int(tot[1]), int(tot[2]), int(tot[4])
        shares, tab = class_shares(bm, 200)
        verdict(5, 'held' if (pb > fb and (cb + tb) > 0) else 'failed',
                'PrudentBot-equivalents outnumber FairBot-equivalents on winning islands at generation 200, with TrustingBots and CooperateBots still present [fewer]',
                'winning-island individuals at 200 (summed over runs, %d islands): FairBot-eq %d, PrudentBot-eq %d, CooperateBot-like %d, TrustingBot-like %d; the counter-prediction (FairBot-eq > PrudentBot-eq) %s'
                % (nisl, fb, pb, cb, tb, 'held' if fb > pb else 'did not hold') + prod5(bm))
    # ---------------------------------------------------------------- 6, 7
    na = A('beh-max-noA')
    if na:
        k, n = uo(na); p = k / n
        inert = A('inert')
        verdict(6, 'held' if p <= 0.70 else ('failed' if p >= 0.85 else 'partial'), 'beh-max-noA <= 0.70 universal-open [>= 0.85]',
                '%d/%d = %.3f (inert-hooks control at this geometry %s; beh-max %s)' % (k, n, p, fmt_uo(inert) if inert else 'not run', fmt_uo(bm) if bm else 'not run'))
    ff = A('ff-beh-max')
    if ff:
        k, n = uo(ff); p = k / n
        verdict(7, 'held' if p >= 0.9 else ('failed' if p < 0.7 else 'partial'), 'ff-beh-max >= 0.9 [< 0.7]',
                '%d/%d = %.3f (a cell cut at 6 of 10 planned runs for cost; the stored legacy ff-open-max at the stored geometry was 20/20)' % (k, n, p))
    # ---------------------------------------------------------------- 8
    th = A('M-thanks-only')
    parts = []
    held8 = []
    if th:
        sh = []
        for r in th:
            t = ts_at(r, 200)
            if t and t.get('tab') is not None:
                tab = np.array(t['tab'])
                fbtab = tab[0]
                tot = fbtab.sum()
                if tot:
                    sh.append(fbtab[2, 1] / tot)                                   # thanks fills with a copy in their ancestry
        x = mean(sh)
        parts.append('copy-ancestry share of FairBot-equivalents carrying a thanks fill at 200: %.3f' % x)
        held8.append(x >= 0.5)
    pu = lambda c: (uo(A(c))[0] / uo(A(c))[1]) if A(c) else float('nan')
    for c, rule, ok in (('M3a-thanks-noinherit', '>= 0.85', lambda p: p >= 0.85), ('M3b-thanks-nocopy', '<= 0.70', lambda p: p <= 0.70),
                        ('M3c-thanks-neither', '<= 0.70', lambda p: p <= 0.70)):
        if A(c):
            parts.append('%s %s (needs %s)' % (c, fmt_uo(A(c)), rule)); held8.append(ok(pu(c)))
    for c in ('M3d-thanks-noevict', 'M3e-thanks-single'):
        if A(c) and th:
            d = paired_diff(A(c), th)
            parts.append('%s %s, difference to M-thanks-only %+.3f (needs within 0.1; falsified by a fall of more than 0.2)' % (c, fmt_uo(A(c)), d))
            held8.append(abs(d) <= 0.1)
    if parts:
        cs = x if th else float('nan')
        m3b = pu('M3b-thanks-nocopy')
        falsified = (cs < 0.25) or (m3b >= 0.9)          # the spec's stated falsifier for the copy-carrier clause
        parts.append('stated falsifier (copy share below 25%% or M3b >= 0.9) %s' % ('TRIPPED' if falsified else 'not tripped'))
        verdict(8, 'held' if all(held8) else ('failed' if falsified else 'partial'), 'contagion (H1): copying is the carrier; inheritance, eviction and multi-hook programs are not',
                '; '.join(parts) + '; clauses held: ' + ', '.join(['copy-ancestry share', 'M3a', 'M3b', 'M3c', 'M3d', 'M3e'][i] for i, h in enumerate(held8) if h))
    # ---------------------------------------------------------------- 9
    gr = A('M-grudge-only')
    if gr:
        conv = np.sum([np.array(r['conv']) for r in gr], 0)          # [event][evicted][multi][from][to]
        g = conv[1].sum((0, 1))                                      # grudge writes: [from, to]
        changed = g.copy(); np.fill_diagonal(changed, 0)
        tot = changed.sum()
        fr = changed.sum(1) / tot if tot else np.zeros(8)
        failed_maj = []
        for r in gr:
            t = ts_at(r, r['gens'])
            if t is None or t.get('cls') is None:
                continue
            c = np.array(t['cls']); isl = np.array(t['isl_pcc'])
            for i in np.where(isl < 0.95)[0]:
                failed_maj.append(int(np.argmax(c[i])))
        db = float(np.mean([x == 3 for x in failed_maj])) if failed_maj else float('nan')
        cbf = fr[2]
        fr_f = []; fr_w = []
        for r in gr:
            t = ts_at(r, r['gens'])
            if t is None or t.get('cls') is None:
                continue
            c = np.array(t['cls']); isl = np.array(t['isl_pcc'])
            for i in range(len(isl)):
                (fr_f if isl[i] < 0.95 else fr_w).append(c[i, 3] / c[i].sum())
        fringe = 'DefectBot-like share on failed islands %.3f against %.3f on efficient ones' % (mean(fr_f), mean(fr_w))
        verdict(9, 'held' if (cbf >= 0.5 and (db >= 0.5)) else ('failed' if not (db >= 0.5) else 'partial'),
                'grudge writes convert CooperateBot-like carriers (suckers); DefectBot-like majorities hold the failed islands [failed islands have no DefectBot-like majority]',
                'from-class of class-changing grudge writes: %s; failed-island majority class DefectBot-like on %.3f of %d failed island-records (universal-open %s)'
                % (', '.join('%s %.3f' % (CL[i], fr[i]) for i in range(8) if fr[i] > 0.005), db, len(failed_maj), fmt_uo(gr)) + '; first clause (converted carriers are CooperateBot-like): ' + ('held' if cbf >= 0.5 else 'failed') + '; ' + fringe)
    # ---------------------------------------------------------------- 10, 11
    om = A('M-open-max')
    e4 = A('M4-early'); l4 = A('M4-late')
    if e4 and om:
        pe = uo(e4)[0] / uo(e4)[1]; po = uo(om)[0] / uo(om)[1]
        ratio = pe / po if po > 0 else float('nan')
        verdict(10, 'held' if ratio >= 0.8 else ('failed' if ratio < 0.5 else 'partial'),
                'writes in generations 0-50 alone recover >= 80% of open-max universal-open [< 50%]',
                'M4-early %s vs M-open-max %s (ratio %.3f); M4-late %s' % (fmt_uo(e4), fmt_uo(om), ratio, fmt_uo(l4) if l4 else 'not run'))
    sh_ = A('M5-sham')
    if sh_:
        k, n = uo(sh_); p = k / n
        verdict(11, 'held' if p <= 0.70 else ('failed' if p >= 0.85 else 'partial'), 'sham writes (unconditioned, matched keys) <= 0.70 universal-open [>= 0.85]',
                '%d/%d = %.3f (beh-max %s)' % (k, n, p, fmt_uo(bm) if bm else 'not run'))
    P('\n## Prediction verdicts\n')
    names = {1: 'statics (the gate table)'}
    P('1. *Statics.* Held, with the PrudentBot reading fixed by the RE (d-clause under box1): FairBot defects against TrustingBot, '
      'the Godel predator cooperates with itself and is suckered by FairBot, PrudentBot exploits TrustingBot and CooperateBot and cooperates '
      'with FairBot; the solver (vacuous box at world 0) and an independent reference agree on all 49 entries (`tools/beh_gate.py`). With the level-PA reading PrudentBot defects with FairBot (gate failed, addendum to the predictions).\n')
    for k in sorted(V):
        held, text, num = V[k]
        P('%d. **%s.** %s. %s\n' % (k, held.upper(), text, num))
    J['verdicts'] = {str(k): dict(verdict=v[0], text=v[1], number=v[2]) for k, v in V.items()}
    # ---------------------------------------------------------------- mechanism summary
    P('\n## Mechanism summary: ablations against their paired reference (universal-open share; difference = reference minus ablation is shown as ablation minus reference)\n')
    rows = []
    groups = (('M-thanks-only', ['M3a-thanks-noinherit', 'M3b-thanks-nocopy', 'M3c-thanks-neither', 'M3d-thanks-noevict', 'M3e-thanks-single']),
              ('M-open-max', ['M3a-max-noinherit', 'M3b-max-nocopy', 'M3c-max-neither', 'M3d-max-noevict', 'M3e-max-single', 'M4-early', 'M4-late']),
              ('beh-max', ['M5-sham', 'beh-max-noA', 'beh-max-hostile']),
              ('inert', ['open-max', 'M-open-max', 'M-thanks-only', 'M-grudge-only', 'beh-max', 'beh-written-only']))
    for ref, abl in groups:
        rr = A(ref)
        if not rr:
            continue
        rows.append(['**%s** (reference)' % ref, fmt_uo(rr), '', '%.3f' % mean([r['eff_islands'] for r in rr])])
        for c in abl:
            if A(c):
                d = paired_diff(A(c), rr)
                rows.append(['%s' % c, fmt_uo(A(c)), ('%+.3f' % d) if d is not None else '', '%.3f' % mean([r['eff_islands'] for r in A(c)])])
    P(md_table(['cell', 'universal-open', 'difference to the reference (paired by run)', 'efficient islands'], rows))
    # ---------------------------------------------------------------- M1 trajectories
    P('\n## M1: response classes against the fixed panel (share of individuals, run-averaged)\n')
    for c in ('beh-max', 'M-open-max', 'M-thanks-only', 'M-grudge-only'):
        rr = A(c)
        if not rr:
            continue
        P('\n### %s (%s)\n' % (c, fmt_uo(rr)))
        rows = []
        for g in (0, 10, 20, 50, 100, 200, 500, 1000):
            sh, tab = class_shares(rr, g)
            if sh is None:
                continue
            rows.append([g] + ['%.3f' % x for x in sh])
        P(md_table(['gen'] + list(CL), rows))
        sh, tab = class_shares(rr, 200)
        if tab is not None:
            rows = []
            for k in range(8):
                t = tab[k]
                if t.sum() == 0:
                    continue
                rows.append([CL[k], int(t.sum())] + ['%d' % (t[o].sum()) for o in range(len(OR))] + [int(t[:, 1].sum())])
            P('\nDeciding origin of the response at generation 200 (individuals summed over runs; the last column counts fills with a copy in their ancestry):\n')
            P(md_table(['class', 'total'] + list(OR) + ['copied'], rows))
    # ---------------------------------------------------------------- M2 conversions
    P('\n## M2: conversions (class-changing events, summed over runs; evicted = the write evicted a fill; multi = several hook nodes with one tag)\n')
    for c in ('beh-max', 'M-open-max', 'M-thanks-only', 'M-grudge-only'):
        rr = A(c)
        if not rr:
            continue
        conv = np.sum([np.array(r['conv']) for r in rr], 0)
        P('\n### %s\n' % c)
        rows = []
        for e in range(4):
            m = conv[e]
            ch = m.sum((0, 1)).copy(); np.fill_diagonal(ch, 0)
            top = sorted([(int(ch[i, j]), CL[i], CL[j]) for i in range(8) for j in range(8) if ch[i, j] > 0], reverse=True)[:5]
            rows.append([R.EVENT_NAMES[e], int(ch.sum()), int(m[1].sum() - np.trace(m[1].sum(0))), int(m[:, 1].sum() - np.trace(m[:, 1].sum(0))),
                         '; '.join('%s->%s %d' % (b, d, n) for n, b, d in top)])
        P(md_table(['event', 'class changes', 'of which evicting', 'of which multi-hook programs', 'largest conversions'], rows))
        mb = conv[4].sum((0, 1))
        P('\nBirths (victim class -> child class), child-class totals: %s\n' % ', '.join('%s %d' % (CL[j], int(mb[:, j].sum())) for j in range(8)))
    # ---------------------------------------------------------------- M6
    P('\n## M6: stranger compatibility of winning-island majorities at the end\n')
    rows = []
    for c, rr in cells.items():
        if not rr:
            continue
        m6 = [r['at'][max(r['at'], key=int)]['m6'] for r in rr]
        rows.append([c, '%.3f' % mean([m['fb_stranger'] for m in m6]), '%.3f' % mean([m['own_stranger'] for m in m6]),
                     '%.3f' % mean([r['rival'] for r in rr])])
    P(md_table(['cell', 'cooperate with the panel FairBot stranger', 'cooperate with an own stranger copy', 'rival-network islands'], rows))
    # ---------------------------------------------------------------- counters
    P('\n## Event counters (mean per run)\n')
    rows = []
    for c, rr in cells.items():
        if not rr:
            continue
        m = np.mean([r['counters'] for r in rr], 0)
        rows.append([c, int(m[0]), int(m[2]), int(m[1]), int(m[5]), int(m[7]), int(m[4]), int(m[17]), int(m[18] + m[19] + m[20]), int(m[22]), int(m[23])])
    P(md_table(['cell', 'encounters', 'thanks writes', 'grudge writes', 'copies', 'contracts', 'evictions', 'behavioural writes', 'rejected (no-evict)', 'no true key', 'outside window'], rows))
    P(TAIL)
    open(os.path.join(ROOT_OUT(), 'hooks-beh.md'), 'w').write('\n'.join(L))
    json.dump(J, open(os.path.join(ROOT_OUT(), 'hooks-beh.json'), 'w'), indent=1, default=str)
    print('\n'.join(L))



TAIL = """
## Counter-predictions and disputes

- **Prediction 5, counter (gemini-4-argon, gpt-6.1-sol): FairBot-equivalents outnumber PrudentBot-equivalents. HELD**, by a wide margin: on winning islands at generation 200 FairBot-eq 1,876, PrudentBot-eq 0; production events into the two classes 230,581 against 498; births with a FairBot-eq child 575,287 against 574. The prior explains it: the two prudent key classes carry 1e-4 of the family's mass against 0.26 for the FairBot-signature keys, and no run grew the prudent class.
- **Prediction 1, disputed static (gemini-4-argon against the RE): the solver sides with the RE's reading** (box vacuously true at world 0): FairBot defects and the Godel predator cooperates, i.e. FairBot exploits the predator; the independent reference agrees on all 49 entries. The statics all hold with PrudentBot read with box1 on d; at level PA the PrudentBot entry fails (mutual defection) and no one-fill program is prudent (addendum to the predictions).
- **Prediction 7** is neither held nor failed: 5/6 = 0.833 sits between the thresholds, on 6 of the 10 planned runs (cut for cost); the one failing run had no efficient island.
- **Prediction 2** is neither held nor failed: 0.700 on 30 runs sits between 0.5 and 0.75. Same-geometry references: the inert-hooks control 11/40 = 0.275, legacy open-max 37/40 = 0.925. The family recovers most of the gap from inert to legacy, not all of it.
- **Secondary N = 200** (10 runs, (200, 8), horizon 600): beh-max 6/10 = 0.600, efficient islands 0.738; not scored against a prediction; at N = 100 the same family gave 0.70 (30 runs, 16 islands), so no sign of a rise with island size at this scale.
- **Scoring conventions.** Prediction 8 is scored by its stated falsifier (copy-ancestry share below 25 percent, or M3b >= 0.9): tripped, hence failed, although its sub-clauses on copying removal (M3b, M3c), eviction (M3d) and multi-hook programs (M3e) held. Prediction 9 is scored by its stated falsifier (a DefectBot-like majority on failed islands): tripped, hence failed; its first clause held (92 percent of class-changing grudge writes come from CooperateBot-like carriers), and failed islands do carry a DefectBot-like fringe (0.046 against 0.001 on efficient islands). Prediction 4 is partial: the held-at-end clause holds under both priors (0.0018 and 0.0105), the founding clause fails under the length prior (hostile constructions are founded on 0.375 of islands, 0.928 under the x10 prior).

## The mechanism of open writes, as far as M1-M6 identify it (plain language)

A program that has just cooperated writes a rule into its own four-slot list: "cooperate with partners like the one I just met", where "like" is a behavioural predicate of the partner (in the legacy cells, the single predicate that the partner provably cooperates with me). The rule is written only about a partner who really was cooperative (thanks) or defective (grudge), and that conditioning is necessary: replacing the conditioned key by a size- and applicability-matched random key drops universal-open from 0.70 to 0.15. A thanks rule on a default-defecting hook turns the writer into a FairBot-like cooperator; a grudge rule on a default-cooperating hook turns a sucker into one (92 percent of grudge conversions start from CooperateBot-like carriers). The rule is then **inherited**: with written fills stripped at birth universal-open falls to 0.20 (thanks-only) and 0.30 (open-max), and with copying also off to 0.45 and 0.525 (within-lifetime writes alone), against 1.00 and 0.95 with everything on. So the carrier is the writing individual's own lineage (H2, inheritance), with selection favouring the converted cooperators on islands where cooperation pays. **Verbatim copying (H1) is not the carrier:** removing it leaves 0.55 (thanks-only) and 1.00 (open-max), and only 2 percent of FairBot-equivalents in thanks-only carry a copied thanks fill; copying matters for grudges (94 percent of FairBot-equivalents in grudge-only carry a copied grudge fill), where the writers are rare suckers. Eviction (H3: no-eviction 1.00 and 0.925) and multi-hook programs (H4: single-hook prior 0.975 and 0.975) are not the mechanism. Timing: writes during generations 0-50 alone give only 0.25 and writes after generation 50 alone 0.80, so conversion is not confined to the founding scramble; the later writes carry more of the effect. Thanks beat grudges (1.00 against 0.575) because grudges convert suckers and leave a small DefectBot-like fringe (0.046 of failed islands) that blocks the 0.95 threshold, while thanks only ever move default-defectors toward cooperation. In the maximal family the winners are generous provers, not the named FairBot: the dominant response on a winning island (rep 0, generation 200) cooperates with CooperateBot, FairBot, TrustingBot and its own copy and defects with DefectBot, PrudentBot and the predator, and the type lists show four stacked friendly guards (box a, box1 a, box c, box1 c); plain base provers (BOX(THEM(ME)) and relatives) hold the rest. The a-free family (no guard on the partner's play towards me) fails (0.10, below the inert control's 0.275), so expressing the prover's guard is what the recovery needs; the winners are not rival networks (M6: every winning-island majority cooperates with the panel FairBot stranger and with an own stranger copy, rival-island share 0 in every cell).
"""


def ROOT_OUT():
    return os.path.join(R.ROOT, 'runs')


if __name__ == '__main__':
    main()
