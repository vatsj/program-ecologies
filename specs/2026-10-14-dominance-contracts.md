# Spec: dominance contracts and refusal on islands: do contracts that deviate to dominating outcomes recover the vNM stable set?, 2026-10-14

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Stable sets on islands" and DEFERRED 15 (the held test, released by the RS on 2026-10-14).
REJECTED.md checked: no entry is re-opened (the stable-sets RE 4 entry concerns flips under single-slot dynamics;
this arm adds two-slot moves).

## The RS's prediction (verbatim, registered)

> My more pointed prediction is that contracts deviating to dominating actions will recover the vNM stable set.

**Operationalization (the RE's, stated before the run; the RS may amend):** "recover" = member occupancy (fraction
of islands whose modal play is one of the three 50–50 pairs V\*) ≥ 0.8 at the horizon *and* island support ⊆ V\* in
≥ 0.5 of runs, in the main contract cell (D1 below) at mN = 0 or mN = 1. The baseline without contracts is 0.28
(mN = 0) and 0.74 (mN = 1, N = 100), with support ⊆ V\* in 0/40 and 0.82 of runs.

## Why

The stable-sets run found that the ecology does not respect the vNM set: its moves are single-slot (relation P),
which neither majority dominance (M) nor commitment dominance (C, equal to M on R) contains. The RS's prediction is
that giving programs the two-slot move, a contract by a winning pair to jointly switch to an outcome both strictly
prefer, recovers the set. The RE bets against it: stable sets are not closed under dominance (every member is
dominated by two outsiders, e.g. (4, 0, 2) ≻ (3, 3, 0) via {1, 3}), so a dominance-following dynamic cycles through
the set. **Static anchor (computed by the RE, `R` = the 20 realizable outcomes of `dollar3`):** the random walk that
takes a uniformly drawn M-dominating move at each step has stationary mass 0.235 on V\* (each member 0.078), 0.53 on
the six unequal pairs and 0.24 on the wasteful pairs; members are dominated only by unequal pairs, so V\* is
recovered only if something blocks those two moves. That something is **refusal**: a member of the current pair
declining an offer that leaves V\*. Refusal is myopically deleterious (the refuser forgoes 4/6 for 3/6) and cannot
bind the excluded player, so its survival is the real question.

## Design

**Game and baseline dynamics.** Exactly the stable-sets machinery (`src/stable_sets.py`: `dollar3`, three slot
populations, fixed roles, the n = 6 weak-arm grammar and length prior L, ε = 0, Moran with W = 0.3, N = 100 per slot,
I = 64, mN ∈ {0, 1} role-preserving unweighted migration, 40 runs per cell, horizons 500 / 1,000 / 2,000 and 10,000
on unresolved runs, the 0.95 modal-play classifier). New code imports it and does not edit it.

**Contract genes.** A contract κ = (S, a_S) names a winning pair S and a demand pair a_S on the grid (as constant
`dollar3` actions). It is a gene in the RS's sense: installed in an individual, it overrides that individual's
demand and is inherited. **Contract events:** at rate ν per island per generation (ν ∈ {0.01, 0.1}; one generation
= N birth–death events per slot), a contract is drawn from the island's contract menu and evaluated at the current
island state: the status quo y is the island's modal realized outcome, and x is the outcome when the S slots play
a_S and the complement keeps its modal program (relation M), with the complement's credible best reply as a
reported variant (relation C, outcome-equal to M on R by Lemma I). The contract is *proposed* iff every member of S
is strictly better at x than at y. **Consent:** for each slot in S one individual is drawn; the contract proceeds iff
neither drawn individual carries the refusal gene and refuses (below). **Installation:** a fraction β of each S slot
(drawn among non-refusers) gets κ installed; β = 1 is the atomic contract (the island jumps to x: the dynamics
contain relation M exactly), β = 0.25 is joint entry that Moran must then carry to fixation (the forced-entry
fraction of the stable-sets run). Installed individuals keep their other genes (refusal bit, program identity for
classification) and pass κ on.

**Menus.** (F) *full menu:* every contract on the grid is available on every island (the RS's mechanism in its
strongest form: every dominating move is eventually offered). (G) *seeded genes, ε = 0:* each founder carries a
contract with probability p_c = 0.1, drawn uniformly from the contracts naming its slot; the island's menu is the set
of contracts carried by living individuals, and contracts migrate with their carriers; nothing new ever appears.

**The refusal gene.** A heritable bit r, neutral on-path. A carrier drawn for consent refuses a contract iff the
status quo is a member of V\* and x is not (the guard that makes V\* absorbing under M). Seeded at frequency
f_r ∈ {0, 0.5, 1}: f_r = 1 is the positive control (V\* absorbing by construction once reached, so it measures
reachability), f_r = 0.5 measures selection on the gene; its frequency trajectory per slot is logged, with the
installation-into-non-refusers rule making refusal myopically costly by construction (state this in the notes; a
variant with installation blind to r is the control that isolates the consent effect).

**Cells** (main = D1; R1 split into R1-public and R1-private by amendment 1). D1: F, β = 1, ν = 0.1, f_r = 0, mN ∈ {0, 1}. D2: as D1 with ν = 0.01. D3: F, β = 0.25,
ν = 0.1, f_r = 0. D4: G, β = 1, ν = 0.1, f_r = 0. R1: D1 with f_r = 0.5 (selection on refusal), and with the
r-blind installation control. R2: D1 with f_r = 1 (positive control). N panel: D1 and R1 at N ∈ {50, 200}, 20 runs.
The no-contract baseline is the stable-sets L cell, rerun under the same seeds for pairing (bit-identical check).

**Static computations before any cell** (notes §1): the uniform-M walk above (reproduce 0.235); the walk with
refusal at V\* (absorbing; mean hitting time from each outsider); the walk interleaved with relation-P drift at the
ratio implied by ν and the measured stable-sets residence times (fair 776, unequal 121 generations at N = 100), giving
a hand prediction for D1's occupancy; the fixation probability of a β = 0.25 jointly installed dominating contract
under the kernel's fitness map (hand bound and simulation on forced islands).

**Statistics.** Member occupancy and coverage per cell at each horizon; support ⊆ V\* by run; the class
distribution (members, unequal, wasteful, grand, disagreement); per island the sequence of contract events (proposed,
refused, installed, fixed or lost under β < 1) and the trigger of every class change (contract vs relation-P drift
vs migration); refusal-gene frequency trajectories with run-level uncertainty and the r-blind control; for D4 the
menu size per island over time; paired-seed differences against the baseline. Efficiency is reported, never used to
select.

**Scale guard.** The sog fully realizable run is still using 3 workers (`sog_full_run`); this run uses ≤ 3 workers
and checks the sibling pids before any multi-worker step. Report the kernel's cost with contract events before the
cells; if the full design exceeds ~6 hours on 3 workers, drop D2 and the N panel first, disclosed.

## Required outputs

`src/dominance_contracts.py` (+ `_run.py`, `_report.py`, importing `stable_sets`), `tests/test_dominance_contracts.py`
(proposal rule on hand cases; refusal guard; β = 1 jumps exactly to x; installed genes are inherited; ν = 0 reproduces
the stable-sets kernel draw for draw; the menu G only shrinks without migration), `notes/dominance-contracts.md` (§1
static computations and hand predictions before any cell, §2 costs), `runs/dominance-contracts.md` and `.json`, a
predictions file from this spec with the RS's prediction first, committed before any counted cell, and the usual
hand-back (draft RESULTS, REJECTED, THEORY §3 / DEFERRED 15 edits, NOTATION, ≤ 5 lines, branch, commits).

## RE predictions (with falsifiers)

1. **The RS's prediction fails in D1:** with every dominating move available and no refusal, islands cycle, and
   member occupancy at the horizon is within 0.1 of the time-weighted walk of §1 (my bet 0.2–0.4 at mN = 0); support
   ⊆ V\* in ≤ 0.2 of runs. *Falsifier:* occupancy ≥ 0.6 in D1 at either mN.
2. **Contracts make things worse for the set at mN = 1:** D1's occupancy at mN = 1 is below the baseline's 0.74,
   because contracts break the fair-pair consensus that drift and migration built. *Falsifier:* D1 at mN = 1 ≥ 0.74.
3. **The rate does not save it:** D2 (ν = 0.01) lies between the baseline and D1. *Falsifier:* D2 outside that
   interval by more than run-level uncertainty.
4. **Refusal is lost where it is private and drifts where it is public** [revised after review: under slot-wide
   consent the refuser's cost falls on its whole slot]: in R1-private the refusal frequency falls (mean below 0.5 by
   the horizon in ≥ 0.8 of runs at mN = 0); in R1-public its frequency is a neutral martingale within islands (mean
   change within run-level uncertainty of 0), and island occupancy of V\* rises with the island's refusal frequency.
   *Falsifier:* refusal rising in ≥ 0.5 of R1-private runs, or a systematic trend in R1-public.
5. **Universal refusal makes V\* reachable and nearly absorbing** [revised after review: the guard blocks M exits,
   not drift or migration]: the contracts-only R2 chain hits V\* from every outcome; the full-kernel R2 reaches
   occupancy ≥ 0.9 and support ⊆ V\* in ≥ 0.8 of runs. *Falsifier:* occupancy ≤ 0.7, read through the measured
   escape hazards (drift and migration leakage), not as unreachability.
6. **Seeded contracts at ε = 0 are close to the baseline:** D4's occupancy within 0.1 of the baseline at mN = 0,
   because menus are sparse and the needed dominating contract is rarely present. *Falsifier:* a difference ≥ 0.2.
7. ~~Joint entry mostly fixes at β = 0.25~~ [withdrawn after review by gemini-4-argon before any run: an installed
   slot-1 demand meets an installed partner only a quarter of the time and otherwise disagrees, so it earns ≈ 1/6
   against the residents' 3/6]. **Revised:** joint entry has a coordination threshold β\* > 0.5 for every dominating
   contract out of a member (computed in §1), fixation at β = 0.25 is ≤ 0.05, and D3 is within run-level uncertainty
   of the baseline. *Falsifier:* fixation ≥ 0.2 at β = 0.25. **Gemini's counter-prediction (registered):** fixation
   < 0.05 and D3 identical to the baseline; it and the revised RE 7 now agree, so the informative cell is D3′ at
   β just above β\*.

8. **Gemini's alternative, registered as a test:** if D1 at mN = 1 beats D1 at mN = 0, it is because contracts break
   wasteful and disagreement traps into unequal pairs that drift and migration then carry into V\*, not because
   contracts select V\*. Decided by the trigger decomposition of entries into V\* (contract vs drift vs migration).

Uncertain: 2 (contracts may also accelerate consensus), 4 (the cost is paid only at contract events, so drift may
dominate at ν = 0.1), 6.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Installation mechanics.** Installation is in place: the individual keeps its program identity and refusal bit,
   and its demand (partner choice and demand, a `dollar3` action naming the coalition partner) is overwritten
   permanently and inherited. A later contract on S′ overwrites the S′ individuals only; the complement keeps
   whatever phenotype it has, an old contract included, and x is evaluated against that actual phenotype.
   **β = 1 (atomic) overwrites every individual of both S slots regardless of r**, so it contains relation M exactly
   on homogeneous islands. Two refusal variants replace the single R1: **R1-public** (consent by one drawn
   individual per S slot; a drawn refuser blocks the whole contract; installation r-blind), where refusal is a
   slot-level public good, and **R1-private** (no veto; at the event every non-refuser in S is overwritten and
   refusers keep their demand), where refusal is a private cost through the coordination penalty. Carrying r and
   refusing *this* offer are logged separately (the guard refuses only exits from V\*).
2. **Evaluation on polymorphic islands.** A contract is proposed iff every member of S is strictly better at x than
   at y, computed by expected payoff of the installed phenotype against the island's actual slot populations (equal
   to the modal-outcome rule on homogeneous islands). Realized payoff changes and departures from the predicted x are
   recorded. The exact-M validation (β = 1 jumps exactly to x) is restricted to homogeneous islands.
3. **The static walk matches the proposal kernel.** §1 builds the exact generator: a uniform draw from the menu's 27
   contracts (3 pairs × 9 demand pairs on `dollar3`'s actions), null draws counted, multiplicities kept; its
   stationary V\* mass replaces the 0.235 uniform-successor anchor as the hand prediction (both reported). The
   interleaving with relation-P drift is a hand estimate only, since contracts change the genotype composition P acts
   on.
4. **Estimands.** Primary horizon 2,000 generations for every run of every cell; D1, R1-public and R2 also run every
   run to 10,000 (no outcome-dependent extension). *Support* = the set of classified islands' modal classes; mixed
   (unclassified) islands are reported and count against support ⊆ V\*. Recovery in either mN counts for the RS's
   prediction, and each is reported.
5. **Menu G.** The island menu is the union of contracts carried by living individuals in any slot; the contract
   universe is the 27 `dollar3` contracts, p_c = 0.1 (≈ 30 copies per island at N = 100); the initial coverage of
   each island's dominating moves is reported, and the trajectory of menu size and coverage (depletion).
6. **D3 threshold.** §1 computes the coordination threshold β\* for every dominating edge under the kernel's fitness
   map; D3 runs at β = 0.25 and **D3′** at the smallest grid β ∈ {0.5, 0.6, 0.75} above the largest β\* for exits
   from members.
7. **Added assays and statistics.** Forced assays for every dominating edge on homogeneous islands (immediate
   payoffs, joint fixation, one-sided fixation, reversal); the empirical transition matrix among the five outcome
   classes for contract events and for non-contract changes, compared with the static walk; return sequences and
   recurrent directed cycles per island, to tell cycling from independent turnover; the trigger decomposition of
   entries into V\*.
8. **Scale guard order.** Keep the N panel; drop D2 first, then D3′, disclosed.

Review notes kept for the RE: Gemini's farsighted-refusal idea (a source-reading program proving that accepting κ
leads to its own exclusion, deriving the guard endogenously) is a candidate follow-up in the modal or realizable arm.
