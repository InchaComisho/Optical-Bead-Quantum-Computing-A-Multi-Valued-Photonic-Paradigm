# Optical Medium Stabilization for Optical Bead Computing

**Part of:** [Optical Bead Computing](../README.md)

---

## Purpose

The optical bead channel does not have to be open air. For near-term classical prototypes, the optical path can be enclosed, sealed, filled with liquid, or formed as a solid transparent block. Each approach changes the stability characteristics of the channel and affects which optical bead states remain reliably distinguishable.

This document surveys the principal optical medium options for OBQC prototypes, explains their physical trade-offs, and provides guidance for choosing a medium for Phase 1 and Phase 2 experiments.

**This document does not claim that any single medium is universally superior.** The best choice depends on the target degrees of freedom, available equipment, required stability, and budget.

---

## Why Open-Air Optical Paths Are Fragile

An open-air free-space optical path is the easiest to build but the most environmentally fragile. Noise sources include:

| Source | Mechanism | Affected DOFs |
|---|---|---|
| Dust contamination | Particle scattering randomly attenuates the beam | Amplitude, wavelength |
| Humidity variation | Water vapor changes refractive index and causes absorption bands | Wavelength, amplitude |
| Air turbulence (heat shimmer) | Refractive index fluctuations distort the wavefront | Phase, spatial mode |
| Thermal gradients | Differential heating of air causes beam steering | Phase, spatial mode |
| Mechanical vibration | Mirror and lens movement shifts beam pointing | Spatial mode, alignment |
| Optical alignment drift | Thermal expansion of mounts slowly drifts beam position | All DOFs |
| Random scattering | Aerosols and dust cause intermittent signal drops | Amplitude |

For an educational demonstration with large alphabet separability margins, open air may be acceptable. For reproducible multi-state encoding with tight margins, open-air paths require additional enclosure.

---

## Sealed Air or Nitrogen Cell

The simplest stabilization step is to enclose the optical path inside a sealed chamber filled with dry air or nitrogen.

**How it works:** A rigid enclosure with optical-quality windows replaces the open-air path. The interior is purged with dry nitrogen or clean dry air and sealed. Temperature control can be added if needed.

**Advantages:**
- Eliminates dust contamination from the beam path
- Eliminates humidity variation (sealed dry gas)
- No liquid absorption or bubble risk
- Mechanically simple to build from off-the-shelf parts
- Low cost

**Limitations:**
- Temperature variation still shifts the refractive index of the gas and causes thermal expansion of the cell
- Pressure variation (barometric) causes small RI changes (negligible for most prototypes)
- Mechanical alignment inside the cell still drifts unless actively stabilized
- Does not reduce thermal turbulence at elevated temperatures unless cooled uniformly

**Best use:** Near-term desktop prototype where dust and humidity are the primary concerns. Suitable for wavelength and polarization encoding with moderate stability requirements.

---

## Sealed Liquid Optical Cell

A transparent liquid-filled optical cell reduces air-turbulence noise and eliminates dust, while providing refractive-index matching to the optical windows.

**Candidate media:**

| Liquid | Transparency | Refractive index | dn/dT (K^-1) | Thermal stability | Notes |
|---|---|---|---|---|---|
| Ultra-pure water | 200-1300 nm | 1.333 | -1.0e-4 | Moderate | Readily available; requires degassing and sealing |
| Silicone oil | 350-2000 nm | 1.40-1.50 | -4.0e-4 | Low | Low vapor pressure; chemically stable; high dn/dT |
| Index-matching liquid | Specified by vendor | 1.46-1.52 | -3.5e-4 | Moderate | Designed for optical use; expensive |
| Glycerol-water | 200-1200 nm | 1.33-1.47 | -2.5e-4 | Moderate | Tunable RI by concentration |
| Fluorinert FC-770 | 250-2000 nm | 1.275 | -1.7e-4 | High | Broad range; chemically inert; expensive |

**Note on ultra-pure water:** Ultra-pure water must be treated as a sealed liquid medium, not a solid material. It requires careful handling: degassing to remove dissolved air (which nucleates bubbles), sealing against contamination, and temperature control to limit dn/dT effects. A standard spectroscopy cuvette (10 mm path length) provides a practical starting cell.

**Advantages:**
- Eliminates open-air turbulence and dust
- Refractive-index matching to window glass reduces reflections
- Mechanically stable (liquid resists transverse beam displacement)
- Moderate cost with commodity glassware

**Limitations:**
- Absorption loss (wavelength-dependent; typically small for visible wavelengths in 10 mm cells)
- Bubble scattering: dissolved gas can nucleate if temperature rises; requires degassing
- Temperature-dependent RI drift: water dn/dT = -1e-4 /K. At 5 cm path length and 0.1 K temperature change, phase shifts by ~5 rad — completely scrambling phase-encoded states. See [docs/sealed-liquid-optical-bead-medium.md](sealed-liquid-optical-bead-medium.md).
- Long-term contamination from container materials (leaching of plasticizers from polymer cells)
- Liquid convection under thermal gradients introduces slow refractive-index fluctuations

**Key practical finding (from simulation):** Phase encoding through a centimeter-scale liquid cell is impractical without sub-millikelvin temperature control. Wavelength and polarization DOFs are far more tolerant of thermal drift and are recommended for Phase 1 liquid-cell prototypes.

**Best use:** Phase 1 classical OBQC prototype using wavelength and polarization encoding, where dust elimination and moderate stability improvement justify the added complexity of a sealed cell.

---

## Solid Transparent Optical Block

Instead of a liquid-filled cell, the optical path may be cast or machined as a solid transparent block. The block replaces the air gap with a material that does not flow, convect, or evaporate.

**Candidate materials:**

| Material | Transmission range | Refractive index | Thermal expansion (CTE) | Stress birefringence | Notes |
|---|---|---|---|---|---|
| Acrylic / PMMA | 380-2000 nm | 1.49 | 70 ppm/K | Moderate to high | Low cost; easy to cast; yellows over time with UV |
| Optical resin (UV-cure) | 380-1500 nm | 1.50-1.56 | 50-100 ppm/K | Moderate | Moldable; may trap bubbles |
| Borosilicate glass | 300-2500 nm | 1.52 | 3.3 ppm/K | Very low | Optical quality; requires machining or molding |
| Fused silica / quartz | 180-2500 nm | 1.46 | 0.55 ppm/K | Very low | Broadest range; low CTE; most expensive |
| Sapphire | 150-5500 nm | 1.77 | 5.3 ppm/K | Low (uniaxial) | Extreme broadband; very hard; expensive |

**Potential advantages:**
- No air turbulence, no liquid convection, no dust
- Fixed optical path geometry after curing or machining
- Compact and mechanically stable
- Easy to fabricate low-cost prototypes with acrylic (casting in a mold)
- Educational demonstration model: the optical bead path is visible inside the block

**Limitations — important for OBQC use:**

*Trapped bubbles:* Cast resins and some acrylic blocks contain microscopic bubbles from the casting process. Bubbles scatter light randomly, adding amplitude noise. Careful degassing of the liquid resin before casting reduces this risk.

*Curing shrinkage:* Polymer resins shrink during curing (typically 2-10% by volume). Shrinkage creates internal mechanical stress that can vary across the block, distorting the optical path.

*Stress-induced birefringence:* Residual mechanical stress from curing or machining rotates the polarization state of transmitted light. This is the most critical limitation for OBQC: any prototype that uses polarization as an encoding DOF will be degraded by stress birefringence in polymer blocks. Acrylic and optical resins have significant stress birefringence. Optical glass and quartz have far lower residual stress.

*Thermal expansion:* PMMA has a CTE of ~70 ppm/K — much higher than glass (~3 ppm/K) or quartz (~0.55 ppm/K). A 10 cm PMMA block changes length by 0.7 mm per 1°C temperature change. This causes phase shifts if the block is part of an interferometric path.

*Long-term yellowing:* Some acrylic grades absorb UV light and gradually yellow, reducing transmission at short wavelengths. Use UV-stabilized grades for long-term prototypes.

*Phase distortion from inhomogeneity:* Refractive index variations across the block (from composition gradients, density variations, or stress) cause wavefront distortion that varies spatially, affecting phase encoding.

**Classification by DOF suitability:**

| DOF | Acrylic/PMMA | Optical resin | Glass | Quartz |
|---|---|---|---|---|
| Wavelength (color) | Good | Good | Excellent | Excellent |
| Intensity / amplitude | Good | Good | Excellent | Excellent |
| Spatial position | Good | Good | Excellent | Excellent |
| Polarization | Poor (birefringence) | Moderate | Good | Excellent |
| Phase | Poor (CTE, stress) | Poor-Moderate | Good | Excellent |
| Time-bin | Good (timing, not material) | Good | Good | Good |

**Best use:** Acrylic or optical resin blocks are good for Phase 1 prototypes that use wavelength, position, or intensity encoding. For polarization-sensitive or phase-sensitive OBQC, use optical glass, quartz, fiber, or waveguides.

---

## Fiber and Waveguide Implementation

For practical long-term photonic implementation, guided optical paths (fiber, planar waveguides, photonic integrated circuits) offer the highest stability.

**Fiber types relevant to OBQC:**

| Fiber type | Primary use | Relevant OBQC DOFs |
|---|---|---|
| Single-mode fiber (SMF) | One spatial mode; long-distance | Wavelength, phase, polarization (with PMF) |
| Polarization-maintaining fiber (PMF) | Stable polarization propagation | Wavelength + polarization |
| Multimode fiber (MMF) | Multiple spatial modes | Spatial mode encoding |
| Few-mode fiber (FMF) | Controlled number of spatial modes | Spatial mode (up to ~10 modes) |
| Photonic crystal fiber | Tailored dispersion and mode confinement | Specialized DOFs |

**Advantages:**
- Guided mode: eliminates free-space alignment sensitivity entirely
- Compact and stable against vibration (flexible cable)
- Less environmental exposure than open-air or liquid-cell setups
- Single-mode fiber ensures consistent mode profile
- Compatible with photonic integrated circuit (PIC) components
- Scalable for multi-channel systems using fiber bundles or WDM

**Limitations:**
- Coupling loss: light must be efficiently coupled into the fiber core (typically requires precision micro-optics)
- Polarization drift in standard SMF: fiber bending and temperature change cause random polarization rotation; use PMF for stable polarization encoding
- Dispersion: wavelength channels spread in time over long fiber lengths; use short fibers for low-dispersion prototypes
- Waveguide crosstalk: closely spaced waveguides in PICs can couple optical energy
- Material constraints: choice of wavelength range limited by fiber transmission window
- Higher fabrication cost and technical complexity than open-air or block prototypes

**Best use:** Advanced prototypes after the open-air or block prototype has validated the encoding strategy. Necessary for any scalable photonic integration.

---

## Classical vs Quantum Considerations

All media discussed above are evaluated primarily for **classical OBQC** — deterministic multi-valued optical state encoding using macroscopic light pulses.

For quantum optical extensions (Phase 3 in the roadmap), the requirements are fundamentally stricter:

| Requirement | Classical OBQC | Quantum OBQC / qudit extension |
|---|---|---|
| Loss tolerance | High: many photons per pulse; loss reduces SNR gradually | Very low: loss destroys single photons; reduces entanglement fidelity |
| Scattering tolerance | Moderate: spurious scatter adds amplitude noise | Very low: each scattering event can destroy quantum coherence |
| Phase stability | Important for phase DOF; moderate tolerance otherwise | Critical: phase coherence required for quantum interference |
| Detector requirement | Standard photodetector or spectrometer | Single-photon detector (SNSPD or APD); timing jitter < 100 ps |
| Decoherence | Not applicable (classical system) | Strict; limits gate fidelity and entanglement lifetime |
| Temperature | Standard temperature control | May require cryogenic temperatures for some sources/detectors |

**A sealed liquid cell or acrylic block that works well for classical OBQC is not automatically suitable for quantum optical bead computing.** The transition to Phase 3 (qudit-compatible quantum extension) requires fiber or waveguide quality optical paths with controlled coupling, minimal scattering, and single-photon-compatible components.

---

## Candidate Medium Comparison Table

| Medium | Stability | Prototype cost | Main advantage | Main limitation | Best use case |
|---|---:|---:|---|---|---|
| Open air | Low | Very low | Simplest to build | Dust, humidity, turbulence | First demonstration |
| Sealed air / nitrogen | Medium | Low | Dust and humidity reduction | Temperature and pressure sensitive | Stable classroom prototype |
| Sealed liquid (water, silicone oil) | Medium-high | Medium | No turbulence; index matching | Bubbles, thermal RI drift, phase instability | Classical OBQC test cell; wavelength + polarization |
| Acrylic / PMMA block | Medium | Low-medium | Solid, compact, no convection | Stress birefringence, bubbles, thermal expansion | Color/position/intensity encoding only |
| Optical glass / quartz | High | Medium-high | Low stress, low absorption, high stability | Machining cost | Precision prototype; polarization and phase capable |
| Fiber / waveguide | Very high | High | Guided path; scalable | Coupling complexity, dispersion | Advanced and scalable implementation |
| Photonic integrated circuit | Very high | Very high | Full integration | Fabrication barrier | Long-term research platform |

No single medium is optimal for all use cases. The recommended progression for OBQC prototyping is:

1. Open air or sealed air for initial feasibility tests
2. Sealed liquid cell or acrylic block for improved stability with wavelength/intensity encoding
3. Optical glass, quartz, or fiber for polarization and phase encoding
4. Fiber / waveguide for scalable engineered systems

---

## Falsifiable Experiments

The following experiments can compare optical media with measurable outcomes:

1. **SER vs medium:** Encode the same M-state alphabet through open-air, sealed-air, sealed-liquid, and acrylic-block paths. Measure symbol error rate for each. Expected result: SER decreases as medium stability increases.

2. **Temperature sensitivity:** For each medium, measure SER as temperature changes from 20°C to 30°C. Expected result: liquid and polymer media show larger SER increase than glass or quartz.

3. **Long-term stability:** Record SER every hour for 8 hours without recalibration. Expected result: open-air and liquid media drift more than glass or sealed-air media.

4. **Polarization stability:** Send a polarization-encoded alphabet through acrylic vs glass. Measure confusion between polarization states. Expected result: acrylic shows higher polarization confusion due to birefringence.

5. **Bubble injection:** Deliberately introduce a small bubble into a sealed liquid cell. Measure amplitude noise increase. Expected result: SER increases proportionally to bubble scattering cross-section.

6. **DOF comparison by medium:** Test wavelength-only, polarization-only, and wavelength+polarization alphabets through each medium. Identify which medium-DOF combinations produce the best SER.

---

## Summary

OBQC optical bead states can be transmitted through multiple optical media. The goal is to find a medium that preserves the distinguishability of the chosen optical bead alphabet under realistic environmental conditions.

The near-term recommendation is:
- Start with **sealed air** or **open air** for initial proof-of-concept
- Move to **sealed liquid** (ultra-pure water or silicone oil, 10 mm cuvette) for reduced turbulence and dust, using wavelength and polarization only
- Use **optical glass or quartz** when polarization or phase encoding is required
- Consider **fiber or waveguide** paths for any production or scalable implementation
- Reserve **quantum optical** extensions for after the classical prototype has validated the encoding strategy

The simulator at [simulator/optical_medium_comparison.py](../simulator/optical_medium_comparison.py) provides a simplified engineering model for comparing effective noise levels across media under different alphabet sizes.

---

*Back to [README.md](../README.md)*  
*See also: [docs/sealed-liquid-optical-bead-medium.md](sealed-liquid-optical-bead-medium.md) | [docs/limitations.md](limitations.md) | [diagrams/optical-medium-options.md](../diagrams/optical-medium-options.md)*
