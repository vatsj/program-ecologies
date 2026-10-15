# Spec: where does the leader-value core exist? A parametric sweep and a proof attempt, 2026-10-14

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
A computation, no ecology. Follow-up to DEFERRED 15 and `notes/leader-value-core.md` (the catalogue: PD exists
uniquely at (C, C); chicken, hawk–dove, divide-the-dollar and three-player majority are empty; SOG one-shot exists
only at the boss's leader wage; allocation games reduce to an exchange economy with a classical core).
REJECTED.md checked: nothing re-opened.

## Why

The RS's equilibrium notion (response functions over action subprofiles, on-path consistency, credibility with
response) has, under the repair the RS and chat Claude agreed, the leader-value core as its outcome set: an outcome
x is in it iff for every coalition S, x_S is not beaten by S's leader value v(S) (the best S can guarantee by moving
first against the complement's credible best response), i.e. the γ-core (Chander–Tulkens) with credibility off path.
Existence fails in many natural games. The RE's conjecture: **existence holds where every coalition's leader value is
bounded by a default it already holds** (owned endowments; second-mover advantage under strategic complements), and
**fails where a surplus is unowned and moving first claims it** (substitutes; division games). The sweep tests this.

## Design

For each family, compute v(S) for every coalition (pure-strategy credible responses as in the notes; mixed
responses as a reported variant where pure ones fail to exist), the leader-value core by linear feasibility
(Bondareva–Shapley balancedness in the TU-like cases, direct enumeration on grids in NTU cases), and the sign of
the first-mover advantage per coalition (v(S) against S's payoff when the complement moves first).
- **Cournot oligopoly**, n ∈ {2, 3, 4}, linear demand, asymmetric constant costs on a grid, capacity limits as a
  variant (strategic substitutes).
- **Bertrand** with differentiated products (complements in prices) and homogeneous products with identical and
  asymmetric costs.
- **Public goods** with concave production, n ∈ {3, 4, 5} (voluntary contributions: substitutes in contributions).
- **A supermodular family with spillovers**: investment games with complementarities, positive and negative
  spillovers.
- **Allocation games** (the RS's class) with continuous goods and convex (Cobb–Douglas, CES) preferences, n = 3, 4:
  the continuous version of the discrete checks in the notes (which had indivisibility artefacts).
- **Controls:** the notes' catalogue recomputed by the new code (exact agreement required).

**Proof attempt.** For supermodular games with positive spillovers (and for allocation games, via Scarf), state and
try to prove existence of the leader-value core; for the substitutes families, state and try to prove emptiness
under a first-mover-advantage condition. Proofs, partial proofs and counterexamples go in the notes, labelled.

**Scale guard.** One worker suffices; at most 2. Two sibling runs use up to 3 workers each.

## Required outputs

`src/core_sweep.py`, `tests/test_core_sweep.py` (the catalogue reproduced; balancedness on known cases),
`notes/core-existence-sweep.md` (definitions, the table per family and parameter, the characterization, the proof
attempts), `runs/core-existence-sweep.json`, predictions committed before any family is computed, and the usual
hand-back (draft RESULTS section, REJECTED entries, THEORY §3 / DEFERRED 15 edits, NOTATION, ≤ 5 lines, branch,
commits).

## RE predictions (with falsifiers)

1. ~~Cournot empty for n ≥ 3 at every cost profile~~ [withdrawn after review by sol: with p = a − Q and common cost,
   a k-coalition leading against independent Nash followers gets v(S) = m²/(4(n − k + 1)), m = a − c, and the equal
   monopoly split gives each m²/(4n), which meets every coalition since k(n − k + 1) ≥ n; the core is nonempty for
   every n]. **Revised:** symmetric linear Cournot nonempty for every n (verified analytically first); with
   asymmetric costs, empty somewhere for n ≥ 3 in the NTU core (uncertain). *Falsifier:* nonempty on the whole
   asymmetric grid.
2. **Differentiated Bertrand (complements in prices): nonempty** (second-mover advantage caps leader values).
   *Falsifier:* empty at a positive share of the grid.
3. ~~Concave public goods nonempty~~ [withdrawn after review by gemini-4-argon: contributions are substitutes, a
   coalition leading by free-riding raises the complement's contributions, which is the conjecture's failure case].
   **Revised:** empty on a substantial share of the grid, with free-riding leadership the violating coalitions.
   *Falsifier:* nonempty everywhere.
4. **Supermodular with positive spillovers: nonempty, with a proof;** with negative spillovers, empty somewhere.
   *Falsifier:* empty for positive spillovers at some parameter.
5. **Continuous allocation games: nonempty for convex preferences** (the classical core by Scarf). *Falsifier:*
   empty at some parameter.
6. **The characterization, weakened** [after review by sol: timing advantage is not incompatibility of claims]:
   some coalition's first-mover advantage is necessary for emptiness, not sufficient; the sufficient condition is
   sought as a balancedness statement. *Falsifier:* one certified empty case in which no coalition gains from moving
   first.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **TU and NTU kept apart.** The NTU leader-value core: S blocks x iff some a_S makes every member of S strictly
   better under the complement's credible response; the TU core: Bondareva–Shapley on v(S) = max over a_S of S's
   summed payoff. Both are reported for every family; ownership claims are read on the NTU core.
2. **The complement's response.** Default as in `notes/leader-value-core.md`: the complement's members play a Nash
   equilibrium among themselves given a_S (the γ-convention). With several equilibria, report pessimistic and
   optimistic bounds (S facing the worst and the best). A small factorial panel varies transfers, follower
   coordination (complement as one coalition) and selection. The identity with the Chander–Tulkens γ-core is stated
   only where the conventions match, and benchmarked against known γ-core existence results (e.g. Helm 2001).
3. **Exactness.** Closed forms for linear Cournot and Bertrand; KKT and root finding for public goods and CES /
   Cobb–Douglas allocation games; grids only as verification, with refinement checks, certified blocking margins and
   an "unresolved" label. Homogeneous Bertrand states its rationing rule and treats unattained optima explicitly.
4. **Certificates of the answer.** Every empty TU case outputs a violating balanced collection; every nonempty case a
   feasible allocation and its minimum coalition slack. Universal claims are falsified by one certified
   counterexample.
5. **Start** with sol's analytic symmetric Cournot case, verified constraint by constraint.
6. **Controls.** Simultaneous-partition payoffs beside leader payoffs (the merger-paradox control: emptiness from
   coalition-size returns rather than timing); Scarf's assumptions checked for the allocation games; the catalogue
   reproduced (implementation consistency only, not the equivalence between the RS's notion and this core).
7. **Boundary.** A static compatibility result; no claim about evolutionary accessibility.
