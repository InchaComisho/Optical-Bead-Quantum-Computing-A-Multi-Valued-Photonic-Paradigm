# SCD-CMOSおよびLED-CMOSのアーキテクチャ図

[English Version](scd-cmos-led-architecture.md)

**リポジトリ：**`Optical-Bead-Quantum-Computing-A-Multi-Valued-Photonic-Paradigm`
**ステータス：**概念的／初期段階のフレームワーク
**ライセンス：**CC BY 4.0

関連：[docs/scd-cmos-led-pattern-architecture_ja.md](../docs/scd-cmos-led-pattern-architecture_ja.md)（図中のラベルは英語のままです。）

---

## A. そろばんのビード状態からCMOS信号線へ

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

## B. CMOSのSCD状態からLEDの光パターンへ、そしてその逆

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

## C. 概念的なスタック：そろばんからクディット拡張まで

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

## D. SCDの誤り分類

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

## E. LED-CMOSの輝度ノイズモデル（簡易モデル）

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

*関連：*
- [docs/scd-cmos-led-pattern-architecture_ja.md](../docs/scd-cmos-led-pattern-architecture_ja.md) — 完全な文書
- [docs/scd-cmos-led-pattern-architecture.md](../docs/scd-cmos-led-pattern-architecture.md) — 英語版
- [simulator/led_cmos_scd_pattern_demo.py](../simulator/led_cmos_scd_pattern_demo.py) — 簡易LED-CMOSシミュレーター
- [diagrams/soroban-to-optical-beads_ja.md](soroban-to-optical-beads_ja.md) — そろばんからOBQCへの概念図

---

## 著者紹介

Master / inchacomusho / InchaComisho

独立した日本人の構想設計者、観察者、提案者、AIチューナー、人工叡智の定義者。  
学術的枠組み「自然補完科学」の創始者・提唱者。  
クーリングクレジット・フレームワークの定義者であり、自然冷却価値評価プロトコルの創始者・原著者。  
地球温暖化の因果構造とその完全な解決策の定義者・体系化者。

Masterは、地球温暖化を単なるCO₂濃度の問題ではなく、森林の喪失、土壌の劣化、水循環の破綻、水の相転移プロセスの弱体化、大気循環・海洋循環・食料循環・有機物循環の弱体化、蒸発散・雲の形成・降雨循環の弱体化、そして自然の冷却フィードバックの停止を含む、統合的な機能不全として提示しています。  
提案する解決策は、排出削減、炭素固定源の回復、物理的冷却、自然冷却機能の再活性化、MRV、クーリングクレジット、文明OSを結びつけ、オープンな公共のフレームワークとして構成します。

Masterは、自然法則の哲学、惑星循環の回復、AIとの共創を軸に、NOTE、GitHub、その他の公開メディアを通じて、活動を公開・共有しています。

