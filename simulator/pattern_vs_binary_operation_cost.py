"""
pattern_vs_binary_operation_cost.py
=====================================
Abstract operation-cost comparison: sequential binary classification pipeline
vs a pattern-recognition pipeline.

PURPOSE
-------
This is NOT a hardware benchmark.
This is NOT a physical optics simulation.
This is an abstract operation-count and cost model under simplified,
explicitly stated assumptions.

Its purpose is to explore under what conditions a pattern-recognition
approach could reduce total operation cost relative to a sequential
binary-style processing pipeline.

Pattern recognition helps only when the reduction in downstream operations
and data movement exceeds the cost of optical pattern extraction and detection.
This model makes that condition explicit and testable.

PIPELINE MODELS
---------------

Baseline (sequential binary):
  Each input item requires:
    - binary_ops_per_item:    binary operations (comparisons, switching)
    - memory_accesses_per_item: memory reads/writes
    - data_movement_per_item: data transfers between processing stages
    - conversions_per_item:   analog-to-digital or format conversions

Pattern pipeline:
  Processing is restructured as:
    - Pattern extraction cost (per item): optical encoding and signal preparation
    - Pattern classification cost (per item): optical matching
    - Detector cost (per item): readout of classification result
    - Reduced binary ops: pattern_reduction_factor * binary_ops_per_item
    - Reduced data movement: proportionally reduced based on overhead_case

UNIT COSTS (abstract, not real joules):
  binary_op_cost      = 1
  memory_access_cost  = 5
  data_movement_cost  = 10
  conversion_cost     = 8

  Pattern extraction and detector costs depend on overhead_case.

PARAMETERS:
  workload_size:           1000, 10000, 100000, 1000000
  pattern_reduction_factor: 0.2, 0.4, 0.6, 0.8
  overhead_case:           low, medium, high

OUTPUT
------
- Printed table (ASCII)
- CSV: simulator/results/pattern_vs_binary_operation_cost.csv

Usage:
    python pattern_vs_binary_operation_cost.py

No external dependencies required.
"""

import csv
import os

# ---------------------------------------------------------------------------
# Unit cost model (abstract units)
# ---------------------------------------------------------------------------

BINARY_OP_COST        = 1
MEMORY_ACCESS_COST    = 5
DATA_MOVEMENT_COST    = 10
CONVERSION_COST       = 8

# Per-item operation counts for baseline pipeline
# These represent a typical repeated classification task (e.g., readout
# discrimination, syndrome detection, pattern lookup)
BINARY_OPS_PER_ITEM        = 16    # comparisons, branches, arithmetic
MEMORY_ACCESSES_PER_ITEM   = 4     # load/store per classification
DATA_MOVEMENT_PER_ITEM     = 2     # transfers between stages
CONVERSIONS_PER_ITEM       = 1     # signal conversion (e.g., ADC sampling)

# Pattern pipeline overhead definitions per overhead_case
# optical_extraction_cost_per_item: encoding and preparing the pattern
# detector_cost_per_item:           reading back the classification result
OVERHEAD_CASES = {
    "low": {
        "optical_extraction_cost_per_item": 3,
        "detector_cost_per_item":           2,
        "description": "Efficient optical layer; low conversion and detector cost",
    },
    "medium": {
        "optical_extraction_cost_per_item": 8,
        "detector_cost_per_item":           5,
        "description": "Moderate optical layer; typical prototype overhead",
    },
    "high": {
        "optical_extraction_cost_per_item": 18,
        "detector_cost_per_item":           12,
        "description": "Expensive optical conversion and high-precision detector",
    },
}

WORKLOAD_SIZES         = [1_000, 10_000, 100_000, 1_000_000]
REDUCTION_FACTORS      = [0.2, 0.4, 0.6, 0.8]

# ---------------------------------------------------------------------------
# Cost computation
# ---------------------------------------------------------------------------

def compute_binary_cost(workload_size):
    """Total cost of baseline sequential binary pipeline."""
    per_item = (BINARY_OPS_PER_ITEM        * BINARY_OP_COST
                + MEMORY_ACCESSES_PER_ITEM * MEMORY_ACCESS_COST
                + DATA_MOVEMENT_PER_ITEM   * DATA_MOVEMENT_COST
                + CONVERSIONS_PER_ITEM     * CONVERSION_COST)
    return workload_size * per_item


def compute_pattern_cost(workload_size, reduction_factor, overhead_case):
    """
    Total cost of pattern-recognition pipeline.

    Reduced binary ops and data movement; plus pattern extraction and detector.
    Memory accesses also reduced proportionally to the reduction factor
    (pattern-based systems avoid many lookup iterations).
    """
    oh = OVERHEAD_CASES[overhead_case]
    extract_cost = oh["optical_extraction_cost_per_item"]
    detect_cost  = oh["detector_cost_per_item"]

    # Reduced operations
    reduced_binary_ops  = BINARY_OPS_PER_ITEM      * reduction_factor
    reduced_mem_accesses = MEMORY_ACCESSES_PER_ITEM * reduction_factor
    reduced_data_movement = DATA_MOVEMENT_PER_ITEM  * reduction_factor
    # Conversions: pattern extraction replaces the digital conversion;
    # cost is now the optical extraction + detector, not the conversion cost.

    per_item = (reduced_binary_ops        * BINARY_OP_COST
                + reduced_mem_accesses    * MEMORY_ACCESS_COST
                + reduced_data_movement   * DATA_MOVEMENT_COST
                + extract_cost
                + detect_cost)

    return workload_size * per_item


def compute_row(workload_size, reduction_factor, overhead_case):
    binary_cost  = compute_binary_cost(workload_size)
    pattern_cost = compute_pattern_cost(workload_size, reduction_factor, overhead_case)
    savings      = binary_cost - pattern_cost
    savings_pct  = 100.0 * savings / binary_cost if binary_cost else 0.0
    break_even   = "yes" if pattern_cost < binary_cost else "no"

    return {
        "workload_size":        workload_size,
        "reduction_factor":     reduction_factor,
        "overhead_case":        overhead_case,
        "binary_cost":          round(binary_cost, 0),
        "pattern_cost":         round(pattern_cost, 0),
        "savings":              round(savings, 0),
        "savings_percent":      round(savings_pct, 2),
        "break_even":           break_even,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_assumptions():
    print("Unit cost assumptions (abstract, not real joules):")
    print("")
    print(f"  binary_op_cost        = {BINARY_OP_COST}")
    print(f"  memory_access_cost    = {MEMORY_ACCESS_COST}")
    print(f"  data_movement_cost    = {DATA_MOVEMENT_COST}")
    print(f"  conversion_cost       = {CONVERSION_COST}")
    print("")
    print("Per-item baseline counts:")
    print(f"  binary ops per item   = {BINARY_OPS_PER_ITEM}")
    print(f"  memory accesses/item  = {MEMORY_ACCESSES_PER_ITEM}")
    print(f"  data movements/item   = {DATA_MOVEMENT_PER_ITEM}")
    print(f"  conversions/item      = {CONVERSIONS_PER_ITEM}")
    print("")
    print("Overhead cases:")
    for case, params in OVERHEAD_CASES.items():
        print(f"  {case:<8}: extract={params['optical_extraction_cost_per_item']:>3}  "
              f"detect={params['detector_cost_per_item']:>3}  "
              f"-- {params['description']}")
    print("")


def print_results_table(results):
    cols = [
        ("workload_size",    12, "Workload"),
        ("reduction_factor",  8, "RedFact"),
        ("overhead_case",    10, "Overhead"),
        ("binary_cost",      14, "Binary cost"),
        ("pattern_cost",     14, "Pattern cost"),
        ("savings_percent",  12, "Savings %"),
        ("break_even",       11, "Break-even"),
    ]
    header = " | ".join(f"{label:<{width}}" for key, width, label in cols)
    sep    = "-+-".join("-" * width for key, width, label in cols)
    print(header)
    print(sep)
    for r in results:
        row = " | ".join(f"{str(r[key]):<{width}}" for key, width, label in cols)
        print(row)


def write_csv(results, path):
    if not results:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = list(results[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  CSV written to: {path}")


# ---------------------------------------------------------------------------
# Summary analysis
# ---------------------------------------------------------------------------

def print_breakeven_summary(results):
    print("")
    print("Break-even analysis summary:")
    print("")
    print("  Pattern recognition achieves lower cost than binary pipeline when:")
    print("  E_OBQC_overhead < (reduction_factor * baseline_savings)")
    print("")

    for overhead_case in OVERHEAD_CASES:
        oh = OVERHEAD_CASES[overhead_case]
        subset = [r for r in results if r["overhead_case"] == overhead_case]
        be_yes = sum(1 for r in subset if r["break_even"] == "yes")
        be_no  = sum(1 for r in subset if r["break_even"] == "no")
        total  = len(subset)
        print(f"  overhead={overhead_case:<8}: break-even in {be_yes}/{total} "
              f"parameter combinations")

    print("")
    print("  Key finding:")
    for overhead_case in OVERHEAD_CASES:
        oh = OVERHEAD_CASES[overhead_case]
        subset = [r for r in results if r["overhead_case"] == overhead_case]
        be_subset = [r for r in subset if r["break_even"] == "yes"]
        if be_subset:
            min_rf  = min(r["reduction_factor"] for r in be_subset)
            min_wl  = min(r["workload_size"] for r in be_subset)
            print(f"    overhead={overhead_case}: break-even requires "
                  f"reduction_factor >= {min_rf} at workload_size >= {min_wl}")
        else:
            print(f"    overhead={overhead_case}: no break-even found in tested range")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    results_dir  = os.path.join(script_dir, "results")
    csv_path     = os.path.join(results_dir, "pattern_vs_binary_operation_cost.csv")

    print("=" * 70)
    print("Pattern Recognition vs Binary Operation Cost Model")
    print("Optical Bead Computing (OBQC)")
    print("=" * 70)
    print("")
    print("DISCLAIMER:")
    print("  This is an abstract operation-cost model, not a hardware benchmark.")
    print("  All cost values are in normalized abstract units, not real joules.")
    print("  Results depend entirely on the assumed cost parameters.")
    print("  This does not prove that OBQC is always more efficient than binary.")
    print("  Pattern recognition helps only for suitable structured workloads")
    print("  where overhead is lower than the savings in downstream operations.")
    print("")

    print_assumptions()

    # Compute all results
    results = []
    for workload_size in WORKLOAD_SIZES:
        for reduction_factor in REDUCTION_FACTORS:
            for overhead_case in OVERHEAD_CASES:
                results.append(compute_row(workload_size, reduction_factor, overhead_case))

    # Print summary table
    print("=" * 70)
    print("Results Table")
    print("=" * 70)
    print("")
    print_results_table(results)

    # Print break-even analysis
    print("")
    print("=" * 70)
    print("Break-Even Analysis")
    print("=" * 70)
    print_breakeven_summary(results)

    # Interpretation
    print("")
    print("=" * 70)
    print("Interpretation")
    print("=" * 70)
    print("")
    print("  The reduction_factor parameter represents how much of the sequential")
    print("  binary processing is avoided by pattern recognition.")
    print("")
    print("  reduction_factor = 0.2 means 20% of binary ops still required (80% saved).")
    print("  reduction_factor = 0.8 means 80% of binary ops still required (20% saved).")
    print("")
    print("  Pattern recognition is beneficial when:")
    print("    (1-reduction_factor) * binary_savings > overhead cost")
    print("")
    print("  For low overhead (efficient optical layer), break-even is achievable")
    print("  even at modest reduction factors and small workload sizes.")
    print("")
    print("  For high overhead (expensive detector/conversion), break-even")
    print("  requires either high reduction factors or large workload sizes.")
    print("")
    print("  These thresholds are what real hardware experiments should measure.")
    print("")

    # Write CSV
    write_csv(results, csv_path)
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
