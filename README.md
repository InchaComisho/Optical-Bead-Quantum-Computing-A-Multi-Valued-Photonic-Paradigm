# Optical Bead Computing
## A Soroban-Inspired Multi-Valued Photonic Computing Paradigm

> **One-sentence definition:** Optical Bead Computing is a soroban-inspired, multi-valued photonic computing framework that encodes information as optical bead patterns using wavelength, polarization, phase, time-bin structure, pulse width, spatial mode, RGBW/SCD patterns, and other distinguishable degrees of freedom of light.

**Repository:** `Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm`  
**Status:** Conceptual framework / early-stage research  
**Primary focus:** Deterministic optical pattern computing, multi-valued photonic encoding, RGBW/SCD optical-symbol decoding  
**License:** CC BY-SA 4.0  
**Published:** 2026-06-03  
**Japanese README:** [README_ja.md](README_ja.md)

---

## Important Scope Clarification

This repository focuses on **Optical Bead Computing (OBQC)** as a multi-valued optical pattern-computing framework.

A broader electronic + optical + quantum-compatible system architecture has been separated into a dedicated repository:

**Electronic-Optical Hybrid Quantum-Compatible Computing Architecture**  
https://github.com/InchaComisho/Electronic-Optical-Hybrid-Quantum-Compatible-Computing-Architecture

That repository should be used for:

- electronic control layers,
- electronic memory and correction layers,
- electronic-optical interfaces,
- hybrid system architecture,
- quantum-compatible photonic extension roadmaps,
- system-level integration between electronics and optical processing.

This OBQC repository should be used for:

- soroban-inspired optical bead patterns,
- multi-valued photonic symbols,
- RGBW / CMOS / SCD optical-symbol decoding,
- deterministic optical pattern recognition,
- state separability and decoding simulations.

In short:

```text
OBQC repository
= optical bead patterns and deterministic multi-valued photonic encoding

Electronic-Optical Hybrid repository
= electronic control + optical processing + quantum-compatible system architecture
```

---

## What This Repository Is Not

This repository does **not** claim:

- a completed universal quantum computer,
- quantum advantage,
- a working fault-tolerant quantum architecture,
- guaranteed superiority over binary computing,
- hardware validation of all proposed optical states,
- unlimited scaling of optical state count.

The term **quantum** in the repository name reflects a long-term conceptual direction and the relevance of high-dimensional optical state ideas. The near-term work here is classical, deterministic, and simulation/prototype oriented.

For electronic-optical hybrid quantum-compatible architecture, use the separate repository linked above.

---

## Abstract

Optical Bead Computing is a proposed framework for multi-valued photonic information processing inspired by the Japanese soroban abacus.

In a soroban, a digit is not represented as a linear binary string. It is represented as a structured bead configuration. A skilled practitioner can perceive and manipulate the whole pattern at once, especially in flash mental arithmetic.

OBQC transfers this principle to photonic information processing. It proposes that information may be represented as optical bead patterns across multiple distinguishable degrees of freedom such as wavelength, polarization, phase, time-bin structure, pulse width, spatial mode, intensity, and RGBW/SCD symbolic patterns.

The goal is not to prove that optical computing is universally superior. The goal is to create a clear, testable, falsifiable framework for evaluating whether pattern-based optical encoding can provide useful advantages for selected tasks such as optical pattern recognition, compact state representation, multi-valued symbolic decoding, and high-dimensional optical classification.

---

## Core Hypothesis

> If distinguishable optical states can be reliably encoded, transformed, measured, and decoded under realistic noise conditions, then soroban-inspired optical bead patterns may support compact, parallel, and pattern-oriented information processing that is structurally distinct from ordinary binary photonic systems.

This hypothesis is testable. The key variables are:

- practical state separability,
- symbol error rate,
- optical noise and crosstalk,
- calibration drift,
- detector resolution,
- energy per symbol,
- decoding latency,
- comparison against binary electronic and binary optical baselines.

---

## Conceptual Origin: From Soroban to Optical Beads

The soroban represents numbers as bead configurations on rods. Each rod encodes a decimal digit using a structured spatial pattern.

OBQC uses this idea as an analogy for optical information processing:

| Soroban | Optical Bead Computing |
|---|---|
| Physical bead on a rod | Optical degree of freedom |
| Bead position | State value within that degree of freedom |
| Full bead configuration | Optical bead state vector |
| Flash mental arithmetic | Optical pattern recognition |
| Soroban calculation | Optical state transformation |

The important point is structural: the full pattern becomes the unit of recognition.

---

## Optical Bead State Model

An optical bead state can be represented as:

```text
B = (lambda, P, phi, tau, w, s, l, A)
```

Where:

- `lambda` = wavelength / color channel
- `P` = polarization
- `phi` = phase
- `tau` = time-bin
- `w` = pulse width
- `s` = spatial mode or position
- `l` = orbital angular momentum
- `A` = amplitude or intensity

The theoretical number of states is the product of the available levels in each degree of freedom:

```text
N_theoretical = n_lambda × n_P × n_phi × n_tau × n_w × n_s × n_l × n_A
```

However, the practically usable state count is always lower than the theoretical maximum.

Practical state separability depends on:

- detector spectral resolution,
- signal-to-noise ratio,
- optical crosstalk,
- thermal drift,
- calibration stability,
- background light,
- detector saturation,
- phase and polarization instability,
- physical alignment.

---

## Near-Term Deterministic Layer

The near-term focus of this repository is deterministic optical pattern computing, not full quantum computation.

Near-term prototypes may use:

- RGB or RGBW LEDs,
- CMOS image sensors,
- color sensors,
- diode lasers,
- polarizers,
- waveplates,
- simple optical paths,
- Python nearest-neighbor decoders.

This deterministic layer can test whether structured optical symbols can be encoded and decoded reliably before attempting any advanced quantum-compatible extension.

---

## SCD / RGBW / CMOS Optical-Symbol Prototype Path

A practical near-term path is the combination of:

```text
Soroban-Coded Decimal (SCD)
+ RGBW optical channels
+ LED or display output
+ CMOS / color sensor readout
+ nearest-neighbor decoding
```

SCD represents decimal digits using a constrained 5-bit pattern inspired by soroban bead structure:

```text
D = (H, L4, L3, L2, L1)
```

Where:

- `H` = five-bead equivalent
- `L4, L3, L2, L1` = lower one-bead equivalents

For RGBW × SCD encoding, a marker bit is needed to avoid zero-state collision:

```text
[M, H, L4, L3, L2, L1]
```

Without the marker bit, R0, G0, B0, and W0 all collapse into the same all-zero vector.

Related files:

- [docs/scd-rgb-optical-bead-encoding.md](docs/scd-rgb-optical-bead-encoding.md)
- [docs/obqc-hybrid-decoder.md](docs/obqc-hybrid-decoder.md)
- [simulator/obqc_hybrid_decoder.py](simulator/obqc_hybrid_decoder.py)

---

## Technical Architecture

```text
Input value / pattern
        |
        v
[Encoder]
Maps value to optical bead state
        |
        v
[Optical State Generator]
LED / laser / modulator / display
        |
        v
[Optical Channel]
Air / sealed air / liquid / acrylic / glass / fiber
        |
        v
[Detector]
CMOS / color sensor / photodiode / spectrometer
        |
        v
[Decoder]
Nearest-neighbor / threshold / probabilistic classifier
        |
        v
Decoded symbol + confidence + error flag
```

---

## Error Model and State Separability

Real optical systems are affected by many error sources:

- Gaussian sensor noise,
- shot noise,
- read noise,
- dark current,
- background light,
- channel crosstalk,
- detector quantization,
- optical alignment error,
- temperature drift,
- saturation,
- aging and calibration drift.

The simulator is intended to test how decoding accuracy changes when these effects are approximated in software.

Key metrics:

- symbol error rate,
- confusion matrix,
- nearest-neighbor margin,
- reject rate,
- signal-to-noise sensitivity,
- state-separability threshold.

---

## Minimal Prototype Roadmap

### Phase 0: Software Simulation

- Define an optical bead alphabet.
- Inject configurable noise.
- Decode using nearest-neighbor classification.
- Measure error rate and margin.
- Compare against binary baselines.

### Phase 1: RGBW / CMOS Prototype

- Use RGB or RGBW LEDs.
- Use CMOS or color-sensor readout.
- Test small state alphabets.
- Verify calibration stability.
- Measure symbol error rate under controlled lighting.

### Phase 2: Multi-Degree Optical Prototype

- Add wavelength, polarization, temporal, or spatial encoding.
- Test multiple degrees of freedom together.
- Add redundancy and rejection thresholds.
- Compare with ordinary binary photonic encoding.

### Phase 3: Long-Term Quantum-Compatible Research

Long-term quantum-compatible exploration should be treated as a separate research direction and connected to the dedicated hybrid architecture repository:

https://github.com/InchaComisho/Electronic-Optical-Hybrid-Quantum-Compatible-Computing-Architecture

---

## Comparative Simulations

This repository includes comparison-oriented simulators and documents. Their purpose is not to prove universal superiority, but to expose trade-offs between encoding schemes.

Relevant comparison themes:

- BCD vs SCD validity checking,
- binary photonic vs optical bead symbols,
- RGBW/SCD pattern decoding,
- pattern recognition vs binary lookup,
- state-count expansion vs noise sensitivity.

Important caveat:

> All simulation results are conditional on explicit assumptions. Changing the assumptions changes the result.

---

## Falsifiable Claims

The following claims are suitable for testing:

1. For a defined optical bead alphabet of N states, can nearest-neighbor decoding achieve a target symbol error rate under a specified noise level?
2. How does symbol error rate increase as the alphabet size grows?
3. Which optical degrees of freedom provide the strongest separability margin?
4. Does redundancy reduce symbol error rate enough to justify its overhead?
5. Does pattern-based optical encoding outperform a binary baseline for any selected workload under measured hardware assumptions?

---

## Limitations

Important limitations include:

- no validated physical prototype yet,
- simplified software noise models,
- uncertain hardware energy cost,
- detector and calibration limits,
- optical loss,
- state crosstalk,
- phase and polarization instability,
- theoretical state count exceeding usable state count,
- risk of overclaiming without hardware benchmarks.

---

## Open Invention Position

This repository is released as an open research-oriented concept.

The purpose is to make the idea visible, searchable, citable, testable, and open to criticism. The concept should be evaluated through simulation, physical prototyping, and comparison with existing electronic and photonic baselines.

---

## Related Repository

For the broader electronic-optical hybrid system architecture and quantum-compatible roadmap, see:

**Electronic-Optical Hybrid Quantum-Compatible Computing Architecture**  
https://github.com/InchaComisho/Electronic-Optical-Hybrid-Quantum-Compatible-Computing-Architecture

---

## Author

**Master / inchacomisho / inchacomusho**

## Collaborative AI

- G (ChatGPT)
- Mini (Gemini)
- Cruce (Claude)
- Real (Perplexity)
- Lola (Dola)
- Mana (Manus)

## Publication Date

2026-06-03

## License

**CC BY-SA 4.0** — Creative Commons Attribution-ShareAlike 4.0 International

You are free to share and adapt this material for any purpose, provided appropriate credit is given and derivative works are distributed under the same license.

---

## Keywords

Optical Bead Computing, Soroban-Inspired Computing, Multi-Valued Photonic Computing, RGBW optical decoding, Soroban-Coded Decimal, SCD, CMOS optical sensor, optical pattern recognition, photonic computing, optical computing, high-dimensional photonic information processing, deterministic optical prototype, nearest-neighbor decoder, open invention, quantum-compatible computing

## Hashtags

#OpticalBeadComputing #PhotonicComputing #OpticalComputing #Soroban #AbacusComputing #MultiValuedLogic #SCD #RGBW #CMOS #OpticalPatternRecognition #OpenInvention #QuantumCompatible
