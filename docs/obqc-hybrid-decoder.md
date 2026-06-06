# OBQC Hybrid Decoder Simulation

## RGBW × Soroban-Coded Decimal 40-State Decoder

This document describes the Phase 2 software simulation for a near-term deterministic OBQC / SCD hybrid decoder.

The model combines:

- 4 optical channels: **R, G, B, W**
- 10 soroban-coded decimal digit patterns: **0–9**
- 1 active-channel marker bit: **M**
- nearest-neighbor decoding under noise

The goal is to test whether a 40-state symbolic alphabet can be decoded under simplified optical sensor noise.

---

## Why the marker bit is necessary

A simple `4 channels × 5 bits` implementation is not sufficient.

The 5-bit soroban-coded decimal pattern for digit 0 is:

```text
0 = [0, 0, 0, 0, 0]
```

If this pattern is placed in an RGBW channel without an active-channel marker, then:

```text
R0 = all-zero vector
G0 = all-zero vector
B0 = all-zero vector
W0 = all-zero vector
```

These four states collapse into the same vector.

That means a nominal 40-state alphabet is not actually distinguishable. Even with zero noise, at least three of the four zero states are structurally ambiguous.

The simulator therefore uses:

```text
[M, H, L4, L3, L2, L1]
```

Where:

- `M` = active-channel marker
- `H` = five-bead equivalent
- `L4, L3, L2, L1` = lower one-bead equivalents

This changes the state vector from:

```text
4 channels × 5 bits = 20 dimensions
```

to:

```text
4 channels × 6 bits = 24 dimensions
```

The result is a structurally unique 40-state alphabet.

---

## State definition

Each symbolic state is defined as:

```text
state = color_channel × scd_digit
```

Where:

```text
color_channel ∈ {R, G, B, W}
scd_digit ∈ {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
```

Total states:

```text
4 × 10 = 40 states
```

Each state is encoded as a 4 × 6 matrix:

```text
rows:    R, G, B, W
columns: M, H, L4, L3, L2, L1
```

Only one color channel is active per state in this first model.

---

## Decoder model

The decoder uses nearest-neighbor classification.

For each noisy received vector, it computes the Euclidean distance to all 40 ideal templates and selects the closest template.

```text
decoded_state = argmin distance(received_signal, template_state)
```

The simulator also tracks:

- best distance
- second-best distance
- margin between nearest and second-nearest templates
- accuracy
- error rate
- reject rate
- confusion matrix

---

## Simulated noise and hardware effects

The simulator is intentionally simplified, but it includes first-stage stress-test parameters:

- additive Gaussian noise
- background light level
- simplified RGBW channel crosstalk
- clipping / saturation
- optional ADC-like quantization
- reject threshold
- nearest-neighbor margin threshold

These parameters are not a substitute for real CMOS/LED measurement.

They are meant to identify whether the state mapping is structurally valid and how quickly decoding fails as noise increases.

---

## How to run

Single run:

```bash
python simulator/obqc_hybrid_decoder.py --noise 0.05 --iterations 10000
```

Noise sweep:

```bash
python simulator/obqc_hybrid_decoder.py \
  --sweep \
  --noise 0.30 \
  --sweep-steps 31 \
  --iterations 10000 \
  --csv simulator/results/obqc_hybrid_decoder_sweep.csv
```

With crosstalk and quantization:

```bash
python simulator/obqc_hybrid_decoder.py \
  --noise 0.10 \
  --crosstalk 0.05 \
  --background 0.02 \
  --quantization-levels 256 \
  --iterations 10000
```

---

## Interpreting results

Example output:

```text
OBQC / SCD Hybrid Decoder Simulation
-------------------------------------
Noise level:        0.0500
Iterations:         10000
Accuracy:           100.0000%
Error rate:         0.0000%
Reject rate:        0.0000%
Mean margin:        ...
Minimum margin:     ...
Mean best distance: ...
Note: observed zero errors in this finite run does not prove true zero error.
```

Important interpretation:

- Observed 0% error in a finite simulation run does not prove true zero error.
- Nearest-neighbor decoding can work well under idealized conditions.
- Real hardware must test crosstalk, temperature drift, calibration instability, detector saturation, shot noise, read noise, dark current, position misalignment, aging, and optical path variation.

---

## What this simulation supports

This simulation supports the following limited claims:

1. A 40-state RGBW × SCD symbolic alphabet can be made structurally unique by adding an active-channel marker bit.
2. Nearest-neighbor decoding can be tested under configurable noise.
3. The decoder can measure where error begins to increase as noise rises.
4. The margin between nearest and second-nearest templates can be used as a rejection or confidence metric.

---

## What this simulation does not prove

This simulation does not prove:

- hardware feasibility,
- quantum advantage,
- zero error in physical systems,
- universal superiority over binary encoding,
- CMOS/LED manufacturing readiness,
- reliable operation under real environmental conditions,
- unlimited scaling of state count.

It is a Phase 2 software model for testing a corrected symbolic mapping and decoding pipeline.

---

## Recommended next steps

1. Add real measured sensor noise data.
2. Replace Gaussian-only noise with hardware-calibrated noise models.
3. Test non-uniform channel gains.
4. Add drift over time.
5. Add calibration errors.
6. Add repeated-symbol voting.
7. Compare nearest-neighbor decoding with threshold decoding and probabilistic decoding.
8. Test the same 40-state alphabet against a binary baseline.
9. Generate confusion matrix plots.
10. Validate with an actual RGBW LED + CMOS/color-sensor prototype.

---

## Safe technical framing

Use this wording:

> Under simplified simulation assumptions, the marker-bit RGBW × SCD model can decode a structurally unique 40-state alphabet using nearest-neighbor classification. Hardware validation is required before making performance claims.

Avoid this wording:

> This proves perfect 40-state optical decoding.

---

## Related files

- [simulator/obqc_hybrid_decoder.py](../simulator/obqc_hybrid_decoder.py)
- [docs/scd-rgb-optical-bead-encoding.md](scd-rgb-optical-bead-encoding.md)
- [README.md](../README.md)
