# OBQC Hybrid Decoder Simulation

## RGBW × Soroban-Coded Decimal 40-State Decoder

This document describes the Phase 2 software simulation for a near-term deterministic OBQC / SCD hybrid decoder.

The model combines:

- 4 optical channels: **R, G, B, W**
- 10 soroban-coded decimal digit patterns: **0–9**
- 1 active-channel marker bit: **M**
- nearest-neighbor decoding under noise
- confidence, margin, error-risk, and reject logic

The goal is to test whether a 40-state symbolic alphabet can be decoded under simplified optical sensor noise, and whether uncertain readings can be rejected before a false output is emitted.

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
- confidence score
- error-risk score
- accepted accuracy
- false accept rate
- reject rate
- calibration request rate
- confusion matrix

---

## Layer 5: Correction and Verification Safeguard

The correction and verification layer avoids forced decoding when the optical reading is ambiguous.

In simple terms:

```text
If the signal is clear, accept and decode.
If the signal is ambiguous, reject and request calibration or re-measurement.
```

The simulator uses these safeguards:

- `margin_threshold`: reject if the best and second-best candidates are too close.
- `reject_threshold`: reject if the closest template is still too far away.
- `confidence_threshold`: reject if the confidence proxy is too low.
- `error_risk_threshold`: reject if the error-risk proxy is too high.

A rejected signal is not treated as a successful output. It is treated as a request for recalibration, re-measurement, larger sensing area, stronger signal margin, better shielding, or stricter decoding conditions.

---

## Confidence and error risk

The simulator estimates confidence from the two nearest distances.

This is not a calibrated physical probability.

It is a bounded confidence proxy:

```text
confidence = softmax(-best_distance, -second_best_distance)
error_risk = 1 - confidence
```

Interpretation:

- If the best state is much closer than the second-best state, confidence rises.
- If the best and second-best states are close, confidence falls.
- Low confidence does not prove the answer is wrong.
- High confidence does not prove the answer is correct.

This is a decision-support metric for rejection, not a guarantee.

---

## False accept rate

The important safety metric is not only total accuracy.

The key safety metric is:

```text
false_accept_rate = accepted but wrong outputs / total trials
```

This measures cases where the safeguard failed to reject an incorrect output.

The simulator also reports:

```text
false_accept_rate_of_accepted = accepted but wrong outputs / accepted outputs
```

This distinguishes two different problems:

- Too many rejects: safe but inefficient.
- Too many false accepts: unsafe because wrong outputs pass through.

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
- confidence threshold
- error-risk threshold

These parameters are not a substitute for real CMOS/LED measurement.

They are meant to identify whether the state mapping is structurally valid and how quickly decoding fails as noise increases.

---

## How to run

Single run:

```bash
python simulator/obqc_hybrid_decoder.py --noise 0.05 --iterations 10000
```

With a margin safeguard:

```bash
python simulator/obqc_hybrid_decoder.py \
  --noise 0.12 \
  --margin-threshold 0.40 \
  --iterations 10000
```

With confidence and error-risk safeguards:

```bash
python simulator/obqc_hybrid_decoder.py \
  --noise 0.12 \
  --confidence-threshold 0.80 \
  --error-risk-threshold 0.20 \
  --iterations 10000
```

Noise sweep:

```bash
python simulator/obqc_hybrid_decoder.py \
  --sweep \
  --noise 0.30 \
  --sweep-steps 31 \
  --iterations 10000 \
  --margin-threshold 0.40 \
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
Noise level:                  0.1200
Iterations:                   10000
Accepted count:               ...
Rejected count:               ...
Correct accepted count:       ...
False accepted count:         ...
Correct output rate / total:  ...
Accepted accuracy:            ...
False accept rate / total:    ...
False accept rate / accepted: ...
Reject rate:                  ...
Calibration request rate:     ...
Mean margin:                  ...
Minimum margin:               ...
Mean confidence:              ...
Mean error risk:              ...
```

Important interpretation:

- Observed 0% false accepts in a finite simulation run does not prove true zero false-accept risk.
- A high reject rate may mean the system is safe but inefficient.
- A low reject rate with many false accepts means the threshold is too permissive.
- Hardware validation must include crosstalk, temperature drift, calibration instability, detector saturation, shot noise, read noise, dark current, position misalignment, aging, and optical path variation.

---

## What this simulation supports

This simulation supports the following limited claims:

1. A 40-state RGBW × SCD symbolic alphabet can be made structurally unique by adding an active-channel marker bit.
2. Nearest-neighbor decoding can be tested under configurable noise.
3. The decoder can measure where error begins to increase as noise rises.
4. The margin between nearest and second-nearest templates can be used as a rejection or confidence metric.
5. A correction layer can trade throughput for safety by rejecting ambiguous readings.

---

## What this simulation does not prove

This simulation does not prove:

- hardware feasibility,
- quantum advantage,
- zero error in physical systems,
- zero false-accept risk,
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

> Under simplified simulation assumptions, the marker-bit RGBW × SCD model can decode a structurally unique 40-state alphabet using nearest-neighbor classification. The correction layer can reject ambiguous readings, but hardware validation is required before making performance or safety claims.

Avoid this wording:

> This proves perfect 40-state optical decoding or complete prevention of false outputs.

---

## Related files

- [simulator/obqc_hybrid_decoder.py](../simulator/obqc_hybrid_decoder.py)
- [docs/scd-rgb-optical-bead-encoding.md](scd-rgb-optical-bead-encoding.md)
- [README.md](../README.md)

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and proposer of the academic framework of Natural Complementary Science.  
Definer of the Cooling Credit Framework, and founder and original author of the Natural Cooling Value Evaluation Protocol.  
Definer and systematizer of the causal structure of global warming and its complete solution.

Master presents global warming not merely as a problem of CO₂ concentration, but as an integrated failure involving forest loss, soil degradation, disruption of water circulation, weakening of water phase-transition processes, weakening of atmospheric circulation, ocean circulation, food circulation and organic matter circulation, weakening of evapotranspiration, cloud formation and rainfall circulation, and the shutdown of natural cooling feedbacks.  
The proposed solution connects emission reduction, recovery of carbon fixation sources, physical cooling, reactivation of natural cooling functions, MRV, Cooling Credit, and Civilization OS into an open public framework.

Master publicly develops and shares work through NOTE, GitHub, and other public media, centered on natural-law philosophy, planetary circulation restoration, and co-creation with AI.

## License

CC BY 4.0

This article is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
Sharing, redistribution, translation, adaptation, and reuse are permitted as long as proper attribution is given.