# Diagram: Optical Medium Options for OBQC

**Part of:** [Optical Bead Computing](../README.md)

This document illustrates the four principal optical medium configurations for OBQC prototypes: open-air free-space, sealed liquid cell, solid transparent block, and fiber/waveguide.

---

## A. Open-Air Free-Space Path

The simplest configuration: source and detector face each other across an open gap.

```mermaid
graph LR
    S["Light Source\n(LED / diode laser)"]
    A["Open air\n(dust, humidity,\nturbulence)"]
    D["Detector\n(color sensor /\nspectrometer)"]

    S -->|"optical bead state"| A
    A -->|"attenuated +\ndisturbed state"| D
```

**Notes:**
- No fabrication required beyond mounting source and detector
- All environmental disturbances (dust, humidity, air turbulence, thermal gradients) are fully present
- Alignment drift is common over time
- Suitable for first demonstrations only
- Recommended encoding DOFs: wavelength (color), intensity

---

## B. Sealed Gas Cell (Air or Nitrogen)

A rigid enclosure with optical windows. Interior filled with dry air or nitrogen and sealed.

```mermaid
graph LR
    S["Light Source"]
    W1["Input Window\n(anti-reflection\ncoated glass)"]
    G["Dry air / N2\n(sealed, filtered)"]
    W2["Output Window"]
    D["Detector"]

    S --> W1
    W1 -->|"enclosed path"| G
    G --> W2
    W2 --> D
```

**Notes:**
- Eliminates dust and humidity from the beam path
- Temperature variation still affects gas RI and alignment
- Easy to build: use an off-the-shelf metal tube or box with mounted windows
- Recommended encoding DOFs: wavelength, polarization

---

## C. Sealed Liquid Optical Cell

A glass or quartz cuvette filled with a transparent liquid (ultra-pure water, silicone oil, or index-matching fluid) and sealed.

```mermaid
graph LR
    S["Light Source"]
    W1["Input Window\n(glass / quartz)"]
    L["Liquid medium\n(degassed, sealed)\nwater / silicone oil /\nindex-matching liquid"]
    W2["Output Window"]
    D["Detector"]
    TC["Temperature\nController"]

    S --> W1
    W1 -->|"no turbulence"| L
    L --> W2
    W2 --> D
    TC -. "stabilizes dn/dT" .-> L
```

**Notes:**
- Eliminates air turbulence; reduces dust; provides index matching at windows
- Temperature control (Peltier) is important to limit thermal RI drift
- Phase encoding is impractical at centimeter-scale path lengths (5 rad/0.1K)
- Bubbles must be removed by degassing before filling
- Recommended DOFs: wavelength + polarization (avoid phase for L > 1 mm)

---

## D. Solid Transparent Optical Block

The optical path is cast or machined as a monolithic solid block of transparent material.

```mermaid
graph LR
    S["Light Source"]
    B["Transparent block\n(acrylic / glass / quartz)\n- no convection\n- no evaporation\n- fixed geometry"]
    D["Detector"]

    S -->|"enters block"| B
    B -->|"exits block"| D
```

**Notes:**
- No moving parts, no liquid, no convection
- Acrylic / PMMA: easy to cast, low cost, but has stress birefringence and high CTE
- Optical glass or quartz: low stress, low CTE, suitable for polarization and phase
- Bubble trapping during casting is a significant risk; degassing required
- Recommended DOFs (acrylic): wavelength, intensity, spatial position
- Recommended DOFs (glass/quartz): all DOFs including polarization and phase

---

## E. Fiber / Waveguide Path

The optical bead channel is guided through a fiber or planar waveguide.

```mermaid
graph LR
    S["Light Source"]
    C1["Input Coupler\n(micro-optic lens)"]
    F["Fiber / Waveguide\n(SMF, PMF, MMF,\nor PIC waveguide)"]
    C2["Output Coupler /\nBeamsplitter"]
    D["Detector array"]

    S --> C1
    C1 -->|"guided mode"| F
    F --> C2
    C2 --> D
```

**Notes:**
- Guided path: immune to free-space alignment drift
- Single-mode fiber (SMF): stable spatial mode; suitable for wavelength, phase
- Polarization-maintaining fiber (PMF): stable polarization axis; suitable for polarization encoding
- Coupling precision is critical; even small misalignment causes large coupling loss
- Compatible with photonic integrated circuits (PICs) for scalable implementation
- Recommended DOFs: wavelength, polarization (with PMF), phase (short fiber)

---

## F. Medium Progression for OBQC Prototyping

```mermaid
graph TD
    A["Phase 0:\nSoftware simulation\n(no hardware)"]
    B["Phase 1a:\nOpen air\nor sealed air\n(feasibility, wavelength+intensity)"]
    C["Phase 1b:\nSealed liquid cell\n(stability, wavelength+polarization)"]
    D["Phase 2a:\nAcrylic block\n(compact, wavelength+position)"]
    E["Phase 2b:\nGlass or quartz block\n(polarization capable)"]
    F["Phase 3:\nFiber / waveguide\n(scalable, all DOFs)"]
    G["Phase 4 (long-term):\nPhotonic integrated circuit\n(quantum compatible)"]

    A --> B
    B --> C
    B --> D
    C --> E
    D --> E
    E --> F
    F --> G
```

**The progression is not mandatory.** Each step is independently useful. A Phase 1 open-air or sealed-air prototype can validate the encoding concept before any liquid or solid medium is used.

---

## G. Noise Level Summary (Qualitative)

```
Medium          Dust    Humidity  Turbulence  Bubble  Stress-bire  Thermal-RI
----------      ----    --------  ----------  ------  -----------  ----------
Open air        HIGH    HIGH      HIGH        none    none         MED
Sealed air      low     low       none        none    none         MED
Sealed liquid   none    none      none        MED     none         HIGH (water)
Acrylic block   none    none      none        MED     MED-HIGH     MED
Glass / quartz  none    none      none        none    low          low
Fiber / wave    none    none      none        none    low (bend)   low

Lower is better. MED = moderate. HIGH = significant design concern.
```

---

*Back to [README.md](../README.md)*  
*See also: [docs/optical-medium-stabilization.md](../docs/optical-medium-stabilization.md)*
