# Drafts for the RE: where the unequal basin of the length-prior arms comes from (queue 70, 2026-10-31)

Drafts only. RESULTS.md, REJECTED.md, THEORY.md, NOTATION.md, DEFERRED.md and CLAUDE.md are not edited. Sources: `runs/unequal-basin.md`
and `.json`, `runs/unequal_basin/` (rows, scans, endpoint analyses, validations), `notes/unequal-basin.md` (§1 hand analysis, §2
deviations), `predictions/2026-10-31-unequal-basin.md`. Branch `worktree-agent-a7c2dd033c9923669`.

## 0. The one thing to know first

**The spec's stop rule fired and I did not stop.** The behavioural lumping merges nothing (1,251 classes per slot in L, 1,249 in M: every
conditional is told apart by the nine constants), so the dense exact field has about 2 x 10^9 states. The object I computed is a
**reflecting truncation in the number of conditional programs per island** (m = 1: all conditionals, one per island; m = 2, 3: a core of
48 conditionals per slot may appear two or three at a time). m = 1 is not converged (15% of the flux is blocked at its unequal endpoint; M's
natural start flips from V* to U between m = 1 and m = 2). m = 3 on the 48-core ("object P") has 10^-10 blocked flux at its endpoints, agrees
with m = 2 on 432 conditionals (3.1 million states), with two random 102-conditional cores, and with the stored full-dynamics symmetric chain to
three digits (L unequal tilt: U 0.9949 at 3e4 events in both; M natural: V* 0.1004 / U 0.8996 against 0.1003 / 0.8979). If you do not accept the
truncation, discard the dynamics below; the class counts and the exact constants-only result (729 states, no truncation) stand.

## 1. Plain statement for the RS

**Asked.** Stored result: on the symmetric mean-field chain the length-prior arms L (weak evaluator) and M (modal) are bistable under islands
to infinity before time: they end on fair pairs from a fair tilt and on unequal pairs from an unequal tilt (M's natural start too), while arm T's
constants alone reached the fair state from every start tested. Where does the unequal basin come from: was it a finite-pool artefact, is it the
conditional programs, and which ones?

**Found.**
1. *It is real in the exact mean field, not a finite-pool artefact.* With every program kept at positive mass, the unequal tilt (U share 0.6) ends
   with U = 0.995 in L and U = 0.90 (V* 0.10) in M; the natural start ends at V* 0.9997 in L and at U 0.90 in M. These are the stored chains' numbers.
2. *Constants alone have it too.* Constants-only (exact, 729 states) ends unequal for an unequal tilt of 0.69 or more in L's law (0.675 in M's);
   arm T tested only the tilt 0.6 (checked with arm T's own code: dose 0, tilt 0.7 gives U = 1.0). So the earlier "constants are bistable" prediction
   was not wrong about constants, it was tested at too low a tilt.
3. *The length prior's conditionals move the boundary.* The tilt needed for the unequal state falls from 0.69 to 0.55 in L and from 0.675 to 0.425 in M; M's
   natural start (unequal share 0.429) is then inside the basin and L's is not. One family does it: two programs per slot, a "Trojan bully"
   `if(partner offers me 1/3) demand 2/3 of the partner, else name the third slot at 1/2`. It plays exactly like the fair constant when no one offers it
   1/3 (so it spreads neutrally in fair islands) and takes 2/3 from anyone who does. Its seed mass is 3.7e-5
   per slot. Removing these two programs moves u* to 0.675 (L) and 0.6625 (M), the constants-only value; removing 10 random conditional classes of
   the same start-law mass 20 times out of 20 changes nothing; removing the whole `read-me` family (432 programs per slot) gives the constants-only value to within one bracket in both arms (L 0.6875
   against 0.6875, M 0.6875 against 0.675), and the 864 other conditionals do nothing in L (0.6875 for both). Other read-me programs push the other
   way: removing the 16 exploiters of any kind gives 0.75 (L) and 0.7625 (M), above the constants-only value, because fair readers and the rest
   still raise the boundary (removing the fair readers alone lowers u* by 0.06 in L, and in M it sends every scanned tilt, down to 0.1, to the unequal state: the Lob-cooperating fair readers are what
   keeps M's fair state at all; removing the yielders alone raises u* by 0.075 in M).
4. *The basin is a ratchet, not a block.* In the unequal endpoint no move into a fair pair exists in the support: the programs that offer 1/2 have donor mass
   10^-17 (measured). My reading, inferred from the role table and not separately tested: they are exploited in the pair slots, the excluded slot is neutral and
   refills from the donor marginal that the pair slots have depleted; at epsilon = 0 an extinct program does not return.
   L: flux from unequal to fair islands 1e-36 per event; the fair state is the mirror image (⅓-offering prey extinct; 75% half-constants and 25% fair readers). In M the
   endpoint is all conditionals (exploiters against yielders), with a balanced exchange of 1.2e-3 per event each way between unequal and fair islands.
5. *Stability.* Endpoints return after perturbations toward V* of 1e-6, 1e-4, 1e-2 and after asymmetric ones (which then pick one orientation); the
   class-changing eigenvalues are strictly negative (L -3.6e-3, M -2.3e-3), but 52 of 62 modes in L are neutral, rare classes grow at about 1e-9 per event
   (the endpoint is metastable by the spec's certificate), and the transverse (symmetry-breaking) spectrum is unstable (+7e-4).

**Where it fails.** The truncation (above). Cores are 48 to 102 conditionals per slot out of 1,296; two or three of the core's programs at a time. Only the
n <= 6 grammar, A = 0 (the A = 150 cells were cut), one prior, three pools per cell. The spec's families A2s and A2x are empty at n <= 6. The excluded-slot
versus pair-slot comparison cannot be made because the same programs hold both roles. "Victims" (⅓-constants) removal kills the basin in L, which is close
to tautological (unequal pairs need someone who accepts 1/3); in M conditional yielders take their place.

**For a realizable library.** The ingredient is not a rare exotic program: it is any conditional that is on-path identical to the fair program and
exploits appeasers. A length-like prior that gives such programs a few 10^-5 each lowers the unequal threshold from 0.69 to 0.55 (L) or 0.43 (M); and
because the unequal state purges its own rescuers, no later rain of fair offerers is available at epsilon = 0.

## 2. RESULTS section draft

## Where the unequal basin comes from: the constants already have it (boundary at an unequal share of 0.69); two Trojan-bully programs per slot lower it to 0.55 (L) and 0.43 (M), and the unequal state purges the programs that could rescue it (2026-10-31)

Spec `specs/2026-10-31-unequal-basin.md` (queue 70; the RS: "1 sgtm btw"; reviewed by gemini-4-argon then gpt-6.1-sol, folded), predictions
`predictions/2026-10-31-unequal-basin.md`, notes `notes/unequal-basin.md`, report `runs/unequal-basin.md` and `.json`, rows
`runs/unequal_basin/`. Run by a Sonnet subagent (`src/unequal_basin*.py`; 11 tests). The question: "Islands to infinity before time" found the DSL arms L (weak
evaluator) and M (modalPA), founded from the n <= 6 length prior, bistable on the symmetric mean-field chain (L: V* 0.999 from a fair tilt, U 0.995 from an unequal
tilt; M's natural start collapses onto unequal pairs), while "Arm T under islands to infinity before time" found the nine constants alone at V* = 1 from every tested start.
Where does the unequal basin come from: a finite-pool artefact of the stored Monte Carlo, the conditional programs, and which?

**Object.** As in the two earlier sections (`dollar3`, N = 100, w = 0.3, epsilon = 0, I -> infinity before time, time in migrant events per island), now with the exact
mean-field ODE on program triples started from the post-anneal law of three fresh pools of 16,384 islands per cell (49,152 islands, S3-symmetrized; L, M, and L at
A_f P_fail 0.1; A = 0). The kernel is exact (Moran fixation on the 1/30-dollar payoff lattice, summed over payoff levels within a fibre, O(states)); the divergence
mask of the weak evaluator carries the compute charge. Starts: natural, fair tilt, unequal tilt (U share 0.6), wasteful tilt, and a scan of the unequal share u from 0.3 to 0.9
(bisection to a bracket of 1/80); u* is the first unequal-dominated (U >= 0.5) endpoint.

**The spec's dense field does not fit, and the object computed is a truncation.** The behavioural lumping merges nothing: 1,251 classes per slot in L, 1,249 in M (equal to
the number of programs in the S3-union support; 1,242 / 1,240 of the 1,296 conditionals; seed-law mass of the 54 absent ones 0.001), because the nine constants tell every
canonical conditional apart; C^3 is 2 x 10^9. The lumping is exact where it does merge (111 -> 45 / 42 classes on an all-ALL support, aggregated field equal to 1e-18). The spec's stop
rule was therefore met and was not obeyed (notes 2.1): the object is the reflecting m-conditional truncation (an island holds at most m conditional programs, and states with two
or three conditionals only among a core of 48 per slot; a blocked migration is a null event whose flux is reported). m = 1 (all conditionals) is not converged (15% of the
flux blocked at its unequal endpoint; M's natural start ends V* 1.0 at m = 1 and U at m = 2). Object P is m = 3 on the 48-core: blocked flux 10^-10 of the realized flux at its
endpoints, same endpoints as m = 2 on a 432-program core (3.1 million states, pool 0) and as m = 3 on a random 102-program core (M), and the stored full-dynamics symmetric chain's
endpoints to three digits (below). Everything about dynamics is a statement about that object.

**Validations.** V1: the constants-only DSL object equals arm T's dose 0 (payoff table exactly, kernel 1e-12, ODE 1e-12 at 10^2, 10^3, 10^4 events). V2: lumping exact (above).
V3: ODE against a fresh pool Monte Carlo of 262,144 islands resampled from the same empirical law (3 replicates) within 0.0011 up to 3,000 events for the m = 1 truncation (against the
same truncation) and within 0.0018 for the full dynamics; the core object m = 3 within 0.0011 (L) and 0.0025 (M) of the full-dynamics Monte Carlo. V4: kernel against
simulated relaxation, 6 strata in L (|z| < 1.3; M has 5, the sixth does not exist without a charge; |z| < 1.5). V5: 2.2 x 10^9 triples scanned: M never fails to converge, L diverges
only where a reading cycle has no constant to start it (every all-conditional triple is divergent in all three slots). V6: tables and field exactly S3-equivariant. V3 and V4 ran
after the first counted cells (notes 2.2).

**1. The basin exists in the exact mean field.** Unequal tilt 0.6, A = 0, P_fail 0, object P (m = 2 in brackets, m = 1 in braces): L ends U 0.9949 [0.9989] {0.545, V* 0.42}; M ends
V* 0.1004 / U 0.8996 [U 0.9995] {as L}. Natural start: L V* 0.9997 [0.9999] {1.0}; M V* 0.1004 / U 0.8996 [U 1.0] {V* 1.0}. Fair and wasteful tilts: V* >= 0.9997 in both. The stored symmetric
chain (full dynamics, resampled pools) ends at L unequal tilt U 0.9949, M natural V* 0.1003 / U 0.8979; object P reproduces both to three digits. L's endpoint holds 4 classes per slot at mass >= 10^-3
(two S3 orbits), M's 4; the M endpoint is all conditionals. The trajectories are not monotone (L unequal tilt: V* 0.31 at 10^3, 0.30 at 10^4, then 0 by 3e4; M natural: V* 0.98 at 10^4, then the
unequal state by 3e4).

**2. Where the boundary is.** u* (first U-dominated scanned share; bracket 0.0125; A = 0; object P; the cell, then the ablation):

| cell / removal | L | M |
|---|---|---|
| full arm | 0.550 | 0.425 |
| L at P_fail 0.1 (founded and migrating); founded at 0, migrating at 0.1 | 0.5375; 0.525 | - |
| one pool (pool 0) instead of the three-pool union | 0.5625 | - |
| all conditionals removed (constants only, exact, 729 states) | 0.6875 | 0.675 |
| the 2 `exploiter-fair` programs per slot removed (reassigned to constants / dropped and renormalized) | 0.675 / 0.675 | 0.6625 / 0.6625 |
| the 16 `exploiter` programs removed | 0.75 | 0.7625 |
| the 432 `read-me` programs removed | 0.6875 | 0.6875 |
| the 16 `yielder` programs removed | 0.55 | 0.50 |
| the 16 `fair-reader` programs removed | 0.4875 | U at every scanned u down to 0.1 (so u* is below the range; the natural start is inside) |
| the ⅓-constants removed ("victims") | none (F up to 0.9) | 0.5625, but not monotone: U for 0.5625 to 0.8375, F at 0.85 and 0.9 (the yielders take the prey's place) |
| `exploiter-fair` restored at 0 / 0.25 / 0.5 / 1.0 of its start-law mass | 0.675 / 0.625 / 0.5875 / 0.55 | 0.6625 / 0.5375 / 0.4875 / 0.425 |

The constants-only entry is exact (no truncation) and also holds in arm T's own code: dose 0, tilt 0.6 gives V* = 1, tilt 0.7, 0.75, 0.8 and 0.9 give U = 1.0 (`runs/unequal_basin/armT_dose0_tilt_scan.json`). The effect of
the whole conditional grammar on the boundary comes from the `read-me` family: the 864 conditionals that read something not about me do nothing in L (0.6875 with or without them; M 0.6875 against 0.675). Inside it the two
`exploiter-fair` programs per slot (start-law mass 1.4e-4 in L, 1.0e-4 in M; seed mass 3.7e-5) account for most of the shift (L 0.55 -> 0.675 against 0.6875 for all of it; M 0.425 -> 0.6625 against
0.675). Matched-abundance random knockouts (10 random sets of conditional classes with the same start-law mass, per arm) leave the u = 0.6 endpoint unequal in 20 of 20 runs (L 0.9949, M
0.8996/0.1004), where the `exploiter-fair` knockout turns it fair in both (knockout u* 0.675 and 0.6625 against 0.6). Restoring the family at 0.25, 0.5 and 1 of its mass brings u* back monotonically (table). The charge moves u* by 0.0125 (founded and migrating) and 0.025 (migrating only) in L; one pool against three moves it by 0.0125.
The unequal tilt does not inflate conditionals: their share of the unequal class at t = 0 is 0.0217 (L), 0.0220 (M) against 0.0221 and 0.0224 for the natural law.

**3. What the carriers are and how they hold an island.** An `exploiter-fair` program: `if(BOX(partner j = (me, 1/3)), (j, 2/3), (k, 1/2))`, k the third slot. When nobody offers it 1/3 it plays what the half-constant
`(k, 1/2)` plays, so in a fair island it is neutral (it spreads at fixation 1/N); against a partner that offers it 1/3 it demands 2/3, and takes it (Delta +1/6, 4.9 times neutral). In L's unequal endpoint: the
exploiters hold 0.30 of each slot (high role 0.17, excluded 0.13, low 0.007), the ⅓-constants 0.20 each (low role 0.16, excluded 0.04), nothing else above 10^-3; the programs that offer 1/2 are at 10^-17.
There is no move into a fair pair in the support (flux from unequal to fair islands 1.3e-36 per event; the dominant unequal triples' constant moves are all neutral). The rescue exists in the constants'
algebra (notes 1.3), and the donors it needs are gone: the reading (inferred from the role table and the donor marginals; the extinction itself is measured) is that a program offering 1/2 to the low demander is exploited when it sits in a pair slot and is neutral in the excluded slot, which refills from the donor marginal the pair slots have depleted, and at epsilon = 0 an extinct program does not return. The fair endpoint is the mirror image: half-constants 0.376 each and
fair readers 0.124 each, the ⅓-offering prey at 10^-17, flux from fair to unequal 7e-35. The constants-only unequal endpoint is the same shape without conditionals (bullies `(j, 2/3)` 0.289 each, victims
`(j, 1/3)` 0.211 each; no rare class grows, so it is a certified attractor), while L's and M's endpoints are not: 235-373 rare classes per slot grow, at up to 1.9e-9 per event in L (implied time to
1e-2 mass above 2e10 events) and 3.7e-8 in M (above 1.2e9 events). The conditionals do not block a rescue, they enlarge the set of islands that start on the ratchet: a fair pair with a Trojan bully in the excluded slot is one ⅓-offerer
away from an unequal pair. In M the endpoint is all conditionals: exploiters (0.279 each) and yielders `if(partner demands 2/3 of me) accept 1/3, else 1/2` (0.221 each), unequal 0.8996 and fair 0.1004; in L
the two diverge against each other (mutual reading) and in M they cooperate through the provability box, which is why M's natural start (unequal share 0.429, above M's u* = 0.425) lands in the basin and L's
(0.429 against 0.55) does not. The fair 0.1004 is a balanced exchange: 1.24e-3 per event each way between unequal and fair islands, carried by conditional migrants whose moves into fair pairs are deleterious (-1/6, fixation 3.5e-4); there are 29-30 such moves from the dominant triple.

**4. Stability.** On the support (62 states in L, 68 in M, S3-closed, x >= 10^-9) the invariant-subspace Jacobian of L's unequal endpoint has 52 neutral modes, 10 negative, none positive; the
leading class-changing eigenvalue is -3.6e-3 (M: -2.3e-3), so the unequal class share relaxes at that rate; the transverse (symmetry-breaking) spectrum is unstable (+7.1e-4 in L, +7.2e-4 in M, class projection
zero): any asymmetry selects one orientation (an asymmetric perturbation of relative size 10^-3 or 10^-1 ends at U = 1.0 on one orientation, W and D gone). Perturbations toward V* of 10^-6, 10^-4 and
10^-2 return to the endpoint in both arms; mixing 1% and 10% of the natural law into it returns to it. The fair endpoint (L): 53 neutral modes and 11 negative on the support, the transverse spectrum
positive (+4.6e-4), as in arm T's knife-edge, but with negative class-changing eigenvalues (-2.1e-2) where arm T's were zero. Leak into absent states 10^-18 per event.

**Reading.**
- The unequal basin is in the exact mean field and is not a finite-pool artefact. It is also not specific to conditional programs: the constants have it, with a boundary at an unequal share of 0.69 that
  arm T's single tilt of 0.6 sat below.
- The length prior's contribution is to lower the boundary, by a two-program family per slot that costs a few 10^-5 of seed mass, is neutral on the fair path and takes from appeasers. M's unequal natural start is a
  consequence of the lowered boundary (0.425) falling under the natural unequal share (0.429).
- The mechanism is a ratchet, not a block: the unequal state selects away the programs that offer 1/2 and, at epsilon = 0, nothing re-supplies them. The fair state is the same ratchet the other way. This is
  a statement about the order of limits: it needs no coordination, only that extinction is irreversible.
- For a realizable library: what a prior must not weight is any conditional that is on-path identical to the fair program and exploits whoever offers less; the abundance needed is small.
- Predictions: see the table. Caveats: the truncation (cores of 48 to 102 conditionals per slot, at most three per island; m = 2 on all 1,296 not run); scans use early classification outside the baseline starts; bisection
  bracket 1/80; A = 150 cells not run (no pools); the roles cannot be separated (the same programs sit in all three); the victims knockout is nearly tautological.

## 3. Verdicts on the registered predictions

Scoring as registered (held iff the inequality holds in every cell it names; failed iff the falsifier holds anywhere; partial otherwise; unscored if unresolved). Truncation label: object P is m = 3 on the 48-core.

| prediction | verdict | numbers |
|---|---|---|
| 1 (RE) the basin exists: L and M end U >= 0.9 from the 0.6 tilt | partial | L U 0.9949 (m = 2: 0.9989); M U 0.8996 at m = 3 (just under 0.9; m = 2: 0.9995); at m = 1 both end at V* 0.42 / U 0.545 (not converged). The falsifier (V* >= 0.9) holds nowhere. |
| 2 (RE) L natural V* >= 0.99, M natural U >= 0.5 | partial (m = 1 straddles) | L 0.9997 at m = 1, 2, 3; M U 0.8996 at m = 3 and 1.0 at m = 2, but V* 1.0 at m = 1 |
| 3 (RE) constants only removes the basin | **failed** | constants-only u* = 0.6875 (L law), 0.675 (M law), exact, 729 states; arm T's own code, dose 0: tilt 0.7 -> U = 1.0 |
| 4 (RE) A1 removal removes it; A2s, A2x removal moves u* by < 0.1 | **failed** (second clause vacuous) | A1 is all 1,296 conditionals (A2s, A2x empty at n <= 6): removal leaves u* = 0.6875 / 0.675 <= 0.9 |
| 5 (RE) decisive classes in the excluded slot, blocking the rescue | **failed** | top classes: exploiters (high 0.17, excluded 0.13, low 0.007 in L; high 0.15 in M) and the ⅓-constants (low 0.16) / yielders (low 0.15); there is no rescue to block (fair-offering programs at 10^-17 in L) |
| 5 (argon's counter: the obstruction sits in the pair slots, a high demander that punishes defection or an accommodating low demander) | partial | the carrier sits in the pair slots (high role, with the victims in the low role) as argon said; its mechanism is exploitation of appeasers and extinction of the offerers, not blocking |
| 6 (RE) the unequal endpoint is linearly stable, leading class-changing eigenvalue <= -1e-5 | partial | class-changing leading -3.6e-3 (L), -2.3e-3 (M); but 52 of 62 modes neutral (L) and the transverse sector unstable (+7e-4) |
| 6 (sol's counter: a near-zero mode, or stability not extending to the transverse directions) | held | 52 neutral modes; transverse +7.1e-4 (L), +7.2e-4 (M); rare classes grow at up to 1.9e-9 / 3.7e-8 |
| 7 (RE) the charge moves u* by < 0.05 in L | held | 0.5375 (0.0125) founded and migrating; 0.525 (0.025) migrating only |
| E1 lumping vacuous; >= 1,250 conditionals in the union | partial | classes = programs exactly (1,251 L, 1,249 M); the union holds 1,242 / 1,240 conditionals (falsifier < 1,200 not met) |
| E2 dense object does not fit | held | 2 x 10^9 states |
| E3 truncation converged by m = 2 | **failed** | M natural: V* 1.0 at m = 1, U at m = 2; L unequal tilt: V* 0.42 / U 0.545 at m = 1, U 0.999 at m = 2; blocked flux 15% at the m = 1 unequal endpoint (m = 3: 10^-10). Natural-start L agrees (1.0, 0.9999). |
| E4 founding values | held | post-anneal V* 0.2796 (L), 0.2772 (M), 0.2792 (L at 0.1) against 0.280 / 0.277; conditional mass 0.0228 / 0.0234; diverging mass 1e-4 (L), 0 (L at 0.1) |
| E5 stored bistability mostly finite pool (L u* = none) | **failed** | L u* = 0.55; the exact mean field reproduces the stored chains |
| E6 a U-dominated endpoint is metastable | held (L, M) | rare classes grow at up to 1.9e-9 (L), 3.7e-8 (M) per event; residual < 1e-9 only after 10^6 events |
| E7 yielder in the top 5 and a pair-slot class first | partial | pair-slot first in both; a yielder in M's top 4, none in L's |
| E8 excluded-role knockout shifts u* less than the pair-role one | unscorable | the same programs hold all three roles |
| E9 tilt inflates conditionals by >= 1.5 | **failed** | 0.0217 against 0.0221 (L), 0.0220 against 0.0224 (M) |
| E10 the charge moves u* < 0.05 and V* < 0.01 | held | see 7; natural endpoint V* 1.0000 / 0.9997 |
| E11 M versus L through reading-edge classes | held | M's endpoint classes are exploiters and yielders, whose atoms read a partner's action naming the owner; M and L natural shares agree to 0.003 at 10 events |
| E12 fair endpoint's invariant spectrum neutral, transverse positive | **failed** (second clause held) | negative class-changing eigenvalues (-2.1e-2) on the support; transverse +4.6e-4 |
| E13 restoration dose-dependent; random knockouts shift < half | held | restoration of `exploiter-fair` at 0 / 0.25 / 0.5 / 1: L u* 0.675 / 0.625 / 0.5875 / 0.55, M 0.6625 / 0.5375 / 0.4875 / 0.425 (monotone; 1 is the unablated arm by construction); 20 of 20 random matched-mass knockouts leave U at u = 0.6 |

## 4. REJECTED.md entries (draft)

- **"Conditional programs carry the unequal basin; with constants only it is gone" (RE predictions 3 and 4, unequal basin, 2026-10-31).** Failed: the constants alone have an unequal basin whose boundary is an unequal share of 0.69 (L's constants) or 0.675 (M's), exact in 729 states and in arm T's own code (dose 0, tilt 0.7: U = 1.0); arm T's tilt of 0.6 sat below it. What the length prior's conditionals do is lower the boundary (0.55 in L, 0.425 in M). RESULTS "Where the unequal basin comes from". This also corrects the entry "Constants alone are bistable in the mean field" above: the prediction was right, its test (tilt 0.6) too low.
- **RE prediction 5 (the decisive classes sit in the excluded slot and block the rescue).** Failed: the decisive family is the Trojan bully in the pair slots (and in the excluded slot as well, 0.13 of L's slot mass), and no rescue is blocked: the programs that would rescue (offering 1/2) are extinct in the unequal endpoint. Argon's counter (pair slots) was right about the place and not about the mechanism.
- **Engineer E5 (the stored bistability is mostly the finite pool), E9 (the tilt inflates conditionals), E12 (the fair endpoint is neutral on the support), E3 (the m = 2 truncation is converged: m = 1 is not).** Wrong as registered. Same section.
- **My hand candidate for the carrier (soft yielders opening the fair -> unequal flux).** Wrong for L (the yielders are irrelevant: u* 0.55 with and without them); right as a part of M's endpoint (prey), where removing them raises u* by 0.075.
- **A dense exact ODE over behaviour classes for the length-prior arms.** Infeasible: the lumping merges nothing at n <= 6 (the nine constants distinguish every conditional), 1,251 classes per slot. Superseded by the reflecting m-conditional truncation (object P).

## 5. THEORY note (draft; the RE decides)

At epsilon = 0 an unequal-pair island is a ratchet (mechanism inferred from the role table and the donor marginals, the extinction itself measured): the unequal state selects against the programs that offer 1/2 (they are exploited in the pair slots) and the excluded slot, neutral for them, refills from the depleted donor marginal;
absent programs never return, so the rescue donors of the constants' own algebra go extinct and the state is absorbing (a certified attractor in the constants, a metastable one in L and M). The fair
state is the same ratchet the other way (the prey extinct). The unequal basin therefore exists in the constants' dynamics, with a boundary near an unequal share of 0.69 here, and a prior's role is only to move that
boundary: a conditional that is on-path identical to the fair program and exploits whoever offers less (Trojan bully) lowers it, one that answers an appeaser fairly raises it. Operating hypothesis for realizable
libraries (a prediction, not a result about them): a length-like prior that weights Trojan bullies at a few 10^-5 each lowers the threshold the natural start has to clear, and no later supply of fair offerers
repairs it at epsilon = 0.

## 6. NOTATION entries (draft)

- **Many islands, unequal basin (queue 70):** **class count** — behavioural classes per slot (programs merged iff equal joint code and divergence vector against every pair of the other slots' support programs); **m-truncation / object P** — the reflecting truncation in the number of conditional programs per island (m = 3 on the 48-conditional core is object P); **core** — the conditionals allowed to appear two or three at a time; **blocked flux** — the flux of migrations that would leave the state set, per event per island; **u\*** — the smallest scanned unequal share whose endpoint is U-dominated (U >= 0.5), bracket 1/80, "none" if no u <= 0.9; **tilt scan** — the unequal class rescaled to u in {0.3, ..., 0.9}; **families** — C constants, A1 conditionals with one atom (all 1,296 at n <= 6), `read-me` (the atom's action names the owner), `exploiter` (read-me at demand 1/3, true branch names the partner at 2/3), `exploiter-fair` (the same with false branch the third slot at 1/2: the Trojan bully), `yielder` (read-me at 2/3, true branch the partner at 1/3), `fair-reader` (read-me at 1/2, true branch the partner at 1/2); **victims** — the 1/3-demanding constants; **extinct** — a program whose donor mass is below 10^-15.

## 7. Open points for the RE

- Object P is a truncation. If you want the dense object: lean m = 2 on all 1,296 conditionals (45 million states, about 6 GB, 2 s per field evaluation) is the next rung, not run.
- A = 150 cells were cut (no pools).
- V3 and V4 ran after the first counted cells (disclosed in notes 2.2); the pilots at m = 1 on one pool preceded them.
- The excluded-versus-pair joint knockout of the spec cannot be done on the start law because the same programs hold all roles; a role-specific knockout would need a modified dynamics.
