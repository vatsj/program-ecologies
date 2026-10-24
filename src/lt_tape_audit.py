"""The soundness test and the adversarial cases for the private-tape experiment (specs/2026-10-24-realizable-randomizer.md,
prediction 1; notes/lt-tape.md section 1.0).

(a) every derived atom of K_T^tape on every ordered pair of the catalogues is true for all tapes, together with every sequent of its
    witness derivation (`soundness_audit`), at two proof budgets;
(b) adaptive and nested programs: branch-dependent simulation, repeated tape reads, nested sims, a sim whose tape must be independent;
(c) adversarial count certificates: malformed, duplicate, omitted, overlapping, over- and under-long prefixes, wrong weights, a
    certificate for another fuel stamp, for another action, copied onto another program, and a replay that reads the opponent:
    every one must be rejected, and the honest certificates accepted.
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_tape as T
import lt_tape_games as G
from lt_tape import (con, nat, L2, TP, EQ, IF, PL, HQ, PAIR, THEM, ME, make_certs, carrier, plist)


# ---------------------------------------------------------------------------------------------------------------- (a)
def pair_soundness(game, K, budgets=(8, 16), limit=None, arm='full', progress=None):
    """Derived atoms and witness sequents over all ordered pairs of the arm's catalogue.  Returns a dict."""
    r = 3 if game == 'rps' else 2
    if game == 'rps':
        (tp,) = G.catalogue_rps(K); tpls = [tp]
    else:
        tpls = list(G.catalogue_insp(K))
    terms, _ = G.arm_terms(game, tpls, arm)
    prover = T.TProver(r, limit=limit or 3 * K)
    eng = T.Engine(prover, K=K, r=r, m=3)
    th = prover.th
    acts = G.RPS.acts[0] if game == 'rps' else None
    pairs = []
    nm = [[t.name for t in lst] for lst in tpls]
    if game == 'rps':
        for ix, x in enumerate(terms[0]):
            for iy, y in enumerate(terms[0]): pairs.append((x, y, 'RPS', nm[0][ix], nm[0][iy]))
    else:
        for ix, x in enumerate(terms[0]):
            for iy, y in enumerate(terms[1]): pairs.append((x, y, 'IN', nm[0][ix], nm[1][iy]))      # inspector's actions I, N
        for iy, y in enumerate(terms[1]):
            for ix, x in enumerate(terms[0]): pairs.append((y, x, 'CK', nm[1][iy], nm[0][ix]))      # inspectee's actions C, K
    nq = nfound = ntimeout = 0
    for (x, y, A, _nx, _ny) in pairs:
        for a in A if A != 'IN' else 'IN':
            psi = th.plays(x, y, a)
            for b in budgets:
                q = prover.query(psi, b)
                nq += 1
                if q['found']: nfound += 1
                if not q['complete']: ntimeout += 1
    nbox, nseq, bad, skipped = T.soundness_audit(prover, eng)
    # play agreement: a derived atom (provable at b) implies the actual play at ample fuel puts all mass on the action
    # unless the play is cut by the fuel (the idealization of `prove`'s cost): reported, not asserted.
    big = T.Engine(prover, K=10 ** 6, r=r, m=3)
    disagree = []; checked = 0
    for (x, y, A, nx, ny) in pairs:
        for a in A:
            psi = th.plays(x, y, a)
            q = prover.cache.get((psi, budgets[-1]))
            if q and q['found']:
                d = big.dist(x, y)
                checked += 1
                if d['dist'].get(a, Fraction(0)) != 1:
                    disagree.append((nx, ny, a, {k: float(v) for k, v in d['dist'].items()}))
    return dict(game=game, K=K, arm=arm, queries=nq, found=nfound, incomplete=ntimeout, boxes=nbox, sequents=nseq,
                false=len(bad), bad=[str(b)[:200] for b in bad[:10]], skipped=skipped, play_checked=checked,
                play_disagree=len(disagree), play_disagree_examples=[str(d) for d in disagree[:12]])


# ---------------------------------------------------------------------------------------------------------------- (b)
def adaptive_cases(r=2):
    """Named adaptive/nested programs over the actions C and K (r = 2); each entry (name, program)."""
    k = 60
    t0 = TP(0)
    cases = {}
    # repeated reads: the same position twice is one draw
    cases['repeat'] = L2(IF(EQ(t0, t0), con('C'), con('K')))
    cases['repeat_branch'] = L2(IF(EQ(t0, nat(0)), IF(EQ(t0, nat(0)), con('C'), con('K')), IF(EQ(t0, nat(1)), con('C'), con('K'))))
    # branch-dependent simulation: simulate the opponent only on digit 0
    cases['branch_sim'] = L2(IF(EQ(t0, nat(0)), IF(EQ(('run', nat(k), THEM, ME), con('C')), con('C'), con('K')), con('C')))
    # the sim's tape is independent of the real tape: compare the real digit with the sim's action (if the opponent is the mixer Mc4)
    cases['indep'] = L2(IF(EQ(t0, nat(0)), IF(EQ(('run', nat(k), THEM, ME), con('K')), con('C'), con('K')),
                           IF(EQ(('run', nat(k), THEM, ME), con('K')), con('K'), con('C'))))
    # nested sims: a sim of a sim
    cases['nested'] = L2(IF(EQ(('run', nat(k), THEM, ME), con('C')), IF(EQ(('run', nat(k), THEM, ME), con('C')), con('C'), con('K')), con('K')))
    # a prover that proves something about a tape reader (for-all), then reads the tape
    cases['prove_tape'] = L2(IF(('prove', nat(8), PL(THEM, ME, 'C')), IF(EQ(t0, nat(1)), con('K'), con('C')), con('K')))
    # same action on both branches (provable for all tapes) and different
    cases['same_both'] = L2(IF(EQ(t0, nat(0)), con('C'), con('C')))
    cases['diff'] = L2(IF(EQ(t0, nat(0)), con('C'), con('K')))
    return cases


def adaptive_soundness(K=3000, budgets=(8, 16)):
    r = 2
    cases = adaptive_cases(r)
    names = list(cases)
    mix = {'Mc4': L2(IF(EQ(TP(0), nat(0)), con('K'), con('C'))), 'C0': L2(con('C')), 'K0': L2(con('K'))}
    progs = {**cases, **mix}
    prover = T.TProver(r, limit=3 * K)
    eng = T.Engine(prover, K=K, r=r, m=3)
    th = prover.th
    nfound = nq = 0
    results = {}
    for nx, x in progs.items():
        for ny, y in progs.items():
            for a in 'CK':
                psi = th.plays(x, y, a)
                for b in budgets:
                    q = prover.query(psi, b); nq += 1
                    if q['found']: nfound += 1
            d = eng.dist(x, y)
            results['%s|%s' % (nx, ny)] = {k: str(v) for k, v in d['dist'].items()}
    nbox, nseq, bad, skipped = T.soundness_audit(prover, eng)
    # padded-space reference agrees with the branching engine (at most one sim: two invocations; the nested cases reach three)
    ref_ok = 0; ref_n = 0; ref_bad = []
    for nx in ('repeat', 'repeat_branch', 'branch_sim', 'indep', 'same_both', 'diff'):
        for ny in ('Mc4', 'C0', 'K0'):
            ref = eng.dist_padded(progs[nx], progs[ny], ninv=2)
            d = eng.dist(progs[nx], progs[ny])
            ref_n += 1
            if ref['dist'] == d['dist'] and ref['steps'] == d['steps']: ref_ok += 1
            else: ref_bad.append((nx, ny))
    return dict(queries=nq, found=nfound, boxes=nbox, sequents=nseq, false=len(bad), bad=[str(b)[:200] for b in bad[:10]],
                skipped=skipped, padded_ref=ref_n, padded_ok=ref_ok, padded_bad=ref_bad)


# ---------------------------------------------------------------------------------------------------------------- (c)
def honest_carrier(j, K, m=3):
    """The carrier CARR_j of the catalogue (tape variant)."""
    ins, ee = G.catalogue_insp(K, m)
    for t in ins:
        if t.name == 'CARR%d' % j: return t.build('tape')
    raise KeyError(j)


def _rebuild(x, certs):
    """x with its CERTS literal replaced."""
    assert x[0] == 'lam' and x[1][0] == 'lam' and x[1][1][0] == 'app'
    return ('lam', ('lam', ('app', x[1][1][1], certs)))


def certificate_attacks(K=3000):
    """Returns (honest results, attack results): dicts name -> (accepted, charge, reason)."""
    r, m = 2, 3
    prover = T.TProver(r, limit=3 * K)
    eng = T.Engine(prover, K=K, r=r, m=m)
    out = {}
    ok = {}
    for j in (1, 2, 3, 4, 6):
        x = honest_carrier(j, K)
        ok['honest_%d_at_p' % j] = eng.check_cert(x, 'I', j)            # exactly the mixer's probability
        ok['honest_%d_below' % j] = eng.check_cert(x, 'I', max(j - 1, 0))
        out['honest_%d_above' % j] = eng.check_cert(x, 'I', j + 1)      # claims more than the carrier has: must reject
    x3 = honest_carrier(3, K)
    # structure: x3 = lam lam app (lam BODY) CERTS ; CERTS = (stamp, [(I, [[0,0],[0,1,0]])])
    body = x3[1][1][1]
    def with_certs(entries, stamp=K): return _rebuild(x3, make_certs(stamp, entries))
    atk = {}
    atk['duplicate_prefix'] = with_certs([('I', [[0, 0], [0, 0], [0, 1, 0]])])           # duplicated cylinder (double counts)
    atk['omitted_prefix'] = with_certs([('I', [[0, 0]])])                                  # weight 1/4 < 3/8
    atk['wrong_weight_overlong'] = with_certs([('I', [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 0, 1]])])   # ragged: unconsumed digits / overlap
    atk['overlong_prefix_only'] = with_certs([('I', [[0, 0, 0], [0, 0, 1], [0, 1, 0]])])   # prefixes longer than the reads (LONG)
    atk['underlong_prefix'] = with_certs([('I', [[0], [1]])])                               # replay needs more digits (SHORT)
    atk['overlap_prefixes'] = with_certs([('I', [[0, 0], [0], [0, 1, 0]])])                # [0] contains [0,0]
    atk['wrong_action_prefix'] = with_certs([('I', [[1], [0, 1, 1]])])                     # leaves producing N listed for I
    atk['wrong_stamp_bigger'] = with_certs([('I', [[0, 0], [0, 1, 0]])], stamp=K * 2)      # minted for a larger budget
    atk['wrong_stamp_smaller'] = with_certs([('I', [[0, 0], [0, 1, 0]])], stamp=K // 2)
    atk['digit_out_of_range'] = with_certs([('I', [[0, 0], [0, 1, 0], [2]])])
    atk['two_entries_same_action'] = with_certs([('I', [[0, 0]]), ('I', [[0, 1, 0]])])
    atk['no_entry_for_action'] = with_certs([('N', [[1]])])
    atk['malformed_certs_nat'] = _rebuild(x3, nat(5))
    atk['malformed_entries'] = _rebuild(x3, PAIR(nat(K), PAIR(nat(7), nat(0))))
    atk['empty_list'] = with_certs([('I', [])])
    # a certificate copied onto another program: M2's honest certificate on a mixer whose probability is 1/8 (M1's body)
    x1 = honest_carrier(1, K); x2 = honest_carrier(2, K)
    atk['copied_cert_other_program'] = _rebuild(x1, x2[1][1][2])
    # replay that reads the opponent: a hash-driven carrier with an honest-looking certificate for the tape variant
    ins, _ = G.catalogue_insp(K)
    for t in ins:
        if t.name == 'CARR3': atk['reads_opponent'] = t.build('hash')
    # a carrier whose body is not a pure mixer: replays reach different leaves than the certificate says
    atk['body_changed'] = _rebuild(honest_carrier(2, K), x3[1][1][2])
    res = {}
    for name, x in atk.items():
        res[name] = eng.check_cert(x, 'I', 3)
    return out, ok, res


def run_all(K=3000, budgets=(8, 16)):
    out = dict(adaptive=adaptive_soundness(K, budgets))
    above, honest, attacks = certificate_attacks(K)
    out['certs_honest_accepted'] = {k: bool(v[0]) for k, v in honest.items()}
    out['certs_overclaim_rejected'] = {k: (not v[0]) for k, v in above.items()}
    out['attacks_rejected'] = {k: (not v[0]) for k, v in attacks.items()}
    out['attacks_detail'] = {k: [bool(v[0]), v[1], v[2]] for k, v in attacks.items()}
    return out
