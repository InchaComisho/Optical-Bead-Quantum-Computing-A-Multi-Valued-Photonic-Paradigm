# Optical Bead State Model

**Part of:** [Optical Bead Computing](../README.md)

---

## 1. The State Vector

An optical bead state is a tuple of values, one per degree of freedom (DOF) of light:

```
B = (λ, P, φ, τ, w, s, ℓ)
```

This vector represents the multi-dimensional configuration of a single optical pulse or signal mode. Like a soroban bead configuration that represents a number, the optical bead state B represents an information symbol through its full multi-dimensional pattern.

---

## 2. Degrees of Freedom

### 2.1 Wavelength (λ)

The wavelength or frequency of the optical carrier. In practice, this corresponds to the spectral channel.

- Discretization: divide the accessible spectral range into n_λ distinguishable bands.
- Practical constraint: adjacent channels must be separated enough that a detector can reliably distinguish them given spectral linewidth, filter bandwidth, and noise.
- Example: 4 levels at 450 nm, 532 nm, 633 nm, 780 nm using diode lasers.

### 2.2 Polarization (P)

The orientation and ellipticity of the electric field oscillation.

- Common discrete states: H (horizontal), V (vertical), D (diagonal, +45°), A (anti-diagonal, −45°), R (right circular), L (left circular).
- Practical constraint: polarization states must be distinguishable given polarization measurement noise, birefringence in optical components, and polarization-mode dispersion in fibers.
- Example: 4 levels using H, V, D, A.

### 2.3 Phase (φ)

The absolute or relative optical phase.

- Common discrete states: 0, π/2, π, 3π/2 for a 4-level phase alphabet.
- Practical constraint: phase measurement requires a reference (interferometric measurement). Phase instability due to thermal fluctuations is a significant noise source.
- Near-term consideration: phase encoding is the most technically demanding DOF for classical prototyping and may be deferred to later prototype phases.

### 2.4 Time-Bin (τ)

The assignment of an optical pulse to a discrete time bin within a defined frame window.

- Discretization: divide the frame period into n_τ time bins; a pulse is assigned to exactly one bin.
- Practical constraint: adjacent bins must be separated by more than the timing jitter of the source and detector.
- Example: 4 time bins within a 10 ns frame using 1 ns pulses and < 200 ps jitter.

### 2.5 Pulse Width (w)

The temporal duration of the optical pulse.

- Discretization: narrow, medium, wide (3 levels), or finer with better timing resolution.
- Practical constraint: pulse width must be distinguishable given detector bandwidth and temporal broadening in the optical channel.

### 2.6 Spatial Mode (s)

The transverse spatial profile or the physical position of the optical beam.

- In free-space: different spatial positions or waveguide ports.
- In fiber: spatial modes in multi-mode or few-mode fiber.
- Example: 4 spatial positions using a 2×2 array of spatial channels.

### 2.7 Orbital Angular Momentum (ℓ)

The topological charge of the optical vortex, corresponding to helical wavefront structure.

- Values: ℓ = 0 (Gaussian), ±1, ±2, ±3, …
- Practical constraint: OAM mode generation and detection requires specialized optics (spiral phase plates, spatial light modulators, q-plates). Atmospheric turbulence strongly degrades OAM modes in free-space propagation.
- Near-term consideration: OAM is appropriate for laboratory prototypes in controlled free-space environments; less suitable for fiber-based near-term prototyping.

---

## 3. Alphabet Definition

An optical bead alphabet is a finite set of distinct state vectors:

```
A = { B_0, B_1, B_2, ..., B_{N-1} }
```

where each B_i is a specific assignment of values to the degrees of freedom.

The alphabet may use all available DOFs, or a subset, depending on the prototype phase:

| Prototype Phase | DOFs Used | Example Alphabet Size |
|---|---|---|
| Phase 1 | λ, P | 4 × 4 = 16 states |
| Phase 1 extended | λ, P, τ | 4 × 4 × 4 = 64 states |
| Phase 2 | λ, P, φ, τ | 4 × 4 × 4 × 4 = 256 states |
| Phase 3 (quantum) | λ, P, φ, τ, ℓ | 4 × 4 × 4 × 4 × 4 = 1024 theoretical states |

**These are theoretical upper bounds.** The practical alphabet size is determined by the minimum inter-state distance that can be reliably decoded above the target accuracy threshold.

---

## 4. Distance Metric and Nearest-Neighbor Decoding

For decoding, a distance metric is needed to assign a received (noisy) state to the closest alphabet member.

The default metric is the normalized Euclidean distance in the multi-dimensional state space:

```
d(B_received, B_i) = sqrt( sum_j ( (B_received[j] - B_i[j]) / range_j )^2 )
```

where range_j is the range of values for DOF j, used to normalize each dimension to [0, 1].

The decoder assigns:

```
B_decoded = argmin_{B_i in A} d(B_received, B_i)
```

A decoding error occurs when B_decoded ≠ B_transmitted.

---

## 5. Separability Margin

The separability margin of an alphabet is the minimum distance between any two distinct alphabet members:

```
margin = min_{i ≠ j} d(B_i, B_j)
```

A larger margin provides more tolerance for noise before decoding errors occur. The critical noise threshold — the noise level at which decoding accuracy begins to fall below a target threshold — scales approximately with margin / 2.

Alphabet design should maximize the minimum margin given the physical constraints of the implementation.

---

## 6. Example Alphabets

### Minimal 6-State Alphabet (Phase 1 feasibility test)

Using wavelength (3 levels: 450 nm, 532 nm, 633 nm) and polarization (2 levels: H, V):

```
B_0 = (450 nm, H)
B_1 = (450 nm, V)
B_2 = (532 nm, H)
B_3 = (532 nm, V)
B_4 = (633 nm, H)
B_5 = (633 nm, V)
```

### 16-State Alphabet

Using wavelength (4 levels) and polarization (4 levels):

```
B_(i,j) = (λ_i, P_j)  for i in {0,1,2,3}, j in {0,1,2,3}
```

### Encoded Digits (0–9)

Using 10 states from the 16-state alphabet, with 6 states as spare/error codes:

```
digit 0 → B_(0,0) = (λ_0, P_0)
digit 1 → B_(0,1) = (λ_0, P_1)
...
digit 9 → B_(2,1) = (λ_2, P_1)
```

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
