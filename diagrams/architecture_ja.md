# 図：光学ビードコンピューティングのシステム・アーキテクチャ

[English Version](architecture.md)

**所属：**[光学ビードコンピューティング](../README_ja.md)

この文書は、光学ビードコンピューティングのフレームワークについて、異なる抽象度でのシステム・アーキテクチャ図を収めています。（図中のラベルは英語のままです。）

---

## 1. 最上位のシステム・アーキテクチャ

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

## 2. エンコーダの詳細

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

## 3. デコーダの詳細

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

## 4. 第1段階のハードウェア・アーキテクチャ（古典的なプロトタイプ）

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

## 5. ソフトウェア・シミュレーションのアーキテクチャ（第0段階）

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

## 6. 三層アーキテクチャの概観

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

*[README_ja.md](../README_ja.md)に戻る*

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


## ライセンス

CC BY 4.0

この記事は、クリエイティブ・コモンズ 表示 4.0 国際ライセンス（CC BY 4.0）の下で公開されています。  
適切なクレジット表示を行う限り、共有、再配布、翻訳、改変、再利用が認められます。

