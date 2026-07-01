# SCD-CMOS and LED-CMOS Architecture Diagrams

**Repository:** `Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm`
**Status:** Conceptual / early-stage framework
**License:** CC BY 4.0

See also: [docs/scd-cmos-led-pattern-architecture.md](../docs/scd-cmos-led-pattern-architecture.md)

---

## A. Soroban Bead State to CMOS Signal Lines

```mermaid
flowchart LR
    subgraph Soroban["Soroban Rod"]
        UB["Upper bead H\n(value 5)"]
        LB4["Lower bead L4\n(value 1)"]
        LB3["Lower bead L3\n(value 1)"]
        LB2["Lower bead L2\n(value 1)"]
        LB1["Lower bead L1\n(value 1)"]
    end

    subgraph CMOS["CMOS Signal Lines"]
        SH["Signal H\n(High / Low)"]
        SL4["Signal L4\n(High / Low)"]
        SL3["Signal L3\n(High / Low)"]
        SL2["Signal L2\n(High / Low)"]
        SL1["Signal L1\n(High / Low)"]
    end

    subgraph SCD["SCD Cell"]
        VAL["Validity Checker\n(thermometer constraint)"]
        DEC["Digit Decoder\n5-bit -> digit 0-9"]
        CBL["Carry / Borrow Logic"]
    end

    UB -- "engaged=High\ndisengaged=Low" --> SH
    LB4 --> SL4
    LB3 --> SL3
    LB2 --> SL2
    LB1 --> SL1

    SH --> VAL
    SL4 --> VAL
    SL3 --> VAL
    SL2 --> VAL
    SL1 --> VAL

    VAL -- "valid pattern" --> DEC
    VAL -- "invalid pattern\n(detected error)" --> ERR["Error Flag"]
    DEC --> CBL
    CBL --> OUT["Decimal Output\n/ Next Cell"]
```

---

## B. CMOS SCD State to LED Optical Pattern and Back

```mermaid
flowchart LR
    subgraph Electronic["Electronic SCD"]
        ENC["SCD Encoder\n(5-bit decimal cell)"]
    end

    subgraph LEDArray["LED / RGB LED Array"]
        LEDH["LED-H\n(upper bead)"]
        LEDL4["LED-L4"]
        LEDL3["LED-L3"]
        LEDL2["LED-L2"]
        LEDL1["LED-L1\n(lowest bead)"]
        COLOR["Color / Brightness\n/ Spatial Position\n(optional extension)"]
    end

    subgraph Medium["Optical Medium"]
        AIR["Open air /\nSealed cell /\nWaveguide"]
    end

    subgraph Sensor["CMOS Image Sensor"]
        PIX["Pixel Array\n(spatial light readout)"]
        THRESH["Threshold /\nClassifier"]
    end

    subgraph Decode["Decoded Output"]
        DSCD["SCD State\nor OBQC State"]
    end

    ENC -- "H, L4, L3, L2, L1\nsignal lines" --> LEDH
    ENC --> LEDL4
    ENC --> LEDL3
    ENC --> LEDL2
    ENC --> LEDL1
    LEDH -- "position\ncolor\nbrightness" --> COLOR
    COLOR --> AIR

    AIR -- "optical pattern\n(may include noise,\nblur, ambient light)" --> PIX
    PIX -- "pixel intensities\ncolor channels" --> THRESH
    THRESH -- "nearest-neighbor\nor CNN classifier" --> DSCD
```

---

## C. Conceptual Stack: Soroban to Qudit Extension

```mermaid
flowchart TD
    SOR["Soroban Abacus\nPhysical bead configuration\n(spatial pattern)"]
    SCD["SCD-CMOS\n5-bit electronic decimal cell\nH + L1-L4 thermometer\n(on/off signal pattern)"]
    LED["LED-CMOS\nLED position + color + brightness\nCMOS sensor readout\n(optical on/off + color pattern)"]
    OBC["Optical Bead Computing\nMulti-degree optical bead state\nwavelength, polarization, phase,\ntime-bin, spatial mode\n(multi-dimensional optical pattern)"]
    QDT["Qudit-Inspired Extension\nHigh-dimensional optical state\nclosely related to qudit encoding\n(long-term research direction)"]

    SOR -- "bead engaged/disengaged\n= High/Low" --> SCD
    SCD -- "High/Low lines\n= LED on/off\n+ color/brightness extension" --> LED
    LED -- "LED/sensor pattern\n-> multi-DOF optical state" --> OBC
    OBC -- "classical multi-valued\n-> quantum-inspired extension" --> QDT

    style SOR fill:#e8f4f8,stroke:#2980b9
    style SCD fill:#e8f8e8,stroke:#27ae60
    style LED fill:#f8f4e8,stroke:#e67e22
    style OBC fill:#f8e8f8,stroke:#8e44ad
    style QDT fill:#f8e8e8,stroke:#c0392b
```

---

## D. SCD Error Classification

```mermaid
flowchart TD
    INPUT["5-bit pattern received"]
    THERM{"Thermometer\nconstraint\nvalid?"}
    VALID["Valid SCD pattern\n(10 out of 32)"]
    DETECTED["Detected error\n(22 out of 32)\ninvalid thermometer structure"]

    VALID --> HFLIP{"H-bit flipped\nor lower bits\nthermometer-preserving\nchange?"}
    SILENT["Silent error\nvalid digit -> different valid digit\n(e.g., 0->5, 1->6, 1->2)"]
    CORRECT["Correct decoding"]

    INPUT --> THERM
    THERM -- "no" --> DETECTED
    THERM -- "yes" --> VALID
    VALID --> HFLIP
    HFLIP -- "yes (error present\nbut undetectable)" --> SILENT
    HFLIP -- "no error" --> CORRECT
```

---

## E. LED-CMOS Brightness Noise Model (Toy)

```mermaid
flowchart LR
    SCD2["SCD digit\n(0-9)"]
    MAP["Map to LED\nbrightness pattern\n(5 brightness values)"]
    NOISE["Add brightness noise\n(Gaussian sigma)"]
    THRESH2["CMOS threshold\nreadout\n(High if > threshold)"]
    DEC2["Decode\nSCD pattern"]
    CHK["Check:\ncorrect /\ndetected error /\nsilent error"]

    SCD2 --> MAP --> NOISE --> THRESH2 --> DEC2 --> CHK
```

---

*See also:*
- [docs/scd-cmos-led-pattern-architecture.md](../docs/scd-cmos-led-pattern-architecture.md) — full documentation
- [docs/scd-cmos-led-pattern-architecture_ja.md](../docs/scd-cmos-led-pattern-architecture_ja.md) — Japanese version
- [simulator/led_cmos_scd_pattern_demo.py](../simulator/led_cmos_scd_pattern_demo.py) — toy LED-CMOS simulator
- [diagrams/soroban-to-optical-beads.md](soroban-to-optical-beads.md) — soroban-to-OBQC conceptual diagram

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

