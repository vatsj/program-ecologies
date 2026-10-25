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
during holdouts is a spontaneous (genesis-driven) transition, counted and included in the dynamics explicitly,
never attributed to migration. [Addendum review, amended by the second addendum review] Spontaneous transitions
are kept as rates on the within-island clock (per generation, from fresh fixed-length windows, failures not
discarded); only a verified closed recurrent class is collapsed to one state, with migrant transitions averaged over
its invariant distribution of full configurations. An island with a positive spontaneous class-change rate that is
not such a class is reported as metastable and not crisp, never forced into a settled state.

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
- **BR (control):** the uncommitted members of the complement play a pure best reply to S's new actions, holding
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
  R. Arm R is the special case where every program is wrapped in one top-level hook at no prior cost, so H against R
  measures what restricting contracts to exposed points costs and buys. [Second addendum review] Matched cells on the
  same hooked grammar and prior: H (writes only into exposed hooks), H-top (the same population, writes also allowed
  at a free top-level wrapper) and H-inert (hooks present, no genesis), so access and prior are varied separately. [Addendum review] In H fills are indexed by
  (t, p), at most one per (t, p), the cap of 8 counting all entries; the fill is written into the hook whose
  evaluation produced the member's stage-1 action (the last hook reached on that path).
- **0:** no contracts (the many-islands baseline).
- **B (diagnostic, [after review], amended after second review):** as R, but a successful genesis installs the
  contract on the signers and on up to 9 further members of each signing slot with the same program (matched copies),
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
2. *Contracts clear some dominated islands.* Under R the settled V\* share is at least 0.15 above arm 0's at the same
   checkpoint [less than 0.05 above].
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
   islands where contracts fire [H outside the interval spanned by 0 and R, or hooked programs lose share].
   *Counter-prediction (gpt-6.1-sol), registered:* restricting hooks changes the reachable attractors and can expose
   holders to exploitation, so H need not lie between them and hooked programs need not gain.

## Addendum 2 (the RS, 2026-10-25): peer-to-peer spread

The RS: "can contracts still spread peer to peer? I don't really see a need nor a suitable mechanism for it but it's in
keeping with the island model." The RE's proposal: copying as a proposal source, not a transfer. In arm **C**, a
fraction q = 0.5 of genesis proposals are drawn from contracts already carried on the island (a whole contract: every
member's fill, keyed as written) instead of uniformly; such a proposal is offered to the coalition of the current
encounter only when its key matches the encounter's situation, and it is accepted by exactly the same test (every
member gains after the responders answer). Copying thus changes which deviations are tried, never which survive the
test, so no contract exists that has not earned its keep in the encounter where it was written; migrants carry their
fills between islands as genes already. (Part W's free copying spread fills without a test and leaked disabled fills
back; this avoids both.) Report C against R: genesis attempts and acceptances by source (uniform or copied), settled
shares, κ and α.

## [After second review] Further checks

- A small N panel (N = 50, 100, 200) for genesis and settled shares, at fixed ν per island and at fixed proposal
  exposure per individual (ν ∝ N), reported separately.
- Replay tests: an accepted genesis, replayed after installation, reproduces its predicted outcome, including
  complement contracts, replacements, two responders and the grand coalition.
- A contract cap of 8 per individual with least-recently-fired eviction, fixed in advance, with a cap-16 sensitivity
  cell; eviction is part of the genesis test and of the oracle, and displaced entries are logged with their
  consequences (the locality claim holds only up to eviction).
- Replay of every accepted installation across all encounter types it affects, with the signers' expected-fitness
  change, not only the founding encounter.
- A no-response arm NR (the coalition is judged against the responders' stage-1 actions), to separate the response
  from encounter-conditioned acceptance.
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
2 hours; never poll periodically. Cut order (disclose): V, C, NR, the cap-16 cell, unmatched B, the N panel at N = 200; keep the tilted starts and ν = 1 (genesis against a short-lived migrant at ν = 0.1 is
rare, so ν = 1 separates "cannot form" from "was not sampled"; also report migrant-encounter genesis conditionally).
