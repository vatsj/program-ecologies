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
- 21:39 UTC: the scheduler task hit its 30-minute background limit and its five clients died with it (sandboxes alive); reattached with tools/daytona_fetch.py (tools/br_reattach.sh)
  to 94dcd599 = m_0of12, d6e057cb = m_1of12, 46f4c468 = m_2of12, 6dbf0dc7 = m_3of12, 411ebf5c = m_4of12; clients are now launched from foreground calls (tools/br_fill.sh) and the
  background task only waits (tools/br_wait.sh, 2 h limit). Lost work: none (clients only poll).
- 22:20 UTC: the R2 enumeration to s0 = 5 (job r2, sandbox 3174ded1) was stopped and the sandbox deleted: size 4 took 433 s and size 5 would have taken about 4 h per shard (terms
  containing a probe tag with a literal child are classified by a full 29 x 29 probe table: seconds each). The exhaustive part for R2 is s0 = 4 (262,358 terms at size 4, run locally in 772 s,
  mass accounting sum 1 - 3e-16; `runs/lt_prior_br/e_R2/enum_R2_s4_0of1.json`); the Monte Carlo (4 x 1.5e6 draws from the prior, S0 = 4) runs as job r2mc (a5468260). R1 was s0 = 5 and R0 s0 = 6 in queue 75; the
  P / O masses do not depend on s0 (they come from the grammar search).
- R0 prudent search first ran with a wrong cap-class label (no spelling found); fixed (`cap_ok`: the classes `[255,510]` and `>=1023`, the same labels queue 75's two-reader search used) and rerun. Note: queue 75's
  R0 two-reader search used the labels `[256,510]` and found none (R0 two exact mass 0 in `step1.json`); that is probably the same label bug, and R0's two-partner mass is negligible either way (R1/R2: 10^-29).
- Local compute: V1 (80 cells) and the `ideal` stage (320 cells) run on the local container (2-3 workers).

## Budget and timing (final)
- Step-3 cell time (sum of job walls on one core): 121.8 CPU-hours (main 40.1, i256 24.3, s 15.8, fo 9.9, lps 24.8, decomp 2.0, long 1.6, ideal 3.3 local, v1 0.4 local); step 2: R2 enumeration to s0 = 4 about 0.2 h local, three prudent / opener searches about 1.3 h local, R2 Monte Carlo 4 x 1.5e6 draws about 6 sandbox-CPU-hours, the stopped R2 s0 = 5 attempt about 0.5 sandbox-CPU-hour; step 0 assays 0.02 h and the holding rerun (120 cells) about 1.5 h local. Total about 135 CPU-hours of the 250 ceiling; no cut applied.
- Pilots disclosed in `predictions/2026-11-08-bully-resistance.md` (step-0 assays, step-2 R2 prudent search, partial look at the main grid before E10, no F+O cell before its addendum).
- The spec's coordinator addendum was merged mid-run (arm F+O, RE 6); F+O ran as chunks fo_*of3 (780 cells) ahead of the remaining queue. The decomposition (E9, E10) and the idealized table are additions to the spec, registered.
- Sandbox clients died with their 30-minute background scheduler once (reattached, no loss); clients are now started from foreground calls (tools/br_fill.sh, br_loop.sh). `python3 tools/daytona_run.py list` is empty at hand-back.

## The model cannot express
- A program that builds the probe from what it read (a quote-from-value primitive): the probe constant is a literal quoted term; R2's probe tag takes a literal code, anything else is stuck.
- Conditional self-cooperation between readers without relying on timeouts: a reader that cooperates iff its partner cooperates with it has only the refusal fixed point under the capped (and the level-iterated) semantics; P x P = 0 even in the idealized table.
- A third party that changes a victim's payoff: offers (O) and refusals (P) act on pairs, but a constant victim never reads, so no reader in the unpaired slot can move the pair; coordinated two-slot moves are not in the single-slot invasion dynamics.
- Punishment or a side payment: nothing in the dollar game lets a reader cost a bully anything except by not pairing with it.
