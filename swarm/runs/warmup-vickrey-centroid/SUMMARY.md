# Warmup run, 2026-10-22: Vickrey-nearest vs centroid

21 runs (7 conditions × 3 replicates), Daytona 4 vCPU / 8 GB, 15-minute cap. **All 21 answers state the correct
condition** (graded on the stated condition; proofs not independently checked). The problem was too easy to
discriminate solving power, so the table compares cost and speed.

| condition | solved | agent wall-clock (s, mean) | input tokens (mean) | output tokens (mean) |
|---|---|---|---|---|
| opus | 3/3 | 127 | 117,960 | 11,954 |
| sol | 3/3 | 162 | 124,202 | 12,704 |
| argon | 3/3 | 811 | 1,067,343 | 38,828 |
| opus+sol | 3/3 | 253 | 697,684 | 24,137 |
| opus+argon | 3/3 | 495 | 895,313 | 43,061 |
| sol+argon | 3/3 | 299 | 848,958 | 28,650 |
| opus+sol+argon | 3/3 | 321 | 1,141,766 | 36,612 |
