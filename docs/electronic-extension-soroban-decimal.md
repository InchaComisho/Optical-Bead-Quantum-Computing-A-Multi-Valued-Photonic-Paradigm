# Electronic Extension: Soroban-Coded Decimal Logic

**Part of:** [Optical Bead Computing](../README.md)

---

## Overview

Optical Bead Computing encodes information as multi-dimensional optical patterns inspired by the soroban abacus. The same soroban structural logic can also be mapped to electronic circuits, giving a complementary electronic representation of decimal digits.

This document describes **Soroban-Coded Decimal (SCD)** logic: a 5-bit constrained decimal cell that mirrors the physical structure of a soroban rod in digital hardware.

---

## 1. The Soroban Decimal Cell

A single soroban rod represents a decimal digit from 0 to 9 using two categories of beads:

- **One upper bead (heaven bead):** value 5 when active
- **Four lower beads (earth beads):** value 1 each when active

The digit value is:

```
digit = 5 * H + count(L1, L2, L3, L4)
```

This maps naturally to a 5-bit digital cell:

```
D = (H, L1, L2, L3, L4)
```

where H ∈ {0, 1} and each Li ∈ {0, 1}.

---

## 2. Thermometer-Coded Lower Beads

For a unique, visually interpretable, and error-detectable encoding, the four lower beads use a **thermometer code**: lower beads activate from right to left in order, with no gaps.

Valid lower bead patterns form a contiguous block:

```
count = 0  →  L = 0000
count = 1  →  L = 0001
count = 2  →  L = 0011
count = 3  →  L = 0111
count = 4  →  L = 1111
```

This gives 5 valid lower states × 2 upper states = 10 valid digit codes.

---

## 3. Complete SCD Encoding Table

| Decimal | H | L4 | L3 | L2 | L1 | 5-bit code |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | `0 0000` |
| 1 | 0 | 0 | 0 | 0 | 1 | `0 0001` |
| 2 | 0 | 0 | 0 | 1 | 1 | `0 0011` |
| 3 | 0 | 0 | 1 | 1 | 1 | `0 0111` |
| 4 | 0 | 1 | 1 | 1 | 1 | `0 1111` |
| 5 | 1 | 0 | 0 | 0 | 0 | `1 0000` |
| 6 | 1 | 0 | 0 | 0 | 1 | `1 0001` |
| 7 | 1 | 0 | 0 | 1 | 1 | `1 0011` |
| 8 | 1 | 0 | 1 | 1 | 1 | `1 0111` |
| 9 | 1 | 1 | 1 | 1 | 1 | `1 1111` |

Out of 2^5 = 32 possible 5-bit patterns, only 10 are valid. The 22 invalid patterns function as detectable error states.

---

## 4. Structural Properties

### 4.1 Direct decimal representation

Each SCD cell holds exactly one decimal digit. There is no implicit conversion step between the stored bit pattern and its decimal value. This contrasts with:

- **Binary-coded decimal (BCD):** 4-bit code, no structural correspondence to soroban
- **Standard binary:** requires multi-digit conversion for decimal output
- **SCD:** the bit pattern directly mirrors the physical bead position

### 4.2 Carry and borrow structure

**Addition of 1** to a cell:
- If lower count < 4: increment lower count (activate next L bit)
- If lower count = 4 and H = 0: reset lower to 0000, set H = 1 (soroban "5-complement carry up")
- If lower count = 4 and H = 1: reset all to 0000, generate carry to next higher cell

This closely matches the mechanical carry logic of a physical soroban, where carry involves moving the heaven bead and resetting earth beads.

### 4.3 Subtraction of 1 (borrow structure)

- If lower count > 0: decrement lower count
- If lower count = 0 and H = 1: set lower to 1111 (= 4), clear H (borrow from the 5-group)
- If lower count = 0 and H = 0: set all to 1111 1 (= 9), generate borrow from next cell

Again, this mirrors soroban borrow mechanics.

### 4.4 Error detection

Any 5-bit pattern not in the valid set of 10 is an illegal state. A simple validity check is:

```
valid(D) = True iff
  lower_count(L) in {0,1,2,3,4}   AND
  lower_is_thermometer(L)
```

where `lower_is_thermometer` checks that lower bits form a contiguous block (no gaps). Invalid states can be detected and flagged without additional parity bits.

---

## 5. Comparison with Existing Decimal Encodings

| Encoding | Bits/digit | Valid patterns | Error detection | Soroban structure |
|---|---|---|---|---|
| **SCD (this proposal)** | 5 | 10 / 32 | Yes (22 invalid states) | Direct |
| BCD (8421) | 4 | 10 / 16 | Partial (6 invalid states) | None |
| Excess-3 | 4 | 10 / 16 | Partial | None |
| 2-of-5 code | 5 | 10 / 32 | Yes (22 invalid) | None |
| Gray code decimal | 4 | 10 / 16 | Partial | None |

SCD uses the same bit count as 2-of-5 code but has a structurally motivated encoding derived from soroban logic.

**Note:** SCD is not intended to compete with compact encodings for storage density. Its value is structural: it mirrors the soroban's bead logic in silicon, making it a natural bridge between the photonic, electronic, and cognitive models in this framework.

---

## 6. Multi-Digit Numbers

A multi-digit decimal number is represented as an array of SCD cells, one per decimal digit:

```
N-digit number:  [ D_{n-1}, D_{n-2}, ..., D_1, D_0 ]
                   most significant       least significant

Each D_i = (H_i, L4_i, L3_i, L2_i, L1_i)
```

This parallels the soroban's multi-rod layout where each rod independently holds one digit.

For a 4-digit number (0–9999): 4 × 5 = 20 bits total, compared to:
- BCD: 16 bits (more compact but no soroban structure)
- Binary: 14 bits minimum (most compact but no decimal structure)

---

## 7. Relationship to Optical Bead Computing

The SCD encoding is the **electronic analog** of an optical bead state in the OBQC framework:

| Domain | Information unit | DOF 1 | DOF 2 | Valid states |
|---|---|---|---|---|
| Soroban (physical) | Bead configuration on one rod | Heaven bead H | Earth beads L1–L4 (thermometer) | 10 |
| SCD (electronic) | 5-bit decimal cell | H bit | L1–L4 bits (thermometer) | 10 of 32 |
| OBC (optical) | Optical bead state B | λ, P, φ, ... | Multi-DOF encoding | Alphabet-defined |

All three representations share the same structural principle: **a value is a multi-component pattern**, not a linear binary sequence.

This alignment allows the three domains to share:
- Encoding table structures
- Pattern-based operation logic
- Error detection through invalid-state checking

---

## 8. Hardware Implementation Notes

### Validity checker (combinational logic)

```
valid(H, L4, L3, L2, L1) =
  NOT (L3 AND NOT L4)  -- no gap: L3 can only be 1 if L4 is 1
  AND NOT (L2 AND NOT L3)
  AND NOT (L1 AND NOT L2)
```

This is a 5-input combinational circuit requiring 3 AND + 3 NOT + 2 AND gates.

### Increment-by-1 (sequential logic sketch)

```
carry_out = H AND (L4 AND L3 AND L2 AND L1)

if NOT carry_out:
    if L4 AND L3 AND L2 AND L1:
        -- lower full, H = 0 → set H = 1, clear lower
        H' = 1, L' = 0000
    else:
        -- activate next lower bead
        L'[i] = first 0 from right set to 1
        H' = H
else:
    -- overflow: reset to 0, carry to next cell
    H' = 0, L' = 0000
```

### FPGA / ASIC suitability

SCD logic is straightforward to implement in FPGA LUTs or ASIC standard cells. The wider cell (5 bits vs 4 for BCD) is offset by simpler carry logic and built-in error detection.

---

## 9. Potential Applications

| Application | Description |
|---|---|
| Decimal arithmetic unit | Hardware decimal adder/subtractor with soroban carry structure |
| Decimal display controller | Direct mapping from SCD cell to 7-segment or dot-matrix soroban display |
| Pattern-based decimal logic | Hardware implementation of pattern-matching operations on decimal values |
| Educational hardware | Teaching soroban arithmetic principles via electronic circuit |
| Hybrid optical-electronic bridge | SCD as intermediate representation between OBC optical states and digital electronics |
| Error-aware decimal computation | Exploit invalid states for lightweight fault detection in arithmetic pipelines |

---

## 10. Limitations and Open Questions

- **Area cost:** 5 bits per digit vs 4 for BCD means 25% more storage per digit.
- **Toolchain support:** No standard CAD tool libraries exist for SCD; custom cell definitions required.
- **Speed:** Soroban-structured carry chains are not necessarily faster than optimized binary adders; benchmarking required.
- **Use case scope:** SCD is suited for specific pattern-oriented decimal applications, not general-purpose arithmetic replacement.
- **No silicon prototype:** As of 2026-06-03, SCD is a proposed logic model without a fabricated hardware implementation.

---

*Back to [README.md](../README.md)*  
*See also: [soroban-origin.md](soroban-origin.md) | [optical-bead-state-model.md](optical-bead-state-model.md)*

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and advocate of the academic framework of Natural Complementary Science.  
Publicly active in natural-law philosophy, planetary circulation restoration, and co-creation with AI.

---

## License

CC BY 4.0

This article is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
Sharing, redistribution, translation, adaptation, and reuse are permitted as long as proper attribution is given.
