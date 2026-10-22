# Warmup: is the Vickrey-nearest core point the centroid?

## Setting

A seller has three items, a, b and c. Four bidders are single-minded: each wants exactly one bundle, values it at a
known amount, and has utility value minus payment if it gets the bundle and zero otherwise.

- P wants the bundle {a, b, c} and values it at v_P.
- A wants {a} and values it at v_A. B wants {b} at v_B. C wants {c} at v_C.

Assume v_A + v_B + v_C > v_P, so the efficient allocation gives each single item to its bidder, and A, B and C are the
winners. Values are known (complete information).

**The core.** A payment vector p = (p_A, p_B, p_C) is in the core if no coalition containing the seller could do better
by trading on its own: for every set S of bidders, the seller's revenue plus the winners' surplus inside S is at least
the best value S could create with the seller. Concretely: 0 ≤ p_i ≤ v_i, and for every subset T of the winners,
Σ_{i∈T} p_i ≥ max(0, v_P − Σ_{j∉T} v_j), where j ranges over the winners not in T.

**The minimum-revenue face.** Let R be the smallest total Σ p_i over the core. The *minimum-revenue face* F is the set
of core points with total exactly R. For three winners, F is a polygon (or a lower-dimensional piece) in the plane
Σ p_i = R.

**VCG and the Vickrey-nearest point.** VCG charges each winner i the harm it does to the others:
p_i^VCG = max(0, v_P − Σ_{j≠i} v_j). The *Vickrey-nearest* point is the point of F closest to p^VCG in Euclidean
distance. Some spectrum auctions use it as their payment rule (Day and Cramton 2012).

## Question

With two winners, the Vickrey-nearest point is the midpoint of the minimum-revenue face whenever no value cap binds.
**With three winners, when is the Vickrey-nearest point equal to the centroid of the polygon F?** Give an exact
condition on (v_P, v_A, v_B, v_C) and prove it. If the two differ, give an example.

## Deliverable

A file `answer.md` containing the condition, a proof, and at least one worked example with both points computed.
