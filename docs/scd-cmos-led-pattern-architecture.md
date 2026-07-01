# SCD-CMOS and LED-CMOS Soroban Pattern Architecture

**Repository:** `Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm`
**Status:** Conceptual extension / early-stage framework
**License:** CC BY 4.0

---

## Abstract

This document extends Optical Bead Computing (OBQC) by connecting soroban bead logic to CMOS electronics, LED optical patterns, and CMOS image-sensor readout.

The key idea is that soroban bead states and electronic High/Low signals are both physical on/off states. A decimal digit can be represented as a constrained 5-bit soroban-coded pattern (SCD: Soroban-Coded Decimal). This pattern can be driven directly onto five CMOS signal lines, displayed as an LED light pattern, and read back by a CMOS image sensor.

This is not claimed to be a universal computer, a replacement for binary arithmetic, or a more compact representation than BCD. SCD uses 5 bits per decimal digit compared to BCD's 4 bits. The additional bit is traded for structural pattern recognition, validity checking, and a conceptual bridge from electronic decimal patterns to Optical Bead Computing.

---

## From Soroban Beads to CMOS Signals

A soroban bead has two physical states: engaged (contributing to the digit value) or disengaged (not contributing). A CMOS wire has two electrical states: High (logic 1) or Low (logic 0). These are structurally the same.

Therefore, a soroban rod with one upper bead and four lower beads maps directly onto five CMOS signal lines:

| Soroban element | CMOS signal | Value when active |
|---|---|---|
| Upper bead (heaven bead) | H | 5 |
| Lower bead 1 | L1 | 1 |
| Lower bead 2 | L2 | 1 |
| Lower bead 3 | L3 | 1 |
| Lower bead 4 | L4 | 1 |

The digit value is computed as:

```
D = (H, L4, L3, L2, L1)

digit = 5*H + count(L1, L2, L3, L4)
```

The lower beads use thermometer-style encoding: active beads are filled from L1 upward without gaps. This preserves the physical logic of soroban bead positions, where earth beads accumulate from the bottom of a column.

---

## SCD Encoding Table

| Digit | H | Lower beads | 5-bit pattern |
|---:|---:|---|---|
| 0 | 0 | 0000 | 0 0000 |
| 1 | 0 | 0001 | 0 0001 |
| 2 | 0 | 0011 | 0 0011 |
| 3 | 0 | 0111 | 0 0111 |
| 4 | 0 | 1111 | 0 1111 |
| 5 | 1 | 0000 | 1 0000 |
| 6 | 1 | 0001 | 1 0001 |
| 7 | 1 | 0011 | 1 0011 |
| 8 | 1 | 0111 | 1 0111 |
| 9 | 1 | 1111 | 1 1111 |

There are 10 valid states out of 32 possible 5-bit combinations. The remaining 22 are structurally invalid by the thermometer constraint.

---

## Why SCD Is Not Just BCD

BCD (Binary-Coded Decimal) encodes one decimal digit in 4 bits. SCD uses 5 bits for the same digit. This means SCD is not more compact than BCD.

| Model | Bits per decimal digit | Valid states | Invalid states | Main advantage | Main limitation |
|---|---:|---:|---:|---|---|
| BCD | 4 | 10 / 16 | 6 / 16 | Compact decimal encoding | Less structural similarity to soroban |
| SCD | 5 | 10 / 32 | 22 / 32 | Soroban-like pattern and validity checking | Larger representation (25% more bits) |

SCD is designed to represent a decimal digit as a recognizable structural pattern — one that mirrors the physical configuration of soroban beads — rather than to minimize storage space. The 22 invalid states exist as a natural consequence of the thermometer constraint and can be used for lightweight validity checking without additional parity bits.

---

## Error Detection and Silent Errors

SCD has 22 invalid states out of 32, meaning that many random bit patterns can be immediately detected as invalid. However, not all errors are detectable.

**Detectable errors:**

Any 5-bit pattern where the lower four bits form a non-thermometer sequence (gaps between active bits) is structurally invalid and can be flagged:

```
0 0011 -> 0 0101  (gap between L2 and L4: invalid thermometer, detected error)
0 1111 -> 0 1011  (gap: detected error)
```

**Silent errors:**

If the H bit flips while the lower bits remain a valid thermometer pattern, the result is another valid digit. The error is undetected:

```
0 0000 -> 1 0000  (digit 0 becomes 5: silent error)
0 0001 -> 1 0001  (digit 1 becomes 6: silent error)
0 0011 -> 1 0011  (digit 2 becomes 7: silent error)
```

Similarly, if lower bits flip in a way that keeps the pattern thermometric:

```
0 0001 -> 0 0011  (digit 1 becomes 2: silent error)
```

**Summary:** SCD is a structural validity code, not a complete error-correcting code. It converts many random errors into detectable failures, but silent errors remain possible — particularly for single-bit flips in H or small thermometer-preserving changes in lower bits.

For reliable error correction, SCD should be combined with an additional parity or ECC layer.

---

## CMOS Implementation

A CMOS implementation can treat the five SCD lines as one decimal cell rather than five independent bits. This aligns the circuit structure with the soroban column abstraction.

### Components

- **Five signal lines per digit:** H, L1, L2, L3, L4
- **Validity checker:** Combinational logic that verifies the thermometer constraint. Detects any lower-bit pattern that is not in {0000, 0001, 0011, 0111, 1111}. Implementable as a simple gate array.
- **Thermometer-pattern detector:** Sub-circuit of the validity checker; specifically identifies the five valid lower patterns.
- **Digit decoder:** Converts valid SCD pattern to a 4-bit BCD or binary output for downstream logic.
- **Increment logic:** Follows soroban carry rules: when lower beads reach 1111 with H=0, set H=1 and clear lower; when H=1 and lower=1111, carry to next digit.
- **Decrement logic:** Follows soroban borrow rules: when H=1 and lower=0000, clear H and set lower=1111.
- **Carry/borrow propagation:** Cascades across digit cells for multi-digit arithmetic.
- **Optional ECC layer:** Additional parity or redundancy coding for silent error coverage.

The validity checker requires no external reference state. It uses only the signal values on the five lines to determine legality, making it simple to implement in combinational CMOS logic.

---

## LED-CMOS Optical Extension

LED displays and CMOS image sensors offer an intuitive bridge from SCD electronic logic to Optical Bead Computing. The same on/off structure that maps soroban beads to CMOS wires can be extended to LED light sources and sensor pixels.

### LED side

A set of five LEDs per digit can represent the SCD pattern directly. Each LED maps to one signal line. The extension to optical encoding adds several new degrees of freedom:

- **Position:** which LED in the array is active
- **Color / wavelength:** different LED colors for different bead types or roles
- **Brightness / intensity:** multiple distinguishable brightness levels per LED
- **Temporal blinking:** pulse patterns carrying additional state information
- **RGB channels:** three independent color channels per LED
- **MicroLED arrays:** high-density spatial encoding

### CMOS sensor side

A CMOS image sensor reads the spatial light pattern emitted by the LED array:

- Converts incoming light intensity at each pixel into an electronic signal
- Classifies color, intensity, and position states
- Applies a threshold or classifier model to decode the received pattern
- Can act as a multi-channel pattern reader without requiring per-channel wiring

### Electro-optical prototype path

```
SCD digital state
-> LED / RGB LED / microLED optical pattern
-> optical medium (air, sealed cell, waveguide)
-> CMOS image sensor
-> pattern classifier (nearest-neighbor, CNN, or simple threshold)
-> decoded SCD state or OBQC state
```

---

## Why LED Color Matters

Simple on/off electronics carry one bit per wire. Light adds additional degrees of freedom that do not exist in pure electronic binary systems:

| Degree of freedom | Electronic analog | Optical extension |
|---|---|---|
| On/off | High/Low | LED on/off |
| — | (not available) | Color / wavelength |
| — | (not available) | Brightness / intensity |
| — | (not available) | Spatial position in array |
| — | (not available) | Pulse timing / temporal pattern |
| — | (not available) | Polarization (with additional optics) |

This connects SCD to Optical Bead Computing: SCD uses structured electronic bead patterns across five binary lines. OBQC generalizes bead patterns into optical degrees of freedom — wavelength, polarization, phase, time-bin, spatial mode. The LED-CMOS layer is a physical intermediate between electronic SCD and full optical bead computing.

---

## Pattern Recognition Rather Than Sequential Calculation

The deeper conceptual shift in SCD and OBQC is from symbolic binary manipulation to structured pattern recognition.

**Traditional digital computation:**

```
number -> binary representation -> sequential logic operations -> result
```

**Soroban-inspired pattern computation:**

```
number -> bead pattern -> pattern recognition -> pattern transformation -> result
```

This does not replace all computation. It may be useful where:

- Decimal structure matters naturally (financial, counting, display applications)
- Fast structural validation is more important than compact storage
- Visual or optical input is the natural interface (camera-based readout, LED arrays)
- Pattern classification is central to the workload
- Sensor, LED, and CMOS systems are already present in the hardware

Flash mental arithmetic (flash anzan) suggests that pattern-based decimal processing has cognitive precedent: skilled practitioners operate on a spatial soroban pattern image, not on digit symbols. The LED-CMOS SCD architecture is an engineering analog of this cognitive model.

---

## Prototype Architecture

### Electronic SCD prototype

```
SCD encoder
  -> CMOS validity checker (thermometer constraint)
  -> digit decoder
  -> carry/borrow logic
  -> multi-digit arithmetic unit
```

### Electro-optical prototype

```
SCD encoder
  -> LED matrix driver
  -> LED array (5 LEDs per digit, optional RGB)
  -> optical medium (air or sealed cell)
  -> CMOS camera / image sensor
  -> pattern classifier (nearest-neighbor or threshold)
  -> decoded SCD state
```

### Optical bead prototype

```
RGB LED / microLED array
  -> optical medium (air, liquid cell, waveguide)
  -> CMOS sensor array
  -> nearest-neighbor classifier over (wavelength, brightness, position)
  -> OBQC state
```

---

## Falsifiable Experiments

The following experiments can be performed to evaluate this framework:

1. **BCD vs SCD error detection comparison:** Apply random independent bit flips to BCD and SCD encodings. Measure invalid-state detection rate and silent-error rate. Verify that SCD detects more errors due to its larger invalid-state fraction.

2. **Silent error characterization:** Map all single-bit and double-bit flip outcomes for each SCD digit. Identify which flips are silent (valid-to-valid transitions).

3. **LED-CMOS digit reader:** Build a physical 5-LED display for one SCD digit. Read back with a CMOS camera. Classify each of the 10 valid patterns correctly under normal lighting.

4. **Classification under noise:** Add brightness variation, blur, ambient light, and camera noise. Measure classification accuracy as a function of noise level.

5. **RGB color expansion:** Replace binary LED on/off with RGB color coding. Test whether the classifier can distinguish more than 2 states per LED position using color information.

6. **Pattern recognition operation count:** Compare operation count for pattern-based SCD classification versus sequential BCD bit-checking under specified workloads.

7. **Sensor noise model validation:** Compare the toy LED-CMOS simulator results with a physical LED-camera measurement.

---

## Limitations

- **SCD uses 5 bits per digit**, which is 25% more than BCD. This increases representation size for all multi-digit numbers.
- **Validity checking is not full correction.** Silent errors remain for H-bit flips and some thermometer-preserving lower-bit changes. Full error correction requires an additional ECC layer.
- **LED/CMOS systems introduce real noise:** brightness variation, blur at focus edges, ambient light contamination, color channel crosstalk, sensor quantization, and lens distortion. These degrade classifier accuracy.
- **Calibration drift:** LEDs change brightness over temperature and age. CMOS sensors have dark current drift and pixel non-uniformity. Regular recalibration is required.
- **Optical prototypes are slower than dedicated CMOS logic** unless specialized hardware (microLED arrays, FPGA-coupled sensors, custom ASICs) is used.
- **No general-purpose computing replacement is claimed.** SCD-CMOS and LED-CMOS are pattern-oriented decimal tools, not universal arithmetic engines.
- **This is a framework for exploration**, not a demonstrated system. All results in the associated simulator are toy models under explicitly stated assumptions.

---

## Summary

SCD-CMOS and LED-CMOS architecture bridges soroban bead logic, electronic on/off states, and optical pattern recognition.

Its value is not compact storage — SCD uses more bits than BCD. Its value is:

1. **Structural representation:** the digit pattern directly mirrors a soroban rod configuration
2. **Validity checking:** 22 out of 32 invalid states are detectable without additional parity
3. **Optical bridge:** the same on/off structure can be extended to LED position, color, and intensity
4. **Path to OBQC:** LED-CMOS prototyping provides a physically realizable bridge from electronic SCD to full Optical Bead Computing with multi-degree optical state encoding

SCD-CMOS is a structured decimal pattern layer. LED-CMOS is its optical interface. OBQC is its generalization to multi-dimensional optical bead states.

---

*See also:*
- [docs/electronic-extension-soroban-decimal.md](electronic-extension-soroban-decimal.md) — original SCD definition
- [simulator/led_cmos_scd_pattern_demo.py](../simulator/led_cmos_scd_pattern_demo.py) — toy LED-CMOS readout simulator
- [diagrams/scd-cmos-led-architecture.md](../diagrams/scd-cmos-led-architecture.md) — architecture diagrams
- [README.md](../README.md) — repository overview

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

