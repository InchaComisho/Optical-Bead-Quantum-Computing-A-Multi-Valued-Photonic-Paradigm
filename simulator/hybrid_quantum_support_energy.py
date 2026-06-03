"""
hybrid_quantum_support_energy.py
=================================
Toy system-level energy model for hybrid quantum computing support systems.

PURPOSE
-------
This is NOT a physical simulation.
This is NOT a quantum computation model.
This is a toy system-level energy model that tests whether an OBQC-like
auxiliary pattern-recognition layer could reduce the auxiliary energy
components of a hybrid quantum computing system.

The model keeps cryogenic energy (E_cryo) unchanged by default.
It does NOT claim that OBQC eliminates cryogenic cooling requirements.

ENERGY DECOMPOSITION
--------------------
E_total = E_quantum_core + E_cryo + E_control + E_readout
        + E_classical_processing + E_data_movement

OBQC targets E_aux = E_control + E_readout + E_classical_processing
                   + E_data_movement

E_aux_OBQC = alpha_control * E_control
           + alpha_readout * E_readout
           + alpha_processing * E_classical_processing
           + alpha_data * E_data_movement
           + E_OBQC_layer

Net benefit condition:
    E_OBQC_layer < sum_i (1 - alpha_i) * E_i_baseline

SCENARIOS
---------
conservative, moderate, optimistic, high_OBQC_overhead, no_benefit

All energy values are in normalized units (not real joules).
Default values represent a rough relative scale for a mid-scale
quantum computing system.

OUTPUT
------
- Printed table (ASCII)
- CSV: simulator/results/hybrid_quantum_support_energy.csv

Usage:
    python hybrid_quantum_support_energy.py

No external dependencies required.
"""

import csv
import os
import math

# ---------------------------------------------------------------------------
# Baseline energy values (normalized units, not real joules)
# ---------------------------------------------------------------------------
# These represent relative scale, not absolute measurements.
# E_cryo is deliberately large to reflect that cryogenic infrastructure
# dominates total system energy in superconducting quantum computers.

BASELINE = {
    "E_quantum_core":        1.0,
    "E_cryo":              100.0,
    "E_control":            20.0,
    "E_readout":            20.0,
    "E_classical_processing": 30.0,
    "E_data_movement":      40.0,
}

# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------
# alpha_* < 1.0 means that component's energy is REDUCED by the OBQC layer.
# alpha_* = 1.0 means no change.
# E_OBQC_layer is the overhead energy consumed by the optical layer itself.

SCENARIOS = [
    {
        "name":                "conservative",
        "description":         "Small auxiliary reductions; low OBQC overhead",
        "alpha_control":        0.95,
        "alpha_readout":        0.90,
        "alpha_processing":     0.85,
        "alpha_data":           0.90,
        "E_OBQC_layer":        10.0,
    },
    {
        "name":                "moderate",
        "description":         "Moderate auxiliary reductions; moderate overhead",
        "alpha_control":        0.85,
        "alpha_readout":        0.75,
        "alpha_processing":     0.65,
        "alpha_data":           0.70,
        "E_OBQC_layer":        12.0,
    },
    {
        "name":                "optimistic",
        "description":         "Significant auxiliary reductions; OBQC scales well",
        "alpha_control":        0.70,
        "alpha_readout":        0.55,
        "alpha_processing":     0.40,
        "alpha_data":           0.50,
        "E_OBQC_layer":        15.0,
    },
    {
        "name":                "high_OBQC_overhead",
        "description":         "Decent reductions but OBQC layer costs too much",
        "alpha_control":        0.75,
        "alpha_readout":        0.65,
        "alpha_processing":     0.55,
        "alpha_data":           0.60,
        "E_OBQC_layer":        45.0,
    },
    {
        "name":                "no_benefit",
        "description":         "OBQC provides no reduction but still has overhead",
        "alpha_control":        1.00,
        "alpha_readout":        1.00,
        "alpha_processing":     1.00,
        "alpha_data":           1.00,
        "E_OBQC_layer":        10.0,
    },
]

# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------

def compute_metrics(baseline, scenario):
    """
    Compute all energy metrics for one scenario.

    Returns a dict of metrics.
    """
    B = baseline
    S = scenario

    # Baseline totals
    baseline_aux = (B["E_control"] + B["E_readout"]
                    + B["E_classical_processing"] + B["E_data_movement"])
    baseline_total = (B["E_quantum_core"] + B["E_cryo"] + baseline_aux)

    # OBQC-assisted auxiliary components
    obqc_control    = S["alpha_control"]    * B["E_control"]
    obqc_readout    = S["alpha_readout"]    * B["E_readout"]
    obqc_processing = S["alpha_processing"] * B["E_classical_processing"]
    obqc_data       = S["alpha_data"]       * B["E_data_movement"]
    obqc_layer      = S["E_OBQC_layer"]

    obqc_aux   = obqc_control + obqc_readout + obqc_processing + obqc_data + obqc_layer
    obqc_total = B["E_quantum_core"] + B["E_cryo"] + obqc_aux

    # Savings
    total_savings         = baseline_total - obqc_total
    total_savings_pct     = 100.0 * total_savings / baseline_total
    aux_savings_pct       = 100.0 * (baseline_aux - obqc_aux) / baseline_aux if baseline_aux else 0.0

    # Cryo fraction
    cryo_fraction_before  = 100.0 * B["E_cryo"] / baseline_total
    cryo_fraction_after   = 100.0 * B["E_cryo"] / obqc_total

    # Net benefit: OBQC is useful only if aux energy decreases
    net_benefit = obqc_aux < baseline_aux

    return {
        "scenario":               S["name"],
        "description":            S["description"],
        "baseline_total":         round(baseline_total, 3),
        "obqc_total":             round(obqc_total, 3),
        "total_savings":          round(total_savings, 3),
        "total_savings_percent":  round(total_savings_pct, 2),
        "auxiliary_baseline":     round(baseline_aux, 3),
        "auxiliary_obqc":         round(obqc_aux, 3),
        "auxiliary_savings_percent": round(aux_savings_pct, 2),
        "cryo_fraction_before":   round(cryo_fraction_before, 2),
        "cryo_fraction_after":    round(cryo_fraction_after, 2),
        "net_benefit":            "yes" if net_benefit else "no",
        # detailed components
        "E_quantum_core":         round(B["E_quantum_core"], 3),
        "E_cryo":                 round(B["E_cryo"], 3),
        "E_control_baseline":     round(B["E_control"], 3),
        "E_readout_baseline":     round(B["E_readout"], 3),
        "E_processing_baseline":  round(B["E_classical_processing"], 3),
        "E_data_baseline":        round(B["E_data_movement"], 3),
        "E_control_obqc":         round(obqc_control, 3),
        "E_readout_obqc":         round(obqc_readout, 3),
        "E_processing_obqc":      round(obqc_processing, 3),
        "E_data_obqc":            round(obqc_data, 3),
        "E_OBQC_layer":           round(obqc_layer, 3),
        "alpha_control":          S["alpha_control"],
        "alpha_readout":          S["alpha_readout"],
        "alpha_processing":       S["alpha_processing"],
        "alpha_data":             S["alpha_data"],
    }


# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def print_baseline(baseline):
    print("Baseline energy components (normalized units):")
    print("")
    for k, v in baseline.items():
        print(f"  {k:<30} {v:>8.1f}")
    total = sum(baseline.values())
    aux   = (baseline["E_control"] + baseline["E_readout"]
             + baseline["E_classical_processing"] + baseline["E_data_movement"])
    print(f"  {'E_aux (sum)':<30} {aux:>8.1f}")
    print(f"  {'E_total (sum)':<30} {total:>8.1f}")
    print("")
    print("  NOTE: E_cryo is kept UNCHANGED in all scenarios.")
    print("  OBQC does not claim to reduce cryogenic cooling requirements.")
    print("")


def print_scenario_table(results):
    cols = [
        ("scenario",              18, "Scenario"),
        ("baseline_total",        14, "Baseline tot"),
        ("obqc_total",            12, "OBQC tot"),
        ("total_savings_percent", 13, "Tot save %"),
        ("auxiliary_baseline",    12, "Aux base"),
        ("auxiliary_obqc",        12, "Aux OBQC"),
        ("auxiliary_savings_percent", 12, "Aux save %"),
        ("cryo_fraction_before",  14, "Cryo% before"),
        ("cryo_fraction_after",   13, "Cryo% after"),
        ("net_benefit",           11, "Net benefit"),
    ]

    header = " | ".join(f"{label:<{width}}" for key, width, label in cols)
    sep    = "-+-".join("-" * width for key, width, label in cols)
    print(header)
    print(sep)
    for r in results:
        row = " | ".join(f"{str(r[key]):<{width}}" for key, width, label in cols)
        print(row)


def print_component_table(results):
    print("")
    print("Per-scenario energy component breakdown:")
    print("")
    for r in results:
        print(f"  Scenario: {r['scenario']}")
        print(f"    {r['description']}")
        print(f"    alpha: control={r['alpha_control']}  readout={r['alpha_readout']}"
              f"  processing={r['alpha_processing']}  data={r['alpha_data']}")
        print(f"    E_OBQC_layer = {r['E_OBQC_layer']}")
        print(f"    Component comparison (baseline -> OBQC):")
        pairs = [
            ("E_quantum_core", "E_quantum_core", "quantum core (unchanged)"),
            ("E_cryo",         "E_cryo",         "cryo (unchanged)"),
            ("E_control_baseline", "E_control_obqc", "control"),
            ("E_readout_baseline", "E_readout_obqc", "readout"),
            ("E_processing_baseline", "E_processing_obqc", "classical processing"),
            ("E_data_baseline", "E_data_obqc", "data movement"),
        ]
        for b_key, o_key, label in pairs:
            b_val = r[b_key]
            o_val = r[o_key]
            pct   = 100.0 * (o_val - b_val) / b_val if b_val else 0.0
            print(f"      {label:<28} {b_val:>6.1f} -> {o_val:>6.1f}  ({pct:+.1f}%)")
        print(f"      {'OBQC layer (new cost)':<28}  --    ->  {r['E_OBQC_layer']:>5.1f}")
        print(f"    Net benefit: {r['net_benefit']}")
        print(f"    Total savings: {r['total_savings']} ({r['total_savings_percent']}%)")
        print(f"    Aux savings: {r['auxiliary_savings_percent']}%")
        print("")


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
# Main
# ---------------------------------------------------------------------------

def main():
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    results_dir  = os.path.join(script_dir, "results")
    csv_path     = os.path.join(results_dir, "hybrid_quantum_support_energy.csv")

    print("=" * 70)
    print("Hybrid Quantum Support Layer - Toy Energy Model")
    print("Optical Bead Computing (OBQC)")
    print("=" * 70)
    print("")
    print("DISCLAIMER:")
    print("  This is a toy system-level energy model, not a physical simulation.")
    print("  Energy values are in normalized units, not real joules.")
    print("  This model keeps E_cryo unchanged by default.")
    print("  It does NOT claim that OBQC eliminates cryogenic cooling.")
    print("  Results depend entirely on the assumed alpha values and overhead.")
    print("  See docs/hybrid-quantum-support-layer.md for full explanation.")
    print("")

    # Print baseline
    print_baseline(BASELINE)

    # Compute results
    results = [compute_metrics(BASELINE, s) for s in SCENARIOS]

    # Print scenario summary table
    print("=" * 70)
    print("Scenario Summary")
    print("=" * 70)
    print("")
    print_scenario_table(results)
    print("")

    # Print component breakdown
    print("=" * 70)
    print("Component Breakdown")
    print("=" * 70)
    print_component_table(results)

    # Interpretation
    print("=" * 70)
    print("Interpretation Notes")
    print("=" * 70)
    print("")
    print("  1. E_cryo dominates total energy in all scenarios.")
    print("     Even a 50% aux reduction leaves >85% of total energy unchanged.")
    print("")
    print("  2. Net benefit (aux energy actually decreases) depends on")
    print("     E_OBQC_layer being smaller than the sum of aux savings.")
    print("     high_OBQC_overhead and no_benefit scenarios show net_benefit=no.")
    print("")
    print("  3. The cryo fraction of total energy INCREASES when aux energy")
    print("     decreases -- confirming that cryogenic cost is not reduced.")
    print("")
    print("  4. Practical value of OBQC depends on:")
    print("     - How accurately alpha values reflect real workloads")
    print("     - Whether OBQC overhead can be kept below the aux savings")
    print("     - Latency, accuracy, and integration constraints not modeled here")
    print("")
    print("  See docs/hybrid-quantum-support-layer.md for full discussion.")
    print("")

    # Write CSV
    write_csv(results, csv_path)
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
