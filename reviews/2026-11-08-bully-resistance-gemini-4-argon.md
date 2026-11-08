# Review of `specs/2026-11-08-bully-resistance.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Two-partner reads vs. the root fuel cap (1,200) and `A_f`:** Both Prudent readers ($P$) and Openers ($O$) perform two reads of up to 400 steps each (800 steps total). In $L_T$, if a partner $j$ being read by $P$ or $O$ is *itself* a reader (e.g., $F$, $B$, $P$, or $O$), $j$'s simulated execution will attempt its own read (another 400 steps), hitting $P$/$O$'s 400-step read cap, timing out, and incurring the $P_{\text{fail}} = 0.1$ charge under $A_f$—or exhausting the 1,200 root cap. Worse, if the non-timeout-accepting variants (`n`) treat a timed-out read as "no", $P$ will refuse to pair with *itself* or with $F$, and $O$ will misclassify reader-held pairs.
  * *Fix:* In Step 1 validation (V2), explicitly require checking the $(P \cup O \cup F \cup B)^3$ sub-table for read timeouts, $A_f$ failure charges, and self/mutual compatibility *before* running Step 3. If nested reads time out at 400/1,200, either supply the shallow/non-recursive read environment used by `Dn`/`Dp` in arm T, or raise the root cap so two 400-step reads plus glue do not forfeit.
* **Opener ($O$) victim-identification ambiguity:** Step 1 defines an unequal pair as two others that "name each other with demands ⅔ / ⅓", and instructs $O$ to "offer ½ to the one getting ⅓". In majority division, the one *getting* ⅓ is the one *demanding* ⅓ (while the bully demands ⅔). Furthermore, when $O$ in slot $i$ reads the other two slots $j, k$, it must pass a third-slot partner to each read; if $j$ or $k$ is a conditional bully $B$, what $B$ outputs depends on who is in the slot $B$ reads.
  * *Fix:* Specify the exact arguments $O$ passes when reading $j$ and $k$ (presumably the actual current triple $(i, j, k)$), and state unambiguously: "if $j$ names $k$ at ⅔ and $k$ names $j$ at ⅓, offer ½ to $k$ (the ⅓-demander)."
* **Prudent ($P$) fallback `o` vs. bullies:** When $P$ reads partner $j$ as a bully and refuses it, fallback `o` names the *other* slot $k$ at ½. If $k$ is also a bully (which names its other slot at ½ when not reading a ⅓-offerer!), $P$'s fallback `o` inadvertently pairs with bully $k$ at ½/½, defeating the purpose of refusal.
  * *Fix:* Check in Step 1 whether `(P_o, B, B)` or `(P_o, B, C)` results in $P_o$ pairing with $B$. If so, separate `P_z` (null fallback) from `P_o` in Step 3, or restrict $P$ to `z` fallback so refusal actually refuses.

**2. Predictions I think are wrong**

* **RE 1 (Mechanism):** I expect **both** mechanisms operate, and the shadow mechanism will falsify RE 1's first clause. Against a fair reader $F$, a Trojan bully $B$ ("if partner names me at ⅓ demand ⅔, else name other slot at ½") behaves *identically* on-path to a fair reader / ½-constant. Unless $B$ triggers an $A_f$ read-failure charge that $F$ does not, $B$ is selectively neutral in an $F$-held island and will fix near $1/N$, drifting in as an unconditional shadow that later locks onto arriving ⅓-constants. If $F$ and $B$ have different read footprints under $A_f$, $B$'s fixation could even exceed $3/N$ (falsifying RE 1).
* **RE 2 (Prudence restores a threshold at $\beta = 3$):** Likely wrong if `P_o` is pooled with `P_z` (see Flaw 3), and questionable even for `P_z`: refusing to pair with $B$ on a fair island prevents $B$ from shadowing $P$, but once an island is unequal $(B + \text{⅓-constant})$ from the founding scramble or tail, $P$ cannot invade it either (a lone $P$ refusing $B$ gets 0 while the $(B, \text{⅓})$ pair still clears).

**3. Missing controls or cheap additions**

* **Invasion assay for $P$ and $O$ in Step 0:** Add $P$ and $O$ to the Step 0.2 single-island Moran invasion assays ($B$ into homogeneous $P$; $P$ and $O$ into $B + \text{⅓-constant}$; $O$ into $B + \text{⅓-reader}$ if any). It costs almost nothing and directly tests *why* $P$ or $O$ should work before spending 250 CPU-hours on Step 3.
* **Track $A_f$ charges in Step 0.1:** Report the exact net payoffs (including $P_{\text{fail}}$ deductions) alongside the outcome class in Step 0.1. A 0.1 read-failure penalty completely dominates neutral drift at $N = 200, w = 0.3$ ($Nw \Delta\pi = 6$).

**4. Alternative explanations not ruled out**

* **Compute-price asymmetry ($A_f$), not strategic prudence:** Because $P$ and $O$ make two reads instead of one, any timeout against junk or complex partners charges them $0.2$ instead of $0.1$. If $P$ or $O$ fails in Step 3, it may be due to double $A_f$ penalties against the 72–88% junk / tail rather than strategic insufficiency. Recording mean $A_f$ charges per family in Step 3 rules this out.

**5. Ideas for the research program**

* Nothing material.
