# Predictions: modal-arm follow-ups (matched control, ratchet, finite-εN), 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-modal-followups-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-modal-followups-fable.md`), then revised. Committed before any of these runs. Where a verdict
changed after review it is marked **[revised after review]**, and the original value is kept in brackets.

## E1. Matched control: does the observation channel alone do it?

The modal arm differed from the weak arm in three ways at once: provability instead of simulation, no X, and
no `ROLE`. The control removes the last two.
- **W0:** the weak arm without X and without `ROLE`. The atoms are C and D; the applications are `THEM(ME)`,
  `THEM(THEM)` and `THEM(^A)` by simulation; self-reference that never terminates gets the minimax action D.
- **M0:** the modal arm with the PA box `BOX` only. Its grammar is isomorphic to W0's: identical program counts
  at every size (2, 2, 12, 30, 136, 484, 2,130 for sizes 1–7), so the same prior. Only the meaning of an
  application changes, from "simulate the opponent" to "it is provable that the opponent plays C".

ε→0 chain, PD, n ∈ {6, 7}, w = 0.3, N ∈ {100, 10³, 10⁴, 3·10⁴}.

Expectations:
- *W0:* FairBot by simulation, `THEM(ME)`, never terminates against itself and plays D, so the only reciprocators
  are third-party probes such as `THEM(^C)`. Those are fakeable.
- *M0:* contains FairBot `BOX(THEM(ME))`, which is unfakeable and enters neutrally. It has no `BOXD`, so it cannot
  express PrudentBot.

Verdicts:
1. **W0 behaves like the weak arm** [revised after review: tightened, from fable's two-state reduction]. P(C,C)
   peaks within one grid step of N = 10³ and is 0.005–0.02 at 3·10⁴ [was: below 0.05]. Exits from its best
   reciprocator are faker-dominated at N ≥ 10⁴.
2. **M0 behaves like the full modal arm** [revised after review: tightened]. P(C,C) rises monotonically and is
   0.70 ± 0.1 at N = 3·10⁴ [was: at least 0.5]. The cooperative-to-all-D ratio grows with exponent 0.50 ± 0.05 over
   N ∈ [10³, 3·10⁴] [was: 0.35–0.55]. M0 has no strict invaders at n ≤ 7, unlike the full arm.

   *Caveat from review:* the channel effect combines unfakeability with cheaper entry. M0's FairBot class has
   μ = 0.0148, against W0's `THEM(^C)` at 0.002, because W0's size-3 self-referential forms defect on themselves.
   E1 cannot separate those two.
3. **The channel is the cause.** At N = 3·10⁴, P(C,C) in M0 is at least 10× that of W0.

*Falsifier:* M0 at N = 3·10⁴ has P(C,C) below 2× W0, meaning the matched contrast fails to reproduce the original
gap. That would not by itself identify X or `ROLE` as the cause; separating them needs separate ablations.

**What the contrast changes.** It isolates the meaning of an application, not just what is observed. M0 gets a
sound provability oracle at no cost; W0 gets simulation, with non-terminating self-reference resolved to the
minimax action. So the contrast includes free reasoning power, and a positive result says what a free, sound
prover buys over simulation, not what a realizable source-reading program buys.

Also reported: ρ_enter, and the exits from the top cooperative state split into strict, neutral and other.

## E2. The ratchet: does the support migrate from FairBot to PrudentBot as N grows?

Fable's review proposed that the support migrates toward PrudentBot-like, shadow-immune programs as N grows.

My counter-prediction:
- FairBot and PrudentBot both enter all-D neutrally, at the same ρ ∝ N^(−1/2).
- Their exits are both neutral drift ∝ 1/N, through neutral masses that differ by about 100×.
- So π(PB)/π(FB) tends to an N-independent constant, roughly [μ(PB)/μ(FB)] × [exploitable-neutral(FB) /
  exploitable-neutral(PB)] ≈ 0.04–0.05. The ratio rose from 0.016 at N = 100 to 0.037 at N = 3·10⁴ (n = 8,
  w = 0.3), which reads as an approach to a plateau.

Cells: full modal arm, n = 8, w = 0.3, N ∈ {10⁵, 3·10⁵}.

**Chain-exploration change, for these cells only:** `eager_poly=False`.
- *Why.* At some N the exploration walks a near-neutral polymorphic line one 1/N grid step at a time. These are
  thousands of states holding about 10⁻⁷ of π, each needing slow replicator integrations, and they made cells take
  2–19 hours.
- *What changes.* Polymorphic successors are expanded only through the θ-pruned rounds, when their stationary
  inflow exceeds θ = 10⁻⁶.
- *Verified.* It reproduces all four finished n = 8, w = 0.3 cells (N = 10³, 3·10³, 10⁴, 3·10⁴) exactly, with
  P(C,C), π(FairBot) and π(PrudentBot) identical to four decimals. Runtimes fall from 7,606 s and 15,217 s to
  34 s and 189 s.
- *Not used.* An earlier variant, `eager_top=False`, did not stop the walk and was dropped.

**Additional check.** Each N is also run at θ = 10⁻⁷; π(PB)/π(FB) must agree with θ = 10⁻⁶ to within 5%. The
validation above covered π(FB) and π(PB) as well as P(C,C).

Verdicts:
4. **A plateau, not a ratchet.** π(PB)/π(FB) at N = 3·10⁵ is below 0.06, and the increase from N = 3·10⁴ to 3·10⁵
   is smaller than the increase from 3·10³ to 3·10⁴. Two points cannot establish an asymptote; this verdict is only
   about the trend over this range.
5. **Cooperation keeps rising** [revised after review]. P(C,C) is 0.80 ± 0.05 at N = 10⁵ and 0.86 ± 0.05 at
   3·10⁵ [was: at least 0.85 at 3·10⁵]. `BOX(THEM(THEM))` has N-independent strict invaders at n = 8, so its
   share of the prover family falls. π of each family member is reported.

   *Caveat from review:* my plateau derivation from neutral masses fails for PrudentBot, by 3× and dependent
   on N. The plateau verdict rests on the observed flattening (extrapolated 0.038–0.042), not on that derivation.

*Falsifier of the plateau:* π(PB)/π(FB) at least 0.08 at N = 3·10⁵, more than double its N = 3·10⁴ value of
0.037. That is evidence for continued migration over this range, not proof of an asymptotic ratchet.

## E3. Finite εN: does the modal arm cooperate without spatial structure?

This is the agent-based Moran process (`src/islands.py`) at finite mutation, so it measures approach rates, not
π. PD, w = 0.3, every agent starting all-D unless stated, 2·10⁵ generations, 3 replicates. A generation is I·N
births. Statistics are over the second half of each run. P(C,C) is interaction-weighted within each island and
averaged over islands. Each replicate is reported separately.

Arms:
- modal, n = 6, all four box kinds: 51 classes;
- weak L_6 with X and `ROLE`, for reference: 112 classes.

Configurations:
- **(a) One big island,** no spatial structure: N = 6,400, mutation 10⁻³ per birth (εN = 6.4 per generation).
  Two controls: a cooperative start, with all agents the arm's reciprocator; and mutation 10⁻⁴ per birth. Together
  they separate slow entry from all-D from instability of the cooperative state.
- **(b) 64 islands of 100,** mutation 10⁻³ per birth, mN = 1, payoff-weighted emigration w_g ∈ {0, 10}. These are
  the multilevel settings; the weak arm gave 0.13 at w_g = 0 and 0.75 at w_g = 10.

Expectation for the modal arm on one island [revised after review]:
- *My original mechanism, superseded:* ALLC floods the cooperative population because nothing removes it, giving
  repeated collapses at P(C,C) 0.2–0.6.
- *Fable's correction, which I adopt:* at finite ε a standing D fringe exists, d ≈ εμ_D/w ≈ 1.6·10⁻³. It prunes ALLC
  at a rate of the same order as ALLC's mutational input. The deterministic mutation–selection ODE on the 51-class
  matrix goes to P(C,C) ≈ 0.99, with ALLC pinned at x* = μ_C/(1 + μ_D) ≈ 0.32, from either start. The same ODE for
  the weak arm goes to all-D.
- *How collapses happen instead:* they need a stochastic excursion of ALLC past the invasion threshold
  (R − P)/(T − P) = ½. The OU estimate for the sd of the ALLC share is 0.15 at ε = 10⁻³ and 0.48 at ε = 10⁻⁴. So
  collapses should be rarer at the higher ε, and re-entry is 10× slower at the lower ε.

Verdicts:
6. **Big island** [revised after review]. Modal P(C,C) is 0.6–0.95 at ε = 10⁻³ [was: 0.2–0.6], and lower at
   ε = 10⁻⁴ than at 10⁻³. The weak arm's is below 0.1. The weak arm with a cooperative start is a negative control:
   its ODE goes to all-D.
7. **Islands at w_g = 0** [revised after review]. Modal P(C,C) is at least 0.7 [was: at least 0.3], against the weak
   arm's 0.13: FairBot has no faker.
8. **Islands at w_g = 10:** modal P(C,C) at least 0.75.
9. **The shadow is pinned** [revised after review]. ALLC's share of the whole population in modal big-island runs is
   0.32 ± 0.1 at both ε [was: ALLC share of cooperators above 0.3].

10. **Mixing.** For the modal arm on the big island, the cooperative start and the all-D start agree to within 0.15
    in second-half P(C,C). [Revised after review: the clause that ε = 10⁻⁴ matches 10⁻³ within 0.2 is replaced by
    verdict 6's ordering.]

*Falsifier of "the modal arm cooperates without spatial structure at finite εN":* big-island modal P(C,C) below 0.1.
