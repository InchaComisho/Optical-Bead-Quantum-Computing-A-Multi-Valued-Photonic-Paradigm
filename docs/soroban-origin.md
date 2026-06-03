# Conceptual Origin: From Soroban to Optical Beads

**Part of:** [Optical Bead Computing](../README.md)

---

## 1. The Soroban Abacus

The soroban is a Japanese abacus used for arithmetic calculation. It consists of a rectangular frame holding a set of vertical rods, each carrying five movable beads: one *heaven bead* (worth 5) above a horizontal bar and four *earth beads* (worth 1 each) below.

A number from 0 to 9 is represented on a single rod by the configuration of beads pushed toward the horizontal bar:

| Value | Earth beads toward bar | Heaven bead toward bar |
|---|---|---|
| 0 | 0 | No |
| 1 | 1 | No |
| 2 | 2 | No |
| 3 | 3 | No |
| 4 | 4 | No |
| 5 | 0 | Yes |
| 6 | 1 | Yes |
| 7 | 2 | Yes |
| 8 | 3 | Yes |
| 9 | 4 | Yes |

A multi-digit number is encoded as the simultaneous bead configuration across all rods. A practitioner does not read each rod serially — they perceive and manipulate the entire spatial pattern at once.

This *whole-pattern* representation is the foundational analogy for Optical Bead Computing.

---

## 2. Flash Mental Arithmetic (Flash Anzan)

Flash anzan (フラッシュ暗算, *flash mental arithmetic*) is a practice in which a series of numbers is displayed on a screen at extremely high speed (sometimes 0.2 seconds per number), and the practitioner computes the running total mentally.

Advanced practitioners achieve accurate results with sequences of 10 or more three-digit numbers displayed at 0.2 seconds each — a computational throughput that no conscious symbol-by-symbol calculation can explain.

Research on expert flash anzan practitioners suggests:

1. **Mental soroban simulation:** Experts report mentally visualizing a soroban and *moving the beads* rather than processing digit symbols.
2. **Spatial pattern operation:** The operation is performed on the spatial bead image, not on an abstract numerical representation.
3. **Right-hemisphere involvement:** Neuroimaging studies suggest greater involvement of spatial/visuospatial processing regions compared to novices who rely more on symbolic arithmetic circuits.

The critical implication is that numerical addition, when mediated by a soroban representation, becomes a *spatial pattern transformation* rather than a symbolic rule application.

---

## 3. From Soroban Patterns to Optical Bead Patterns

Optical Bead Computing (OBC) extends the soroban analogy from physical beads on rods to optical states across degrees of freedom of light.

The mapping is as follows:

| Soroban | Optical Bead Computing |
|---|---|
| A physical rod | A degree of freedom of light (e.g., wavelength axis) |
| A bead on a rod | A discrete state within one degree of freedom |
| Bead position (up / down / count) | State level within that DOF (e.g., 450 nm / 532 nm / 633 nm) |
| Full bead configuration across all rods | Optical bead state vector B = (λ, P, φ, τ, w, s, ℓ) |
| Soroban arithmetic operation | Optical state transformation |
| Visual pattern recognition in flash anzan | Multi-dimensional optical state decoding |

The analogy captures the structural principle: **an information unit is not a single binary value but a structured multi-dimensional configuration that is encoded, transformed, and recognized as a whole pattern.**

---

## 4. Why Pattern Logic Matters

In binary computing, a symbol is either 0 or 1. To represent a number, we concatenate multiple binary symbols. Each symbol carries no structural relationship to the others; the meaning is in their positional sequence.

In soroban representation, the structural configuration is inherently spatial and multi-valued. The "digit 7" is not a sequence of three bits; it is a specific spatial arrangement (two earth beads + one heaven bead) that a practitioner perceives as a single gestalt.

The hypothesis motivating OBQC is that this structural difference — pattern-as-unit versus symbol-sequence — may have computational implications when transferred to optical systems. Specifically:

- Multi-dimensional optical states may allow more information to be packed into a single measurement event.
- Pattern-based decoding may be robust to certain classes of noise (e.g., if the pattern as a whole shifts but remains distinguishable from all other patterns).
- For tasks that are structurally pattern-like (recognition, classification, lookup), the optical bead representation may map more naturally to the task structure.

These hypotheses are not proven. They define the research questions that OBQC is designed to investigate.

---

## 5. What the Analogy Does Not Claim

The soroban-to-optical-beads analogy is a conceptual and structural motivation. It does not imply:

- That optical bead computing is equivalent to human mental arithmetic.
- That it replicates neurological pattern processing.
- That it automatically achieves the speed or accuracy of expert flash anzan practitioners.
- That the analogy proves any computational advantage.

The analogy is a *design principle*: structure information as multi-dimensional patterns rather than binary sequences, and explore what computational tasks this structure supports effectively.

---

*Back to [README.md](../README.md)*
