# Pattern vs Binary Flash Emulator

## Conceptual Energy-Latency Model for SCD / RGB-White Optical Bead Pattern Processing

**Status:** Toy emulator / conceptual model — NOT hardware benchmarks  
**File:** [`simulator/pattern_vs_binary_flash_emulator.py`](../simulator/pattern_vs_binary_flash_emulator.py)  
**Results:** `simulator/results/pattern_vs_binary_flash_emulator.csv`

---

## Table of Contents

1. [What Is Being Compared](#1-what-is-being-compared)
2. [What Flash Pattern Processing Means](#2-what-flash-pattern-processing-means)
3. [Why This Is Not Real Measured Hardware Power](#3-why-this-is-not-real-measured-hardware-power)
4. [What Assumptions Favor the Optical Bead Model](#4-what-assumptions-favor-the-optical-bead-model)
5. [What Assumptions Favor the Binary Model](#5-what-assumptions-favor-the-binary-model)
6. [How to Run the Emulator](#6-how-to-run-the-emulator)
7. [How to Interpret Results](#7-how-to-interpret-results)
8. [Why This Is Falsifiable](#8-why-this-is-falsifiable)
9. [Limitations](#9-limitations)

---

## 1. What Is Being Compared

The emulator compares three approaches to classifying one symbol from a 40-symbol alphabet:

| Method | Description |
|---|---|
| **Binary sequential** | Represents 40 symbols as 6-bit integers. Scans candidates one-by-one, comparing 6 bits per candidate. Average case: 20 iterations. |
| **Binary indexed lookup** | Optimized digital baseline: O(1) table lookup using the 6-bit code as an address. 1 memory read + 1 verification compare. |
| **Optical SCD / RGB-white** | Represents each symbol as a color-layer marker (R / G / B / White) plus a 5-position Soroban-Coded Decimal (SCD) bead pattern. 4 layers × 10 SCD digits = 40 symbols. All 9 channels (4 marker + 5 bead) are read simultaneously in one parallel snapshot. |

The binary indexed lookup is included specifically to prevent an unfair comparison. The sequential approach is included because it reflects the worst-case binary scan, which is often the implicit strawman in "pattern vs. serial" arguments.

---

## 2. What Flash Pattern Processing Means

"Flash pattern processing" draws from two sources:

**Flash anzan (flash mental arithmetic):** Expert soroban practitioners can compute sums of many numbers displayed for fractions of a second per number. Research suggests they do this by mentally simulating a virtual soroban — operating on a spatial bead pattern rather than on individual digit symbols. The cognitive operation is a whole-pattern transformation, not a serial digit-by-digit computation.

**Structural parallel decode:** In the optical bead model, the analog of flash recognition is that the entire symbol pattern — color marker plus all five SCD bead positions — is captured in a single CMOS readout step. No candidate list is scanned. The decode path is:

```
Step 1 (parallel readout): read all 9 channels simultaneously
Step 2 (threshold pass):   compare all readings against threshold in one vectorized pass
Step 3 (validity check):   verify SCD thermometer code and decode digit
```

The total latency is 3 logical steps regardless of alphabet size. In contrast, binary sequential latency scales linearly with alphabet size.

This is a structural argument about the decode path, not a claim about hardware speed.

---

## 3. Why This Is Not Real Measured Hardware Power

All energy values in this emulator are **relative units under configurable assumptions**. They are not watts, joules, or any measured physical quantity.

The energy model assigns arbitrary relative costs to different operations:

```
binary_bit_compare_energy  = 1.0   (per bit comparison)
binary_memory_read_energy  = 2.0   (per word memory read)
binary_control_step_energy = 0.5   (per loop/branch step)
led_on_energy              = 1.5   (per active LED bead)
cmos_pixel_read_energy     = 0.8   (per CMOS channel read)
optical_threshold_energy   = 0.4   (per threshold comparison)
validity_check_energy      = 0.5   (per SCD validity check)
```

These ratios are plausible engineering intuitions, but they are not derived from measurements of any physical device. Changing any of these values changes the results. The sensitivity analysis section of the emulator demonstrates this explicitly.

No quantum advantage is claimed or implied. No superiority of optical bead computing over binary computers is guaranteed. The emulator is a tool for exploring whether the architecture can be made technically concrete and what assumptions would need to hold for it to be advantageous.

---

## 4. What Assumptions Favor the Optical Bead Model

Optical pattern processing shows lower relative energy and latency than binary sequential search when:

1. **LED emission costs are low** relative to binary bit-comparison and memory-read costs. If each active LED bead costs less than one binary memory read, the optical side benefits.

2. **CMOS pixel read costs are low.** The optical decode requires 9 CMOS channel reads (4 marker + 5 bead). If each read is cheap relative to binary memory reads, the parallel readout is efficient.

3. **The task is classification over a large alphabet.** Binary sequential latency scales as O(N) where N is the alphabet size. Optical latency is constant at 3 steps. For N = 40, binary sequential requires ~140 steps vs. 3 for optical — a structural latency advantage that grows with N.

4. **Sensor noise is moderate** (sigma < ~0.10 at the default threshold). Under low noise, the SCD thermometer code provides a built-in error detection mechanism: invalid bead patterns are detected before a wrong symbol is returned.

5. **The alphabet is dense relative to the encoding space.** 40 symbols from 4 × 10 = 40 possible combinations means 100% utilization. Binary 6-bit encoding covers 64 states; only 40 are used.

---

## 5. What Assumptions Favor the Binary Model

Binary indexed lookup outperforms the optical model when:

1. **Optical overhead is high.** If LED emission and CMOS read costs are large relative to binary bit-compare and memory-read costs, the parallel optical readout consumes more relative energy per symbol than a single indexed memory lookup.

2. **CMOS pixel read cost is especially high.** The emulator reads 9 channels per symbol. If each channel read costs more than ~0.8 relative units, the optical energy budget grows quickly.

3. **Sensor noise is high** (sigma >= 0.10 to 0.15 at default thresholds). Under high noise, optical error rates climb, and the effective cost per correct recognition increases (since errors require retransmission or correction).

4. **The alphabet is small.** For very small alphabets (N ≤ 4), even sequential binary search requires only a few iterations. The optical parallel readout's advantage over sequential scan is small.

5. **No hardware parallelism is available.** The optical model's latency advantage depends on simultaneous multi-channel readout in a single hardware step. If the CMOS sensor must be read serially, latency increases linearly with channels.

The sensitivity analysis section of the emulator includes a "no-benefit case" scenario that explicitly shows a parameter region where binary indexed lookup wins on both energy and error rate.

---

## 6. How to Run the Emulator

**Requirements:** Python 3.8+. No mandatory external dependencies.  
**Optional:** `matplotlib` for PNG plots.

```
# Basic run with default parameters (10,000 trials)
python simulator/pattern_vs_binary_flash_emulator.py

# Custom trial count and noise level
python simulator/pattern_vs_binary_flash_emulator.py --trials 5000 --sigma 0.05

# Skip plots even if matplotlib is installed
python simulator/pattern_vs_binary_flash_emulator.py --no-plots

# Help
python simulator/pattern_vs_binary_flash_emulator.py --help
```

**Output files:**

| File | Contents |
|---|---|
| Console | ASCII summary table: operation counts, energy, latency, error rates, sensitivity analysis |
| `simulator/results/pattern_vs_binary_flash_emulator.csv` | All aggregated metrics + sensitivity rows |
| `simulator/results/pattern_vs_binary_energy.png` | Energy bar chart (if matplotlib available) |
| `simulator/results/pattern_vs_binary_latency.png` | Latency bar chart (if matplotlib available) |
| `simulator/results/pattern_vs_binary_error_rates.png` | Sensitivity analysis chart (if matplotlib available) |

**Changing model parameters:**

All energy parameters, noise parameters, and the binary sequential fraction are defined as module-level constants at the top of `simulator/pattern_vs_binary_flash_emulator.py`. Edit them directly to explore different assumptions:

```python
# Binary energy model
BINARY_BIT_COMPARE_ENERGY  = 1.0
BINARY_MEMORY_READ_ENERGY  = 2.0
BINARY_CONTROL_STEP_ENERGY = 0.5

# Optical energy model
LED_ON_ENERGY              = 1.5
CMOS_PIXEL_READ_ENERGY     = 0.8
OPTICAL_THRESHOLD_ENERGY   = 0.4
VALIDITY_CHECK_ENERGY      = 0.5

# Noise model
SIGMA_SENSOR               = 0.08
RGB_CROSSTALK              = 0.05
```

---

## 7. How to Interpret Results

### Operation Count Table

Shows per-symbol mean counts of each operation type:

- Binary sequential reports `bit_comparisons`, `memory_reads`, `control_steps`.
- Optical SCD reports `active_beads`, `cmos_reads`, `threshold_comparisons`, `validity_checks`.

These counts are fixed by the model (not noisy), so the mean equals the deterministic count for a 20-iteration average-case sequential search.

### Energy and Latency Table

- **Energy (relative units):** Sum of all operation counts × their per-unit cost, averaged over trials.
- **Latency (steps):** Logical steps in the decode path. Binary sequential = `n_iterations × (bits + 1)`. Binary indexed = 2. Optical = 3.

The percentage comparisons show how optical differs from each binary baseline. A positive `vs Bin-Sequential` percentage means optical uses less relative energy.

### Error Rate Table

Only the optical model is subject to noise errors in this emulator. Binary models are treated as error-free (perfect memory and comparators).

- **Detected errors:** The SCD thermometer code is violated — the bead pattern is illegal. The decoder knows recognition failed.
- **Silent errors:** The bead pattern is a valid SCD code, but maps to the wrong symbol. These require nearest-neighbor correction or redundancy coding to catch.
- **Any error:** Total error rate.

### Sensitivity Analysis Table

Five scenarios with different optical energy parameters and noise levels. Each row shows:

- Optical energy under that scenario
- Binary indexed energy (constant reference)
- `vs Idx` percentage: positive means optical wins on energy
- Error rate under that scenario's noise level
- Which approach is favored

Read this table to understand which assumptions are load-bearing. The "no-benefit case" row explicitly shows that optical loses under pessimistic cost assumptions.

---

## 8. Why This Is Falsifiable

The model makes specific, testable predictions under stated assumptions:

1. **Energy falsifiability:** If real LED emission, CMOS readout, and analog threshold comparison costs per operation can be measured and compared to real digital memory-read and bit-comparison costs, the relative energy ratios become measurable. If the real ratios fall in the "no-benefit" range, optical processing loses.

2. **Latency falsifiability:** The 3-step optical latency assumes fully parallel CMOS readout. If hardware forces serial channel reads, latency scales as `O(channels)`. An experiment measuring CMOS readout timing would confirm or refute the parallel-step assumption.

3. **Error rate falsifiability:** The optical error model predicts specific error rate vs. noise relationships (sigma → error rate curve). These can be tested in software with different sigma values, or in hardware with calibrated noise injection.

4. **Alphabet scaling falsifiability:** The model predicts that optical latency advantage vs. sequential binary grows with alphabet size. This is directly testable in software by changing `ALPHABET_SIZE`.

None of these predictions require the optical bead model to be "correct" — they define conditions under which it would be better or worse than binary processing.

---

## 9. Limitations

| Limitation | Details |
|---|---|
| **No hardware measurements** | All energy values are relative model units, not real power measurements. |
| **Simplified binary model** | Real binary processors use pipelining, caching, and branch prediction. The sequential model is naive; the indexed model is optimistic. Neither is a precise CPU microarchitecture model. |
| **Simplified optical model** | Real optical sensors have dark current, shot noise, nonlinearity, spatial variation, and temperature dependence not fully captured by additive Gaussian noise. |
| **Crosstalk model** | RGB crosstalk is modeled as a fixed fraction. Real spectral overlap between wavelength channels is wavelength-dependent and filter-quality-dependent. |
| **Latency model** | Logical steps (readout / threshold / validity) are not equivalent to real clock cycles. Real hardware may require many clock cycles per logical step, or may pipeline multiple steps. |
| **Error model coverage** | Detected error rate depends on SCD thermometer validity. Silent errors due to layer confusion are also modeled. Errors from OAM or polarization degrees of freedom are not included (this model uses only color + SCD beads). |
| **Alphabet structure** | The 40-symbol alphabet uses only 4 layers × 10 digits. Extending to larger alphabets requires additional degrees of freedom or more layers, each introducing new noise coupling terms. |
| **No hardware prototype** | As of 2026-06-06, no physical optical bead hardware exists. All results are from software simulation. |
| **Energy model ratios are assumptions** | The claim that `LED_ON_ENERGY < BINARY_MEMORY_READ_ENERGY` is a model assumption, not a measurement. Different real hardware choices would yield different ratios. |

---

*This document is part of the Optical Bead Computing repository.*  
*See also: [docs/limitations.md](limitations.md) | [docs/roadmap.md](roadmap.md)*

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
