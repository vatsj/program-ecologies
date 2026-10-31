# Where the unequal basin of the length-prior arms comes from (notes, 2026-10-31)

Spec `specs/2026-10-31-unequal-basin.md` (queue 70; the RS: "1 sgtm btw"; reviewed by gemini-4-argon, then gpt-6.1-sol in
`--mode amended`, both folded; the folded spec is the authority). Follows `notes/many-islands.md` (arms L, M, R; the
kernel; the symmetric chain), `notes/many-islands-t.md` (the exact ODE) and `notes/forfeit-pricing.md` (A_f). §1 is
written by hand before any code of this experiment and before any counted cell; §2 (deviations, choices where the spec
is silent, costs) is appended as they arise.

## 1. Hand analysis, before code

### 1.0 Disclosure about order

Nothing of this experiment had been run when §1 was written. I read the spec and both reviews, `src/dollar3.py` (the
grammar, `Lang`, `Slots`, the two evaluators `_weak_into` and `_modal_into`), `src/stable_sets.py` (`seed_law`,
`arm_data`, `Tables`), `src/many_islands.py` (`Arm`, `jl`, `pfix`, `island_run`, `permute_support`, `chain_run`),
`src/many_islands_run.py` (`build_pool`, `symmetrize`, `resample_job`), `src/many_islands_t_ode.py` (the ODE) and the
RESULTS sections "Islands to infinity before time" and "Arm T under islands to infinity before time". Two stored summary
facts were looked at, both published: the diversity records of the stored chains (distinct programs per slot and Σq², in
`runs/many_islands/chain_L_A0_p0.json` and `sym_L_A0_symtiltU.json`) and the pool wall time (1,930 s per 16,384-island
pool). No scratch query was run on this experiment's own objects and every number below is from pencil arithmetic that
`tests/test_unequal_basin.py` and the validations check afterwards, never the other way round.

### 1.1 What L and M are, from the files

Both arms use `dollar3.build('weak', 6)`: one grammar, one prior, 1,305 canonical functions per slot, absolute slot
labels (`Slots`), the same seed law in every slot (`stable_sets.seed_law('L', s)`: μ, the length prior of `Lang.canon`).

- **Grammar at n ≤ 6.** A ::= a (nine constants, 1 node) | if(B, A, A), B ::= BOX(THEM_j = a) | not B | and B B | or B B.
  The atom costs 3 nodes, `not` costs 1 more, `and`/`or` cost 1 plus both operands, so the smallest conditional is
  `if(atom, a, a')` at size 1 + 3 + 1 + 1 = 6 and **every conditional of the n ≤ 6 arm has exactly one atom and size
  exactly 6** (`not` would give size 7). Atoms: j one of the owner's two others, a one of j's nine actions, level 0 only
  in these arms: 18 atoms. Spellings: 18 × 9 × 9 = 1,458. The ones with equal branches (162) reduce to constants. The
  rest are the 18 × 72 = **1,296 canonical single-atom conditionals** (x on the true branch, z ≠ x on the false
  branch), and 9 + 1,296 = 1,305, the spec's count.
- **Consequence for the spec's families.** The spec's syntactic families C / A1 / A2s / A2x have **A2s and A2x
  empty**: no program of the n ≤ 6 grammar has two essential atoms. A1 is the whole set of 1,296 conditionals. So
  prediction 3 ("all conditionals removed") and prediction 4's first clause ("A1 removed") are the same ablation, and
  the second clause ("removing A2s or A2x moves u\* by less than 0.1") is vacuous (removing an empty family is a
  no-op). I register this before any counted cell; the informative syntactic split is a finer partition of A1 (§1.4).
- **Prior mass.** μ(size 1) = 2^−(log₂ 9 + 0 + 1) = 1/18 per constant, 0.5 in all. Each size-6 spelling has
  2^−(log₂ 1458 + 2 log₂ 6 + 1) = 1/(2 · 1458 · 36) = 9.53 × 10⁻⁶; all 1,458 spellings together 0.01389. The total is
  0.51389. So a canonical conditional has seed mass 9.53 × 10⁻⁶ / 0.51389 = **1.85 × 10⁻⁵**, the 1,296 together
  **0.0240**; the constants hold 0.976 (the direct 0.973 plus 0.003 from the 162 collapsed spellings), 0.108 each.
  Every conditional is at the same mass. Conditionals are 2.4% of every slot at founding.
- **Evaluators.** *L (weak):* least fixed point from bottom; an atom reading a bottom value leaves its slot bottom; a slot
  still bottom at the fixed point plays (ALL, 2/3), local action 8. A conditional in slot s reads slot j's action in this
  encounter; if j's program is a constant, or a conditional that reads the third slot k and k is a constant, the read
  resolves. If s reads j and j reads s (or the three read in a cycle), both are bottom: **divergence**, both play the
  null action. The stored joint code (`val[0]·81 + val[1]·9 + val[2]`, 729 values) forgets which slots diverged, so the
  charge A_f cannot be applied through it: the DSL needs a divergence mask next to the code (§1.5). *M (modalPA):*
  stable actions on the linear GL chain with the PA box; a mutual reader pair is resolved by Löb instead of
  diverging (a FairBot-style pair cooperates), and `_modal_into` always converges (the engineer checks it on the
  whole support). So M has no charge and no divergence, and M differs from L exactly on triples with a mutual reading
  edge.
- **Which triples have a reading edge.** A triple has a reading edge only if two or more of its three programs are
  conditionals reading each other (or three in a cycle). With conditionals at 2.4% per slot, two conditionals appear in
  one island with probability about 3 × 0.024² ≈ 1.7 × 10⁻³, and a mutual edge in a small fraction of those. This is the
  only place L and M can differ, and it is also the only place P_fail can matter. Hand estimate: the settled
  post-anneal law has mutual-edge mass below 10⁻⁴ and the charge moves nothing at the natural start (prediction 7 looks
  safe; the exceptions would be programs that spread because of the edge).

### 1.2 Units: what w = 0.3 acts on

Same as `notes/many-islands-t.md` §1.1. `Tables.PAY` is in dollars (outcome sixths / 6): a fair pair pays ½ each, an
unequal pair ⅔ and ⅓; w = 0.3 acts on dollars; `pfix(dpay, 100, 0.3)`. A sixth is 0.1667 dollars, wΔ = 0.05, so with
N = 100 (ρ = e^(wΔ)):

| payoff change of the migrant | wΔ | P_fix | units of neutral (0.01) |
|---|---|---|---|
| +1/6 | +0.05 | (1 − e^−0.05)/(1 − e^−5) = 0.04877/0.99326 = 0.0491 | 4.9 |
| +1/3 | +0.10 | 0.09516/0.99995 = 0.0952 | 9.5 |
| 0 | 0 | 0.01 | 1 |
| −1/6 | −0.05 | 0.04877 · e^−4.95/(1 − e^−5) = 0.04877 · 0.00708/0.99326 = 3.5 × 10⁻⁴ | 0.035 |
| −1/3 | −0.10 | 0.09516 · e^−9.9/0.99995 = 4.7 × 10⁻⁶ | 5 × 10⁻⁴ |
| −½ | −0.15 | 0.1393 · e^−14.85 = 5 × 10⁻⁸ | 5 × 10⁻⁶ |

P_fail = 0.1 dollars is wP_fail = 0.03: a divergent slot is charged 0.6 of a sixth. In integer 30ths of a dollar (the
unit I will use for the payoff lattice) a sixth is 5 and the charge is 3, so payoff differences are integers and
`pfix` is a table of integer differences. Neutral moves (fixation 0.01 per migrant) are the only way to leave a state
in which all moves are weakly deleterious, and a move that costs a sixth is 28 times rarer than neutral.

### 1.3 The key triples and the constants-only rescue

Write a triple (a₀, a₁, a₂); the unequal pair is {H, Lw} with H demanding ⅔ of Lw, Lw naming H at ⅓, and the third
slot E excluded, payoff 0. By S₃ there are six orientations; take H = 0, Lw = 1, E = 2: (1,⅔), (0,⅓), E. Payoffs
(⅔, ⅓, 0).

**With constants only** every single-migrant move out of this triple is one of:
1. *Lw rescues itself.* Lw → (2, ½) (a constant naming E at ½). It pays ½ iff E names slot 1 with demand ≤ ½ (E =
   (1,⅓) or (1,½)); else Lw gets 0. When E offers, Δ = +1/6 and P_fix = 0.049; when not, Δ = −⅓, 4.7 × 10⁻⁶. So the
   rescue needs the excluded slot to offer ½ or ⅓ to the underpaid member, and then it is a selected move.
2. *E moves neutrally.* E has payoff 0 whatever it does while Lw plays (0,⅓), unless E names slot 1 and slot 1 names
   E (no). So E drifts at fixation 0.01 among all programs in the donor marginal. Drift to (1,½) or (1,⅓) enables move 1.
3. *H concedes.* H → (1,½) pays ½ instead of ⅔ (against Lw = (0,⅓) the pair {0,1} is wasteful but pays H ½): Δ = −1/6,
   0.035 of neutral. Alternatively H → (2,·) or H → ALL pays 0: Δ = −⅔.
4. *Lw demands more.* Lw → (0,½): pair sum 7/6 > 1, Lw gets 0.
5. *Lw → (0,⅔)*: no pair.

So with constants the way out of U is "E offers (drift) then Lw switches (selected)", or the 0.035-of-neutral concession by
H. This is the same table as arm T's constants (V1 checks the equality). Arm T's exact ODE reached V\* = 1 from every
start including the unequal tilt, in time of order 10³–10⁴ events per island. The mean-field timescale for a constants-only
U island to leave is 1/(Σ over rescue paths): E drifts to an offering constant at rate ≈ (donor mass of offering
constants in slot E, about 2/9) × 0.01 per slot-E event, then Lw's rescue move at the donor mass of (2,½) in slot 1
(≈ 1/9) × 0.049: of order 10⁻³ × 5 × 10⁻³ per event, two-step; hence a slow tail of order 10³–10⁴ events, as arm T found.

**Entering U from V\*** with constants only: from the fair pair F0 = ((1,½), (0,½), E), a H-migrant (1,⅔) meets Lw =
(0,½): pair sum 7/6 > 1, H gets 0. Deleterious, 5 × 10⁻⁸ of neutral. A Lw-migrant (0,⅓) meets H = (1,½): the pair {0,1}
is wasteful, Lw gets ⅓ instead of ½: −1/6, 0.035 of neutral. A neutral move happens in E only. So **constants-only
fair islands are immune to unequal invaders** and the fair pair is leaving only through W (waste), then back; the
instability of the symmetric state in arm T was among the three fair pairs, not toward U.

### 1.4 Which program shapes could carry an unequal basin

An unequal basin is a state of the donor marginals q in which the flux into U is not below the flux out. The flux into U
needs a **soft resident** in a pair slot: a program that, when its partner presses a demand of ⅔, pays ⅓ instead of
dropping to 0. A constant is never soft against ⅔ unless it is already the (0,⅓) victim. A conditional resident can be
soft *and* fair: Lw′ = `if(THEM_0 = (1,⅔), (0,⅓), (0,½))` pays ½ in a fair pair and ⅓ against a bully, so in F0 it has
the same payoff as the constant (0,½) (neutral entry, 0.01), and then a bully migrant (1,⅔) into slot 0 earns ⅔
against it (selected, +1/6, 4.9× neutral). So:

- **Soft-yielder family (my hand candidate for the carrier).** A1 programs whose atom reads the *pair partner's* action
  "names me at ⅔" and whose true branch names that partner at ⅓. Per slot and per partner there is one atom and
  the false branch is any of eight actions: 2 partners × 8 false branches = 16 programs per slot, of which the
  false branch (j,½) is the fair-compatible one. All have seed mass 1.85 × 10⁻⁵ each, 3 × 10⁻⁴ for the family.
  Their role: a bridge **into** U (neutral entry in F, then a constant bully), i.e. they open the V\* → U flux that
  constants lack.
- **Blocking E programs.** E conditionals reading slot 1 (`if(THEM_1 = (2,½), (1,z), …)`): the rescue of 1.3 is
  blocked iff E's reply to the switch is not an offer ≤ ½ to slot 1. For a conditional, the reply is its true-branch
  action if the atom is "slot 1 plays (2,½)". An E conditional with true-branch (1,⅔) or (anything not naming 1)
  blocks, and is neutral while slot 1 plays (0,⅓). So the donor marginal of E in a U-dominated population decides
  the rescue supply; the length prior puts the same mass on every canonical conditional, so supply of blockers and
  offerers is balanced in the prior, differing from the constants-only supply (2/9 offering) by the conditional
  share: block and offer both move by at most the 2.4% conditional mass. **On the prior's own mass, blocking by
  conditional E programs cannot be a first-order effect** (it changes the rescue supply by at most 2.4% of its
  value); a basin must come from enrichment during the dynamics (U triples where conditional residents are
  over-represented), which is a question of the ODE's feedback, not of the prior's mass.
- **Retaliating H.** H's reply to the switch does not enter Lw's payoff after Lw leaves the pair, so retaliation by H
  cannot block move 1; it can only change H's own concession (move 3). The RE's second falsifier clause ("blocked
  rescue is blocked by retaliation from the high demander") is therefore, by the payoff algebra, not a way to block
  move 1; it could only arise in the two-step paths where Lw first fails to switch because H punishes the pair formed
  by the *old* partner (not a feature of the single-atom grammar here).

My hand prediction of the carrier, with the confidence it deserves: **the soft yielders in the pair slots open the
V\* → U flux and are what the attribution will rank first**, and the unequal basin exists, if at all, as a flux
balance between that inflow and the 1.3 rescue (which is nearly the same as in arm T), not as a block of the rescue.
That is closer to gemini-4-argon's counter to prediction 5 (pair slots) than to the RE's (excluded slot), but for a
different reason: argon puts the obstruction in the rescue; I put it in the inflow. The data will rank them.

Also noted before any run: the U-tilt keeps within-class frequencies of the post-anneal law, and conditionals may be
enriched inside the unequal class at founding (a founding scramble selects soft yielders into U), so the 0.6 tilt could
inflate yielders' donor share (the spec's tilt check). The fair tilt does the same for fair residents.

### 1.5 The class count, the stop rule, and what to do about it

**Lumping is vacuous here.** The spec merges two programs of slot s if every pair of programs of the other two slots
gives the same joint code and divergence vector. The supports contain all nine constants of every slot (added by the
spec). A conditional y = if(THEM_j = a, x, z) played against the nine constants of slot j and any program of the third
slot returns x when the constant is a and z otherwise; so y's behaviour determines (j, a, x, z). Two canonical
conditionals are therefore always distinguished, and no conditional equals a constant (x ≠ z). **C per slot equals the
support size**, no merge at all, in L and in M. The union support: each (type, slot) pair is founded and settled
about 1.1 times in the 49,152 islands (4,400 conditional settlements over 3 × 1,296 pairs), and the S₃-union takes six
images of each, so I expect the S₃-union to contain **at least 1,250 of the 1,296 conditionals per slot** (E1 below).
A single 16,384-island pool has about 350 distinct programs per slot (the stored diversity record at 1 event: 348 / 313
/ 324 in L pool 0).

**The dense exact object does not fit.** With C ≈ 1,300 per slot there are C³ ≈ 2.2 × 10⁹ triples, 17 GB for one
vector of doubles, with 16 GB of memory in total and a field that needs about ten vectors. The kernel can be applied in
O(C³) rather than O(C⁴) (a migrant's payoff takes at most 24 distinct integer values in a fibre of the context, so the
Moran inflow is a sum over payoff levels), but the state itself is the obstacle: it is the spec's stop condition,
"if even that is infeasible, stop and report the class counts before running anything counted".

What I will do under that rule is stated in §2 when the count is measured. The candidate I pre-register here is a
**reflecting truncation in the number of conditionals per island** (an island may hold at most m conditional programs;
a migration that would give it m + 1 is a null event, mass conserved, and the rate of such blocked events is reported
as the truncation's leak). m = 1 has 729 + 3 × 1,296 × 81 = 316,000 states and m = 2 about 4.6 × 10⁷ (7.6 × 10⁶ up to
S₃); at the seed 93% of the mass has no conditional, 6.7% has one and 0.2% two or more, so I expect m = 2 to be close to
exact for the first-order question of what a rare conditional does inside an otherwise-constant island, and
the m = 1 / m = 2 comparison is the convergence check in m (E3). The truncation is a different object from the spec's
and is disclosed as such; the Monte Carlo of V3 (full dynamics at 10², 10³, 3·10³ events) bounds its error from outside.

### 1.6 Expected support at the endpoint, and what the Jacobian can say

At ε = 0 no program can be created: a program is either in the empirical start's support or absent forever. The
constants-only endpoint of arm T was a single fair pair held by one constant per slot at positive mass for the
others, with all eigenvalues zero within 10⁻⁶ on the support (neutral directions along the faces). Here I expect the
same for the V\*-dominated endpoint (mass concentrated on few constants, 1,296 conditionals decaying), and for a
U-dominated endpoint, if it exists, one that is not an asymptotic attractor either: any U island with an offering E
constant in the donor marginal leaks into V\* at the rescue rate above, so the U state is **metastable** unless the
offering mass in E's marginal is exactly zero. A metastable U endpoint with a lifetime of 10⁵–10⁷ events is the most
likely finding if the stored bistability is reproduced, and I register that "basin" will be reported as metastable
when the residual falls below the stated tolerance only at the horizon.

### 1.7 Prediction of the charge's role

P_fail 0.1 charges only divergent slots. Divergence needs a mutual reading edge between two conditionals (§1.1), and
mutual edges are charged −0.1 per divergent slot and pay 0 otherwise: strongly selected against. They exist at the
founding and early annealing and are washed out; at the settled start they are a thousandth or less of the mass.
Prediction: |Δu\*| from the charge is below 0.05 (the RE's 7), the post-anneal V\* moves by less than 0.01, and the L
and M cells differ only through mutual edges, so L and M natural starts are close until a reading edge matters (they
differ in the stored chains for later reasons: in M a mutual edge between two Löbian conditionals is not an obstacle,
and M's U collapse at 3·10⁴ events needs a program family that cooperates only under provability; that is what the
attribution will show).
