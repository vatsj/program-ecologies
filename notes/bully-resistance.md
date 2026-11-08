# Queue 76: notes (engineer's log; deviations, operations, budget). Appended as the run proceeds.

## Deviations from the spec (so far)
- The worktree base lacked the spec and queue 75's code; fast-forwarded to `main-t69lqz` (c1d47a1) before starting.
- Catalogue K = 55: T+'s 31 programs, 8 prudent readers P (P<dir><fb><to>), 4 lenient-probe readers Q (the spec's probe-timeout-accept variant, fallback z),
  8 openers O, and 4 programs of the matched control F2 (T's single reader, fallback z, plus P's second read made and ignored). F2 was appended after the
  step-0 assays were run; the first 51 programs are identical in code, steps, timeouts and forfeits (checked), so the assays on the 51-program table stand.
- Step-0 invasion assays use the exact fixation probability of the two-type Moran chain (one invader slot, the other slots monomorphic: frequency-independent
  fitness, rho = (1 - 1/r)/(1 - 1/r^N), r = exp(0.3 d)) over ALL named resident triples of each class instead of sampling; the 10^4-trial Monte Carlo (jump chain) and
  the full kernel are checks (kernel max |z| = 1.97 over 24 assays, jump chain max |z| = 3.4 over 420, 1 above 3), and a neutral twin gives the empirical 1/N baseline
  (0.00513 +- 0.00016 against 0.005). The kernel itself stops a run on play identity, so neutral invaders are not resolvable by it.
- Exploiter mass: all arms keep queue 75's exploiter share 0.01 delta / 0.09 (the arms differ only in what fills delta).
- P's probe is the third-slot constant naming the read partner at 1/3 (C3 for dir n, C0 for dir p); "takes 2/3" is the partner naming the third slot at 2/3
  (code 2 for dir n, 5 for dir p).
- R2 gets two probe tags (probn, probp; arity 1, literal child 0..8), the mirror of readn / readp, rather than one tag.
- Pilots disclosed in `predictions/2026-11-08-bully-resistance.md` (addendum).

## Operations log
- 2026-11-08 21:07 UTC: step 3 main chunks launched on Daytona (scheduler tools/br_sched.sh, queue runs/br_launch/queue.txt: 12 main chunks m_*of12, 5 control/variant/seed/charge-off
  chunks s_*of5, 5 I = 256 chunks i_*of5). Sandbox ids are in runs/br_launch/launch.log (untracked) and below.
  94dcd599 = m_0of12, d6e057cb = m_1of12, 46f4c468 = m_2of12, 6dbf0dc7 = m_3of12, 411ebf5c = m_4of12.
