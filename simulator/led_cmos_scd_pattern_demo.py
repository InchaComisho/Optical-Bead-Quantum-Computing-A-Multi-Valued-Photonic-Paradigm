"""
led_cmos_scd_pattern_demo.py - Toy LED-CMOS SCD Pattern Readout Demo
======================================================================
Demonstrates:
  - SCD digit encoding (soroban-coded decimal, 5-bit thermometer pattern)
  - Mapping to a simplified LED brightness pattern
  - Adding Gaussian brightness noise (simulated CMOS sensor noise)
  - CMOS-like threshold readout
  - Decoding back to an SCD pattern
  - Reporting correct, detected-error, and silent-error outcomes

Output:
  - Console summary table (ASCII only)
  - results/led_cmos_scd_pattern_demo.csv

NOTE: This is a TOY MODEL of LED-CMOS readout.
It is NOT a physical sensor simulation.
Results depend entirely on the stated noise and threshold assumptions.
This does NOT prove that SCD outperforms BCD in all cases.
See docs/scd-cmos-led-pattern-architecture.md for full context.

Usage:
    python led_cmos_scd_pattern_demo.py
    python led_cmos_scd_pattern_demo.py --trials 5000
    python led_cmos_scd_pattern_demo.py --sigma 0.30
    python led_cmos_scd_pattern_demo.py --sigma 0.15 --trials 2000
"""

import random
import math
import os
import csv
import argparse
import sys


# ---------------------------------------------------------------------------
# SCD encoding: 5-bit thermometer (H, L4, L3, L2, L1)
# ---------------------------------------------------------------------------

# Table of valid SCD patterns indexed by digit 0-9
# Each entry is (H, L4, L3, L2, L1) as integers 0 or 1
SCD_TABLE = {
    0: (0, 0, 0, 0, 0),
    1: (0, 0, 0, 0, 1),
    2: (0, 0, 0, 1, 1),
    3: (0, 0, 1, 1, 1),
    4: (0, 1, 1, 1, 1),
    5: (1, 0, 0, 0, 0),
    6: (1, 0, 0, 0, 1),
    7: (1, 0, 0, 1, 1),
    8: (1, 0, 1, 1, 1),
    9: (1, 1, 1, 1, 1),
}

# Reverse map: valid SCD tuple -> digit
SCD_REVERSE = {v: k for k, v in SCD_TABLE.items()}

# All 32 possible 5-bit patterns
ALL_PATTERNS = [(h, l4, l3, l2, l1)
                for h in range(2)
                for l4 in range(2)
                for l3 in range(2)
                for l2 in range(2)
                for l1 in range(2)]

VALID_PATTERNS = set(SCD_TABLE.values())


def is_thermometer(l4, l3, l2, l1):
    """Return True if lower four bits form a valid thermometer pattern."""
    lower = (l4, l3, l2, l1)
    valid_lowers = {(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 1),
                   (0, 1, 1, 1), (1, 1, 1, 1)}
    return lower in valid_lowers


def is_valid_scd(pattern):
    """Return True if pattern is a valid SCD 5-tuple."""
    return pattern in VALID_PATTERNS


# ---------------------------------------------------------------------------
# LED brightness mapping
# ---------------------------------------------------------------------------

# Bright LED: brightness = 1.0 (on)
# Dark LED:   brightness = 0.0 (off)
LED_ON = 1.0
LED_OFF = 0.0


def scd_to_led_brightness(digit):
    """Map SCD digit to a list of 5 LED brightness values [H, L4, L3, L2, L1]."""
    h, l4, l3, l2, l1 = SCD_TABLE[digit]
    return [float(h), float(l4), float(l3), float(l2), float(l1)]


# ---------------------------------------------------------------------------
# Noise and threshold readout
# ---------------------------------------------------------------------------

def add_brightness_noise(brightness_list, sigma, rng):
    """Add independent Gaussian noise to each LED brightness value."""
    return [b + rng.gauss(0.0, sigma) for b in brightness_list]


def cmos_threshold_readout(noisy_brightness, threshold=0.5):
    """Apply a CMOS-like threshold: returns 1 if brightness > threshold, else 0."""
    return tuple(1 if b > threshold else 0 for b in noisy_brightness)


# ---------------------------------------------------------------------------
# Error classification
# ---------------------------------------------------------------------------

def classify_outcome(original_digit, decoded_pattern):
    """
    Classify the outcome of one trial:
      - 'correct':        decoded pattern matches the original digit
      - 'detected':       decoded pattern is structurally invalid (thermometer violation)
      - 'silent_error':   decoded pattern is valid but maps to a different digit
    """
    if decoded_pattern == SCD_TABLE[original_digit]:
        return 'correct'
    if not is_valid_scd(decoded_pattern):
        return 'detected'
    # Valid pattern but wrong digit
    return 'silent_error'


# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(trials_per_digit=1000, sigma=0.20, threshold=0.5, seed=42):
    """
    Run the LED-CMOS SCD pattern demo simulation.

    For each digit 0-9:
      - Encode as SCD
      - Map to LED brightness
      - Add Gaussian noise (sigma)
      - Apply CMOS threshold
      - Decode
      - Count correct / detected / silent_error outcomes

    Returns a list of result dicts, one per digit.
    """
    rng = random.Random(seed)
    results = []

    for digit in range(10):
        correct = 0
        detected = 0
        silent = 0
        base_brightness = scd_to_led_brightness(digit)

        for _ in range(trials_per_digit):
            noisy = add_brightness_noise(base_brightness, sigma, rng)
            decoded = cmos_threshold_readout(noisy, threshold)
            outcome = classify_outcome(digit, decoded)
            if outcome == 'correct':
                correct += 1
            elif outcome == 'detected':
                detected += 1
            else:
                silent += 1

        results.append({
            'digit': digit,
            'trials': trials_per_digit,
            'correct': correct,
            'detected_error': detected,
            'silent_error': silent,
            'correct_rate': correct / trials_per_digit,
            'detected_rate': detected / trials_per_digit,
            'silent_rate': silent / trials_per_digit,
        })

    return results


def run_sigma_sweep(sigmas, trials_per_digit=500, threshold=0.5, seed=42):
    """Run simulation across multiple sigma values, averaging over all digits."""
    sweep_results = []
    for sigma in sigmas:
        per_digit = run_simulation(trials_per_digit, sigma, threshold, seed)
        avg_correct = sum(r['correct_rate'] for r in per_digit) / 10.0
        avg_detected = sum(r['detected_rate'] for r in per_digit) / 10.0
        avg_silent = sum(r['silent_rate'] for r in per_digit) / 10.0
        sweep_results.append({
            'sigma': sigma,
            'avg_correct_rate': avg_correct,
            'avg_detected_rate': avg_detected,
            'avg_silent_rate': avg_silent,
        })
    return sweep_results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_scd_table():
    """Print the SCD encoding table to console (ASCII only)."""
    print("SCD Encoding Table")
    print("  Digit | H | L4 L3 L2 L1 | 5-bit pattern")
    print("  ------+---+-------------+--------------")
    for d in range(10):
        h, l4, l3, l2, l1 = SCD_TABLE[d]
        print(f"    {d}   | {h} | {l4}  {l3}  {l2}  {l1}   | {h} {l4}{l3}{l2}{l1}")
    print()


def print_results_table(results, sigma, threshold):
    """Print per-digit results table to console."""
    print(f"LED-CMOS SCD Pattern Demo Results")
    print(f"  sigma={sigma:.3f}  threshold={threshold:.2f}")
    print(f"  Trials per digit: {results[0]['trials']}")
    print()
    print("  Digit | Correct | Detected | Silent  | Correct% | Detected% | Silent%")
    print("  ------+---------+----------+---------+----------+-----------+--------")
    for r in results:
        print(
            f"    {r['digit']}   | "
            f"{r['correct']:7d} | "
            f"{r['detected_error']:8d} | "
            f"{r['silent_error']:7d} | "
            f"{r['correct_rate']*100:8.1f} | "
            f"{r['detected_rate']*100:9.1f} | "
            f"{r['silent_rate']*100:7.1f}"
        )
    total_trials = sum(r['trials'] for r in results)
    total_correct = sum(r['correct'] for r in results)
    total_detected = sum(r['detected_error'] for r in results)
    total_silent = sum(r['silent_error'] for r in results)
    print("  ------+---------+----------+---------+----------+-----------+--------")
    print(
        f"  Total | "
        f"{total_correct:7d} | "
        f"{total_detected:8d} | "
        f"{total_silent:7d} | "
        f"{total_correct/total_trials*100:8.1f} | "
        f"{total_detected/total_trials*100:9.1f} | "
        f"{total_silent/total_trials*100:7.1f}"
    )
    print()


def print_sweep_table(sweep_results):
    """Print sigma sweep summary table."""
    print("Sigma Sweep (averaged over digits 0-9)")
    print("  Sigma  | Correct%  | Detected% | Silent%")
    print("  -------+-----------+-----------+--------")
    for r in sweep_results:
        print(
            f"  {r['sigma']:.3f}  | "
            f"{r['avg_correct_rate']*100:9.1f} | "
            f"{r['avg_detected_rate']*100:9.1f} | "
            f"{r['avg_silent_rate']*100:7.1f}"
        )
    print()


def save_csv(results, sweep_results, csv_path):
    """Save per-digit results and sweep results to a CSV file."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow([
            "# TOY MODEL WARNING: This is a simplified brightness-noise model.",
            "", "", "", "", "", "", ""
        ])
        writer.writerow([
            "# It is NOT a physical sensor simulation.",
            "", "", "", "", "", "", ""
        ])
        writer.writerow([
            "# Results depend entirely on stated sigma and threshold assumptions.",
            "", "", "", "", "", "", ""
        ])
        writer.writerow([])

        # Per-digit results
        writer.writerow([
            "section", "digit", "trials", "sigma", "threshold",
            "correct", "detected_error", "silent_error",
            "correct_rate", "detected_rate", "silent_rate"
        ])
        for r in results:
            writer.writerow([
                "per_digit",
                r['digit'],
                r['trials'],
                "",
                "",
                r['correct'],
                r['detected_error'],
                r['silent_error'],
                f"{r['correct_rate']:.4f}",
                f"{r['detected_rate']:.4f}",
                f"{r['silent_rate']:.4f}",
            ])

        writer.writerow([])

        # Sigma sweep
        writer.writerow([
            "section", "sigma", "avg_correct_rate", "avg_detected_rate", "avg_silent_rate",
            "", "", "", "", "", ""
        ])
        for r in sweep_results:
            writer.writerow([
                "sweep",
                f"{r['sigma']:.3f}",
                f"{r['avg_correct_rate']:.4f}",
                f"{r['avg_detected_rate']:.4f}",
                f"{r['avg_silent_rate']:.4f}",
                "", "", "", "", "", ""
            ])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Toy LED-CMOS SCD pattern readout demo.\n"
            "NOTE: This is a simplified model, not a physical sensor simulation."
        )
    )
    parser.add_argument(
        "--trials", type=int, default=1000,
        help="Number of trials per digit (default: 1000)"
    )
    parser.add_argument(
        "--sigma", type=float, default=0.20,
        help="Gaussian brightness noise sigma (default: 0.20)"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.5,
        help="CMOS readout threshold (default: 0.5)"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed (default: 42)"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    csv_path = os.path.join(results_dir, "led_cmos_scd_pattern_demo.csv")

    print()
    print("=" * 70)
    print("Optical Bead Computing - LED-CMOS SCD Pattern Demo")
    print("=" * 70)
    print()
    print("TOY MODEL WARNING:")
    print("  This demo uses a simplified Gaussian brightness noise model.")
    print("  It is NOT a physical sensor or optics simulation.")
    print("  Results depend entirely on the stated sigma and threshold.")
    print("  See docs/scd-cmos-led-pattern-architecture.md for full context.")
    print()

    print_scd_table()

    # Main simulation at specified sigma
    results = run_simulation(
        trials_per_digit=args.trials,
        sigma=args.sigma,
        threshold=args.threshold,
        seed=args.seed
    )
    print_results_table(results, args.sigma, args.threshold)

    # Sigma sweep
    sigmas = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    sweep = run_sigma_sweep(sigmas, trials_per_digit=max(200, args.trials // 5),
                            threshold=args.threshold, seed=args.seed)
    print_sweep_table(sweep)

    # Save CSV
    save_csv(results, sweep, csv_path)
    print(f"Results saved to: {csv_path}")
    print()

    # Brief interpretation
    total_trials = sum(r['trials'] for r in results)
    total_silent = sum(r['silent_error'] for r in results)
    total_detected = sum(r['detected_error'] for r in results)
    total_correct = sum(r['correct'] for r in results)
    print("Key findings (at sigma={:.2f}, threshold={:.2f}):".format(
        args.sigma, args.threshold))
    print(f"  Correct:        {total_correct/total_trials*100:.1f}%")
    print(f"  Detected error: {total_detected/total_trials*100:.1f}%  "
          "(invalid thermometer pattern, flagged)")
    print(f"  Silent error:   {total_silent/total_trials*100:.1f}%  "
          "(valid pattern, wrong digit, undetected)")
    print()
    print("Interpretation:")
    print("  At low sigma, brightness noise rarely crosses the threshold.")
    print("  At high sigma, threshold crossings produce invalid patterns (detected)")
    print("  or valid-but-wrong patterns (silent errors).")
    print("  Silent errors arise from H-bit crossings (digit shifts by +-5)")
    print("  or thermometer-preserving lower-bit crossings (adjacent digit shifts).")
    print()
    print("  SCD can detect many random-error patterns due to its 22/32 invalid-")
    print("  state fraction, but cannot detect all silent errors without ECC.")
    print()


if __name__ == "__main__":
    main()
