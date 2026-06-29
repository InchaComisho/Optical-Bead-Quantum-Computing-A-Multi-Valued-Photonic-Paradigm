#!/usr/bin/env python3
"""
pattern_vs_binary_flash_emulator.py
=====================================
Conceptual emulator: SCD / RGB-white optical bead pattern processing
vs binary sequential and indexed-lookup computation.

IMPORTANT FRAMING
-----------------
  - This is a TOY EMULATOR using a CONFIGURABLE CONCEPTUAL ENERGY-LATENCY MODEL.
  - All energy and latency values are RELATIVE UNITS under stated assumptions.
  - NOT measured hardware performance.
  - NOT a claim of quantum advantage.
  - NOT a claim of guaranteed superiority over binary computers.
  - Results depend entirely on the energy model parameters.
  - A SENSITIVITY ANALYSIS shows when each approach is favorable and when not.
  - This is a FALSIFIABLE MODEL: change parameters, results change accordingly.

Task: classify one of 40 symbols from a noisy optical or binary input.

Binary baseline A (sequential search):
  - 6-bit binary representation of 40 symbols
  - Compares candidate words sequentially, bit-by-bit
  - Average case: N/2 iterations = 20

Binary baseline B (indexed lookup):
  - O(1) table lookup using 6-bit code as index
  - Optimized digital baseline to prevent unfair comparison

Optical model (SCD / RGB-white):
  - 4 color-layer markers (R, G, B, White) x 10 SCD digits = 40 symbols
  - SCD digit: (H, L4, L3, L2, L1) thermometer-coded 5-bead pattern
  - Parallel readout: all 9 channels (4 marker + 5 bead) read simultaneously
  - Noise: Gaussian, RGB crosstalk, ambient offset, intensity drift

Usage:
    python pattern_vs_binary_flash_emulator.py
    python pattern_vs_binary_flash_emulator.py --trials 5000 --sigma 0.05
"""

import argparse
import csv
import math
import os
import random
import sys

# =============================================================================
# CONFIGURABLE PARAMETERS
# All energy values are RELATIVE UNITS, not real measured power.
# Change these to explore the sensitivity of results to assumptions.
# =============================================================================

RANDOM_SEED                = 42
N_TRIALS                   = 10000
ALPHABET_SIZE              = 40        # 4 layers x 10 SCD digits
BINARY_BITS                = 6         # ceil(log2(40)) = 6
SCD_BEAD_POSITIONS         = 5         # H, L4, L3, L2, L1
MARKER_CHANNELS            = 4         # R, G, B, White
N_LAYERS                   = 4
N_DIGITS                   = 10

# Binary energy model (relative units per operation)
BINARY_BIT_COMPARE_ENERGY  = 1.0      # per bit comparison
BINARY_MEMORY_READ_ENERGY  = 2.0      # per word memory read
BINARY_CONTROL_STEP_ENERGY = 0.5      # per loop/branch step

# Optical energy model (relative units per element)
LED_ON_ENERGY              = 1.5      # per active LED bead (emission)
CMOS_PIXEL_READ_ENERGY     = 0.8      # per CMOS channel read
OPTICAL_THRESHOLD_ENERGY   = 0.4      # per threshold comparison
VALIDITY_CHECK_ENERGY      = 0.5      # per SCD thermometer validity check

# Noise model
SIGMA_SENSOR               = 0.08     # Gaussian noise std dev per channel
RGB_CROSSTALK              = 0.05     # fractional bleed between color channels
AMBIENT_OFFSET             = 0.03     # constant ambient light offset
INTENSITY_DRIFT_RATE       = 1e-5     # per-trial slow drift (caps ~0.10 at 10k trials)
THRESHOLD_MARGIN           = 0.50     # bead-on threshold

# Sequential search: expected fraction of alphabet scanned before match
BINARY_SEQ_FRACTION        = 0.5      # 0.5 = average case; 1.0 = worst case

# =============================================================================
# SCD ALPHABET
# =============================================================================

LAYERS = ["R", "G", "B", "W"]

# True 4-channel (R, G, B, W) marker intensities per layer
LAYER_SIGNALS = {
    0: (1.0, 0.0, 0.0, 0.0),   # R
    1: (0.0, 1.0, 0.0, 0.0),   # G
    2: (0.0, 0.0, 1.0, 0.0),   # B
    3: (0.0, 0.0, 0.0, 1.0),   # White
}


def scd_encode_digit(digit):
    """Encode decimal digit 0-9 as SCD (H, L4, L3, L2, L1) bead pattern."""
    assert 0 <= digit <= 9, f"Invalid digit: {digit}"
    H  = 1 if digit >= 5 else 0
    e  = digit % 5
    L4 = 1 if e >= 4 else 0
    L3 = 1 if e >= 3 else 0
    L2 = 1 if e >= 2 else 0
    L1 = 1 if e >= 1 else 0
    return (H, L4, L3, L2, L1)


_VALID_EARTH_PATTERNS = {(0,0,0,0), (0,0,0,1), (0,0,1,1), (0,1,1,1), (1,1,1,1)}


def scd_decode_beads(H, L4, L3, L2, L1):
    """
    Decode SCD bead pattern to (digit, is_valid).
    is_valid = False signals a DETECTED error (invalid thermometer code).
    """
    earth_pattern = (L4, L3, L2, L1)
    is_valid = earth_pattern in _VALID_EARTH_PATTERNS
    digit = 5 * H + (L4 + L3 + L2 + L1)
    return digit, is_valid


def build_alphabet():
    """
    Build 40-symbol alphabet (4 layers x 10 SCD digits).
    Returns list of symbol dicts, ordered by symbol index.
    """
    symbols = []
    for layer_idx, layer_name in enumerate(LAYERS):
        for digit in range(N_DIGITS):
            sym_idx = layer_idx * N_DIGITS + digit
            if sym_idx >= ALPHABET_SIZE:
                break
            symbols.append({
                "idx":        sym_idx,
                "layer_idx":  layer_idx,
                "layer_name": layer_name,
                "digit":      digit,
                "scd":        scd_encode_digit(digit),
            })
    return symbols


# =============================================================================
# BINARY SIMULATION
# =============================================================================

def simulate_binary_sequential(true_idx):
    """
    Model sequential bit-by-bit symbol search.
    Returns per-trial metrics dict.
    """
    n_iters = math.ceil(BINARY_SEQ_FRACTION * ALPHABET_SIZE)  # average case
    bit_compares   = n_iters * BINARY_BITS
    mem_reads      = n_iters
    control_steps  = n_iters

    energy = (
        bit_compares  * BINARY_BIT_COMPARE_ENERGY  +
        mem_reads     * BINARY_MEMORY_READ_ENERGY  +
        control_steps * BINARY_CONTROL_STEP_ENERGY
    )
    # Latency: serial iterations, each costing (bits + 1 control) steps
    latency = n_iters * (BINARY_BITS + 1)

    return {
        "method":              "binary_sequential",
        "bit_comparisons":     bit_compares,
        "memory_reads":        mem_reads,
        "control_steps":       control_steps,
        "active_beads":        0,
        "cmos_reads":          0,
        "threshold_compares":  0,
        "validity_checks":     0,
        "energy":              energy,
        "latency":             latency,
        "detected_error":      False,
        "silent_error":        False,
        "any_error":           False,
    }


def simulate_binary_indexed(true_idx):
    """
    Model O(1) indexed lookup (optimized digital baseline).
    Returns per-trial metrics dict.
    """
    bit_compares  = BINARY_BITS   # verify the fetched entry
    mem_reads     = 1
    control_steps = 1

    energy = (
        bit_compares  * BINARY_BIT_COMPARE_ENERGY  +
        mem_reads     * BINARY_MEMORY_READ_ENERGY  +
        control_steps * BINARY_CONTROL_STEP_ENERGY
    )
    latency = 2  # lookup + verify

    return {
        "method":              "binary_indexed",
        "bit_comparisons":     bit_compares,
        "memory_reads":        mem_reads,
        "control_steps":       control_steps,
        "active_beads":        0,
        "cmos_reads":          0,
        "threshold_compares":  0,
        "validity_checks":     0,
        "energy":              energy,
        "latency":             latency,
        "detected_error":      False,
        "silent_error":        False,
        "any_error":           False,
    }


# =============================================================================
# OPTICAL NOISE MODEL
# =============================================================================

def _argmax4(t):
    """Return index of maximum in a 4-tuple."""
    best, best_i = t[0], 0
    for i in range(1, 4):
        if t[i] > best:
            best, best_i = t[i], i
    return best_i


def add_marker_noise(true_signal_4ch, trial_idx):
    """
    Add noise to 4-channel marker signal.
    Noise sources: Gaussian, RGB crosstalk, ambient offset, intensity drift.
    """
    r, g, b, w = true_signal_4ch

    # Crosstalk: each channel picks up a fraction of adjacent channels
    r2 = r + RGB_CROSSTALK * (g + b + w * 0.3)
    g2 = g + RGB_CROSSTALK * (r + b + w * 0.3)
    b2 = b + RGB_CROSSTALK * (r + g + w * 0.3)
    w2 = w + RGB_CROSSTALK * (r + g + b) * 0.2

    # Gaussian noise per channel
    r2 += random.gauss(0, SIGMA_SENSOR)
    g2 += random.gauss(0, SIGMA_SENSOR)
    b2 += random.gauss(0, SIGMA_SENSOR)
    w2 += random.gauss(0, SIGMA_SENSOR)

    # Ambient offset and drift
    offset = AMBIENT_OFFSET + INTENSITY_DRIFT_RATE * trial_idx
    return (r2 + offset, g2 + offset, b2 + offset, w2 + offset)


def add_bead_noise(bead_val, trial_idx):
    """Add Gaussian noise + ambient offset + drift to a single bead reading."""
    return (bead_val
            + AMBIENT_OFFSET
            + random.gauss(0, SIGMA_SENSOR)
            + INTENSITY_DRIFT_RATE * trial_idx)


# =============================================================================
# OPTICAL SIMULATION
# =============================================================================

def simulate_optical(symbol, trial_idx):
    """
    Model SCD/RGB-white parallel pattern decoding.

    Latency model (3 steps, parallel):
      Step 1 — parallel readout: all 9 channels (4 marker + 5 bead) captured
      Step 2 — threshold pass: vectorized comparison against threshold
      Step 3 — SCD validity check and digit decode

    Energy counted per physical operation:
      - LED active beads (emission cost)
      - CMOS reads (sensor readout cost)
      - Threshold comparisons (analog/digital comparison cost)
      - Validity check (logic cost)

    Returns per-trial metrics dict.
    """
    layer_idx = symbol["layer_idx"]
    digit     = symbol["digit"]
    scd       = symbol["scd"]         # (H, L4, L3, L2, L1), each 0 or 1

    # --- Physical operation counts ---
    active_beads        = 1 + sum(scd)          # 1 marker LED + active SCD beads
    cmos_reads          = MARKER_CHANNELS + SCD_BEAD_POSITIONS   # 4 + 5 = 9
    threshold_compares  = MARKER_CHANNELS + SCD_BEAD_POSITIONS   # 9
    validity_checks     = 1

    energy = (
        active_beads       * LED_ON_ENERGY          +
        cmos_reads         * CMOS_PIXEL_READ_ENERGY +
        threshold_compares * OPTICAL_THRESHOLD_ENERGY +
        validity_checks    * VALIDITY_CHECK_ENERGY
    )
    latency = 3   # parallel readout + threshold + validity (see docstring)

    # --- Noise simulation ---
    # Marker detection
    noisy_marker  = add_marker_noise(LAYER_SIGNALS[layer_idx], trial_idx)
    detected_layer = _argmax4(noisy_marker)
    layer_correct  = (detected_layer == layer_idx)

    # Bead detection
    noisy_beads   = tuple(add_bead_noise(float(b), trial_idx) for b in scd)
    thresholded   = tuple(1 if v > THRESHOLD_MARGIN else 0 for v in noisy_beads)

    H_d, L4_d, L3_d, L2_d, L1_d = thresholded
    decoded_digit, is_valid = scd_decode_beads(H_d, L4_d, L3_d, L2_d, L1_d)

    # Error classification
    if not is_valid:
        # Thermometer pattern broken → detected error; we know recognition failed
        detected_err = True
        silent_err   = False
    elif not layer_correct:
        # Wrong layer detected but SCD pattern happened to be valid → silent error
        detected_err = False
        silent_err   = True
    elif decoded_digit != digit:
        # Valid SCD, correct layer, but digit misread → silent error
        detected_err = False
        silent_err   = True
    else:
        detected_err = False
        silent_err   = False

    any_error = detected_err or silent_err

    return {
        "method":              "optical_scd",
        "bit_comparisons":     0,
        "memory_reads":        0,
        "control_steps":       0,
        "active_beads":        active_beads,
        "cmos_reads":          cmos_reads,
        "threshold_compares":  threshold_compares,
        "validity_checks":     validity_checks,
        "energy":              energy,
        "latency":             latency,
        "detected_error":      detected_err,
        "silent_error":        silent_err,
        "any_error":           any_error,
    }


# =============================================================================
# AGGREGATION HELPERS
# =============================================================================

def aggregate(results):
    """Compute mean metrics across a list of trial result dicts."""
    n = len(results)
    if n == 0:
        return {}
    keys = [k for k in results[0] if k != "method"]
    agg = {"method": results[0]["method"], "n_trials": n}
    for k in keys:
        vals = [r[k] for r in results]
        if isinstance(vals[0], bool):
            agg[k + "_rate"] = sum(1 for v in vals if v) / n
        elif isinstance(vals[0], (int, float)):
            agg[k + "_mean"] = sum(vals) / n
    return agg


# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

SENSITIVITY_SCENARIOS = [
    {
        "name":                  "optimistic_optical",
        "label":                 "Optimistic optical (low overhead)",
        "LED_ON_ENERGY":         0.8,
        "CMOS_PIXEL_READ_ENERGY":0.4,
        "OPTICAL_THRESHOLD_ENERGY": 0.2,
        "VALIDITY_CHECK_ENERGY": 0.2,
        "SIGMA_SENSOR":          0.05,
    },
    {
        "name":                  "moderate_optical",
        "label":                 "Moderate optical (default params)",
        "LED_ON_ENERGY":         LED_ON_ENERGY,
        "CMOS_PIXEL_READ_ENERGY":CMOS_PIXEL_READ_ENERGY,
        "OPTICAL_THRESHOLD_ENERGY": OPTICAL_THRESHOLD_ENERGY,
        "VALIDITY_CHECK_ENERGY": VALIDITY_CHECK_ENERGY,
        "SIGMA_SENSOR":          SIGMA_SENSOR,
    },
    {
        "name":                  "conservative_optical",
        "label":                 "Conservative optical (higher overhead)",
        "LED_ON_ENERGY":         2.5,
        "CMOS_PIXEL_READ_ENERGY":1.5,
        "OPTICAL_THRESHOLD_ENERGY": 0.8,
        "VALIDITY_CHECK_ENERGY": 1.0,
        "SIGMA_SENSOR":          0.10,
    },
    {
        "name":                  "high_cmos_read",
        "label":                 "High CMOS read overhead",
        "LED_ON_ENERGY":         LED_ON_ENERGY,
        "CMOS_PIXEL_READ_ENERGY":3.0,
        "OPTICAL_THRESHOLD_ENERGY": OPTICAL_THRESHOLD_ENERGY,
        "VALIDITY_CHECK_ENERGY": VALIDITY_CHECK_ENERGY,
        "SIGMA_SENSOR":          SIGMA_SENSOR,
    },
    {
        "name":                  "no_benefit",
        "label":                 "No-benefit case (high cost + high noise)",
        "LED_ON_ENERGY":         4.0,
        "CMOS_PIXEL_READ_ENERGY":4.0,
        "OPTICAL_THRESHOLD_ENERGY": 2.0,
        "VALIDITY_CHECK_ENERGY": 2.0,
        "SIGMA_SENSOR":          0.18,
    },
]


def compute_optical_energy_scenario(sc, avg_active_beads, cmos_reads,
                                     thresh_compares, validity_checks):
    """Compute optical energy for a sensitivity scenario."""
    return (
        avg_active_beads  * sc["LED_ON_ENERGY"]            +
        cmos_reads        * sc["CMOS_PIXEL_READ_ENERGY"]   +
        thresh_compares   * sc["OPTICAL_THRESHOLD_ENERGY"] +
        validity_checks   * sc["VALIDITY_CHECK_ENERGY"]
    )


def compute_error_rate_scenario(sigma, alphabet, n_sample=500):
    """
    Estimate optical error rate for a given sigma using a small quick sample.
    Resets and restores global SIGMA_SENSOR for this call only.
    """
    global SIGMA_SENSOR
    old_sigma = SIGMA_SENSOR
    SIGMA_SENSOR = sigma
    errors = 0
    sample = random.choices(alphabet, k=n_sample)
    for i, sym in enumerate(sample):
        r = simulate_optical(sym, i)
        if r["any_error"]:
            errors += 1
    SIGMA_SENSOR = old_sigma
    return errors / n_sample


# =============================================================================
# OUTPUT HELPERS
# =============================================================================

def _hr(ch="-", n=78):
    return ch * n


def _col(s, w):
    """Left-align string in column of width w."""
    return str(s)[:w].ljust(w)


def _rcol(s, w):
    """Right-align value in column of width w."""
    return str(s)[:w].rjust(w)


def print_header(title):
    print()
    print(_hr("="))
    print(f"  {title}")
    print(_hr("="))


def print_section(title):
    print()
    print(_hr("-"))
    print(f"  {title}")
    print(_hr("-"))


# =============================================================================
# MAIN SIMULATION
# =============================================================================

def run_simulation(n_trials, alphabet):
    """
    Run n_trials of all three methods and collect raw results.
    Returns (seq_results, idx_results, opt_results).
    """
    seq_results = []
    idx_results = []
    opt_results = []

    for i in range(n_trials):
        sym = alphabet[i % ALPHABET_SIZE]   # cycle through all symbols evenly
        seq_results.append(simulate_binary_sequential(sym["idx"]))
        idx_results.append(simulate_binary_indexed(sym["idx"]))
        opt_results.append(simulate_optical(sym, i))

    return seq_results, idx_results, opt_results


def run_sensitivity_analysis(alphabet, n_sample=500):
    """
    For each sensitivity scenario, compute optical energy and error rate
    vs the two binary baselines (which don't change).
    Returns list of scenario result dicts.
    """
    # Fixed binary reference values (no noise, deterministic)
    n_iters_seq  = math.ceil(BINARY_SEQ_FRACTION * ALPHABET_SIZE)
    energy_seq   = (n_iters_seq * BINARY_BITS   * BINARY_BIT_COMPARE_ENERGY +
                    n_iters_seq                  * BINARY_MEMORY_READ_ENERGY +
                    n_iters_seq                  * BINARY_CONTROL_STEP_ENERGY)
    energy_idx   = (BINARY_BITS                  * BINARY_BIT_COMPARE_ENERGY +
                    1                            * BINARY_MEMORY_READ_ENERGY +
                    1                            * BINARY_CONTROL_STEP_ENERGY)

    # Average optical physical counts (from alphabet statistics)
    avg_active_beads = sum(1 + sum(s["scd"]) for s in alphabet) / len(alphabet)
    cmos_reads       = MARKER_CHANNELS + SCD_BEAD_POSITIONS
    thresh_compares  = MARKER_CHANNELS + SCD_BEAD_POSITIONS
    validity_checks  = 1

    rows = []
    for sc in SENSITIVITY_SCENARIOS:
        opt_energy   = compute_optical_energy_scenario(
            sc, avg_active_beads, cmos_reads, thresh_compares, validity_checks)
        err_rate     = compute_error_rate_scenario(sc["SIGMA_SENSOR"], alphabet, n_sample)
        vs_seq       = (energy_seq  - opt_energy) / energy_seq   * 100
        vs_idx       = (energy_idx  - opt_energy) / energy_idx   * 100
        favorable    = "optical" if opt_energy < energy_idx else "binary_indexed"
        rows.append({
            "scenario":       sc["name"],
            "label":          sc["label"],
            "opt_energy":     opt_energy,
            "seq_energy":     energy_seq,
            "idx_energy":     energy_idx,
            "vs_seq_pct":     vs_seq,
            "vs_idx_pct":     vs_idx,
            "error_rate":     err_rate,
            "favorable":      favorable,
        })
    return rows


# =============================================================================
# REPORT
# =============================================================================

def print_main_results(agg_seq, agg_idx, agg_opt, n_trials):
    print_header("Pattern vs Binary Flash Emulator  --  Conceptual Energy-Latency Model")

    print("""
  FRAMING NOTICE
  --------------
  All values below are RELATIVE UNITS under configurable assumptions.
  This is NOT measured hardware performance.
  This is NOT a claim of quantum advantage or guaranteed superiority
  of optical bead computing over binary computers.
  Results change when model parameters change (see sensitivity analysis).
""")

    print_section("Configuration")
    print(f"  Trials            : {n_trials:,}")
    print(f"  Alphabet size     : {ALPHABET_SIZE}  (4 layers x 10 SCD digits)")
    print(f"  Binary bits       : {BINARY_BITS}  (ceil(log2(40)) = 6)")
    print(f"  SCD bead positions: {SCD_BEAD_POSITIONS}  (H, L4, L3, L2, L1)")
    print(f"  Marker channels   : {MARKER_CHANNELS}  (R, G, B, White)")
    print(f"  Sensor noise sigma: {SIGMA_SENSOR}")
    print(f"  RGB crosstalk     : {RGB_CROSSTALK}")
    print(f"  Ambient offset    : {AMBIENT_OFFSET}")
    print(f"  Threshold margin  : {THRESHOLD_MARGIN}")
    print()
    print(f"  Binary energy model (relative units):")
    print(f"    bit compare  : {BINARY_BIT_COMPARE_ENERGY}")
    print(f"    memory read  : {BINARY_MEMORY_READ_ENERGY}")
    print(f"    control step : {BINARY_CONTROL_STEP_ENERGY}")
    print()
    print(f"  Optical energy model (relative units):")
    print(f"    LED bead on  : {LED_ON_ENERGY}")
    print(f"    CMOS read    : {CMOS_PIXEL_READ_ENERGY}")
    print(f"    threshold cmp: {OPTICAL_THRESHOLD_ENERGY}")
    print(f"    validity chk : {VALIDITY_CHECK_ENERGY}")

    print_section("Per-Symbol Operation Counts (mean over trials)")

    hdr = (f"  {'Metric':<30}  {'Bin-Sequential':>16}  "
           f"{'Bin-Indexed':>14}  {'Optical-SCD':>14}")
    print(hdr)
    print(f"  {_hr('-', 76)}")

    def row(label, key_seq, key_idx, key_opt, fmt=".1f"):
        v_seq = agg_seq.get(key_seq, 0)
        v_idx = agg_idx.get(key_idx, 0)
        v_opt = agg_opt.get(key_opt, 0)
        fs = f"{{:{fmt}}}"
        print(f"  {label:<30}  {fs.format(v_seq):>16}  "
              f"{fs.format(v_idx):>14}  {fs.format(v_opt):>14}")

    row("Bit comparisons (mean)",
        "bit_comparisons_mean", "bit_comparisons_mean", "bit_comparisons_mean")
    row("Memory reads (mean)",
        "memory_reads_mean", "memory_reads_mean", "memory_reads_mean")
    row("Control steps (mean)",
        "control_steps_mean", "control_steps_mean", "control_steps_mean")
    row("Active LED beads (mean)",
        "active_beads_mean", "active_beads_mean", "active_beads_mean")
    row("CMOS pixel reads (mean)",
        "cmos_reads_mean", "cmos_reads_mean", "cmos_reads_mean")
    row("Threshold comparisons (mean)",
        "threshold_compares_mean", "threshold_compares_mean", "threshold_compares_mean")
    row("Validity checks (mean)",
        "validity_checks_mean", "validity_checks_mean", "validity_checks_mean")

    print_section("Energy and Latency (mean over trials, relative units)")

    hdr2 = (f"  {'Metric':<30}  {'Bin-Sequential':>16}  "
            f"{'Bin-Indexed':>14}  {'Optical-SCD':>14}")
    print(hdr2)
    print(f"  {_hr('-', 76)}")

    e_seq = agg_seq.get("energy_mean", 0)
    e_idx = agg_idx.get("energy_mean", 0)
    e_opt = agg_opt.get("energy_mean", 0)
    l_seq = agg_seq.get("latency_mean", 0)
    l_idx = agg_idx.get("latency_mean", 0)
    l_opt = agg_opt.get("latency_mean", 0)

    print(f"  {'Energy (rel. units, mean)':<30}  {e_seq:>16.2f}  "
          f"{e_idx:>14.2f}  {e_opt:>14.2f}")
    print(f"  {'Latency (steps, mean)':<30}  {l_seq:>16.1f}  "
          f"{l_idx:>14.1f}  {l_opt:>14.1f}")

    def pct(a, b):
        if b == 0:
            return "N/A"
        return f"{(b - a) / b * 100:+.1f}%"

    print()
    print(f"  Energy vs binary-sequential : optical {pct(e_opt, e_seq)}")
    print(f"  Energy vs binary-indexed    : optical {pct(e_opt, e_idx)}")
    print(f"  Latency vs binary-sequential: optical {pct(l_opt, l_seq)}")
    print(f"  Latency vs binary-indexed   : optical {pct(l_opt, l_idx)}")

    print_section("Error Rates (optical only; binary modeled as error-free)")

    det_rate    = agg_opt.get("detected_error_rate", 0)
    silent_rate = agg_opt.get("silent_error_rate", 0)
    any_rate    = agg_opt.get("any_error_rate", 0)

    print(f"  Detected errors (invalid SCD thermometer) : {det_rate:.4f}  "
          f"({det_rate*100:.2f}%)")
    print(f"  Silent errors   (valid decode, wrong sym) : {silent_rate:.4f}  "
          f"({silent_rate*100:.2f}%)")
    print(f"  Any error                                 : {any_rate:.4f}  "
          f"({any_rate*100:.2f}%)")
    print()
    print(f"  Note: ~{det_rate/(any_rate+1e-12)*100:.1f}% of errors are detectable "
          f"(SCD thermometer broken).")
    print(f"  Silent errors require nearest-neighbor correction or redundancy.")


def print_sensitivity_analysis(rows):
    print_section("Sensitivity Analysis  --  Optical Energy vs Binary Indexed Lookup")
    print("""
  Shows optical energy under five scenarios vs the fixed binary baselines.
  The binary indexed baseline does NOT change across scenarios.
  'favorable' shows which approach has lower relative energy.

  Under configurable assumptions, optical PATTERN PROCESSING is beneficial only
  when LED and CMOS read costs are low relative to binary memory/compare costs.
""")

    hdr = (f"  {'Scenario':<38}  {'Opt E':>7}  {'Idx E':>7}  "
           f"{'vs Idx':>7}  {'Err%':>6}  {'Favors':>12}")
    print(hdr)
    print(f"  {_hr('-', 80)}")

    for r in rows:
        vs_idx = f"{r['vs_idx_pct']:+.1f}%"
        err_pct = f"{r['error_rate']*100:.1f}%"
        print(f"  {r['label']:<38}  {r['opt_energy']:>7.2f}  {r['idx_energy']:>7.2f}  "
              f"{vs_idx:>7}  {err_pct:>6}  {r['favorable']:>12}")

    print()
    print("  'vs Idx' = (binary_indexed_energy - optical_energy) / binary_indexed_energy")
    print("  Positive = optical uses LESS relative energy than binary indexed.")
    print("  Negative = optical uses MORE relative energy (binary indexed wins).")
    print()
    print("  CONCLUSION: Under moderate and optimistic optical assumptions the model")
    print("  shows optical using less relative energy than sequential binary, but")
    print("  the advantage over optimized indexed lookup depends on hardware cost")
    print("  parameters. Under high CMOS read or no-benefit assumptions, binary wins.")


def print_latency_comparison():
    print_section("Latency Step Comparison (structural model, not clock cycles)")

    n_seq  = math.ceil(BINARY_SEQ_FRACTION * ALPHABET_SIZE)
    l_seq  = n_seq * (BINARY_BITS + 1)
    l_idx  = 2
    l_opt  = 3

    print(f"""
  Binary sequential ({n_seq} iterations x {BINARY_BITS+1} steps/iter) : {l_seq} steps
  Binary indexed    (1 lookup + 1 verify)                    :  {l_idx} steps
  Optical SCD       (readout + threshold + validity)         :  {l_opt} steps

  Latency model assumptions:
  - Binary sequential: each iteration reads 1 word + compares {BINARY_BITS} bits (serial).
  - Binary indexed:    direct address lookup, then 1 verification compare.
  - Optical SCD:       all {MARKER_CHANNELS + SCD_BEAD_POSITIONS} channels read in PARALLEL in 1 step;
                       then 1 threshold pass; then 1 validity check.

  Optical latency advantage vs sequential : {l_seq - l_opt}x fewer steps.
  Optical latency vs indexed lookup        : {l_opt - l_idx} extra steps (optical slower by 1).

  The latency advantage over sequential is structural: pattern recognition
  does not scan candidates one-by-one. The comparison against indexed lookup
  is closer -- both are O(1) in the number of candidates.

  This latency model uses logical steps, NOT nanosecond measurements.
""")


# =============================================================================
# CSV OUTPUT
# =============================================================================

def save_csv(agg_seq, agg_idx, agg_opt, sensitivity_rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []

    def flat(d, prefix=""):
        return {f"{prefix}{k}": v for k, v in d.items()}

    rows.append({**flat(agg_seq, "seq_"), **flat(agg_idx, "idx_"), **flat(agg_opt, "opt_")})

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        # Main results
        writer = csv.writer(f)
        writer.writerow(["SECTION", "main_results"])
        if rows:
            writer.writerow(list(rows[0].keys()))
            writer.writerow(list(rows[0].values()))

        writer.writerow([])
        writer.writerow(["SECTION", "sensitivity_analysis"])
        if sensitivity_rows:
            writer.writerow(list(sensitivity_rows[0].keys()))
            for r in sensitivity_rows:
                writer.writerow(list(r.values()))

    print(f"\n  CSV saved: {output_path}")


# =============================================================================
# OPTIONAL PLOTS
# =============================================================================

def try_plot(agg_seq, agg_idx, agg_opt, sensitivity_rows, out_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not available -- skipping plots.")
        return

    os.makedirs(out_dir, exist_ok=True)

    methods  = ["Bin-Sequential", "Bin-Indexed", "Optical-SCD"]
    energies = [agg_seq["energy_mean"], agg_idx["energy_mean"], agg_opt["energy_mean"]]
    colors   = ["#4472C4", "#ED7D31", "#70AD47"]

    # Energy bar chart
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(methods, energies, color=colors, edgecolor="black", linewidth=0.7)
    ax.set_ylabel("Relative energy units (mean per trial)")
    ax.set_title("Conceptual Energy Comparison\n"
                 "(relative units, NOT measured hardware power)")
    for bar, val in zip(bars, energies):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(energies) * 0.01,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(energies) * 1.2)
    fig.tight_layout()
    p = os.path.join(out_dir, "pattern_vs_binary_energy.png")
    fig.savefig(p, dpi=120)
    plt.close(fig)
    print(f"  Plot saved: {p}")

    # Latency bar chart
    latencies = [agg_seq["latency_mean"], agg_idx["latency_mean"], agg_opt["latency_mean"]]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(methods, latencies, color=colors, edgecolor="black", linewidth=0.7)
    ax.set_ylabel("Latency steps (conceptual model)")
    ax.set_title("Conceptual Latency Comparison\n"
                 "(logical steps, NOT nanosecond measurements)")
    for bar, val in zip(bars, latencies):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(latencies) * 0.01,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(latencies) * 1.2)
    fig.tight_layout()
    p = os.path.join(out_dir, "pattern_vs_binary_latency.png")
    fig.savefig(p, dpi=120)
    plt.close(fig)
    print(f"  Plot saved: {p}")

    # Sensitivity analysis: optical energy across scenarios
    sc_labels  = [r["label"][:30] for r in sensitivity_rows]
    opt_e      = [r["opt_energy"] for r in sensitivity_rows]
    idx_e_ref  = sensitivity_rows[0]["idx_energy"]
    sc_colors  = ["#70AD47", "#4472C4", "#FFC000", "#ED7D31", "#FF0000"]
    fig, ax = plt.subplots(figsize=(9, 4))
    x = list(range(len(sc_labels)))
    bars = ax.bar(x, opt_e, color=sc_colors, edgecolor="black", linewidth=0.7, label="Optical energy")
    ax.axhline(idx_e_ref, color="navy", linewidth=1.5, linestyle="--",
               label=f"Binary-indexed baseline ({idx_e_ref:.1f})")
    ax.set_xticks(x)
    ax.set_xticklabels(sc_labels, rotation=18, ha="right", fontsize=7.5)
    ax.set_ylabel("Relative energy units")
    ax.set_title("Sensitivity Analysis: Optical Energy vs Binary Indexed\n"
                 "(relative units, configurable model)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    p = os.path.join(out_dir, "pattern_vs_binary_error_rates.png")
    fig.savefig(p, dpi=120)
    plt.close(fig)
    print(f"  Plot saved: {p}")


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    global SIGMA_SENSOR, N_TRIALS, RANDOM_SEED  # must be before any use

    parser = argparse.ArgumentParser(
        description=(
            "Conceptual emulator: SCD/RGB-white pattern processing "
            "vs binary sequential and indexed-lookup computation.\n\n"
            "FRAMING: relative energy units under configurable assumptions. "
            "NOT measured hardware performance. NOT quantum advantage."
        )
    )
    parser.add_argument("--trials",  type=int,   default=N_TRIALS,
                        help=f"Number of trials (default: {N_TRIALS})")
    parser.add_argument("--sigma",   type=float, default=SIGMA_SENSOR,
                        help=f"Sensor noise sigma (default: {SIGMA_SENSOR})")
    parser.add_argument("--seed",    type=int,   default=RANDOM_SEED,
                        help=f"Random seed (default: {RANDOM_SEED})")
    parser.add_argument("--no-plots", action="store_true",
                        help="Skip matplotlib plots even if available")
    args = parser.parse_args()

    SIGMA_SENSOR = args.sigma
    N_TRIALS     = args.trials

    random.seed(args.seed)

    print("=" * 78)
    print("  pattern_vs_binary_flash_emulator  --  Conceptual emulator")
    print("  SCD / RGB-white optical bead pattern vs binary comparison")
    print("=" * 78)
    print()
    print(f"  Trials: {N_TRIALS:,}   Seed: {args.seed}   Sigma: {SIGMA_SENSOR}")
    print()
    print("  Building alphabet...")
    alphabet = build_alphabet()
    print(f"  Alphabet: {len(alphabet)} symbols built.")

    print("  Running simulation...")
    seq_results, idx_results, opt_results = run_simulation(N_TRIALS, alphabet)

    print("  Aggregating...")
    agg_seq = aggregate(seq_results)
    agg_idx = aggregate(idx_results)
    agg_opt = aggregate(opt_results)

    print("  Running sensitivity analysis...")
    sensitivity_rows = run_sensitivity_analysis(alphabet, n_sample=min(500, N_TRIALS))

    # ---- Console report ----
    print_main_results(agg_seq, agg_idx, agg_opt, N_TRIALS)
    print_latency_comparison()
    print_sensitivity_analysis(sensitivity_rows)

    # ---- Guardrail reminder ----
    print_section("Guardrail / Limitations Reminder")
    print("""
  1. All numbers are RELATIVE UNITS under configurable assumptions.
  2. Binary sequential baseline is naive; binary INDEXED LOOKUP is O(1)
     and represents the optimized digital alternative.
  3. Optical latency advantage vs indexed lookup is small (3 vs 2 steps)
     in this model; the large advantage is only over naive sequential.
  4. Optical error rates depend heavily on noise parameters (sigma).
     At sigma >= 0.12, error rates may exceed 10%, degrading any advantage.
  5. No real hardware measurements were made or implied.
  6. No quantum advantage is claimed or implied.
  7. No guaranteed superiority of optical bead computing is claimed.
  8. Change any parameter block at the top of this file to test assumptions.
""")

    # ---- CSV ----
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path   = os.path.join(script_dir, "results",
                              "pattern_vs_binary_flash_emulator.csv")
    save_csv(agg_seq, agg_idx, agg_opt, sensitivity_rows, csv_path)

    # ---- Plots ----
    if not args.no_plots:
        out_dir = os.path.join(script_dir, "results")
        print()
        try_plot(agg_seq, agg_idx, agg_opt, sensitivity_rows, out_dir)
    else:
        print("  Plots skipped (--no-plots).")

    print()
    print("  Done.")
    print()


if __name__ == "__main__":
    main()
