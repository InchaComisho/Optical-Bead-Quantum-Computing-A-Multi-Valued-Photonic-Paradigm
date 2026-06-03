"""
run_comparisons.py - Run all OBQC comparison simulators
=========================================================
Runs all three comparison simulators in sequence and reports
the locations of the generated CSV files.

Usage:
    python run_comparisons.py
    python run_comparisons.py --trials 1000
"""

import subprocess
import sys
import os
import argparse
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

SIMULATORS = [
    {
        "name": "Electronic BCD vs SCD",
        "script": "electronic_binary_vs_scd.py",
        "csv": os.path.join(RESULTS_DIR, "electronic_binary_vs_scd.csv"),
        "description": "Compares BCD and SCD encoding under random bit flips.",
    },
    {
        "name": "Photonic Binary vs OBC",
        "script": "photonic_binary_vs_obqc.py",
        "csv": os.path.join(RESULTS_DIR, "photonic_binary_vs_obqc.csv"),
        "description": "Compares binary and multi-state optical bead encoding under Gaussian noise.",
    },
    {
        "name": "Qudit-Inspired Toy Channel",
        "script": "qudit_inspired_channel.py",
        "csv": os.path.join(RESULTS_DIR, "qudit_inspired_channel.csv"),
        "description": "Toy parametric channel model for M-level symbol transmission.",
    },
    {
        "name": "Optical Medium Comparison",
        "script": "optical_medium_comparison.py",
        "csv": os.path.join(RESULTS_DIR, "optical_medium_comparison.csv"),
        "description": "Compares noise models for open-air, sealed-air, sealed-liquid, "
                       "acrylic, glass/quartz, and fiber media.",
    },
]


def run_script(script_name, extra_args=None):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = [sys.executable, script_path]
    if extra_args:
        cmd.extend(extra_args)

    print(f"  Running: {script_name}")
    print("  " + "-" * 60)

    start = time.time()
    result = subprocess.run(
        cmd,
        capture_output=False,
        text=True,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"\n  ERROR: {script_name} exited with code {result.returncode}")
        return False

    print(f"\n  Completed in {elapsed:.1f}s")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run all OBQC comparison simulators"
    )
    parser.add_argument("--trials", type=int, default=None,
                        help="Override default trial count for all simulators")
    args = parser.parse_args()

    print("=" * 70)
    print("OBQC Comparative Simulation Suite")
    print("=" * 70)
    print()
    print(f"  This runs {len(SIMULATORS)} comparison simulators:")
    for sim in SIMULATORS:
        print(f"    - {sim['name']}: {sim['description']}")
    print()
    print("  DISCLAIMER: These are simplified, model-based comparisons.")
    print("  They do NOT prove superiority of any encoding scheme.")
    print("  See docs/comparative-simulation-framework.md for details.")
    print()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    results_summary = []
    all_ok = True

    for sim in SIMULATORS:
        print(f"{'=' * 70}")
        print(f"  [{sim['name']}]")
        print(f"  {sim['description']}")
        print()

        extra_args = []
        if args.trials is not None:
            extra_args.extend(["--trials", str(args.trials)])

        ok = run_script(sim["script"], extra_args=extra_args)
        results_summary.append((sim["name"], sim["csv"], ok))
        all_ok = all_ok and ok
        print()

    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print("  Generated CSV files:")
    for name, csv_path, ok in results_summary:
        status = "OK" if ok else "FAILED"
        exists = os.path.isfile(csv_path)
        exists_str = "(file exists)" if exists else "(file not found)"
        print(f"    [{status}] {name}")
        print(f"           {csv_path} {exists_str}")
    print()
    print(f"  Results directory: {RESULTS_DIR}")
    print()

    if all_ok:
        print("  All simulators completed successfully.")
    else:
        print("  WARNING: One or more simulators reported errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
