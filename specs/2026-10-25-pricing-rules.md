# Spec: what compute should cost: three pricing rules across three games, 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. The RS (2026-10-24): (1) "I'm comfortable with a capped simulator primitive. It's a bash command
and we're aiming for Turing-completeness, so I see no principled reason to withhold it." (2) "One point in favor of A
[a timed-out read pays the full cap] is that it points the finger more directly at the reason we need the restriction
in the first place: infinite loops. I don't think I have an answer to your question [does 'compute costs are
nontrivial' mean every step should cost, or only wasted computation?]; I'm hoping we find experiments that answer the
question for us (ie meaningfully inform it)." Follows RESULTS "Rock–paper–scissors with a compute price", "A private
random tape in the realizable language", the PD price results (RESULTS "Price scaling paths", "K at n = 8") and
DEFERRED 16. REJECTED.md checked: atom pricing and per-match budget prices were dropped for the PD because they
rebuild the ALLC ladder; the flat per-step price here is the same kind and is run as the reference, not re-proposed.

## Why

A flat per-step price large enough to let the coin beat simulators in RPS (about 10⁻³ per step in L_T) would make PD
certificate checks (2–4·10⁴ steps) cost 20–40 per encounter against stakes of 1–2, and a price small enough for the PD
leaves mutual simulation in RPS nearly free. The question the RS left open is which notion of cost the ecology needs.
This experiment informs it by a robustness criterion: **a pricing rule is better if one price level delivers every
game's target at once, over a wide band of levels**, and worse if each game needs its own level.

## Pricing rules

All in L_T with the capped simulator primitive (the RS's ruling) and the private tape where a game uses coins. K is
the fuel cap of a root evaluation, recorded per game in the notes. [Redefined after review, so that each rule isolates
one notion of cost.]
- **F (every step):** every evaluation step costs c (the stored runs' rule).
- **A (failure only):** each nested read that times out costs P_fail; root steps and the steps of reads that finish are
  free; a root evaluation that exceeds K forfeits, as now. A is parameterized by P_fail itself, so its scale is the
  same in every game whatever K is. Charged per timed-out read call; when an inner read times out and the outer read
  handles it and finishes, only the inner call is charged.
- **F+A (every step, failure at the cap):** every step costs c, and a timed-out read is charged c·K *in place of* its
  own steps (never both). [Ledger made explicit after second review] Each step is charged once, to the root
  evaluation that executes it, whatever the nesting; a timed-out call's charge replaces the steps of its whole subtree;
  a call nested in a timed-out call is not charged separately. Tests cover partial-cap and nested timeouts.
- **B (every step, amortized):** every step costs c, but a reader pays a given read once per island lifetime: a cache
  keyed on the reader's quote and the read program's quote, both including their carried certificates, stores the
  cost only (the read is re-executed every time, against a fresh tape); timeouts are cached like other steps.
  [Made executable after second review] The first execution's actual charge is paid by the reader that runs it; later
  executions of the same keyed read are free, including their subtree, and their steps are not counted as root steps.
  The cache belongs to the island, migrates with nobody, is keyed on certificates (so a new certificate is a new key)
  and is cleared when the island is reset. Cache hits, first payers and cumulative charges are logged; a pre-warmed
  cache is compared with a cold one in the RPS cell.

## Games and targets

1. **RPS** (L_T with the tape; `src/lt_tape*.py`): target = the uniform mixer, or guarded mixers, hold the lottery
   with population exploitability ≤ 0.1 (the stored flat-price run: `U` 0.045 at c₀, 0.91 at 10⁻³).
2. **Inspection** (L_T with the tape): target = efficient islands ≥ 0.6 (the stored run: 0.875 unpriced).
3. **PD** (the realizable carrier lottery under world K and S-nonself production; `src/world_k*.py`,
   `src/provenance*.py`): target = universal-open runs ≥ 0.7 at (100, 64) (the stored world-K value 0.75–0.95).

## Design

For F, F+A and B at c ∈ {10⁻⁵, 10⁻⁴, 10⁻³, 10⁻²}, and for A at P_fail ∈ {0.01, 0.1, 1, 10} (and zero as the shared
reference), each game's primary lottery (the stored geometry; 40 runs RPS and inspection, 20 runs PD), paired founders across rules. Costs are
computed from the stored per-encounter step records where they exist (the tables carry steps per pair and per route);
B needs per-island caches and is computed in the kernel. The headline table: for each rule, the set of levels at which
each game meets its target, and the **joint band** (levels meeting all three). [After review] Static payoff tables over
a fine grid (c from 10⁻⁶ to 10⁻¹, P_fail from 10⁻³ to 10²) are computed for RPS and inspection from the stored step and
timeout records, to show where invasions flip between the panel's points. Inspection has no timeouts on its efficient
path, so A cannot test it against verification cost; the informative games for A are RPS and the PD. Secondary: which programs win, cost paid per
encounter, forfeits and timeouts.

[After second review] **Scoring and scope.** Targets are scored with run-level 95% intervals: met if the interval lies
above the threshold, failed if below, *undetermined* otherwise; a joint band needs every game met. Prices are reported
raw and normalized by each game's stakes (the payoff range), beside each game's K and timeout frequency, and the
result is stated as robustness under these conventions, not an intrinsic ranking of cost notions. Before launch the
engineer audits whether the stored records carry the nested-call counts A and F+A need, and records fresh event
traces where they do not; certificate production, retries and checks are priced like any other steps unless the
notes state an exemption. One complete cross-game panel (every rule at c = 10⁻⁴ and 10⁻³, P_fail ∈ {0.1, 1}) is run
before any optional cell, and any level that meets all three targets is rechecked at one larger geometry. Controls:
timeout-free bounded simulators (a read that would time out returns a default after a fixed small budget), and a
constant per-read toll. Reported beside the targets: support and transitions, non-play, gross and net payoffs, PD
P(C,C). This is a fixed-geometry lottery comparison, not evidence about large populations.

## Predictions (the RE's; falsifiers in brackets)

1. *F has no joint band.* No c in the panel meets all three targets under F [some c does].
2. *A has a joint band.* Under A, at least two adjacent P_fail levels meet all three targets [no adjacent pair does].
3. *A's mechanism.* Under A the RPS simulators lose to `U` at every P_fail ≥ 0.1, because a mutual simulation times
   out and pays P_fail [`U` below 0.5 at P_fail = 0.1]. *Counter-prediction (gpt-6.1-sol), registered:* timeout-heavy
   simulators decline, but readers that finish (against `U`, against constants, or with bounded reads that do not time
   out) can keep RPS off its target.
4. *B helps the PD and hurts the coin.* B keeps the PD target at c = 10⁻³ (repeated checks amortized), and in RPS it
   amortizes the simulators' reads too, so `U`'s share under B is at most its share under F at every c [B above F at
   some c by more than 0.1]. (Revised after review: the cache stores cost only.) *Counter-prediction (gpt-6.1-sol),
   registered:* subsidized reads change a frequency-dependent ecology, predators of simulators included, so `U`'s
   share need not be ordered against F's.
5. *F+A against F.* Charging timeouts at the cap widens F's RPS band downward (the coin wins at lower c) but leaves
   F's PD failure at high c, so F+A also has no joint band [F+A has one].

## Required outputs

- `src/pricing_rules.py` (+ runner, report) importing the existing L_T, tape and world-K modules; no existing file
  edited.
- `tests/test_pricing_rules.py`: the three rules' charges on hand-built encounters (a mutual simulation, a successful
  certificate check, a repeated check of the same partner); c = 0 reproduces each stored lottery draw for draw.
- `notes/pricing-rules.md` (§1 hand table of charges per rule for the named programs, before code; §2 deviations).
- `predictions/2026-10-25-pricing-rules.md`, before any counted cell, with the RS's statements first.
- `runs/pricing-rules.md` and `.json`, `runs/pricing_rules/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** PD lotteries in L_T are the expensive part; measure one PD run first and size the panel
(cut order, disclosed: c = 10⁻², B in inspection, F+A in inspection, PD at 10⁻⁵). Other subagents are running: check `ps` and free
memory before each batch; at most 2 workers while others are alive. One job per process; no `multiprocessing.Pool`;
one background wait per batch that exits at completion and fires if the log stops changing for 2 hours; never poll
periodically.
