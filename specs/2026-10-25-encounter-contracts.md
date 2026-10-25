# Spec: contracts that form in encounters, with the responders' programs answering, 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second
review]); to be run by a Sonnet subagent after "many islands" (queue 65) hands back, reusing its rare-migration machinery. The RS (2026-10-25):

> "Contracts spawn when they Pareto-improve in aggregate, across the population. Alternatively, they could spawn with
> some rate on individual sets of programs that stand to benefit … it clears up the picture on coalitional deviation,
> since it references an explicit opponent response. To spell it out, coalitions deviate when they Pareto-improve even
> after their opponents respond to their new action profile … This also only makes sense in the extensional wing,
> where response to behavior is defined."
>
> "This is why I want the deviations to be contracts. They trigger on the rare special cases where they apply and don't
> hinder the program elsewhere. [Holders] shouldn't need to [meet each other]. Can we instead only replace the actions
> at that point? In contract language, the responders get to see the contracts mutate into existence, and they only
> actually do if they earn their keep." Best-reply response: "sounds like the right control". Farsighted response: no.

Follows RESULTS "Dominance contracts and refusal on islands" (aggregate dominance test, atomic installation), "Deriving
immigrant rejection, Step 0" (the veto's churn), "Hooks follow-ups in the weak wing" and "Every behavioural predicate as
a hook key" (behaviour-keyed fills), "Churn among the fair pairs in the primary object", and DEFERRED 15 (the RS's
notion: credibility "given the opponent coalition gets a chance to respond"; the old gripe that the response was
either circular in f or a one-round best reply). REJECTED.md checked: the aggregate-test contracts are not rejected
but superseded as the contract layer for stable sets if this works; nothing re-opened.

## Why

The stored contract layer tests a contract against slot mean payoffs and installs it on whole slots at once. On a fair
island a single migrant's dent of about 1/N makes every fair contract pass, so the veto rotates islands by uniform
restarts that never anneal (the RE's reading of the kernel; the many-islands reference arm measures it). The RS's
version tests a contract on the specific programs of one encounter, against the responders' actual programs, and
installs it only on its signers, as an override that fires only in the situation where it was written.

## The object

Three-player majority division (`dollar3`), weak (simulation) arm, the L seeds, N = 100 per slot, w = 0.3, under the
many-islands order of limits: founding, an annealed mutation tail, then the rare-migration jump chain with islands
relaxed to their attractors (program-and-contract triples or persistent mixtures), and I → ∞ by the pool dynamics.
[After review] Genesis keeps running during relaxation (it is within-island dynamics). An island is settled when its
on-path behaviour (each slot's stage-2 action distribution against the island) has been fixed for 500 generations and
no contract formed in that window fires on path; silent contracts may keep drifting and are recorded, not waited on.
[After second review] The pool keeps each island's full program-and-contract state (never only its outcome class).
Settlement is checked against an independent no-migrant holdout of 5,000 further generations; any class change
during holdouts is a spontaneous (genesis-driven) transition, counted on the within-island clock and handled by the two-clock rule below,
never attributed to migration. [Addendum review, amended by the second addendum review] Spontaneous transitions
are kept as rates on the within-island clock (per generation, from fresh fixed-length windows, failures not
discarded); only a verified closed recurrent class is collapsed to one state, with migrant transitions averaged over
its invariant distribution of full configurations. An island with a positive spontaneous class-change rate that is
not such a class is reported as metastable and not crisp, never forced into a settled state. [Addendum C review]
The two clocks are not added: in the rare-migration limit genesis is within-island dynamics, so before each migrant
an island's state is its within-island limit (a closed class, or the invariant law of its recurrent class), and only
migrant transitions are jumps on the migration clock. Classes identified from holdouts are labelled provisional, with
an escape-rate upper bound propagated into the share dynamics. [Addendum S review] A positive escape rate dominates
migration as m → 0, so a class enters the limit only if its closure is certified from transition support (no
reachable configuration leaves it); otherwise the cell is reported at an explicit finite migration rate (mN = 10⁻³),
not as the limit. Hitting probabilities into recurrent classes are reported separately from their internal laws, and
invariant averaging is used only where mixing before the next migrant is shown.

**Contract.** A pair (situation key, fill) carried by an individual as an inherited gene. The key is the full
action profile of the encounter as the three programs play it without overrides (each slot's partner and demand); the
fill is the carrier's own action. In an encounter whose program-action profile equals the key, the carrier plays the
fill; elsewhere it plays its program. An individual carries at most one fill per key (a later contract with the same
key replaces the earlier one); the cap is fixed under Further checks.

**Evaluation of an encounter (one round of response).** Stage 1: every program plays as usual, giving the profile p.
Stage 2: carriers whose key equals p switch to their fills; every non-carrier re-evaluates its program against the
others' stage-2 actions (the responders see the contract). The stage-2 actions are the encounter's outcome. Further
reactions happen through later contracts, not inside an encounter. [After review] Stage-2 semantics in the weak arm:
a responder re-runs its program with every simulation atom of a carrier replaced by that carrier's fill (a behavioural
substitution: the responder sees what the carrier does at that point, not a re-simulation of the carrier's program
and contract), and with non-carrier opponents simulated as in stage 1. [Addendum review] The substitution applies at every
simulation depth (a nested simulation of a carrier also sees its fill); replay tests cover the two-responder case
(|S| = 1) under this rule. "Carrier" in stage 2 means an individual with
a contract whose key equals p; every other individual of the encounter is a responder. Fitness is the expected encounter payoff against
uniformly drawn members of the other two slots, as in the stable-sets kernel.

**Genesis.** At rate ν per island per generation (ν = 0.1 and 1 as a sensitivity) an encounter triple is drawn from the
island's slots, a coalition S is drawn uniformly from the seven nonempty subsets of the three slots, and a new action
profile for S is drawn uniformly among those that differ from S's stage-2 actions. The responders (the complement of
S) answer as in stage 2 against S's new actions. If every member of S earns strictly more in that encounter than
before (its stage-2 payoff with the contracts already in force), each member individual acquires the contract (key = p,
fill = its new action), replacing any fill it already had for p. [After review] During genesis, members of S play their
proposed actions; complement members that carry a contract for p play their fills (they are committed), and the other
complement members respond as in stage 2. Otherwise nothing happens.
Genesis applies to the encounter only, never to whole slots.

**Arms.**
- **R (the RS's):** behavioural response as above.
- **BR (control; a robust-acceptance diagnostic, [addendum S review]):** the uncommitted members of the complement play a pure best reply to S's new actions, holding
  committed complement members (those with a fill for p) fixed (two uncommitted members jointly: the pure Nash
  equilibria of the remaining game; one: its pure best replies); S's contract forms only if every member gains under
  every such reply (BR changes acceptance only; installed contracts then play under the arm's ordinary semantics, and
  replay reports the gains they actually deliver); rejections are logged separately by cause (no pure equilibrium, or some equilibrium failing the
  Pareto test). [After second review] If the remaining game has no pure equilibrium, the proposal is rejected (no
  vacuous acceptance); the notes check by enumeration how often this case arises.
- **H (the RS's synthesis, addendum 2026-10-25):** genesis may write only into hooks the signers' programs expose
  ("I'd propose mutations restrict to hooks exposed by the underlying programs"). The weak `dollar3` grammar gains the
  leaf `HOOK(t, a₀)` (tag t ∈ {0, 1}, default a₀ one of the nine actions), priced by the length prior like any node.
  A hook is exposed in an encounter if the program's evaluation reaches it there. A contract is a set of fills, one
  per member, each written into a hook that member reaches in the genesis encounter, keyed by the situation as in R
  and carrying the proposed action; a member that reaches no hook cannot join the coalition. Responders answer as in
  R. [Addendum S review] H restricts singleton deviations too (an unhooked member cannot deviate alone); every arm
  reports the share of genesis and of V\* conversions from |S| = 1 against |S| = 2, 3, so individual plasticity and
  coalitional contractibility are read separately. Arm R is the special case where every program is wrapped in one top-level hook at no prior cost, so H against R
  measures what restricting contracts to exposed points costs and buys. [Second addendum review] Matched cells on the
  same hooked grammar and prior: H (writes only into exposed hooks), H-top (the same population, writes also allowed
  at a free top-level wrapper) and H-inert (hooks present, no genesis), so access and prior are varied separately. [Addendum review] In H fills are indexed by
  (t, p), at most one per (t, p), the cap of 8 counting all entries; the fill is written into the hook whose
  evaluation produced the member's stage-1 action (the last hook reached on that path). [Addendum C review] `HOOK(t, a₀)` is a leaf, so a stage-1 path that ends at hook t
  fixes which fill can apply: in stage 2 a carrier whose stage-1 path ended at `HOOK(t, a₀)` and that holds a fill for
  (t, p) plays that fill, and responders substitute it for that carrier's simulation atoms.
- **0:** no contracts (the many-islands baseline).
- **B (diagnostic, [after review], amended after second review):** as R, but a successful genesis installs the
  contract on the signers and on exactly 9 further members of each signing slot with the same program (matched copies;
  cells where fewer exist report the realized count and the payoff changes the broadcast induces),
  to separate the responder test from dilution of a two-individual installation; unmatched broadcasting (random
  members) is reported separately as a secondary cell.
- **V (reference, if cheap):** the stored aggregate test with the veto, under the same order of limits.

## Outputs

- Genesis: contracts formed per island-generation, by coalition size and by the island's outcome class; the share that
  fire on path afterwards; carried but silent contracts (the reservoir) over time.
- Island level, under the rare-migration jump chain: the post-anneal and settled shares of outcome classes; the
  fair-to-fair conversion rates κ (to the donor's pair) and α (to the third pair) per migrant, the rates out of
  dominated classes into V\*, and the I → ∞ share dynamics from three starts (post-anneal, tilted toward one fair pair,
  tilted toward one dominated class), with island switching rates at the last checkpoint.
- [After review] For every firing contract that moves an island: whether it was newly formed in that migrant's window
  or a reservoir relic formed earlier and drifted while silent.
- Whether a settled island has any improving contract left (contract-stable) and, if so, which coalition, by an
  exhaustive oracle over every encounter triple type, coalition and action profile on the settled state ([after
  second review]; random genesis failing to find one is not contract-stability).
- For the RS: where "every island efficient and all three fair pairs present" holds or fails under R, against 0 and BR.

## Predictions (the RE's; falsifiers in brackets)

1. *Settled islands go quiet.* On settled fair-pair islands without migrants, in fresh fixed windows after settlement, genesis forms no contract that fires on
   path [a settled fair island keeps forming firing contracts at a rate above 10⁻³ per island-generation].
   *Counter-prediction (gemini-4-argon), registered:* monomorphic settled fair islands go quiet, but polymorphic ones
   keep forming firing contracts above 10⁻³ through drift in silent and committed fills.
2. *Contracts clear some dominated islands.* Under R the settled V\* share is at least 0.15 above arm 0's at the same
   checkpoint [less than 0.05 above].
   *Counter-prediction (gpt-6.1-sol), registered:* gains are heterogeneous with no robust 0.15 uplift across ν and N;
   installations with a positive expected-fitness change, not acceptance counts, predict conversions.
3. *Coordination barrier.* Contracts whose fill needs the other member slot to change as well rarely spread from their
   two signers, because other members of the partner slot do not carry the fill: of contracts formed on dominated
   islands, those that fix in both member slots are under 0.1, and conversions run mostly through partner slots whose
   programs already accept the new action (readers) [at least 0.3 fix in both].
4. *Third-pair moves exist.* Under R, α > 0 with an interval excluding 0 on fair islands [α's interval includes 0].
   [Second addendum review] Exposure budget: at least 2·10⁴ migrant events per arm on fair islands; α is reported
   absent at this resolution if its 95% upper bound is below 10⁻³ per migrant, and unresolved otherwise.
   *Counter-prediction (gemini-4-argon), registered:* a third-pair contract needs slots 1 and 3 to change together,
   its two signers are a 1/N minority each, and it dies by drift, so α's interval includes 0 or α < 10⁻³.
5. *R and BR differ where programs do not best-reply.* The two arms' settled V\* shares differ by at least 0.05, and the
   difference traces to responders whose program reply is not a best reply [within 0.05 everywhere].
   *Counter-prediction (gpt-6.1-sol), registered:* encounter-level response differences can coexist with small
   aggregate differences, and BR's worst-equilibrium rule can create differences by another route.
6. *Coverage.* In the I → ∞ dynamics under R, all three fair pairs keep positive shares from every start [some pair's
   share → 0]. *Counter-prediction (gpt-6.1-sol), registered:* symmetric nonlinear pool dynamics can have unstable
   interior coexistence and attracting boundaries, so coverage depends on invasion rates and the start.

## Addendum (the RS's synthesis): arm H

Outputs for H: the prior mass of hooked programs at n ≤ 6 and how many hooks they carry; the share of genesis
attempts blocked because a needed member reaches no hook; settled shares, κ and α against R and 0; whether hooked
programs gain or lose share over time (contractibility selected for or against); and where on the programs' paths the
fills that move islands sit (a top-level hook or a hook inside a branch).

7. *H lies between 0 and R.* H's settled V\* share is between arm 0's and arm R's, and hooked programs gain share on
   islands where contracts fire [H outside the interval spanned by 0 and R, or hooked programs lose share]. Restriction
   and dilution are read separately: H against H-top is the cost of restricting writes, H-inert against 0 the cost of
   hook syntax in the prior.
   *Counter-prediction (gpt-6.1-sol), registered:* restricting hooks changes the reachable attractors and can expose
   holders to exploitation, so H need not lie between them and hooked programs need not gain.

## Addendum 2 (the RS, 2026-10-25): peer-to-peer spread

The RS: "can contracts still spread peer to peer? I don't really see a need nor a suitable mechanism for it but it's in
keeping with the island model." The RE's proposal: copying as a proposal source, not a transfer. In arm **C**, a
fraction q = 0.5 of genesis proposals are drawn from contracts already carried on the island instead of uniformly.
[Addendum C review, amended] Every installed contract keeps its bundle identity (key p, the signing coalition and
each member's fill), inherited with the fills; a copied proposal is an actual surviving bundle drawn by the frequency
of its carriers, offered to the same coalition of slots, and made in an encounter drawn among the island's triples whose situation is
p (by their frequency; if none exists, the copied proposal is logged as unmatched and no encounter is wasted), and it is accepted by exactly the same test (every
member gains after the responders answer). Copying thus changes which deviations are tried, never which survive the
test, so no contract exists that has not earned its keep in the encounter where it was written; migrants carry their
fills between islands as genes already. (Part W's free copying spread fills without a test and leaked disabled fills
back; this avoids both.) Report C against R: genesis attempts and acceptances by source (uniform or copied), settled
shares, κ and α. A recombination variant (one fill per slot drawn by frequency, across bundles) is a separate,
secondary cell if cheap.

## Addendum 3 (the RS, 2026-10-25): the Pareto clause as selection

The RS: "Eventually I'm hoping we can migrate the Pareto improvement clause from a precondition on mutation to an
observed fitness constraint. If the mutation doesn't serve me I'll die and won't pass it to my offspring, losing the
coalition my slot." Arm **S** is R with the acceptance test removed: genesis installs every proposed contract on its
signers (same proposal law, same keys, same two-stage evaluation), and selection alone decides what survives. Each
member's fill is inherited in its own slot, so a bundle is not co-transmitted; its halves are selected separately.
Since S installs every proposal, its genesis rate is set so that installations per island-generation match R's
proposals (not R's acceptances), and a matched S-low cell installs at R's acceptance rate, so S against R separates
removing the filter from changing the input rate.

Outputs for S: survival and fixation of each half and of whole bundles (both halves present above 0.5 in their slots),
split by whether a half is silent (its key not on path) or firing while it rises; settled shares, κ and α against R
and 0; the share of S's conversions that pass R's test at the moment they fire (selection rediscovering the clause).

8. *Selection keeps only what each member wants alone.* [Revised before the run after both reviews of addendum 3, which
   showed the RE's silent-halves mechanism wrong: keys use override-free play, so on a resident island both halves fire
   at once.] Under S, conversions come from fills that raise their holder's fitness without the other signer present
   (singleton-compatible, or the partner slot's programs already accommodate): at least 0.8 of S's conversions are of
   this kind, and conversions that need two signers to coordinate are at least 5× rarer per migrant than under R
   [fewer than 0.5 of this kind, or coordinated conversions within 2× of R]. The original prediction (silent halves
   drifting up neutrally) is kept in the predictions file as withdrawn, with the reviewers' counter-predictions.

## [After second review] Further checks

- A small N panel (N = 50, 100, 200) for genesis and settled shares, at fixed ν per island and at fixed proposal
  exposure per individual (ν ∝ N), reported separately.
- Replay tests: an accepted genesis, replayed after installation, reproduces its predicted outcome, including
  complement contracts, replacements, two responders and the grand coalition.
- A contract cap of 8 per individual with least-recently-fired eviction, fixed in advance, with a cap-16 sensitivity
  cell; eviction is part of the genesis test and of the oracle, and displaced entries are logged with their
  consequences (the locality claim holds only up to eviction).
- [Addendum S review] An execution-consistent BR cell: uncommitted responders actually play the selected equilibrium
  (the worst for S among pure equilibria, ties by a fixed order), so acceptance and execution agree.
- Firing hazards also from fixed-age, unselected post-anneal snapshots, with time to settlement and the never-settled
  mass.
- Efficiency reported three ways: V\* membership of the modal outcome, encounter efficiency, and whether the island's
  expected slot-payoff vector is Pareto-dominated.
- Configuration snapshots and replays include eviction order and bundle provenance; for each sampled configuration,
  paired migrant and no-migrant branches with common random numbers give the migrant's incremental conversion
  probability.
- Establishment stratified by whether each signer's fill raises its fitness without the other signer present.
- On settled V\* islands, the share whose fair play depends on stage-2 overrides on path against those where the
  programs play fair in stage 1 and contracts were only a transient bridge.
- Replay of every accepted installation across all encounter types it affects, with the signers' expected-fitness
  change, not only the founding encounter.
- A no-response arm NR (the coalition is judged against the responders' stage-1 actions), to separate the response
  from encounter-conditioned acceptance; not cuttable.
- [Addendum C review] BR against R at proposal level: for each proposal, the actual reply, whether it is a best reply,
  the worst-equilibrium verdict and the installed payoffs, so non-best-reply behaviour and equilibrium conservatism are
  separated.
- Establishment and conversion stratified by the sign of the signers' expected-fitness change at installation (not
  only founding-encounter gains).
- α's uncertainty clustered by source island and configuration, not treating migrant events as independent.
- Conclusions are finite-N (50–200) and labelled so.
- Matched no-migrant windows beside migrant windows, and contract-lineage attribution, so that third-pair moves are
  not spontaneous genesis events that happened to coincide with a migrant.

## Required outputs

- `src/encounter_contracts.py` (+ runner, report), importing the many-islands and stable-sets code; no existing file
  edited.
- `tests/test_encounter_contracts.py`: the two-stage evaluation on hand-built triples (a contract that fires, one that
  does not, a responder that reacts); genesis by hand on a mismatched-migrant encounter and on an unequal island; BR on
  a hand-built case where it differs from R; with ν = 0 the arm reproduces arm 0 draw for draw.
- `notes/encounter-contracts.md` (§1 before code: worked genesis examples on fair, unequal, wasteful and disagreement
  islands, with the response; the coordination-barrier argument; §2 deviations).
- `predictions/2026-10-25-encounter-contracts.md` before any counted cell, with the RS's messages first.
- `runs/encounter-contracts.md` and `.json`, `runs/encounter_contracts/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** At most 3 workers, 2 while another subagent is alive; one job per process; no
`multiprocessing.Pool`; one background wait per batch that exits at completion and fires if the log stops changing for
2 hours; never poll periodically. Cut order (disclose): V, the recombination cell, S-low, C, the cap-16 cell, unmatched B, the N panel at N = 200; keep the tilted starts and ν = 1 (genesis against a short-lived migrant at ν = 0.1 is
rare, so ν = 1 separates "cannot form" from "was not sampled"; also report migrant-encounter genesis conditionally).
