"""
photonic_binary_vs_obqc.py - Photonic encoding comparison: binary vs optical bead
==================================================================================
Compares binary photonic encoding (M=2 states) against high-dimensional optical
bead encoding (M=4 to 128 states) under a simplified Gaussian noise model in a
normalized D-dimensional state space.

MODEL DISCLAIMER:
  This is a simplified classical noisy-symbol model, NOT a full quantum or
  physical optics simulation. States are represented as grid points in a
  normalized D-dimensional space [0,1]^D. Noise is independent Gaussian per
  dimension. Decoding uses nearest-neighbor distance.

  This model captures:
    - the geometric trade-off between alphabet size and inter-state distance
    - how noise sensitivity increases as more states are packed into the same space
    - throughput proxy = log2(M) * (1 - SER) as a simplified info-rate estimate

  This model does NOT capture:
    - photon shot noise, quantum measurement, or detector statistics
    - optical crosstalk, polarization mode coupling, phase instability
    - hardware engineering constraints of real photonic systems
    - quantum channel capacity (Holevo bound, etc.)

IMPORTANT:
  This simulation does NOT claim that optical bead encoding outperforms binary
  photonic encoding in all cases, or in any real hardware setting.
  Results depend entirely on the stated model assumptions.

No mandatory external dependencies. numpy and matplotlib are used if available.
Random seed is fixed for reproducibility.
ASCII-only console output.

Usage:
    python photonic_binary_vs_obqc.py
    python photonic_binary_vs_obqc.py --trials 1000 --csv results/my_results.csv
"""

import random
import math
import os
import csv
import itertools
import argparse

# Optional imports
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42
DEFAULT_TRIALS = 500

SIGMA_VALUES = [0.01, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20]

# Configurations to compare: (label, M, D)
#   Binary photonic baseline: M=2, D=1
#   Optical bead variants: varying M and D
CONFIGS = [
    ("Binary  M=2   D=1", 2, 1),
    ("OBC     M=4   D=2", 4, 2),
    ("OBC     M=8   D=2", 8, 2),
    ("OBC     M=16  D=2", 16, 2),
    ("OBC     M=64  D=2", 64, 2),
    ("OBC     M=4   D=4", 4, 4),
    ("OBC     M=16  D=4", 16, 4),
    ("OBC     M=64  D=4", 64, 4),
    ("OBC     M=128 D=7", 128, 7),
]

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
DEFAULT_CSV = os.path.join(RESULTS_DIR, "photonic_binary_vs_obqc.csv")

# ---------------------------------------------------------------------------
# Alphabet construction
# ---------------------------------------------------------------------------

def build_grid_alphabet(M, D):
    """
    Build an M-state alphabet in D-dimensional [0,1]^D space.

    States are arranged on a regular grid: n_levels evenly spaced values per
    dimension, where n_levels = ceil(M^(1/D)), minimum 2.

    For M=2, D=1: states at [0.0] and [1.0], margin=1.0
    For M=4, D=2: 2x2 grid, states at corners, margin=1.0
    For M=16, D=2: 4x4 grid, margin=0.333
    etc.

    Returns:
        list of tuples: first M grid points in lexicographic order
    """
    if D == 0 or M < 2:
        raise ValueError(f"Invalid M={M} or D={D}")

    n_levels = max(2, math.ceil(M ** (1.0 / D)))
    step = 1.0 / (n_levels - 1) if n_levels > 1 else 1.0
    levels = [i * step for i in range(n_levels)]

    all_states = list(itertools.product(levels, repeat=D))
    return [list(s) for s in all_states[:M]]


def min_inter_state_distance(alphabet):
    """Compute the minimum Euclidean distance between any two distinct states."""
    min_d = float("inf")
    n = len(alphabet)
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean(alphabet[i], alphabet[j])
            if d < min_d:
                min_d = d
    return min_d

# ---------------------------------------------------------------------------
# Noise and decoding
# ---------------------------------------------------------------------------

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def add_gaussian_noise(state, sigma, rng):
    """Add independent Gaussian noise to each dimension, clipping to [0,1]."""
    return [max(0.0, min(1.0, v + rng.gauss(0.0, sigma))) for v in state]


def nearest_neighbor_decode(received, alphabet):
    """Return index of nearest alphabet state to the received point."""
    best_idx = 0
    best_d = euclidean(received, alphabet[0])
    for i, state in enumerate(alphabet[1:], 1):
        d = euclidean(received, state)
        if d < best_d:
            best_d = d
            best_idx = i
    return best_idx

# ---------------------------------------------------------------------------
# Simulation core
# ---------------------------------------------------------------------------

def compute_ser(alphabet, sigma, n_trials, rng):
    """
    Estimate symbol error rate by Monte Carlo simulation.

    Args:
        alphabet: list of state vectors
        sigma: Gaussian noise standard deviation per dimension
        n_trials: number of trials
        rng: random.Random instance

    Returns:
        float: symbol error rate
    """
    errors = 0
    M = len(alphabet)
    for _ in range(n_trials):
        true_idx = rng.randint(0, M - 1)
        received = add_gaussian_noise(alphabet[true_idx], sigma, rng)
        decoded_idx = nearest_neighbor_decode(received, alphabet)
        if decoded_idx != true_idx:
            errors += 1
    return errors / n_trials

# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(configs, sigma_values, n_trials, seed):
    rng = random.Random(seed)
    results = []

    for label, M, D in configs:
        alphabet = build_grid_alphabet(M, D)
        actual_M = len(alphabet)  # may be <= M if grid doesn't fill exactly
        margin = min_inter_state_distance(alphabet)
        bits_per_symbol = math.log2(actual_M) if actual_M >= 2 else 0.0

        for sigma in sigma_values:
            ser = compute_ser(alphabet, sigma, n_trials, rng)
            throughput_proxy = bits_per_symbol * (1.0 - ser)
            results.append({
                "label": label.strip(),
                "M": actual_M,
                "D": D,
                "bits_per_symbol": round(bits_per_symbol, 4),
                "separability_margin": round(margin, 4),
                "sigma": sigma,
                "trials": n_trials,
                "symbol_error_rate": round(ser, 5),
                "throughput_proxy": round(throughput_proxy, 5),
            })

    return results

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 75)
    print("Photonic Binary vs Optical Bead Encoding Comparison Simulator")
    print("=" * 75)
    print()
    print("MODEL: Simplified noisy D-dimensional symbol classification.")
    print("  - States are grid points in [0,1]^D normalized space.")
    print("  - Noise is independent Gaussian per dimension.")
    print("  - Decoding is nearest-neighbor distance.")
    print("  - This is NOT a quantum or physical optics simulation.")
    print("  - Results are under idealized model assumptions only.")
    print()

def print_alphabet_summary(configs):
    print("--- Alphabet properties ---")
    print()
    print(f"  {'Label':<25} {'M':>5} {'D':>3} {'bits/sym':>9} {'margin':>8}")
    print("  " + "-" * 55)
    for label, M, D in configs:
        alphabet = build_grid_alphabet(M, D)
        actual_M = len(alphabet)
        margin = min_inter_state_distance(alphabet)
        bits = math.log2(actual_M) if actual_M >= 2 else 0.0
        print(f"  {label:<25} {actual_M:>5} {D:>3} {bits:>9.3f} {margin:>8.4f}")
    print()
    print("  NOTE: margin = minimum Euclidean distance between any two states.")
    print("  Higher M (for fixed D) -> smaller margin -> more noise-sensitive.")
    print("  Higher D (for fixed M) -> may preserve larger margin.")
    print()

def print_results_table(results):
    print("--- Simulation results (symbol error rate and throughput proxy) ---")
    print()
    print(f"  {'Label':<25} {'sig':>5} {'M':>5} {'D':>3} {'SER':>7} {'bits/sym':>9} {'tput':>7}")
    print("  " + "-" * 68)

    last_label = None
    for row in results:
        if row["label"] != last_label:
            if last_label is not None:
                print()
            last_label = row["label"]
        print(
            f"  {row['label']:<25} {row['sigma']:>5.2f} {row['M']:>5} {row['D']:>3} "
            f"{row['symbol_error_rate']:>7.4f} {row['bits_per_symbol']:>9.3f} "
            f"{row['throughput_proxy']:>7.4f}"
        )
    print()

def print_interpretation():
    print("--- Interpretation (model-specific, not general claims) ---")
    print()
    print("  Binary photonic (M=2):")
    print("    - Maximum separability margin (1.0 in normalized space).")
    print("    - Very low SER even at high sigma.")
    print("    - But only 1 bit per symbol.")
    print()
    print("  Optical bead high-dimensional (large M):")
    print("    - More bits per symbol: log2(M) increases with M.")
    print("    - Smaller margin as M increases for fixed D -> faster SER rise.")
    print("    - Throughput proxy may peak at intermediate M for a given sigma.")
    print()
    print("  Higher D for same M:")
    print("    - Spreads states across more dimensions, preserving margin.")
    print("    - May maintain throughput at higher sigma, at cost of more DOFs.")
    print()
    print("  These are model-level results. Real photonic systems have")
    print("  additional noise sources not modeled here (crosstalk, drift,")
    print("  calibration, detector resolution). See docs/limitations.md.")

def write_csv(results, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = [
        "label", "M", "D", "bits_per_symbol", "separability_margin",
        "sigma", "trials", "symbol_error_rate", "throughput_proxy",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  CSV saved: {csv_path}")

# ---------------------------------------------------------------------------
# Optional matplotlib plot
# ---------------------------------------------------------------------------

def plot_throughput(results, save_path=None):
    if not HAS_MATPLOTLIB:
        return

    from collections import defaultdict
    by_label = defaultdict(lambda: {"sigmas": [], "tput": []})
    for row in results:
        by_label[row["label"]]["sigmas"].append(row["sigma"])
        by_label[row["label"]]["tput"].append(row["throughput_proxy"])

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, data in sorted(by_label.items()):
        ax.plot(data["sigmas"], data["tput"], marker="o", label=label)

    ax.set_xlabel("Gaussian noise sigma")
    ax.set_ylabel("Throughput proxy [bits/symbol * (1-SER)]")
    ax.set_title("Photonic encoding: throughput proxy vs noise\n"
                 "(simplified model - not physical optics simulation)")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=120)
        print(f"  Plot saved: {save_path}")
    else:
        plt.show()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(n_trials=DEFAULT_TRIALS, sigma_values=SIGMA_VALUES, configs=CONFIGS,
         seed=SEED, csv_path=DEFAULT_CSV, plot=False, plot_path=None):

    print_header()
    print(f"  Trials per condition: {n_trials}  |  Seed: {seed}")
    print(f"  numpy: {'available' if HAS_NUMPY else 'not available'}")
    print(f"  matplotlib: {'available' if HAS_MATPLOTLIB else 'not available'}")
    print()

    print_alphabet_summary(configs)

    print(f"  Running simulation ({len(configs)} configs x {len(sigma_values)} sigma values "
          f"x {n_trials} trials)...")
    print()

    results = run_simulation(configs, sigma_values, n_trials, seed)
    print_results_table(results)
    print_interpretation()
    print()
    write_csv(results, csv_path)

    if plot or plot_path:
        plot_throughput(results, save_path=plot_path)

    print()
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Photonic binary vs optical bead encoding comparison"
    )
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS,
                        help=f"Trials per condition (default: {DEFAULT_TRIALS})")
    parser.add_argument("--seed", type=int, default=SEED,
                        help=f"Random seed (default: {SEED})")
    parser.add_argument("--csv", type=str, default=DEFAULT_CSV,
                        help="Output CSV path")
    parser.add_argument("--plot", action="store_true",
                        help="Show throughput plot (requires matplotlib)")
    parser.add_argument("--save-plot", type=str, default=None,
                        help="Save plot to file")
    args = parser.parse_args()
    main(
        n_trials=args.trials,
        seed=args.seed,
        csv_path=args.csv,
        plot=args.plot,
        plot_path=args.save_plot,
    )
