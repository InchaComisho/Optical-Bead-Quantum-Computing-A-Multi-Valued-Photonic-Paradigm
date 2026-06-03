# Optical Bead Computing
## A Soroban-Inspired Multi-Valued Photonic Computing Paradigm

> **Optical Bead Computing** is a soroban-inspired, multi-valued photonic computing framework that encodes information as optical bead patterns using wavelength, polarization, phase, time-bin structure, pulse width, spatial mode, and other degrees of freedom of light.

**Repository:** `Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm`  
**Status:** Conceptual framework / early-stage research  
**License:** CC BY-SA 4.0  
**Published:** 2026-06-03

---

## Table of Contents

1. [Abstract](#abstract)
2. [Conceptual Origin: From Soroban to Optical Beads](#conceptual-origin-from-soroban-to-optical-beads)
3. [Why This Is Not Just Binary Photonics](#why-this-is-not-just-binary-photonics)
4. [Core Hypothesis](#core-hypothesis)
5. [Optical Bead State Model](#optical-bead-state-model)
6. [Deterministic OBQC vs Quantum OBQC](#deterministic-obqc-vs-quantum-obqc)
7. [Technical Architecture](#technical-architecture)
8. [Error Model and State Separability](#error-model-and-state-separability)
9. [Minimal Prototype Roadmap](#minimal-prototype-roadmap)
10. [Optical Medium Stabilization](#optical-medium-stabilization)
11. [Possible Applications](#possible-applications)
12. [Hybrid Quantum Support Layer](#hybrid-quantum-support-layer)
13. [Sealed Liquid Optical Bead Medium](#sealed-liquid-optical-bead-medium)
13. [Electronic Extension: Soroban-Coded Decimal Logic](#electronic-extension-soroban-coded-decimal-logic)
14. [Comparative Simulations](#comparative-simulations-binary-bcd-scd-and-optical-beads)
15. [What OBQC Is Not](#what-obqc-is-not)
14. [Falsifiable Claims](#falsifiable-claims)
15. [Limitations](#limitations)
16. [Roadmap](#roadmap)
17. [Repository Structure](#repository-structure)
18. [Author](#author)
19. [Keywords](#keywords)

---

## Abstract

Optical Bead Computing (OBC) is a proposed framework for multi-valued photonic information processing inspired by the structure and operational logic of the Japanese soroban abacus. In a soroban, numerical values are represented not as individual digits but as spatial bead configurations — patterns that carry meaning through their arrangement rather than through linear symbol sequences.

This framework proposes that a similar principle can be applied to light: that information may be encoded as *optical bead patterns* across multiple simultaneous degrees of freedom (wavelength, polarization, phase, time-bin, pulse width, spatial mode, orbital angular momentum), and that computation or recognition tasks may be performed by transforming and decoding these multi-dimensional optical states.

The framework distinguishes three layers: a near-term *deterministic* layer using classical multi-valued optical encoding, a *quantum-inspired* layer borrowing high-dimensional state concepts from qudit research, and a long-term *quantum optical* extension involving single-photon sources and quantum gates. The near-term layer is the primary focus of this repository.

This document presents the conceptual model, state formalism, error considerations, a minimal simulation framework, and a prototype roadmap. Claims are limited to what is technically grounded. The goal is to provide a clear, reproducible, and falsifiable research framework for soroban-inspired photonic computing.

---

## Conceptual Origin: From Soroban to Optical Beads

See also: [docs/soroban-origin.md](docs/soroban-origin.md)

### The Soroban Abacus

The soroban (Japanese abacus) represents numbers as configurations of beads along rods. Each rod corresponds to a positional column; each bead configuration within a rod encodes a digit from 0 to 9. A complete soroban value is a *spatial pattern* — the entire bead arrangement across all rods — rather than a string of independently decoded symbols.

Skilled soroban practitioners do not read digits serially. They perceive and manipulate the full pattern at once.

### Flash Mental Arithmetic

In *flash anzan* (flash mental arithmetic), practitioners watch sequences of numbers displayed for fractions of a second on a screen and compute their sum with high accuracy. Research suggests that advanced practitioners mentally simulate a virtual soroban — they operate on a spatial pattern image rather than on symbolic digit representations.

This demonstrates that numerical operations can be executed as rapid *visual pattern recognition and transformation*, where the pattern itself is the computational unit.

### From Soroban to Optical Beads

Optical Bead Computing transfers this principle to photonic information processing:

- Where a soroban encodes a number as a bead configuration across physical rods, OBQC encodes a state as a multi-dimensional optical configuration across degrees of freedom of light.
- Where a soroban practitioner recognizes and transforms bead patterns, an OBQC decoder recognizes and maps optical patterns to output values.
- Where flash anzan shows pattern-speed advantage in human cognition, OBQC explores whether pattern-based optical encoding offers structural advantages in photonic systems.

The central analogy:

| Soroban | Optical Bead Computing |
|---|---|
| Physical bead on a rod | Optical degree of freedom (λ, P, φ, …) |
| Bead position (up/down) | State value within that degree of freedom |
| Full bead configuration | Optical bead state vector B |
| Soroban calculation | Optical state transformation |
| Flash pattern recognition | Optical pattern decoding |

---

## Why This Is Not Just Binary Photonics

Conventional digital electronics and standard optical communication systems are fundamentally binary at the information layer: each channel carries a 0 or a 1. Even high-throughput optical fiber systems typically encode information by switching a single optical property (presence/absence of a pulse, or phase shift between two states).

OBQC proposes a different structure:

| System | Information Layer | State Count per Symbol |
|---|---|---|
| Binary electronics | Single bit per wire | 2 |
| Conventional optical communication | On/off keying or BPSK | 2 |
| Advanced optical modulation (QAM, OFDM) | Multiple bits per symbol | 4 to 1024+ |
| **Optical Bead Computing** | **Multi-dimensional bead state vector** | **Configurable; determined by usable degrees of freedom** |

The distinction is not primarily one of raw state count. It is structural: OBQC proposes treating the full multi-dimensional optical configuration as a single *pattern unit*, analogous to a soroban bead arrangement, rather than as a set of independently multiplexed binary channels.

This structural difference may offer advantages for:
- Pattern-oriented recognition tasks where the full state vector is the meaningful unit
- Compact encoding of high-dimensional classes or templates
- Optical systems where operating across multiple degrees of freedom simultaneously reduces per-channel bandwidth requirements

Whether these structural advantages translate into practical computational benefits depends on physical realizability, which is an open research question.

---

## Core Hypothesis

> If distinguishable optical states can be reliably encoded, transformed, and decoded across multiple degrees of freedom of light, then multi-valued optical bead computing may support compact, parallel, and pattern-oriented information processing that is structurally distinct from binary optical systems.

This hypothesis is falsifiable and testable. The key variables are:

- The number of reliably distinguishable states per degree of freedom under realistic noise conditions
- The achievable total alphabet size as a function of joint encoding across multiple degrees of freedom
- The decoding accuracy as a function of state count, noise level, and redundancy coding
- The computational tasks for which pattern-based encoding offers structural benefits over binary encoding

---

## Optical Bead State Model

See also: [docs/optical-bead-state-model.md](docs/optical-bead-state-model.md)

### State Vector

An optical bead state is defined as a tuple:

```
B = (λ, P, φ, τ, w, s, ℓ)
```

Where each component represents one degree of freedom of light:

| Symbol | Degree of Freedom | Example States |
|---|---|---|
| λ | Wavelength / color channel | 450 nm, 532 nm, 633 nm, 780 nm, … |
| P | Polarization state | H, V, D, A, R, L |
| φ | Phase state | 0, π/4, π/2, 3π/4, π, … |
| τ | Time-bin / temporal position | bin 0, bin 1, bin 2, … |
| w | Pulse width | narrow, medium, wide |
| s | Spatial mode / position | mode 0, mode 1, mode 2, … |
| ℓ | Orbital angular momentum (OAM) | ℓ = 0, ±1, ±2, … |

### Theoretical vs Practical State Count

The theoretical number of states is the product of the number of levels per degree of freedom:

```
N_theoretical = n_λ × n_P × n_φ × n_τ × n_w × n_s × n_ℓ
```

For example, 4 wavelengths × 4 polarizations × 4 phases × 4 time-bins = 256 theoretical states.

**However, the number of practically distinguishable states is always less than the theoretical maximum.**

Practical state separability depends on:
- Detector spectral resolution and sensitivity
- Signal-to-noise ratio
- Crosstalk between adjacent states in each degree of freedom
- Channel drift and environmental instability
- Calibration accuracy and stability
- Interaction effects between degrees of freedom (e.g., polarization-dependent phase shifts)

The practically usable alphabet size must be determined empirically for each physical implementation. The simulator in this repository provides tools to estimate separability under Gaussian noise models.

---

## Deterministic OBQC vs Quantum OBQC

See also: [docs/deterministic-vs-quantum.md](docs/deterministic-vs-quantum.md)

| Layer | Description | Status |
|---|---|---|
| **Deterministic Optical Bead Computing** | Classical multi-valued optical state encoding and decoding using macroscopic light sources and detectors | Near-term simulation / prototype |
| **Quantum-Inspired OBQC** | Uses qudit-like high-dimensional encoding concepts without requiring full quantum coherence or entanglement | Conceptual / research framework |
| **Quantum Optical Bead Computing** | Future extension using single photons, qudits, entanglement, and quantum gates | Long-term research direction |

The deterministic layer is the primary near-term focus. It does not require quantum coherence and can be prototyped with:
- Diode lasers or LEDs
- Standard polarizing optics
- Optical modulators
- Color sensors or spectrometers
- Standard Python-based decoding software

The quantum extension is a long-term research direction and is not a prerequisite for the deterministic prototype.

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Optical Bead Computing Architecture               │
│                                                                     │
│  ┌──────────┐   ┌───────────────┐   ┌──────────────────────────┐   │
│  │ Encoder  │──▶│ Optical State │──▶│  Optical Bead Channel /  │   │
│  │          │   │  Generator    │   │  Transformation Layer    │   │
│  └──────────┘   └───────────────┘   └──────────────────────────┘   │
│                                                  │                  │
│  ┌──────────────────────────────────────────┐   │                  │
│  │  Error Correction / Redundancy Layer     │◀──┘                  │
│  └──────────────────────────────────────────┘                      │
│                          │                                          │
│             ┌────────────▼────────────┐                            │
│             │  Decoder / Pattern      │                            │
│             │  Recognition Unit       │                            │
│             └────────────────────────┘                            │
│                          │                                          │
│             ┌────────────▼────────────┐                            │
│             │   Software Simulator /  │                            │
│             │   Analysis Layer        │                            │
│             └────────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────┘
```

**Component descriptions:**

- **Encoder:** Maps input values or data to optical bead state vectors. Implements the alphabet definition and state assignment.
- **Optical State Generator:** Physical or simulated source producing optical pulses with specified wavelength, polarization, phase, temporal, and spatial properties.
- **Optical Bead Channel / Transformation Layer:** The propagation medium or transformation network through which optical states pass. May include beam splitters, waveplates, phase modulators, delay lines, and spatial light modulators.
- **Error Correction / Redundancy Layer:** Applies redundancy coding, parity checks, or forward error correction to reduce symbol error rate.
- **Decoder / Pattern Recognition Unit:** Measures optical properties of received states and maps them to the nearest defined state in the alphabet. In hardware: a multi-channel detector array with associated signal processing. In simulation: nearest-neighbor distance computation.
- **Software Simulator / Analysis Layer:** Python-based simulation framework for encoding, noise injection, decoding, and evaluation. See the `simulator/` directory.

---

## Error Model and State Separability

See also: [docs/limitations.md](docs/limitations.md)

Realistic optical systems are subject to multiple noise and error sources. The simulator models the following:

| Error Source | Description | Modeled As |
|---|---|---|
| **Gaussian noise** | Random fluctuations in measured optical parameters | Additive Gaussian noise per dimension |
| **Detector quantization** | Finite detector resolution limits distinguishable levels | Floor/ceiling quantization |
| **Channel drift** | Slow systematic drift of optical properties over time | Linear drift term |
| **Spectral overlap** | Adjacent wavelength channels bleed into each other | Gaussian spectral cross-coupling |
| **Polarization error** | Rotation or ellipticity error in polarization states | Angular rotation noise |
| **Phase instability** | Phase fluctuations due to thermal or mechanical perturbation | Phase noise term |
| **Temporal jitter** | Uncertainty in pulse arrival time or time-bin assignment | Jitter distribution |

**Decoding strategy:**

The default decoder uses nearest-neighbor distance in the normalized state space. The decoder assigns each received state to the closest state in the defined alphabet.

**Evaluation metrics:**

- Symbol error rate (SER) as a function of alphabet size and noise level
- Confusion matrix: which states are most likely to be confused with which others
- Separability margin: minimum distance between adjacent states

---

## Minimal Prototype Roadmap

See also: [docs/roadmap.md](docs/roadmap.md)

### Phase 0: Software Simulation (Current)

- Define an optical bead alphabet in Python
- Encode integer values as optical bead state vectors
- Inject configurable Gaussian noise
- Decode using nearest-neighbor distance
- Measure symbol error rate
- Generate and plot confusion matrix
- Test redundancy coding strategies

**Target:** Demonstrate that N states can be encoded and decoded above a target accuracy for given noise levels.

### Phase 1: Classical Optical Prototype

- **Source:** RGB LED array or diode laser with tunable wavelength
- **Polarization:** Linear polarizers and waveplates
- **Detection:** Color sensor, spectrometer, or multi-channel photodetector
- **Decoder:** Python-based nearest-neighbor classifier
- **Target alphabet:** 6 to 24 distinguishable states
- **Metric:** Symbol error rate < 5% under laboratory conditions

### Phase 2: Multi-Degree Optical Prototype

- Combine wavelength + polarization + temporal bin encoding
- Target alphabet: 64 to 256 states
- Calibration procedure and drift correction
- Forward error correction integration
- Reproducible calibration and measurement documentation

### Phase 3: Qudit-Compatible Research Extension (Long-term)

- Single photon source (e.g., SPDC or quantum dot)
- Time-bin or frequency-bin qudit encoding
- Path encoding and interferometric gates
- Compatibility evaluation with quantum gate operations
- **Note:** This phase is not required for the deterministic prototype and represents a separate long-term research direction.

---

## Optical Medium Stabilization

See also: [docs/optical-medium-stabilization.md](docs/optical-medium-stabilization.md) | [diagrams/optical-medium-options.md](diagrams/optical-medium-options.md) | [simulator/optical_medium_comparison.py](simulator/optical_medium_comparison.py)

OBQC does not require an open-air optical path. For near-term prototypes, the optical bead channel can be stabilized by enclosing or replacing the open-air gap with a more controlled medium.

| Medium | Near-term feasibility | Main benefit | Main risk |
|---|---|---|---|
| Open air | Very easy | Simplest first test | Dust, humidity, turbulence |
| Sealed air / nitrogen | Easy | Dust and humidity elimination | Temperature and pressure drift |
| Sealed liquid (water, silicone oil) | Moderate | Enclosed and index-stabilized path | Bubbles, thermal RI drift, phase instability |
| Acrylic / PMMA block | Easy to moderate | Solid, compact, no convection | Stress birefringence (avoid for polarization DOF) |
| Optical glass / quartz | Moderate | Low stress, best optical quality | Machining cost |
| Fiber / waveguide | Advanced | Guided, stable, scalable | Coupling complexity |

Key considerations:
- **Ultra-pure water** is a sealed liquid medium requiring degassing, sealing, and temperature control — not a solid material.
- **Acrylic / PMMA** is suitable for wavelength, intensity, and spatial encoding but has significant stress birefringence that degrades polarization DOF.
- **Glass and quartz** are recommended when polarization or phase encoding is needed.
- **Fiber and waveguides** are the long-term path toward scalable implementation.
- **Quantum optical extensions** require stricter loss, scattering, and phase-coherence control than classical OBQC prototypes — liquid and polymer media are not automatically suitable.

---

## Possible Applications

The following applications are proposed as research directions. None are claimed to be currently implemented or demonstrated.

| Application | Description | Layer |
|---|---|---|
| Optical pattern recognition | Classify high-dimensional optical patterns directly | Deterministic |
| Photonic AI inference | Optical implementation of lookup-table or template-matching inference | Deterministic |
| Optical memory addressing | Use multi-valued optical states as compact address codes | Deterministic |
| High-dimensional communication coding | Encode more information per optical symbol | Deterministic |
| Sensor fusion | Combine multi-modal sensor data into optical bead state representations | Deterministic |
| Image preprocessing | Optical bead encoding as a preprocessing stage for visual data | Deterministic |
| Low-latency optical classification | Pattern-based classification at optical speeds | Deterministic |
| Educational model | Connect soroban/flash arithmetic concepts to photonic systems | Conceptual |
| Qudit research platform | Testbed for high-dimensional quantum state encoding protocols | Quantum extension |

**These applications require hardware implementation and experimental validation before any performance claims can be made.**

---

## Hybrid Quantum Support Layer

See also: [docs/hybrid-quantum-support-layer.md](docs/hybrid-quantum-support-layer.md) | [simulator/hybrid_quantum_support_energy.py](simulator/hybrid_quantum_support_energy.py) | [simulator/pattern_vs_binary_operation_cost.py](simulator/pattern_vs_binary_operation_cost.py)

OBQC is not claimed to replace superconducting quantum processors or to eliminate cryogenic cooling requirements. Superconducting qubits require millikelvin temperatures to operate, and no optical auxiliary layer changes this.

However, OBQC may be explored as a potential low-energy pattern-recognition support layer for the surrounding infrastructure of hybrid quantum systems. Many near-term quantum computers are hybrid systems that combine a quantum processor with substantial room-temperature classical infrastructure including control electronics, readout discrimination, syndrome decoding, and post-processing. As systems scale, this auxiliary infrastructure may grow significantly.

An OBQC-like optical pattern-recognition layer may potentially reduce:
- Readout signal classification overhead (treating readout signals as noisy multi-dimensional patterns)
- Data movement between readout electronics and classical decoders
- High-dimensional multiplexing of I/O channels into the cryostat
- Repeated binary operations for recurring pattern-matching tasks in error-candidate detection
- Energy cost of selected classical post-processing workloads

**The net benefit of such a layer is conditional.** It is useful only if the energy consumed by the optical layer is less than the energy saved in auxiliary processing. This condition is made explicit and falsifiable in the toy energy model.

| Target | OBQC Role | Limitation |
|---|---|---|
| Superconducting quantum systems | Auxiliary readout / preprocessing layer | Does not remove cryogenic qubit cooling |
| Photonic quantum systems | More natural optical-state support layer | Detector and loss constraints remain |
| Classical post-processing | Pattern-based reduction of repeated workloads | Only useful if overhead is lower than saved computation |
| Error-candidate detection | Fast recognition of repeated error patterns | Requires benchmark validation against digital decoders |
| I/O multiplexing | High-dimensional optical encoding per channel | Integration and conversion overhead must be characterized |

The toy energy model (`simulator/hybrid_quantum_support_energy.py`) evaluates the net-benefit condition across five scenarios (conservative, moderate, optimistic, high_OBQC_overhead, no_benefit). The pattern-cost model (`simulator/pattern_vs_binary_operation_cost.py`) identifies under what workload and overhead conditions pattern recognition achieves lower cost than sequential binary processing.

---

## Sealed Liquid Optical Bead Medium

See also: [docs/sealed-liquid-optical-bead-medium.md](docs/sealed-liquid-optical-bead-medium.md) | Simulator: [simulator/liquid_medium_noise.py](simulator/liquid_medium_noise.py)

For near-term classical Optical Bead Computing prototypes, the optical channel does not need to be open air. A **sealed transparent liquid medium** — an immersion-stabilized optical cell — may improve environmental stability by eliminating dust contamination, air turbulence, and humidity variation.

In this model, optical bead states are transmitted through a closed transparent liquid cell (e.g., a spectroscopy cuvette filled with distilled water, glycerol solution, or optical-grade oil). The liquid provides a mechanically stable, sealed propagation medium.

### Potential advantages

- Dust and airborne particle contamination: eliminated by sealing
- Air turbulence (heat shimmer): eliminated; replaced by slow liquid convection
- Humidity variation: eliminated inside the sealed cell
- Refractive index matching to window glass: reduces reflection losses at cell boundaries

### Known limitations

| Limitation | Physical mechanism | Severity |
|---|---|---|
| Absorption loss | Beer-Lambert attenuation: I = I₀ exp(−αL) | Low (< 1 dB for 5 cm water at visible wavelengths) |
| Scattering from bubbles / impurities | Random amplitude drops | Low-moderate (eliminated by degassing and filtration) |
| Temperature-dependent refractive index drift | dn/dT ≈ −1×10⁻⁴ K⁻¹ for water | **Critical for phase encoding** |
| Wavelength-dependent transmission | Different α per wavelength channel | Moderate; requires per-channel calibration |
| Long-term material degradation | Oxidation, microbial growth, outgassing | Low (use chemically stable media, sealed container) |
| Phase instability from temperature | ~5 rad phase shift per 0.1 K at 5 cm path | **Severe; see below** |

### Critical finding: phase encoding is impractical at centimeter-scale path lengths

Simulation (`simulator/liquid_medium_noise.py`) shows that in water at 5 cm path length, a temperature deviation of only 0.1 K causes approximately **5 rad** of phase drift — enough to completely scramble any phase-encoded optical bead state. Achieving < 0.1 rad phase stability at 5 cm would require temperature control to better than 2 mK, which is impractical in a near-term prototype.

**Practical implication:** For Phase 1 and Phase 2 liquid-medium prototypes, use **wavelength and polarization** encoding only. Phase encoding should be deferred until active interferometric stabilization or sub-millimeter path lengths are available.

### Liquid medium comparison

| Medium | Transparency | Refractive index | dn/dT (K⁻¹) | Recommended for |
|---|---|---|---|---|
| Distilled water | 200–1300 nm | 1.333 | −1.0×10⁻⁴ | Phase 1 baseline; low cost |
| Glycerol-water | 200–1200 nm | 1.33–1.47 | −2.5×10⁻⁴ | Tunable RI; higher dn/dT |
| Immersion oil | 400–800 nm | 1.515 | −3.0×10⁻⁴ | RI-matched windows; shorter range |
| Fluorinert FC-770 | 250–2000 nm | 1.275 | −1.7×10⁻⁴ | Broadest range; highest cost |

This approach is a **classical optical prototype design choice**. It hosts macroscopic multi-photon pulses, not single photons. It does not enable quantum coherence or quantum advantage.

---

## Electronic Extension: Soroban-Coded Decimal Logic

See also: [docs/electronic-extension-soroban-decimal.md](docs/electronic-extension-soroban-decimal.md) | Simulator: [simulator/soroban_decimal.py](simulator/soroban_decimal.py)

The soroban structural logic is not limited to photonic systems. It maps directly onto electronic circuit design as **Soroban-Coded Decimal (SCD)** — a 5-bit constrained decimal cell that mirrors the physical structure of a soroban rod in digital hardware.

### SCD Cell Definition

```
D = (H, L4, L3, L2, L1)

digit = 5 * H + count(L4, L3, L2, L1)
```

Where H is the heaven bead (value 5) and L1–L4 are earth beads (value 1 each), encoded using a **thermometer code** that activates beads in order without gaps.

### Encoding Table

| Decimal | H | L4 L3 L2 L1 | 5-bit code |
|---:|:---:|:---:|:---:|
| 0 | 0 | 0 0 0 0 | `0 0000` |
| 1 | 0 | 0 0 0 1 | `0 0001` |
| 2 | 0 | 0 0 1 1 | `0 0011` |
| 3 | 0 | 0 1 1 1 | `0 0111` |
| 4 | 0 | 1 1 1 1 | `0 1111` |
| 5 | 1 | 0 0 0 0 | `1 0000` |
| 6 | 1 | 0 0 0 1 | `1 0001` |
| 7 | 1 | 0 0 1 1 | `1 0011` |
| 8 | 1 | 0 1 1 1 | `1 0111` |
| 9 | 1 | 1 1 1 1 | `1 1111` |

10 valid states out of 32 possible 5-bit patterns. The remaining 22 are **detectable error states** by definition — any non-thermometer lower pattern is illegal and can be flagged without additional parity bits.

### Carry and Borrow Structure

The increment and decrement operations follow soroban mechanical logic directly:

- **4 + 1:** lower count reaches 4; H = 0 → set H = 1, clear lower (soroban "5-complement carry-up")
- **9 + 1:** H = 1, lower full → reset cell to 0, carry to next digit
- **5 − 1:** H = 1, lower = 0 → clear H, set lower to 1111 (borrow from the 5-group)
- **0 − 1:** cell = 0, lower = 0 → set to 9, borrow from next digit

### Relationship to the Optical Layer

SCD is the **electronic analog** of an optical bead state:

| Domain | Information unit | Component 1 | Component 2 | Valid states |
|---|---|---|---|---|
| Physical soroban | Bead configuration / rod | Heaven bead H | Earth beads (thermometer) | 10 |
| SCD (electronic) | 5-bit decimal cell | H bit | L1–L4 bits (thermometer) | 10 of 32 |
| OBC (optical) | Optical bead state B | λ, P, φ, ... | Multi-DOF encoding | Alphabet-defined |

All three share the same structural principle: a value is a **multi-component pattern**, not a linear binary sequence. This alignment enables a unified conceptual framework across cognitive, electronic, and photonic domains.

### SCD is not intended to replace BCD for storage density. Its value is structural and educational: it makes soroban arithmetic directly observable in circuit logic.

---

## What OBQC Is Not

In the interest of credibility, the following clarifications are important:

- **OBQC is not claimed to be a completed universal quantum computer.** No quantum gates, no error-corrected qubits, no quantum advantage has been demonstrated.
- **OBQC is not claimed to outperform CPUs, GPUs, or classical computers** for general-purpose computation. No comparative benchmarks exist at this stage.
- **OBQC is not a proof that all theoretical optical states can be reliably distinguished.** The theoretical state count is an upper bound. The practical alphabet size is smaller and must be determined experimentally.
- **OBQC is not a photonic multiplexing scheme.** While optical multiplexing (WDM, PDM, OFDM) uses multiple degrees of freedom for bandwidth, OBQC uses them structurally as a multi-valued alphabet inspired by soroban pattern logic.
- **OBQC is a proposed framework** for exploring soroban-inspired multi-valued optical encoding and pattern-based computation, with a clear experimental roadmap and falsifiable claims.

---

## Comparative Simulations: Binary, BCD, SCD, and Optical Beads

See also: [docs/comparative-simulation-framework.md](docs/comparative-simulation-framework.md)

This repository includes a set of comparison simulators that measure trade-offs between four encoding approaches under controlled, explicitly stated model assumptions. The goal is **not** to prove universal superiority of any scheme — it is to expose measurable trade-offs between compactness, error detection, symbol density, and noise sensitivity.

| Comparison | What it tests | Expected trade-off |
|---|---|---|
| BCD vs SCD | Decimal digit encoding under random bit flips | SCD uses 25% more bits but has 68.75% invalid states vs BCD's 37.5% — converting more bit-flip errors from silent to detected |
| Binary photonic vs OBQC | Alphabet size M under D-dimensional Gaussian noise | Binary M=2 is most robust; higher-M OBC carries more bits/symbol but SER rises faster with noise; higher D preserves margin |
| Binary-like vs qudit-like toy channel | M-level symbol transmission under loss and confusion | Higher M scales throughput proxy in clean channels but requires proportionally better measurement reliability to maintain advantage |

### Simulator links

- [simulator/electronic_binary_vs_scd.py](simulator/electronic_binary_vs_scd.py) — BCD vs SCD bit-flip comparison
- [simulator/photonic_binary_vs_obqc.py](simulator/photonic_binary_vs_obqc.py) — Binary vs optical bead photonic comparison
- [simulator/qudit_inspired_channel.py](simulator/qudit_inspired_channel.py) — Toy qudit-inspired channel (analytical, NOT quantum simulation)
- [simulator/run_comparisons.py](simulator/run_comparisons.py) — Run all three at once
- [docs/comparative-simulation-framework.md](docs/comparative-simulation-framework.md) — Framework documentation and fairness rules

### Key caveats

- The photonic comparison uses a simplified geometric noise model, not a physical optics simulation.
- The qudit channel model is a toy analytical model and does NOT simulate quantum mechanics.
- The electronic comparison uses an independent bit-flip model; real hardware faults are correlated.
- All results are under idealized, explicitly stated model assumptions. Changing the assumptions changes the results.

---

## Falsifiable Claims

The following claims are specific, measurable, and testable:

1. **State encoding accuracy:** For a defined optical bead alphabet of N states, can encoding and nearest-neighbor decoding achieve symbol error rate below a target threshold (e.g., < 5%) at a specified noise level?

2. **SER scaling:** How does symbol error rate increase as the alphabet size N increases under fixed noise conditions?

3. **Degree-of-freedom robustness:** Which optical degrees of freedom (wavelength, polarization, phase, etc.) yield the highest separability margin under realistic noise conditions?

4. **Redundancy improvement:** Does applying redundancy coding (e.g., majority voting or repetition coding) measurably reduce symbol error rate?

5. **Pattern encoding compression:** For selected structured data types, does optical bead pattern encoding reduce the number of symbols required to represent a value compared to binary encoding?

These claims can be tested initially in software simulation (Phase 0) before any hardware is built.

---

## Limitations

See also: [docs/limitations.md](docs/limitations.md)

| Limitation | Description |
|---|---|
| **Noise** | All optical systems are subject to shot noise, thermal noise, and amplifier noise, which reduce the number of distinguishable states |
| **Crosstalk** | Adjacent states in wavelength, phase, or polarization dimensions may bleed into each other |
| **Optical alignment** | Phase and polarization measurements require precise alignment; mechanical perturbations cause errors |
| **Detector limits** | Detector resolution, dynamic range, and sampling rate constrain achievable state separability |
| **Scalability** | Adding degrees of freedom increases state count multiplicatively in theory but in practice introduces new sources of crosstalk |
| **Calibration drift** | Optical systems drift over time due to thermal expansion, mechanical relaxation, and component aging |
| **Energy cost** | Laser sources, modulators, and cryogenic detectors (for quantum extension) consume significant power |
| **Hardware complexity** | Multi-degree optical systems require precise, expensive, and environment-sensitive components |
| **Theoretical vs usable state count** | The theoretical state product N = n_λ × n_P × ... always exceeds the practical usable alphabet |
| **No demonstrated hardware** | As of 2026-06-03, no physical prototype exists; all results are from software simulation |

---

## Roadmap

See also: [docs/roadmap.md](docs/roadmap.md)

| Version | Milestone | Status |
|---|---|---|
| v0.1 | README clarification and conceptual framework documentation | ✅ Complete |
| v0.2 | Python simulator: encode, decode, SER measurement | 🔲 Planned |
| v0.3 | Noise model: Gaussian, jitter, drift, crosstalk | 🔲 Planned |
| v0.4 | Visualization: confusion matrix, state space diagram | 🔲 Planned |
| v0.5 | Prototype documentation: Phase 1 hardware specification | 🔲 Planned |
| v1.0 | Reproducible optical bead experiment with measured SER data | 🔲 Long-term |

---

## Repository Structure

```
Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm/
│
├── README.md                          ← This file
│
├── docs/
│   ├── soroban-origin.md                        ← Soroban and flash anzan conceptual origin
│   ├── optical-bead-state-model.md              ← State vector formalism and DOF model
│   ├── deterministic-vs-quantum.md              ← Three-layer framework comparison
│   ├── electronic-extension-soroban-decimal.md  ← SCD logic: 5-bit soroban decimal cell
│   ├── comparative-simulation-framework.md      ← Comparison framework and fairness rules
│   ├── sealed-liquid-optical-bead-medium.md     ← Sealed liquid cell as optical channel
│   ├── optical-medium-stabilization.md          ← All medium options: air, liquid, solid, fiber
│   ├── limitations.md                           ← Noise, crosstalk, scalability limitations
│   └── roadmap.md                               ← Detailed prototype roadmap
│
├── simulator/
│   ├── README.md                      ← Simulator usage guide
│   ├── encode_decode.py               ← Optical bead alphabet, encoding, decoding
│   ├── noise_model.py                 ← Gaussian noise, jitter, drift models
│   ├── confusion_matrix.py            ← Multi-trial evaluation and confusion matrix
│   ├── soroban_decimal.py             ← SCD encode/decode, increment, add, display
│   ├── electronic_binary_vs_scd.py    ← BCD vs SCD comparison under bit flips
│   ├── photonic_binary_vs_obqc.py     ← Binary vs optical bead photonic comparison
│   ├── qudit_inspired_channel.py      ← Toy qudit-inspired channel (NOT quantum sim)
│   ├── liquid_medium_noise.py         ← Sealed liquid cell noise model
│   ├── optical_medium_comparison.py   ← Stability comparison across all media
│   ├── run_comparisons.py             ← Run all comparison simulators
│   └── results/                       ← Generated CSV output files
│
└── diagrams/
    ├── soroban-to-optical-beads.md    ← Conceptual analogy diagram (Mermaid)
    ├── optical-bead-state-space.md    ← State space visualization (Mermaid)
    ├── architecture.md                ← System architecture diagram (Mermaid)
    └── optical-medium-options.md      ← Medium options: air, liquid, solid, fiber (Mermaid)
```

---

## Author

**Master / inchacomisho / inchacomusho**

## Collaborative AI

| Name | Model |
|---|---|
| G | ChatGPT |
| Mini | Gemini |
| Cruce | Claude |
| Real | Perplexity |
| Lola | Dola |
| Mana | Manus |

## Publication Date

2026-06-03

## License

**CC BY-SA 4.0** — Creative Commons Attribution-ShareAlike 4.0 International

You are free to share and adapt this material for any purpose, provided you give appropriate credit and distribute your contributions under the same license.

---

## Suggested Repository Topics

```
photonic-computing  optical-computing  multi-valued-logic  soroban  abacus
flash-mental-arithmetic  qudit  quantum-inspired  high-dimensional-computing
optical-pattern-recognition
```

---

## Keywords

Optical Bead Computing, Soroban-Inspired Computing, Multi-Valued Photonic Computing, High-Dimensional Photonic Information Processing, Qudit-Inspired Computing, Optical Pattern Recognition, Photonic AI, Flash Mental Arithmetic, Abacus Computing, Optical State Encoding

## Hashtags

#OpticalBeadComputing #PhotonicComputing #OpticalComputing #Soroban #AbacusComputing #MultiValuedLogic #Qudit #QuantumInspired #PhotonicAI #OpticalPatternRecognition
