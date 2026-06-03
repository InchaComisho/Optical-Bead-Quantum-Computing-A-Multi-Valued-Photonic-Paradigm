"""
qudit_inspired_channel.py - Toy qudit-inspired channel comparison
==================================================================
A toy comparison between binary-like (M=2) and qudit-like (M>2) symbol
transmission channels, using a simple analytical/statistical channel model.

TOY MODEL DISCLAIMER:
  This is a toy model for educational illustration ONLY.
  It is NOT:
    - A simulation of quantum mechanics or quantum computing
    - A proof of quantum advantage for any encoding scheme
    - A model of real quantum optical hardware
    - A calculation of quantum channel capacity (Holevo bound, etc.)
    - A claim that qudit encoding outperforms qubit encoding in practice

  What it IS:
    - A simplified parametric model showing how alphabet size M interacts
      with loss probability and measurement confusion probability
    - A transparent, falsifiable tool for visualizing throughput trade-offs
      at different M values
    - An educational bridge to qudit concepts for readers familiar with
      classical information theory

  The "qudit-like" label means only that the model uses M-level symbols
  analogous to qudits (d-level quantum systems). No quantum mechanics is
  simulated or implied.

Channel model:
  For each transmitted symbol:
    1. With probability p_loss: symbol is lost (erasure, detected)
    2. Otherwise: with probability p_confuse, symbol is mapped to a
       uniformly random wrong symbol; with probability 1-p_confuse,
       symbol is received correctly

Metrics (analytical):
  correct_rate              = (1 - p_loss) * (1 - p_confuse)
  erasure_rate              = p_loss
  symbol_error_rate         = (1 - p_loss) * p_confuse
  bits_per_symbol           = log2(M)
  throughput_proxy          = correct_rate * bits_per_symbol
    (approximate useful bits per symbol slot; ignores coding overhead)

All results are exact analytically. The Monte Carlo mode is included
for verification and to demonstrate statistical agreement.

No external dependencies required.
ASCII-only output.

Usage:
    python qudit_inspired_channel.py
    python qudit_inspired_channel.py --monte-carlo --trials 50000
"""

import random
import math
import os
import csv
import argparse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42
M_VALUES = [2, 4, 8, 16, 32, 64, 128]
P_LOSS_VALUES = [0.0, 0.01, 0.05, 0.10]
P_CONFUSE_VALUES = [0.0, 0.01, 0.05, 0.10, 0.20]

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
DEFAULT_CSV = os.path.join(RESULTS_DIR, "qudit_inspired_channel.csv")

# ---------------------------------------------------------------------------
# Analytical channel model
# ---------------------------------------------------------------------------

def analytical_metrics(M, p_loss, p_confuse):
    """
    Compute channel metrics analytically.

    The confusion probability p_confuse is the probability that a
    non-lost symbol is decoded as any specific wrong symbol.
    Total symbol error probability given no loss = p_confuse (mapped to
    any of the M-1 wrong symbols with equal probability p_confuse/(M-1),
    so total error = p_confuse).

    Returns dict of metrics.
    """
    bits_per_symbol = math.log2(M) if M >= 2 else 0.0
    correct_rate = (1.0 - p_loss) * (1.0 - p_confuse)
    erasure_rate = p_loss
    symbol_error_rate = (1.0 - p_loss) * p_confuse
    throughput_proxy = correct_rate * bits_per_symbol

    return {
        "M": M,
        "bits_per_symbol": round(bits_per_symbol, 4),
        "p_loss": p_loss,
        "p_confuse": p_confuse,
        "correct_rate": round(correct_rate, 6),
        "erasure_rate": round(erasure_rate, 6),
        "symbol_error_rate": round(symbol_error_rate, 6),
        "throughput_proxy": round(throughput_proxy, 6),
        "mode": "analytical",
    }

# ---------------------------------------------------------------------------
# Monte Carlo verification
# ---------------------------------------------------------------------------

def monte_carlo_metrics(M, p_loss, p_confuse, n_trials, rng):
    """
    Estimate channel metrics by Monte Carlo simulation.

    Used for verification against the analytical results.
    """
    correct = 0
    erased = 0
    symbol_error = 0

    for _ in range(n_trials):
        true_sym = rng.randint(0, M - 1)

        if rng.random() < p_loss:
            erased += 1
            continue

        if rng.random() < p_confuse:
            # Decode as a uniformly random wrong symbol
            wrong = rng.randint(0, M - 2)
            decoded = wrong if wrong < true_sym else wrong + 1
            symbol_error += 1
        else:
            decoded = true_sym
            correct += 1

    total = n_trials
    bits_per_symbol = math.log2(M) if M >= 2 else 0.0
    correct_rate = correct / total
    throughput_proxy = correct_rate * bits_per_symbol

    return {
        "M": M,
        "bits_per_symbol": round(bits_per_symbol, 4),
        "p_loss": p_loss,
        "p_confuse": p_confuse,
        "correct_rate": round(correct_rate, 6),
        "erasure_rate": round(erased / total, 6),
        "symbol_error_rate": round(symbol_error / total, 6),
        "throughput_proxy": round(throughput_proxy, 6),
        "mode": f"monte_carlo_n={n_trials}",
    }

# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(m_values, p_loss_values, p_confuse_values,
                   use_monte_carlo=False, n_trials=10000, seed=SEED):
    rng = random.Random(seed)
    results = []

    for M in m_values:
        for p_loss in p_loss_values:
            for p_confuse in p_confuse_values:
                if use_monte_carlo:
                    row = monte_carlo_metrics(M, p_loss, p_confuse, n_trials, rng)
                else:
                    row = analytical_metrics(M, p_loss, p_confuse)
                results.append(row)

    return results

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 70)
    print("Qudit-Inspired Toy Channel Comparison")
    print("=" * 70)
    print()
    print("TOY MODEL WARNING:")
    print("  This is NOT a quantum computing simulation.")
    print("  This is NOT a proof of quantum advantage.")
    print("  This is a simplified parametric channel model for educational use.")
    print("  See docs/comparative-simulation-framework.md for full explanation.")
    print()

def print_summary_table(results, m_values, p_loss_values, p_confuse_values):
    # Print a condensed table: for selected p_loss and p_confuse, show
    # throughput_proxy across M values

    print("--- Throughput proxy across M values (selected channel parameters) ---")
    print()
    print("  throughput_proxy = correct_rate x log2(M)")
    print("  (simplified metric; does not account for FEC or hardware overhead)")
    print()

    # Show a few representative (p_loss, p_confuse) pairs
    representative = [
        (0.0,  0.0),   # ideal channel
        (0.0,  0.05),  # confusion only
        (0.05, 0.05),  # loss + confusion
        (0.10, 0.10),  # degraded channel
    ]

    for p_loss, p_confuse in representative:
        if p_loss not in p_loss_values or p_confuse not in p_confuse_values:
            continue
        print(f"  p_loss={p_loss:.2f}  p_confuse={p_confuse:.2f}:")
        print(f"  {'M':>6} {'bits/sym':>9} {'correct':>9} {'SER':>7} {'tput':>7}")
        print("  " + "-" * 45)
        for row in results:
            if row["p_loss"] == p_loss and row["p_confuse"] == p_confuse:
                print(
                    f"  {row['M']:>6} {row['bits_per_symbol']:>9.3f} "
                    f"{row['correct_rate']:>9.4f} {row['symbol_error_rate']:>7.4f} "
                    f"{row['throughput_proxy']:>7.4f}"
                )
        print()

def print_interpretation():
    print("--- Interpretation (toy model, not physical quantum results) ---")
    print()
    print("  Ideal channel (p_loss=0, p_confuse=0):")
    print("    throughput_proxy = log2(M)")
    print("    Higher M always wins: more information per symbol, no errors.")
    print("    Real channels are never ideal.")
    print()
    print("  Confusion-dominated channel (p_confuse > 0):")
    print("    Higher M carries more bits but requires lower confusion probability")
    print("    to maintain the same throughput proxy.")
    print("    At high p_confuse, the throughput proxy advantage of larger M erodes.")
    print()
    print("  Loss + confusion channel:")
    print("    Combined effect limits effective throughput.")
    print("    Throughput proxy = (1-p_loss)*(1-p_confuse)*log2(M).")
    print("    All three factors must be controlled for benefit from larger M.")
    print()
    print("  Real qudit systems face additional challenges not in this model:")
    print("    - Measurement reliability degrades with M in real quantum hardware.")
    print("    - Decoherence rates scale with system complexity.")
    print("    - Error correction overhead is not modeled here.")
    print("    - This toy model does NOT capture those effects.")
    print()
    print("  This model is useful only for qualitative illustration of the")
    print("  trade-off between M, loss, and confusion at the level of a")
    print("  simplified parametric channel - nothing more.")

def write_csv(results, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = [
        "M", "bits_per_symbol", "p_loss", "p_confuse",
        "correct_rate", "erasure_rate", "symbol_error_rate",
        "throughput_proxy", "mode",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  CSV saved: {csv_path}")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(m_values=M_VALUES, p_loss_values=P_LOSS_VALUES,
         p_confuse_values=P_CONFUSE_VALUES,
         use_monte_carlo=False, n_trials=10000,
         seed=SEED, csv_path=DEFAULT_CSV):

    print_header()
    mode_str = f"Monte Carlo (n={n_trials})" if use_monte_carlo else "Analytical"
    print(f"  Mode: {mode_str}  |  Seed: {seed}")
    print(f"  M values: {m_values}")
    print(f"  p_loss values: {p_loss_values}")
    print(f"  p_confuse values: {p_confuse_values}")
    print()

    results = run_simulation(m_values, p_loss_values, p_confuse_values,
                             use_monte_carlo=use_monte_carlo,
                             n_trials=n_trials, seed=seed)

    print_summary_table(results, m_values, p_loss_values, p_confuse_values)
    print_interpretation()
    print()
    write_csv(results, csv_path)
    print()
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Qudit-inspired toy channel comparison"
    )
    parser.add_argument("--monte-carlo", action="store_true",
                        help="Use Monte Carlo instead of analytical computation")
    parser.add_argument("--trials", type=int, default=10000,
                        help="Trials per condition (Monte Carlo mode only)")
    parser.add_argument("--seed", type=int, default=SEED,
                        help=f"Random seed (default: {SEED})")
    parser.add_argument("--csv", type=str, default=DEFAULT_CSV,
                        help="Output CSV path")
    args = parser.parse_args()
    main(
        use_monte_carlo=args.monte_carlo,
        n_trials=args.trials,
        seed=args.seed,
        csv_path=args.csv,
    )
