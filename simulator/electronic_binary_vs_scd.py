"""
electronic_binary_vs_scd.py - Electronic encoding comparison: BCD vs SCD under bit flips
==========================================================================================
Compares Binary-Coded Decimal (BCD, 4-bit) against Soroban-Coded Decimal (SCD, 5-bit)
under a random independent bit-flip noise model.

Metrics reported per encoding and per flip probability p:
  correct_rate      - fraction of trials decoded correctly
  detected_rate     - fraction of trials with structurally invalid decoded pattern
  silent_error_rate - fraction of trials decoded to a different valid digit

Key facts:
  BCD : 4 bits per digit, 10/16 valid states (62.5%), 6/16 invalid (37.5%)
  SCD : 5 bits per digit, 10/32 valid states (31.25%), 22/32 invalid (68.75%)

IMPORTANT: This simulation does NOT claim that SCD beats BCD in all cases.
  - BCD is more compact (4 bits vs 5 bits per digit, 25% more storage for SCD)
  - SCD has more invalid states and therefore detects more random bit-flip errors
  - Detection is not correction; correction requires additional redundancy
  - Results depend on the independent-flip noise model; correlated hardware faults behave differently

No external dependencies required.
Random seed is fixed for reproducibility.

Usage:
    python electronic_binary_vs_scd.py
    python electronic_binary_vs_scd.py --trials 5000 --csv results/my_results.csv

Output:
    Console table (ASCII only)
    CSV file: simulator/results/electronic_binary_vs_scd.csv
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
DEFAULT_TRIALS = 10000
P_VALUES = [0.001, 0.005, 0.010, 0.020, 0.050, 0.100]
DIGITS = list(range(10))

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
DEFAULT_CSV = os.path.join(RESULTS_DIR, "electronic_binary_vs_scd.csv")

# ---------------------------------------------------------------------------
# BCD encoding (4-bit)
# ---------------------------------------------------------------------------

BCD_BITS = 4

def bcd_encode(d):
    """Encode decimal digit d (0-9) as a 4-bit list [b3, b2, b1, b0], MSB first."""
    return [(d >> i) & 1 for i in range(BCD_BITS - 1, -1, -1)]

def bcd_decode(bits):
    """
    Decode a 4-bit list to a decimal digit.
    Returns the digit (0-9) if valid, or None if the pattern is out of decimal range (10-15).
    """
    val = 0
    for b in bits:
        val = (val << 1) | b
    if 0 <= val <= 9:
        return val
    return None  # invalid: 10-15

BCD_VALID_COUNT = 10
BCD_TOTAL_STATES = 2 ** BCD_BITS
BCD_INVALID_COUNT = BCD_TOTAL_STATES - BCD_VALID_COUNT

# ---------------------------------------------------------------------------
# SCD encoding (5-bit): H + L4 L3 L2 L1 in thermometer code
# ---------------------------------------------------------------------------

SCD_BITS = 5

_SCD_LOWER_ENCODE = [0b0000, 0b0001, 0b0011, 0b0111, 0b1111]
_SCD_LOWER_DECODE = {0b0000: 0, 0b0001: 1, 0b0011: 2, 0b0111: 3, 0b1111: 4}

def scd_encode(d):
    """Encode decimal digit d (0-9) as a 5-bit list [H, L4, L3, L2, L1]."""
    h = 1 if d >= 5 else 0
    lower_count = d - 5 * h
    lower_bits = _SCD_LOWER_ENCODE[lower_count]
    l4 = (lower_bits >> 3) & 1
    l3 = (lower_bits >> 2) & 1
    l2 = (lower_bits >> 1) & 1
    l1 = lower_bits & 1
    return [h, l4, l3, l2, l1]

def scd_decode(bits):
    """
    Decode a 5-bit list [H, L4, L3, L2, L1] to a decimal digit.
    Returns the digit (0-9) if valid, or None if the lower bits are not a thermometer code.
    """
    h, l4, l3, l2, l1 = bits
    lower_bits = (l4 << 3) | (l3 << 2) | (l2 << 1) | l1
    if lower_bits not in _SCD_LOWER_DECODE:
        return None  # invalid: non-thermometer lower pattern
    return 5 * h + _SCD_LOWER_DECODE[lower_bits]

SCD_VALID_COUNT = 10
SCD_TOTAL_STATES = 2 ** SCD_BITS
SCD_INVALID_COUNT = SCD_TOTAL_STATES - SCD_VALID_COUNT

# ---------------------------------------------------------------------------
# Bit flip model
# ---------------------------------------------------------------------------

def flip_bits(bits, p, rng):
    """Flip each bit independently with probability p."""
    return [1 - b if rng.random() < p else b for b in bits]

# ---------------------------------------------------------------------------
# Simulation core
# ---------------------------------------------------------------------------

def run_encoding_trial(encode_fn, decode_fn, p, n_trials, rng):
    """
    Run n_trials encode-flip-decode trials, sampling each digit uniformly.

    Returns dict with:
        correct           - count decoded correctly
        detected_error    - count with invalid decoded pattern
        silent_error      - count decoded to a different valid digit
        total             - total trials
    """
    correct = 0
    detected_error = 0
    silent_error = 0

    for _ in range(n_trials):
        digit = rng.randint(0, 9)
        encoded = encode_fn(digit)
        noisy = flip_bits(encoded, p, rng)
        decoded = decode_fn(noisy)

        if decoded is None:
            detected_error += 1
        elif decoded == digit:
            correct += 1
        else:
            silent_error += 1

    total = correct + detected_error + silent_error
    return {
        "correct": correct,
        "detected_error": detected_error,
        "silent_error": silent_error,
        "total": total,
    }

def rate(counts, key):
    """Return key count as a fraction of total."""
    return counts[key] / counts["total"]

# ---------------------------------------------------------------------------
# Expected theoretical rates (approximate, for single-bit flip only)
# ---------------------------------------------------------------------------

def bcd_invalid_fraction():
    return BCD_INVALID_COUNT / BCD_TOTAL_STATES

def scd_invalid_fraction():
    return SCD_INVALID_COUNT / SCD_TOTAL_STATES

# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(n_trials, p_values, seed):
    rng = random.Random(seed)
    results = []

    for p in p_values:
        # BCD
        bcd_counts = run_encoding_trial(bcd_encode, bcd_decode, p, n_trials, rng)
        results.append({
            "encoding": "BCD",
            "bits_per_digit": BCD_BITS,
            "valid_states": BCD_VALID_COUNT,
            "total_states": BCD_TOTAL_STATES,
            "invalid_fraction": round(BCD_INVALID_COUNT / BCD_TOTAL_STATES, 4),
            "flip_prob": p,
            "trials": n_trials,
            "correct_rate": round(rate(bcd_counts, "correct"), 5),
            "detected_error_rate": round(rate(bcd_counts, "detected_error"), 5),
            "silent_error_rate": round(rate(bcd_counts, "silent_error"), 5),
        })

        # SCD
        scd_counts = run_encoding_trial(scd_encode, scd_decode, p, n_trials, rng)
        results.append({
            "encoding": "SCD",
            "bits_per_digit": SCD_BITS,
            "valid_states": SCD_VALID_COUNT,
            "total_states": SCD_TOTAL_STATES,
            "invalid_fraction": round(SCD_INVALID_COUNT / SCD_TOTAL_STATES, 4),
            "flip_prob": p,
            "trials": n_trials,
            "correct_rate": round(rate(scd_counts, "correct"), 5),
            "detected_error_rate": round(rate(scd_counts, "detected_error"), 5),
            "silent_error_rate": round(rate(scd_counts, "silent_error"), 5),
        })

    return results

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_encoding_info():
    print("=" * 70)
    print("Electronic Binary vs SCD Comparison Simulator")
    print("=" * 70)
    print()
    print("DISCLAIMER: This is a falsifiable simulation framework.")
    print("It does NOT claim that SCD beats BCD in all cases.")
    print("See docs/comparative-simulation-framework.md for full explanation.")
    print()
    print("--- Encoding properties ---")
    print()
    print(f"  {'Encoding':<8} {'Bits/digit':>10} {'Valid':>6} {'Total':>6} {'Invalid':>8} {'Invalid%':>9}")
    print("  " + "-" * 50)
    print(f"  {'BCD':<8} {BCD_BITS:>10} {BCD_VALID_COUNT:>6} {BCD_TOTAL_STATES:>6} "
          f"{BCD_INVALID_COUNT:>8} {100*BCD_INVALID_COUNT/BCD_TOTAL_STATES:>8.1f}%")
    print(f"  {'SCD':<8} {SCD_BITS:>10} {SCD_VALID_COUNT:>6} {SCD_TOTAL_STATES:>6} "
          f"{SCD_INVALID_COUNT:>8} {100*SCD_INVALID_COUNT/SCD_TOTAL_STATES:>8.1f}%")
    print()
    print("  SCD overhead vs BCD: +25% storage per decimal digit")
    print("  SCD invalid state fraction: 68.75%  (BCD: 37.5%)")
    print("  -> SCD detects more random bit-flip errors,")
    print("     at the cost of 25% more bits per digit.")
    print("  -> Detection is NOT correction. Correction needs additional redundancy.")
    print()

def print_results_table(results):
    print("--- Simulation results (bit-flip noise model) ---")
    print()
    header = (
        f"  {'Encoding':<8} {'p_flip':>7} {'Correct%':>10} "
        f"{'Detected%':>10} {'Silent%':>10}"
    )
    print(header)
    print("  " + "-" * 52)

    last_p = None
    for row in results:
        if row["flip_prob"] != last_p:
            if last_p is not None:
                print()
            last_p = row["flip_prob"]
        print(
            f"  {row['encoding']:<8} {row['flip_prob']:>7.3f} "
            f"{100*row['correct_rate']:>9.2f}% "
            f"{100*row['detected_error_rate']:>9.2f}% "
            f"{100*row['silent_error_rate']:>9.2f}%"
        )
    print()

def print_interpretation():
    print("--- Interpretation ---")
    print()
    print("  At low flip probability (p <= 0.01):")
    print("    - Both BCD and SCD decode correctly most of the time.")
    print("    - SCD detects slightly more errors due to its larger invalid region.")
    print()
    print("  At moderate flip probability (p ~ 0.05):")
    print("    - Both schemes show significant error rates.")
    print("    - SCD converts more errors into detected (not silent) errors.")
    print("    - BCD has more silent errors (wrong digit, not detected).")
    print("    - SCD uses 25% more bits, so it experiences slightly more flip events.")
    print()
    print("  At high flip probability (p ~ 0.10):")
    print("    - Both schemes are unreliable without additional error correction.")
    print("    - SCD's detection advantage remains, but correction is still needed.")
    print()
    print("  Conclusion: SCD is suitable for pattern-oriented decimal logic")
    print("  where structural validity is valuable and storage density is secondary.")
    print("  BCD is preferable for compact decimal storage in standard hardware.")

def write_csv(results, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = [
        "encoding", "bits_per_digit", "valid_states", "total_states",
        "invalid_fraction", "flip_prob", "trials",
        "correct_rate", "detected_error_rate", "silent_error_rate",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  CSV saved: {csv_path}")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(n_trials=DEFAULT_TRIALS, p_values=P_VALUES, seed=SEED, csv_path=DEFAULT_CSV):
    print_encoding_info()
    print(f"  Trials per condition: {n_trials}  |  Seed: {seed}")
    print(f"  Flip probabilities: {p_values}")
    print()

    results = run_simulation(n_trials, p_values, seed)
    print_results_table(results)
    print_interpretation()
    print()
    write_csv(results, csv_path)
    print()
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Electronic BCD vs SCD comparison simulator"
    )
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS,
                        help=f"Trials per condition (default: {DEFAULT_TRIALS})")
    parser.add_argument("--seed", type=int, default=SEED,
                        help=f"Random seed (default: {SEED})")
    parser.add_argument("--csv", type=str, default=DEFAULT_CSV,
                        help="Output CSV path")
    args = parser.parse_args()
    main(n_trials=args.trials, seed=args.seed, csv_path=args.csv)
