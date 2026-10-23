# Main problem, run 2 (2026-10-22): prudent modal agents, repaired definition

One replicate per condition, 60-minute cap, Daytona 4 vCPU / 8 GB. **All 7 conditions solved both parts**: a prudent
agent of depth 2, verified by the checker (six of seven found the same 7-symbol formula `B(a & (d -> B(F)))`), and a
valid proof that no depth-1 agent is prudent. Every proof uses the same short argument: at world 0 FairBot looks like
CooperateBot, so a depth-1 agent that defects against CooperateBot defects against FairBot at world 1, and FairBot
then defects forever. Several also report the minimal size: 7 symbols with constants, 8 without.

| condition | agent time to finish (s) | formula | input tokens | output tokens | notes |
|---|---|---|---|---|---|
| opus | 161 | `B(a & (d -> B(F)))` | 274,587 | 11,300 |  |
| sol | 78 | `B(a & (d -> B(F)))` | 118,244 | 5,520 |  |
| argon | 2011 | `B(a & (d -> B(~d)))` | 1,676,835 | 38,974 |  |
| opus+sol | 227 | `B(a & (d -> B(F)))` | 720,518 | 18,360 |  |
| opus+argon | 465 | `B(a & (d -> B(F)))` | 914,469 | 18,640 |  |
| sol+argon | 480 | `B(a & (d -> B(F)))` | 1,240,546 | 14,047 |  |
| opus+sol+argon | 382 | `B(a & (d -> B(F)))` | 1,287,598 | 15,964 | opus killed mid-call (partial) |

**Reading.** Once the definition was right, the problem was easy for every model alone. It does not separate
swarms from solo agents; as on the warmup, swarms cost more tokens and time for the same answer.

# Sonnet alone vs a Sonnet pair (2026-10-22), same problem

The RS asked whether two Sonnet agents that can message each other outperform one. Three replicates per condition,
60-minute cap, same sandbox, problem and checker as run 2; the pair shares `/work` and `board.md`.

| condition | rep | finish (s) | formula (checker: prudent) | depth-1 proof | input tokens | output tokens | USD |
|---|---|---|---|---|---|---|---|
| sonnet | 0 | 52 | `B(a) & B(B(F) \| ~d)` | valid | 99,884 | 5,428 | 0.09 |
| sonnet | 1 | 53 | `B(a) & B(B(F) \| ~d)` | valid | 134,657 | 6,036 | 0.11 |
| sonnet | 2 | 42 | `B(a) & B(B(F) \| ~d)` | valid | 98,715 | 4,728 | 0.08 |
| sonnet+sonnet2 | 0 | 54 | `B(a) & B(B(F) \| ~d)` | valid | 275,342 | 12,158 | 0.21 |
| sonnet+sonnet2 | 1 | 43 | `B(a & (B(F) \| ~d))` | valid | 297,922 | 9,671 | 0.19 |
| sonnet+sonnet2 | 2 | 83 | `B(a & (B(F) \| ~d))` | valid | 463,482 | 12,287 | 0.36 |

**Reading.** 6/6 solved both parts in under a minute and a half, with the same world-1 argument as run 2 (RE read every
proof). The pair is never better: same answer, about 2.4× the cost, and its messages are status and "please review"
notes; in r0 and r2 both agents wrote `answer.md` concurrently. The problem is below Sonnet's ceiling, so it cannot
show a gain from communication; the grid stable-sets problem is the harder test.
