"""Step 1 report of queue 75: merges the exhaustive enumeration shards, the Monte Carlo runs and the targeted search of each
machine into runs/lt-prior.json and runs/lt-prior.md.

    python3 src/lt_prior_report.py DIR S0_R0 S0_R1      # DIR holds enum_<M>_*.json, mc_<M>_*.json, search_<M>.json
"""
import os, sys, json, glob, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_prior as P

GROUPS = ['const', 'junk_f', 'junk_r', 'const_read', 'single', 'two', 'bully', 'exploit', 'yielder', 'other_cond']
READERS = ('single', 'two')


def grp(fam):
    return P.group_of(fam)


def merge_enum(files):
    stats = {}
    ex = {}
    wall = 0; evals = 0; shards = set()
    s0 = None
    for f in files:
        d = json.load(open(f))
        s0 = d['s0']
        wall += d['wall']; evals += d['evals']; shards.add((d['shard'], d['K']))
        for s, st in d['stats'].items():
            tgt = stats.setdefault(int(s), {})
            for k, v in st.items():
                e = tgt.setdefault(k, [0.0, 0])
                e[0] += v[0]; e[1] += v[1]
        for k, dd in d['examples'].items():
            for s, lst in dd.items():
                cur = ex.setdefault(k, {}).setdefault(int(s), [])
                for x in lst:
                    if len(cur) < 3:
                        cur.append(x)
    return stats, ex, dict(wall=wall, evals=evals, shards=sorted(shards), s0=s0)


def merge_mc(files):
    n = 0; lost = 0; cnt = {}; cntM = {}; ex = {}
    for f in files:
        d = json.load(open(f))
        n += d['n']; lost += d['lost']
        for k, v in d['counts'].items():
            e = cnt.setdefault(k, [0, 10 ** 9]); e[0] += v[0]; e[1] = min(e[1], v[1])
        for k, v in d['countsM'].items():
            cntM[k] = cntM.get(k, 0) + v
        for k, v in d['examples'].items():
            ex.setdefault(k, v)
    return dict(n=n, lost=lost, counts=cnt, countsM=cntM, examples=ex)


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (c - h) / den), min(1.0, (c + h) / den)


def report_machine(mn, dirn, s0):
    mach = P.MACHINES[mn]
    q = mach.extinction()
    sm = mach.size_masses(s0)
    smE = mach.size_masses(s0, tags=P.ENUM_TAGS[mn])
    en_files = sorted(glob.glob(os.path.join(dirn, 'enum_%s_s%d_*.json' % (mn, s0))))
    stats, exm, einfo = merge_enum(en_files)
    mc_files = sorted(glob.glob(os.path.join(dirn, 'mc_%s_*.json' % mn)))
    mc = merge_mc(mc_files) if mc_files else None
    sr_path = os.path.join(dirn, 'search_%s.json' % mn)
    search = json.load(open(sr_path)) if os.path.exists(sr_path) else None
    R = dict(machine=mn, tags=mach.tags, n_tags=mach.T, mean_arity=mach.mean_arity, finite_mass_q=q, lost_mass=1 - q,
             s0=s0, enum_info=einfo, internal_errors_note='evaluator internal errors are counted as stuck (see mc / enum shards)')
    # ---- V3: mass accounting of the exhaustive part
    enum_total = sum(v[0] for st in stats.values() for v in st.values())
    enum_by_size = {s: sum(v[0] for v in st.values()) for s, st in stats.items()}
    excluded = sum(sm[s] - smE[s] for s in range(1, s0 + 1))
    above = q - sum(sm[1:s0 + 1])
    R['accounting'] = dict(enumerated=enum_total, enumerated_expected=sum(smE[1:s0 + 1]), excluded_lib_libsrc_sim=excluded,
                           above_s0_finite=above, lost_infinite=1 - q,
                           sum=enum_total + excluded + above + (1 - q), by_size=enum_by_size,
                           terms_by_size={s: sum(v[1] for v in st.values()) for s, st in stats.items()})
    # ---- exhaustive class masses by group (and exact members)
    exh = {g: 0.0 for g in GROUPS}
    exh_exact = {g: 0.0 for g in GROUPS}
    exh_cnt = {g: 0 for g in GROUPS}
    const_by_code = [0.0] * 9
    members = {}
    minsize = {}
    spell = {}
    for s, st in stats.items():
        for k, (m, c) in st.items():
            fam, ex = k.split('|')
            g = grp(fam)
            exh[g] += m; exh_cnt[g] += c
            if ex:
                exh_exact[g] += m
                members[ex] = members.get(ex, 0.0) + m
            if fam.startswith('const:'):
                const_by_code[int(fam.split(':')[1])] += m
            if g in READERS + ('bully', 'exploit', 'yielder', 'other_cond'):
                key = (g, 'exact' if ex else 'family')
                sp = spell.setdefault(key, {}).setdefault(s, [0.0, 0])
                sp[0] += m; sp[1] += c
    R['exhaustive'] = dict(raw=exh, raw_exact_member=exh_exact, terms=exh_cnt, constants_by_code=const_by_code,
                           members=members)
    # ---- Monte Carlo (the part not covered by the exhaustive enumeration)
    if mc:
        n = mc['n']
        part = {g: [0, 0] for g in GROUPS}       # [count M, count all]
        part_exact = {g: 0 for g in GROUPS}
        cbc = [0] * 9
        for k, v in mc['counts'].items():
            fam, ex = k.split('|')
            part[grp(fam)][1] += v[0]
        for k, v in mc['countsM'].items():
            fam, ex = k.split('|')
            g = grp(fam)
            part[g][0] += v
            if ex:
                part_exact[g] += v
            if fam.startswith('const:'):
                cbc[int(fam.split(':')[1])] += v
        R['mc'] = dict(n=n, lost=mc['lost'], lost_fraction=mc['lost'] / n, finite=n - mc['lost'],
                       count_M=part, count_M_exact=part_exact, const_M_by_code=cbc)
        est = {}
        for g in GROUPS:
            k = part[g][0]
            lo, hi = wilson(k, n)
            est[g] = dict(M_raw=k / n, M_raw_ci=[lo, hi], total_raw=exh[g] + k / n, total_raw_ci=[exh[g] + lo, exh[g] + hi],
                          total_cond=(exh[g] + k / n) / q, total_cond_ci=[(exh[g] + lo) / q, (exh[g] + hi) / q], hits_M=k)
        R['estimate'] = est
        estc = [exh_c + c / n for exh_c, c in zip(const_by_code, cbc)]
        R['const_by_code_raw'] = estc
        R['const_by_code_cond'] = [x / q for x in estc]
        R['mc_files'] = [os.path.basename(f) for f in mc_files]
    # ---- targeted search: lower bounds (sizes above s0 only, so as not to count the exhaustive spellings twice)
    if search:
        lb = {g: {'exact': 0.0, 'family': 0.0} for g in GROUPS}
        by_size = {}
        shortest = {}
        for k, szd in search['classes'].items():
            fam, ex = k.split('|')
            g = grp(fam)
            for s, forms in szd.items():
                s = int(s)
                for form, (m, c, e, *_t) in forms.items():
                    by_size.setdefault((g, 'exact' if ex else 'family'), {}).setdefault(s, [0.0, 0, ''])
                    t = by_size[(g, 'exact' if ex else 'family')][s]
                    t[0] += m; t[1] += c
                    if e and not t[2]:
                        t[2] = e
                    if s > s0:
                        lb[g]['family'] += m
                        if ex:
                            lb[g]['exact'] += m
        R['search'] = dict(wall=search['wall'], lower_bound_beyond_s0=lb,
                           by_size={'%s/%s' % k: {str(s): v for s, v in d.items()} for k, d in by_size.items()})
    # ---- the combined statement
    comb = {}
    for g in GROUPS:
        e_ex = exh_exact[g]; e_fam = exh[g]
        s_ex = R['search']['lower_bound_beyond_s0'][g]['exact'] if search else 0.0
        s_fam = R['search']['lower_bound_beyond_s0'][g]['family'] if search else 0.0
        comb[g] = dict(lower_bound_exact_raw=e_ex + s_ex, lower_bound_family_raw=max(e_fam, 0) + s_fam)
        if mc:
            comb[g]['mc_estimate_cond'] = R['estimate'][g]['total_cond']
            comb[g]['mc_hits_M'] = R['estimate'][g]['hits_M']
    R['combined'] = comb
    # ---- the headline ratios
    cst = None
    if mc:
        cst = R['estimate']['const']['total_raw']
    else:
        cst = exh['const']
    rd_lb = comb['single']['lower_bound_exact_raw'] + comb['two']['lower_bound_exact_raw']
    rd_lb_f = comb['single']['lower_bound_family_raw'] + comb['two']['lower_bound_family_raw']
    R['headline'] = dict(
        const_raw=cst, const_cond=cst / q,
        reader_exact_lower_bound_raw=rd_lb, reader_family_lower_bound_raw=rd_lb_f,
        rho_R_exact_lower_bound=rd_lb / cst, rho_R_family_lower_bound=rd_lb_f / cst,
        reader_exact_lower_bound_cond=rd_lb / q, reader_family_lower_bound_cond=rd_lb_f / q,
        beta_exact_lower_bound_ratio=(comb['bully']['lower_bound_exact_raw'] / rd_lb) if rd_lb else None,
        beta_family_ratio=(comb['bully']['lower_bound_family_raw'] / rd_lb_f) if rd_lb_f else None,
        junk_cond=(R['estimate']['junk_f']['total_cond'] + R['estimate']['junk_r']['total_cond']) if mc else None,
        junk_f_cond=R['estimate']['junk_f']['total_cond'] if mc else None,
        junk_r_cond=R['estimate']['junk_r']['total_cond'] if mc else None)
    # shortest spellings
    short = {}
    for g in ('single', 'two', 'bully', 'exploit', 'yielder'):
        for kind in ('exact', 'family'):
            sizes = {}
            for key, d in (spell.items()):
                if key == (g, kind):
                    for s, (m, c) in d.items():
                        sizes.setdefault(int(s), [0.0, 0])
                        sizes[int(s)][0] += m; sizes[int(s)][1] += c
            if search and 'by_size' in R['search']:
                for s, v in R['search']['by_size'].get('%s/%s' % (g, kind), {}).items():
                    if int(s) > s0 or int(s) not in sizes:
                        t = sizes.setdefault(int(s), [0.0, 0])
                        t[0] += v[0]; t[1] += v[1]
            if sizes:
                smin = min(sizes)
                ex = None
                for k, dd in exm.items():
                    fam, e = k.split('|')
                    if grp(fam) == g and (bool(e) == (kind == 'exact')) and smin in dd:
                        ex = dd[smin][0]; break
                if ex is None and search:
                    ex = R['search']['by_size'].get('%s/%s' % (g, kind), {}).get(str(smin), [0, 0, ''])[2]
                short[g + '/' + kind] = dict(min_size=smin, example=ex, counts={str(smin + i): sizes.get(smin + i, [0, 0])[1] for i in range(3)},
                                             masses={str(smin + i): sizes.get(smin + i, [0, 0])[0] for i in range(3)})
    R['shortest'] = short
    return R


def md(R):
    out = []
    for mn in ('R0', 'R1'):
        r = R['machines'].get(mn)
        if not r:
            continue
        out.append('## Machine %s' % mn)
        out.append('')
        out.append('tags %d, mean arity %.4f, finite-tree mass q = %.6f (lost mass %.6f); exhaustive enumeration to size s0 = %d' % (
            r['n_tags'], r['mean_arity'], r['finite_mass_q'], r['lost_mass'], r['s0']))
        a = r['accounting']
        out.append('')
        out.append('Mass accounting (V3): enumerated %.9f (expected %.9f), excluded lib/libsrc/sim %.9f, above s0 (finite) %.9f, lost %.9f; sum %.12f' % (
            a['enumerated'], a['enumerated_expected'], a['excluded_lib_libsrc_sim'], a['above_s0_finite'], a['lost_infinite'], a['sum']))
        out.append('')
        out.append('| class | exhaustive raw (size <= s0) | MC estimate, cond. on finite [95% CI] | hits outside exhaustive | search lower bound beyond s0 (raw) |')
        out.append('|---|---|---|---|---|')
        for g in GROUPS:
            e = r.get('estimate', {}).get(g)
            lb = r.get('search', {}).get('lower_bound_beyond_s0', {}).get(g, {})
            out.append('| %s | %.4g | %s | %s | %s |' % (g, r['exhaustive']['raw'][g],
                       ('%.4g [%.3g, %.3g]' % (e['total_cond'], e['total_cond_ci'][0], e['total_cond_ci'][1])) if e else '-',
                       e['hits_M'] if e else '-', ('exact %.3g / family %.3g' % (lb['exact'], lb['family'])) if lb else '-'))
        h = r['headline']
        out.append('')
        out.append('Headline: constants %.4g (cond.); reader lower bound (exact members) raw %.3g, rho_R >= %.3g; (family level) rho_R >= %.3g; bully/reader ratio (exact) %s, (family) %s; junk %.4g (forfeit %.4g, failed-read %.4g)' % (
            h['const_cond'], h['reader_exact_lower_bound_raw'], h['rho_R_exact_lower_bound'], h['rho_R_family_lower_bound'],
            h['beta_exact_lower_bound_ratio'], h['beta_family_ratio'], h['junk_cond'] or float('nan'), h['junk_f_cond'] or float('nan'), h['junk_r_cond'] or float('nan')))
        out.append('')
        out.append('Shortest spellings: ' + json.dumps(r['shortest']))
        out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    dirn = sys.argv[1]
    s0 = {'R0': int(sys.argv[2]), 'R1': int(sys.argv[3])}
    R = dict(machines={mn: report_machine(mn, dirn, s0[mn]) for mn in ('R0', 'R1')})
    json.dump(R, open(os.path.join(dirn, 'lt-prior.json'), 'w'), indent=1, default=str)
    open(os.path.join(dirn, 'lt-prior.md'), 'w').write(md(R))
    print(md(R))
