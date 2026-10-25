"""Runner for the exploration-cap audit.  One job per process.

    python3 src/exploration_audit_run.py m2cell GAME ARM C N STAGE [--max_states K] [--seeds published|randomK:SEED] [--tag T]
        STAGE in cap (published settings, or those given), full (whole state space)
    python3 src/exploration_audit_run.py solvercheck GAME ARM C N      # log GTH vs jump GTH vs dense generator on identical sets
Environment: MIXED2_CACHE must point at the class-table cache (rebuilt on a miss).  Results -> runs/exploration_audit/.
"""
import argparse, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"          # one thread per worker (at most 3 workers in all); must precede the numpy import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import exploration_audit as X


def cmd_m2cell(a):
    A = X.m2_arm(a.game, a.arm, a.c)
    cell = 'm2_%s_%s_c%g_N%d' % (a.game, a.arm, a.c, a.N)
    X.log('[%s] K=%s' % (cell, A.K), 'S=', A.K[0] * A.K[1])
    if a.stage == 'full':
        out, ch = X.m2_full(A, a.N)
        stage = 'c_full' + a.tag
    else:
        seeds = None
        label = 'published'
        if a.seeds.startswith('random'):
            k, sd = a.seeds[6:].split(':')
            seeds = X.random_seeds(A, int(k), int(sd)); label = a.seeds
        out, ch = X.m2_capped(A, a.N, max_states=a.max_states, max_add=a.max_add,
                              log_theta=math.log(a.theta), seeds=seeds, verbose=a.verbose)
        out['seeds_label'] = label
        stage = 'cap%d_%s%s' % (a.max_states, label, a.tag)
    X.record(cell, stage, out)
    st = out['stat']
    X.log('  %s: states=%d capped=%s u0g=%.4f u1g=%.4f frontier=%s time=%.0fs rss=%.0fMB' % (
        stage, out['n_states'], out.get('capped'), st['u0g'], st['u1g'], out.get('frontier_mass'), out['time_s'], out['rss_mb']))


def cmd_solvercheck(a):
    M = X.m2()
    A = X.m2_arm(a.game, a.arm, a.c)
    N = a.N
    K0, K1 = A.K
    S = K0 * K1
    cell = 'solvercheck_%s_%s_c%g_N%d' % (a.game, a.arm, a.c, N)
    outf, chf = X.m2_full(A, N)
    pif = np.exp(chf.lpi)
    t0 = time.time()
    states, pig = X.generator_solve(A, N)
    tg = time.time() - t0
    rec = dict(S=S, tv_full_vs_generator=X.tv(pif, pig), max_abs=float(np.abs(pif - pig).max()), generator_time_s=tg)
    if S <= 2500:
        ch = M.TwoPopChain(A, N)
        for s in range(S):
            ch.add(s)
        LA, lpi, info = ch.solve()
        pil = np.exp(lpi - np.logaddexp.reduce(lpi))
        rec['tv_full_vs_log_gth'] = X.tv(pif, pil)
        rec['log_gth_solver'] = info.get('solver', 'log_gth')
    pi_g = pig / pig.sum()
    sg = X.stats_under_pi(A, states, np.log(np.maximum(pi_g, 1e-300)))
    rec['u0g_full'] = outf['stat']['u0g']; rec['u0g_generator'] = sg['stat']['u0g']
    X.record(cell, 'solver_check', rec)
    X.log(cell, rec)


def cmd_ult(a):
    cell = 'ult_%s_%s_N%d' % (a.game, a.arm, a.N)
    out, tp = X.ult_cell(a.game, a.arm, a.N, a.w, a.n, a.stage)
    X.record(cell, 'stage_' + a.stage, out)
    X.log(cell, a.stage, 'pairs', out['n_pairs'], 'expanded', out['n_expanded'], 'cut', out['cut_flow'],
          'rej %.4f sP %.4f sR %.4f' % (out['reject'], out['share_P'], out['share_R']), 'frontier %.4f' % out['frontier_mass'])
    X.log('  top outcomes', out['top_outcomes'][:5])


def cmd_mdfixed(a):
    cell = 'mdfixed_%s_N%d' % (a.arm, a.N)
    out, ch, d = X.md_fixed(a.arm, a.N, a.theta, a.max_states, verbose=a.verbose, lazy2=a.lazy2)
    X.record(cell, 'cap%d_th%g%s' % (a.max_states, a.theta, '_lazy2' if a.lazy2 else ''), out)
    X.log(cell, 'states', out['n_states'], 'cut %.3e' % out['cut'], 'eff %.4f' % out['eff'], {k: round(v, 4) for k, v in out['label_mass'].items() if v > 1e-3},
          'const-pairs %.3f' % out['mass_constant_pairs'], '%.0fs %.0fMB' % (out['time_s'], out['rss_mb']))


def cmd_sacell(a):
    cell = 'sa_%s_N%d' % (a.name, a.N)
    res = X.sa_run(a.name, a.N, log_theta=math.log(a.theta), max_states=a.max_states, twins=a.twins, closure_nodes=a.closure_nodes,
                   verbose=a.verbose, skip_published=a.skip_published)
    summ = X.sa_summary(res)
    X.record(cell, 'd_twins' if a.twins else 'd_lumped', summ)
    X.log(cell, 'twins' if a.twins else 'lumped', summ['rerun_stat'], '->', summ['resolve_stat'], 'states', summ['resolve_n_states'],
          'log10cut', summ['resolve_log10_cut'], 'deep', summ['n_deep'], summ['n_deep_mod_twins'], '%.0fs' % summ['time_s'])


def cmd_d3(a):
    cell = 'd3_%s_N%d' % (a.arm, a.N)
    out, ch = X.d3_cell(a.arm, a.N, a.theta, core_max=a.core_max, promote=a.promote, max_rounds=a.max_rounds)
    X.record(cell, 'theta%g_core%d_prom%g' % (a.theta, a.core_max, a.promote), out)
    X.log(cell, 'theta', a.theta, 'states', out['states'], 'core', out['core'], 'rel_cut %.4f chg %.4f' % (out['rel_cut'], out['rel_cut_change']),
          {k: round(v, 4) for k, v in out['mass_by_coalition'].items()}, 'eff %.4f' % out['efficiency'], '%.0fs %.0fMB' % (out['time_s'], out['rss_mb']))


def cmd_enf(a):
    cell = 'enfC_%s_pool%d_c%g_N%d_%s' % (a.arm, a.pool, a.c, a.N, a.tie)
    out = X.enf_partC(a.arm, a.pool, a.c, a.N, a.tie, a.theta)
    X.record(cell, 'theta%g' % a.theta, out)
    X.log(cell, 'theta', a.theta, 'states', out['states'], 'rel_cut_change %.4f' % out['rel_cut_change'], out['summary'], 'eff', out['efficiency'], '%.0fs' % out['wall_s'])


def cmd_union(a):
    cell = 'union_%s_c%g_N%d' % (a.arm, a.c, a.N)
    out = X.union_cell(a.arm, a.c, a.N, a.theta, core_max=a.core_max)
    X.record(cell, 'theta%g_core%d' % (a.theta, a.core_max), out)
    X.log(cell, 'theta', a.theta, 'states', out['states'], 'rel_cut_change %.4f' % (out['rel_cut_change'] or float('nan')), out['summary'], '%.0fs' % out['wall_s'])


def cmd_conc(a):
    cell = 'conc_%s_%s_c%g_N%d' % (a.arm, a.enf, a.c, a.N)
    out = X.conc_cell(a.arm, a.N, a.theta, enf=a.enf, pool=a.pool, c=a.c)
    X.record(cell, 'theta%g' % a.theta, out)
    X.log(cell, 'theta', a.theta, 'states', out['states'], 'rel_cut_change %.4f' % out['rel_cut_change'], out['summary'], '%.0fs' % out['wall_s'])


def cmd_chk(a):
    cell = 'chk_%s_%s_N%d' % (a.arm, a.game, a.N)
    out = X.chk_onepop(a.arm, a.game, a.N, a.max_states, log_theta=math.log(a.theta), twins=not a.lumped)
    X.record(cell, 'cap%d_th%g%s' % (a.max_states, a.theta, '_lumped' if a.lumped else ''), out)
    X.log(cell, 'cap', a.max_states, 'states', out['n_states'], 'left', out['n_cand_left'], 'log10cut', out['log10_cut'],
          'pay %.4f eff %.4f' % (out['pay_per_player'], out['efficiency']), '%.0fs' % out['time_s'])


def cmd_mdlimn(a):
    cell = 'mdlimn_%s_N%d' % (a.arm, a.N)
    out = X.md_limN(a.arm, a.N, a.theta, twins=a.twins)
    X.record(cell, 'th%g%s' % (a.theta, '_twins' if a.twins else '_lumped'), out)
    X.log(cell, 'theta', a.theta, 'twins', a.twins, 'P_eff %.4f' % out['P_efficient'], 'states', out['n_states'], 'log10cut', out['log10_cut'],
          'effset %.3f deep %.3f greedy %.3f' % (out['effset_mass'], out['deep_mass'], out['greedy_mass']), '%.0fs' % out['wall_s'])


def cmd_rps(a):
    cell = 'rps_%s_D%d_n%d_N%d' % (a.arm, a.D, a.n, a.N)
    out = X.rps_cell(a.arm, a.N, n=a.n, D=a.D, log10theta=a.log10theta, closure_nodes=a.closure_nodes, max_states=a.max_states)
    X.record(cell, 'lt%g_cl%d' % (a.log10theta, a.closure_nodes), out)
    X.log(cell, 'e_prog %.4f e_act %.4f mix %.3f X %.3f' % (out['e_prog'], out['e_act'], out['mix_pop'], out['share_X']), 'rec', out['n_recurrent'],
          'cut', out['log10_cut'], 'left', out['n_cand_left'], 'closure_complete', out['closure_complete'], '%.0fs' % out['time_s'])


def cmd_rpsp(a):
    cell = 'rpsp_%s_%s_c%g_D%d_N%d' % (a.arm, a.kind, a.c, a.D, a.N)
    out = X.rps_priced_cell(a.arm, a.c, a.kind, a.N, D=a.D, log10theta=a.log10theta, closure_nodes=a.closure_nodes, branch=a.branch,
                            att_starts=a.att_starts, max_states=a.max_states)
    X.record(cell, 'lt%g_cl%d_b%d_att%d' % (a.log10theta, a.closure_nodes, a.branch, a.att_starts), out)
    X.log(cell, 'e_prog %.4f e_gross %.4f mix %.3f X %.3f poly %.4f' % (out['e_prog'], out['e_gross'], out['mix_pop'], out['share_X'] or 0, out['poly_mass']),
          'rec', out['n_recurrent'], 'cut', out['log10_cut'], 'left', out['n_cand_left'], 'closure_complete', out['closure_complete'], '%.0fs' % out['time_s'])


def cmd_sab(a):
    cell = 'sb_%s_N%d' % (a.name, a.N)
    out = X.sa_bounded(a.name, a.N, log_theta=math.log(a.theta), max_states=a.max_states, twins=a.twins, verbose=a.verbose)
    X.record(cell, 'b_twins' if a.twins else 'b_lumped', out)
    X.log(cell, 'twins' if a.twins else 'lumped', out['rerun_stat'], '->', out['resolve_stat'], 'states', out['resolve_n_states'],
          'log10cut', out['resolve_log10_cut'], 'left', out['resolve_n_cand_left'], 'poly %.2e' % out['resolve_mass_poly'], '%.0fs' % out['time_s'])


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd')
    sb = sp.add_parser('sab')
    sb.add_argument('name'); sb.add_argument('N', type=int); sb.add_argument('--theta', type=float, default=1e-14)
    sb.add_argument('--max_states', type=int, default=20000); sb.add_argument('--twins', action='store_true'); sb.add_argument('--verbose', action='store_true')
    rp = sp.add_parser('rps')
    rp.add_argument('arm'); rp.add_argument('N', type=int); rp.add_argument('--n', type=int, default=6); rp.add_argument('--D', type=int, default=12)
    rp.add_argument('--log10theta', type=float, default=-14.0); rp.add_argument('--closure_nodes', type=int, default=6000)
    rp.add_argument('--max_states', type=int, default=20000)
    pp = sp.add_parser('rpsp')
    pp.add_argument('arm'); pp.add_argument('N', type=int); pp.add_argument('--c', type=float, required=True); pp.add_argument('--kind', default='depth')
    pp.add_argument('--D', type=int, default=12); pp.add_argument('--log10theta', type=float, default=-8.0)
    pp.add_argument('--closure_nodes', type=int, default=6000); pp.add_argument('--branch', type=int, default=8)
    pp.add_argument('--att_starts', type=int, default=1000); pp.add_argument('--max_states', type=int, default=40000)
    ml = sp.add_parser('mdlimn')
    ml.add_argument('arm'); ml.add_argument('N', type=int); ml.add_argument('--theta', type=float, default=1e-7); ml.add_argument('--twins', action='store_true')
    ck = sp.add_parser('chk')
    ck.add_argument('arm'); ck.add_argument('game'); ck.add_argument('N', type=int); ck.add_argument('--max_states', type=int, default=3000)
    ck.add_argument('--theta', type=float, default=1e-14); ck.add_argument('--lumped', action='store_true')
    cn = sp.add_parser('conc')
    cn.add_argument('arm'); cn.add_argument('N', type=int); cn.add_argument('--enf', default='CC'); cn.add_argument('--pool', type=int, default=0)
    cn.add_argument('--c', type=float, default=0.5); cn.add_argument('--theta', type=float, required=True)
    un = sp.add_parser('union')
    un.add_argument('arm'); un.add_argument('N', type=int); un.add_argument('--c', type=float, default=0.5)
    un.add_argument('--theta', type=float, required=True); un.add_argument('--core_max', type=int, default=2500)
    en = sp.add_parser('enf')
    en.add_argument('arm'); en.add_argument('pool', type=int); en.add_argument('N', type=int); en.add_argument('--c', type=float, default=0.5)
    en.add_argument('--tie', default='whack'); en.add_argument('--theta', type=float, required=True)
    d3 = sp.add_parser('d3')
    d3.add_argument('arm'); d3.add_argument('N', type=int); d3.add_argument('--theta', type=float, required=True)
    d3.add_argument('--core_max', type=int, default=2500); d3.add_argument('--promote', type=float, default=1e-5)
    d3.add_argument('--max_rounds', type=int, default=40)
    s2 = sp.add_parser('sacell')
    s2.add_argument('name'); s2.add_argument('N', type=int); s2.add_argument('--theta', type=float, default=1e-14)
    s2.add_argument('--max_states', type=int, default=20000); s2.add_argument('--twins', action='store_true')
    s2.add_argument('--closure_nodes', type=int, default=0); s2.add_argument('--verbose', action='store_true')
    s2.add_argument('--skip_published', action='store_true')
    f = sp.add_parser('mdfixed')
    f.add_argument('arm'); f.add_argument('N', type=int); f.add_argument('--theta', type=float, default=1e-12)
    f.add_argument('--max_states', type=int, default=8000); f.add_argument('--verbose', action='store_true')
    f.add_argument('--lazy2', action='store_true')
    u = sp.add_parser('ult')
    u.add_argument('game'); u.add_argument('arm'); u.add_argument('stage'); u.add_argument('--N', type=int, default=100)
    u.add_argument('--w', type=float, default=0.1); u.add_argument('--n', type=int, default=5)
    c = sp.add_parser('m2cell')
    c.add_argument('game'); c.add_argument('arm'); c.add_argument('c', type=float); c.add_argument('N', type=int); c.add_argument('stage')
    c.add_argument('--max_states', type=int, default=1500); c.add_argument('--max_add', type=int, default=400)
    c.add_argument('--theta', type=float, default=1e-10); c.add_argument('--seeds', default='published'); c.add_argument('--tag', default='')
    c.add_argument('--verbose', action='store_true')
    s = sp.add_parser('solvercheck')
    s.add_argument('game'); s.add_argument('arm'); s.add_argument('c', type=float); s.add_argument('N', type=int)
    a = ap.parse_args()
    {'m2cell': cmd_m2cell, 'solvercheck': cmd_solvercheck, 'ult': cmd_ult, 'mdfixed': cmd_mdfixed, 'sacell': cmd_sacell, 'd3': cmd_d3, 'enf': cmd_enf, 'union': cmd_union, 'conc': cmd_conc, 'chk': cmd_chk, 'mdlimn': cmd_mdlimn, 'rps': cmd_rps, 'rpsp': cmd_rpsp, 'sab': cmd_sab}[a.cmd](a)


if __name__ == '__main__':
    main()
