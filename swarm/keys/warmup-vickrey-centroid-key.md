# Answer key (do not give to agents): warmup

**Answer.** The Vickrey-nearest point equals the centroid of F exactly when every winner's VCG payment is positive,
v_P > Σ_{j≠i} v_j for each winner i. (Degenerate cases where F is a point or a segment are excluded.)

**Why.**
- When every p_i^VCG > 0, the lower bounds are p_i ≥ p_i^VCG, and the pair constraints give upper bounds
  p_i ≤ v_i. All six bounds are the faces of a box with lower corner p^VCG and sides v_i − p_i^VCG = Σ v − v_P, the
  same for every i: a cube.
- F is the cube cut by the plane Σ p = R. Its centroid lies on the cube's main diagonal through p^VCG, by symmetry
  under permuting coordinates about the corner.
- The Vickrey-nearest point is the orthogonal projection of p^VCG onto the plane. It moves along (1, 1, 1), so it
  lies on the same diagonal.
- When some p_i^VCG = 0, that side is v_i < Σ v − v_P, the box is not a cube, and the two points generally differ.

**Numerical check** (RE, 2026-10-22, `scratchpad/warmup.py`; 2,570 random integer instances with a two-dimensional
face): all 482 with every VCG payment positive coincide; 10% of the 2,088 with a zero VCG payment coincide; the largest
gap is 3.18.

**Example.** v = (20; 15, 10, 3). p^VCG = (7, 2, 0) and R = 20. The Vickrey-nearest point is (11, 6, 3): the even
surcharge of 11/3 each would push p_C past its cap of 3, so p_C stops at 3 and A and B split the remaining 8. The
centroid of F is (11.692, 6.692, 1.615).

**Grading.**
- Full credit: the correct condition and a valid proof.
- Partial credit: the correct condition supported only by examples, or a proof of one direction only.
- No credit: "never" or "always".
