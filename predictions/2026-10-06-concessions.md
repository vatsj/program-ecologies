# Predictions: concessions, a boss grammar with probes (2026-10-06)

Spec: `specs/2026-10-06-concessions.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-06-concessions-gpt-6.1-sol.md`; where
they differ the spec's [after review] text is the resolution). Code: `src/concessions.py`, `src/concessions_report.py`,
`tests/test_concessions.py` (4 pass). Committed before any chain or lottery run; the static tables below were
computed first and are included as the static addendum the spec allows (`runs/concessions-static.json`).

## Design as run

- **Game and workers** unchanged: the union run's social organization game (wage s ∈ {0, 1/4, 1/2}, whack policy
  ∈ {strike, none, source}, L = 1, c the whack cost) and its quorum-arm worker grammar (n = 10, level-0 boxes, 452
  functions, 364 classes), length prior.
- **Probe semantics.** `BOX_L(W_j(^(s',none)) = a)`: the quoted encounter ((s', none), W1, W2), with the current
  encounter's two workers and the constant boss (s', none), is evaluated on its own linear GL Kripke chain; the probe
  holds at world n of the main encounter iff W_j's *executed* action in the quoted encounter equalled a at every
  world m with L ≤ m < n (so every strike probe is vacuously true at world 0, and at world ≤ L for L = 1). CC: executed
  = committed. RR: executed = after the per-world rational override of `src/union_enforcement.py`, ties to the
  committed recommendation; recommended and executed quoted plays are both recorded. Tests: for probe-free bosses the
  evaluator equals `union.encounter` / `union_enforcement.encounter_e` on 297 bosses × 449 worker pairs × 4
  evaluators; an independent history-based trace reproduces the stable play, box monotonicity and Lemma 0 (base
  boxes and probes); W1↔W2 slot symmetry; the named plays below.
- **Grammars.** Boss atoms: the union run's `BOX(W_j = work/strike)` (level 0) plus probes at L ∈ {0, 1}, j ∈ {1, 2},
  a ∈ {work, strike}: P₀ the 0-boss probes (8 atoms), P₀₁ the 0- and 1/4-boss probes (16 atoms). D\* (two probes,
  three outcomes) first appears at **n = 11**, where P₀₁ has **439,209 boss functions**: the dense class tensor does
  not fit the chain, so the chain language is built by the spec's **mass-preserving substitution**: every constant
  and one-atom function of the n = 11 grammar (1,449) plus the eight D\* variants (`D*_j` with probe levels L₁/₄, L₀ ∈
  {0, 1}), exact behavioural classes over all 452 × 452 worker pairs, and each class carries the n = 11 prior mass of
  every function with its behaviour (two-atom functions assigned by a fingerprint over 3,000 worker pairs; 550
  merges re-checked exactly, 0 failures). Two-atom functions with a novel policy are null mutations (P₀₁: 0.0133 of
  the boss prior, 376,699 policies); their best invasion of each named state is audited below. P₀ uses its own
  12-atom grammar at the same cutoff n = 11 (152,937 functions; one-atom functions included, null 0.0125). **Sham**:
  P₀₁'s exact function list and masses with every probe replaced by a literal constant at every world (true for
  a = work, false for a = strike); a box of a false sentence would be true at world 0 and act as a world-0 wage faker,
  so a literal is the inert choice. It lumps into the union run's 297 boss classes. **Reference (mass-preserved)**:
  P₀₁'s prior with every probe-carrying function removed as a null mutation (0.064 of the mass) and every other
  function keeping its P₀₁ mass (the nine constants 0.1025 each in both).
- **Chain** (`union_chain.UChain`: hybrid exploration, log-scaled GTH core; seeds = every named boss × named worker
  pair plus every strict-NE triple of the class game, the audit's discovery for fixed-role chains; dense log GTH
  re-solve as a check where the explored set ≤ 6,000 states; θ = 10⁻⁹, sensitivity at 10⁻¹¹ for the main cells).
  Twin-expanded = lumped here: states are monomorphic triples, every slot mutant is a complete transition, and the
  classes are exact behavioural classes (strongly lumpable), so twin drift is already in the generator.
- **Basin rates.** Basins by outcome summary: fair, 1/4 (intermediate), zero wage, whacking (realized repression);
  strike and scab-split states are transient. k[A→B] = Σ_{i∈A} π_i Σ_{j∉A} q_ij h_B(j) / π_A per mutation event, h_B the
  hitting probability of B before any other basin (sparse LU on the jump chain of the explored generator), with
  residence times and return fractions.
- **Preservation of demands.** For the fair states carrying 0.99 of the fair mass (≤ 60 states): the neutral worker
  substitutes in either slot, classified by demand (smallest quoted wage, 0 or 1/4, at which the worker works beside
  the resident other worker; else ≥ 1/2) against the resident replaced; the statistic is the fair π-fraction with a
  demand-lowering neutral substitute, and with one after whose fixation some boss class strictly invades.
- **Three-role distribution threshold** (social organization lottery definition): among π-states with positive total
  payoff, the fraction whose minimum share is ≥ 1/6.
- **Lottery**: ε = 0, I = 16, N = 100 per slot, mN = 0.1, c = 0.5, horizon 10⁵, 40 runs, seeds iid from each slot's
  prior over the chain language's classes (null mass removed), the island Moran kernel of `src/sog_lottery.py` with
  the verified-closed stop on the global support. **Fair island** = locally closed (every present class of each slot
  gives the same play against every combination of the island's present classes) with play (1/2, none-executed, W, W).
  Establishment = first check (every generation to 2,000, every 25 to 10⁴, every 100 after) with some fair island,
  censored at the stop; persistence = fraction of islands fair at the stop (closed runs are frozen) or horizon.

## Static addendum (computed before this file)

**Static findings, evaluator-checked (CC, c = 0.5).**
- *The accommodation ratchet is real (sol).* T₀ beside D₀ in the read slot W1 is neutral (D₀ pays it 1/2; W1 neutral
  mass 0.0027 at (D₀, T₁, T₁) includes T₀); at (D₀, T₀, T₀) the constant 1/4 bosses invade strictly (+0.5, mass 0.34,
  1.6·10⁻² per event at N = 10⁴): no probe is needed for the cut. Against D\* T₀ in W1 earns 1/4 and is deleterious.
- *D\* protects only the slot it reads.* At F\* = (D\*, T₁, T₁) the unread slot W2 has neutral substitutes of mass 0.499
  (the scab among them, demand 0), so a demand-lowering neutral worker substitute exists in P₀₁'s fair state.
- *Probes bring their own world-0 wage fakers.* `if(BOX(W1(^(0,none))=work),(1/2,·),(0,·))` pays 1/2 at world 0 (the
  probe is vacuous there), the militants' `BOX(s ∈ {0,1/4})` fails forever, and the boss pays 0 for work. Strict boss
  entry at F\*, F₀ = (D₀, T₁, T₁) and Fc = ((1/2,none), T₁, T₁): mass 0.0095 in the chain language (6.3·10⁻⁴ per event,
  N-independent) plus 0.0021 among the excluded two-atom policies. Wage fakers of the militant pair (no threat):
  P₀₁ 0.0032 (0.0021 probe-carrying), reference 0.0011.
- *The current-encounter concession C₁ does not land at (pay 0, strike)* (spec's hand analysis): against the militant
  pair it lands at **(pay 0, work)**; C₁ pays 1/2 at world 0 and is itself a world-0 wage faker.
- *The unfakeable fair state exists:* F\*⁻ = (D\*[L1], militant⁻, militant⁻), with level-1 probes (militant⁻ works at
  world 0 of the quoted encounter, so only BOX1 certifies it); no strict boss invader in the chain language or in the
  whole n = 11 grammar; its exits are the boss shadow (constant fair bosses, neutral) and W2 (neutral, 0.499). D0[L1]
  (one atom, mass 4.4·10⁻⁵) does the same with militant⁻ in W1.
- *Masses.* Each D\* variant 9.7·10⁻⁹ (no fingerprint duplicates in the n = 11 grammar); D₀, D₀q, D0[L1], D14
  4.4·10⁻⁵ each; constants 0.1025 each (0.923 of the boss prior); T₀, T₁, militant⁻, T₀⁻ 1.2·10⁻³ each; scab and
  constant striker 0.480 each.
- *Fakers by exhaustive search over the chain language* (CC): 195 worker classes (mass 0.50, the constant striker
  0.48 among them) are certified to strike against the 0-boss; 106 of them (mass 0.012) work for ≤ 0 against some
  boss class (128 / 0.014 at 1/4): soundness certifies play against the quoted boss only. Boss side: 184 wage-faker
  classes (mass 0.0083, of which probe-carrying 0.0055) pay < 1/2 for work from a self-pair that refuses every constant
  low wage; 684 coercers (mass 0.44: committed whackers). Lemma 0 reference: 0 boss classes get work from the
  militant⁻ pair at s < 1/2.
**Named workers** (union-run grammar, level-0 boxes about the current encounter):

- scab: `work`
- T0 (strike iff s = 0): `if(BOX(s in {0}),strike,work)`
- T1 = militant (strike iff s <= 1/4): `if(BOX(s in {0,1/4}),strike,work)`
- always strike: `strike`
- union: `f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS`
- militant- (strike iff not BOX(s = 1/2)): `if(BOX(s in {1/2}),work,strike)`
- T0- (strike iff not BOX(s in {1/4,1/2})): `if(BOX(s in {1/4,1/2}),work,strike)`

**Named bosses** (`W_j(^(s,none))` = worker j's play against the quoted constant boss (s, none) beside the current other worker):

- (0,strike): `(0,strike)`
- (0,none): `(0,none)`
- (0,source): `(0,source)`
- (1/4,strike): `(1/4,strike)`
- (1/4,none): `(1/4,none)`
- (1/4,source): `(1/4,source)`
- (1/2,strike): `(1/2,strike)`
- (1/2,none): `(1/2,none)`
- (1/2,source): `(1/2,source)`
- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/4,none),(0,none))`
- D0[L1] = if(BOX1(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX1(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D14 = if(BOX(W1(^1/4)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(1/4,none))=strike),(1/2,none),(0,none))`
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))): `f[BOX(W1(^(0,none))=strike),BOX(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- D*[L1] (both probes BOX1): `f[BOX1(W1(^(0,none))=strike),BOX1(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession): `if(BOX(W1=strike),(1/2,none),(0,none))`
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)): `if(BOX(W1=work),(1/2,none),(0,none))`
- committed whacker (0,strike): `(0,strike)`

**What the probes read** (quoted self-pair play, executed / recommended; fv = first world from which the strike probe fails, 127 = never):

| worker pair | vs (0,none) | vs (1/4,none) | fv strike@0 L0 / L1 | fv strike@1/4 L0 / L1 |
|---|---|---|---|---|
| scab | WW / WW | WW / WW | 0 / 1 | 0 / 1 |
| T0 | SS / SS | WW / WW | 127 / 127 | 1 / 1 |
| T1 | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| strike | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| union | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| mil- | SS / SS | SS / SS | 0 / 127 | 0 / 127 |
| T0- | SS / SS | WW / WW | 0 / 127 | 0 / 1 |

**Play and payoffs (boss, W1, W2) of every named boss against every named worker self-pair** (CC):

| boss | scab | T0 | T1 | strike | union | mil- | T0- |
|---|---|---|---|---|---|---|---|
| (0,strike) | (0,strike) WW (2, 0, 0) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) |
| (0,none) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| (0,source) | (0,source) WW (2, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (-1, -1, -1) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) |
| (1/4,strike) | (1/4,strike) WW (1.5, 0.25, 0.25) | (1/4,strike) WW (1.5, 0.25, 0.25) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) WW (1.5, 0.25, 0.25) |
| (1/4,none) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) |
| (1/4,source) | (1/4,source) WW (1.5, 0.25, 0.25) | (1/4,source) WW (1.5, 0.25, 0.25) | (1/4,source) SS (0, 0, 0) | (1/4,source) SS (0, 0, 0) | (1/4,source) SS (-1, -1, -1) | (1/4,source) SS (0, 0, 0) | (1/4,source) WW (1.5, 0.25, 0.25) |
| (1/2,strike) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) SS (-1, -1, -1) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) |
| (1/2,none) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| (1/2,source) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) SS (0, 0, 0) | (1/2,source) WW (0, -0.5, -0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) |
| D0 | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0q | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0[L1] | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D* | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D*[L1] | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| wage faker | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,strike) WW (2, 0, 0) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) |

**Mixed pairs** (W1, W2) for the bosses that read W1 (probe, current-encounter and faker bosses):

| boss | T1, scab | scab, T1 | T1, T0 | T0, T1 | T1, strike | strike, scab | scab, strike | mil-, scab |
|---|---|---|---|---|---|---|---|---|
| D0 | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0q | (1/4,none) SW (0.75, 0, 0.25) | (0,none) WS (1, 0, 0) | (1/4,none) SW (0.75, 0, 0.25) | (1/4,none) WS (0.75, 0.25, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SW (0.75, 0, 0.25) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0[L1] | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D* | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D*[L1] | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| wage faker | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,strike) SW (0.5, -1, 0) | (0,strike) WS (0.5, 0, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SW (0.5, -1, 0) | (0,strike) WS (0.5, 0, -1) | (0,strike) SW (0.5, -1, 0) |

### Languages (mass-preserving substitution)

| arm | grammar functions (n = 11) | included functions | boss classes | worker classes | boss mass included | merged by fingerprint | null (novel two-atom policies) | probe functions dropped (ref) | merge check failures |
|---|---|---|---|---|---|---|---|---|---|
| P01 | 439209 | 1457 | 1393 | 364 | 0.9861 | 0.0006 (12994) | 0.0133 (376699 policies) | 0.0000 | 0 / 150 |
| P0 | 152937 | 873 | 841 | 364 | 0.9867 | 0.0008 (6498) | 0.0125 (130615 policies) | 0.0000 | 0 / 150 |
| sham | 439209 | 1457 | 297 | 364 | 0.9861 | 0.0135 (423928) | 0.0004 (13752 policies) | 0.0000 | 0 / 550 |
| ref | 439209 | 297 | 297 | 364 | 0.9355 | 0.0000 (0) | 0.0004 (13752 policies) | 0.0641 | 0 / 0 |

### Prior masses of the named classes

| boss class | P01 | P0 | sham | ref |
|---|---|---|---|---|
| (0,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (0,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (0,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| D0 | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D0q | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D0[L1] | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D14 | 4.4e-05 | – | 0.11 | – |
| D* | 9.7e-09 | – | 0.11 | – |
| D*[L1] | 9.7e-09 | – | 0.11 | – |
| C1 | 4.4e-05 | 7.4e-05 | 5.3e-05 | 4.4e-05 |
| wage faker | 4.4e-05 | 7.4e-05 | 5.3e-05 | 4.4e-05 |
| committed whacker | 0.10 | 0.10 | 0.11 | 0.10 |
| D* family (8 variants, each) | 9.7e-09 | – | – | – |
| all constants | 0.923 | 0.923 | 0.984 | 0.923 |
| all probe classes | 0.048 | 0.041 | 0.000 | 0.000 |

Worker masses (all arms): scab 0.48, T0 1.2e-03, T1 1.2e-03, strike 0.48, union 9.9e-06, mil- 1.2e-03, T0- 1.2e-03.


#### Named states, P01 (CC, c = 0.5)

| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |
|---|---|---|---|---|---|---|---|---|---|
| F*: D* | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.327 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| D*T0: D* | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0112; 5.2e-04 | 0.328 | 0.0040 | 0.499 | 0.0026 | W1 `if(BOX(s in {1/4}),strike,work)` (strict, Δ +0.25) | +0.5; 0.0024 |
| F*-: D*[L1] | militant- | militant- | (1/2,none) WW | 1, 0.5, 0.5 | 0.0000; 0.00 | 0.318 | 0.0053 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | none; 0.0000 |
| F0: D0 | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.327 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| R0: D0 | T0 | T0 | (1/2,none) WW | 1, 0.5, 0.5 | 0.3393; 0.02 | 0.328 | 0.0027 | 0.499 | 0.0000 | B `(1/4,none)` (strict, Δ +0.5) | +1; 0.0066 |
| Q0: D0q | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0112; 5.2e-04 | 0.328 | 0.0040 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +0.5; 0.0024 |
| Fc: (1/2,none) | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.225 | 0.4988 | 0.499 | 0.0000 | W1 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| Fs: (1/2,none) | scab | scab | (1/2,none) WW | 1, 0.5, 0.5 | 0.6578; 0.04 | 0.226 | 0.0198 | 0.020 | 0.0000 | B `(0,none)` (strict, Δ +1) | +1; 0.0088 |
| Z: (0,none) | scab | scab | (0,none) WW | 2, 0, 0 | 0.0000; 0.00 | 0.226 | 0.5198 | 0.520 | 0.0000 | W1 `strike` (neutral-change, Δ +0) | none; 0.0000 |
| ZS: (0,none) | strike | strike | (0,none) SS | 0, 0, 0 | 0.0000; 0.00 | 0.555 | 0.5198 | 0.520 | 0.0000 | W1 `work` (neutral-change, Δ +0) | none; 0.0000 |
| ZT1: (0,none) | T1 | T1 | (0,none) SS | 0, 0, 0 | 0.3368; 0.03 | 0.331 | 0.9988 | 0.999 | 0.0000 | B `(1/2,strike)` (strict, Δ +1) | +2; 0.0062 |

#### Named states, P0 (CC, c = 0.5)

| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |
|---|---|---|---|---|---|---|---|---|---|
| F0: D0 | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0107; 7.1e-04 | 0.326 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0022 |
| R0: D0 | T0 | T0 | (1/2,none) WW | 1, 0.5, 0.5 | 0.3385; 0.02 | 0.328 | 0.0027 | 0.499 | 0.0000 | B `(1/4,strike)` (strict, Δ +0.5) | +1; 0.0061 |
| Q0: D0q | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0107; 5.0e-04 | 0.328 | 0.0040 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +0.5; 0.0022 |
| Fc: (1/2,none) | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0107; 7.1e-04 | 0.224 | 0.4988 | 0.499 | 0.0000 | W1 `work` (neutral-keep, Δ +0) | +1; 0.0022 |
| Fs: (1/2,none) | scab | scab | (1/2,none) WW | 1, 0.5, 0.5 | 0.6584; 0.04 | 0.227 | 0.0198 | 0.020 | 0.0000 | B `(0,none)` (strict, Δ +1) | +1; 0.0083 |
| Z: (0,none) | scab | scab | (0,none) WW | 2, 0, 0 | 0.0000; 0.00 | 0.227 | 0.5198 | 0.520 | 0.0000 | W1 `strike` (neutral-change, Δ +0) | none; 0.0000 |
| ZS: (0,none) | strike | strike | (0,none) SS | 0, 0, 0 | 0.0000; 0.00 | 0.556 | 0.5198 | 0.520 | 0.0000 | W1 `work` (neutral-change, Δ +0) | none; 0.0000 |
| ZT1: (0,none) | T1 | T1 | (0,none) SS | 0, 0, 0 | 0.3372; 0.03 | 0.331 | 0.9988 | 0.999 | 0.0000 | B `(1/2,strike)` (strict, Δ +1) | +2; 0.0059 |

## RE predictions (verbatim from the spec)

1. **The accommodation ratchet is real with the zero-wage probe alone and absent with the full discriminator:**
   in P₀, T₀ is neutral against D₀ and the 1/4-boss strictly invades after it, so P₀ CC's π sits at the smallest
   positive wage (1/4 occupancy ≥ 0.5 at N = 10⁴, fair ≤ 0.1); in P₀₁, T₀ is deleterious against D\* and the fair
   state's only neutral exit is the boss shadow. *Falsifier:* P₀ fair ≥ 0.3 at 10⁴, or a neutral worker exit from
   (D\*, militant, militant) other than through the boss shadow.
2. **With the full discriminator the fair share grows with N under the length prior:** P₀₁ CC at c = 0.5 gives fair
   ≥ 0.3 at N = 10⁴ with a positive log-odds slope, against ≤ 0.005 for the reference and ≤ 0.05 for the sham
   grammar (expressivity, not prior mass). The exponent is not predicted; the basin-rate calculation is the claim.
   *Falsifier:* P₀₁ fair ≤ 0.1 at 10⁴, or the sham grammar within 0.05 of P₀₁. Grey zone 0.1–0.3.
3. **No quorum is needed:** union mass in P₀₁'s fair support ≤ 0.1. *Falsifier:* ≥ 0.5.
4. **RR gives the smallest positive wage** (sol's reading adopted: the militant's strike at 1/4 is overridden, so D\*
   pays 1/4; 1/4 occupancy ≥ 0.5, fair ≤ 0.1 at N = 10⁴) **and the pool gives zero wage** (fair ≤ 0.05). *Falsifier:*
   RR fair ≥ 0.3, or pool fair ≥ 0.2.
5. **Quickly, in the lottery:** P₀₁ CC reaches a fair island within 500 generations in ≥ 0.6 of runs against ≤ 0.1
   for the reference, and ≥ 0.5 of its islands are fair at the horizon. *Falsifier:* ≤ 0.3 of runs reaching a fair
   island by 10⁴, or fair persistence ≤ 0.2.
6. **The spoilers are accommodating workers and alternative bosses, not fakers** [after review]: D\*'s fakers have
   mass ≤ 10⁻³ and change nothing by more than 0.05; the preservation-of-demands statistic shows that every neutral
   worker substitute of the P₀₁ fair state is a militant twin (same demands), and that P₀'s fair state has T₀ as a
   demand-lowering neutral substitute. *Falsifier:* a faker of mass ≥ 10⁻² strictly invading the P₀₁ fair state, or a
   demand-lowering neutral substitute in P₀₁'s fair state.

The RS's prediction is item 5 and the direction of 2; the RE invites him to put numbers on them.

## The RS's prediction (2026-10-06, as stated)

"Bosses adopt concessions of the form 'if they strike, give them what they want', and unions demand higher wages and
get them quickly." No numbers were added. Scored as below (verdict rules).

## Subagent predictions (made after the static tables, before any chain or lottery run)

The static tables decide two RE clauses in advance (the unread slot's neutral scab at F\*, and probe-carrying wage
fakers of mass 0.0095 at F\*); what follows is about π and the lottery.

- **S1 (the length prior still decides).** P₀₁ CC, c = 0.5: fair ≤ 0.02 at N = 10³ and 10⁴. D\* (9.7·10⁻⁹) cannot
  compete with the constant fair bosses (0.10 each) for entry, and every fair state built on T₁ has an N-independent
  strict faker exit. *Falsifier:* fair ≥ 0.1 at either N. Grey zone 0.02–0.1.
- **S2 (expressivity adds little).** |fair(P₀₁) − fair(ref)| ≤ 0.01 at N = 10⁴ (CC, c = 0.5); the sham equals the
  reference on every summary to 0.005 (it lumps into the same 297 classes; only class masses differ, by ≤ 7%).
  *Falsifier:* P₀₁ − ref ≥ 0.05 on fair, or sham − ref ≥ 0.02 on any summary.
- **S3 (no ratchet in π).** P₀ CC at N = 10⁴: 1/4 occupancy (s = 1/4, both work) ≤ 0.05 and zero wage ≥ 0.4: the
  ratchet is real but runs through T₀ (1.2·10⁻³) and D₀ (7.5·10⁻⁵), far below the constants. *Falsifier:* 1/4
  occupancy ≥ 0.2.
- **S4 (fair exits).** The fair basin's escape rate (basin calculation) falls between N = 10³ and 10⁴ by a factor
  between 2 and 15 in P₀₁ CC (neutral 1/N exits dominate in π-weight, as in the union run's −0.83 slope, because the
  fakeable fair states carry little π). *Falsifier:* factor < 1.5 (strict N-independent exits dominate) or > 30.
- **S5 (who holds the fair mass).** P₀₁ CC, N = 10⁴: states with a probe-carrying boss hold ≤ 0.3 of the fair mass,
  and the unfakeable F\*⁻-type states (a probe boss with militant⁻ in the read slot) ≤ 0.1. *Falsifier:* probe-boss
  share of fair ≥ 0.6.
- **S6 (no quorum).** Union mass in P₀₁'s fair support ≤ 0.01. *Falsifier:* ≥ 0.1.
- **S7 (RR).** P₀₁ RR at N = 10³ and 10⁴: 1/4 occupancy ≥ 0.6, fair ≤ 0.02, within 0.05 of the reference RR on
  every summary (in RR the 1/4-probe never certifies a strike, since a rational worker works at 1/4, so P₀₁ RR has
  no fair discriminator; the constant striker remains the free enforcer of 1/4). *Falsifier:* 1/4 occupancy < 0.4 or
  fair ≥ 0.1.
- **S8 (pool).** P₀₁ CC + pool: zero wage ≥ 0.9 and fair ≤ 0.01 at c = 0.1; at c = 0.5 (the pool whacker ties the
  fair boss at 1 − s − c = 1/2) zero wage ≥ 0.6. *Falsifier:* fair ≥ 0.05 at c = 0.1.
- **S9 (lottery establishment).** P₀₁ CC: a fair island by generation 500 in ≤ 0.2 of runs and by 10⁴ in ≤ 0.3; the
  reference likewise. *Falsifier:* P₀₁ ≥ 0.5 of runs by 500.
- **S10 (lottery persistence).** Fair islands at the stop/horizon ≤ 0.05 (mean over runs) in P₀₁ CC and the
  reference. *Falsifier:* ≥ 0.2 in P₀₁ CC.
- **S11 (lottery RR).** P₀₁ RR: ≥ 0.6 of islands at s = 1/4 with production at the stop (social organization lottery
  RR-main: 0.90). *Falsifier:* ≤ 0.3.
- **S12 (preservation of demands).** ≥ 0.9 of P₀₁ CC's fair π (N = 10⁴) has a demand-lowering neutral worker
  substitute, and ≥ 0.5 has one after whose fixation some boss strictly invades. *Falsifier:* first ≤ 0.5.
- **S13 (no growth in N).** P₀₁ CC fair log-odds against log N over N ∈ {10², 10³, 10⁴, 3·10⁴} has slope ≤ 0.
  *Falsifier:* slope ≥ +0.2.

**Three-role distribution threshold** (reported, not a verdict): ≤ 0.02 of eligible π in every CC cell, ≤ 0.01 in RR
(only s = 1/2 with both working reaches a 1/6 minimum share).

## Verdict rules

- A prediction **holds** iff every stated clause holds at the stated N and c; **failed, falsifier fired** iff a
  falsifier condition holds; **failed** if a stated clause fails with no falsifier fired; **inconclusive** if the
  deciding number lies in a stated grey zone or moves across a threshold between θ = 10⁻⁹ and 10⁻¹¹.
- Clauses decided by the static tables (RE 1's "only neutral exit is the boss shadow", RE 6's substitute and faker
  clauses) are scored from the static tables and flagged as such; the static tables were computed before this file.
  RE 6's "D\*'s fakers have mass ≤ 10⁻³" is read as the total mass of boss classes that strictly invade
  (D\*, T₁, T₁) while paying < 1/2 (no-threat wage fakers), and "change nothing by more than 0.05" as fair(P₀₁) minus
  fair(P₀₁ with those classes removed as null mutations) at N = 10⁴, computed if the chain time allows.
- "1/4 occupancy" = π mass of states with s = 1/4 and both workers working (the intermediate summary); "fair" = π
  mass with s = 1/2, both working and no whack; RE 4's pool clause is scored at c = 0.1 and c = 0.5 separately.
- **The RS's prediction** holds iff (i) probe-concession bosses (pay 1/2 to the militant pair, 0 to the scab pair)
  hold ≥ 0.3 of π in P₀₁ CC at N = 10⁴, and (ii) RE 5's establishment clause holds (≥ 0.6 of P₀₁ CC lottery runs with a
  fair island within 500 generations); fails if both fail; partial otherwise.
- Lottery fractions are reported with Wilson 95% intervals over 40 runs; island fractions as mean ± 1.96 SE over
  runs. Chain claims are about π at the stated N (ε → 0); lottery claims are about the ε = 0 absorption lottery.
