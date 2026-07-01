# Roadmap: Optical Bead Computing

**Part of:** [Optical Bead Computing](../README.md)

---

## Overview

This roadmap describes the planned development of the Optical Bead Computing (OBC) framework, from software simulation to physical prototype. Each phase has clear entry criteria, deliverables, and success metrics.

The roadmap is organized around verifiable milestones, not speculative timelines. A phase is complete when its success metrics are achieved and documented, not when a date passes.

---

## Version Milestones

| Version | Milestone | Status |
|---|---|---|
| v0.1 | README clarification and conceptual framework documentation | ✅ Complete |
| v0.2 | Python simulator: encode, noise, decode, SER measurement | 🔲 In progress |
| v0.3 | Extended noise model: drift, crosstalk, jitter | 🔲 Planned |
| v0.4 | Visualization: confusion matrix, state space diagram, SER vs N plot | 🔲 Planned |
| v0.5 | Phase 1 hardware specification document | 🔲 Planned |
| v0.6 | Optical medium stabilization: compare air, liquid, solid, fiber paths | ✅ Complete |
| v0.7 | Hybrid quantum support layer: energy model, pattern-cost model, hybrid architecture | ✅ Complete |
| v1.0 | Reproducible optical bead experiment with measured SER data | 🔲 Long-term |

---

## Phase 0: Software Simulation

**Purpose:** Validate the encoding/decoding concept in software before any hardware is built.

**Entry criteria:** Alphabet definition, state vector model, noise model.

**Deliverables:**
- `simulator/encode_decode.py`: alphabet definition, encoding, nearest-neighbor decoding
- `simulator/noise_model.py`: Gaussian noise, jitter, channel drift
- `simulator/confusion_matrix.py`: multi-trial evaluation and confusion matrix
- Measured SER curves as a function of alphabet size and noise level
- Documented separability margins for each DOF

**Success metrics:**
- The simulator correctly encodes and decodes a defined alphabet under zero noise.
- SER vs noise level curve is monotonically increasing and matches analytical estimates.
- Confusion matrix correctly identifies which states are most likely confused.
- Redundancy coding demonstrably reduces SER.

**Known limitations of this phase:**
- Noise models are simplified (Gaussian, linear drift) and may not capture all physical effects.
- No real hardware data is available for calibration.
- Results are existence proofs, not performance guarantees.

---

## Phase 1: Classical Optical Prototype

**Purpose:** Build the simplest possible physical optical bead system and measure real-world SER.

**Entry criteria:** Phase 0 complete; simulation-predicted SER curves guide hardware design.

**Proposed hardware:**
- Light source: RGB diode laser or LED array (3–4 wavelengths)
- Polarization: linear polarizers and waveplates (2–4 polarization states)
- Detector: RGB color sensor (e.g., TCS3200) or compact spectrometer
- Interface: Arduino or Raspberry Pi for signal conditioning; Python for decoding
- Optional: Fiber optic channel for controlled-length propagation

**Alphabet target:** 6 to 24 states using wavelength and polarization only.

**Measurement protocol:**
1. Calibrate source and detector: record mean and variance for each state.
2. Transmit each state N_trials ≥ 100 times.
3. Decode each received measurement by nearest-neighbor classifier.
4. Compute SER and confusion matrix.
5. Compare measured SER with Phase 0 simulation prediction.
6. Test redundancy coding (majority vote over 3 transmissions).

**Success metrics:**
- Measured SER < 5% for the designed alphabet under laboratory conditions.
- Measured confusion matrix matches simulation prediction within a defined tolerance.
- Hardware reproducibility: SER remains stable across 3 calibration-decode cycles.

**Documentation requirement:**
All experimental procedures, hardware configuration, and measurement data must be published in `docs/prototype-phase1.md` and committed to this repository for reproducibility.

---

## Phase 2: Multi-Degree Optical Prototype

**Purpose:** Extend to 3–4 simultaneous degrees of freedom and characterize practical alphabet limits.

**Entry criteria:** Phase 1 complete; SER measured and documented.

**Additional hardware:**
- Temporal modulator: electro-optic modulator or acousto-optic modulator for time-bin or pulse width encoding
- Phase modulator: fiber phase modulator or free-space PZT-mounted mirror
- Timing electronics: fast photodetector + oscilloscope or FPGA time-tagger

**Alphabet target:** 64 to 256 states using wavelength + polarization + temporal encoding.

**Key questions to answer:**
- What is the practical alphabet size limit for 3-DOF encoding under laboratory conditions?
- Which DOF combination yields the best SER for a given total state count?
- How much does calibration drift degrade SER over a 1-hour measurement period?
- Does forward error correction (e.g., Hamming code) allow higher state counts at target SER?

**Success metrics:**
- > 64 states decoded with SER < 5% under stable laboratory conditions.
- Characterization of SER degradation as a function of time since calibration.
- Comparison of redundancy coding strategies.

---

## Phase 3: Qudit-Compatible Research Extension (Long-term)

**Purpose:** Investigate compatibility with single-photon qudit encoding for quantum optical extension.

**Entry criteria:** Phase 2 complete; classical prototype well-characterized.

**This phase is distinct from Phases 0–2.** It enters the domain of quantum optics and requires substantially more complex and expensive hardware.

**Research questions:**
- Can the Phase 2 encoding alphabet be mapped to a qudit encoding scheme compatible with single-photon sources?
- What modifications to the encoder and decoder are needed for single-photon operation?
- What decoherence effects appear at the single-photon level that are absent in the classical prototype?
- What quantum gate operations can be applied to optical bead states?

**Hardware requirements:**
- Single-photon source (SPDC pair source, quantum dot, or NV center)
- Single-photon detectors (SNSPD or Si APD)
- Interferometric stability at the single-photon level
- Cryogenic infrastructure if required by detector choice

**Note:** This phase is a long-term research direction. It is **not required** for the near-term deterministic prototype to be useful or scientifically valid. The deterministic prototype stands alone as a research contribution.

---

## v0.6 Optical Medium Stabilization

**Purpose:** Extend the simulation and documentation framework to cover optical channel medium options, and design the first reproducible medium-comparison experiment.

**Entry criteria:** v0.5 Phase 1 hardware specification complete.

**Deliverables:**
- `docs/optical-medium-stabilization.md`: survey of all medium options with trade-offs
- `docs/sealed-liquid-optical-bead-medium.md`: detailed liquid cell design
- `diagrams/optical-medium-options.md`: Mermaid diagrams for all medium configurations
- `simulator/optical_medium_comparison.py`: simplified medium noise model comparison
- `simulator/liquid_medium_noise.py`: liquid-cell-specific noise model
- Experimental protocol for measuring SER vs medium type
- Falsifiable prediction: SER ranking by medium (open_air > sealed_air > liquid/acrylic > glass > fiber) to be validated by measurement

**Success metrics:**
- Simulator runs for all six media without error
- Documentation clearly states trade-offs without overclaiming
- Protocol specifies at least one reproducible medium-comparison experiment

**Key findings from simulation (model-level, requires experimental confirmation):**
- Phase encoding through centimeter-scale liquid cells requires sub-millikelvin temperature control — not practical for Phase 1 prototypes
- Acrylic / PMMA blocks have significant stress birefringence that degrades polarization DOF
- Glass / quartz and fiber achieve the lowest simulated SER at any M value
- For Phase 1: use sealed air or liquid cell with wavelength + polarization only
- For Phase 2+: use glass, quartz, or fiber when polarization or phase encoding is required

---

## v0.7 Hybrid Quantum Support Layer

**Purpose:** Model OBQC as a potential auxiliary pattern-recognition layer for hybrid quantum computing systems, and define a falsifiable research framework for evaluating this hypothesis.

**Entry criteria:** v0.6 optical medium stabilization framework complete.

**Deliverables:**
- `docs/hybrid-quantum-support-layer.md`: full conceptual and technical discussion of the OBQC hybrid quantum support hypothesis, including energy model, architecture proposals, and falsifiable research questions
- `simulator/hybrid_quantum_support_energy.py`: toy energy model comparing baseline hybrid quantum support pipeline vs OBQC-assisted auxiliary pipeline across five scenarios
- `simulator/pattern_vs_binary_operation_cost.py`: abstract operation-cost comparison of sequential binary processing vs pattern-recognition pipeline
- Updated `README.md`: new Hybrid Quantum Support Layer section with role table and links
- Updated `docs/limitations.md`: hybrid quantum support limitations subsection
- Updated `docs/comparative-simulation-framework.md`: hybrid quantum support comparison section

**Key claims to preserve:**
- OBQC does not eliminate cryogenic cooling for superconducting qubits
- OBQC does not claim quantum advantage
- OBQC does not replace the quantum processor core
- Net benefit of an OBQC auxiliary layer is conditional on E_OBQC_layer < auxiliary savings

**Success metrics:**
- Both new simulators run without errors and produce valid CSV output
- The documentation clearly states what OBQC can and cannot reduce
- The energy model makes the net-benefit condition explicit and falsifiable

---

## Contribution Guidelines

Contributions are welcome at any phase. Priority areas:

1. **Simulator improvements:** more realistic noise models, additional DOFs, visualization tools.
2. **Alphabet optimization:** algorithms for maximizing minimum inter-state distance.
3. **Redundancy coding:** implementation of standard error-correcting codes in the optical bead context.
4. **Hardware documentation:** anyone with access to appropriate optics equipment is encouraged to attempt Phase 1 and contribute measurement data.
5. **Literature review:** connections to existing multi-level optical modulation, qudit quantum optics, and optical pattern recognition research.

---

*Back to [README.md](../README.md)*

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