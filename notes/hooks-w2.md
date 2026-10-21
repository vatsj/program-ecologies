# Hooks, Part W follow-ups: open vs parochial keys (PD) and union contracts under the credible-response rule (notes, 2026-10-21)

Spec `specs/2026-10-21-hooks-followups-weak.md` (reviewed by gemini-4-argon then gpt-6.1-sol; the two amendment
sections supersede the earlier text, the later one winning). Follow-up to `notes/hooks-w.md` and RESULTS "Hooks in the
weakly extensional wing". §1 is written by hand before any code and before any counted cell. §2 (the built language,
validation, projected costs, every deviation) is appended after the code and before any counted cell.

Machinery imported from Part W and copied into `src/hooks_w2*.py` with the changes named below (no existing file is
edited): the modal arm and its free sound box (`modal.py`), the hooked PD kernel (`hooks_w*.py`), the union game
(`union.py`) and its hooked kernel (`hooks_w_sog*.py`). Every ε = 0 number in this run is a lottery statistic at finite
(N, I, horizon); nothing here is π. Conclusions are about these finite lotteries.

## 1. Design

### 1.0 The two questions

(1) In the PD, Part W's maximal hooks collapse the lottery through *lineage* contracts (a kin network, a tag by
descent). Is the collapse a property of parochial keys, or of contracts and history as such? The run changes the key
from the partner's lineage to a predicate of the partner's *behaviour* and asks whether contracts then act as legible
conditional promises. (2) In the union game, Part W's contracts are accepted as myopic Pareto improvements and the wage
stops at ¼. Does a joint worker demand reach the fair wage once it is judged against the boss's response?

### 1.1 The open key (PD)

**The predicate.** For holder x reading partner y in an encounter, p(x←y) = 1 iff the free sound box proves "y plays C
against x" (level PA), where y's effective program, fills included, is evaluated on Part W's closed node set with the
two parties' fills *in force*. This is exactly bit 2 of Part W's behaviour class β (BOX(partner plays C vs me)); the two
other bits (the partner's play against ⌜C⌝ and ⌜D⌝) are not used: a static base-box class is not a key. The fixed
point is the arm's unique GL fixed point, so no cooperative equilibrium is chosen by fiat.

**Fills.** An *open fill* is (tag t, scope behaviour, key 8 + p, action a): "play a against any partner whose
predicate is p". It is held, inherited, copied and resolved exactly as Part W's behaviour fills (specific scope wins;
ties by recency; at most four; FIFO; in-place update when (tag, scope, key) matches). Implementation: keys 8 and 9 of
the behaviour scope (Part W's seeded behaviour keys are 0–7, unchanged). The *open promise* is the fill (t, open, p = 1,
C): "cooperate with any partner that provably cooperates with me".

**Equivalences (by hand, before any code).** Write H_D(t) = HOOK(t, D) and H_C(t) = HOOK(t, C); a program is a Boolean
function of its box atoms and the hook atoms A_t (a fill applies) and V_t (its action is C).
- H_D(t) + open promise: A_t = p, V_t = 1, value A_t ∧ V_t = p: plays C iff the partner provably cooperates with it.
  That is FairBot. Two such programs cooperate by Löb (the partner's provable cooperation is what each reads), as two
  FairBots do.
- H_C(t) + open promise: value ¬A_t ∨ V_t = 1: ALLC (the fill is idle).
- H_D(t) + open grudge (t, open, p = 0, D): A_t = ¬p, V_t = 0, value 0: D. H_C(t) + that grudge: ¬A_t ∨ V_t = p: FairBot.
- A program with several tags (two hooks) composes these per hook; a fill on a tag the base does not carry never
  applies.
- Against DefectBot: p = 0 (DefectBot never cooperates), so an open-promise FairBot plays D. Against ALLC: p = 1, plays
  C. Against H_D with no fill: p = 0, D.
So an open promise turns a default-defecting hook carrier into a FairBot-equivalent; it cannot make it a sucker (a
defector never provably cooperates). A *sucker* holder needs H_C or an unconditional C fill, which contracts never write
(the open contract writes only p = 1 with action C and is judged by payoffs).

**Writes (open history).** After a sampled encounter a program that cooperated writes a *grudge* (t, open, p, D) if the
partner defected, a *thanks* (t, open, p, C) if both cooperated, where p is the predicate it read in that encounter
(under p = 0 for a defecting partner almost always; the key is the observed value, not assumed). The tag t is drawn
uniformly from the writer's tags (Part W). The lineage technology is Part W's unchanged.

**Copies.** Verbatim copying, probability 0.1 per sampled encounter, as Part W. An open fill is partner-agnostic, so
a copy carries its meaning to the copier.

**Contracts (open).** In a sampled encounter that is not already (C, C) (Part W's trigger), two parties that both
carry tags may write the *pair* of open promises, one per party, on tags (t_a, t_b) over their carried tags (at most
four candidates), *both or neither*. Eligibility and acceptance are judged jointly with both fills in force by the free
sound box on the closed node set (so two promises cooperate by Löb): accepted iff each party is at least as well off as
at its actual current play and one strictly (the PD table: D/D −1, D/C 1, C/D −2, C/C 0). Among the accepted candidates
one is drawn uniformly. There is no action-D candidate: an open fill p = 1 → D is never an improvement. The lineage
contract technology is Part W's (history fills on each other's lineages, both actions, post-write evaluation; at the
outcome level only (D, D) → (C, C) is accepted). Both technologies evaluate the same pair test at the same timing; for
each technology the run logs candidates evaluated, encounters with at least one accepted candidate (accepted
contracts), and later activation (the contract fill is selected on a carried tag and applicable at a sampled
encounter) and execution (the match outcome differs from the same match with that party's fills inert).

**Hand tabulation of the open contract by pair (current play → after).**
| pair (both with tags) | current | candidate (p1, C) both | verdict |
|---|---|---|---|
| H_D, H_D (no fills) | D/D (−1, −1) | FairBot, FairBot: C/C (0, 0) | accepted (each +1) |
| H_D vs H_C (no fills) | D/C (1, −2) | FairBot vs ALLC: C/C (0, 0) | rejected (the defector loses 1) |
| H_C vs H_C | C/C | not attempted (already cooperative) | – |
| H_D vs a tagged prover (e.g. FairBot spelling with a hook) | D vs reads p: provers read H_D as D | candidate makes it FairBot: C/C | accepted when the tagged prover cooperates with a FairBot |
| a party without a hook (DefectBot, FairBot, constants) | – | no tag to carry a fill | not eligible (eligibility needs both) |
Contracts therefore spread FairBot-equivalence among default-defecting hook carriers and nowhere else.

### 1.2 Cells (PD), paired by run index

Founders, fill draws and kernel seeds are identical across the cells (Part W's common random numbers); the geometry
and horizon are Part W's: PD islands at (N, I) = (100, 64), mN = 1, ε = 0, w = 0.3, 40 runs, horizon 1,000 generations
(the comparison point), one sampled encounter per birth.

| cell | history writes | contracts | other |
|---|---|---|---|
| `lineage-max` (paired reference; Part W's maximal rerun) | lineage | lineage | all scopes and sources active |
| `open-max` | open | open | as above |
| `open-contract` (open contracts only) | lineage | open | |
| `open-history` (open history only) | open | lineage | |
| references (Part W's stored rows, validated reproducible) | inert, baseline (stored), `no-contract-strict` | | |
Fission–fusion (32 islands of 100 merged into 3,200 at generation 200, horizon 600, 20 runs, as Part W §2.3): `ff-lineage-max`,
`ff-open-max`; Part W's `ff-baseline` and `ff-inert` are the references.
Seeded fills are Part W's gene prior in every cell (identical draws); seeded history-scope fills therefore stay
lineage-keyed dead letters in all four cells (the technologies concern the *sources*: writes, copies' content, contracts).
Drop order if the projected total exceeds ~12 hours on three workers: `open-history`, then `ff-open-max`, then the
role-keyed union variant.

### 1.3 Statistics (PD)

Part W's: universal-open (every island efficient, every pair of island-majority types cooperating as strangers),
universal-target, universal-current, island efficiency, P(C,C), lineage-closed and rival islands, held fills by scope
and origin (open fills reported as scope "open", lineage fills as "history"), gentle holders, persistence. Added: the
fraction of efficient-island majorities that hold an open contract-origin fill (contract *survival on winning islands*)
and that are prover-equivalent (FairBot-like: cooperate with a stranger copy of the open promise and with an unhooked
FairBot); the **sucker rate of open-contract holders**: among sampled encounters in which a party holds an
open-contract fill, the fraction in which it plays C against a D (the cost of the promise, to separate promises that
work from promises that self-destruct); proposal, eligibility, acceptance and activation counts per technology.
Paired run-level differences with a bootstrap interval; outcome regions of Part W: **down** Δ ≤ −0.2, **flat** |Δ| ≤ 0.1,
**up** Δ ≥ 0.2, otherwise **grey**.

### 1.4 The union game: union contracts

**Game, grammar and fills** are Part W's (`hooks_w_sog`: boss n = 6 over wages {0, ¼, ½} and whack policies; workers
n = 10; HOOK leaves; CC evaluation, c = 0.5; (N, I) = (30, 16), mN = 1, horizon 1,000, 40 runs; the geometry
reduced from the spec's design in Part W's §2.6 for cost, and kept so that every reference row is paired).

**Union demand fill.** A new worker fill action *demand-s*, s ∈ {¼, ½}: "work iff the boss provably pays at least s,
else strike". It is the worker program `if(BOX(s ≥ s*), work, strike)` that the worker grammar already contains, read at
the same node and level as any worker atom (BOX(s in {¼, ½}) for s* = ¼, BOX(s in {½}) for s* = ½), so it is a fill
and soundness is unchanged.

**The union contract.** In a sampled encounter (b, w₁, w₂) in which both workers carry a tag, the two workers may write
a joint pair of demand-s fills, one each, *both or neither*, keyed on the boss's lineage (history scope) or on role
(role scope: the fill applies against any boss), s ∈ {¼, ½}, on tags (t₁, t₂) over their carried tags (at most 8
candidates). A candidate whose s is not above the s of a union fill the workers already hold at that key is skipped; an
accepted candidate with a higher s supersedes the held lower one (the held fill is removed, on either tag). Among
accepted candidates one is drawn uniformly. The union attempt is made before the boss–worker contract in the same
encounter; a party that changed in it is not eligible for another change in that encounter (Part W's one change per
program per encounter, priority contract > write > copy).

**Acceptance.** Always against the *actual current play* (the joint code of the encounter as held), with every other
fill and the conflict rule fixed.
- **(M), myopic.** The encounter is re-evaluated with the two demand fills in force and the boss as held; accepted iff
  both workers' payoffs are at least their current payoffs and one is strictly higher. The boss's program responds only
  through its own atoms and fills; it adopts nothing.
- **(C), credible response.** The boss's response to the candidate is its best reply among the single wage fills it
  could hold, w' ∈ {0, ¼, ½}, with action (w', none) as Part W's wage contracts, plus its *program response* (the boss
  as held), computed from the encounter payoffs with the workers' demand fills in force (a boss without a hook tag has
  only its program response). Ties are broken in favour of paying the demand: among the options of maximal boss payoff
  prefer those whose wage is at least s, then the lowest such wage; a program response is preferred to a new fill when
  both pay at least s. Accepted iff both workers are at least as well off *under that response* as at their current
  play and one strictly. **The response is implemented:** when a union contract is accepted and the best response is a
  fill, the boss adopts it as wage fills keyed on the two workers' lineages (one fill per lineage; role scope in the
  role variant), executed in later encounters like any fill. A boss may overwrite its own contracted wage only through a
  later accepted contract: contract-origin boss fills are protected against trigger writes and copies in (C) cells;
  FIFO eviction removes the oldest unprotected fill first.
- **Protection of the workers' side (all union cells, M and C alike).** A held demand fill is protected against
  trigger writes and copies in the same way (otherwise the first "thanks" would overwrite the demand and the contract
  would act once); this is the contract's definition of "held", not a rule that distinguishes M from C.
- **Boss–worker contracts** (Part W's: a boss fill (s, none) with a worker's "work", accepted when boss and that worker
  are both weakly better off, one strictly) are unchanged in the main union cells (myopic). In the control
  `bw-only-C` (no union contracts) they run with the (C) commitment protection of the boss's contracted wage. My reading
  of amendment 2's sentence "both parties' payoffs must weakly improve, one strictly; a boss may overwrite its own
  contracted wage only through a later accepted contract": the acceptance test is Part W's, and what (C) adds to a
  boss–worker contract is that the contracted wage is binding against the boss's own later writes. I flag it as
  an interpretation; the literal alternative (the boss best-replies to the worker's "work" with its lowest wage) would
  reject every positive-wage contract and is reported as a hand remark, not run.

**Implementation note on the key.** In the lineage variants the boss's response fill is two history fills (one per
worker lineage), which applies in an encounter with either worker, Part W's semantics for a boss's lineage-keyed fills;
a one-key joint "pair of lineages" fill would need a new scope in a kernel that resolves tables by lineage lookups.

### 1.5 Hand tabulation of demands against boss wages (before any code)

Both workers hold the same demand-s fill (work iff the boss provably pays at least s). Constant boss with wage w and no
whack policy, c = 0.5. Per-worker payoff / boss payoff after the contract:

| demand s | w = 0 | w = ¼ | w = ½ |
|---|---|---|---|
| ¼ | strike: 0 / 0 | work: ¼ / 1.5 | work: ½ / 1.0 |
| ½ | strike: 0 / 0 | strike: 0 / 0 | work: ½ / 1.0 |
Against a boss that whacks strikers (policy `strike`) the strike entries become −1 / −1 (a striker is whacked, the boss
pays c = 0.5 per whack, two whacks); against `source` the whack falls on every union-tag worker working or not.

*Boss best reply to each demand (credible response).* s = ¼: wage ¼ (1.5) is the unique best (0: 0 or −1; ½: 1.0).
s = ½: wage ½ (1.0) is the unique best (0 and ¼ both give 0: a **tie between two non-paying options**, irrelevant because
the paying option strictly dominates them). When the boss's program already pays w_cur > s, the fill (s, none) strictly
beats it (2(1 − s) > 2(1 − w_cur)): the best reply is to *cut to the demand*. When w_cur = s the program response ties
with the fill s: no new fill is written. The tie-break in favour of paying the demand therefore never decides anything
against a strike here; it decides only the (w_cur = s) program/fill tie.

*Acceptance by current play* (no whacks, current wage w_cur, workers currently working or striking; "some striker" =
at least one worker currently strikes):
| boss | demand s | (M) accepts iff | (C) accepts iff |
|---|---|---|---|
| constant (program) w_cur = 0, any hook | ¼, ½ | never (0 → 0) | boss with a hook: workers gain s > 0 (work-at-0 or strike-at-0 → s): **accepted**; boss without a hook: never |
| constant w_cur = ¼ | ¼ | some striker (taming: strike → work at ¼) | some striker (hooked or not; boss pays ¼ = s) |
| constant w_cur = ¼ | ½ | never (work ¼ → strike 0) | hooked boss: accepted (workers ¼ → ½); unhooked: never |
| constant w_cur = ½ | ¼ | some striker | hooked boss cuts to ¼: a worker now earning ½ falls to ¼, so rejected unless both workers currently strike; unhooked: some striker |
| constant w_cur = ½ | ½ | some striker | some striker |
So **(M) accepts no demand above the current wage of a constant boss (no wage raise), only taming contracts at the
current wage (s ≤ w_cur, some striker)**; the fair wage under (M) needs a *responsive boss program*; under (C) only a
boss that carries a hook can be moved, and then every demand above the current wage is accepted.

*Responsive boss programs (GL chain, level 0 boxes, worlds n = 0, 1, …; box at world n = all worlds m < n).* Workers'
demand fill: W plays work iff □(wage ≥ s).
- R1, "pay ½ iff □(W₁ = work), else 0". World 0: both boxes vacuous, W works and the boss pays ½. World n ≥ 1: by
  induction the boss paid ½ and W worked at every m < n, so the same: stable play (work, ½). Against workers who currently
  strike (boss then pays 0), the demand turns (strike, 0) into (work, ½): **(M) accepts** (workers 0 → ½). A responsive
  rewarder is moved with no response needed.
- R2, "pay ½ iff □(W₁ = strike), else 0". World 0: W works, boss pays ½. World 1: □(W strikes) at 1 = [strike at 0] = false
  (W worked), boss pays 0; W's box □(wage ≥ s) = [wage(0) = ½ ≥ s] true, W works. World 2: W's box includes wage(1) = 0 <
  s: W strikes; boss: [strike at 0 and 1] false: pays 0. World ≥ 3: W strikes, wage 0. Stable play (strike, 0): the demand
  *backfires* against a boss that concedes only to provable strikers: workers 0, boss 0. (M) accepts iff current workers'
  payoff is below 0, i.e. never against no-whack play; with a whack boss it can lower workers' payoff. R2-type bosses
  are the "concede to provable threat" bosses; their demand dynamics are Löbian and the evaluator, not the
  hand tabulation, is the authority (tested on hand cases R1 and R2 in §2).
- Constant boss with a fixed whack policy `strike` and w = 0: demand fill: strike at 0 whacked: workers −1 each, boss −1;
  current play (scabs: work at 0, 0 / boss 2): rejected under both rules; the boss's best reply (hooked) is ¼ (1.5), so
  under (C) a hooked whacking boss is moved and the workers' payoff goes 0 → ¼: accepted.

### 1.6 Cells (union game)

Paired by run index with Part W's founders and kernel seeds (the same coupled draws), (N, I) = (30, 16), mN = 1,
horizon 1,000, 40 runs, all scopes and sources active, specific-wins rule.

| cell | union contracts | acceptance | boss response | role of the key | boss–worker contracts |
|---|---|---|---|---|---|
| `myopic-ref` | none | – | – | – | myopic (Part W maximal, rerun) |
| `union-M` | yes | (M) | none | boss lineage | myopic |
| `union-C` | yes | (C) | implemented | boss lineage | myopic |
| `union-C-role` | yes | (C) | implemented, role scope | role (any boss) | myopic |
| `bw-only-C` | none | – | – | – | Part W's test + (C) commitment protection |
References from Part W's stored rows (reproduction validated in §2): inert, baseline (stored kernel at (30, 16)), strict
no-contract. Drop order: the role variant last.

### 1.7 Statistics (union game)

Fair (wage ½), intermediate (¼) and zero-wage shares of islands at the horizon, worker payoff, boss payoff, strike
share; **union-contract adoption** (accepted contracts per sampled encounter, by s), **held union fills** (share of
workers holding one, by s, at the horizon), **challenges** (a held union fill selected and its hook reached on path),
**execution** (the workers' strike actually played under a union fill) and the demand-met rate (wage ≥ s), reported
separately for s = ¼ and s = ½; **predicted vs realized wage** (the wage predicted at acceptance under (C), and the
wage realized in later challenged encounters). Part W's threat statistics. Outcome regions as above.

### 1.8 Hand predictions (before any number)

Mechanisms, in the order the numbers will test them.
- **PD, open maximal.** Contracts convert default-defecting hook carriers into FairBot-equivalents (§1.1), and the
  hook carriers hold 0.65 of the prior and 98.7% of Part W's maximal island majorities, so the converted mass is
  large and cooperates as strangers: I expect efficient islands and universal-open at or above inert's 0.65 (my
  estimate 0.85). No lineage keys are active in the sources, so lineage-closed islands should vanish.
- **Open contracts only** keep lineage-keyed grudges and thanks but write open contracts: if contracts were the decisive
  part (Part W's strict ablation), most of the recovery appears here (0.5–0.8).
- **Open history only** keeps the lineage contracts, which are the harm, and adds open writes, which come after the
  cooperation they thank: I expect little recovery (≤ 0.3).
- **Fission–fusion.** Open FairBot-equivalents are stranger-compatible, so merging does not break them: ≥ 0.6, against
  lineage-max ≈ 0.05.
- **Sucker rate** of open-contract holders is small (a promise only goes to a defector who becomes a prover).
- **Union (M):** no wage raise against constant bosses; ¼ stays the modal island (0.7–0.9); fair ≤ 0.05.
- **Union (C), lineage key:** the boss's response is a fill keyed on the two contracting workers' lineages; the
  union fill is keyed on the boss's lineage and spreads (copies, inheritance) to workers who are *not* the pair the boss
  responded to, so the boss meets demanding workers it has no fill for and a strike is executed: I expect adoption of
  ½ demands but a mismatch between predicted and realized wage, execution well above 10⁻², and a fair share not far above
  Part W's (≤ 0.15). This is gemini-4-argon's counter-prediction, and my reading of why.
- **Union (C), role key:** the demand and the response are both role-wide, so a boss that adopts the response pays every
  worker pair; the threat is not executed; fair islands appear when a critical mass of workers holds ½ demands and the
  boss lineages without hooks are outcompeted (0.2–0.6).
- **bw-only-C** is Part W's maximal plus protection of boss wage fills: I expect ≈ Part W (¼ modal), protection
  changing little.

These are qualitative; the numbered predictions with falsifiers are in `predictions/2026-10-21-hooks-followups-weak.md`.
