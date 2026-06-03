# Comparative Simulation Framework

**Part of:** [Optical Bead Computing](../README.md)

---

## Purpose

This document describes the comparative simulation framework included in this repository. The framework is **not** a proof of universal superiority for any encoding scheme. It is a falsifiable, reproducible set of simulations designed to expose measurable trade-offs between four classes of information representation:

1. Binary integer / BCD electronic encoding
2. Soroban-Coded Decimal (SCD) electronic encoding
3. Binary photonic encoding (two optical states)
4. High-dimensional optical bead encoding (multi-valued photonic)

The simulations operate under controlled, explicitly stated assumptions. Results depend on those assumptions. Changing the noise model, alphabet design, or metric definition changes the results. The source code and random seeds are published so that any result can be reproduced, challenged, or extended.

No claims are made about:
- Universal computational superiority of any scheme
- Quantum advantage
- Practical deployability without hardware validation
- Real-world performance outside the stated model assumptions

---

## Electronic Comparison

### Binary Integer Representation

A decimal digit 0–9 can be stored in a standard 4-bit binary integer. All 16 possible 4-bit patterns (0000 to 1111) are valid bit patterns from the perspective of binary logic. The six patterns corresponding to values 10–15 are "above the decimal range" but are not structurally illegal in binary hardware.

Key properties:
- 4 bits per decimal digit
- All 16 patterns decode to some integer; none are inherently flagged as errors by the hardware
- Storage-optimal for representing values 0–15
- No structural correspondence to soroban bead logic
- Carry and borrow in decimal arithmetic require software-level handling

### BCD (Binary-Coded Decimal)

BCD encodes decimal digits 0–9 as 4-bit patterns identical to their binary representation. The six patterns 10–15 (1010 to 1111) are defined as invalid for decimal purposes. BCD is widely used in financial arithmetic, display controllers, and decimal-centric embedded systems.

Key properties:
- 4 bits per decimal digit (same as binary)
- 10 valid states out of 16 possible (62.5% valid)
- 6 invalid states (37.5% detectable by range check)
- Compact decimal digit storage
- No structural soroban bead logic; invalid states come only from the decimal range boundary

### Soroban-Coded Decimal (SCD)

SCD encodes decimal digits 0–9 as 5-bit patterns: one heaven bead bit (H, value 5) and four earth bead bits (L4, L3, L2, L1) in thermometer code (no gaps allowed).

The thermometer constraint means that the only valid lower-bead patterns are:
`0000, 0001, 0011, 0111, 1111`

Any other pattern (e.g., `0101`, `1010`, `1100`) is structurally invalid — it cannot arise from a legitimate soroban bead configuration.

Key properties:
- 5 bits per decimal digit (25% more than BCD)
- 10 valid states out of 32 possible (31.25% valid)
- 22 invalid states (68.75% detectable by pattern check)
- Pattern-oriented: each valid state directly mirrors a physical soroban rod configuration
- More invalid states means more random bit-flip errors are detectable
- Not storage-optimal; not intended for maximum compression

### Electronic Encoding Comparison Table

| Model | Bits per decimal digit | Valid states | Invalid states | Valid fraction | Main advantage | Main limitation |
|---|---:|---:|---:|---:|---|---|
| Binary integer | 4 | 16 / 16 | 0 / 16 | 100% | Storage-efficient; all patterns usable | No decimal error detection from pattern alone |
| BCD | 4 | 10 / 16 | 6 / 16 | 62.5% | Compact decimal digit; standard support | Fewer invalid states for error detection |
| SCD | 5 | 10 / 32 | 22 / 32 | 31.25% | Soroban pattern logic; more detectable error states | 25% more storage than BCD |

---

## Electronic Error Simulation

### Model

A random bit-flip model is applied to each encoded digit:

- Each bit in the stored code word is independently flipped with probability p
- p values span a range from very low (0.001, representing high-reliability storage) to moderate (0.10, representing a degraded or noisy channel)
- 10,000 trials per digit per p value are performed
- Random seed is fixed for reproducibility

### Outcome categories

For each trial:
- **Correct:** the decoded value equals the original digit
- **Detected error:** the received bit pattern is structurally invalid (out of decimal range for BCD; non-thermometer pattern for SCD)
- **Silent error:** the received bit pattern decodes to a *different valid digit* — the error is not detectable from the pattern alone

### Key distinction: detection is not correction

A detected error means the system knows something went wrong. It does not automatically know what the correct value was. Error *correction* requires redundancy (e.g., parity bits, Reed-Solomon, repetition coding) which is outside the scope of this comparison.

SCD has more invalid states (22/32 = 68.75%) than BCD (6/16 = 37.5%), so a higher fraction of random bit-flip errors will land in an invalid state and be detected. However:

- SCD uses 25% more bits per digit
- More bits per digit means more bit-flip opportunities at the same p
- The net benefit of SCD's error detection versus its larger code word size is a measurable trade-off, not an automatic win

The simulator reports all three metrics (correct, detected, silent) separately so the trade-off is visible.

---

## Photonic Comparison

### Binary Photonic Encoding

Binary optical encoding uses two states per symbol, typically:
- presence/absence of a pulse
- two phase states (0 and π)
- two polarization states (H and V)

With only two states, the minimum inter-state separation distance is maximized for a given physical space. This makes binary photonic encoding very robust to noise and crosstalk. However, each symbol carries only 1 bit of information.

### High-Dimensional Optical Bead Encoding

Optical bead encoding uses M states per symbol, where M > 2. States are distributed across a multi-dimensional space defined by degrees of freedom of light (wavelength, polarization, phase, time-bin, spatial mode, etc.).

As M increases:
- Bits per symbol = log₂(M) increases
- More information is carried per symbol transmission
- The minimum inter-state separation distance decreases for the same physical space
- Noise sensitivity, crosstalk, and calibration requirements increase

### Simulation Model

The photonic comparison uses a simplified, normalized D-dimensional state-space model:

- Each symbol is represented as a point in [0, 1]^D
- Alphabets are constructed as regular grid points in D-dimensional space
- Gaussian noise is added independently to each dimension
- Nearest-neighbor decoding is used

This is a classical noisy-channel model, not a quantum or physical optics simulation. It captures the geometric relationship between alphabet size, state-space dimension, noise tolerance, and decoding accuracy under idealized conditions.

### Metrics

| Metric | Definition |
|---|---|
| M | Alphabet size (number of distinct symbols) |
| D | State-space dimension (degrees of freedom used) |
| bits_per_symbol | log₂(M) |
| separability_margin | Minimum Euclidean distance between any two states in the alphabet |
| symbol_error_rate (SER) | Fraction of symbols decoded incorrectly under noise |
| throughput_proxy | bits_per_symbol × (1 − SER) — approximate useful information per symbol |

The throughput proxy is a simplified metric. It does not account for channel capacity, forward error correction, latency, or hardware cost. It is useful for visualizing the trade-off between symbol density and noise sensitivity.

### Expected qualitative results

- Binary photonic (M=2) will show very low SER even at high noise levels, because the two states are maximally separated
- As M increases for fixed D, the SER rises faster with noise, and the throughput proxy peaks at some M that depends on the noise level
- For higher D with the same M, the separability margin is larger (states are spread across more dimensions), which may improve SER at the cost of more hardware degrees of freedom

---

## Quantum-Inspired Toy Channel

A third simulator (`qudit_inspired_channel.py`) models a highly simplified channel comparison between M=2 binary-like encoding and M>2 qudit-like encoding.

The model introduces:
- **Loss probability p_loss:** the symbol is erased (detected, not decoded) — analogous to photon loss in a real optical channel
- **Confusion probability p_confuse:** the symbol is decoded as a wrong symbol

This is an **analytical toy model**, not a physical quantum simulation. It does not:
- Model quantum coherence, superposition, or entanglement
- Compute quantum channel capacity (Holevo bound, etc.)
- Account for optical loss, detector efficiency, or dark counts accurately
- Prove or disprove quantum advantage for any task

Its purpose is to illustrate the trade-off between symbol alphabet size, channel loss, and measurement reliability in a transparent, falsifiable way.

---

## Fairness Rules

All simulations in this framework follow these rules:

1. **Fixed random seed (42):** all stochastic simulations use the same seed for reproducibility
2. **Symmetric sweep:** both (or all) compared schemes are evaluated at the same parameter values (p, sigma, M)
3. **Multi-point evaluation:** results are reported across a range of noise levels, not at a single cherry-picked value
4. **All metrics reported:** correct rate, detected error rate, silent error rate, and throughput proxy are all reported — not just the best-looking metric
5. **No single winner:** the simulator reports raw numbers and notes the trade-offs; it does not declare a "winner"
6. **CSV output:** all results are written to CSV files for independent analysis, re-plotting, and verification
7. **Stated assumptions:** every simulator file documents its assumptions in comments; changing assumptions changes results

---

## Limitations of This Framework

- The photonic model is a geometric approximation, not a physical optics simulation
- The electronic model assumes uniform random bit flips; real hardware has correlated failure modes
- The qudit model is a toy analytical model, not a quantum information-theoretic calculation
- No hardware has been built; all results are from software simulation under stated assumptions
- Real optical systems have additional noise sources not modeled here (see `docs/limitations.md`)
- Detection of invalid states (SCD, BCD) does not imply correction; correction requires additional redundancy

---

*Back to [README.md](../README.md)*  
*See also: [docs/limitations.md](limitations.md) | [simulator/README.md](../simulator/README.md)*
