# Per-mutant lattice rates — verdicts written 2026-09-23 (file dated per task spec 2026-09-21), before the run

The ε→0 object for the torus (death-birth Moran, von Neumann k = 4, weak
n = 6 with ROLE, PD, w = 0.3, mutation off inside each trial):

(a) ρ_enter(R): one copy of R in all-D; run until the R share reaches 0.5 or
    R is extinct; 2000 trials at sides 32 and 64;
    R ∈ {THEM(^C), or(X,THEM(ME)), THEM(^ROLE)}.
(b) M_exit(R): from all-R, mutants drawn one at a time from μ over the
    behavioural classes, each allowed to fix or go extinct (no mutation in
    between) before the next; count mutants until the R share drops below
    0.5; 50 trials at sides 32 and 64.
(c) Shadow pruning: all-R plus one ALLC and one D at random sites; record
    the lifetime of each in generations; 500 trials per side,
    R ∈ {THEM(^C), or(X,THEM(ME))}.

**Verdicts:**
1. ρ_enter is side-independent within ×1.5.
2. M_exit is side-independent within ×2.  Falsifier for lim_N efficiency:
   M_exit grows ∝ N instead.
3. Lone-D lifetime in FairBot (or(X,THEM(ME))) > 10× lone-D lifetime in
   THEM(^C).
4. ALLC lifetime in FairBot < ALLC lifetime in THEM(^C).
