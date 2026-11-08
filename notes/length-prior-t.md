# Queue 75: notes (engineer's log; deviations, timing, budget). Appended as the run proceeds.

## Deviations from the spec (so far)
- The worktree base lacked the spec; fast-forwarded to b37b647 before starting.
- Step 1 enumeration reaches s0 = 6 for R0 (2.1e8 terms, 1,183 s on one shard of four) and s0 = 5 for R1 (7.7e6 terms), not the
  spec's target of 9: the term count grows x30 per node and 7 nodes would be 8.6e9 (R0) terms. An R1 run to s0 = 6 was started on
  Daytona and abandoned (see below).
- R1 has two tags (readn, readp), 20 tags. lib / libsrc / sim stay in the prior but are not enumerated (mass accounted exactly, sampled by
  Monte Carlo); nat literals in the enumeration are blocks of n+1 evaluated at a representative value.
- Probe set: 27 library programs + 2 bullies (29 partners). Classes: exact table equality with the 31 members of T+, plus
  response-map family labels. Partner-independence by a taint tracker; R1 read macro by precomputed read outcomes (fast and hybrid paths,
  both checked against full tables); evaluator internal errors (a `run` of a quoted open term) are counted as stuck.
- Targeted search is a depth-one decision-tree grammar: masses are lower bounds.
- Pilot disclosure: 14 Daytona pilot cells (2a, delta 0.03, beta 0; N = 100 runs 0-11, N = 400 runs 0-1) were read before the full launch;
  the same cells are re-run in the counted grid (deterministic, identical).

## Operations log
- Two R1 s0 = 6 Daytona runs launched twice: first with an enumerator that leaked compiled closures on shards other than 0 (OOM), then
  with the leak fixed; the second pair ran 5,900 s: one sandbox exited 1 with no output (about 13 sandbox-CPU-hours lost), the other lost its
  client to a gateway error. R1 s0 = 6 abandoned; R1 s0 = 5 run locally in 4 shards (shard 1 killed once, relaunched).
- A scheduler stopped at its 30-minute limit took its client processes with it (they were not detached): five g2 sandboxes were orphaned and
  recovered with tools/daytona_fetch.py (no work lost, rows fetched). Clients are now started with setsid.
- Container restart (2026-11-08, about 07:00 UTC): every local process was lost (scheduler, clients, fetchers, the local R1 shard-1
  enumeration). Six sandboxes survived and were mapped from the launch logs: c7b9387c = g2_5of6, 7b679084 = g4_0of13, 47746f0d =
  g4_1of13, 76a6e583 = g4_2of13, b02b5951 = g4_3of13, ab3247b3 = g4_4of13; fetchers reattached to all six; R1 shard 1 relaunched locally
  (about 35 min); scheduler re-armed for g4_5of13 .. g4_12of13. Lost work: the in-progress R1 shard-1 run only.
- Budget: 5 g1 + 6 g2 chunks at about 1.2 h x 4 CPUs each; projected total about 255 sandbox-CPU-hours of the 300 ceiling, no cut applied.
- Second container restart (about 10:40 UTC): scheduler and fetchers lost again; seven sandboxes survived and were mapped from the launch
  logs (7e3ac59a = g4_10of13, 5c34cce1 = g4_5, 7d7d7370 = g4_6, b45e1e8b = g4_7, 7d04ff0f = g4_8, af36189c = g4_9, 27f7464a = long64);
  fetchers reattached to all; long64 and slice2 had already completed. No work lost. g4_11 and g4_12 re-queued. Remaining long work is
  launched on Daytona only.
