# simulator/results/

[English Version](README.md)

このディレクトリには、比較シミュレーターが生成したCSV出力ファイルが含まれています。

---

## 生成されるファイル

| ファイル | 生成元 | 内容 |
|---|---|---|
| `electronic_binary_vs_scd.csv` | `electronic_binary_vs_scd.py` | ビット反転ノイズのもとでの、BCD対SCDの指標 |
| `photonic_binary_vs_obqc.csv` | `photonic_binary_vs_obqc.py` | ガウスノイズのもとでの、二進対光学ビードの指標 |
| `qudit_inspired_channel.csv` | `qudit_inspired_channel.py` | 簡易クディットチャネルのスループットの指標 |
| `optical_medium_comparison.csv` | `optical_medium_comparison.py` | MとDの構成にわたる、媒質の種類ごとのSER |
| `hybrid_quantum_support_energy.csv` | `hybrid_quantum_support_energy.py` | 簡易エネルギーモデル：OBQCの補助層対基準（E_cryoは不変） |
| `pattern_vs_binary_operation_cost.csv` | `pattern_vs_binary_operation_cost.py` | 抽象的なコストモデル：パターンのパイプライン対二進のパイプライン |

---

## 生成方法

```bash
# Run all simulators at once
python run_comparisons.py

# Or run each individually
python electronic_binary_vs_scd.py
python photonic_binary_vs_obqc.py
python qudit_inspired_channel.py
```

---

## 注記

- CSVファイルは決定論的です。同じスクリプトを同じシードで実行すれば、常に同じ出力が得られます。
- 既定の乱数シード：42。`--seed N`で上書きできます。
- 試行回数が多いと、CSVファイルが大きくなることがあります。大きな生成ファイルをコミットしないでください。
- 再現性のため、小さな実演の結果（既定の設定）はコミットしてかまいません。
- すべてのCSVファイルは、標準的なカンマ区切りのUTF-8エンコーディングです。

---

## 免責事項

これらのCSVファイルは、簡略化したシミュレーションモデルの結果を含みます。
物理的なハードウェアからの実験的な測定ではありません。
いかなる計算上の優位性の証明でもありません。
明示的に述べたモデルの仮定からの、再現可能で反証可能な出力です。

完全な説明は、[docs/comparative-simulation-framework_ja.md](../../docs/comparative-simulation-framework_ja.md)を参照してください。

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

