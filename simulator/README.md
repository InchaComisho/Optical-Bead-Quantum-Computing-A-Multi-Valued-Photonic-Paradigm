# Optical Bead Computing — Simulator

This directory contains a minimal Python simulator for the Optical Bead Computing (OBC) framework.

**No mandatory external dependencies.** The core scripts run on Python 3.7+ standard library only. `numpy` and `matplotlib` are used for enhanced output if available but are not required.

---

## Files

| File | Description |
|---|---|
| `encode_decode.py` | Alphabet definition, encoding, nearest-neighbor decoding, SER measurement |
| `noise_model.py` | Gaussian noise, temporal jitter, channel drift, spectral crosstalk |
| `confusion_matrix.py` | Multi-trial evaluation, confusion matrix output, optional heatmap plot |
| `soroban_decimal.py` | Soroban-Coded Decimal (SCD) 5-bit cell: encode, decode, increment, add, display |

---

## Quick Start

```bash
# Run the basic encode/decode demo
python encode_decode.py

# Run the noise model demo
python noise_model.py

# Run the confusion matrix evaluator (default settings)
python confusion_matrix.py

# Run the Soroban-Coded Decimal (SCD) electronic extension demo
python soroban_decimal.py

# Run with custom sigma and trial count
python confusion_matrix.py --sigma 0.07 --trials 300

# Limit to 12 states
python confusion_matrix.py --sigma 0.05 --states 12

# Run SER sweep over a range of noise levels
python confusion_matrix.py --sweep

# Show heatmap plot (requires matplotlib)
python confusion_matrix.py --plot

# Save heatmap plot to file
python confusion_matrix.py --save confusion.png
```

---

## Alphabet Structure

The default alphabet is built from three degrees of freedom:

- **Wavelength:** 4 normalized levels → [0.00, 0.33, 0.67, 1.00]
- **Polarization:** 4 normalized levels → [0.00, 0.33, 0.67, 1.00]
- **Time-bin:** 3 normalized levels → [0.00, 0.50, 1.00]

Total alphabet size: 4 × 4 × 3 = **48 states**

All values are normalized to [0, 1]. Physical interpretation:
- 0.00 / 0.33 / 0.67 / 1.00 in wavelength corresponds to, e.g., 450 nm / 532 nm / 633 nm / 780 nm
- 0.00 / 0.33 / 0.67 / 1.00 in polarization corresponds to H / D / V / A linear states
- 0.00 / 0.50 / 1.00 in time-bin corresponds to early / middle / late bin

---

## Noise Models

### Gaussian noise (`noise_model.py`)

Additive Gaussian noise applied independently to each dimension. Models detector noise, source intensity fluctuations, and environmental perturbations.

```
sigma = 0.01   → very low noise; nearly all states distinguishable
sigma = 0.05   → moderate noise; typical laboratory conditions
sigma = 0.10   → high noise; practical decoding begins to fail for many states
sigma = 0.20   → severe noise; most states confused with neighbors
```

### Temporal jitter

Displacement of the time-bin coordinate by a Gaussian-distributed jitter value. Models timing uncertainty in pulse arrival.

### Channel drift

Slow deterministic shift in all coordinates proportional to elapsed time since calibration. Models thermal expansion, laser wavelength drift.

### Spectral crosstalk

Random shift in the wavelength coordinate within a bounded range. Models adjacent channel leakage from finite filter bandwidth.

### Combined realistic model

`realistic_noise()` in `noise_model.py` applies all noise types in sequence. Use this for the most realistic SER estimates.

---

## Expected Results

Under default Gaussian noise model with 48-state alphabet:

| σ | Expected SER (approximate) |
|---|---|
| 0.01 | < 0.001 |
| 0.02 | ~ 0.005 |
| 0.05 | ~ 0.05–0.15 |
| 0.10 | ~ 0.30–0.50 |
| 0.18 | ~ 0.60–0.80 |

Actual values depend on the random seed. Run with `--trials 500` for more stable estimates.

---

## Optional Dependencies

```bash
# For heatmap visualization
pip install matplotlib

# For faster matrix operations
pip install numpy
```

Both packages are optional. The simulator runs correctly without them.

---

## Extending the Simulator

To test a smaller or larger alphabet:

```python
from encode_decode import build_alphabet

# 2 wavelengths × 2 polarizations × 2 time-bins = 8 states
small_alphabet = build_alphabet(
    wavelengths=[0.0, 1.0],
    polarizations=[0.0, 1.0],
    timebins=[0.0, 1.0]
)

# 4 wavelengths × 6 polarizations × 4 time-bins = 96 states
large_alphabet = build_alphabet(
    wavelengths=[0.0, 0.33, 0.67, 1.0],
    polarizations=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    timebins=[0.0, 0.33, 0.67, 1.0]
)
```

To use the realistic noise model in the confusion matrix:

```python
from encode_decode import decode
from noise_model import realistic_noise

# Replace add_noise(state, sigma) with realistic_noise(state, ...)
```

---

*Back to [README.md](../README.md)*
