# Review of `predictions/2026-09-30-modal-arm.md` by Fable (Claude subagent), post-hoc pilot

**1. Design flaws / confounds**
- **Falsifier 2 cannot fire.** "No strict invader of all-FairBot" is a theorem of soundness. FairBot
  cooperates with q only if PA proves q(FB) = C, so q really does cooperate. The check tests the evaluator,
  not the dynamics. Replace it with a quantitative falsifier: the fitted exponent of π(coop)/π(all-D)
  against N falling outside [0.4, 0.6].
- **Verdict 6 confounds the observation channel with the language.** The modal arm has no X and no `ROLE`,
  so μ(C), μ(D) and μ of the 3-node reciprocator differ from the weak arm's. Run the weak arm with X and
  `ROLE` stripped at the same n, or compare exponents only.
- **Exits are counted from all-FairBot only.** That is right for the ε→0 chain, but it cannot see
  `BOXD1(THEM(^D))`. That class has size 4 and μ = 1.4e-3, about 1,000× PrudentBot's. FairBot trusts it, it
  strictly invades any FairBot/ALLC mixture, and it cooperates with D, since D provably defects on D. It is
  a magnet for D. State that the claim holds for ε → 0 only.
- **`src/modal.py`: no semantic or prior bug found.** World-0 vacuity makes the PA-level `BOXD` of any boxed
  program unprovable. So `BOXD` is nearly inert and only inflates a(s), a uniform bits penalty that is
  harmless for ratios. The test defaults to n = 5, while the brief says n = 6.

**2. Predictions that are wrong**
- **Verdict 1 magnitudes.** At n = 6 there are three unfakeable neutral entrants of equal mass into all-D.
  Total entry mass is about 4.6× μ(FairBot). The observed values are 0.19 / 0.38 / 0.62 / 0.73. Monotonicity
  holds, and the exponent of the cooperative-to-D ratio is about 0.43. Score as failed on magnitude.
- **Verdict 5.** π(PrudentBot) is 0.0101 and 0.0127, so it narrowly fails. π(PB)/π(FB) is roughly
  [μ(PB)/μ(FB)] × [exploitable(FB)/exploitable(PB)], about 0.04, which matches.
- **Unlisted.** `BOX(THEM(THEM))` has no strict invaders at n = 6 but 12 at n = 8. It is fakeable, which is
  the weak arm's faker law operating inside the modal arm.

**3. Missing controls / cheap additions**
- N = 10⁵ and 3·10⁵ at n = 6.
- A PA-only control, without `BOX1`/`BOXD1`.
- Per-class entry and exit, to test π_i/π_D ≈ μ_i·ρ_i(N)·N/μ(exploitable neutrals of i).
- One finite-εN agent-based cell, to probe the `BOXD1(THEM(^D))` interception.
- A prior uniform over behaviours: it should change the constant, not the exponent.

**4. Alternative explanations**
- Efficiency is built in. A free, sound, self-referential oracle removes grounding cost and fakeability by
  construction, so the content is the exponent and the constant.
- ρ(FairBot | all-D) ∝ √w.

**5. Ideas beyond this experiment**
- **A ratchet.** The shadow route that spoils FairBot leads toward shadow-immune programs. PrudentBot's
  exploitable neutral mass is 100× smaller. Predict that the lim_N support migrates from FairBot toward
  PrudentBot-like classes as N grows, with no peak in total cooperation.
