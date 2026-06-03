"""
optical_medium_comparison.py - Optical medium stability comparison simulator
=============================================================================
Compares simplified environmental and material noise models for six optical
medium configurations used as the optical bead transmission channel:

  open_air       - free-space, unenclosed
  sealed_air     - dry-air or nitrogen cell with optical windows
  sealed_liquid  - transparent liquid cell (water, silicone oil, etc.)
  acrylic_block  - solid cast polymer block (PMMA / acrylic)
  glass_quartz   - precision optical glass or quartz block
  fiber_waveguide - single-mode or polarization-maintaining fiber

MODEL DISCLAIMER:
  This is a simplified engineering toy model, NOT a physical optics simulation.
  Noise parameters are qualitative engineering estimates, NOT measured values.
  Real performance depends on material choice, cell design, temperature control,
  and fabrication quality, all of which must be characterized empirically.

  The model is intended to:
    - compare relative noise assumptions across media under different alphabet sizes
    - guide prototype design decisions about which medium to test first
    - demonstrate the trade-off between stability, complexity, and DOF suitability

  This model does NOT:
    - prove that any medium is universally superior
    - replace empirical measurement in a real optical setup
    - model quantum optical effects

Noise model:
  Each medium is characterized by component noise sigma values (independent,
  Gaussian-equivalent approximations) for each noise source:
    gaussian_sigma     : baseline detector and source noise
    dust_sigma         : amplitude noise from dust particles
    humidity_sigma     : RI drift from humidity variation
    thermal_sigma      : thermal RI drift (from dn/dT and temperature variation)
    bubble_sigma       : amplitude noise from bubble scattering
    stress_sigma       : polarization/phase error from birefringence / stress
    alignment_sigma    : beam pointing instability

  Combined effective noise:
    effective_sigma = sqrt(sum of all sigma_i^2)

  Attenuation loss is reported separately and does NOT enter the SER simulation
  (it is a systematic effect, not a random noise source in this model).

  Symbol error rate is computed by nearest-neighbor decoding of states in a
  D-dimensional normalized [0,1]^D grid alphabet, with Gaussian noise
  of magnitude effective_sigma applied to each received state.

Standard Python only. numpy and matplotlib used only if available.
ASCII-only console output. Reproducible seed. CSV output.

Usage:
    python optical_medium_comparison.py
    python optical_medium_comparison.py --trials 5000
    python optical_medium_comparison.py --plot
"""

import random
import math
import os
import csv
import itertools
import argparse

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42
DEFAULT_TRIALS = 500   # use 5000 for publication-quality stability

M_VALUES = [4, 8, 16, 32, 64]
D_VALUES = [2, 4, 7]

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
DEFAULT_CSV = os.path.join(RESULTS_DIR, "optical_medium_comparison.csv")

# ---------------------------------------------------------------------------
# Medium noise presets
# ---------------------------------------------------------------------------
# All sigma values are in normalized [0,1] state-space units.
# They represent Gaussian-equivalent noise standard deviations.
# These are qualitative engineering estimates, NOT empirical measurements.
#
# dominant_noise_note: brief label for the main noise source(s)
# attenuation_loss: fraction of signal amplitude lost (0=none, 0.1=10%)
#   Note: attenuation_loss is NOT used in the SER calculation.
#   It is reported as a separate metric for reference.

MEDIUM_PRESETS = {
    "open_air": {
        "gaussian_sigma":   0.020,   # detector / source noise
        "dust_sigma":       0.060,   # high: airborne particles
        "humidity_sigma":   0.040,   # high: vapor pressure variation
        "thermal_sigma":    0.030,   # moderate: air RI fluctuation
        "bubble_sigma":     0.000,   # not applicable
        "stress_sigma":     0.000,   # not applicable
        "alignment_sigma":  0.050,   # high: free-space drift
        "attenuation_loss": 0.00,    # negligible for short paths
        "dominant_noise_note": "dust, humidity, alignment drift",
        "DOF_notes": "wavelength, intensity only recommended",
    },
    "sealed_air": {
        "gaussian_sigma":   0.020,
        "dust_sigma":       0.010,   # low: sealed enclosure
        "humidity_sigma":   0.010,   # low: dry gas fill
        "thermal_sigma":    0.025,   # moderate: temperature variation
        "bubble_sigma":     0.000,
        "stress_sigma":     0.000,
        "alignment_sigma":  0.025,   # moderate: thermal expansion of mounts
        "attenuation_loss": 0.00,
        "dominant_noise_note": "temperature drift, alignment",
        "DOF_notes": "wavelength + polarization recommended",
    },
    "sealed_liquid": {
        "gaussian_sigma":   0.020,
        "dust_sigma":       0.003,   # very low: sealed
        "humidity_sigma":   0.000,   # sealed: none
        "thermal_sigma":    0.040,   # high: dn/dT (water -1e-4/K; critical for phase)
        "bubble_sigma":     0.025,   # moderate: dissolved gas; requires degassing
        "stress_sigma":     0.000,   # not applicable
        "alignment_sigma":  0.010,   # low: mechanically stable cell
        "attenuation_loss": 0.03,    # ~3% for 5cm water at 633nm
        "dominant_noise_note": "thermal RI drift (critical for phase), bubble risk",
        "DOF_notes": "wavelength + polarization; phase impractical at cm scale",
    },
    "acrylic_block": {
        "gaussian_sigma":   0.020,
        "dust_sigma":       0.000,   # sealed solid
        "humidity_sigma":   0.000,   # sealed
        "thermal_sigma":    0.030,   # moderate: PMMA CTE ~70 ppm/K
        "bubble_sigma":     0.020,   # moderate: casting defects
        "stress_sigma":     0.035,   # high: curing shrinkage -> birefringence
        "alignment_sigma":  0.008,   # low: fixed geometry
        "attenuation_loss": 0.05,    # ~5% absorption in PMMA at short wavelengths
        "dominant_noise_note": "stress birefringence, thermal expansion, trapped bubbles",
        "DOF_notes": "wavelength, intensity, spatial position only; polarization degraded",
    },
    "glass_quartz": {
        "gaussian_sigma":   0.020,
        "dust_sigma":       0.000,
        "humidity_sigma":   0.000,
        "thermal_sigma":    0.008,   # low: CTE ~3-0.5 ppm/K
        "bubble_sigma":     0.000,   # optical quality: bubble-free
        "stress_sigma":     0.004,   # very low: optical-grade glass
        "alignment_sigma":  0.008,
        "attenuation_loss": 0.01,    # <1% for optical glass
        "dominant_noise_note": "detector noise (dominant), low thermal drift",
        "DOF_notes": "all DOFs including polarization and phase",
    },
    "fiber_waveguide": {
        "gaussian_sigma":   0.020,
        "dust_sigma":       0.000,
        "humidity_sigma":   0.000,
        "thermal_sigma":    0.012,   # low: fiber dn/dT, but thermally isolated
        "bubble_sigma":     0.000,
        "stress_sigma":     0.010,   # low: bend-induced birefringence in SMF
        "alignment_sigma":  0.004,   # very low: guided mode
        "attenuation_loss": 0.04,    # ~4% from coupling losses (not fiber loss)
        "dominant_noise_note": "coupling loss, bend birefringence",
        "DOF_notes": "wavelength + phase (SMF); wavelength + polarization (PMF)",
    },
}

MEDIUM_ORDER = [
    "open_air", "sealed_air", "sealed_liquid",
    "acrylic_block", "glass_quartz", "fiber_waveguide",
]

# ---------------------------------------------------------------------------
# Effective sigma computation
# ---------------------------------------------------------------------------

def compute_effective_sigma(preset):
    """Compute effective noise sigma as quadrature sum of all components."""
    components = [
        "gaussian_sigma", "dust_sigma", "humidity_sigma", "thermal_sigma",
        "bubble_sigma", "stress_sigma", "alignment_sigma",
    ]
    return math.sqrt(sum(preset[c] ** 2 for c in components))

# ---------------------------------------------------------------------------
# Alphabet and nearest-neighbor (reuse from photonic_binary_vs_obqc logic)
# ---------------------------------------------------------------------------

def build_grid_alphabet(M, D):
    """Build M states as a D-dimensional [0,1]^D grid (first M points)."""
    n_levels = max(2, math.ceil(M ** (1.0 / D)))
    step = 1.0 / (n_levels - 1) if n_levels > 1 else 1.0
    levels = [i * step for i in range(n_levels)]
    states = list(itertools.product(levels, repeat=D))
    return [list(s) for s in states[:M]]


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def min_margin(alphabet):
    n = len(alphabet)
    m = float("inf")
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean(alphabet[i], alphabet[j])
            if d < m:
                m = d
    return m


def nearest_neighbor(received, alphabet):
    best, best_d = 0, euclidean(received, alphabet[0])
    for i, s in enumerate(alphabet[1:], 1):
        d = euclidean(received, s)
        if d < best_d:
            best_d, best = d, i
    return best


def add_noise(state, sigma, rng):
    return [max(0.0, min(1.0, v + rng.gauss(0.0, sigma))) for v in state]


def compute_ser(alphabet, sigma, n_trials, rng):
    errors = 0
    M = len(alphabet)
    for _ in range(n_trials):
        true_idx = rng.randint(0, M - 1)
        received = add_noise(alphabet[true_idx], sigma, rng)
        if nearest_neighbor(received, alphabet) != true_idx:
            errors += 1
    return errors / n_trials

# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(m_values, d_values, n_trials, seed):
    rng = random.Random(seed)
    results = []

    for medium_name in MEDIUM_ORDER:
        preset = MEDIUM_PRESETS[medium_name]
        eff_sigma = compute_effective_sigma(preset)

        for D in d_values:
            for M in m_values:
                alphabet = build_grid_alphabet(M, D)
                actual_M = len(alphabet)
                margin = min_margin(alphabet)
                bits = math.log2(actual_M) if actual_M >= 2 else 0.0

                ser = compute_ser(alphabet, eff_sigma, n_trials, rng)
                throughput = bits * (1.0 - ser)

                results.append({
                    "medium": medium_name,
                    "M": actual_M,
                    "D": D,
                    "effective_sigma": round(eff_sigma, 5),
                    "attenuation_loss": preset["attenuation_loss"],
                    "separability_margin": round(margin, 4),
                    "bits_per_symbol": round(bits, 4),
                    "trials": n_trials,
                    "symbol_error_rate": round(ser, 5),
                    "throughput_proxy": round(throughput, 5),
                    "dominant_noise_note": preset["dominant_noise_note"],
                    "DOF_notes": preset["DOF_notes"],
                })

    return results

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 72)
    print("Optical Medium Comparison Simulator")
    print("=" * 72)
    print()
    print("TOY MODEL DISCLAIMER:")
    print("  This is a simplified engineering noise model, NOT a physical")
    print("  optics simulation. Noise parameters are qualitative estimates.")
    print("  Real performance must be characterized empirically.")
    print("  See docs/optical-medium-stabilization.md for full explanation.")
    print()


def print_medium_summary():
    print("--- Medium noise presets ---")
    print()
    print(f"  {'Medium':<20} {'eff_sigma':>10} {'atten':>7}  Dominant noise")
    print("  " + "-" * 68)
    for name in MEDIUM_ORDER:
        p = MEDIUM_PRESETS[name]
        eff = compute_effective_sigma(p)
        print(
            f"  {name:<20} {eff:>10.4f} {p['attenuation_loss']:>7.2f}  "
            f"{p['dominant_noise_note']}"
        )
    print()
    print("  effective_sigma = quadrature sum of all component sigmas")
    print("  attenuation_loss is reported separately (not used in SER calc)")
    print()


def print_results_table(results, d_filter=2):
    print(f"--- SER and throughput proxy at D={d_filter} ---")
    print()
    print(f"  {'Medium':<20} {'M':>5} {'eff_sig':>8} {'margin':>8} {'SER':>7} "
          f"{'bits':>6} {'tput':>7}")
    print("  " + "-" * 68)

    last_medium = None
    for row in results:
        if row["D"] != d_filter:
            continue
        if row["medium"] != last_medium:
            if last_medium is not None:
                print()
            last_medium = row["medium"]
        print(
            f"  {row['medium']:<20} {row['M']:>5} {row['effective_sigma']:>8.4f} "
            f"{row['separability_margin']:>8.4f} {row['symbol_error_rate']:>7.4f} "
            f"{row['bits_per_symbol']:>6.3f} {row['throughput_proxy']:>7.4f}"
        )
    print()


def print_interpretation():
    print("--- Interpretation (model-specific) ---")
    print()
    print("  open_air: highest effective noise -> highest SER at any M.")
    print("  sealed_air: moderate improvement by eliminating dust and humidity.")
    print("  sealed_liquid: lower dust/humidity noise but thermal RI drift is")
    print("    significant. Phase encoding impractical at cm-scale path lengths.")
    print("  acrylic_block: no dust or convection, but stress birefringence is")
    print("    the dominant noise for polarization DOFs. Color/position OK.")
    print("  glass_quartz: lowest effective sigma -> lowest SER at any M.")
    print("    Best option for polarization and phase DOFs.")
    print("  fiber_waveguide: very low environmental noise; coupling loss is")
    print("    the main practical concern (modeled as attenuation, not SER).")
    print()
    print("  All results are under idealized, model-level assumptions.")
    print("  Do not use these numbers as specifications for real hardware.")
    print()


def write_csv(results, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = [
        "medium", "M", "D", "effective_sigma", "attenuation_loss",
        "separability_margin", "bits_per_symbol", "trials",
        "symbol_error_rate", "throughput_proxy",
        "dominant_noise_note", "DOF_notes",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"  CSV saved: {csv_path}")


def plot_throughput(results, d_filter=2, save_path=None):
    if not HAS_MATPLOTLIB:
        return
    from collections import defaultdict
    by_medium = defaultdict(lambda: {"M": [], "tput": []})
    for row in results:
        if row["D"] != d_filter:
            continue
        by_medium[row["medium"]]["M"].append(row["M"])
        by_medium[row["medium"]]["tput"].append(row["throughput_proxy"])

    fig, ax = plt.subplots(figsize=(10, 6))
    for name in MEDIUM_ORDER:
        data = by_medium[name]
        if data["M"]:
            ax.plot(data["M"], data["tput"], marker="o", label=name)

    ax.set_xlabel("Alphabet size M")
    ax.set_ylabel("Throughput proxy [log2(M) * (1-SER)]")
    ax.set_title(
        f"Optical Medium Comparison (D={d_filter})\n"
        "(simplified noise model - not a physical measurement)"
    )
    ax.legend(fontsize=9)
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

def main(m_values=M_VALUES, d_values=D_VALUES, n_trials=DEFAULT_TRIALS,
         seed=SEED, csv_path=DEFAULT_CSV, plot=False, plot_path=None):

    print_header()
    print_medium_summary()
    print(f"  Trials per condition : {n_trials}  (use --trials 5000 for stable results)")
    print(f"  M values             : {m_values}")
    print(f"  D values             : {d_values}")
    print(f"  Seed                 : {seed}")
    print(f"  matplotlib           : {'available' if HAS_MATPLOTLIB else 'not available'}")
    print()
    print(f"  Running ({len(MEDIUM_ORDER)} media x {len(d_values)} D-values x "
          f"{len(m_values)} M-values x {n_trials} trials)...")
    print()

    results = run_simulation(m_values, d_values, n_trials, seed)

    for d in d_values:
        print_results_table(results, d_filter=d)

    print_interpretation()
    write_csv(results, csv_path)

    if plot or plot_path:
        plot_throughput(results, d_filter=2, save_path=plot_path)

    print()
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Optical medium stability comparison simulator"
    )
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS,
                        help=f"Trials per condition (default: {DEFAULT_TRIALS}; "
                             f"use 5000 for stable results)")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--csv", type=str, default=DEFAULT_CSV)
    parser.add_argument("--plot", action="store_true",
                        help="Show throughput plot (requires matplotlib)")
    parser.add_argument("--save-plot", type=str, default=None)
    args = parser.parse_args()
    main(
        n_trials=args.trials,
        seed=args.seed,
        csv_path=args.csv,
        plot=args.plot,
        plot_path=args.save_plot,
    )
