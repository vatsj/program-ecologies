"""Results table and support+transition rendering."""
import json
import numpy as np


def cell_report(chain, prov, lang, game, cfg, div_rate, thresh=1e-3, top_states=12):
    """Return (row dict, markdown text) for one sweep cell."""
    L = lang
    support = chain.support(thresh)
    pi_total = float(sum(w for _, w in support))
    eff = game.efficient_symmetric()
    # realised mean payoff per player under pi
    realised = 0.0
    mean_bits = 0.0
    for key, w in zip(chain.keys_list, chain.pi):
        ids, x, kind = chain.states[key]
        U = prov.U(ids); x = np.array(x)
        realised += w * float(x @ U @ x)
        mean_bits += w * float(np.dot(x, L.bits[list(ids)]))
    row = dict(cfg)
    row.update({
        'n_programs': int(len(prov.ids)),
        'n_classes': int(len(getattr(prov, 'classes', []))) or None,
        'n_states': len(chain.states),
        'n_terminal_classes': len(chain.terminal),
        'indeterminate': len(chain.indeterminate),
        'divergence_rate': float(div_rate),
        'mean_bits_support': mean_bits,
        'mean_payoff': realised,
        'efficient_payoff': eff,
        'deadweight_loss': eff - realised,
        'support': [(chain.describe_state(k, L), float(w)) for k, w in support[:top_states]],
    })
    lines = []
    lines.append('### %s' % ', '.join('%s=%s' % kv for kv in cfg.items()))
    lines.append('')
    lines.append('programs %d, classes %s, states %d, terminal classes %d, indeterminate %d, divergence rate %.4f' % (
        row['n_programs'], row['n_classes'], row['n_states'], row['n_terminal_classes'], row['indeterminate'], div_rate))
    lines.append('mean payoff %.4f, efficient %.4f, deadweight loss %.4f, mean bits in support %.2f' % (realised, eff, eff - realised, mean_bits))
    if len(chain.terminal) > 1:
        lines.append('absorption: ' + ', '.join('class %d: %.3f' % (c, p) for c, p in chain.absorb.items()))
    lines.append('')
    lines.append('| pi | state |')
    lines.append('|---|---|')
    for key, w in support[:top_states]:
        lines.append('| %.4f | %s |' % (w, chain.describe_state(key, L)))
    lines.append('')
    lines.append('Transitions out of the support (share of mutation events, mutants responsible):')
    lines.append('')
    for key, w in support[:top_states]:
        outs = chain.out_transitions(key)
        if not outs:
            lines.append('- %s: absorbing (no exits)' % chain.describe_state(key, L))
            continue
        lines.append('- %s' % chain.describe_state(key, L))
        for share, b, muts in outs:
            ms = ', '.join('%s (%.2e)' % (L.src(q), mw) for q, mw in muts)
            lines.append('    - %.2e -> %s   via %s' % (share, chain.describe_state(b, L), ms))
    if chain.indeterminate:
        lines.append('')
        lines.append('INDETERMINATE transitions (replicator did not converge): %d; first: from %s with mutant %s' % (
            len(chain.indeterminate), chain.describe_state(chain.indeterminate[0][0], L), L.src(chain.indeterminate[0][1])))
    lines.append('')
    return row, '\n'.join(lines)


def write_table(rows, path):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys and k != 'support':
                keys.append(k)
    with open(path, 'w') as f:
        f.write('| ' + ' | '.join(keys) + ' | support |\n')
        f.write('|' + '---|' * (len(keys) + 1) + '\n')
        for r in rows:
            vals = []
            for k in keys:
                v = r.get(k, '')
                vals.append('%.4g' % v if isinstance(v, float) else str(v))
            sup = '; '.join('%.3f %s' % (w, s) for s, w in r['support'][:4])
            f.write('| ' + ' | '.join(vals) + ' | ' + sup + ' |\n')
    with open(path.replace('.md', '.json'), 'w') as f:
        json.dump(rows, f, indent=1, default=str)
