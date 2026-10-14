# Dominance contracts and refusal on islands (notes, 2026-10-14)

Spec `specs/2026-10-14-dominance-contracts.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the "Amendments after
review" section supersedes the earlier text where they conflict). Follow-up to RESULTS "Stable sets on islands" and
DEFERRED 15 (the RS's held prediction, released 2026-10-14). §1 is written before any code of this experiment and
before any counted cell; §1.10 (code validation of §1 and the forced-island simulation) is appended after the code
exists and before any counted cell; §2 (costs) after that.

*Disclosure.* The numbers in §1.2–§1.6 come from four short static scripts (Markov chains on the 20 outcomes of R and
a deterministic two-slot replicator flow under the kernel's fitness map; no island dynamics, no seeds). They are
recomputed by `src/dominance_contracts.py` and checked in §1.10.

## 1. Design

### 1.1 The object as it will be implemented

The stable-sets machinery is unchanged (`src/stable_sets.py`: `dollar3`, three slot populations per island, fixed
roles, the n = 6 weak-arm grammar and the length prior L, ε = 0, Moran with w = 0.3, N = 100 per slot, I = 64,
mN ∈ {0, 1} role-preserving unweighted migration, generation = 3·I·N births, the 0.95 modal-play classifier).
`src/dominance_contracts.py` imports it and adds:

- **Genotype** of an individual of slot s: (program k, override o, refusal bit r, carried contract c). k is the
  canonical function (kept for classification); o ∈ {none} ∪ the slot's nine `dollar3` actions is the installed
  contract's demand (partner and demand), which overrides the program's play and is inherited; r ∈ {0, 1}; c ∈
  {none} ∪ the 27 contracts (menu G only). **Play class** = k if o = none, else the constant action o. Fitness is the
  stable-sets fitness of the play class (expected payoff, in dollars, against one uniform member of each other slot
  on the island); parent weight count · exp(w f), victim uniform, migrant parents from a uniform other island.
  Offspring copy the whole genotype.
- **Contract universe** (amendment 3): the 27 contracts κ = (S, d_S), S one of the three pairs, d_S ∈ {1/3, 1/2,
  2/3}² as constant `dollar3` actions in which the two members name each other. Three are infeasible (d sum > 1) and
  can never be proposed. There is no grand-coalition contract, so (2, 2, 2) can never be entered by a contract.
- **Contract events** happen at generation boundaries, after the generation's classification (cls[g] is the
  pre-event state): each island independently has an event with probability ν. Under menu F κ is uniform over the
  27; under menu G it is uniform over the island's menu (the set of distinct contracts carried by living
  individuals in any slot; an empty menu is logged and nothing happens).
- **Proposal** (amendment 2): with S = {i, j}, the contract's promised payoffs are x_i = d_i, x_j = d_j (the members
  name each other, so the complement's play is irrelevant to x and relation C coincides with M by construction:
  every complement action is a best reply and gives the same x). κ is proposed iff d_i > ȳ_i and d_j > ȳ_j, where
  ȳ_s is slot s's mean payoff at the current island state (= the modal outcome's payoff on homogeneous islands).
- **Guard** (the refusal gene): fires iff the island's modal realized outcome (argmax of the encounter distribution)
  is a member of V\* and x is not (x ∈ V\* iff d = (1/2, 1/2)). A carrier refuses an offer only when the guard fires;
  carrying r and refusing are logged separately.
- **Consent and installation** (amendment 1):
  - *none* (D cells, f_r = 0): installation of κ in a fraction β of each S slot.
  - *public* (R1-public, R2): one individual drawn per S slot (by counts); if the guard fires and either drawn
    individual carries r, the contract is blocked for the whole island; otherwise installation is r-blind.
  - *private* (R1-private): no veto; at the event every non-refusing individual of S is overwritten and refusers
    (carriers whose guard fires) keep their demand.
  - *blind* (the r-blind control; my reading under the amended design, fixed now): no veto and r-blind
    installation, so r is an inert marker seeded at 1/2: D1 plus a neutral marker, the martingale baseline for the
    bit.
  - **β = 1 (atomic)** overwrites every eligible individual of both S slots; **β < 1** overwrites round(βN)
    individuals per S slot drawn uniformly without replacement among the eligible. Installation keeps k, r and c and
    sets o; a later contract on S′ overwrites only S′ individuals; the complement keeps its phenotype, an old override
    included.
- **Menu G** (amendment 5): each founder carries a contract with probability p_c = 0.1, uniform over the 18
  contracts naming its slot. Carrying is a gene separate from the installed override; installation does not create
  carriers; carriers migrate with their lineages. Nothing new ever appears.
- **ν = 0** consumes no random numbers in the contract logic and must reproduce `stable_sets.kern` draw for draw
  (test); early stopping on closure is used only at ν = 0, since closure is not absorption once contracts act.
- **Seeds:** the stable-sets L seeds (`run_seed('L0' | 'L1', r)`), so every cell is paired with the baseline founder
  for founder; r and c are drawn after the founders from the same seeded generator. The baseline (ν = 0) is the
  stable-sets L cell rerun under the same seeds; bit-identical class sequences are a validation item.

### 1.2 The exact proposal generator on R

From an outcome y, the proposed contracts are those whose pair outcome x strictly improves both members of S on y.
Every proposed contract leads to a different x (multiplicity 1), so the generator is: with probability n(y)/27 move
to a uniformly chosen pair-dominator of y, otherwise stay (a null draw). Counts n(y):

| y | proposed contracts n(y) | where they lead |
|---|---|---|
| fair (3, 3, 0) | 2 | (4, 0, 2) via {1, 3}; (0, 4, 2) via {2, 3} (both unequal) |
| unequal (4, 2, 0) | 3 | (0, 3, 3) member; (0, 4, 2) unequal; (0, 3, 2) wasteful (all via {2, 3}, the low member and the excluded) |
| wasteful (3, 2, 0) | 4 | (4, 0, 2), (0, 4, 2) unequal; (0, 3, 3) member; (0, 3, 2) wasteful |
| wasteful (2, 2, 0) | 7 | own pair to (3, 3, 0); the other two pairs' (4|2) to the excluded's side, (3|3), (3|2) |
| (2, 2, 2) | 3 | each fair pair |
| (0, 0, 0) | 18 | every feasible pair outcome |

Hand facts: (2, 2, 2) and (0, 0, 0) are never entered and (2, 2)-type wasteful pairs are entered by nothing (no
outcome is improved for both members by moving to (2, 2)), so all three are transient; the recurrent class is the
fair, unequal and (3, 2)-type wasteful outcomes (15). **Every recurrent outsider has exactly one proposed contract
into V\*.** The jump chain on the recurrent class is the uniform-successor walk of the spec restricted to pair
dominators (identical, since the grand coalition dominates only (0, 0, 0)).

- **Uniform-successor walk** (the spec's anchor): stationary V\* = 4/17 = **0.235** (each member 0.078), unequal
  9/17 = 0.529, wasteful 4/17 = 0.235: reproduced. (The spec's "0.24 on the wasteful pairs" is this 0.235.)
- **The exact generator** weights each state by its holding time 27/n(y): fair 0.235/2, unequal 0.529/3, wasteful
  0.235/4, normalized: **V\* = 1/3 exactly** (each member 1/9), unequal 1/2, wasteful 1/6. This replaces 0.235 as the
  hand prediction for an island run by contracts alone. Second eigenvalue modulus 0.934: relaxation ≈ 15 draws,
  i.e. ≈ 150 generations at ν = 0.1 and ≈ 1,500 at ν = 0.01.

### 1.3 The walk with refusal at V\* (absorbing)

With V\* absorbing, the mean hitting time is **27 draws from every unequal and (3, 2)-type wasteful outcome** (one
contract in 27 leads in, and no other contract leaves the set of such outcomes for a different hitting rate), 19.3
from a (2, 2) pair, 9 from (2, 2, 2), 22.7 from (0, 0, 0): 270 generations at ν = 0.1. P(not absorbed by 2,000
generations) ≈ e^{−7.4} ≈ 6·10⁻⁴. **The contracts-only R2 chain hits V\* from every outcome** (R2's reachability
clause is a theorem of the generator).

### 1.4 Interleaving with relation-P drift (hand estimate)

- **mN = 0.** After the scramble the baseline islands are closed (no variation). A β = 1 contract leaves both S slots
  playing one constant each and the complement's composition unchanged and irrelevant (mutual naming), so nothing
  relation P can act on is created: **D1 at mN = 0 is the generator walk** started from the scramble's output.
  Early on the island payoffs are low (mostly disagreement among diverse constants), so nearly every feasible
  contract is proposed and the first jump is to a nearly uniform feasible pair outcome (fair 1/6, unequal 1/3,
  wasteful 1/2) within ~15 generations; after that the walk relaxes in ~150 generations. **Hand: D1 occupancy 1/3
  at every horizon ≥ 500, unequal 1/2, wasteful 1/6, disagreement and (2, 2, 2) ≈ 0.**
- **mN = 1.** A class-level chain with the contract rates plus the baseline's measured exits (fair → unequal at
  1/776 per generation; unequal 1/121, 0.65 to a member; wasteful 1/26, half to a member, assumed). At ν = 0 it gives
  0.807, against the measured 0.805 at 10,000 (a consistency check of the reduction). **ν = 0.1: 0.54** (0.47–0.59
  over the assumptions: no P exit from fair, all unequal P exits to members, no wasteful P exits); **ν = 0.01: 0.74**
  (0.68–0.89). Caveat: the P rates were measured on islands converging to a fair-pair consensus; under contracts the
  migrants are diverse constants and the rates may differ. Hand trigger split at ν = 0.1: entries into V\* per
  unequal-island-generation 0.0037 by contract and ≈ 0.0054 by P, i.e. **≈ 0.6 of entries into V\* not by a
  contract** if the baseline rates hold (this is RE 8's question).

### 1.5 Refusal (hand estimates)

- **R1-public.** Installation is r-blind and a veto protects the whole island, so the bit has the same fitness as its
  absence in every slot: a neutral martingale within islands, and between islands too (emigration is unweighted).
  At mN = 0 each slot's bit fixes by drift from 1/2 in ≈ 1.4N = 140 generations, mostly before the island's first
  guarded offer. With bits (r₁, r₂, r₃) fixed, member P_ij is absorbing iff r_k = 1 or r_i = r_j = 1 (its two exits
  are via {i, k} and {j, k}). Seven of the eight configurations have an absorbing member (all three when two or more
  slots refuse). Walk with these absorbing sets, started from the baseline's class mix: **occupancy 0.85 at 2,000,
  0.91 at 10,000, limit 0.917** at mN = 0. Support ⊆ V\* needs all 64 islands: ≈ 0.917⁶⁴ ≈ 0.004 of runs.
  mN = 1 (class chain with contract exits × (1 − 1/2)² = 0.25): **0.76**.
- **R1-private.** At a guarded event the refusers keep their demand and everyone else is overwritten. If the buyer
  slot (the member offered 4) refuses entirely, the outcome does not change (the excluded slot installs an offer, a
  neutral residue); if the buyer accepts and the excluded slot refuses, the buyer names a partner who does not name
  it back and the island crashes to disagreement (unless the excluded constant already offers). With bits fixed per
  slot, P_ij is absorbing iff r_i = r_j = 1 (four of eight configurations). **Occupancy 0.68 at 2,000, limit 0.72**
  at mN = 0. Selection on r acts only in slots polymorphic for r at a guarded event that goes through: a refuser in
  the buyer slot keeps 3 while the installed buyers rise to 4 once the excluded slot converts, and a refuser in the
  excluded slot keeps an unanswered constant (0 against 2): **myopically costly, but at mN = 0 most bits fix by drift
  before the first guarded event**, so the decline of the mean is small. At mN = 1 the bit stays polymorphic and pays
  the cost at every guarded event.
- **R1-blind.** = D1 (1/3) with an inert marker; mean change of the marker 0.
- **R2 (f_r = 1, public).** Contract exits from V\* are impossible; exits only by drift or migration. mN = 0:
  **occupancy ≈ 1 at 2,000** (minus islands still polymorphic). mN = 1 (class chain, contract exits 0): **0.89**
  (0.95 with a slower P exit). The escape hazard is the baseline's fair-pair P exit (1/776 per generation at N = 100).

### 1.6 Joint entry: the coordination threshold β\* for every dominating edge

Edges y → x for every realization of y by constants (the pair naming each other, the excluded slot at each of its
nine constants; (2, 2, 2) as (ALL, 1/3)³; (0, 0, 0) as (ALL, 2/3)³), with a fraction β of each S slot installed and the
complement fixed. Two thresholds under the kernel's fitness map:

- **β\*_static**: the smallest β at which both installed phenotypes are strictly fitter than their residents at
  installation;
- **β\*_flow**: the smallest β on the diagonal from which the deterministic selection flow of the two S slots
  (dp_s/dt = w p_s(1 − p_s)(f_inst − f_res), the large-N limit of the Moran step) reaches the contract's outcome.

| edge (y → x) | β\*_static | β\*_flow (max over the excluded constant; min) |
|---|---|---|
| fair → unequal (every member exit) | **0.76** (8 of 9; tie when the excluded already offers) | **0.40**; 0 |
| unequal → member | 0.67 (7 of 9) | 0.28; 0 |
| unequal → unequal | 0.51 | 0.25; 0 |
| unequal → wasteful | 0.67 | 0.32 (one realization never); 0 |
| (3, 2) wasteful → member | 0.67 | 0.28; 0 |
| (3, 2) wasteful → unequal (buyer the 3-member) | 0.76 | 0.40; 0 |
| (2, 2) wasteful → own fair pair | 0 | 0 |
| (2, 2, 2) → member | 0.41 | 0.40 |
| (0, 0, 0) → anything | ≈ 0 | ≈ 0 |

Mechanism of a member exit, say (3, 3, 0) → (4, 0, 2) via {1, 3}: the installed buyer (slot 1, now naming 3 at 2/3)
earns 4 only against installed partners (fraction p₃) and 0 otherwise, against the residents' sure 3; the installed
excluded slot earns 2·p₁ against its residents' 0. Statically the buyer needs 4β > 3 (β > 0.75); dynamically the
excluded slot's offerers grow at once and pull the buyer over from β ≈ 0.40. **The operative β\* is the flow
threshold** (it is what the kernel's selection does in the large-N limit): its maximum over member exits is 0.40, so
**D3′ runs at β = 0.5**, the smallest grid value above it. The static threshold 0.76 exceeds every grid value
(disclosed; RE 7's "β\* > 0.5" is true of β\*_static and false of β\*_flow, scored on both).

Hand bound at β = 0.25 for a member exit: the buyer's installed fraction starts at Δf = (4·0.25 − 3)/6 = −1/3 dollar,
w·Δf = −0.1 per generation, N·|s| ≈ 10, so it is lost within ~30 generations unless drift carries it, while the
excluded slot's offerers grow only to ≈ 0.3 and then drift neutrally. **Per attempt, joint fixation ≤ 0.05.** But the
offerers left in the excluded slot are a neutral residue that makes the next attempt easier (β\*_flow = 0 once the
excluded slot offers): at β = 0.25 member exits happen by repeated attempts, a drift-prepared contract. Entries into
members (β\*_flow ≤ 0.28) and exits from unequal pairs (≤ 0.25–0.32) sit at or near 0.25, so **at β = 0.25 the walk is
biased toward V\*: exits from members are suppressed more than entries into them.** The forced-island simulation
(§1.10) measures the per-attempt probabilities.

### 1.7 Menu G (hand)

About 10 carriers per slot (30 per island) give each contract ≈ 1.1 expected copies, so ≈ 18 of the 27 contracts are
on a typical island's menu at the start (≈ 0.67 coverage of each island's dominating moves). Carrying is neutral
(a hitchhiker on its lineage), so menus deplete by drift: at mN = 0 each unit ends monomorphic on one lineage, a
carrier with probability ≈ 0.1, so a closed island keeps ≈ 0.3 contracts. Contracts act in the first few hundred
generations (an early jump to a near-uniform feasible pair outcome, fair 1/6, then a few walk steps) and then the
island freezes. **Hand: D4 at mN = 0 ≈ 0.20–0.32** (the early jump distribution is less fair than the baseline's 0.28,
and a few steps relax it toward 1/3); at mN = 1 migration keeps the global carrier pool at 0.1 and menus partly
stocked, **0.55–0.75**.

### 1.8 Hand predictions per cell (horizon 2,000; occupancy = classified member islands, as the baseline's numbers)

| cell | mN = 0 | mN = 1 |
|---|---|---|
| baseline (ν = 0) | 0.281 (bit-identical) | 0.739 (bit-identical) |
| D1 (F, β = 1, ν = 0.1) | **0.33** (0.29–0.37); unequal 0.50, wasteful 0.17; support ⊆ V\* 0/40 | **0.54** (0.45–0.62); support ⊆ V\* ≤ 0.05 |
| D2 (ν = 0.01) | 0.30 (0.26–0.34) | 0.72 (0.62–0.80) |
| D3 (β = 0.25) | 0.45 (0.32–0.65), above baseline | 0.65 (0.5–0.8) |
| D3′ (β = 0.5) | 0.36 (0.30–0.45) | 0.55 (0.45–0.7) |
| D4 (G) | 0.26 (0.20–0.32) | 0.65 (0.55–0.75) |
| R1-public (f_r = 1/2) | 0.85 (0.10,000: 0.91); support ⊆ V\* ≤ 0.05 | 0.76 (0.65–0.85) |
| R1-private | 0.68 (0.55–0.75) | 0.55 (0.45–0.7); refusal falls |
| R1-blind | 0.33 | 0.54 |
| R2 (f_r = 1) | ≥ 0.97 | 0.89 (0.8–0.95) |
| N panel, D1 at N = 50 / 200 | 0.33 / 0.33 (N-free walk) | 0.56 / 0.50 |

### 1.9 Statistics (fixed now)

- **Member occupancy** = fraction of islands classified (≥ 0.95 of encounters) on a V\* member, as the baseline's
  0.281 / 0.739; member-mixed islands reported beside it. **Support ⊆ V\*** (amendment 4): every island classified on
  a member or member-mixed (other-mixed islands and every non-member class count against); the stable-sets
  definition (classified islands only) reported beside it for comparison with the baseline's 0.82.
- **The RS's prediction** (operationalization in the spec): D1, occupancy ≥ 0.8 at 2,000 and support ⊆ V\* in ≥ 0.5
  of runs, at mN = 0 or 1; each mN reported; also scored at 10,000 and, as a secondary reading, on every cell.
- **Settled sequence** per island: maximal runs of one classified outcome lasting ≥ 5 generations (mixed spells and
  shorter runs are the transitions between them). Transition A → B **trigger**: *contract* if an installation on the
  island falls between A's last generation and B's first; otherwise from the slots whose majority play class changed:
  *migration* if a new majority class entered the unit through a migrant, *contract residue* if it entered through an
  earlier installation, *drift* (neutral) or *strict P* (by the payoff difference at the crossing, as the stable-sets
  taxonomy) if it was seeded; *conditional* if no majority changed. Entries into V\* are decomposed by trigger.
- **Transition matrices** among the five classes (members, unequal, wasteful, grand, disagreement): contract-installed
  jumps (classified at the event and one generation after) and non-contract settled transitions, compared with the
  generator's jump chain.
- **Returns and cycles**: per island, the settled sequence's revisits (A … A) and minimal directed cycles; the class
  patterns of cycles, the net circulation n(A → B) − n(B → A) per class pair, and the fraction of member exits
  followed by a return to the same member versus another member.
- **Refusal trajectories**: per-slot bit frequency every 10 generations (island and run means), the change by run, and
  per island the correlation of the bit's frequency with the island's member time-share over the last 250
  generations; refused offers, carried-but-not-refusing counts, guarded events.
- **β < 1 fates**: per installation, joint fixation / one-sided / lost / superseded, by edge class.
- **Menu G**: menu size and coverage of the current dominating moves per island over time.
- **Escape hazards** (R2): exits from V\* per member-island-generation, by trigger.
- Efficiency (expected total payoff) reported, never used to select. Paired differences against the baseline use the
  shared founders.

### 1.10 Code validation of §1 and the forced-island simulation (before any counted cell)

Code: `src/dominance_contracts.py` (contracts, static walks and thresholds, the kernel `dkern`, run setup),
`src/dominance_contracts_run.py` (cells, analysis, static report, validation, forced assays),
`tests/test_dominance_contracts.py` (7 tests, passing). Static numbers in `runs/dominance-contracts-static.json`;
identity and costs in `runs/dominance-contracts-validate.json`; assays in `runs/dominance_contracts/assays.json`.

- **Erratum to §1.1:** the infeasible contracts are three *per pair*, nine of the 27 (d sum > 1); nothing else in §1
  depends on the count (the generator counts proposed contracts only, and an infeasible draw is a null draw).
- **§1.2–§1.3 reproduced by code:** the generator's stationary V\* mass is 1/3 exactly (unequal 1/2, wasteful 1/6),
  the uniform-successor walk's 4/17 = 0.2353, multiplicities all 1, |λ₂| = 0.934 (relaxation 15.2 draws), hitting
  time to V\* 27 draws from every unequal and (3, 2)-type wasteful outcome (19.3 from (2, 2), 9 from (2, 2, 2), 22.7
  from (0, 0, 0)), and the probability that the next member after a member exit is the same member is 0.319.
- **§1.6 reproduced:** β\*_flow over member exits max 0.399 (min 0), β\*_static 0.76 (one realization in nine a tie);
  the full per-edge table is in the static file.
- **Kernel identity (ν = 0):** `dkern` reproduces `stable_sets.kern` draw for draw (status, stop generation, final
  counts, every generation's island classes, migrant births) on the four stable-sets validation configurations, and
  the full-size baseline runs B0 / B1 reproduce the stored stable-sets L0 / L1 runs (stop generation, status, migrant
  births and every horizon's class labels) on the 6 runs checked per cell; every B run is compared again in the
  report.
- **Tests:** the proposal rule on hand cases (members left only for unequal pairs; 3, 4, 7, 3, 18 proposals from
  unequal, (3, 2), (2, 2), (2, 2, 2), (0, 0, 0)); every recurrent outsider has exactly one contract into V\*; β = 1
  jumps exactly to x on homogeneous islands (every installation, the proposal holding at the pre-event state); the
  public guard with universal refusal keeps every member island on its member (every proposal out of V\* refused)
  while the same islands without the bit leave; under private consent the refusers keep their demand and the rest
  are overwritten; installed overrides are inherited by births with their bits; menu G only shrinks without
  migration.
- **Forced-island simulation** (every dominating edge out of a P12 outcome, (2, 2, 2) and (0, 0, 0); the excluded
  slot at each of its nine constants, 25 islands each (200 for (2, 2, 2) and (0, 0, 0)); N = 100, mN = 0, Moran to
  closure; joint = the island ends on x):

| edge | β = 0.25 | 0.4 | 0.5 | 0.6 | 0.75 |
|---|---|---|---|---|---|
| member → unequal (two edges) | **0.12, 0.15** | 0.34, 0.30 | 0.53, 0.49 | 0.70, 0.74 | 0.93, 0.92 |
| unequal → member | 0.19, 0.23 | 0.52, 0.50 | 0.73, 0.75 | 0.86, 0.87 | 0.99, 0.96 |
| unequal → unequal | 0.29, 0.30 | 0.58, 0.59 | 0.78, 0.78 | 0.92 | 1.00 |
| unequal → wasteful | 0.21, 0.16 | 0.41, 0.39 | 0.61, 0.58 | 0.76, 0.69 | 0.90, 0.89 |
| (3, 2) → member | 0.24 | 0.54 | 0.71 | 0.88 | 0.95 |
| (2, 2) → own fair pair | 0.52 (0.43 other) | 0.76 | 0.90 | 0.92 | 0.95 |
| (2, 2, 2) → member | 0.09–0.12 | 0.46–0.51 | 0.73–0.77 | 0.90–0.94 | 0.99 |
| (0, 0, 0) → pair outcome | 0.47–0.59 | 0.80–0.90 | 0.89–0.96 | 0.96–1.00 | 0.99–1.00 |

  At β = 0.25 the member exit fixes in 0.13 of attempts averaged over the excluded constant, made of ≈ 0.07 when the
  excluded constant is neutral and ≈ 0.7 when it already offers the buyer 1/3 (the buyer alone completes the move).
  **This is above my hand bound (≤ 0.05) and above RE 7's and Gemini's ≤ 0.05, and below RE 7's falsifier (0.2).**
  Entries into members fix at 0.19–0.24 at β = 0.25: 1.6 times the exit rate, not ≥ 3 (S6's second clause fails).
  With these acceptance probabilities in the generator the class-level stationary mass on V\* is ≈ 0.45 (rates
  slowed ≈ 5×, relaxation ≈ 750 generations); D3′ (β = 0.5) accepts member exits half the time.

## 2. Costs and the scale guard

- One run at N = 100 to 10,000 generations: 0.4 s at mN = 0 (islands are monomorphic between contract events, so
  exact event skipping jumps generation to generation) and 26–30 s at mN = 1 (migrants keep units active); D3 and D4
  at mN = 1 to 2,000: 6–8 s. Type tables stay small (≈ 230 genotypes per slot without the bit, ≈ 370 with it, ≈ 530
  under menu G; no capacity overflow).
- **The whole design is about 1.5 CPU-hours: nothing is dropped.** The N panel's D1 and R1-public cells also run to
  10,000 (an addition over the spec's 2,000 for the panel, disclosed before the cells; R1-private stays at 2,000).
  At most 3 workers (the fully realizable social organization run holds 3 workers plus its driver).
- Forced assays: 18 s on 3 workers.
