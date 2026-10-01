# Review of `predictions/2026-10-01-priced-arm.md` by Fable (Claude subagent), before the run

1. **Exp 3 is foreordained.** A clique world has no strict or neutral exit: ρ(D | clique) ≈ 10⁻⁶⁷ and
   ρ(FairBot | clique) ≈ 10⁻³⁵ at N = 10³. It is the unique closed class, so π(clique) ≈ 1 everywhere.
   - The clique strictly invades `BOX(THEM(THEM))`, at ρ = 0.26.
   - Only hitting times are informative. They should fall like 1/m with mass per spelling, and be
     m-independent with fixed total mass.
   - Report `near_closed`, `absorb_error` and the number of terminal classes.
2. **Exp 2 entry cap is a bug.** A cap of 50 generations loses every success at N ≥ 1,024: 0 successes, 17–20
   undecided, against 18–19 successes with cap 500. Undecided trials were counted as failures, which would
   spuriously fire prediction 5's falsifier.
   - Raise the cap and exclude undecided trials from the denominator.
   - Ladder trials need at least 2·10⁴.
3. **Pricing bookkeeping.**
   - Costs per pair, in units of c: PrudentBot pays 6 against C, and the level-1 provers are taxed one extra
     world.
   - `prov.cost` was indexed by canonical id, not by class: a latent bug.
   - c = 0 reproduces `build(8)` exactly.
4. **Predictions.**
   - *Exp 1 magnitudes:* a family-level three-state estimate gives, at c = 10⁻³, 0.17 / 0.36 / 0.39 / 0.27,
     peaking at 10⁴. At c = 10⁻² it gives 0.14 / 0.14 / 0.02 / 0.004.
   - *Prediction 3:* trivially true, since ALLC is the only strict invader.
   - *Prediction 7:* at c = 0.01 expect 1.0–1.9× the measured neutral; at least 3× only at c = 0.1.
   - *Prediction 4:* holds, but because μ(PrudentBot) = 1.4·10⁻⁶.
5. **Controls.**
   - A depth-only price, without the atom multiplier. The PrudentBot → FairBot rung exists only because of the
     multiplier.
   - Exp 3 without `BOX(THEM(THEM))`.
   - Report entry at the family level.
6. **Alternative.** The proxy inverts real proof cost: FairBot pays more against D than against itself. A
   realistic proxy shrinks the entry barrier. Mechanism (b) is robust to the proxy; mechanism (a) is not.
7. **Beyond.** Under atom pricing no universal cooperator escapes the ladder: every cheaper subset-of-atoms
   program passes the resident's test. The escape is a **lazy prover**:
   - it reads off a reply to constants and to exact copies at cost 0, and runs the Löbian check only otherwise;
   - its payoffs against D, C and itself equal the free FairBot's, so entry is neutral and ALLC is a neutral
     shadow;
   - it is universal, and meets both conditions of §9.2 under pricing.

   This re-opens the "CliqueBot-shaped short-circuit" objection of the REJECTED Levin entry: the short-circuit
   is on cost, not on cooperation.
