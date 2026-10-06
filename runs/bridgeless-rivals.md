# Bridge-less rivals: prior mass in n, and mediation before loss at N ≥ 200 (`src/bridgeless_rivals.py`)

Spec `specs/2026-10-05-bridgeless-rivals.md`; predictions `predictions/2026-10-05-bridgeless-rivals.md`. Modal arm, PD, w = 0.3, ε = 0, iid length-prior seeds at n = 9, complete island graph, generation = I·N births, boundary mN = 0.3·N/T_nuc (1.091 at N = 200, 1.714 at N = 400). Finite-cutoff screening and finite-horizon lottery and hazard results, not π. Intervals: Wilson 95% over runs (runs are the independent units), exact Poisson for hazards, bootstrap for q.

## 1. Static screening (n = 9, 12, 13; n = 15 does not fit)

n = 15: 374,074 canonical functions (140 GB at one byte per pair); n = 14: 126,370 (16 GB); neither fits. Largest cutoff n = 13 (51,234 canonical functions). Classes merged within L_n by identical row and column; the n = 9 and 12 blocks reproduce the existing caches exactly. Masses in cut units (normalized within the cutoff) unless marked raw (units of the infinite length prior; inf = raw/(π²/12)). Omitted tail ω(n) = π²/12 − Σ_{s≤n} 1/(2s²) < 1/(2n).

### Rivals of A = {FairBot, `BOX1(THEM(ME))`}

| n | classes (canons) | ω(n) | rivals (full) | rival μ cut / raw / inf | union bridge μ | path length 1 / 2 / 3 / none |
|---|---|---|---|---|---|---|
| 9 | 863 (1,210) | 0.0526 | 20 (8) | 2.4e-05 / 1.9e-05 / 2.3e-05 | 0.0105 | 2 / 15 / 3 / 0 |
| 12 | 13,514 (22,690) | 0.0400 | 443 (241) | 4.1e-05 / 3.2e-05 / 3.9e-05 | 0.0145 | 58 / 379 / 6 / 0 |
| 13 | 27,189 (51,234) | 0.0370 | 839 (450) | 4.5e-05 / 3.6e-05 / 4.3e-05 | 0.0147 | 103 / 721 / 15 / 0 |

Bridge-less rivals by threshold τ (heaviest bridge ≤ τ; "total": total bridge mass ≤ τ; "safe": heaviest establisher bridge ≤ τ). Cells: count, bridge-less fraction of rival μ, bridge-less / bridged ratio, bridge-less raw mass.

| n | variant | τ = 0 | τ = 10⁻⁵ | τ = 10⁻⁴ | τ = 10⁻³ |
|---|---|---|---|---|---|
| 9 | heaviest | 3, 0.214, 0.272, 4.0e-06 | 13, 0.354, 0.547, 6.6e-06 | 13, 0.354, 0.547, 6.6e-06 | 13, 0.354, 0.547, 6.6e-06 |
| 9 | total | 3, 0.214, 0.272, 4.0e-06 | 3, 0.214, 0.272, 4.0e-06 | 13, 0.354, 0.547, 6.6e-06 | 13, 0.354, 0.547, 6.6e-06 |
| 9 | safe | 3, 0.214, 0.272, 4.0e-06 | 13, 0.354, 0.547, 6.6e-06 | 13, 0.354, 0.547, 6.6e-06 | 13, 0.354, 0.547, 6.6e-06 |
| 12 | heaviest | 76, 0.252, 0.337, 8.2e-06 | 220, 0.417, 0.714, 1.3e-05 | 252, 0.420, 0.725, 1.4e-05 | 252, 0.420, 0.725, 1.4e-05 |
| 12 | total | 76, 0.252, 0.337, 8.2e-06 | 80, 0.252, 0.337, 8.2e-06 | 97, 0.255, 0.343, 8.3e-06 | 252, 0.420, 0.725, 1.4e-05 |
| 12 | safe | 78, 0.252, 0.337, 8.2e-06 | 248, 0.420, 0.725, 1.4e-05 | 252, 0.420, 0.725, 1.4e-05 | 252, 0.420, 0.725, 1.4e-05 |
| 13 | heaviest | 152, 0.253, 0.338, 9.0e-06 | 445, 0.419, 0.722, 1.5e-05 | 509, 0.425, 0.739, 1.5e-05 | 509, 0.425, 0.739, 1.5e-05 |
| 13 | total | 152, 0.253, 0.338, 9.0e-06 | 167, 0.254, 0.340, 9.0e-06 | 216, 0.257, 0.347, 9.2e-06 | 509, 0.425, 0.739, 1.5e-05 |
| 13 | safe | 176, 0.253, 0.339, 9.0e-06 | 505, 0.425, 0.739, 1.5e-05 | 509, 0.425, 0.739, 1.5e-05 | 509, 0.425, 0.739, 1.5e-05 |

Composition of rival mass (fractions of rival μ): A-faked = some member of the reference pair strictly invades R (ρ(A_j into R) > 1/N, R a sucker of A_j); mediated = mediator mass > 10⁻⁴; "hard" = bridge-less at τ, neither A-faked nor mediated.

| n | A-faked | τ = 0 bridge-less | τ = 0 hard | τ = 10⁻⁴ bridge-less | of which A-faked | τ = 10⁻⁴ hard (count) |
|---|---|---|---|---|---|---|
| 9 | 0.140 | 0.214 | 0.214 | 0.354 | 0.140 | 0.214 (3) |
| 12 | 0.165 | 0.252 | 0.252 | 0.420 | 0.164 | 0.256 (112) |
| 13 | 0.166 | 0.253 | 0.253 | 0.425 | 0.165 | 0.259 (214) |

Cutoff tracking (rivals at the lower cutoff followed by representative canon; rival status is per canon and cutoff-invariant, so rival raw mass only accumulates; "gained" = bridge-less at the lower cutoff with a bridge at the higher):

| step | rivals | split into ≥ 2 classes | τ = 0 bridge-less | gained a bridge (any part) | μ of gainers | heaviest gained bridge μ |
|---|---|---|---|---|---|---|
| 9-12 | 20 | 2 | 3 | 0 | 0 | 0 |
| 12-13 | 443 | 7 | 76 | 6 | 3.5e-08 | 4.3e-10 |
| 9-13 | 20 | 2 | 3 | 0 | 0 | 0 |

### Rivals of probe-readers {`BOX(THEM(^C))`, `BOX1(THEM(^C))`} (comparison)

| n | classes (canons) | ω(n) | rivals (full) | rival μ cut / raw / inf | union bridge μ | path length 1 / 2 / 3 / none |
|---|---|---|---|---|---|---|
| 9 | 863 (1,210) | 0.0526 | 16 (5) | 1.2e-05 / 9.2e-06 / 1.1e-05 | 0.0155 | 0 / 13 / 3 / 0 |
| 12 | 13,514 (22,690) | 0.0400 | 276 (115) | 2.4e-05 / 1.9e-05 / 2.3e-05 | 0.0212 | 1 / 269 / 6 / 0 |
| 13 | 27,189 (51,234) | 0.0370 | 532 (220) | 2.7e-05 / 2.1e-05 / 2.6e-05 | 0.0214 | 1 / 500 / 31 / 0 |

Bridge-less rivals by threshold τ (heaviest bridge ≤ τ; "total": total bridge mass ≤ τ; "safe": heaviest establisher bridge ≤ τ). Cells: count, bridge-less fraction of rival μ, bridge-less / bridged ratio, bridge-less raw mass.

| n | variant | τ = 0 | τ = 10⁻⁵ | τ = 10⁻⁴ | τ = 10⁻³ |
|---|---|---|---|---|---|
| 9 | heaviest | 3, 0.434, 0.767, 4.0e-06 | 13, 0.717, 2.534, 6.6e-06 | 13, 0.717, 2.534, 6.6e-06 | 13, 0.717, 2.534, 6.6e-06 |
| 9 | total | 3, 0.434, 0.767, 4.0e-06 | 3, 0.434, 0.767, 4.0e-06 | 13, 0.717, 2.534, 6.6e-06 | 13, 0.717, 2.534, 6.6e-06 |
| 9 | safe | 3, 0.434, 0.767, 4.0e-06 | 13, 0.717, 2.534, 6.6e-06 | 13, 0.717, 2.534, 6.6e-06 | 13, 0.717, 2.534, 6.6e-06 |
| 12 | heaviest | 16, 0.296, 0.420, 5.6e-06 | 220, 0.709, 2.436, 1.3e-05 | 220, 0.709, 2.436, 1.3e-05 | 220, 0.709, 2.436, 1.3e-05 |
| 12 | total | 16, 0.296, 0.420, 5.6e-06 | 80, 0.429, 0.752, 8.2e-06 | 97, 0.434, 0.767, 8.3e-06 | 220, 0.709, 2.436, 1.3e-05 |
| 12 | safe | 78, 0.429, 0.752, 8.2e-06 | 220, 0.709, 2.436, 1.3e-05 | 220, 0.709, 2.436, 1.3e-05 | 220, 0.709, 2.436, 1.3e-05 |
| 13 | heaviest | 62, 0.294, 0.417, 6.2e-06 | 445, 0.707, 2.418, 1.5e-05 | 445, 0.707, 2.418, 1.5e-05 | 445, 0.707, 2.418, 1.5e-05 |
| 13 | total | 62, 0.294, 0.417, 6.2e-06 | 167, 0.428, 0.749, 9.0e-06 | 216, 0.434, 0.767, 9.2e-06 | 445, 0.707, 2.418, 1.5e-05 |
| 13 | safe | 160, 0.426, 0.743, 9.0e-06 | 445, 0.707, 2.418, 1.5e-05 | 445, 0.707, 2.418, 1.5e-05 | 445, 0.707, 2.418, 1.5e-05 |

Composition of rival mass (fractions of rival μ): A-faked = some member of the reference pair strictly invades R (ρ(A_j into R) > 1/N, R a sucker of A_j); mediated = mediator mass > 10⁻⁴; "hard" = bridge-less at τ, neither A-faked nor mediated.

| n | A-faked | τ = 0 bridge-less | τ = 0 hard | τ = 10⁻⁴ bridge-less | of which A-faked | τ = 10⁻⁴ hard (count) |
|---|---|---|---|---|---|---|
| 9 | 0.415 | 0.434 | 0.434 | 0.717 | 0.283 | 0.434 (3) |
| 12 | 0.412 | 0.296 | 0.296 | 0.709 | 0.280 | 0.429 (80) |
| 13 | 0.411 | 0.294 | 0.294 | 0.707 | 0.279 | 0.428 (166) |

Cutoff tracking (rivals at the lower cutoff followed by representative canon; rival status is per canon and cutoff-invariant, so rival raw mass only accumulates; "gained" = bridge-less at the lower cutoff with a bridge at the higher):

| step | rivals | split into ≥ 2 classes | τ = 0 bridge-less | gained a bridge (any part) | μ of gainers | heaviest gained bridge μ |
|---|---|---|---|---|---|---|
| 9-12 | 16 | 2 | 3 | 1 | 1.8e-06 | 2.5e-09 |
| 12-13 | 276 | 7 | 16 | 0 | 0 | 0 |
| 9-13 | 16 | 2 | 3 | 1 | 1.8e-06 | 3.3e-09 |

### The 20 heaviest rivals of A at n = 9

| rival | μ | full | bridges (n, mass, safe mass) | heaviest bridge (μ) | prey: A-net / bridges (heaviest) | mediators (n, mass) | path | ρ₂₀₀(R into FB, FB1) | ρ₂₀₀(FB, FB1 into R) |
|---|---|---|---|---|---|---|---|---|---|
| `BOX1(THEM(^not(BOX(THEM(ME)))))` | 5.4e-06 | y | 70, 5.3e-03, 5.1e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 8.4e-03 / 5.2e-03 (`BOX(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 5.4e-06 | y | 70, 5.3e-03, 5.1e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 8.4e-03 / 5.2e-03 (`BOX(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.2e-06 | y | 0, 0, 0 | none | 5.3e-03 / 5.3e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 3 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.8e-06 | y | 0, 0, 0 | none | 5.3e-03 / 5.3e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 3 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.6e-06 | FB1 only | 20, 5.2e-03, 5.2e-03 | `BOX(THEM(THEM))` (5.1e-03) | 5.4e-03 / 5.3e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 1 | 5.0e-03, 7.2e-09 | 5.0e-03, 7.2e-09 |
| `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 1.6e-06 | FB1 only | 22, 5.2e-03, 5.2e-03 | `BOX(THEM(THEM))` (5.1e-03) | 5.4e-03 / 5.3e-03 (`BOX1(THEM(THEM))`) | 8, 1.7e-03 | 1 | 5.0e-03, 7.2e-09 | 5.0e-03, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(^C)))))` | 7.9e-07 | y | 70, 5.3e-03, 5.1e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 8.4e-03 / 5.2e-03 (`BOX(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(^D)))))` | 7.9e-07 | y | 70, 5.3e-03, 5.1e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 8.4e-03 / 5.2e-03 (`BOX(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.8e-07 | FB only | 61, 6.8e-05, 2.3e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 9.1e-07 / 9.1e-07 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 6.8e-07 | FB only | 64, 7.6e-05, 3.0e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 9.1e-07 / 9.1e-07 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 6.8e-07 | FB only | 56, 6.4e-05, 2.3e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 4.8e-06 / 4.8e-06 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(ME))))))` | 6.8e-07 | FB only | 59, 7.2e-05, 3.0e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 4.8e-06 / 4.8e-06 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 2.3e-07 | y | 22, 5.1e-03, 5.1e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 1.6e-04 / 1.6e-04 (`or(BOX(THEM(ME)),BOXD(THEM(ME)))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(^C))))` | 2.3e-07 | y | 0, 0, 0 | none | 5.3e-03 / 5.3e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 3 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `not(BOXD1(THEM(^not(BOX(THEM(^C))))))` | 1.1e-07 | FB only | 56, 6.4e-05, 2.3e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 4.8e-06 / 4.8e-06 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(^D))))))` | 1.1e-07 | FB only | 59, 7.2e-05, 3.0e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 4.8e-06 / 4.8e-06 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOXD(THEM(^C))))))` | 1.1e-07 | FB only | 61, 7.3e-05, 3.1e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 3.8e-06 / 3.8e-06 (`or(BOX(THEM(ME)),not(BOX1(THEM(ME))))`) | 71, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX1(THEM(^C))))))` | 1.1e-07 | FB only | 61, 6.8e-05, 2.3e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 9.1e-07 / 9.1e-07 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX1(THEM(^D))))))` | 1.1e-07 | FB only | 64, 7.6e-05, 3.0e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 9.1e-07 / 9.1e-07 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 74, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOXD1(THEM(^C))))))` | 1.1e-07 | FB only | 66, 7.6e-05, 3.1e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 0 / 0 (–) | 71, 7.1e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |

### The 20 heaviest rivals of A at n = 13

| rival | μ | full | bridges (n, mass, safe mass) | heaviest bridge (μ) | prey: A-net / bridges (heaviest) | mediators (n, mass) | path | ρ₂₀₀(R into FB, FB1) | ρ₂₀₀(FB, FB1 into R) |
|---|---|---|---|---|---|---|---|---|---|
| `BOX1(THEM(^not(BOX(THEM(ME)))))` | 6.8e-06 | y | 1780, 5.5e-03, 5.2e-03 | `BOX1(THEM(THEM))` (5.2e-03) | 8.8e-03 / 8.8e-03 (`BOX(THEM(THEM))`) | 143, 1.4e-06 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 6.8e-06 | y | 1796, 5.5e-03, 5.2e-03 | `BOX1(THEM(THEM))` (5.2e-03) | 8.8e-03 / 8.8e-03 (`BOX(THEM(THEM))`) | 155, 1.4e-06 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 3.4e-06 | FB1 only | 617, 5.3e-03, 5.3e-03 | `BOX(THEM(THEM))` (5.2e-03) | 5.6e-03 / 5.6e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 1 | 5.0e-03, 7.2e-09 | 5.0e-03, 7.2e-09 |
| `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 3.4e-06 | FB1 only | 664, 5.3e-03, 5.3e-03 | `BOX(THEM(THEM))` (5.2e-03) | 5.6e-03 / 5.6e-03 (`BOX1(THEM(THEM))`) | 420, 1.8e-03 | 1 | 5.0e-03, 7.2e-09 | 5.0e-03, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 3.2e-06 | y | 0, 0, 0 | none | 5.5e-03 / 5.5e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.2e-06 | y | 0, 0, 0 | none | 5.5e-03 / 5.5e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 3.2e-06 | y | 0, 0, 0 | none | 5.5e-03 / 5.5e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(^C)))))` | 1.6e-06 | y | 1872, 5.5e-03, 5.2e-03 | `BOX1(THEM(THEM))` (5.2e-03) | 8.8e-03 / 8.8e-03 (`BOX(THEM(THEM))`) | 155, 1.4e-06 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `BOX1(THEM(^not(BOX(THEM(^D)))))` | 1.6e-06 | y | 1841, 5.5e-03, 5.2e-03 | `BOX1(THEM(THEM))` (5.2e-03) | 8.8e-03 / 8.8e-03 (`BOX(THEM(THEM))`) | 155, 1.4e-06 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `not(BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 1.3e-06 | FB only | 1812, 1.8e-04, 6.9e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(ME))))` (8.0e-06) | 3.5e-06 / 3.5e-06 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 2509, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(ME))))))` | 1.3e-06 | FB only | 1689, 1.7e-04, 6.9e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(ME))))` (8.0e-06) | 1.2e-05 / 1.2e-05 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 2510, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 1.3e-06 | FB only | 1750, 1.6e-04, 5.3e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(THEM))))` (8.0e-06) | 3.5e-06 / 3.5e-06 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 2503, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 1.3e-06 | FB only | 1640, 1.5e-04, 5.3e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(THEM))))` (8.0e-06) | 1.2e-05 / 1.2e-05 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 2481, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(^C))))` | 6.9e-07 | y | 0, 0, 0 | none | 5.5e-03 / 5.5e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 6.9e-07 | y | 0, 0, 0 | none | 5.5e-03 / 5.5e-03 (`BOX1(THEM(THEM))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 6.9e-07 | y | 545, 5.2e-03, 5.2e-03 | `BOX1(THEM(THEM))` (5.2e-03) | 2.8e-04 / 2.8e-04 (`or(BOX1(THEM(THEM)),BOXD1(THEM(ME)))`) | 0, 0 | 2 | 7.2e-09, 7.2e-09 | 7.2e-09, 7.2e-09 |
| `not(BOXD1(THEM(^not(BOX1(THEM(^D))))))` | 2.9e-07 | FB only | 1800, 1.8e-04, 6.9e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(ME))))` (8.0e-06) | 3.6e-06 / 3.6e-06 (`or(BOX(THEM(ME)),not(BOXD(THEM(^C))))`) | 2509, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(^C))))))` | 2.9e-07 | FB only | 1637, 1.5e-04, 5.3e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(THEM))))` (8.0e-06) | 1.2e-05 / 1.2e-05 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 2478, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOX(THEM(^D))))))` | 2.9e-07 | FB only | 1683, 1.7e-04, 6.9e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(ME))))` (8.0e-06) | 1.3e-05 / 1.3e-05 (`or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))`) | 2510, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |
| `not(BOXD1(THEM(^not(BOXD(THEM(^C))))))` | 2.9e-07 | FB only | 1739, 1.7e-04, 7.2e-05 | `or(BOX(THEM(ME)),not(BOXD(THEM(ME))))` (8.0e-06) | 9.1e-06 / 9.1e-06 (`or(BOX(THEM(THEM)),not(BOX1(THEM(ME))))`) | 2460, 7.4e-03 | 2 | 7.2e-09, 2.2e-40 | 7.2e-09, 0.264 |

### Forced rivals (n = 9)

| label | class | μ | tags against | bridge mass (static) | heaviest bridge | tag-3 mass (kernel) | tag-2 network mass | mediator mass |
|---|---|---|---|---|---|---|---|---|
| P* | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.2e-06 | `BOX1(THEM(ME))` | 0 | none | 8.1e-06 | 3.2e-03 | 0 |
| P*' | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.8e-06 | `BOX1(THEM(ME))` | 0 | none | 8.1e-06 | 3.2e-03 | 0 |
| S* | `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.8e-07 | `BOX(THEM(ME))` | 6.8e-05 | `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))` (3.6e-06) | 7.0e-05 | 6.5e-03 | 7.1e-03 |
| B1 | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 5.4e-06 | `BOX1(THEM(ME))` | 5.3e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 5.3e-03 | 3.1e-04 | 0 |
| H | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.6e-06 | `BOX1(THEM(ME))` | 5.2e-03 | `BOX(THEM(THEM))` (5.1e-03) | 0.0103 | 3.2e-06 | 0 |
| B4 | `BOX1(THEM(^not(BOX(THEM(^C)))))` | 7.9e-07 | `BOX1(THEM(ME))` | 5.3e-03 | `BOX1(THEM(THEM))` (5.1e-03) | 5.3e-03 | 3.2e-04 | 0 |

## 2. Enriched lottery (N = 200, I = 64, mN = 1.091, n = 9, horizon 10⁵, 100 runs per cell)

**(d) iid control:** 100 runs; generic separation ever 0, at the horizon 0; island P(C,C) 1.000 (min 1.000); cf cross-island 1.000; q (holder form) 0.81 [0.74, 0.89] (100 pairs); q_est (local establishment form) 0.81 [0.75, 0.89]; status {'frozen': 100}; 0.03 worker-h.

### Separation, loss and mediation

Horizon separated = tags 1 and 2 each hold a certified island at the end; generic = any two certified holders mutually defect at the end. Hazard = network losses per minority-island-generation after the first separation (exposure ∫ min(held₁, held₂) dt). Rival-island losses by strong-holder transition: replacement 2>1 / absorption (mediation) 2>3 / capture 2>0. Mediation-before-loss = runs with a 2>3 event at or before the loss (or horizon) / runs in which the rival established.

| cell | rival | runs | rival established | ever separated | horizon separated | generic sep. end | losses (A / R) / exposure | hazard [95%] | KM S(10²/10³/10⁴/10⁵) | rival-island losses 2>1 / 2>3 / 2>0 | last loss of R by tag | mediation-before-loss | worker-h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (a) dense | P* | 100 | 0.98 [0.93, 0.99] | 0.98 [0.93, 0.99] | 0.97 [0.92, 0.99] | 97 | 0 (0 / 0) / 2.0e+08 | 0 [0, 1.9e-08] | 1.00 / 1.00 / 1.00 / 1.00 | 11 / 0 / 0 | – | 0.00 [0.00, 0.04] | 1.79 |
| (a) dense | P*' | 100 | 0.98 [0.93, 0.99] | 0.98 [0.93, 0.99] | 0.97 [0.92, 0.99] | 97 | 1 (1 / 0) / 2.1e+08 | 4.8e-09 [1.2e-10, 2.7e-08] | 1.00 / 0.99 / 0.99 / 0.99 | 10 / 0 / 0 | – | 0.00 [0.00, 0.04] | 1.82 |
| (a) dense | S* | 100 | 0.37 [0.28, 0.47] | 0.34 [0.25, 0.44] | 0.01 [0.00, 0.05] | 1 | 33 (0 / 33) / 3.1e+05 | 1.1e-04 [7.3e-05, 1.5e-04] | 0.79 / 0.03 / 0.03 / 0.03 | 151 / 0 / 1 | {'1': 24, 'None': 8, '0': 1} | 0.00 [0.00, 0.09] | 0.01 |
| (a) dense | B1 | 100 | 0.87 [0.79, 0.92] | 0.85 [0.77, 0.91] | 0.12 [0.07, 0.20] | 12 | 73 (33 / 40) / 2.2e+07 | 3.3e-06 [2.6e-06, 4.2e-06] | 0.99 / 0.65 / 0.14 / 0.14 | 33 / 2162 / 177 | {'3': 31, '1': 3, '0': 4, 'None': 2} | 0.80 [0.71, 0.87] | 0.23 |
| (a) dense | H | 100 | 0.98 [0.93, 0.99] | 0.97 [0.92, 0.99] | 0.01 [0.00, 0.05] | 1 | 96 (79 / 17) / 1.9e+06 | 5.0e-05 [4.1e-05, 6.2e-05] | 0.99 / 0.38 / 0.01 / 0.01 | 6 / 2907 / 0 | {'3': 17} | 0.92 [0.85, 0.96] | 0.06 |
| (a) dense | B4 | 100 | 0.84 [0.76, 0.90] | 0.82 [0.73, 0.88] | 0.09 [0.05, 0.16] | 11 | 73 (44 / 29) / 1.6e+07 | 4.5e-06 [3.5e-06, 5.6e-06] | 1.00 / 0.62 / 0.11 / 0.11 | 34 / 2173 / 160 | {'3': 18, '0': 6, '1': 5} | 0.76 [0.66, 0.84] | 0.23 |
| (c) nobridge | B1 | 100 | 0.78 [0.69, 0.85] | 0.77 [0.68, 0.84] | 0.67 [0.57, 0.75] | 67 | 11 (1 / 10) / 1.3e+08 | 8.3e-08 [4.2e-08, 1.5e-07] | 0.97 / 0.86 / 0.86 / 0.86 | 22 / 0 / 240 | {'0': 7, 'None': 2, '1': 1} | 0.00 [0.00, 0.05] | 0.95 |
| (b) sparse | P* | 100 | 0.54 [0.44, 0.63] | 0.54 [0.44, 0.63] | 0.54 [0.44, 0.63] | 54 | 0 (0 / 0) / 1.1e+08 | 0 [0, 3.5e-08] | 1.00 / 1.00 / 1.00 / 1.00 | 8 / 0 / 0 | – | 0.00 [0.00, 0.07] | 0.82 |
| (b) sparse | P*' | 100 | 0.60 [0.50, 0.69] | 0.60 [0.50, 0.69] | 0.60 [0.50, 0.69] | 60 | 0 (0 / 0) / 1.1e+08 | 0 [0, 3.5e-08] | 1.00 / 1.00 / 1.00 / 1.00 | 8 / 0 / 0 | – | 0.00 [0.00, 0.06] | 0.87 |
| (b) sparse | S* | 100 | 0.09 [0.05, 0.16] | 0.08 [0.04, 0.15] | 0.00 [0.00, 0.04] | 1 | 8 (0 / 8) / 1.84e+03 | 4.3e-03 [1.9e-03, 8.5e-03] | 0.75 / 0.00 / 0.00 / 0.00 | 26 / 0 / 1 | {'None': 4, '1': 4} | 0.00 [0.00, 0.30] | 0.03 |
| (b) sparse | B1 | 100 | 0.27 [0.19, 0.36] | 0.27 [0.19, 0.36] | 0.03 [0.01, 0.08] | 3 | 24 (8 / 16) / 6.5e+06 | 3.7e-06 [2.4e-06, 5.5e-06] | 1.00 / 0.52 / 0.11 / 0.11 | 15 / 475 / 56 | {'3': 12, '1': 2, '0': 2} | 0.78 [0.59, 0.89] | 0.07 |
| (b) sparse | H | 100 | 0.71 [0.61, 0.79] | 0.70 [0.60, 0.78] | 0.00 [0.00, 0.04] | 0 | 70 (48 / 22) / 3.7e+05 | 1.9e-04 [1.5e-04, 2.4e-04] | 0.99 / 0.39 / 0.00 / 0.00 | 12 / 2075 / 0 | {'3': 20, 'None': 2} | 0.96 [0.88, 0.99] | 0.03 |
| (b) sparse | B4 | 100 | 0.33 [0.25, 0.43] | 0.31 [0.23, 0.41] | 0.06 [0.03, 0.12] | 6 | 25 (12 / 13) / 1.2e+07 | 2.0e-06 [1.3e-06, 3.0e-06] | 1.00 / 0.68 / 0.19 / 0.19 | 8 / 726 / 29 | {'3': 12, '1': 1} | 0.73 [0.56, 0.85] | 0.12 |

### Establishment, bridge founders, efficiency and q

| cell | rival | per-island local rival establishment (tag 2 / the class R) | islands established by A / rival / bridge (mean per run) | bridge founders: seeded islands, copies (mean) | runs with a bridge establishment | bridge alive at end (runs) | bridge islands at end (mean) | mediation events | islands held at end A / R / bridge / other | island P(C,C) (min) | runs all-D / with island P(C,C) < 0.95 | cf cross P(C,C): all / separated runs | q holder [95%] | Δq holder vs (d) | q_est [95%] | Δq_est vs (d) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (a) dense | P* | 0.0478 / 0.0478 | 39.6 / 24.38 / 0.00 | 0.1, 0.1 | 0 | 0 | 0.00 | 0 | 38.3 / 25.7 / 0.0 / 0.0 | 0.982 (0.968) | 0 / 0 | 0.607 / 0.595 | 0.74 [0.68, 0.79] | -0.07 [-0.17, +0.01] | 0.81 [0.75, 0.86] | -0.01 [-0.10, +0.08] |
| (a) dense | P*' | 0.0469 / 0.0464 | 37.0 / 27.02 / 0.00 | 0.1, 0.1 | 0 | 0 | 0.00 | 0 | 34.9 / 29.1 / 0.0 / 0.0 | 0.982 (0.970) | 0 / 0 | 0.594 / 0.582 | 0.74 [0.68, 0.81] | -0.07 [-0.16, +0.03] | 0.81 [0.75, 0.88] | -0.00 [-0.10, +0.09] |
| (a) dense | S* | 0.0053 / 0.0052 | 63.3 / 0.66 / 0.01 | 0.8, 0.8 | 1 | 1 | 0.00 | 0 | 64.0 / 0.0 / 0.0 / 0.0 | 1.000 (0.996) | 0 / 0 | 0.999 / 0.910 | 0.71 [0.65, 0.78] | -0.10 [-0.20, +0.00] | 0.76 [0.69, 0.82] | -0.06 [-0.16, +0.04] |
| (a) dense | B1 | 0.0234 / 0.0234 | 31.3 / 18.50 / 13.64 | 41.8, 67.5 | 83 | 81 | 33.63 | 2162 | 19.0 / 10.7 / 33.6 / 0.6 | 0.988 (0.000) | 1 / 1 | 0.946 / 0.634 | 0.37 [0.32, 0.42] | -0.44 [-0.54, -0.36] | 0.85 [0.78, 0.93] | +0.04 [-0.07, +0.15] |
| (a) dense | H | 0.0516 / 0.0516 | 14.3 / 27.99 / 21.68 | 56.0, 132.7 | 99 | 99 | 41.32 | 2907 | 2.5 / 20.2 / 41.3 / 0.0 | 1.000 (0.984) | 0 / 0 | 0.997 / 0.659 | 0.36 [0.31, 0.40] | -0.45 [-0.54, -0.37] | 0.85 [0.79, 0.92] | +0.04 [-0.06, +0.13] |
| (a) dense | B4 | 0.0211 / 0.0208 | 30.4 / 19.62 / 13.39 | 41.1, 66.0 | 80 | 79 | 31.81 | 2173 | 18.2 / 13.3 / 31.8 / 0.7 | 0.998 (0.975) | 0 / 0 | 0.956 / 0.624 | 0.29 [0.25, 0.33] | -0.52 [-0.60, -0.44] | 0.76 [0.70, 0.83] | -0.05 [-0.15, +0.05] |
| (c) nobridge | B1 | 0.0211 / 0.0208 | 40.5 / 23.12 / 0.00 | 0.0, 0.0 | 0 | 0 | 0.00 | 0 | 39.0 / 24.3 / 0.0 / 0.7 | 0.978 (0.000) | 1 / 1 | 0.730 / 0.611 | 0.60 [0.53, 0.67] | -0.21 [-0.31, -0.12] | 0.76 [0.69, 0.84] | -0.06 [-0.16, +0.05] |
| (b) sparse | P* | 0.0119 / 0.0119 | 53.2 / 10.79 / 0.00 | 0.1, 0.1 | 0 | 0 | 0.00 | 0 | 51.5 / 12.5 / 0.0 / 0.0 | 0.990 (0.970) | 0 / 0 | 0.793 / 0.617 | 0.78 [0.71, 0.85] | -0.03 [-0.14, +0.06] | 0.85 [0.78, 0.92] | +0.03 [-0.07, +0.13] |
| (b) sparse | P*' | 0.0128 / 0.0122 | 52.5 / 11.49 / 0.00 | 0.1, 0.1 | 0 | 0 | 0.00 | 0 | 50.7 / 13.3 / 0.0 / 0.0 | 0.990 (0.966) | 0 / 0 | 0.781 / 0.635 | 0.71 [0.65, 0.78] | -0.10 [-0.20, -0.01] | 0.77 [0.71, 0.85] | -0.04 [-0.15, +0.06] |
| (b) sparse | S* | 0.0009 / 0.0009 | 63.5 / 0.12 / 0.00 | 0.8, 0.8 | 0 | 0 | 0.00 | 0 | 63.7 / 0.0 / 0.0 / 0.3 | 1.000 (0.984) | 0 / 0 | 0.995 / – | 0.86 [0.79, 0.93] | +0.05 [-0.05, +0.15] | 0.87 [0.81, 0.95] | +0.06 [-0.04, +0.16] |
| (b) sparse | B1 | 0.0042 / 0.0042 | 46.1 / 3.90 / 13.63 | 41.9, 67.1 | 83 | 82 | 18.22 | 475 | 43.3 / 2.1 / 18.2 / 0.4 | 0.999 (0.971) | 0 / 0 | 0.985 / 0.486 | 0.63 [0.56, 0.69] | -0.18 [-0.29, -0.08] | 0.86 [0.79, 0.94] | +0.05 [-0.07, +0.16] |
| (b) sparse | H | 0.0119 / 0.0119 | 23.7 / 13.52 / 26.73 | 56.4, 131.1 | 99 | 99 | 41.42 | 2075 | 13.2 / 9.4 / 41.4 / 0.0 | 1.000 (1.000) | 0 / 0 | 1.000 / – | 0.40 [0.35, 0.46] | -0.41 [-0.50, -0.32] | 0.83 [0.76, 0.90] | +0.01 [-0.09, +0.12] |
| (b) sparse | B4 | 0.0058 / 0.0052 | 45.1 / 6.84 / 12.06 | 41.4, 66.6 | 84 | 85 | 18.81 | 726 | 40.5 / 4.6 / 18.8 / 0.0 | 0.999 (0.967) | 0 / 0 | 0.975 / 0.585 | 0.61 [0.54, 0.68] | -0.20 [-0.31, -0.09] | 0.92 [0.84, 1.00] | +0.10 [-0.01, +0.22] |

## 3. Unconditional natural runs (f): (200, 64), boundary, 3000 runs

Ever separated 0.01 [0.01, 0.01]; separated at the horizon 0.00 [0.00, 0.01] (Wilson 95%; zero gives the rule-of-three bound 3/n = 0.0010). Island P(C,C) mean 0.9996, min 0.000; 0.37 worker-h.

| separation | bridge-less (τ = 0) | bridge-less (τ = 10⁻⁴) | A-faked | bridged | neither in A / not a rival of A |
|---|---|---|---|---|---|
| ever (first separated pair) | 8 | 0 | 0 | 21 | 0 |
| at the horizon (every pair) | 8 | 0 | 0 | 1 | 0 |

Every separation (first separated pair of each ever-separated run, and every pair separated at the end): bridge classes of the pair in the run's support, seeded copies / islands, islands held at the end, alive at the end, mediation transitions (a strong holder of the pair replaced by a bridge class), islands held at the end by each member.

| rep | kind | pair | rival type | bridge classes | seeded copies / islands | bridge islands at end | bridge alive | mediations | held a / b | separated at end |
|---|---|---|---|---|---|---|---|---|---|---|
| 51 | first | `BOX1(THEM(ME))` × `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | bridged | 3 | 151 / 60 | 0 | n | 2 | 64 / 0 | n |
| 122 | first | `BOX1(THEM(ME))` × `BOX1(THEM(^not(BOX(THEM(^D)))))` | bridged | 2 | 77 / 43 | 41 | y | 74 | 0 / 23 | n |
| 269 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` × `BOX1(THEM(ME))` | bridged | 2 | 75 / 45 | 39 | y | 71 | 0 / 25 | n |
| 278 | first | `BOX1(THEM(ME))` × `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | bridged | 4 | 144 / 59 | 54 | y | 43 | 10 / 0 | n |
| 535 | first | `BOX1(THEM(ME))` × `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | bridged | 2 | 137 / 55 | 57 | y | 74 | 0 / 7 | n |
| 285 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` × `BOX(THEM(THEM))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 35 / 29 | y |
| 285 | end | `BOX(THEM(THEM))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 29 / 35 | y |
| 820 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` × `BOX(THEM(THEM))` | bridged | 4 | 131 / 55 | 64 | y | 3 | 0 / 64 | n |
| 993 | first | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` × `BOX1(THEM(ME))` | bridged | 2 | 122 / 55 | 59 | y | 29 | 5 / 0 | n |
| 1042 | first | `BOX1(THEM(ME))` × `BOX1(THEM(^not(BOX(THEM(ME)))))` | bridged | 3 | 70 / 43 | 38 | y | 85 | 0 / 26 | n |
| 1246 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` × `BOX1(THEM(ME))` | bridged | 4 | 117 / 55 | 64 | y | 54 | 0 / 0 | n |
| 1308 | first | `BOX1(THEM(^not(BOX(THEM(THEM)))))` × `BOX1(THEM(ME))` | bridged | 4 | 62 / 40 | 40 | y | 95 | 0 / 24 | n |
| 1044 | first | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 48 / 16 | y |
| 1044 | end | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 48 / 16 | y |
| 1364 | first | `BOX(THEM(THEM))` × `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | bridged | 4 | 140 / 56 | 64 | y | 0 | 64 / 0 | n |
| 1263 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` × `BOX1(THEM(ME))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 14 / 50 | y |
| 1263 | end | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 50 / 14 | y |
| 1617 | first | `BOX1(THEM(ME))` × `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | bridged | 3 | 137 / 54 | 48 | y | 6 | 16 / 0 | n |
| 1774 | first | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` × `BOX1(THEM(ME))` | bridged | 5 | 114 / 53 | 37 | y | 85 | 27 / 0 | n |
| 1922 | first | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 62 / 2 | y |
| 1922 | end | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 62 / 2 | y |
| 2154 | first | `BOX1(THEM(^not(BOX(THEM(THEM)))))` × `BOX1(THEM(ME))` | bridged | 1 | 74 / 42 | 47 | y | 83 | 17 / 0 | n |
| 2180 | first | `BOX1(THEM(ME))` × `BOX1(THEM(^not(BOX(THEM(THEM)))))` | bridged | 5 | 79 / 48 | 0 | n | 0 | 64 / 0 | n |
| 2088 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` × `BOX(THEM(THEM))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 8 / 56 | y |
| 2088 | end | `BOX(THEM(THEM))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 56 / 8 | y |
| 2110 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` × `BOX1(THEM(ME))` | bridged | 3 | 58 / 37 | 0 | n | 0 | 38 / 26 | y |
| 2110 | end | `BOX1(THEM(ME))` × `BOX1(THEM(^not(BOX(THEM(ME)))))` | bridged | 3 | 58 / 37 | 0 | n | 0 | 26 / 38 | y |
| 2422 | first | `BOX(THEM(ME))` × `BOX1(THEM(^not(BOX(THEM(THEM)))))` | bridged | 2 | 63 / 39 | 19 | y | 34 | 45 / 0 | n |
| 2282 | first | `BOX1(THEM(^C))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 0 / 55 | y |
| 2282 | end | `BOX(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 9 / 55 | y |
| 2493 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` × `BOX1(THEM(ME))` | bridged | 3 | 63 / 40 | 0 | n | 0 | 0 / 64 | n |
| 2510 | first | `BOX1(THEM(^not(BOX(THEM(THEM)))))` × `BOX1(THEM(ME))` | bridged | 4 | 73 / 47 | 23 | y | 5 | 0 / 41 | n |
| 2542 | first | `BOX1(THEM(ME))` × `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | bridged | 2 | 134 / 54 | 57 | y | 4 | 7 / 0 | n |
| 2725 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` × `BOX1(THEM(ME))` | bridged | 3 | 121 / 58 | 0 | n | 1 | 0 / 64 | n |
| 2883 | first | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 54 / 10 | y |
| 2883 | end | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 54 / 10 | y |
| 2799 | first | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 43 / 21 | y |
| 2799 | end | `BOX1(THEM(ME))` × `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | bridge-less (tau = 0) | 0 | 0 / 0 | 0 | n | 0 | 43 / 21 | y |

