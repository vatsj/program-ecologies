# Spec: hooks follow-ups in the weakly extensional wing: parochial vs open contracts (PD) and union contracts judged against the boss's response (union game), 2026-10-21

Status: draft by the RE; to be reviewed sequentially by gemini-4-argon then gpt-6.1-sol (`--mode amended`); to be run by
a Sonnet subagent. Run under the RS's 24-hour autonomy window (2026-10-21). Follow-up to RESULTS "Hooks in the weakly
extensional wing" and DEFERRED 12 and 15. REJECTED.md checked: nothing re-opened.

## Why

Part W found that maximal hooks are not neutral: in the PD, pair contracts accepted when (D, D) → (C, C) between two
default defectors, keyed on each other's *lineage*, act as a tag by descent; the resulting kin networks displace the
provers (universal-open 1.00 → 0.00; strict contract ablation 0.675). In the union game, history-keyed worker grudges
are tested and select the ¼ wage on 0.85 of islands, never ½, and boss–worker contracts are accepted only as myopic
Pareto improvements. Two questions follow. (1) Is the PD collapse caused by *parochial keys* (lineage) rather than by
hooks or contracts as such? If contracts and history are keyed on the partner's behaviour instead, a contract becomes a
legible conditional promise to a behaviour class rather than to a family. (2) Does a joint worker demand reach the fair
wage once contracts are judged against the boss's best response (the RS's leader-value notion, DEFERRED 15) rather than
myopically?

## Design

**Machinery.** `src/hooks_w*.py` and `src/hooks_w_sog*.py` (import only; a new module may copy and extend them), the
Part W objects and validation (the PD at (100, 64), mN = 1, ε = 0, 40 runs; fission–fusion 32 × 100 merged at 200;
the union game at (30, 16), mN = 1, 40 runs), provenance-preserving copies throughout (IMPLEMENTATION), founders and
fill draws coupled across cells.

**Part 1, PD: parochial vs open keys.**
- *Lineage maximal* (Part W's maximal, rerun as the paired reference).
- *Open maximal:* every lineage key replaced by the partner's behaviour class (the three PA boxes), for history writes,
  copies and contracts; behaviour-keyed contracts are joint fills "cooperate with class β" where β is the partner's class.
- *Open contracts only:* lineage-keyed history writes kept, contracts behaviour-keyed.
- *Open history only:* contracts lineage-keyed, history behaviour-keyed.
- References: inert, baseline (stored), and Part W's strict no-contract.
Also fission–fusion for lineage maximal and open maximal.

**Part 2, union game: union contracts.**
- *Myopic* (Part W's maximal, rerun as the paired reference).
- *Worker union contracts:* in an encounter the two workers may write a joint fill "strike unless the wage is at least
  s" (s ∈ {¼, ½}), keyed on the boss's lineage, accepted under (M) the myopic rule (both workers at least as well off at
  the re-evaluated encounter, one strictly) or (C) the **credible-response rule**: the boss's response is its best reply
  among the actions its program and fills can express, given the joint fill; accepted iff both workers are at least as
  well off under that response and one strictly. Boss–worker contracts are also judged under the same rule in (C).
- *Union contracts keyed on role* (the boss slot, any lineage) under (C), as the open variant.

**Statistics.** Universal-open, island efficiency, P(C,C), lineage-closed islands and held fills by scope and origin
(Part 1); fair, ¼ and zero wage shares, worker payoff, union-contract adoption and execution (strikes actually played
under a union fill) with the number of challenges (Part 2). Paired run-level intervals against the reference; outcome
regions predeclared.

**Scale guard.** ≤ 3 workers; a sibling realizable run uses up to 3; check `ps` before multi-worker steps; one job per
process. **Waiting:** watch short commands in the foreground; for long batches wait on one background command that exits
at completion, or end the turn with outputs on disk; never poll periodically. Drop order: open-history-only, then
fission–fusion of open maximal, then the role-keyed union variant.

## Required outputs

`src/hooks_w2*.py`, `tests/test_hooks_w2.py` (behaviour-keyed contracts and writes; the credible-response acceptance on
hand cases; reproduction of Part W's maximal cells), `notes/hooks-w2.md` (§1 design and hand predictions; §2 costs),
`runs/hooks-w2.md` and `.json`, predictions committed before any counted cell, and the usual hand-back.

## RE predictions (with falsifiers)

1. **Parochial keys cause the PD collapse:** open maximal has universal-open ≥ 0.65 (at least the inert level), against
   lineage maximal's ≈ 0. *Falsifier:* open maximal ≤ 0.2.
2. **Contracts are the decisive part:** open contracts only recovers most of the gain (≥ 0.5); open history only does not
   (≤ 0.3). *Falsifier:* the reverse ordering.
3. **Open maximal survives fission–fusion** (≥ 0.7 universal-open). *Falsifier:* ≤ 0.4.
4. **Myopic union contracts change nothing:** under (M) the fair share stays ≤ 0.05 (a joint strike demand is never a
   myopic Pareto improvement). *Falsifier:* ≥ 0.15.
7. **Counter-predictions registered (gemini-4-argon).** If β is a static box class, open contracts make defectors
   suckers to their own class or an unbridgeable β-clique, so predictions 1 and 2 fail; lineage-keyed (C) union contracts
   fail (≤ 0.10) while role-keyed (C) succeed (≥ 0.30).
5. **Credible-response union contracts reach the fair wage on some islands:** under (C) the fair share is ≥ 0.2, with
   union strikes rarely executed (≤ 10⁻²). *Falsifier:* fair share ≤ 0.05.
6. **The role-keyed union contract does at least as well as the lineage-keyed one** under (C). *Falsifier:* lower by ≥ 0.2.

## Amendments after the first review (gemini-4-argon; these supersede the text above where they conflict)

1. **Open keys defined.** An open contract or open history fill is keyed on one behavioural predicate of the partner's
   *effective* behaviour (base program plus its fills, evaluated on Part W's closed node set): "the partner provably
   cooperates with me". A behaviour-keyed contract is therefore the joint fill "cooperate with any partner that provably
   cooperates with me", a conditional promise to a class defined relative to the holder, evaluated before the new fill
   is written. Static base-box classes are not used as keys.
2. **The credible-response rule defined.** Under (C) the boss's response to a candidate union fill is its best wage in
   {0, ¼, ½} (a single wage fill the boss could hold), computed from the encounter payoffs with the workers' joint fill in
   force; ties are broken in favour of paying the demand (not being struck). A union contract with a higher s that is
   accepted supersedes a held one with a lower s. Adoption, held share and execution are reported separately for s = ¼
   and s = ½.
3. **Controls.** Part W's maximal (boss–worker contracts only, no union contracts) evaluated under (C), separating union
   contracts from credible-response boss–worker contracts; the main (C) union cell keeps boss–worker contracts myopic.
4. **Logs.** The sucker rate of holders of open contracts (C against D), and contract survival on winning islands, to
   tell open contracts that work as promises from open contracts that self-destruct.

## Amendments after the second review (gpt-6.1-sol; these supersede the text above where they conflict)

1. **Open contracts are judged jointly, by the prover.** An open contract is the pair of fills "cooperate with any partner
   that provably cooperates with me", one per party; eligibility is evaluated with *both* fills in force, by the arm's
   free sound box on Part W's closed node set, so two such promises cooperate by Löb (as two FairBots do) and no
   cooperative fixed point is chosen by fiat. Accepted iff, so evaluated, the encounter is a Pareto improvement over
   actual current play. Lineage contracts keep Part W's (post-write) eligibility, so both technologies use the same
   timing; proposal, eligibility, acceptance and activation rates are logged per technology.
2. **The credible response is implemented, not only valued.** Under (C), when a union contract is accepted, the boss
   adopts the best-response wage as a fill keyed on the two workers' lineages (or on role in the role-keyed variant),
   executed in later encounters; predicted and realized wages are logged. Acceptance compares against actual current play
   (the boss's present wage), with every other fill and the conflict rule fixed. Boss–worker contracts: both parties'
   payoffs must weakly improve, one strictly; a boss may overwrite its own contracted wage only through a later accepted
   contract.
3. **Matched union cells.** Union contracts run under (M) and (C) with identical proposals, priorities and supersession
   rules; named cells: union-M, union-C, union-C-role, boss–worker-only-C, and the myopic reference.
4. **Hand tabulation first.** Notes §1 tabulates every candidate demand against every boss wage, ties included, and the
   predicted acceptance under each rule, before any code; prediction 4's "never" is restated as "against non-conceding
   constant bosses", with responsive bosses tabulated.
5. **Scope.** Conclusions are about these finite lotteries; support and transitions are reported; superseded predictions
   are scored separately from amended ones.
