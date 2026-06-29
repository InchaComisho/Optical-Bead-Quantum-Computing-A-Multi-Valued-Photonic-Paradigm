# Limitations of Optical Bead Computing

**Part of:** [Optical Bead Computing](../README.md)

---

## Purpose of This Document

Stating limitations clearly is not a weakness — it is what makes a research framework credible. This document catalogs the known and expected limitations of the Optical Bead Computing (OBC) framework, organized by category.

---

## 1. Fundamental Physical Limitations

### 1.1 Shot Noise

All optical detection is ultimately subject to shot noise (photon counting statistics). The signal-to-noise ratio for a detected optical pulse with mean photon count n is approximately sqrt(n). This sets a fundamental lower bound on measurement uncertainty that cannot be eliminated by engineering improvement.

At low light levels (few-photon pulses), shot noise significantly limits the number of distinguishable states per degree of freedom.

### 1.2 Heisenberg Uncertainty

Phase and photon number are conjugate variables. High phase precision requires high photon number, which conflicts with the goal of energy-efficient, low-power optical encoding. This is a fundamental tradeoff, not an engineering problem.

---

## 2. Noise Sources

| Noise Source | Description | Affected DOFs |
|---|---|---|
| Thermal noise | Johnson-Nyquist noise in detector electronics | All |
| Shot noise | Photon counting statistics | All |
| Laser frequency noise | Linewidth and frequency jitter of the source | λ, φ |
| Phase noise | Phase fluctuations due to thermal/mechanical perturbation | φ |
| Polarization rotation | Birefringence in components and fiber | P |
| Timing jitter | Pulse arrival time uncertainty | τ, w |
| Amplitude noise | Intensity fluctuations of the optical source | All (intensity-encoded) |
| Dark counts | Detector false positives in the absence of signal | All |

---

## 3. Crosstalk

### 3.1 Spectral Crosstalk

Wavelength channels with finite spectral linewidth overlap with adjacent channels. The crosstalk power is approximately:

```
P_crosstalk ≈ exp( -(Δλ / σ_λ)^2 )
```

where Δλ is the channel separation and σ_λ is the source linewidth. Channels must be separated by several linewidths to achieve low crosstalk.

### 3.2 Polarization Crosstalk

Imperfect polarizers and birefringent optical elements rotate or mix polarization states. Polarization extinction ratio (PER) of typical polarizing optics is 20–40 dB, limiting the number of distinguishable polarization states in practice to 2–4.

### 3.3 Phase Crosstalk

Phase states must be separated by more than the phase noise RMS. For a typical free-space optical path at room temperature, phase fluctuations can be tens of milliradians to radians depending on path length. Stabilization using active feedback is possible but adds complexity.

### 3.4 OAM Mode Crosstalk

OAM modes are orthogonal in ideal free-space conditions but suffer significant crosstalk under atmospheric turbulence, beam misalignment, and aperture truncation. In fiber, OAM modes couple to other spatial modes at bends and imperfections.

---

## 4. Calibration and Drift

### 4.1 Calibration Requirements

The optical bead alphabet is defined relative to a calibration reference. Any drift in:
- Source wavelength or intensity
- Polarization reference frame
- Phase reference path
- Timing reference

causes systematic shifts that move transmitted states closer to adjacent alphabet members, increasing error rates.

### 4.2 Drift Sources

| Drift Source | Timescale | Impact |
|---|---|---|
| Thermal expansion | Minutes to hours | Phase, alignment |
| Mechanical vibration | Milliseconds to seconds | Phase, OAM, alignment |
| Component aging | Months to years | Wavelength, polarization |
| Environmental humidity | Hours to days | Phase (hygroscopic optics) |
| Laser aging | Months to years | Wavelength stability |

Practical systems require periodic recalibration. Long-term autonomous operation requires active stabilization feedback.

---

## 5. Scalability

### 5.1 State Count vs Practical Alphabet Size

The theoretical state count grows multiplicatively with the number of degrees of freedom:

```
N_theoretical = n_λ × n_P × n_φ × n_τ × n_w × n_s × n_ℓ
```

However, as the alphabet size increases, the minimum inter-state distance decreases (for a fixed physical space), and noise increasingly causes decoding errors. The practical alphabet size is constrained by the worst-case noise floor across all dimensions.

Adding more degrees of freedom introduces new crosstalk mechanisms. The marginal benefit of each additional DOF must be weighed against the added complexity and new error sources.

### 5.2 Hardware Complexity

Each degree of freedom requires dedicated hardware:
- Wavelength: tunable source or filter bank
- Polarization: polarizing optics, waveplates
- Phase: phase modulator, interferometric reference
- Time-bin: fast modulator, timing electronics
- Spatial mode: spatial light modulator or waveguide array
- OAM: spiral phase plates or spatial light modulator

A system using 5 DOFs simultaneously requires all of the above hardware, precisely aligned and stabilized. This is feasible in a research laboratory but challenging to scale or deploy outside controlled environments.

---

## 6. Comparison with Existing Technologies

OBQC should not be positioned as a replacement for existing technologies without experimental evidence. Relevant comparisons:

| Technology | State of maturity | Relevant advantage over OBQC |
|---|---|---|
| Binary digital computing | Mature, highly optimized | Decades of optimization, software ecosystem, error-free operation at scale |
| Optical communications (WDM) | Mature | Industrial-grade wavelength multiplexing already deployed |
| Advanced modulation (QAM) | Mature | High spectral efficiency in communications, standardized |
| GPU/TPU parallel computing | Mature | Massively parallel digital computation for AI workloads |
| Qudit quantum computing | Early research | Genuine quantum advantage potential; OBQC Layer 3 is related |

The claim that OBQC offers advantages over these technologies is an open research hypothesis for specific workloads, not a demonstrated fact.

---

## 7. The Theoretical-vs-Practical Gap

The single most important limitation to state clearly:

> The theoretical state count of an optical bead system is always much larger than the practical usable alphabet.

A system with 4 wavelengths × 4 polarizations × 4 phases × 4 time-bins has N_theoretical = 256 states. Under realistic noise conditions in a laboratory prototype, the practical alphabet that can be decoded with < 5% SER may be 16, 32, or 64 states, depending on the noise floor.

This gap is not a failure of the framework — it is the key experimental quantity to measure. The purpose of the simulator and prototype roadmap is to characterize this gap under realistic conditions.

---

## 7. Optical Medium Limitations

The choice of optical channel medium introduces additional limitations beyond those of open-air free-space paths. See also [docs/optical-medium-stabilization.md](optical-medium-stabilization.md).

### 7.1 Liquid Media

| Limitation | Impact |
|---|---|
| Absorption loss | Wavelength-dependent signal attenuation; differential gain across channels |
| Bubble scattering | Random amplitude drops; requires degassing and sealed container |
| Thermal refractive index drift | dn/dT ~ -1e-4 /K for water; at 5 cm path length, 0.1 K causes ~5 rad phase shift |
| Long-term contamination | Leaching from container materials; microbial growth in water |
| Liquid convection | Thermal gradients drive slow refractive-index fluctuations |

**Critical limitation for phase encoding:** At centimeter-scale path lengths, liquid media require sub-millikelvin temperature control for phase stability. Phase DOF should be deferred to shorter-path or solid-medium implementations.

### 7.2 Solid Polymer Media (Acrylic / Optical Resin)

| Limitation | Impact |
|---|---|
| Stress birefringence | Curing and machining stress rotates polarization state; degrades polarization DOF |
| Trapped bubbles | Cast polymer may contain microscopic voids from the curing process |
| Curing shrinkage | Volume contraction during polymerization creates internal stress |
| Thermal expansion | PMMA CTE ~70 ppm/K (vs glass ~3 ppm/K); significant path length change with temperature |
| Long-term yellowing | UV absorption increases over time in some acrylic grades |

**Key implication:** Acrylic / PMMA blocks are suitable for wavelength, intensity, and spatial position encoding, but are not recommended for polarization or phase DOFs without characterization of birefringence and CTE effects.

### 7.3 Optical Glass, Quartz, and Fiber

These materials have much lower stress birefringence, lower CTE, and better optical homogeneity than polymer alternatives. However:
- Glass and quartz blocks require precision machining or molding; fabrication cost is higher
- Fiber coupling requires precision micro-optic alignment; coupling loss is a practical concern
- Fiber birefringence in standard SMF accumulates with temperature and bending; use polarization-maintaining fiber (PMF) for stable polarization encoding

### 7.4 Quantum Optical Extensions

For Phase 3 quantum optical extensions, the requirements on all media are substantially stricter:
- Single-photon loss budget is extremely tight; even 1 dB loss reduces quantum state fidelity significantly
- Rayleigh scattering from bubbles, inclusions, or material inhomogeneity destroys single-photon state purity
- Phase coherence must be maintained over the full path length; any stochastic phase fluctuation degrades quantum interference
- Liquid cells and polymer blocks are not suitable for single-photon quantum optical experiments without significant engineering
- Fiber (low-loss SMF or PMF) or integrated photonic circuits are the appropriate medium for quantum OBQC extensions

---

## 8. Hybrid Quantum Support Limitations

This section covers limitations specific to the hypothesis that OBQC can serve as an auxiliary pattern-recognition layer in hybrid quantum computing systems. See also [docs/hybrid-quantum-support-layer.md](hybrid-quantum-support-layer.md).

### 8.1 OBQC Does Not Eliminate Cryogenic Cooling

Superconducting qubits require operation below approximately 20 mK to maintain quantum coherence. This is a fundamental physical requirement determined by the energy scales of superconducting circuit components relative to thermal fluctuations at room temperature (kT at 300 K is approximately 26 meV; the qubit transition energy for a transmon is typically 5-10 GHz, corresponding to 20-40 ueV). No optical auxiliary layer changes this.

Any proposal that OBQC "solves" the cooling problem of quantum computing would be incorrect. The correct framing is: OBQC may reduce auxiliary processing overhead around a quantum system that still requires cryogenic cooling.

### 8.2 Auxiliary Energy May Be a Small Fraction of Total System Energy

In current superconducting quantum computers, cryogenic infrastructure (dilution refrigerators) consumes 10-30 kW of electrical power. Room-temperature electronics may consume 1-5 kW. If OBQC reduces auxiliary electronics energy by 20-50%, the total system energy saving is modest relative to the cryo plant.

At scale (millions of qubits), the balance may shift as control and readout infrastructure grows, but this remains a hypothesis requiring hardware-level confirmation.

### 8.3 Interface Conversion Costs May Erase Benefits

Hybrid quantum systems operate across multiple signal domains: quantum microwave signals at millikelvin, amplified RF at 4 K, digital electronics at room temperature, and potentially optical signals. Every conversion between domains introduces:
- Energy cost (conversion electronics, laser drivers, detectors)
- Signal fidelity loss (noise added at each stage)
- Latency (propagation, detector integration time)

The benefit of optical pattern recognition may be partially or fully erased by the conversion overhead at the boundaries. This must be measured in real hardware, not assumed.

### 8.4 Real-Time Latency Constraints

Quantum error correction typically operates under strict latency requirements. For a surface code with physical gate time of ~100 ns and code cycle time of ~1 us, the classical decoder must complete syndrome analysis within this window to avoid falling behind the computation. Optical analog processing introduces additional latency from:
- Optical propagation time
- Detector integration and reset time
- Analog-to-digital conversion of the classifier output

Whether OBQC-like processing can meet these timing requirements in a real system has not been demonstrated.

### 8.5 Benchmark Data Does Not Exist

No experiment has demonstrated that an optical pattern-recognition layer reduces auxiliary energy in a real quantum computing system. All claims in this framework are model-level hypotheses based on simplified assumptions. The toy models in this repository (`hybrid_quantum_support_energy.py`, `pattern_vs_binary_operation_cost.py`) are starting points for framing the hypothesis, not evidence of the hypothesis.

### 8.6 Quantum Advantage Is Not Claimed

OBQC is a classical multi-valued optical encoding framework. It does not provide quantum speedup, quantum advantage, or any computational benefit that requires quantum coherence or entanglement. It is proposed as a classical auxiliary layer, not a quantum component.

---

## 10. Current Status Limitation

As of 2026-06-03:

- No physical optical bead prototype has been built.
- No experimental symbol error rate data exists.
- All results are from software simulation under simplified noise models.
- The framework is conceptual and requires experimental validation.

---

*Back to [README.md](../README.md)*

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
