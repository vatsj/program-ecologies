## Queue 75 additions to REJECTED.md (draft)

- **RE 1 (the threshold is a copy count in N).** Falsified: delta\* rises with N at I = 64 and I = 256 (c\* = I N delta\* = 35, 380, 1,560 founder copies at N = 100, 200, 400). Reading to drop: "a small positive reader mass suffices in large enough worlds"; on the tested grid larger N needs a larger reader share, and more islands I lower it.
- **RE 5 (R1 brackets it: rho_R >= 1e-3).** Falsified with a certified upper bound (rho_R <= 1.3e-5 at 95%); the lower bound is 4e-10. Reading to drop: "a read primitive makes readers cheap enough for a length prior".
- **RE 6, R1 half (under R1 some tested cell reaches delta\*).** Falsified: the projected law has no delta\* at any feasible delta.
- **E4 (delta = 1e-4 is a reader-free world at T0's level).** Falsified: 0.50 / 0.51 against T0's 0.73 / 0.26 at N = 200 / 400.
- **gemini-4-argon's counter (beta < 0.05).** False: the bully / reader lower-bound ratio is 3.09 in R0 and R1; a Trojan bully is as short as a fair reader.
- **A reading to drop: "family-level classes are the readers".** On sampled partners the non-exact family-level classes mostly fail to reproduce (R0 single 11 / 36; R1 single 3 / 26); only exact-member classes enter.
- **A reading to drop: "a length prior over the syntax is a prior over reader-like programs".** 72-88% of the finite mass is forfeits (junk), and the conditional mass outside the library is mostly other conditionals (R1 0.153) and constants-with-reads (0.041).
- **Dropped: the R1 enumeration to size 6** (two Daytona launches, one killed by memory, one lost its client after 5,900 s; the term count and the 0.1 s per tainted term made 8 CPU-h per shard-set); R1 was enumerated to size 5 and the size-6 readers are reached by the targeted search.
