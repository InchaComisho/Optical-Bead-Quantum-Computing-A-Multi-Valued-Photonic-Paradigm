# Diagram: Optical Bead Computing System Architecture

**Part of:** [Optical Bead Computing](../README.md)

This document contains system architecture diagrams for the Optical Bead Computing framework at different levels of abstraction.

---

## 1. Top-Level System Architecture

```mermaid
graph LR
    Input["Input Data\n(values, symbols,\npatterns)"]
    Encoder["Encoder\n(maps values to\nbead state vectors)"]
    Generator["Optical State\nGenerator\n(produces light with\nspecified DOF states)"]
    Channel["Optical Channel\n& Transformation\n(propagation, filtering,\nmodulation)"]
    Noise["Noise Sources\n(thermal, shot noise,\njitter, drift)"]
    Decoder["Decoder\n(nearest-neighbor\nor ML classifier)"]
    Output["Decoded Output\n(values, symbols,\npatterns)"]
    ErrorCorr["Error Correction\n(redundancy coding,\nFEC)"]

    Input --> Encoder
    Encoder --> Generator
    Generator --> Channel
    Noise --> Channel
    Channel --> ErrorCorr
    ErrorCorr --> Decoder
    Decoder --> Output
```

---

## 2. Encoder Detail

```mermaid
graph TB
    Val["Input value N\n(integer in [0, N_alphabet-1])"]
    AlphLookup["Alphabet lookup\nB_N = alphabet[N]"]
    StateVec["State vector B\n= (λ, P, φ, τ, w, s, ℓ)"]

    Val --> AlphLookup
    AlphLookup --> StateVec

    StateVec --> LamCtrl["Wavelength control\nλ → laser drive / filter select"]
    StateVec --> PolCtrl["Polarization control\nP → waveplate / modulator"]
    StateVec --> PhiCtrl["Phase control\nφ → EOM or PZT"]
    StateVec --> TauCtrl["Time-bin control\nτ → pulse trigger timing"]
    StateVec --> SpCtrl["Spatial mode control\ns → beam router / port select"]
```

---

## 3. Decoder Detail

```mermaid
graph TB
    Detect["Multi-channel detector\n(spectrometer + polarimeter\n+ timing electronics)"]
    MeasVec["Measured state vector\nB_received = (λ_m, P_m, τ_m, ...)"]
    DistCalc["Distance calculation\nd(B_received, B_i) for all i"]
    NNSearch["Nearest-neighbor search\nargmin_i d(B_received, B_i)"]
    DecodedIdx["Decoded index i*"]

    Detect --> MeasVec
    MeasVec --> DistCalc
    DistCalc --> NNSearch
    NNSearch --> DecodedIdx
```

---

## 4. Phase 1 Hardware Architecture (Classical Prototype)

```
┌─────────────────────────────────────────────────────────────────┐
│                Phase 1 Hardware Block Diagram                   │
│                                                                 │
│  ┌──────────────┐    ┌────────────────┐    ┌────────────────┐  │
│  │  RGB Diode   │───▶│  Polarizing    │───▶│  Optical path  │  │
│  │  Laser Array │    │  Filter /      │    │  (free space   │  │
│  │  (3–4 λ)     │    │  Waveplate     │    │  or short       │  │
│  └──────────────┘    └────────────────┘    │  fiber)        │  │
│                                            └───────┬────────┘  │
│                                                    │           │
│  ┌──────────────┐    ┌────────────────┐    ┌──────▼─────────┐  │
│  │  Python      │◀───│  Signal proc.  │◀───│  Color sensor  │  │
│  │  Decoder     │    │  (Arduino /    │    │  or compact    │  │
│  │  (nearest    │    │  RPi ADC)      │    │  spectrometer  │  │
│  │  neighbor)   │    └────────────────┘    └────────────────┘  │
│  └──────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘

DOFs used: λ (wavelength), P (polarization)
Target alphabet: 6–24 states
```

---

## 5. Software Simulation Architecture (Phase 0)

```mermaid
graph TB
    subgraph Simulator["simulator/ (Python)"]
        AlphDef["encode_decode.py\nAlphabet definition\nbuild_alphabet()"]
        EncFunc["encode(value, alphabet)\n→ state tuple"]
        NoiseFunc["noise_model.py\ngaussian_noise()\ntemporal_jitter()\nchannel_drift()\nspectral_crosstalk()"]
        DecFunc["decode(received, alphabet)\n→ index (nearest neighbor)"]
        ConfMat["confusion_matrix.py\ncompute_confusion_matrix()\nprint_confusion_matrix()\nplot_confusion_matrix()"]
        SERFunc["symbol_error_rate()\nser_vs_sigma_sweep()"]
    end

    AlphDef --> EncFunc
    EncFunc --> NoiseFunc
    NoiseFunc --> DecFunc
    DecFunc --> ConfMat
    ConfMat --> SERFunc
```

---

## 6. Three-Layer Architecture Overview

```mermaid
graph TB
    subgraph L3["Layer 3: Quantum Optical Bead Computing (long-term)"]
        QSrc["Single-photon source\n(SPDC / quantum dot)"]
        QDet["Single-photon detector\n(SNSPD / APD)"]
        QGate["Quantum gates\n(beam splitter, phase shifter)"]
        Qudit["Qudit state space\n|ψ⟩ in d-dimensional Hilbert space"]
    end

    subgraph L2["Layer 2: Quantum-Inspired OBQC (medium-term research)"]
        QiEnc["Qudit-structured encoding\n(time-bin / frequency-bin structure)"]
        QiDec["High-dim classical decoding\n(homodyne / heterodyne)"]
        QiAna["Density-matrix analysis tools\n(applied to classical mixed states)"]
    end

    subgraph L1["Layer 1: Deterministic Optical Bead Computing (near-term focus)"]
        ClassSrc["Classical light source\n(LED / diode laser)"]
        ClassDet["Classical detector\n(color sensor / spectrometer)"]
        ClassEnc["Multi-valued encoding\n(λ, P, τ, ...)"]
        SWsim["Software simulator\n(Python)"]
    end

    L1 -->|"encoding structure\ncompatible with"| L2
    L2 -->|"extends to\nsingle-photon regime"| L3
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
