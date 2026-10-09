# 光学ビードコンピューティング — シミュレーター

[English Version](README.md)

このディレクトリには、光学ビードコンピューティング（OBC）フレームワークのための、最小限のPythonシミュレーターが含まれています。

**必須の外部依存関係はありません。**中核のスクリプトは、Python 3.7以上の標準ライブラリのみで動作します。`numpy`と`matplotlib`は、利用できる場合に出力を強化するために使われますが、必須ではありません。

---

## ファイル

| ファイル | 説明 |
|---|---|
| `encode_decode.py` | アルファベットの定義、符号化、最近傍復号、SERの測定 |
| `noise_model.py` | ガウスノイズ、時間ジッタ、チャネルのドリフト、スペクトルのクロストーク |
| `confusion_matrix.py` | 複数試行の評価、混同行列の出力、任意のヒートマップのプロット |
| `soroban_decimal.py` | そろばん符号化十進（SCD）の5ビットセル：符号化、復号、インクリメント、加算、表示 |
| `liquid_medium_noise.py` | 密閉した液体の光学セルのノイズモデル（吸収、散乱、熱による位相ドリフト） |
| `electronic_binary_vs_scd.py` | **比較：**ランダムなビット反転のもとでの、BCD対SCD |
| `photonic_binary_vs_obqc.py` | **比較：**ガウスノイズのもとでの、二進のフォトニック対多状態の光学ビード |
| `qudit_inspired_channel.py` | **簡易モデル：**M準位のクディット着想のチャネル（解析的。量子シミュレーションではない） |
| `hybrid_quantum_support_energy.py` | **簡易エネルギーモデル：**OBQCの補助層対、基準となるハイブリッド量子支援システム（E_cryoは不変） |
| `pattern_vs_binary_operation_cost.py` | **抽象的なコストモデル：**逐次的な二進パイプライン対パターン認識パイプライン |
| `led_cmos_scd_pattern_demo.py` | **簡易モデル：**LED-CMOSによるSCDパターンの読み出し（輝度ノイズ、しきい値、誤りの分類） |
| `run_comparisons.py` | すべての比較シミュレーターを順に実行 |
| `results/` | 生成されたCSV出力ファイルのためのディレクトリ |

---

## クイックスタート

```bash
# Run the basic encode/decode demo
python encode_decode.py

# Run the noise model demo
python noise_model.py

# Run the confusion matrix evaluator (default settings)
python confusion_matrix.py

# Run the Soroban-Coded Decimal (SCD) electronic extension demo
python soroban_decimal.py

# --- Comparison simulators ---
# Run all comparison simulators at once
python run_comparisons.py

# Or run each comparison simulator individually
python electronic_binary_vs_scd.py
python photonic_binary_vs_obqc.py
python qudit_inspired_channel.py

# Run with custom sigma and trial count
python confusion_matrix.py --sigma 0.07 --trials 300

# Limit to 12 states
python confusion_matrix.py --sigma 0.05 --states 12

# Run SER sweep over a range of noise levels
python confusion_matrix.py --sweep

# Show heatmap plot (requires matplotlib)
python confusion_matrix.py --plot

# Save heatmap plot to file
python confusion_matrix.py --save confusion.png
```

---

## アルファベットの構造

既定のアルファベットは、三つの自由度から構築されます。

- **波長：**4つの正規化した水準 → [0.00, 0.33, 0.67, 1.00]
- **偏光：**4つの正規化した水準 → [0.00, 0.33, 0.67, 1.00]
- **時間ビン：**3つの正規化した水準 → [0.00, 0.50, 1.00]

アルファベットの総数：4 × 4 × 3 = **48状態**

すべての値は[0, 1]に正規化されています。物理的な解釈：
- 波長の0.00 / 0.33 / 0.67 / 1.00は、たとえば450 nm / 532 nm / 633 nm / 780 nmに対応
- 偏光の0.00 / 0.33 / 0.67 / 1.00は、H / D / V / Aの直線偏光状態に対応
- 時間ビンの0.00 / 0.50 / 1.00は、早い／中間／遅いビンに対応

---

## ノイズモデル

### ガウスノイズ（`noise_model.py`）

各次元に独立に加えられる、加法的なガウスノイズ。検出器のノイズ、光源の強度の揺らぎ、環境の摂動をモデル化します。

```
sigma = 0.01   → very low noise; nearly all states distinguishable
sigma = 0.05   → moderate noise; typical laboratory conditions
sigma = 0.10   → high noise; practical decoding begins to fail for many states
sigma = 0.20   → severe noise; most states confused with neighbors
```

### 時間ジッタ

ガウス分布するジッタの値による、時間ビンの座標の変位。パルスの到着の不確かさをモデル化します。

### チャネルのドリフト

較正からの経過時間に比例した、すべての座標のゆっくりした決定論的なずれ。熱膨張とレーザー波長のドリフトをモデル化します。

### スペクトルのクロストーク

有界の範囲内での、波長座標のランダムなずれ。有限のフィルター帯域による、隣接チャネルの漏れをモデル化します。

### 組み合わせた現実的なモデル

`noise_model.py`の`realistic_noise()`は、すべての種類のノイズを順に適用します。最も現実的なSERの推定には、これを用いてください。

---

## 期待される結果

48状態のアルファベットを用いた既定のガウスノイズモデルのもとで：

| σ | 期待されるSER（概算） |
|---|---|
| 0.01 | < 0.001 |
| 0.02 | ~ 0.005 |
| 0.05 | ~ 0.05–0.15 |
| 0.10 | ~ 0.30–0.50 |
| 0.18 | ~ 0.60–0.80 |

実際の値は乱数シードに左右されます。より安定した推定には、`--trials 500`で実行してください。

---

## 任意の依存関係

```bash
# For heatmap visualization
pip install matplotlib

# For faster matrix operations
pip install numpy
```

どちらのパッケージも任意です。これらがなくても、シミュレーターは正しく動作します。

---

## シミュレーターの拡張

より小さい、あるいはより大きいアルファベットを試験するには：

```python
from encode_decode import build_alphabet

# 2 wavelengths × 2 polarizations × 2 time-bins = 8 states
small_alphabet = build_alphabet(
    wavelengths=[0.0, 1.0],
    polarizations=[0.0, 1.0],
    timebins=[0.0, 1.0]
)

# 4 wavelengths × 6 polarizations × 4 time-bins = 96 states
large_alphabet = build_alphabet(
    wavelengths=[0.0, 0.33, 0.67, 1.0],
    polarizations=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    timebins=[0.0, 0.33, 0.67, 1.0]
)
```

混同行列で現実的なノイズモデルを使うには：

```python
from encode_decode import decode
from noise_model import realistic_noise

# Replace add_noise(state, sigma) with realistic_noise(state, ...)
```

---

## 光学媒質の比較

```bash
python optical_medium_comparison.py
python optical_medium_comparison.py --trials 5000
python optical_medium_comparison.py --plot
python optical_medium_comparison.py --save-plot medium_comparison.png
```

六つの光学媒質について、簡略化した環境ノイズと材料ノイズのモデルを比較します。
`open_air`、`sealed_air`、`sealed_liquid`、`acrylic_block`、`glass_quartz`、`fiber_waveguide`。

各媒質は、構成要素ごとのノイズのσ（粉塵、湿度、熱による屈折率のドリフト、
気泡による散乱、応力複屈折、アライメントのドリフト）で特徴づけられます。合成した実効のσを使って、
D次元の状態空間におけるM状態のアルファベットの、記号誤り率をシミュレートします。

示すこと：
- `open_air`は、実効ノイズが最も高く（sigma = 0.095）、SERも最も高い
- `glass_quartz`と`fiber_waveguide`は、ノイズが最も低く、どのMでも最良のSERになる
- `acrylic_block`は、大きな応力複屈折を持つ（偏光の自由度を劣化させる）
- `sealed_liquid`は、位相符号化にとって重大な、熱による屈折率のドリフトを持つ
- 次元Dが高いほど、状態がより多くの次元に広がり、より高いMでもマージンが保たれる

出力：コンソールの表（D=2、4、7）＋`results/optical_medium_comparison.csv`

**簡易モデルに関する警告：**ノイズのパラメータは、定性的な工学的推定であり、
測定値ではありません。実験設計の指針として使い、ハードウェアの仕様としては使わないでください。

[docs/optical-medium-stabilization_ja.md](../docs/optical-medium-stabilization_ja.md)を参照。

---

## 密閉した液体の光学ビード媒質

```bash
python liquid_medium_noise.py
python liquid_medium_noise.py --path-length 1.0 --delta-T 0.1
```

光学ビードの伝送媒質として使う、密閉した透明な液体の光学セルに固有のノイズ源を
モデル化します。`noise_model.py`を、次で拡張します。

- **吸収による減衰**（ランベルト・ベール：I = I0 * exp(-alpha * L)）
- 気泡と不純物による**散乱ノイズ**（乗法的な対数正規）
- 温度に依存した屈折率の変化による**熱的な位相ドリフト**
- **波長に依存した透過の差**（波長に依存したalpha）
- **熱勾配によるビームのステアリング**（任意の空間モードの変位）

次のプリセットを含みます：`water_clean`、`water_uncontrolled`、`glycerol_water`、
`immersion_oil`、`open_air_baseline`（比較用）。

**シミュレーションからの重要な知見：**  
経路長5 cmでは、0.1 Kの温度偏差が約5 radの位相ドリフトを引き起こします。
サブミリケルビンの温度制御、あるいはサブミリメートルの経路長がなければ、
液体セルでの位相符号化は実用的ではありません。液体媒質の試作機の出発点となる自由度としては、
波長と偏光が推奨されます。

[docs/sealed-liquid-optical-bead-medium_ja.md](../docs/sealed-liquid-optical-bead-medium_ja.md)を参照。

---

## 電子的な二進対SCD

```bash
python electronic_binary_vs_scd.py
python electronic_binary_vs_scd.py --trials 5000
```

ランダムで独立なビット反転のノイズモデルのもとで、二進化十進（BCD、4ビット）と
そろばん符号化十進（SCD、5ビット）を比較します。

測定するもの：
- **correct_rate** — 正しい数字に復号された試行の割合
- **detected_error_rate** — 復号されたパターンが構造上無効だった（捕捉された）試行の割合
- **silent_error_rate** — 別の有効な数字に復号された（検出されない）試行の割合

主なトレードオフ：
- BCDは1桁あたり4ビット、SCDは1桁あたり5ビットを使う（記憶のオーバーヘッドは+25%）
- BCDは6/16 = 37.5%が無効状態、SCDは22/32 = 68.75%が無効状態
- したがってSCDは、より多くのランダムなビット反転の誤りを、*検出された*誤りに変える
- どちらの方式も、追加の冗長性なしには、誤りの*訂正*を提供しない

出力：コンソールの表＋`results/electronic_binary_vs_scd.csv`

**このシミュレーションは、SCDがあらゆる場合にBCDを上回るとは主張しません。**
完全な説明は、`docs/comparative-simulation-framework_ja.md`を参照してください。

---

## フォトニックな二進対OBQC

```bash
python photonic_binary_vs_obqc.py
python photonic_binary_vs_obqc.py --trials 1000
python photonic_binary_vs_obqc.py --plot          # requires matplotlib
python photonic_binary_vs_obqc.py --save-plot throughput.png
```

正規化したD次元の状態空間における、簡略化したガウスノイズモデルのもとで、二進のフォトニック符号化（M=2、1ビット／記号）と、
多状態の光学ビード符号化（M=4〜128、最大7ビット／記号）を比較します。

測定するもの：
- **symbol_error_rate (SER)** — 誤って復号された記号の割合
- **bits_per_symbol** — log2(M)
- **throughput_proxy** — bits_per_symbol * (1 - SER)
- **separability_margin** — アルファベット内の任意の二つの状態の間の最小距離

主な結果（このモデルに固有）：
- 二進のM=2は、試験したすべてのノイズ水準で、ほぼゼロのSERを保つ
- Mが高い構成は、記号あたりのビット数が多いが、ノイズに対してSERがより速く上昇する
- 同じMでより多くの次元（高いD）を使うと、分離マージンが保たれる

出力：コンソールの表＋`results/photonic_binary_vs_obqc.csv`

**警告：これは完全な量子あるいは物理光学のシミュレーションではありません。**
簡略化した幾何学的なモデルです。結果は、述べたモデルの仮定にのみ左右されます。

---

## クディット着想の簡易チャネル

```bash
python qudit_inspired_channel.py
python qudit_inspired_channel.py --monte-carlo --trials 50000
```

損失確率と混同確率でパラメータ化した、M=2の二進的な記号の伝送と、
M>2のクディット的な記号の伝送との、簡易な解析的比較。

測定するもの：
- **correct_rate** = (1 - p_loss) * (1 - p_confuse)
- **erasure_rate** = p_loss
- **symbol_error_rate** = (1 - p_loss) * p_confuse
- **throughput_proxy** = correct_rate * log2(M)

主な結果：
- 理想的なチャネルでは、Mが高いほど、スループットの代理指標は常に増える
- p_confuseまたはp_lossが増えるにつれて、Mが高いことの優位性を保つには、
  それに応じてより良い測定の信頼性が必要になる

出力：コンソールの表＋`results/qudit_inspired_channel.csv`

**簡易モデルに関する警告：これは量子コンピューティングのシミュレーションではありません。**
**量子優位性の証明でもありません。**
これは、教育的な例示のみを目的とした、簡略化したパラメトリックなモデルです。
現実のクディット系は、ここでとらえていないデコヒーレンス、モード結合、
測定の不完全さに直面します。

---

## ハイブリッド量子支援のエネルギーモデル

```bash
python hybrid_quantum_support_energy.py
```

この簡易モデルは、OBQC的な補助層が、ハイブリッド量子アーキテクチャの支援システムのエネルギーを、
五つのシナリオ（conservative、moderate、optimistic、high_OBQC_overhead、no_benefit）にわたって減らせるかを推定します。

**重要：**このモデルは、既定でE_cryo（極低温冷却のエネルギー）を変えません。
OBQCが極低温冷却の要件をなくすとは主張しません。
補助層が何をしようと、超伝導量子ビットはミリケルビンの温度を必要とします。

モデルは、次が成り立つかどうかを評価します。

```
E_OBQC_layer < sum_i (1 - alpha_i) * E_i_baseline
```

これが成り立つなら、OBQC層は補助エネルギーを正味で削減します。
成り立たない場合（high_OBQC_overhead、no_benefit）は、その層は節約する以上のコストがかかります。

出力：コンソールの表＋`results/hybrid_quantum_support_energy.csv`

完全な文脈、アーキテクチャの議論、反証可能な研究上の問いについては、
[docs/hybrid-quantum-support-layer_ja.md](../docs/hybrid-quantum-support-layer_ja.md)を参照してください。

---

## パターン認識対二進の演算コスト

```bash
python pattern_vs_binary_operation_cost.py
```

この抽象的なコストモデルは、簡略化し、明示的に述べた仮定のもとで、
逐次的な二進方式の分類パイプラインと、パターン認識パイプラインを比較します。

掃引するパラメータ：
- workload_size：1,000 / 10,000 / 100,000 / 1,000,000
- pattern_reduction_factor：0.2 / 0.4 / 0.6 / 0.8（なお必要な二進演算の割合）
- overhead_case：low / medium / high（光学的な抽出と検出器のコスト）

パターン認識が、より低い総コストを達成する（break_even = yes）のは、次の場合に限られます。

```
overhead < (1 - reduction_factor) * binary_savings
```

オーバーヘッドが低い場合、損益分岐点は、控えめな削減係数でも到達可能です。
オーバーヘッドが高い場合は、大きな削減係数と大きなワークロードが必要です。

出力：コンソールの表＋`results/pattern_vs_binary_operation_cost.csv`

**これは抽象的なコストモデルであり、ハードウェアのベンチマークではありません。**
結果は、仮定したコストパラメータに全面的に左右されます。

---

## LED-CMOS SCDパターンのデモ

```bash
python led_cmos_scd_pattern_demo.py
python led_cmos_scd_pattern_demo.py --trials 5000
python led_cmos_scd_pattern_demo.py --sigma 0.15
python led_cmos_scd_pattern_demo.py --sigma 0.30 --trials 2000
```

この簡易デモは、SCD（そろばん符号化十進）の数字を、簡略化したLEDの輝度パターンに対応づけ、
CMOS的なしきい値モデルで読み戻し、数字0〜9のすべてについて、正しい率、検出された誤りの率、
沈黙の誤りの率を測定します。

示すこと：
- **SCD符号化：**各十進の数字は、5ビットの温度計パターン（H + L1–L4）
- **LEDの輝度の対応：**信号線ごとに、High=輝度1.0、Low=輝度0.0
- **ガウスノイズの注入：**LEDの強度のばらつきとCMOSセンサーのノイズをモデル化
- **しきい値による読み出し：**CMOS的なしきい値が、連続的な輝度をHigh/Lowに変換
- **誤りの分類：**
  - `correct`：復号されたパターンが、元の数字と一致する
  - `detected_error`：復号されたパターンが、温度計の制約に違反する（構造上無効）
  - `silent_error`：復号されたパターンは有効だが、別の数字に対応する（例：Hビットの反転による0→5）
- **σの掃引：**ノイズ水準に応じて誤り率がどう変わるかを示す

出力：コンソールの表＋`results/led_cmos_scd_pattern_demo.csv`

**簡易モデルに関する警告：**ノイズのパラメータは、ガウス型の輝度の摂動であり、
測定された物理光学の値ではありません。結果は、述べたσとしきい値にのみ左右されます。
これは、[docs/scd-cmos-led-pattern-architecture_ja.md](../docs/scd-cmos-led-pattern-architecture_ja.md)に記述した
SCD-CMOS／LED-CMOSアーキテクチャの、概念的な実演です。

---

## すべての比較の実行

```bash
python run_comparisons.py
python run_comparisons.py --trials 2000   # override trial count for stochastic simulators
```

すべての比較シミュレーターを順に実行し、生成された各CSVファイルの場所を報告します。
すべての出力は`results/`に保存されます。

ハイブリッドのエネルギーモデルと演算コストのモデルは決定論的であり、
`--trials`パラメータを使いません。

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

