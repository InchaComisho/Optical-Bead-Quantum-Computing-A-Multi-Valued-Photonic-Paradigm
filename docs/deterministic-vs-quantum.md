# Deterministic OBQC vs Quantum OBQC

**Part of:** [Optical Bead Computing](../README.md)

---

## Overview

Optical Bead Computing (OBC) is organized into three distinct layers that differ in their physical requirements, maturity, and research goals. These layers are not competing alternatives — they are sequential levels of abstraction that build on each other.

| Layer | Name | Physical Basis | Timeline |
|---|---|---|---|
| Layer 1 | Deterministic Optical Bead Computing | Classical macroscopic optics | Near-term |
| Layer 2 | Quantum-Inspired OBQC | Classical optics with qudit-like encoding structure | Medium-term research |
| Layer 3 | Quantum Optical Bead Computing | Single-photon quantum optics | Long-term research |

---

## Layer 1: Deterministic Optical Bead Computing

### Definition

Deterministic OBQC uses macroscopic optical signals (many-photon pulses) from classical light sources (LEDs, diode lasers) to encode, transmit, and decode multi-valued optical bead states.

There is no quantum coherence, no entanglement, and no superposition of states. Each transmitted pulse is in one definite optical bead state from the alphabet.

### Physical Requirements

- Diode laser or LED light source
- Wavelength-selectable source (e.g., tunable laser or filter bank)
- Polarizing optics (polarizers, waveplates, polarizing beam splitters)
- Optical modulator (for phase or temporal encoding in later phases)
- Photodetector, color sensor, or spectrometer
- Signal processing software (Python-based)

### Computational Character

Deterministic OBQC is a *multi-valued classical optical encoding system*. It is analogous to QAM or multi-level modulation in optical communications, but structured as a multi-dimensional bead pattern alphabet rather than a maximally efficient binary-compatible modulation format.

The computational interest lies in:
- Whether pattern-based encoding offers structural advantages for specific tasks
- How the practical alphabet size scales with physical noise parameters
- Whether soroban-inspired pattern operations (not just encoding) can be implemented optically

### Status

This is the primary near-term focus of this repository. Software simulation is available in the `simulator/` directory. Hardware prototype design is in planning.

---

## Layer 2: Quantum-Inspired OBQC

### Definition

Quantum-Inspired OBQC borrows structural concepts from qudit (d-dimensional quantum) research — specifically the idea of high-dimensional state spaces and multi-basis encoding — and applies them to classical optical systems or to optical systems that use quantum-like state structure without requiring full quantum coherence.

Examples:
- Using time-frequency encoding structures analogous to qudit bases, but with classical pulses
- Designing encoding alphabets that would be compatible with single-photon protocols if the source were upgraded
- Using density-matrix-like analysis tools for error characterization, applied to classical mixed-state analogs

### Why This Layer Exists

Many optical encoding techniques developed for quantum communication (time-bin qudits, frequency-bin qudits, OAM mode qudits) can be used classically first — with many-photon pulses and standard detectors — to test encoding/decoding strategies before committing to the much more demanding single-photon quantum regime.

This layer is a *research methodology bridge*, not a separate technology.

### Status

Conceptual / research framework. No hardware implementation. Relevant literature includes:
- Time-bin qudit encoding in optical fiber
- Frequency-bin qudit encoding with electro-optic combs
- OAM mode multiplexing for classical and quantum communications

---

## Layer 3: Quantum Optical Bead Computing

### Definition

Quantum Optical Bead Computing extends OBQC to single-photon quantum states, where each optical bead state vector represents a quantum state of light, and operations are quantum gates acting on multi-dimensional (qudit) Hilbert spaces.

In this layer:
- Information is encoded in single-photon qudits (d-level quantum systems)
- Superposition and entanglement of optical bead states are physically real
- Quantum interference plays a role in computation
- Quantum error correction is required for useful computation

### Physical Requirements

- Single-photon sources (SPDC, quantum dots, NV centers)
- Single-photon detectors (SNSPD, APD)
- Interferometric stability at the single-photon level
- Quantum gate elements (beam splitters, phase shifters, nonlinear optical elements)
- Cryogenic infrastructure (for some detector and source types)

### Relation to Qudit Quantum Computing

Qudit quantum computing is an active research area. Qudits (d > 2) can offer advantages in:
- Reducing circuit depth for certain algorithms
- More efficient encoding of multi-valued classical data
- Simplifying quantum error correction codes

OBQC's quantum extension aims to position soroban-inspired multi-dimensional encoding as a natural fit for qudit quantum systems. However, this is a long-term research direction that depends on advances in qudit quantum hardware.

### Status

Long-term research direction. No hardware prototype. No demonstrated quantum advantage.

---

## Key Distinction Summary

| Property | Layer 1 (Deterministic) | Layer 2 (Q-Inspired) | Layer 3 (Quantum) |
|---|---|---|---|
| Quantum coherence required | No | No (but compatible structure) | Yes |
| Superposition | No | No | Yes |
| Entanglement | No | No | Yes |
| Single-photon source needed | No | No | Yes |
| Quantum advantage possible | No | No | Potentially |
| Near-term prototype feasible | Yes | Partially | No |
| Current focus of this repo | **Primary** | Secondary | Background |

---

## Common Misconception

It would be a misrepresentation to say that Optical Bead Computing "is a quantum computer" or that it uses quantum effects to achieve computational advantage. That would confuse Layer 1 with Layer 3.

The honest description is:
- Layers 1 and 2 are classical optical computing frameworks inspired by soroban pattern logic and qudit encoding structure.
- Layer 3 is a long-term research direction that has not been demonstrated.
- The near-term value is in exploring multi-valued optical encoding and its practical limits.

---

*Back to [README.md](../README.md)*
