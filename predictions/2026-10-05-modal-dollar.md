# Predictions: the modal arm on two-player divide-the-dollar, one population (2026-10-05)

Spec `specs/2026-10-05-modal-dollar.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-modal-dollar-gpt-6.1-sol.md`;
where the spec's [after review] text and the review differ, the spec is the resolution). Code `src/modal_dollar.py`
(on `src/dollar3.py`'s canonical reduction, `src/dollar_partitions.py`'s chain/summary/lottery code and
`src/chain.py`, `src/gl_proofs.py`). Committed before any counted run (chains, reduced subsystem, augmentation,
fixed roles, lotteries).

**Computed before this commit** (the static go/no-go checkpoint, which the spec allows first because it decides whether
P′ is a candidate; recorded in the addendum below and in `runs/modal-dollar.md`): the class counts at n = 7 and 11;
the GLS+Def audit of the evaluator (all 21,321 pairs at n = 7 plus P, and a 6,000-pair sample at n = 11); the
certificates of the four named encounters; the invasion table of every self-efficient class by the five constants
and by its neutral neighbours (two-step exits), its payoff entering the greedy polymorphism, and fixation
probabilities at N = 10³ and 10⁴, in both arms. No chain, reduced-subsystem, augmentation, fixed-role or lottery
number was computed before this commit.

## Design as implemented (deviations from the spec stated)

- **Grammar and prior.** The spec's two-slot restriction of `dollar3`: A ::= a | if(B, A, A); B ::= BOX_L(THEM = a)
  (3 nodes) | not B | and B B | or B B; L ∈ {PA, PA + Con}. Programs are merged into canonical functions
  (essential atoms, action table) as in `dollar3.Lang`; μ = Σ over spellings of size ≤ n of 2^−bits, bits =
  log2 a(|p|) + 2 log2 |p| + 1. Program counts a(s): 5 at s = 1, 250 at s = 6–9, 5,250 at s = 10, 40,250 at s = 11.
- **Evaluators.** Two-player restrictions of `dollar3.eval_modal` / `dollar3.eval_weak` (the three-player kernels
  cannot be called on a two-player game; the code is the same algorithm, checked below against GLS+Def). Modal: an
  atom is true at world n iff the opponent played a at every world m with L ≤ m < n; the stable value is the play.
  **Matched weak arm:** identical grammar and prior; the atom is evaluated by simulating the opponent in the
  encounter (budget iteration from bottom); the level is ignored (a level-1 atom is the level-0 atom, so grammar and
  prior are identical by construction); a program still bottom at the fixed point plays the game's minimax action
  S1 (`games/dollar5.yaml`, as in the published weak `dollar5` arm).
- **Classes** = payoff-equivalence classes (identical payoff rows and columns). n = 7: 205 canonical functions;
  **modal 205 classes, weak 77**. n = 11: 14,605 canonical functions; **modal 8,118 classes, weak 368** (reported
  here before any attempt at the n = 11 chain, as the brief requires).
- **P′ is already in L_7.** The spec's spelling `if(BOX(THEM = S1), S5, if(BOX(THEM = S5), S3, S3))` reduces to the
  one-atom function `if(BOX(S1), S5, S3)` (size 6). So the paired n = 7 chains already test P′ (and its PA + Con
  twin `if(BOX1(S1), S5, S3)`). P = `if(BOX(S1), S5, if(BOX(S5), S1, S3))` is a two-atom function whose minimal
  spelling is 11 nodes; it first appears at n = 11 (n = 10 has two-atom functions only through and/or).
- **Augmentation arm** (if n = 11 does not fit): P and P′ added to both n = 7 languages with identical syntax mass,
  swept over 10⁻⁴, 10⁻³, 10⁻² of the prior (split equally between P and P′; P′'s own n = 7 mass kept); "policy
  duplicates" are read as the PA + Con twins (`if(BOX1(S1), S5, S3)` and P with BOX1 atoms), which get the same added
  mass. The un-augmented n = 7 pair is kept as the comparison.
- **Chain:** `src/chain.py`'s lazy attractor chain (as `src/dollar_partitions.py`'s one-population arm) on the class
  payoff matrix, w = 0.3, N ∈ {10², 10³, 10⁴, 3·10⁴, 10⁵}, at θ = 10⁻⁷ and 10⁻⁹ (both reported).
- **Statistics.** P(efficient) = π-weighted probability that a random encounter is an efficient split (demands sum to
  1); E[max share] as in RESULTS "Divide-the-dollar partitions"; **greedy-polymorphism mass** = π of polymorphic states
  in which S5 holds ≥ 0.5; the **efficient set** = π of states whose encounters are ≥ 0.99 efficient. Entry/exit rates
  (per mutation event) of the efficient set and of the greedy polymorphisms are reported against N.
- **Reduced subsystem** {S3, S5, A5 = `if(BOX(S5), S1, S3)`, P, P′}: same chain code on the 5×5 payoff block, masses
  from the n = 7 prior (P at 10⁻⁴) renormalized over the five; N = 10³, 10⁴, 3·10⁴. (The chain code is the dense
  reference at this size: every state is expanded; GTH on the closed class.)

## The RE's predictions (copied verbatim from the spec)

1. **At n = 7 both arms leak by the same mechanism.** One-atom accommodators are neutral shadows of S3 in both arms,
   S5 invades them, and the greedy polymorphism holds ≥ 0.8 of π by N = 3·10⁴ in the modal arm and in the matched
   weak arm; the weights need not agree within 0.1 (sol's point), the mechanism must. *Falsifier:* modal
   P(efficient) ≥ 0.7 at N = 3·10⁴ at n = 7.
2. **P is strictly invaded by S5 and does not rescue efficiency** (sol's objection, adopted): with P in the
   language the modal arm's P(efficient) ≤ 0.6 at N = 3·10⁴, and the reduced subsystem shows P entering the old
   polymorphism and ending in a P/S5 mixture near x_P = 1/3. *Falsifier:* P(efficient) ≥ 0.8 at 3·10⁴ with P and
   without P′.
3. **P′ cannot re-enter the greedy polymorphism:** its invasion payoff is within 0.05 of the polymorphism's mean
   (it earns 5/6 only against the accommodator fraction, ≈ 0.25, and 0 against S5), so it is at best neutral there,
   and the modal arm with P′ keeps P(efficient) ≤ 0.6 at N = 3·10⁴. **Sound reading does not rescue bargaining
   efficiency; certified commitment helps the greedy.** *Falsifier:* P′'s invasion payoff exceeds the mean by
   ≥ 0.1, or modal P(efficient) ≥ 0.8 at N = 3·10⁴ with P′ (then the RE's first-draft hypothesis is back).
4. **Fixed roles keep the accommodator ratchet under sound reading** (endpoints ≥ 0.9 of π at N ≥ 10³ in the modal
   fixed-role chain), and **the modal lottery matches the weak one** (50–50 ≥ 0.8 of islands at (100, 64),
   mN = 0.1, in both arms). *Falsifier:* endpoints ≤ 0.6 at N = 10³, or the arms' 50–50 shares differing by ≥ 0.2.

## The subagent's predictions (written after the static checkpoint, before any chain)

- **S1 (modal n = 7 rescues efficiency at a √N rate).** Modal P(efficient) ≥ 0.75 at N = 3·10⁴ and is non-decreasing
  from 10⁴ to 10⁵; the odds π(efficient set)/π(greedy polymorphisms) grow like N^β with β ∈ [0.3, 0.7] over
  [10⁴, 10⁵]. *Falsifier:* P(efficient) < 0.6 at 3·10⁴, or lower at 10⁵ than at 10⁴.
- **S2 (mechanism).** The efficient set's exit into the greedy polymorphism is two-step neutral (a one-atom
  accommodating shadow drifts in at μ/N, then S5 invades strictly), slope in N ∈ [−1.1, −0.9] over [10³, 10⁵];
  the polymorphism's re-entry into efficiency at N ≥ 10⁴ is carried by P′-type programs (`if(BOX_L(S1), S5, S3)`,
  `if(BOX_L(S1), S5, S2)`: exploit a provable conceder, otherwise demand at most 1/2), ≥ 0.5 of the re-entry flow,
  with ρ slope ∈ [−0.6, −0.4] (first-order neutral, positively frequency-dependent). *Falsifier:* either slope
  outside its interval, or P′-type programs < 0.5 of the re-entry flow at N ≥ 10⁴.
- **S3 (the matched weak arm does not leak at n = 7).** In this grammar no reader is a neutral shadow of S3 (a
  reader's self-play diverges to S1), so every exit from all-S3 is deleterious with a barrier ∝ N; weak
  P(efficient) ≥ 0.9 at N ≥ 10⁴. *Falsifier:* weak P(efficient) < 0.8 at N = 10⁴ or 3·10⁴.
- **S4 (P is a greedy-helper, as sol said).** In the reduced subsystem P enters the S5–A5 polymorphism strictly and
  the replicator lands in an S5/P mixture with x_P within 0.02 of 1/3; with P added (augmentation, P only) the modal
  P(efficient) at N = 3·10⁴ moves by less than 0.05. *Falsifier:* x_P outside [0.31, 0.35], or |Δ P(efficient)| ≥ 0.05
  with P alone.
- **S5 (augmentation is a prior effect in the efficient direction).** With P and P′ (and twins) added at swept mass,
  modal P(efficient) at 3·10⁴ is non-decreasing in the added mass and not below the un-augmented value by more than
  0.02; the weak augmented arm stays ≥ 0.9. *Falsifier:* modal P(efficient) at mass 10⁻² below the un-augmented
  value by ≥ 0.05.
- **S6 (reduced subsystem is interpretable).** The reduced {S3, S5, A5, P, P′} chain's P(efficient) at N = 10⁴ and
  3·10⁴ is within 0.2 of the full modal n = 7 (+P at 10⁻⁴) chain, and its top transitions are S3 → A5 (neutral),
  A5 → S5/A5 (strict), S5/A5 → P′ (re-entry), P′ → S3 (neutral). *Falsifier:* a difference ≥ 0.2, or a different
  top cycle.
- **S7 (fixed roles).** Agree with RE 4's first clause: modal fixed-role endpoints (1/6 | 5/6) + (5/6 | 1/6) ≥ 0.9 of
  π at N ≥ 10³; the weak fixed-role arm in this grammar also ≥ 0.9. *Falsifier:* modal endpoints ≤ 0.6 at N = 10³.
- **S8 (lotteries).** 50–50 ≥ 0.8 of islands at (100, 64), mN = 0.1 in both arms, and the arms within 0.1 of each
  other at every cell. *Falsifier:* either arm < 0.7, or a difference ≥ 0.2 in any cell.
- **S9 (θ convergence).** Every chain's P(efficient) agrees between θ = 10⁻⁷ and 10⁻⁹ within 0.01. *Falsifier:* a
  difference > 0.02.

## Verdict rules

- P(efficient) is read at θ = 10⁻⁹ where both thresholds ran (θ = 10⁻⁷ otherwise, stated). "Holds" needs every
  clause; a clause that cannot be evaluated because the run did not happen is "not run", not a failure.
- RE 2's "with P in the language" is read on n = 11 if its chain runs, otherwise on the augmentation arm with P alone
  (stated); its falsifier ("≥ 0.8 with P and without P′") needs a language without P′, which no cutoff provides
  (P′ is in L_7), so it is read on the augmentation arm with P alone added to L_7 minus P′ and its twin, if run.
- RE 3's "the modal arm with P′" is read on the un-augmented n = 7 modal chain (P′ is in L_7).
- A falsifier firing is reported as such, whatever the reason; a mechanism clause that holds for a different reason
  is reported as "held for a different reason".

## Addendum: the static checkpoint (computed before this commit)

- **Audit.** GLS+Def provability (`src/gl_proofs.py`'s decision procedure, five-valued definitional constants
  P^a_xy) of every box atom against the evaluator: 0 disagreements in 21,321 pairs (41,814 atoms) at n = 7 plus P,
  and 0 in a 6,000-pair sample at n = 11 (23,936 atoms).
- **Certificates.** P′ vs P′: neither atom provable, plays (S3, S3). P′ vs A5: both atoms provable (6 sequents, 2 Löb
  steps each), plays (S5, S1): P′ exploits the certified conceder by a Löbian fixed point. P′ vs P: no atom
  provable, (S3, S3). P vs S5: BOX(S5) provable (2 sequents, 0 Löb), (S1, S5): P accepts the certified greed.
- **Candidates.** Modal: 42 self-efficient classes (S3, 32 neutral shadows of S3, others, P), mass 0.200 (S3 0.193).
  Strictly invaded by a constant: A5 and its twin, `if(BOX_L(S3), S3, S1)` (S4, S5), `if(BOX_L(S3), S3, S2)`,
  `if(BOX_L(S4), S1|S2, S3)` (S4), and **P (S5, ρ = 0.094 at N = 10³)**; S3 and P′ are not. Weak: S3 is the only
  self-efficient class and has **no neutral neighbour** (every reader's self-play diverges to S1); its exits are all
  deleterious (total 2·10⁻²⁴ per event at N = 10³, 8·10⁻²²⁰ at 10⁴).
- **The greedy polymorphism.** Modal G = S5 2/3 + A5 1/3, mean 5/18 (sol's number); weak G = S5 0.8 + A5_w 0.2,
  mean 1/6. **P′'s payoff entering modal G equals the mean (0.2778 vs 0.2778), but its fixation probability is
  9.2·10⁻³ at N = 10³ and 2.9·10⁻³ at 10⁴ (×√10 per decade: first-order neutral, positively frequency-dependent),
  and its fate is all-P′.** P enters G strictly (+0.111) and lands in S5 2/3 + P 1/3. G's total efficient re-entry
  flow: 1.8·10⁻⁵ (10³), 1.1·10⁻⁶ (10⁴) per event; S3's two-step exit into inefficiency 1.9·10⁻⁷ at 10⁴.
