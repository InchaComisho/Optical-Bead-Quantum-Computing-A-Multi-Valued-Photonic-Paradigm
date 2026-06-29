# SCD and RGB Optical Bead Encoding

## A cautious framework for soroban-inspired multivalued pattern computing

> **Status:** Conceptual framework / simulation target  
> **Scope:** SCD, LED-CMOS, RGB/white optical bead encoding  
> **Important:** This document makes limited, testable claims only. It does not claim universal superiority over existing computing systems.

---

## 1. Purpose

This document defines a cautious and testable version of a soroban-inspired decimal pattern encoding system for electronic and optical prototypes.

The goal is to define a reproducible experimental target:

1. encode decimal digits using **Soroban-Coded Decimal (SCD)**,
2. map SCD bead patterns into LED / CMOS-readable optical patterns,
3. extend a single SCD cell with RGB/white active optical layers,
4. evaluate which errors are detectable, which are silent, and which require additional redundancy.

The framework should make limited, falsifiable claims rather than broad performance claims.

---

## 2. SCD: Soroban-Coded Decimal

A soroban rod represents one decimal digit using:

- one upper bead worth 5,
- four lower beads worth 1 each.

A simple electronic SCD cell can therefore be represented as five bits:

```text
[H, L4, L3, L2, L1]
```

where:

- `H` is the upper bead,
- `L4..L1` are the lower beads,
- lower beads use a thermometer-style code.

One possible encoding is:

| Digit | SCD pattern |
|---:|---|
| 0 | `00000` |
| 1 | `00001` |
| 2 | `00011` |
| 3 | `00111` |
| 4 | `01111` |
| 5 | `10000` |
| 6 | `10001` |
| 7 | `10011` |
| 8 | `10111` |
| 9 | `11111` |

Only 10 of the 32 possible 5-bit patterns are valid. The other 22 patterns are structurally invalid.

This gives SCD a useful property: many random bit errors become invalid patterns and can be detected.

However, detection is not complete. Some bit flips transform one valid SCD digit into another valid SCD digit. These are **silent errors** unless additional checks are used.

---

## 3. What SCD can and cannot claim

### Safe claim

SCD defines a smaller valid state space inside the full 5-bit space. This can increase the chance that random bit flips become detectable invalid states.

### Unsafe claim

SCD should not be described as complete error detection without extra redundancy.

For single-bit flips across the 10 SCD digits:

- 50 possible single-bit flip events exist: 10 digits × 5 bit positions.
- 24 become structurally invalid and are detected.
- 26 become different valid digits and are silent errors.

So, under this specific single-bit flip model:

```text
single-bit detected fraction ~= 48%
single-bit silent-error fraction ~= 52%
```

This is still useful, but it is not perfect.

Error correction requires additional redundancy, repeated sampling, parity, distance expansion, calibration confidence, or higher-level validation.

---

## 4. LED-CMOS mapping

A near-term prototype can map an SCD pattern to a small LED array and read it with a CMOS sensor.

```text
SCD bits -> LED bead pattern -> CMOS image -> decoder -> digit
```

This is a classical optical/electronic pattern-recognition prototype.

Possible near-term hardware:

- RGB LED matrix or micro-LED display,
- CMOS image sensor or color camera,
- optical isolation / enclosure,
- threshold or nearest-neighbor decoder,
- calibration frame for color and intensity drift.

The prototype can test whether spatial bead-like patterns are easier to decode, visualize, or validate than ordinary binary encodings under some workloads.

---

## 5. RGB / white optical bead extension

A cautious optical extension is to use active color layers:

```text
R, G, B, White
```

where:

- `R` = red emission,
- `G` = green emission,
- `B` = blue emission,
- `White` = simultaneous red + green + blue emission.

Combining 4 active optical layers with 10 SCD digit patterns gives:

```text
4 layers × 10 digit patterns = 40 symbols
```

This is better described as a **40-symbol alphabet** than as a proven 40-base computer.

The safer term is:

```text
40-state RGB/white SCD optical bead cell
```

---

## 6. Why black/off is excluded in the default model

A previous extension considered:

```text
Black/off, R, G, B, White
```

which would give:

```text
5 layers × 10 digit patterns = 50 symbols
```

However, black/off is physically weaker as an information-bearing active layer because it represents absence of light. It is more vulnerable to:

- ambient light,
- dark-current offset,
- sensor bias,
- neighboring LED leakage,
- threshold ambiguity,
- inability to distinguish an intended zero-emission marker from a missing or failed signal.

Therefore, the default prototype should first use only active optical layers:

```text
R / G / B / White
```

This gives a lower but more robust 40-state model.

---

## 7. Critical issue: digit zero and layer identification

There is an important design issue.

The SCD digit `0` is represented as:

```text
00000
```

If a layer is encoded only by coloring active beads, then digit zero has no lit bead. In that case, the detector cannot know whether the symbol was:

```text
R-zero, G-zero, B-zero, or White-zero
```

because all would appear blank.

Therefore, a practical RGB/white SCD optical bead cell needs a **layer marker** or **reference pixel**.

A minimal symbol can be represented as:

```text
[layer marker] + [5 SCD bead positions]
```

The layer marker is always lit in the selected color layer, even when the digit pattern is zero.

This changes the physical design from a pure 5-position cell to a **5+1 position cell**:

```text
M | H L4 L3 L2 L1
```

where `M` is the optical layer marker.

This marker improves decodability and makes the 40-state alphabet well-defined.

---

## 8. Decoder principle

A simple decoder can use nearest-neighbor matching.

1. Capture the marker and five bead positions as RGB intensity vectors.
2. Determine the layer from the marker.
3. Read each bead position relative to the expected layer color.
4. Convert active/inactive bead positions to a 5-bit SCD pattern.
5. Decode the SCD pattern.
6. Reject invalid SCD patterns.
7. Reject low-confidence color or intensity measurements.

This produces three possible outcomes:

| Outcome | Meaning |
|---|---|
| Correct | decoded layer and digit match the transmitted symbol |
| Detected error | invalid SCD pattern, invalid layer, or low confidence |
| Silent error | decoded as a different valid layer/digit |

The key metric is not only total error rate, but the ratio of detected errors to silent errors.

---

## 9. Safe falsifiable claims

The current safe claims are:

1. SCD uses only 10 valid states out of 32 possible 5-bit patterns.
2. SCD can structurally detect some invalid patterns without a separate parity bit.
3. SCD does not detect all bit errors.
4. RGB/white active layers can define a 40-symbol alphabet when paired with SCD.
5. A practical 40-state cell requires a marker/reference position to identify the layer for digit zero.
6. LED-CMOS prototypes can test this idea with low-cost classical hardware.
7. Actual performance must be measured under noise, crosstalk, drift, calibration error, and optical alignment error.

---

## 10. Claims to avoid until measured

Until experimental evidence exists, avoid claiming:

- complete error detection,
- guaranteed error-free computing,
- replacement for existing computing systems in all workloads,
- large energy reductions without benchmarks,
- production readiness.

The correct public framing is:

> This is a soroban-inspired multivalued pattern-encoding framework that may be testable with low-cost LED-CMOS prototypes.

---

## 11. Proposed next simulation

The next simulation target is:

```text
simulator/rgb_scd_40_state_decoder.py
```

It should evaluate:

- 40-state alphabet construction,
- marker-based layer identification,
- SCD pattern decoding,
- Gaussian sensor noise,
- RGB channel crosstalk,
- ambient offset,
- detected vs silent error rates.

This simulation should explicitly report when errors are detected and when they are silent.

---

## 12. Conclusion

The core idea remains valuable: soroban-inspired spatial patterns may offer a useful way to explore multivalued, visually decodable, pattern-oriented computation.

The most credible path is not to claim universal superiority, but to build a small falsifiable prototype:

```text
SCD -> RGB/white LED pattern -> CMOS capture -> decoder -> error statistics
```

If the prototype shows robust detection, low silent-error rates, and useful pattern-recognition behavior under realistic noise, the framework becomes stronger.

If it does not, the model can be revised.

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
