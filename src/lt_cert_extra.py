"""Extra cells for certificates as code, after the main run: cross-checker carriers whose scripts Run the other
checker's call instead of naming it as a hypothesis (does the regress of notes §1.7(e) occur?), and the same for the
naive checker.  Writes runs/certificates_as_code/extra_.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C

OUT = os.path.join(os.path.dirname(__file__), '..', 'runs', 'certificates_as_code')


def body():
    out = {}
    for K in (10 ** 6, 10 ** 7):
        V = K // 4
        progs, _ = C.build_arm(K, 'S')
        run_s = C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.RUN, 0)))
        d = C.h_getcerts(progs['CB'])
        dscr = [e for e in C.uncons(d) if e[0] == 'D']
        for nm, md in (('CBS2run', 5), ('CBNrun', 1)):
            progs[nm] = C.carrier(C.body_CB(md, V, K), C.cons([('C', run_s)] + dscr))
        progs['CBrun'] = C.carrier(C.body_CB(0, V, K), C.cons([('C', run_s)] + dscr))
        rows = {}
        for x, y in [('CB', 'CBS2run'), ('CBS2run', 'CB'), ('CBrun', 'CBS2'), ('CBrun', 'CBS2run'), ('CB', 'CBNrun'),
                     ('CBNrun', 'CB'), ('CBrun', 'CBNrun'), ('CBS2', 'CBS2run')]:
            L.CACHE.clear()
            r0 = L.STATS['regress']
            res, tot = C.check_value(C.WRAP_MODE[C.ID[{'CB': 'CHKS', 'CBrun': 'CHKS', 'CBS2': 'CHKS2', 'CBS2run': 'CHKS2',
                                                       'CBNrun': 'CHKN'}[y]]], V, progs[x], progs[y], 'C', K)
            rows['%s checked by %s' % (x, y)] = {'result': res, 'inner': tot - 1, 'regress_events': L.STATS['regress'] - r0,
                                                 'play_x': L.play(progs[x], progs[y], K)[0],
                                                 'play_y': L.play(progs[y], progs[x], K)[0]}
        out[str(K)] = rows
    return out


def selfprobe():
    """Supplement (after the main run): arm O with self-probe production.  The frozen procedure's probes are other
    carriers, so under the self-only checker no carrier gets a C script; here each carrier's C script is produced
    against its own (D-only) twin, then carried, and the arm-O cells are re-played."""
    out = {}
    for K in (10 ** 5, 10 ** 6, 10 ** 7):
        V = K // 4
        progs, _ = C.build_arm(K, 'O')
        prod = C.Producer()
        fam = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap']
        scripts = {}
        for nm in fam:
            bf = C.CARRIER_BODIES[nm]
            d = [e for e in C.uncons(C.h_getcerts(progs[nm]))]
            p1 = C.carrier(bf(2, V, K), C.cons(d))
            s = prod.produce(2, p1, p1, 'C', K, V)
            scripts[nm] = None if s is None else C.show_script(s)
            progs[nm] = C.carrier(bf(2, V, K), C.cons(([('C', s)] if s else []) + d))
        names = fam + ['C', 'D', 'Ccert', 'SFc', 'CB0']
        cells = {}
        for x in names:
            for y in names:
                cells['%s|%s' % (x, y)] = L.play(progs[x], progs[y], K)[0]
        out[str(K)] = {'scripts': scripts, 'cells': cells}
    return out


if __name__ == '__main__':
    if 'selfprobe' in sys.argv:
        res = L.run_big(selfprobe)
        json.dump(res, open(os.path.join(OUT, 'selfprobe_O.json'), 'w'), indent=1)
        fam = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap']
        for K, r in res.items():
            print(K, r['scripts'])
            for x in fam:
                print(' ', x, ' '.join(r['cells']['%s|%s' % (x, y)][0] + r['cells']['%s|%s' % (y, x)][0]
                                       for y in fam + ['Ccert', 'SFc', 'CB0']))
    else:
        res = L.run_big(body)
        json.dump(res, open(os.path.join(OUT, 'extra_.json'), 'w'), indent=1)
        for K, rows in res.items():
            for k, v in rows.items(): print(K, k, v)
