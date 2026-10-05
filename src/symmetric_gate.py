"""The symmetric gate (specs/2026-10-05-symmetric-gate.md): type tables under three contract-access rules.

`contracts._eval_types` answers a box atom of reader t against opponent u with target tau from contracts iff u and tau
both carry, whoever t is.  Here one per-reader flag rc[t] is added: the atom is a contract read iff rc[t] = 1 and u and
tau both carry; otherwise it is a source read through the gate.

    asym   rc = 1 for every type (the rule as run; reproduces runs/contracts_types_b0.npz bit for bit)
    sym    rc[t] = 1 iff t carries a contract (readers that carry nothing have no checker)
    q<x>   rc[t] = 1 iff t carries, or t's canonical source is assigned "reads contracts"; one uniform u_p per canonical
           source from default_rng(20251005).random(K), source p reads iff u_p < x (nested in x; quenched)

"Reader" is the executing program at every level: a box is a statement about the opponent's actual play, which is the
opponent's own execution, so boxes inside it are evaluated under the opponent's access (soundness; the audit below
re-derives every atom under the rule and counts violations).

    python3 src/symmetric_gate.py          # builds runs/symmetric_gate_types.npz (val per rule at b in {0, inf}) + audit
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import contracts as CT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
TYPES = os.path.join(RUNS, 'symmetric_gate_types.npz')
RULES = ('asym', 'sym', 'q0.5', 'q0.25')
QSEED = 20251005


@njit(cache=True)
def _eval_types_rc(nat, ak, al, af, aa, tt, src, con, nc_type, cs_type, rep, BC, BD, mask, rc, max_worlds):
    """contracts._eval_types with a per-reader contract-access flag rc[t]."""
    NT = src.shape[0]
    hc = np.ones((2, NT, NT), np.bool_)
    hd = np.ones((2, NT, NT), np.bool_)
    val = np.zeros((NT, NT), np.int8)
    prev = -np.ones((NT, NT), np.int64)
    last = np.zeros((NT, NT), np.int64)
    for n in range(max_worlds):
        for t in range(NT):
            p = src[t]
            for u in range(NT):
                idx = 0
                for j in range(nat[p]):
                    f = af[p, j]
                    if f == 0:
                        tg = t
                    elif f == 1:
                        tg = u
                    else:
                        a = aa[p, j]
                        tg = cs_type[a] if con[u] >= 0 else nc_type[a]
                    L = al[p, j]
                    if rc[t] == 1 and con[u] >= 0 and con[tg] >= 0:
                        x = rep[con[u]]; y = rep[con[tg]]
                        b = BC[L, x, y] if ak[p, j] == 0 else BD[L, x, y]
                    elif mask[t, u] == 0:
                        b = False
                    else:
                        b = hc[L, u, tg] if ak[p, j] == 0 else hd[L, u, tg]
                    if b: idx |= 1 << j
                if prev[t, u] >= 0 and idx != prev[t, u]:
                    last[t, u] = n
                prev[t, u] = idx
                val[t, u] = (tt[p] >> idx) & 1
        changed = False
        for L in range(2):
            if n < L:
                continue
            for x in range(NT):
                for y in range(NT):
                    c = val[x, y] == 1
                    if hc[L, x, y] and not c:
                        hc[L, x, y] = False; changed = True
                    if hd[L, x, y] and c:
                        hd[L, x, y] = False; changed = True
        if not changed and n >= 2:
            return val, n, last, hc, hd
    return val, -1, last, hc, hd


@njit(cache=True)
def _audit_rc(nat, ak, al, af, aa, tt, src, con, nc_type, cs_type, rep, BC, BD, mask, rc, hc, hd, val, S):
    """contracts._audit with the access flag: [contract reads, true, violations, source reads legible, masked,
    source boxes true, source violations, carrier pairs, carrier pairs off-table, recompute mismatch]."""
    NT = src.shape[0]
    out = np.zeros(10, np.int64)
    for t in range(NT):
        p = src[t]
        for u in range(NT):
            if con[t] >= 0 and con[u] >= 0:
                out[7] += 1
                if val[t, u] != S[con[t], con[u]]:
                    out[8] += 1
            idx = 0
            for j in range(nat[p]):
                f = af[p, j]
                if f == 0:
                    tg = t
                elif f == 1:
                    tg = u
                else:
                    a = aa[p, j]
                    tg = cs_type[a] if con[u] >= 0 else nc_type[a]
                L = al[p, j]
                want = 1 if ak[p, j] == 0 else 0
                if rc[t] == 1 and con[u] >= 0 and con[tg] >= 0:
                    x = rep[con[u]]; y = rep[con[tg]]
                    b = BC[L, x, y] if ak[p, j] == 0 else BD[L, x, y]
                    out[0] += 1
                    if b:
                        out[1] += 1
                        if val[u, tg] != want:
                            out[2] += 1
                elif mask[t, u] == 0:
                    b = False
                    out[4] += 1
                else:
                    b = hc[L, u, tg] if ak[p, j] == 0 else hd[L, u, tg]
                    out[3] += 1
                    if b:
                        out[5] += 1
                        if val[u, tg] != want:
                            out[6] += 1
                if b: idx |= 1 << j
            if ((tt[p] >> idx) & 1) != val[t, u]:
                out[9] += 1
    return out


def reads_assignment(K, q):
    """Quenched per canonical source: nested in q."""
    u = np.random.default_rng(QSEED).random(K)
    return u < q


def rc_for(C, rule):
    NT = C.NT
    car = (C.tcon >= 0)
    if rule == 'asym':
        return np.ones(NT, np.int8)
    if rule == 'sym':
        return car.astype(np.int8)
    if rule.startswith('q'):
        r = reads_assignment(C.K, float(rule[1:]))
        return (car | r[C.tsrc]).astype(np.int8)
    raise ValueError(rule)


def setup():
    C = CT.Contracts(8); C.compute_validity(); C.build_types()
    # same literal fallback as Contracts.evaluate
    cs = C.cs_type.copy()
    for a in C.literal_without_own_carrier:
        c = C.cls[a]
        alt = [t for t in range(C.K, C.NT) if C.tcon[t] == c]
        cs[a] = alt[0] if alt else -1
    C._cs_eval = cs
    return C


def evaluate(C, b, rule, max_rounds=60):
    """Joint fixed point of the gate under an access rule (as Contracts.evaluate)."""
    nat, ak, al, af, aa, tt = C.arr
    NT = C.NT; cs = C._cs_eval
    rc = rc_for(C, rule)
    mask = np.ones((NT, NT), np.int8)
    kt = C.k[C.tsrc]
    seen = {}
    for r in range(max_rounds):
        val, worlds, last, hc, hd = _eval_types_rc(nat, ak, al, af, aa, tt, C.tsrc, C.tcon, C.nc_type, cs, C.rep, C.BC, C.BD,
                                                   mask, rc, 200)
        if worlds < 0:
            raise RuntimeError('type evaluation did not stabilize')
        if b >= CT.INF:
            return val, dict(rounds=1, cycle=False, worlds=int(worlds)), (last, hc, hd, mask, rc)
        new = ((kt[None, :] * (1 + last.T)) <= b).astype(np.int8)
        if (new == mask).all():
            return val, dict(rounds=r + 1, cycle=False, worlds=int(worlds)), (last, hc, hd, mask, rc)
        h = new.tobytes()
        if h in seen:
            mask = np.minimum(mask, new)
            val, worlds, last, hc, hd = _eval_types_rc(nat, ak, al, af, aa, tt, C.tsrc, C.tcon, C.nc_type, cs, C.rep, C.BC, C.BD,
                                                       mask, rc, 200)
            return val, dict(rounds=r + 1, cycle=True, worlds=int(worlds)), (last, hc, hd, mask, rc)
        seen[h] = r
        mask = new
    raise RuntimeError('gate iteration did not settle')


def audit(C, val, aux):
    last, hc, hd, mask, rc = aux
    nat, ak, al, af, aa, tt = C.arr
    o = _audit_rc(nat, ak, al, af, aa, tt, C.tsrc, C.tcon, C.nc_type, C._cs_eval, C.rep, C.BC, C.BD, mask, rc, hc, hd, val, C.S)
    keys = ['contract_reads', 'contract_box_true', 'contract_violations', 'source_reads_legible', 'source_reads_masked',
            'source_box_true', 'source_violations', 'carrier_pairs', 'carrier_pairs_off_table', 'recompute_mismatch']
    return {k: int(v) for k, v in zip(keys, o)}


def main():
    t0 = time.time()
    C = setup()
    old = np.load(os.path.join(RUNS, 'contracts_types.npz'))
    old0 = np.load(os.path.join(RUNS, 'contracts_types_b0.npz'))['val_0']
    assert (old['tsrc'] == C.tsrc).all() and (old['tcon'] == C.tcon).all()
    save = {}; info = {}
    for b, bl in ((0, '0'), (CT.INF, 'inf')):
        for rule in RULES:
            if bl == 'inf' and rule.startswith('q'):
                continue
            t = time.time()
            val, inf_, aux = evaluate(C, b, rule)
            a = audit(C, val, aux)
            save['val_%s_%s' % (bl, rule)] = val
            info['%s_%s' % (bl, rule)] = dict(info=inf_, audit=a, time_s=time.time() - t)
            print(bl, rule, inf_, a, '%.0fs' % (time.time() - t), flush=True)
    K = C.K
    for q in (0.25, 0.5):
        r = reads_assignment(K, q)
        info['readers_q%g' % q] = dict(n=int(r.sum()), mu=float(C.mu[r].sum()))
    info['repro_asym_b0'] = bool((save['val_0_asym'] == old0).all())
    info['repro_asym_inf'] = bool((save['val_inf_asym'] == old['val_inf']).all())
    np.savez_compressed(TYPES, **save)
    json.dump(info, open(os.path.join(RUNS, 'symmetric_gate_tables_info.json'), 'w'), indent=1)
    print('repro asym b0', info['repro_asym_b0'], 'inf', info['repro_asym_inf'], '%.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
