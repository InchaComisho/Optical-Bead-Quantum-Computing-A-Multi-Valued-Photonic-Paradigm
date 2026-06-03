"""
confusion_matrix.py - Optical Bead Computing confusion matrix evaluator
=========================================================================
Runs multi-trial encode/decode simulations and outputs a confusion matrix.

The confusion matrix C[i][j] counts how many times true state i was
decoded as state j. Diagonal entries are correct decodings; off-diagonal
entries are errors.

Optionally uses numpy and matplotlib for better output if available,
but falls back to pure Python text output if they are not installed.

Usage:
    python confusion_matrix.py
    python confusion_matrix.py --sigma 0.06 --trials 200 --states 12
"""

import argparse
import random
import math

# Optional imports
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from encode_decode import build_alphabet, encode, decode, add_noise


# ---------------------------------------------------------------------------
# Confusion matrix computation
# ---------------------------------------------------------------------------

def compute_confusion_matrix(alphabet, sigma=0.05, n_trials=200):
    """
    Compute the confusion matrix for a given alphabet and noise level.

    C[i][j] = number of times true state i was decoded as state j.
    Diagonal = correct decodings. Off-diagonal = errors.

    Args:
        alphabet (list): optical bead alphabet
        sigma (float): Gaussian noise standard deviation
        n_trials (int): number of trials per true state

    Returns:
        list of lists: N×N confusion matrix (integer counts)
    """
    N = len(alphabet)
    C = [[0] * N for _ in range(N)]

    for true_idx in range(N):
        true_state = alphabet[true_idx]
        for _ in range(n_trials):
            received = add_noise(true_state, sigma=sigma)
            decoded_idx = decode(received, alphabet)
            C[true_idx][decoded_idx] += 1

    return C


def symbol_error_rate_from_matrix(C):
    """
    Compute the overall symbol error rate from a confusion matrix.
    """
    total = sum(sum(row) for row in C)
    correct = sum(C[i][i] for i in range(len(C)))
    return (total - correct) / total if total > 0 else 0.0


# ---------------------------------------------------------------------------
# Text output
# ---------------------------------------------------------------------------

def print_confusion_matrix(C, max_display=16):
    """
    Print a confusion matrix as a text table.
    Truncates display to max_display states for readability.
    """
    N = len(C)
    display_N = min(N, max_display)

    print(f"Confusion matrix (showing first {display_N} of {N} states):")
    print(f"Rows = true state, Columns = decoded state")
    print()

    header = "     " + "".join(f"{j:4d}" for j in range(display_N))
    if display_N < N:
        header += "  ..."
    print(header)
    print("     " + "-" * (display_N * 4 + 4))

    for i in range(display_N):
        row_str = f"{i:4d}|"
        for j in range(display_N):
            mark = f"{C[i][j]:4d}"
            row_str += mark
        if display_N < N:
            row_str += "  ..."
        print(row_str)

    if display_N < N:
        print(f"  ... ({N - display_N} more rows not shown)")

    print()
    ser = symbol_error_rate_from_matrix(C)
    correct = sum(C[i][i] for i in range(N))
    total = sum(sum(row) for row in C)
    print(f"Symbol error rate : {ser:.4f}  ({total - correct} errors / {total} total)")
    print(f"Decoding accuracy : {1.0 - ser:.4f}  ({correct} / {total} correct)")


def print_top_confusions(C, top_n=10):
    """
    Print the top off-diagonal confusions (most common error pairs).
    """
    N = len(C)
    errors = []
    for i in range(N):
        for j in range(N):
            if i != j and C[i][j] > 0:
                errors.append((C[i][j], i, j))
    errors.sort(reverse=True)

    print(f"Top {min(top_n, len(errors))} most frequent confusion pairs:")
    for count, true_i, decoded_j in errors[:top_n]:
        print(f"  True={true_i:3d} → Decoded={decoded_j:3d}  count={count:4d}")
    if not errors:
        print("  (no errors observed)")


# ---------------------------------------------------------------------------
# Matplotlib heatmap output
# ---------------------------------------------------------------------------

def plot_confusion_matrix(C, sigma, title=None, save_path=None):
    """
    Plot the confusion matrix as a heatmap using matplotlib.

    Only called if matplotlib is available.
    """
    if not HAS_MATPLOTLIB:
        return

    N = len(C)
    if HAS_NUMPY:
        matrix = np.array(C, dtype=float)
        row_sums = matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        norm_matrix = matrix / row_sums
    else:
        row_totals = [sum(row) or 1 for row in C]
        norm_matrix = [[C[i][j] / row_totals[i] for j in range(N)] for i in range(N)]
        if HAS_NUMPY:
            norm_matrix = np.array(norm_matrix)

    fig, ax = plt.subplots(figsize=(max(6, N * 0.4), max(5, N * 0.4)))
    if HAS_NUMPY:
        im = ax.imshow(norm_matrix, cmap="Blues", vmin=0, vmax=1)
    else:
        im = ax.imshow(norm_matrix, cmap="Blues", vmin=0, vmax=1)

    plt.colorbar(im, ax=ax, label="Normalized count (row)")
    ax.set_xlabel("Decoded state")
    ax.set_ylabel("True state")

    ser = symbol_error_rate_from_matrix(C)
    title = title or f"Optical Bead Confusion Matrix  σ={sigma:.3f}  SER={ser:.4f}"
    ax.set_title(title)

    tick_step = max(1, N // 16)
    ticks = list(range(0, N, tick_step))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=120)
        print(f"Saved confusion matrix plot to: {save_path}")
    else:
        plt.show()


# ---------------------------------------------------------------------------
# SER sweep
# ---------------------------------------------------------------------------

def ser_vs_sigma_sweep(alphabet, sigma_values, n_trials=200):
    """
    Compute SER for a range of noise levels.

    Returns:
        list of (sigma, SER) pairs
    """
    results = []
    for sigma in sigma_values:
        C = compute_confusion_matrix(alphabet, sigma=sigma, n_trials=n_trials)
        ser = symbol_error_rate_from_matrix(C)
        results.append((sigma, ser))
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Optical Bead Computing confusion matrix evaluator"
    )
    parser.add_argument(
        "--sigma", type=float, default=0.05,
        help="Gaussian noise standard deviation (default: 0.05)"
    )
    parser.add_argument(
        "--trials", type=int, default=200,
        help="Number of trials per state (default: 200)"
    )
    parser.add_argument(
        "--states", type=int, default=None,
        help="Limit alphabet to first N states (default: full alphabet)"
    )
    parser.add_argument(
        "--sweep", action="store_true",
        help="Run SER sweep over a range of sigma values"
    )
    parser.add_argument(
        "--plot", action="store_true",
        help="Show confusion matrix heatmap (requires matplotlib)"
    )
    parser.add_argument(
        "--save", type=str, default=None,
        help="Save confusion matrix plot to file (e.g., confusion.png)"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Optical Bead Computing - confusion matrix evaluator")
    print("=" * 60)

    alphabet = build_alphabet()
    if args.states is not None:
        alphabet = alphabet[: args.states]

    print(f"\nAlphabet size : {len(alphabet)} states")
    print(f"Noise level   : sigma = {args.sigma}")
    print(f"Trials/state  : {args.trials}")
    print(f"numpy         : {'available' if HAS_NUMPY else 'not available'}")
    print(f"matplotlib    : {'available' if HAS_MATPLOTLIB else 'not available'}")
    print()

    C = compute_confusion_matrix(alphabet, sigma=args.sigma, n_trials=args.trials)
    print_confusion_matrix(C)
    print()
    print_top_confusions(C)

    if args.sweep:
        print("\n--- SER vs noise level sweep ---")
        sigma_values = [0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.13, 0.17, 0.22]
        results = ser_vs_sigma_sweep(alphabet, sigma_values, n_trials=args.trials)
        print(f"{'σ':>8}  {'SER':>8}  bar")
        for sigma, ser in results:
            bar = "#" * int(ser * 40)
            print(f"  {sigma:.3f}    {ser:.4f}   |{bar}")

    if args.plot or args.save:
        if HAS_MATPLOTLIB:
            plot_confusion_matrix(C, sigma=args.sigma, save_path=args.save)
        else:
            print("\nmatplotlib not available. Install it with: pip install matplotlib")

    print("\nDone.")


if __name__ == "__main__":
    main()
