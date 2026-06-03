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
| `liquid_medium_noise.py` | Sealed liquid optical cell noise model (absorption, scattering, thermal phase drift) |
| `electronic_binary_vs_scd.py` | **Comparison:** BCD vs SCD under random bit flips |
| `photonic_binary_vs_obqc.py` | **Comparison:** Binary photonic vs multi-state optical bead under Gaussian noise |
| `qudit_inspired_channel.py` | **Toy model:** M-level qudit-inspired channel (analytical, NOT quantum simulation) |
| `hybrid_quantum_support_energy.py` | **Toy energy model:** OBQC auxiliary layer vs baseline hybrid quantum support system (E_cryo unchanged) |
| `pattern_vs_binary_operation_cost.py` | **Abstract cost model:** Sequential binary pipeline vs pattern-recognition pipeline |
| `run_comparisons.py` | Run all comparison simulators in sequence |
| `results/` | Directory for generated CSV output files |

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

# --- Comparison simulators ---
# Run all comparison simulators at once
python run_comparisons.py

# Or run each comparison simulator individually
python electronic_binary_vs_scd.py
python photonic_binary_vs_obqc.py
python qudit_inspired_channel.py

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

## Optical Medium Comparison

```bash
python optical_medium_comparison.py
python optical_medium_comparison.py --trials 5000
python optical_medium_comparison.py --plot
python optical_medium_comparison.py --save-plot medium_comparison.png
```

Compares simplified environmental and material noise models for six optical media:
`open_air`, `sealed_air`, `sealed_liquid`, `acrylic_block`, `glass_quartz`, `fiber_waveguide`.

Each medium is characterized by component noise sigmas (dust, humidity, thermal RI drift,
bubble scattering, stress birefringence, alignment drift). The combined effective sigma
is used to simulate symbol error rate for M-ary alphabets in D-dimensional state space.

What it shows:
- `open_air` has the highest effective noise (sigma = 0.095) -> highest SER
- `glass_quartz` and `fiber_waveguide` have the lowest noise -> best SER at any M
- `acrylic_block` has significant stress birefringence (degrades polarization DOF)
- `sealed_liquid` has thermal RI drift that is critical for phase encoding
- Higher D spreads states across more dimensions, preserving margin at higher M

Output: console table (D=2, 4, 7) + `results/optical_medium_comparison.csv`

**TOY MODEL WARNING:** Noise parameters are qualitative engineering estimates, NOT
measured values. Use this to guide experimental design, not as hardware specifications.

See [docs/optical-medium-stabilization.md](../docs/optical-medium-stabilization.md).

---

## Sealed Liquid Optical Bead Medium

```bash
python liquid_medium_noise.py
python liquid_medium_noise.py --path-length 1.0 --delta-T 0.1
```

Models noise sources specific to a sealed transparent liquid optical cell used as
the optical bead transmission medium. Extends `noise_model.py` with:

- **Absorption attenuation** (Beer-Lambert: I = I0 * exp(-alpha * L))
- **Scattering noise** from bubbles and impurities (multiplicative lognormal)
- **Thermal phase drift** from temperature-dependent refractive index change
- **Differential wavelength transmission** (wavelength-dependent alpha)
- **Thermal gradient beam steering** (optional spatial mode displacement)

Includes presets for: `water_clean`, `water_uncontrolled`, `glycerol_water`,
`immersion_oil`, and `open_air_baseline` (for comparison).

**Key finding from simulation:**  
At 5 cm path length, a 0.1 K temperature deviation causes ~5 rad phase drift.
Phase encoding is impractical in a liquid cell without sub-millikelvin temperature
control or sub-millimeter path length. Wavelength and polarization are the
recommended starting DOFs for liquid-medium prototypes.

See [docs/sealed-liquid-optical-bead-medium.md](../docs/sealed-liquid-optical-bead-medium.md).

---

## Electronic Binary vs SCD

```bash
python electronic_binary_vs_scd.py
python electronic_binary_vs_scd.py --trials 5000
```

Compares Binary-Coded Decimal (BCD, 4-bit) against Soroban-Coded Decimal (SCD, 5-bit)
under a random independent bit-flip noise model.

What it measures:
- **correct_rate** — fraction of trials decoded to the correct digit
- **detected_error_rate** — fraction of trials with a structurally invalid decoded pattern (caught)
- **silent_error_rate** — fraction of trials decoded to a different valid digit (undetected)

Key trade-off:
- BCD uses 4 bits per digit; SCD uses 5 bits per digit (+25% storage overhead)
- BCD has 6/16 = 37.5% invalid states; SCD has 22/32 = 68.75% invalid states
- SCD therefore converts more random bit-flip errors into *detected* errors
- Neither scheme provides error *correction* without additional redundancy

Output: console table + `results/electronic_binary_vs_scd.csv`

**This simulation does NOT claim SCD beats BCD in all cases.**
See `docs/comparative-simulation-framework.md` for full explanation.

---

## Photonic Binary vs OBQC

```bash
python photonic_binary_vs_obqc.py
python photonic_binary_vs_obqc.py --trials 1000
python photonic_binary_vs_obqc.py --plot          # requires matplotlib
python photonic_binary_vs_obqc.py --save-plot throughput.png
```

Compares binary photonic encoding (M=2, 1 bit/symbol) against multi-state
optical bead encoding (M=4 to 128, up to 7 bits/symbol) under a simplified
Gaussian noise model in normalized D-dimensional state space.

What it measures:
- **symbol_error_rate (SER)** — fraction of symbols decoded incorrectly
- **bits_per_symbol** — log2(M)
- **throughput_proxy** — bits_per_symbol * (1 - SER)
- **separability_margin** — minimum distance between any two states in the alphabet

Key result (model-specific):
- Binary M=2 maintains near-zero SER across all tested noise levels
- Higher-M configurations carry more bits/symbol but SER rises faster with noise
- Using more dimensions (higher D) for the same M preserves the separability margin

Output: console table + `results/photonic_binary_vs_obqc.csv`

**WARNING: This is NOT a full quantum or physical optics simulation.**
It is a simplified geometric model. Results depend on stated model assumptions only.

---

## Qudit-Inspired Toy Channel

```bash
python qudit_inspired_channel.py
python qudit_inspired_channel.py --monte-carlo --trials 50000
```

A toy analytical comparison between M=2 binary-like and M>2 qudit-like symbol
transmission, parameterized by loss probability and confusion probability.

What it measures:
- **correct_rate** = (1 - p_loss) * (1 - p_confuse)
- **erasure_rate** = p_loss
- **symbol_error_rate** = (1 - p_loss) * p_confuse
- **throughput_proxy** = correct_rate * log2(M)

Key result:
- In an ideal channel, higher M always increases throughput proxy
- As p_confuse or p_loss increases, the advantage of higher M requires
  proportionally better measurement reliability to maintain

Output: console table + `results/qudit_inspired_channel.csv`

**TOY MODEL WARNING: This is NOT a quantum computing simulation.**
**This is NOT a proof of quantum advantage.**
This is a simplified parametric model for educational illustration only.
Real qudit systems face decoherence, mode coupling, and measurement
imperfections not captured here.

---

## Hybrid Quantum Support Energy Model

```bash
python hybrid_quantum_support_energy.py
```

This toy model estimates whether an OBQC-like auxiliary layer could reduce
support-system energy in hybrid quantum architectures across five scenarios:
conservative, moderate, optimistic, high_OBQC_overhead, and no_benefit.

**Important:** This model keeps E_cryo (cryogenic cooling energy) unchanged
by default. It does NOT claim that OBQC eliminates cryogenic cooling requirements.
Superconducting qubits require millikelvin temperatures regardless of what the
auxiliary layer does.

The model evaluates whether:

```
E_OBQC_layer < sum_i (1 - alpha_i) * E_i_baseline
```

If this holds, the OBQC layer produces a net auxiliary energy reduction.
If not (high_OBQC_overhead, no_benefit), the layer costs more than it saves.

Output: console table + `results/hybrid_quantum_support_energy.csv`

See [docs/hybrid-quantum-support-layer.md](../docs/hybrid-quantum-support-layer.md)
for full context, architecture discussion, and falsifiable research questions.

---

## Pattern Recognition vs Binary Operation Cost

```bash
python pattern_vs_binary_operation_cost.py
```

This abstract cost model compares a sequential binary-style classification
pipeline against a pattern-recognition pipeline under simplified, explicitly
stated assumptions.

Parameters swept:
- workload_size: 1,000 / 10,000 / 100,000 / 1,000,000
- pattern_reduction_factor: 0.2 / 0.4 / 0.6 / 0.8 (fraction of binary ops still required)
- overhead_case: low / medium / high (optical extraction and detector cost)

Pattern recognition achieves lower total cost (break_even = yes) only when:
```
overhead < (1 - reduction_factor) * binary_savings
```

For low overhead, break-even is reachable at modest reduction factors.
For high overhead, large reduction factors and large workloads are needed.

Output: console table + `results/pattern_vs_binary_operation_cost.csv`

**This is an abstract cost model, not a hardware benchmark.**
Results depend entirely on the assumed cost parameters.

---

## Run All Comparisons

```bash
python run_comparisons.py
python run_comparisons.py --trials 2000   # override trial count for stochastic simulators
```

Runs all comparison simulators in sequence and reports the location of
each generated CSV file. All outputs go to `results/`.

The hybrid energy and operation-cost models are deterministic and do not
use a `--trials` parameter.

---

*Back to [README.md](../README.md)*
