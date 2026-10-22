FORMULA: B(a & (d -> B(~d)))
DEPTH: 2

---

# Solution: Prudent Modal Agents

## 1. Existence and Minimal-Depth Examples (Question 1)

**Yes**, a prudent agent exists, and the smallest possible modal depth of a prudent agent is **2**.

### Minimal Examples

Depending on whether propositional constants (`T`, `F`) are permitted, the minimal-size prudent formulas of modal depth $2$ are:

1. **Without constants (minimal size = 8 symbols):**
   $$\varphi_X = \Box\big(a \land (d \to \Box\neg d)\big) \qquad \text{(`B(a & (d -> B(~d)))`)}$$
   (As shown in Section 3, the only other constant-free prudent formulas of size $8$ up to logical equivalence are `B(a & (d -> B(~a)))` and `B(a & (d -> B(~c)))`.)

2. **With constants (minimal size = 7 symbols):**
   $$\varphi_X = \Box\big(a \land (d \to \Box\bot)\big) \qquad \text{(`B(a & (d -> B(F)))`)}$$
   (Note that in GL, $\Box(a \land (d \to \Box\neg a))$ is logically equivalent to $\Box(a \land (d \to \Box\bot))$.)

3. **Using only the single atom `d` (no `a` or `c`):**
   $$\varphi_X = \Box(d \leftrightarrow \Box\neg d) \qquad \text{(`B((d -> B(~d)) & (B(~d) -> d))`)}$$

### Intuitions and World-by-World Evaluation

In the Kripke semantics of GL on the finite linear frames $0 < 1 < 2 < \dots$, any box formula $\Box\chi$ holds vacuously at world $0$. In particular:
- At world $m = 0$, the formula $\Box\bot$ (or $\Box\neg d$, since $d$ holds at world $0$ for CooperateBot, FairBot, and $X$) is **true** at $m = 0$ and **false** at all worlds $m \ge 1$.
- Therefore, the implication $d \to \Box\bot$ (or $d \to \Box\neg d$) inside the outer box requires that **if the opponent cooperates with DefectBot at world $m$, then $m$ must be world $0$** (i.e., the opponent must defect against DefectBot at every world $m \ge 1$).
- Conjoining this with $a$ inside the outer box ($\Box(a \land (d \to \Box\neg d))$) requires that at every world $m < n$:
  1. the opponent $Y$ cooperates with $X$ at world $m$ ($a$ holds at $m$), and
  2. $Y$ defects against DefectBot at every world $m \ge 1$ ($d$ fails at $m \ge 1$).

Let us trace the truth values (where `C` = True, `D` = False) across worlds $n = 0, 1, 2, 3, \dots$ for $\varphi_X = \Box(a \land (d \to \Box\neg d))$ (the table for `B(a & (d -> B(F)))` is identical at every world):

| Matchup / Atom | $n = 0$ | $n = 1$ | $n = 2$ | $n = 3$ | $n \ge 4$ | Stabilized Outcome |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$X$ vs CooperateBot (`CB`)** | C | C | **D** | **D** | **D** | **D** |
| **$X$ vs DefectBot (`DB`)** | C | **D** | **D** | **D** | **D** | **D** |
| **$X$ vs FairBot (`FB`)** | C | C | **C** | **C** | **C** | **C** |
| **FairBot (`FB`) vs $X$** | C | C | **C** | **C** | **C** | **C** |
| **$X$ vs $X$ (itself)** | C | C | **C** | **C** | **C** | **C** |

**Verification of each row:**
- **At world $n = 0$:** Every outer box $\Box(\dots)$ is vacuously true (`C`), so $\text{act}(X, Y, 0) = \text{C}$ and $\text{act}(FB, Y, 0) = \text{C}$ for every opponent $Y$.
- **Against DefectBot (`DB`):** At world $m = 0$, $a = \text{act}(DB, X, 0) = \text{D}$, so $a \land (d \to \Box\neg d)$ is false at $m = 0$. Hence for all $n \ge 1$, $\text{act}(X, DB, n) = \text{D}$.
- **Against CooperateBot (`CB`):** At world $m = 0$, $a = \text{C}$ and $\Box\neg d = \text{C}$ (vacuously), so $a \land (d \to \Box\neg d)$ holds at $m = 0$, giving $\text{act}(X, CB, 1) = \text{C}$. However, at world $m = 1$, $d = \text{act}(CB, DB, 1) = \text{C}$, while $\Box\neg d$ is false (since $\text{act}(CB, DB, 0) = \text{C}$ at $m = 0$). Thus $d \to \Box\neg d$ fails at $m = 1$, so for all $n \ge 2$, $\text{act}(X, CB, n) = \text{D}$.
- **Against FairBot (`FB`, $\varphi_{FB} = \Box a$):** Against `DB`, FairBot cooperates at $m = 0$ (vacuously) and defects at all $m \ge 1$ (since $\text{act}(DB, FB, 0) = \text{D}$). Thus for $Y = FB$, the atom $d = \text{act}(FB, DB, m)$ is `C` at $m = 0$ and `D` at all $m \ge 1$, so $d \to \Box\neg d$ holds at **all** worlds $m \ge 0$ (at $m = 0$ because $\Box\neg d$ is vacuously true; at $m \ge 1$ because $d$ is false). By simultaneous induction on $n \ge 0$, $\text{act}(X, FB, n) = \text{C}$ and $\text{act}(FB, X, n) = \text{C}$ for all $n \ge 0$.
- **Against itself ($X$ vs $X$):** As shown above, $\text{act}(X, DB, 0) = \text{C}$ and $\text{act}(X, DB, m) = \text{D}$ for all $m \ge 1$. Thus when $Y = X$, the atom $d = \text{act}(X, DB, m)$ is `C` at $m = 0$ and `D` at all $m \ge 1$, so $d \to \Box\neg d$ holds at all $m \ge 0$. By induction on $n \ge 0$, $a = \text{act}(X, X, m) = \text{C}$ holds for all $m < n$, so $\text{act}(X, X, n) = \text{C}$ for all $n \ge 0$.

Checking with `/work/check.py`:
```
$ python3 check.py "B(a & (d -> B(~d)))"
depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES
```

---

## 2. Impossibility Proof for Modal Depth $< 2$ (Question 2)

**Theorem 1.** *No fully modalized formula $\varphi_X$ of modal depth $0$ or $1$ (of any size, with or without constants) defines a prudent agent.*

**Proof.** Let $\varphi_X$ be a fully modalized formula of modal depth $\le 1$.

### Case 1: Modal depth $0$
A fully modalized formula of modal depth $0$ contains no boxes $\Box$, and since every atom must occur inside at least one $\Box$, it contains no atoms (`a`, `c`, `d`) at all. Thus $\varphi_X$ is a boolean combination of the constants `T` and `F`, so its truth value is constant across all opponents and all worlds. In particular, $\text{act}(X, CB, n) = \text{act}(X, FB, n)$ for all $n$, so $X$ cannot defect against CooperateBot while cooperating with FairBot.

### Case 2: Modal depth $1$
Suppose $\varphi_X$ has modal depth $1$. Since $\varphi_X$ is fully modalized of depth $1$, it is a boolean combination of box subformulas $\Box\psi_1, \dots, \Box\psi_k$, where each $\psi_i = \psi_i(a, c, d)$ has modal depth $0$ (i.e., $\psi_i$ is a purely propositional formula in the atoms $a, c, d$ and constants $T, F$).

1. **Behavior at world $m = 0$ against `CB` and `FB`:**
   - When the opponent is $Y = CB$ ($\varphi_{CB} = \top$), we have $\text{act}(CB, Z, m) = T$ for every agent $Z$ and every world $m \ge 0$. Therefore, against $CB$, the triple of atoms $(a, c, d)$ at world $m$ is:
     $$v^{CB}(m) = \big(\text{act}(CB, X, m),\ \text{act}(CB, CB, m),\ \text{act}(CB, DB, m)\big) = (T, T, T) \qquad \text{for all } m \ge 0.$$
   - When the opponent is $Y = FB$ ($\varphi_{FB} = \Box a$), at world $m = 0$ the box $\Box a$ holds vacuously (as $\{k : k < 0\} = \emptyset$), so $\text{act}(FB, Z, 0) = T$ for every agent $Z$. Therefore, against $FB$, the triple of atoms $(a, c, d)$ at world $m = 0$ is:
     $$v^{FB}(0) = \big(\text{act}(FB, X, 0),\ \text{act}(FB, CB, 0),\ \text{act}(FB, DB, 0)\big) = (T, T, T).$$

2. **Equality of $X$'s actions against `CB` and `FB` at world $n = 1$:**
   Because each $\psi_i(a, c, d)$ is a depth-$0$ propositional formula and $v^{CB}(0) = v^{FB}(0) = (T, T, T)$, each $\psi_i$ has the exact same truth value at world $m = 0$ against both $CB$ and $FB$:
   $$\text{ev}(\psi_i, 0, X, CB) = \psi_i(T, T, T) = \text{ev}(\psi_i, 0, X, FB).$$
   At world $n = 1$, the truth value of $\Box\psi_i$ is $\forall m < 1,\ \text{ev}(\psi_i, m, X, Y) \equiv \text{ev}(\psi_i, 0, X, Y) = \psi_i(T, T, T)$ for both $Y = CB$ and $Y = FB$. Since $\varphi_X$ is a boolean combination of $\Box\psi_1, \dots, \Box\psi_k$, it follows that:
   $$\text{act}(X, FB, 1) = \text{act}(X, CB, 1).$$

3. **Stationarity of $X$'s action against `CB` for all worlds $n \ge 1$:**
   Against $CB$, $v^{CB}(m) = (T, T, T)$ at *every* world $m \ge 0$. Thus for every depth-$0$ formula $\psi_i$ and every world $m \ge 0$, $\text{ev}(\psi_i, m, X, CB) = \psi_i(T, T, T)$. Consequently, for every world $n \ge 1$:
   $$\text{ev}(\Box\psi_i, n, X, CB) = \bigwedge_{m=0}^{n-1} \psi_i(T, T, T) = \psi_i(T, T, T) = \text{ev}(\Box\psi_i, 1, X, CB).$$
   Since every $\Box\psi_i$ has the same truth value at all worlds $n \ge 1$ against $CB$, so does their boolean combination $\varphi_X$:
   $$\text{act}(X, CB, n) = \text{act}(X, CB, 1) \qquad \text{for all } n \ge 1.$$

4. **Contradiction with prudence:**
   - For $X$ to defect against CooperateBot in the limit, we must have $\lim_{n\to\infty} \text{act}(X, CB, n) = F$. By Step 3, this forces $\text{act}(X, CB, 1) = F$.
   - By Step 2, $\text{act}(X, FB, 1) = \text{act}(X, CB, 1) = F$, so $X$ defects against FairBot at world $m = 1$.
   - However, FairBot's formula is $\varphi_{FB} = \Box a$, so at every world $n \ge 2$:
     $$\text{act}(FB, X, n) = \bigwedge_{m=0}^{n-1} \text{act}(X, FB, m) \le \text{act}(X, FB, 1) = F.$$
     Thus $\text{act}(FB, X, n) = F$ for all $n \ge 2$, meaning FairBot defects against $X$ in the limit (`FB_reply = D`).

Hence $X$ cannot simultaneously defect against CooperateBot and induce FairBot to cooperate with $X$. No agent of modal depth $< 2$ is prudent. $\blacksquare$

---

## 3. Characterization of Depth-2 Prudent Agents and Exact Minimal Size (Question 3)

We give both (A) a complete semantic characterization of all depth-$2$ prudent agents and (B) a rigorous proof of the exact minimal symbol size of prudent formulas across all modal depths.

### A. Complete Characterization of Depth-2 Prudent Agents

For any opponent $Y$ and world $m \ge 0$, let
$$v^Y(m) = \big(\text{act}(Y, X, m),\ \text{act}(Y, CB, m),\ \text{act}(Y, DB, m)\big) \in \{T, F\}^3$$
be the valuation of $(a, c, d)$ at world $m$, and let
$$S^Y_m = \{ v^Y(k) \mid 0 \le k < m \} \subseteq \{T, F\}^3$$
be the set of atom valuations occurring strictly before world $m$.

- **Expressive completeness at depth 1:** For any depth-$0$ formula $\chi$, $\text{ev}(\Box\chi, m, X, Y) = T \iff S^Y_m \subseteq \chi^{-1}(T)$. Conversely, for any subset $S_0 \subseteq \{T, F\}^3$, the depth-$1$ formula
  $$\beta_{S_0} := \Box\Big(\bigvee_{u \in S_0} (v = u)\Big) \land \bigwedge_{u \in S_0} \neg\Box(v \ne u)$$
  holds at world $m$ if and only if $S^Y_m = S_0$. Therefore, a behavior at world $m$ is definable by a modal formula $\psi$ of depth $\le 1$ if and only if it is a boolean function $\psi(v^Y(m), S^Y_m)$ of the pair $(v^Y(m), S^Y_m)$.
- **Expressive completeness at depth 2:** A fully modalized formula $\varphi_X$ of depth $\le 2$ is a boolean combination of boxes $\Box\psi_i$ with $\text{depth}(\psi_i) \le 1$. Since $\text{ev}(\Box\psi, n, X, Y) = \bigwedge_{m=0}^{n-1} \psi(v^Y(m), S^Y_m)$ depends only on the history set of pairs
  $$\mathcal{H}^Y_n := \big\{ (v^Y(m), S^Y_m) \;\big|\; 0 \le m < n \big\},$$
  and each individual pair $p = (v_0, S_0)$ can be detected in $\mathcal{H}^Y_n$ by $\neg\Box\neg((v = v_0) \land \beta_{S_0})$, a behavior across Kripke frames is definable by a fully modalized formula of depth $\le 2$ if and only if it is a boolean function $\Phi(\mathcal{H}^Y_n)$ of the history set $\mathcal{H}^Y_n$.

Denote the atom triples by $TTT = (T,T,T)$, $TTF = (T,T,F)$, $TFF = (T,F,F)$, and $FFF = (F,F,F)$, and define the seven canonical pairs $(v, S)$:
$$\begin{aligned}
p_0 &= (TTT,\ \emptyset), & p_1 &= (TTF,\ \{TTT\}), & p_2 &= (TTF,\ \{TTT, TTF\}), 
p_3 &= (TFF,\ \{TTT, TTF\}), & p_4 &= (TFF,\ \{TTT, TTF, TFF\}), 
q_{CB} &= (TTT,\ \{TTT\}), & q_{DB,0} &= (FFF,\ \emptyset), & q_{DB,1} &= (FFF,\ \{FFF\}).
\end{aligned}$$

#### 1. Exact Characterization of Single-Box Depth-2 Prudent Agents ($\varphi_X = \Box\psi$)

**Theorem 2 (Single-Box Characterization).** *Let $\psi$ be any formula of modal depth $1$. Then $\varphi_X = \Box\psi$ is prudent if and only if $\psi(v, S)$ satisfies the following 7-point truth table:*
1. $\psi(p_0) = \psi(p_1) = \psi(p_2) = \psi(p_3) = \psi(p_4) = T$, *and*
2. $\psi(q_{CB}) = \psi(q_{DB,0}) = F$
*(with $\psi(v, S)$ arbitrary on all other $2048 - 7 = 2041$ pairs $(v, S)$).*

**Proof.** For $\varphi_X = \Box\psi$, $\text{act}(X, Y, n) = \forall (v, S) \in \mathcal{H}^Y_n,\ \psi(v, S) = T$ is monotonically non-increasing in $n$: once $\text{act}(X, Y, n) = F$ at some world $n$, it remains $F$ for all $n' \ge n$.
- **FairBot (`FB`):** For FairBot ($\Box a$) to cooperate with $X$ in the limit, we need $\text{act}(X, FB, m) = T$ for *all* $m \ge 0$. Under this condition, $\text{act}(FB, X, m) = T$ for all $m \ge 0$, while $\text{act}(FB, CB, m) = T$ for all $m \ge 0$, $\text{act}(FB, DB, 0) = T$, and $\text{act}(FB, DB, m) = F$ for all $m \ge 1$. Thus $v^{FB}(0) = TTT$ and $v^{FB}(m) = TTF$ for $m \ge 1$, so $\mathcal{H}^{FB}_\infty = \{p_0, p_1, p_2\}$. Hence $X$ and $FB$ cooperate with each other iff $\psi(p_0) = \psi(p_1) = \psi(p_2) = T$.
- **CooperateBot (`CB`):** Since $v^{CB}(m) = TTT$ for all $m \ge 0$, we have $\mathcal{H}^{CB}_1 = \{p_0\}$ and $\mathcal{H}^{CB}_n = \{p_0, q_{CB}\}$ for all $n \ge 2$. Given $\psi(p_0) = T$, $X$ defects against $CB$ iff $\psi(q_{CB}) = F$ (which yields $\text{act}(X, CB, \cdot) = (T, T, F, F, \dots)$).
- **DefectBot (`DB`) and Self (`X`):** Since $v^{DB}(m) = FFF$ for all $m \ge 0$, $\mathcal{H}^{DB}_1 = \{q_{DB,0}\}$ and $\mathcal{H}^{DB}_n = \{q_{DB,0}, q_{DB,1}\}$ for $n \ge 2$. By monotonicity of $\Box\psi$, for $X$ to cooperate with itself in the limit, we must have $\text{act}(X, X, m) = T$ for all $m \ge 0$. At $m = 0$, $v^X(0) = TTT$, so $(v^X(0), S^X_0) = p_0$. At $m = 1$, $v^X(1) = (T, T, \text{act}(X, DB, 1))$ and $S^X_1 = \{TTT\}$. If $\text{act}(X, DB, 1) = T$, then $(v^X(1), S^X_1) = (TTT, \{TTT\}) = q_{CB}$, which would force $\text{act}(X, X, 2) = \psi(q_{CB}) = F$, contradicting self-cooperation! Therefore we *must* have $\text{act}(X, DB, 1) = F$, i.e., $\psi(q_{DB,0}) = F$. Then $\text{act}(X, DB, \cdot) = (T, F, F, F, \dots)$, which fixes $(v^X(1), S^X_1) = p_1$, $(v^X(2), S^X_2) = p_3$, and $(v^X(m), S^X_m) = p_4$ for all $m \ge 3$ (provided $\text{act}(X, X, m) = T$). Thus $\text{act}(X, X, n) = T$ for all $n \ge 0$ iff $\psi(p_3) = \psi(p_4) = T$. $\blacksquare$

#### 2. Characterization of General Depth-2 Prudent Agents

More generally, for an arbitrary fully modalized depth-$2$ formula $\varphi_X$ represented by a boolean function $\Phi(\mathcal{H})$ on history sets, the exact conditions for prudence are:
1. **FairBot condition:** $\Phi(\emptyset) = \Phi(\{p_0\}) = \Phi(\{p_0, p_1\}) = \Phi(\{p_0, p_1, p_2\}) = T$.
2. **CooperateBot condition:** $\Phi(\{p_0, q_{CB}\}) = F$, which forces $\text{act}(X, CB, \cdot) = (T, T, F, F, F, \dots)$.
3. **DefectBot condition:** $\Phi(\{q_{DB,0}, q_{DB,1}\}) = F$, which forces $\text{act}(X, DB, \cdot) = (T, \delta_1, F, F, F, \dots)$ where $\delta_1 = \Phi(\{q_{DB,0}\}) \in \{F, T\}$.
4. **Self-cooperation condition:** Since $\text{act}(X, CB, m) = \text{act}(X, DB, m) = F$ for all $m \ge 2$, the self-play valuation is $v^X(0) = TTT$, $v^X(1) = (T, T, \delta_1)$, and $v^X(m) = (\text{act}(X, X, m), F, F) \in \{TFF, FFF\}$ for all $m \ge 2$. Because $\mathcal{H}^X_n$ is monotonically non-decreasing within a finite set of at most $6$ reachable pairs, $\mathcal{H}^X_n$ stabilizes in at most $5$ worlds to a terminal history set $\mathcal{H}^X_\infty$, and $X$ cooperates with itself iff $\Phi(\mathcal{H}^X_\infty) = T$.

---

### B. Exact Minimal Symbol Size of Prudent Formulas

Following the syntax of `check.py`, each atom (`a`, `c`, `d`), constant (`T`, `F`), unary operator (`~`, `B`), and binary connective (`&`, `|`, `->`) counts as $1$ symbol.

**Theorem 3 (Minimal Size Bound).** *Across all modal depths:*
1. *With constants (`T`, `F`), the minimal symbol size of a prudent formula is **7**, achieved uniquely (up to semantic equivalence) by `B(a & (d -> B(F)))`.*
2. *Without constants, the minimal symbol size of a prudent formula is **8**, achieved (up to syntactic rearrangement of `a & (d -> ...)`) only by the three formulas `B(a & (d -> B(~d)))`, `B(a & (d -> B(~a)))`, and `B(a & (d -> B(~c)))`.*

*(Note: If `A -> B` is not treated as primitive and is instead expanded to `~A | B` as in `check.py`'s internal AST, the minimal AST node count is **8** with constants and **9** without constants.)*

**Proof.** Let $\varphi_X$ be any prudent formula (of any modal depth $D \ge 2$). Suppose $\varphi_X$ has $L$ leaf occurrences (atoms or constants), $B_{\text{cnt}}$ box operators `B`, and $N_{\text{cnt}}$ negations `~`. Since every binary connective (`&`, `|`, `->`) joins two subtrees, the number of binary connectives is $L - 1$, giving the exact size identity:
$$\text{size}(\varphi_X) = 2L - 1 + B_{\text{cnt}} + N_{\text{cnt}}.$$
By Theorem 1, $D = \text{depth}(\varphi_X) \ge 2$, so $B_{\text{cnt}} \ge 2$.

#### Step 1: Without constants, $N_{\text{cnt}} \ge 1$
Against CooperateBot, $(a, c, d) = (T, T, T)$ at every world $m \ge 0$. All operators in $\{a, c, d, T, \land, \lor, \to, \Box\}$ preserve constant truth $T^\omega = (T, T, T, \dots)$ (since $T \land T = T \lor T = (T \to T) = T$ and $\Box(T^\omega) = T^\omega$). Therefore, any formula without the constant `F` and without negation `~` evaluates to $T$ at every world against CooperateBot. Since $\varphi_X$ defects against CooperateBot, any constant-free prudent formula must have $N_{\text{cnt}} \ge 1$.

#### Step 2: Every prudent formula has $L \ge 3$ leaf occurrences
Since $\varphi_X$ is prudent, FairBot cooperates with $X$ in the limit, which forces $\text{act}(X, FB, \cdot) = T^\omega$. Meanwhile, $\lim_{n\to\infty} \text{act}(X, CB, n) = F$ and $\lim_{n\to\infty} \text{act}(X, DB, n) = F$. On the three opponents $(FB, CB, DB)$, let $E_k = (\underbrace{T, \dots, T}_k, F, F, \dots)$ for $k \ge 1$, and $E_0 = F^\omega$.
- Under $\neg$ and $\Box$, these sequences satisfy:
  $$\Box(T^\omega) = T^\omega,\qquad \Box(E_k) = E_{k+1} \ \ (k \ge 0),\qquad \Box(\neg E_k) = E_1 \ \ (k \ge 1),$$
  where the last equality holds because $(\neg E_k)_0 = F$, so $\Box(\neg E_k)$ already becomes $F$ at world $1$.
- On $(FB, CB, DB)$, the leaves have triples of sequences:
  $$T = (T^\omega, T^\omega, T^\omega),\quad F = (F^\omega, F^\omega, F^\omega),\quad a = c = (T^\omega, T^\omega, F^\omega),\quad d = (E_1, T^\omega, F^\omega).$$
- Consequently, applying any unary chain $U$ of `~` and `B` to any leaf $z \in \{a, c, d, T, F\}$ produces a triple $U(z)$ on $(FB, CB, DB)$ of one of only two types:
  - **Type I ($FB = CB$):** $U(z) = (s_1, s_1, s_2)$ has the exact same sequence on $FB$ and $CB$, with $s_1, s_2 \in \{T^\omega, E_k, \neg E_k \mid k \ge 0\}$. (This holds for all $z \in \{a, c, T, F\}$ and for any $U(d)$ containing $\Box\neg$, since $\Box(\neg E_k) = E_1 = \Box(F^\omega)$ merges $FB$ and $CB$.)
  - **Type II ($\pm \Box^k d$):** $U(d) = \Box^k d = (E_{k+1}, T^\omega, E_k)$ or $\neg\Box^k d = (\neg E_{k+1}, F^\omega, \neg E_k)$ for some $k \ge 0$.

This immediately rules out $L = 1$: no Type I or Type II triple is $T^\omega$ on $FB$ while having limit $F$ on $CB$.

Now suppose for contradiction that $L = 2$, so $\varphi_X = U_0(U_1(x) \circ U_2(y))$ for some unary chains $U_0, U_1, U_2$ and a single binary connective $\circ \in \{\land, \lor, \to\}$. Since $\Box s = T^\omega \iff s = T^\omega$ and $\Box s$ is never $F^\omega$, for $U_0(\psi)$ to equal $T^\omega$ on $FB$ while having limit $F$ on $CB$ and $DB$, the binary combination $\psi = U_1(x) \circ U_2(y)$ must be constant on $FB$ (say $T^\omega$, absorbing any outer $\neg$ into $\circ$) and have limit $F$ on both $CB$ and $DB$:
- If both $U_1(x), U_2(y)$ are Type I, then $\psi$ is identical on $FB$ and $CB$, impossible.
- If both $U_1(x), U_2(y)$ are Type II, then on $CB$ both are constant ($T^\omega$ or $F^\omega$) from world $0$ onward and agree with their values on $FB$ at world $0$ (since $(E_{k+1})_0 = T = (T^\omega)_0$), so $\psi$ on $CB$ is constant and equals $\psi_0$ on $FB$, impossible.
- If one is Type II (say $U_1(d) = (E_{k+1}, T^\omega, E_k)$, absorbing any $\neg$ into $\circ$) and the other is Type I ($U_2(y) = (s_1, s_1, s_2)$ with $\ell_1 := \lim_{m\to\infty} (s_1)_m$):
  - For $m > k$ on $CB$, $(T^\omega)_m = T$, so we need $T \circ \ell_1 = F$.
  - For $m > k$ on $FB$, $(E_{k+1})_m = F$, so we need $F \circ \ell_1 = T$.
  - Thus $u \circ \ell_1 = \neg u$. Among $\circ \in \{\land, \lor, \to\}$, this is possible only if $\circ$ is $\to$ and $\ell_1 = F$ (i.e., $\psi = U_1(d) \to U_2(y)$).
  - However, on $DB$, $U_1(d) = E_k$ has limit $\lim_{m\to\infty} (E_k)_m = F$. Therefore, on $DB$, $\psi = U_1(d) \to U_2(y)$ has limit $F \to \lim s_2 = T$, so $U_0(\psi) = \Box^r \psi$ also has limit $T$ on $DB$, contradicting defection against $DB$!

Thus no formula with $L \le 2$ leaves (of any modal depth or size) can be prudent. Hence $L \ge 3$.

#### Step 3: Concluding the Size Bounds and Uniqueness
Substituting $L \ge 3$ and $B_{\text{cnt}} \ge 2$ into $\text{size}(\varphi_X) = 2L - 1 + B_{\text{cnt}} + N_{\text{cnt}}$:
1. **With constants:**
   $$\text{size}(\varphi_X) \ge 2(3) - 1 + 2 + 0 = 7,$$
   with equality only when $L = 3$, $B_{\text{cnt}} = 2$, and $N_{\text{cnt}} = 0$.
2. **Without constants:** Since $N_{\text{cnt}} \ge 1$ by Step 1,
   $$\text{size}(\varphi_X) \ge 2(3) - 1 + 2 + 1 = 8,$$
   with equality only when $L = 3$, $B_{\text{cnt}} = 2$, and $N_{\text{cnt}} = 1$.

Moreover, at equality ($L = 3, B_{\text{cnt}} = 2$), $\text{depth}(\varphi_X) = 2$ forces the two boxes to be nested, so $\varphi_X = \Box\psi$ (since any outer negation would make $\text{act}(X, FB, 0) = F$). By Theorem 2:
- To distinguish $p_0 = (TTT, \emptyset)$ from $q_{CB} = (TTT, \{TTT\})$, the inner box $\Box\chi$ must satisfy $\chi(TTT) = F$, so $\chi = \bot$ (with constants, size $1$) or $\chi \in \{\neg a, \neg c, \neg d\}$ (without constants, size $2$).
- Since $L = 3$ and one leaf is inside $\Box\chi$, $\psi$ combines two unboxed atoms with $\Box\chi$. To distinguish $p_1 = (TTF, \{TTT\})$ from $q_{CB} = (TTT, \{TTT\})$, one unboxed atom must be $d$; to distinguish $p_3 = (TFF, \{TTT, TTF\})$ from $q_{DB,0} = (FFF, \emptyset)$, the other unboxed atom must be $a$.
- Evaluating on $\{p_0, p_1, p_3, q_{CB}, q_{DB,0}\}$ uniquely forces $\psi \equiv a \land (d \to \Box\chi)$, yielding `B(a & (d -> B(F)))` (size 7 with constants) and `B(a & (d -> B(~d)))`, `B(a & (d -> B(~a)))`, `B(a & (d -> B(~c)))` (size 8 without constants). $\blacksquare$

### Computational Verification

The script `/work/verify_results.py` independently verifies all results above:
- Exhaustively enumerating all pairwise-inequivalent fully modalized depth-$\le 2$ formulas up to size $8$ confirms $0$ prudent formulas of size $\le 6$ (with constants) or $\le 7$ (without constants), exactly $1$ equivalence class at size $7$ with constants (`B(a & (d -> B(F)))`), and $3$ equivalence classes at size $8$ without constants (`B(a & (d -> B(~a)))`, `B(a & (d -> B(~c)))`, `B(a & (d -> B(~d)))`).
- Testing Theorem 2's 7-pair criterion across all $2,420$ pairwise-inequivalent depth-$\le 1$ formulas $\psi$ up to size $7$ yields $0$ mismatches against `check.py`.
