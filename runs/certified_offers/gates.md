# Queue 79 gates (C1 tables unless marked; kappa = 50; K = 87)

## G1 soundness

- check map: C0 term = C1 primitive = host reference on all 95 programs and forgers, both sides: **True**
- accepted (28): Ocn, Ocp, FcSnoy, FcSnon, FcSnzy, FcSnzn, FcSpoy, FcSpon, FcSpzy, FcSpzn, FcDnfy, FcDnfn, FcDnzy, FcDnzn, FcDpfy, FcDpfn, FcDpzy, FcDpzn, Rcn, Rcp, Rcsn, Rcsp, Bcn, Bcp, PcPnzy, PcPnzn, PcPpzy, PcPpzn
- forgers rejected: {'XmBn': True, 'XfakeBn': True, 'XswapBn': True, 'XappBn': True, 'XbitBn': True, 'XopBn': True, 'XifBn': True, 'Xconst': True}
- catalogue certificates equal the host parse: True
- C1: 28 carriers; certified-branch profiles 95000, **false 0**; fallback profiles 116932, differing from the standalone fallback 448 {'FcSnoy': 12, 'FcSnon': 12, 'FcSnzy': 12, 'FcSnzn': 12, 'FcSpoy': 4, 'FcSpon': 4, 'FcSpzy': 4, 'FcSpzn': 4, 'FcDnfy': 44, 'FcDnfn': 44, 'FcDnzy': 44, 'FcDnzn': 44, 'FcDpfy': 36, 'FcDpfn': 36, 'FcDpzy': 36, 'FcDpzn': 36, 'Rcsn': 12, 'Rcsp': 4, 'Bcn': 12, 'Bcp': 4, 'PcPnzy': 12, 'PcPnzn': 12, 'PcPpzy': 4, 'PcPpzn': 4}
- C0: 28 carriers; certified-branch profiles 95000, **false 0**; fallback profiles 116932, differing from the standalone fallback 448 {'FcSnoy': 12, 'FcSnon': 12, 'FcSnzy': 12, 'FcSnzn': 12, 'FcSpoy': 4, 'FcSpon': 4, 'FcSpzy': 4, 'FcSpzn': 4, 'FcDnfy': 44, 'FcDnfn': 44, 'FcDnzy': 44, 'FcDnzn': 44, 'FcDpfy': 36, 'FcDpfn': 36, 'FcDpzy': 36, 'FcDpzn': 36, 'Rcsn': 12, 'Rcsp': 4, 'Bcn': 12, 'Bcp': 4, 'PcPnzy': 12, 'PcPnzn': 12, 'PcPpzy': 4, 'PcPpzn': 4}

| program | C0 check steps (w=0 / w=1) | C1 |
|---|---|---|
| C0 | F 24 / F 24 | F 51 |
| C1 | F 24 / F 24 | F 51 |
| C2 | F 24 / F 24 | F 51 |
| C3 | F 24 / F 24 | F 51 |
| C4 | F 24 / F 24 | F 51 |
| C5 | F 24 / F 24 | F 51 |
| C6 | F 24 / F 24 | F 51 |
| C7 | F 24 / F 24 | F 51 |
| C8 | F 24 / F 24 | F 51 |
| Snoy | F 39 / F 39 | F 51 |
| Snon | F 39 / F 39 | F 51 |
| Snzy | F 39 / F 39 | F 51 |
| Snzn | F 39 / F 39 | F 51 |
| Spoy | F 39 / F 39 | F 51 |
| Spon | F 39 / F 39 | F 51 |
| Spzy | F 39 / F 39 | F 51 |
| Spzn | F 39 / F 39 | F 51 |
| Dnfy | F 39 / F 39 | F 51 |
| Dnfn | F 39 / F 39 | F 51 |
| Dnzy | F 39 / F 39 | F 51 |
| Dnzn | F 39 / F 39 | F 51 |
| Dpfy | F 39 / F 39 | F 51 |
| Dpfn | F 39 / F 39 | F 51 |
| Dpzy | F 39 / F 39 | F 51 |
| Dpzn | F 39 / F 39 | F 51 |
| Xn | F 39 / F 39 | F 51 |
| Xp | F 39 / F 39 | F 51 |
| Bn | F 39 / F 39 | F 51 |
| Bp | F 39 / F 39 | F 51 |
| Jf | F 24 / F 24 | F 51 |
| Jr | F 39 / F 39 | F 51 |
| Pnoy | F 39 / F 39 | F 51 |
| Pnon | F 39 / F 39 | F 51 |
| Pnzy | F 39 / F 39 | F 51 |
| Pnzn | F 39 / F 39 | F 51 |
| Ppoy | F 39 / F 39 | F 51 |
| Ppon | F 39 / F 39 | F 51 |
| Ppzy | F 39 / F 39 | F 51 |
| Ppzn | F 39 / F 39 | F 51 |
| Qnzy | F 39 / F 39 | F 51 |
| Qnzn | F 39 / F 39 | F 51 |
| Qpzy | F 39 / F 39 | F 51 |
| Qpzn | F 39 / F 39 | F 51 |
| Onfy | F 39 / F 39 | F 51 |
| Onfn | F 39 / F 39 | F 51 |
| Onzy | F 39 / F 39 | F 51 |
| Onzn | F 39 / F 39 | F 51 |
| Opfy | F 39 / F 39 | F 51 |
| Opfn | F 39 / F 39 | F 51 |
| Opzy | F 39 / F 39 | F 51 |
| Opzn | F 39 / F 39 | F 51 |
| Fnzy | F 39 / F 39 | F 51 |
| Fnzn | F 39 / F 39 | F 51 |
| Fpzy | F 39 / F 39 | F 51 |
| Fpzn | F 39 / F 39 | F 51 |
| Rnn | F 39 / F 39 | F 51 |
| Rny | F 39 / F 39 | F 51 |
| Rpn | F 39 / F 39 | F 51 |
| Rpy | F 39 / F 39 | F 51 |
| Ocn | T 167 / F 168 | T 51 |
| Ocp | F 167 / T 168 | F 51 |
| FcSnoy | T 167 / T 168 | T 51 |
| FcSnon | T 167 / T 168 | T 51 |
| FcSnzy | T 167 / T 168 | T 51 |
| FcSnzn | T 167 / T 168 | T 51 |
| FcSpoy | T 167 / T 168 | T 51 |
| FcSpon | T 167 / T 168 | T 51 |
| FcSpzy | T 167 / T 168 | T 51 |
| FcSpzn | T 167 / T 168 | T 51 |
| FcDnfy | T 167 / T 168 | T 51 |
| FcDnfn | T 167 / T 168 | T 51 |
| FcDnzy | T 167 / T 168 | T 51 |
| FcDnzn | T 167 / T 168 | T 51 |
| FcDpfy | T 167 / T 168 | T 51 |
| FcDpfn | T 167 / T 168 | T 51 |
| FcDpzy | T 167 / T 168 | T 51 |
| FcDpzn | T 167 / T 168 | T 51 |
| Rcn | T 167 / F 168 | T 51 |
| Rcp | F 167 / T 168 | F 51 |
| Rcsn | T 167 / F 168 | T 51 |
| Rcsp | F 167 / T 168 | F 51 |
| Bcn | T 167 / T 168 | T 51 |
| Bcp | T 167 / T 168 | T 51 |
| PcPnzy | T 167 / T 168 | T 51 |
| PcPnzn | T 167 / T 168 | T 51 |
| PcPpzy | T 167 / T 168 | T 51 |
| PcPpzn | T 167 / T 168 | T 51 |
| XmBn | F 39 / F 39 | F 51 |
| XfakeBn | F 107 / F 107 | F 51 |
| XswapBn | F 41 / F 41 | F 51 |
| XappBn | F 93 / F 93 | F 51 |
| XbitBn | F 134 / F 134 | F 51 |
| XopBn | F 131 / F 131 | F 51 |
| XifBn | F 24 / F 24 | F 51 |
| Xconst | F 24 / F 24 | F 51 |

## G2 reader-reader (every seat pattern, every non-carrier third slot)

| families | pointing triples | fair pair (x, y) | pair read timed out | third timed out | mean pair charge | non-pointing (fair pair) | other outcomes (pointing) |
|---|---|---|---|---|---|---|---|
| c_open x c_acc | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_open x c_firm | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_firm x c_firm | 90624 | 90624 | 0 | 1536 | 0.000 | 0 (0) | [] |
| c_acc x c_acc | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_firm x c_acc | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_prud x c_prud | 5664 | 5664 | 0 | 96 | 0.000 | 0 (0) | [] |
| c_open x c_open | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_accs x c_open | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_accs x c_firm | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_bully x c_firm | 11328 | 11328 | 0 | 192 | 0.000 | 0 (0) | [] |
| c_bully x c_open | 708 | 708 | 0 | 12 | 0.000 | 708 (0) | [] |
| c_bully x c_acc | 708 | 708 | 0 | 12 | 0.000 | 708 (0) | [] |
| c_bully x c_bully | 1416 | 1416 | 0 | 24 | 0.000 | 0 (0) | [] |
| c_prud x c_firm | 22656 | 22656 | 0 | 384 | 0.000 | 0 (0) | [] |

Three-carrier triples:

- Fc^3: 4096 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}
- Pc^3: 64 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}
- Bc,Fc,Fc: 512 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}

## G2_C0 reader-reader (every seat pattern, every non-carrier third slot)

| families | pointing triples | fair pair (x, y) | pair read timed out | third timed out | mean pair charge | non-pointing (fair pair) | other outcomes (pointing) |
|---|---|---|---|---|---|---|---|
| c_open x c_acc | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_open x c_firm | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_firm x c_firm | 90624 | 90624 | 0 | 1536 | 0.000 | 0 (0) | [] |
| c_acc x c_acc | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_firm x c_acc | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_prud x c_prud | 5664 | 5664 | 0 | 96 | 0.000 | 0 (0) | [] |
| c_open x c_open | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_accs x c_open | 354 | 354 | 0 | 6 | 0.000 | 1062 (0) | [] |
| c_accs x c_firm | 5664 | 5664 | 0 | 96 | 0.000 | 5664 (0) | [] |
| c_bully x c_firm | 11328 | 11328 | 0 | 192 | 0.000 | 0 (0) | [] |
| c_bully x c_open | 708 | 708 | 0 | 12 | 0.000 | 708 (0) | [] |
| c_bully x c_acc | 708 | 708 | 0 | 12 | 0.000 | 708 (0) | [] |
| c_bully x c_bully | 1416 | 1416 | 0 | 24 | 0.000 | 0 (0) | [] |
| c_prud x c_firm | 22656 | 22656 | 0 | 384 | 0.000 | 0 (0) | [] |

Three-carrier triples:

- Fc^3: 4096 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}
- Pc^3: 64 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}
- Bc,Fc,Fc: 512 triples, non-fair share 0.250, mean gross payoff per slot 0.2500 (cycle-free rule: 1/3); by preference orientation {'nnn': (1.0, 0.0), 'nnp': (0.0, 0.333), 'npn': (0.0, 0.333), 'npp': (0.0, 0.333), 'pnn': (0.0, 0.333), 'pnp': (0.0, 0.333), 'ppn': (0.0, 0.333), 'ppp': (1.0, 0.0)}

## G3 legibility (bully | victim; rows: the excluded-slot program class over all three rotations)

| bully, victim | excluded | n | bully read TO | victim read TO | excluded read TO | outcomes |
|---|---|---|---|---|---|---|
| Bn|Rcn | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rcn | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bn|Rcn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bn|Rcn | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bn|Rcn | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bn|Rcn | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rnn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rnn | Bc | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rnn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bn|Rnn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bn|Rnn | Fc | 48 | 48 | 48 | 48 | {'D': 30, 'F(be)': 18} |
| Bn|Rnn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bn|Rnn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rnn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bn|Rnn | Pc | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rnn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rnn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bn|Rnn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rnn | Rcs | 6 | 6 | 6 | 6 | {'D': 3, 'W': 3} |
| Bn|Rnn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bn|C3 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | Bc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Fc | 48 | 0 | 0 | 0 | {'U(b4,v2)': 48} |
| Bn|C3 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bn|C3 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | Pc | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rcsn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rcsn | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bn|Rcsn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bn|Rcsn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bn|Rcsn | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bn|Rcsn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bn|Rcsn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcsn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bn|Rcsn | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bn|Rcsn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rcsn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bn|Rcsn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcsn | Rcs | 6 | 3 | 3 | 3 | {'D': 3, 'F(ev)': 3} |
| Bn|Rcsn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bp|Rcp | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rcp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bp|Rcp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bp|Rcp | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bp|Rcp | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bp|Rcp | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rpn | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rpn | Bc | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rpn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bp|Rpn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bp|Rpn | Fc | 48 | 48 | 48 | 48 | {'D': 30, 'F(be)': 18} |
| Bp|Rpn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bp|Rpn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rpn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bp|Rpn | Pc | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rpn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rpn | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bp|Rpn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rpn | Rcs | 6 | 6 | 6 | 6 | {'W': 3, 'D': 3} |
| Bp|Rpn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bp|C0 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | Bc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Fc | 48 | 0 | 0 | 0 | {'U(b4,v2)': 48} |
| Bp|C0 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bp|C0 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | Pc | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rcsp | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rcsp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bp|Rcsp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bp|Rcsp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bp|Rcsp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bp|Rcsp | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bp|Rcsp | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcsp | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bp|Rcsp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bp|Rcsp | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rcsp | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bp|Rcsp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcsp | Rcs | 6 | 3 | 3 | 3 | {'F(ev)': 3, 'D': 3} |
| Bp|Rcsp | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcn|Rcn | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rcn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 24, 'F(ev)': 24} |
| Bcn|Rcn | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rcn | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 6, 'F(ev)': 6} |
| Bcn|Rcn | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rnn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bcn|Rnn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcn|Rnn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcn|Rnn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcn|Rnn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcn|Rnn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rnn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rnn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcn|Rnn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcn|Rnn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcn|Rnn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bcn|Rnn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|Rnn | Rcs | 6 | 3 | 3 | 3 | {'F(be)': 3, 'W': 3} |
| Bcn|Rnn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcn|C3 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|C3 | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcn|C3 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcn|C3 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcn|C3 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcn|C3 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rcsn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bcn|Rcsn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcn|Rcsn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcn|Rcsn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 24, 'F(ev)': 24} |
| Bcn|Rcsn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rcsn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcn|Rcsn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 6, 'F(ev)': 6} |
| Bcn|Rcsn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcn|Rcsn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bcn|Rcsn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcp|Rcp | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rcp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 24, 'F(be)': 24} |
| Bcp|Rcp | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rcp | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 6, 'F(be)': 6} |
| Bcp|Rcp | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rpn | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bcp|Rpn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcp|Rpn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcp|Rpn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcp|Rpn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcp|Rpn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rpn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rpn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcp|Rpn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcp|Rpn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcp|Rpn | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bcp|Rpn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|Rpn | Rcs | 6 | 3 | 3 | 3 | {'W': 3, 'F(be)': 3} |
| Bcp|Rpn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcp|C0 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|C0 | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcp|C0 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcp|C0 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcp|C0 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcp|C0 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rcsp | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bcp|Rcsp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcp|Rcsp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcp|Rcsp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 24, 'F(be)': 24} |
| Bcp|Rcsp | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rcsp | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcp|Rcsp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 6, 'F(be)': 6} |
| Bcp|Rcsp | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcp|Rcsp | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bcp|Rcsp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | X | 6 | 6 | 6 | 6 | {'D': 6} |

## G3_C0 legibility (bully | victim; rows: the excluded-slot program class over all three rotations)

| bully, victim | excluded | n | bully read TO | victim read TO | excluded read TO | outcomes |
|---|---|---|---|---|---|---|
| Bn|Rcn | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rcn | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bn|Rcn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcn | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bn|Rcn | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bn|Rcn | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|Rcn | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bn|Rcn | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|Rcn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcn | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rnn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rnn | Bc | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rnn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bn|Rnn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rnn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bn|Rnn | Fc | 48 | 48 | 48 | 48 | {'D': 30, 'F(be)': 18} |
| Bn|Rnn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bn|Rnn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rnn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rnn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bn|Rnn | Pc | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rnn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rnn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bn|Rnn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rnn | Rcs | 6 | 6 | 6 | 6 | {'D': 3, 'W': 3} |
| Bn|Rnn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bn|C3 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | Bc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|C3 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Fc | 48 | 0 | 0 | 0 | {'U(b4,v2)': 48} |
| Bn|C3 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bn|C3 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bn|C3 | Pc | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bn|C3 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|C3 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bn|Rcsn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bn|Rcsn | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bn|Rcsn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bn|Rcsn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bn|Rcsn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bn|Rcsn | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bn|Rcsn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bn|Rcsn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bn|Rcsn | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcsn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bn|Rcsn | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bn|Rcsn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bn|Rcsn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bn|Rcsn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(ev)': 3} |
| Bn|Rcsn | Rcs | 6 | 3 | 3 | 3 | {'D': 3, 'F(ev)': 3} |
| Bn|Rcsn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bp|Rcp | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rcp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bp|Rcp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcp | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bp|Rcp | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bp|Rcp | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|Rcp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bp|Rcp | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|Rcp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcp | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rpn | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rpn | Bc | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rpn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bp|Rpn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rpn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bp|Rpn | Fc | 48 | 48 | 48 | 48 | {'D': 30, 'F(be)': 18} |
| Bp|Rpn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bp|Rpn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rpn | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rpn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bp|Rpn | Pc | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rpn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rpn | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bp|Rpn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rpn | Rcs | 6 | 6 | 6 | 6 | {'W': 3, 'D': 3} |
| Bp|Rpn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bp|C0 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | Bc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|C0 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Fc | 48 | 0 | 0 | 0 | {'U(b4,v2)': 48} |
| Bp|C0 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bp|C0 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bp|C0 | Pc | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bp|C0 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|C0 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bp|Rcsp | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bp|Rcsp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 6} |
| Bp|Rcsp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bp|Rcsp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bp|Rcsp | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bp|Rcsp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 48} |
| Bp|Rcsp | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bp|Rcsp | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bp|Rcsp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcsp | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bp|Rcsp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 12} |
| Bp|Rcsp | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bp|Rcsp | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bp|Rcsp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'U(b4,v2)': 3} |
| Bp|Rcsp | Rcs | 6 | 3 | 3 | 3 | {'F(ev)': 3, 'D': 3} |
| Bp|Rcsp | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcn|Rcn | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rcn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcn | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 24, 'F(ev)': 24} |
| Bcn|Rcn | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rcn | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|Rcn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 6, 'F(ev)': 6} |
| Bcn|Rcn | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|Rcn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcn | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rnn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bcn|Rnn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcn|Rnn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcn|Rnn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rnn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcn|Rnn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcn|Rnn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rnn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rnn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rnn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcn|Rnn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcn|Rnn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcn|Rnn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bcn|Rnn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|Rnn | Rcs | 6 | 3 | 3 | 3 | {'F(be)': 3, 'W': 3} |
| Bcn|Rnn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcn|C3 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|C3 | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcn|C3 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|C3 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcn|C3 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcn|C3 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcn|C3 | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcn|C3 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcn|C3 | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'U(b4,v2)': 3} |
| Bcn|C3 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcn|Rcsn | B | 6 | 6 | 6 | 6 | {'D': 3, 'F(be)': 3} |
| Bcn|Rcsn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C4 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcn|Rcsn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcn|Rcsn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcn|Rcsn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 24, 'F(ev)': 24} |
| Bcn|Rcsn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcn|Rcsn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcn|Rcsn | Oc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcn|Rcsn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 6, 'F(ev)': 6} |
| Bcn|Rcsn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcn|Rcsn | R | 12 | 12 | 12 | 12 | {'D': 6, 'F(be)': 3, 'W': 3} |
| Bcn|Rcsn | Rc | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | Rcs | 6 | 0 | 0 | 0 | {'F(be)': 3, 'F(ev)': 3} |
| Bcn|Rcsn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcp|Rcp | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rcp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcp | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 24, 'F(be)': 24} |
| Bcp|Rcp | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rcp | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|Rcp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 6, 'F(be)': 6} |
| Bcp|Rcp | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|Rcp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcp | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rpn | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bcp|Rpn | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcp|Rpn | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcp|Rpn | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rpn | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcp|Rpn | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcp|Rpn | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rpn | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rpn | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rpn | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcp|Rpn | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcp|Rpn | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcp|Rpn | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bcp|Rpn | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|Rpn | Rcs | 6 | 3 | 3 | 3 | {'W': 3, 'F(be)': 3} |
| Bcp|Rpn | X | 6 | 6 | 6 | 6 | {'D': 6} |
| Bcp|C0 | B | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|C0 | Bc | 6 | 0 | 0 | 0 | {'F(be)': 6} |
| Bcp|C0 | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C1 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|C0 | F(single) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | F(two) | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | F2 | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | Fc | 48 | 0 | 0 | 0 | {'F(be)': 48} |
| Bcp|C0 | J | 6 | 0 | 0 | 3 | {'U(b4,v2)': 6} |
| Bcp|C0 | O | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | Oc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | P | 24 | 0 | 0 | 0 | {'U(b4,v2)': 24} |
| Bcp|C0 | Pc | 12 | 0 | 0 | 0 | {'F(be)': 12} |
| Bcp|C0 | Q | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | R | 12 | 0 | 0 | 0 | {'U(b4,v2)': 12} |
| Bcp|C0 | Rc | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | Rcs | 6 | 0 | 0 | 0 | {'U(b4,v2)': 3, 'F(be)': 3} |
| Bcp|C0 | X | 6 | 0 | 0 | 0 | {'U(b4,v2)': 6} |
| Bcp|Rcsp | B | 6 | 6 | 6 | 6 | {'F(be)': 3, 'D': 3} |
| Bcp|Rcsp | Bc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | C0 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C1 | 3 | 0 | 0 | 0 | {'F(ev)': 3} |
| Bcp|Rcsp | C2 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C3 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C4 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C5 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C6 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C7 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | C8 | 3 | 0 | 0 | 0 | {'U(b4,v2)': 3} |
| Bcp|Rcsp | F(single) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | F(two) | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | F2 | 12 | 12 | 12 | 12 | {'D': 9, 'F(be)': 3} |
| Bcp|Rcsp | Fc | 48 | 0 | 0 | 0 | {'F(ev)': 24, 'F(be)': 24} |
| Bcp|Rcsp | J | 6 | 3 | 3 | 3 | {'U(b4,v2)': 6} |
| Bcp|Rcsp | O | 24 | 24 | 24 | 24 | {'D': 15, 'F(be)': 9} |
| Bcp|Rcsp | Oc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | P | 24 | 24 | 24 | 24 | {'D': 18, 'F(be)': 6} |
| Bcp|Rcsp | Pc | 12 | 0 | 0 | 0 | {'F(ev)': 6, 'F(be)': 6} |
| Bcp|Rcsp | Q | 12 | 12 | 12 | 12 | {'D': 12} |
| Bcp|Rcsp | R | 12 | 12 | 12 | 12 | {'D': 6, 'W': 3, 'F(be)': 3} |
| Bcp|Rcsp | Rc | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | Rcs | 6 | 0 | 0 | 0 | {'F(ev)': 3, 'F(be)': 3} |
| Bcp|Rcsp | X | 6 | 6 | 6 | 6 | {'D': 6} |

## G4 mixed worlds (triples with a carrier and a simulating reader, third slot any program; shares of profiles)

| carrier x reader | n | carrier TO (regress) | reader TO | reader TO by regress | reader TO by cap |
|---|---|---|---|---|---|
| Bc x B | 2088 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Bc x F | 20880 | 0.621 (0.000) | 0.621 | 0.000 | 0.621 |
| Bc x O | 8352 | 0.644 (0.000) | 0.644 | 0.000 | 0.644 |
| Bc x P | 12528 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Bc x R | 4176 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Bc x X | 2088 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Fc x B | 16704 | 0.625 (0.000) | 0.625 | 0.000 | 0.625 |
| Fc x F | 167040 | 0.642 (0.000) | 0.642 | 0.000 | 0.642 |
| Fc x O | 66816 | 0.675 (0.000) | 0.675 | 0.000 | 0.675 |
| Fc x P | 100224 | 0.625 (0.000) | 0.625 | 0.000 | 0.625 |
| Fc x R | 33408 | 0.625 (0.000) | 0.625 | 0.000 | 0.625 |
| Fc x X | 16704 | 0.625 (0.000) | 0.625 | 0.000 | 0.625 |
| Oc x B | 2088 | 0.000 (0.000) | 0.227 | 0.000 | 0.227 |
| Oc x F | 20880 | 0.000 (0.000) | 0.262 | 0.000 | 0.262 |
| Oc x O | 8352 | 0.000 (0.000) | 0.454 | 0.000 | 0.454 |
| Oc x P | 12528 | 0.000 (0.000) | 0.227 | 0.000 | 0.227 |
| Oc x R | 4176 | 0.000 (0.000) | 0.227 | 0.000 | 0.227 |
| Oc x X | 2088 | 0.000 (0.000) | 0.227 | 0.000 | 0.227 |
| Pc x B | 4176 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Pc x F | 41760 | 0.621 (0.000) | 0.621 | 0.000 | 0.621 |
| Pc x O | 16704 | 0.644 (0.000) | 0.644 | 0.000 | 0.644 |
| Pc x P | 25056 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Pc x R | 8352 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Pc x X | 4176 | 0.609 (0.000) | 0.609 | 0.000 | 0.609 |
| Rc x B | 2088 | 0.000 (0.000) | 0.238 | 0.000 | 0.238 |
| Rc x F | 20880 | 0.000 (0.000) | 0.334 | 0.000 | 0.334 |
| Rc x O | 8352 | 0.000 (0.000) | 0.477 | 0.000 | 0.477 |
| Rc x P | 12528 | 0.000 (0.000) | 0.238 | 0.000 | 0.238 |
| Rc x R | 4176 | 0.000 (0.000) | 0.238 | 0.000 | 0.238 |
| Rc x X | 2088 | 0.000 (0.000) | 0.238 | 0.000 | 0.238 |
| Rcs x B | 2088 | 0.747 (0.000) | 0.747 | 0.000 | 0.747 |
| Rcs x F | 20880 | 0.761 (0.000) | 0.761 | 0.000 | 0.761 |
| Rcs x O | 8352 | 0.787 (0.000) | 0.787 | 0.000 | 0.787 |
| Rcs x P | 12528 | 0.747 (0.000) | 0.747 | 0.000 | 0.747 |
| Rcs x R | 4176 | 0.747 (0.000) | 0.747 | 0.000 | 0.747 |
| Rcs x X | 2088 | 0.747 (0.000) | 0.747 | 0.000 | 0.747 |

"by regress" above counts the evaluator's identical-key regress detector, which arm T's nested reads never trigger (their keys differ level by level); the operational split is G4b.

## G4b timed-out reads re-evaluated with every cap and the root fuel x20 (sample per group): still timed out = regress, completed = cap exhaustion

| carrier x reader | timed-out profiles | sampled | reader reads: n / still TO | carrier fallback reads: n / still TO |
|---|---|---|---|---|
| Bc x B | 848 | 300 | 146 / 146 | 154 / 154 |
| Bc x F | 8640 | 300 | 131 / 131 | 169 / 169 |
| Bc x O | 3584 | 300 | 144 / 144 | 156 / 156 |
| Bc x P | 5088 | 300 | 152 / 152 | 148 / 148 |
| Bc x R | 1696 | 300 | 146 / 146 | 154 / 154 |
| Bc x X | 848 | 300 | 140 / 140 | 160 / 160 |
| Fc x B | 6960 | 300 | 158 / 158 | 142 / 142 |
| Fc x F | 71456 | 300 | 161 / 161 | 139 / 139 |
| Fc x O | 30080 | 300 | 145 / 145 | 155 / 155 |
| Fc x P | 41760 | 300 | 160 / 160 | 140 / 140 |
| Fc x R | 13920 | 300 | 140 / 140 | 160 / 160 |
| Fc x X | 6960 | 300 | 151 / 151 | 149 / 149 |
| Oc x B | 158 | 158 | 158 / 158 | 0 / 0 |
| Oc x F | 1820 | 300 | 300 / 300 | 0 / 0 |
| Oc x O | 1264 | 300 | 300 / 300 | 0 / 0 |
| Oc x P | 948 | 300 | 300 / 300 | 0 / 0 |
| Oc x R | 316 | 300 | 300 / 300 | 0 / 0 |
| Oc x X | 158 | 158 | 158 / 158 | 0 / 0 |
| Pc x B | 1696 | 300 | 158 / 158 | 142 / 142 |
| Pc x F | 17280 | 300 | 140 / 140 | 160 / 160 |
| Pc x O | 7168 | 300 | 165 / 165 | 135 / 135 |
| Pc x P | 10176 | 300 | 156 / 156 | 144 / 144 |
| Pc x R | 3392 | 300 | 150 / 150 | 150 / 150 |
| Pc x X | 1696 | 300 | 153 / 153 | 147 / 147 |
| Rc x B | 166 | 166 | 166 / 166 | 0 / 0 |
| Rc x F | 2324 | 300 | 300 / 300 | 0 / 0 |
| Rc x O | 1328 | 300 | 300 / 300 | 0 / 0 |
| Rc x P | 996 | 300 | 300 / 300 | 0 / 0 |
| Rc x R | 332 | 300 | 300 / 300 | 0 / 0 |
| Rc x X | 166 | 166 | 166 / 166 | 0 / 0 |
| Rcs x B | 1040 | 300 | 162 / 162 | 138 / 138 |
| Rcs x F | 10592 | 300 | 155 / 155 | 145 / 145 |
| Rcs x O | 4384 | 300 | 162 / 162 | 138 / 138 |
| Rcs x P | 6240 | 300 | 161 / 161 | 139 / 139 |
| Rcs x R | 2080 | 300 | 144 / 144 | 156 / 156 |
| Rcs x X | 1040 | 300 | 140 / 140 | 160 / 160 |

The same with the third slot restricted to constants (the only reads are between the carrier and the reader):

| carrier x reader | timed-out profiles | sampled | reader reads: n / still TO | carrier fallback reads: n / still TO |
|---|---|---|---|---|
| Bc x B | 36 | 36 | 18 / 18 | 18 / 18 |
| Bc x F | 488 | 300 | 157 / 157 | 143 / 143 |
| Bc x O | 288 | 288 | 144 / 144 | 144 / 144 |
| Bc x P | 216 | 216 | 108 / 108 | 108 / 108 |
| Bc x R | 72 | 72 | 36 / 36 | 36 / 36 |
| Bc x X | 36 | 36 | 18 / 18 | 18 / 18 |
| Fc x B | 416 | 300 | 150 / 150 | 150 / 150 |
| Fc x F | 5632 | 300 | 149 / 149 | 151 / 151 |
| Fc x O | 3328 | 300 | 159 / 159 | 141 / 141 |
| Fc x P | 2496 | 300 | 149 / 149 | 151 / 151 |
| Fc x R | 832 | 300 | 143 / 143 | 157 / 157 |
| Fc x X | 416 | 300 | 148 / 148 | 152 / 152 |
| Pc x B | 72 | 72 | 36 / 36 | 36 / 36 |
| Pc x F | 976 | 300 | 156 / 156 | 144 / 144 |
| Pc x O | 576 | 300 | 142 / 142 | 158 / 158 |
| Pc x P | 432 | 300 | 148 / 148 | 152 / 152 |
| Pc x R | 144 | 144 | 72 / 72 | 72 / 72 |
| Pc x X | 72 | 72 | 36 / 36 | 36 / 36 |
| Rcs x B | 36 | 36 | 18 / 18 | 18 / 18 |
| Rcs x F | 488 | 300 | 154 / 154 | 146 / 146 |
| Rcs x O | 288 | 288 | 144 / 144 | 144 / 144 |
| Rcs x P | 216 | 216 | 108 / 108 | 108 / 108 |
| Rcs x R | 72 | 72 | 36 / 36 | 36 / 36 |
| Rcs x X | 36 | 36 | 18 / 18 | 18 / 18 |

## G5 first 59 programs unchanged

- {'code': True, 'steps': True, 'nto': True, 'fo': True, 'JT': True}

## V3 C1 vs C0

- profiles 658503; action differences 0 (without a timeout change 0); timeout differences 856; forfeit differences 0; outcome triples differing 0 (of which without any carrier 0); first-59 block identical: True
  - Snoy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Snon: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Snzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Snzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Spoy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Spon: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Spzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Spzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Dnfy: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dnfn: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dnzy: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dnzn: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dpfy: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dpfn: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dpzy: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Dpzn: {'code': 0, 'nto': 19, 'fo': 0, 'code_with_nto_change': 0}
  - Xn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Xp: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Bn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Bp: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Pnoy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Pnon: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Pnzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Pnzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Ppoy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Ppon: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Ppzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Ppzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Qnzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Qnzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Qpzy: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Qpzn: {'code': 0, 'nto': 4, 'fo': 0, 'code_with_nto_change': 0}
  - Onfy: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Onfn: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Onzy: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Onzn: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Opfy: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Opfn: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Opzy: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
  - Opzn: {'code': 0, 'nto': 20, 'fo': 0, 'code_with_nto_change': 0}
