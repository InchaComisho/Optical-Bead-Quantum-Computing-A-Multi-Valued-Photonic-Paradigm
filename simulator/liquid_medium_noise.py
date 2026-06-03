"""
liquid_medium_noise.py - Sealed liquid optical bead medium noise model
=======================================================================
Extends the baseline noise model (noise_model.py) with additional noise
sources specific to a sealed transparent liquid optical cell.

PHYSICAL CONTEXT:
  In a sealed liquid optical bead medium, the optical signal propagates
  through a transparent liquid (e.g., water, glycerol solution, immersion oil)
  rather than open air. This reduces air-turbulence and dust noise but
  introduces liquid-specific noise sources:

    - Absorption attenuation (Beer-Lambert law, wavelength-dependent)
    - Scattering from bubbles or impurities (multiplicative amplitude noise)
    - Temperature-dependent refractive index drift (affects phase)
    - Differential wavelength transmission (per-channel attenuation offset)
    - Thermal gradient beam steering (affects spatial mode coordinate)

MODEL DISCLAIMER:
  This is a simplified analytical model for simulation purposes.
  Real liquid optical cells require empirical calibration of all parameters.
  The model does NOT replace physical characterization of a real cell.
  All parameters (alpha, dn_dT, etc.) are configurable and should be
  set to measured values for a specific medium and path length.

No external dependencies required.
ASCII-only output.

Usage:
    python liquid_medium_noise.py
    python liquid_medium_noise.py --path-length 5.0 --delta-T 0.5
"""

import random
import math
import argparse

# ---------------------------------------------------------------------------
# Physical constants and reference parameters
# ---------------------------------------------------------------------------

# Absorption coefficients (1/cm) for common media at visible wavelengths
# These are approximate literature values for reference.
# Real systems require empirical measurement.
ABSORPTION_DB = {
    "water":          {450: 0.003, 532: 0.001, 633: 0.003, 780: 0.025},   # per cm
    "glycerol_water": {450: 0.005, 532: 0.002, 633: 0.004, 780: 0.028},   # per cm
    "immersion_oil":  {450: 0.010, 532: 0.005, 633: 0.008, 780: 0.040},   # per cm
}

# Thermo-optic coefficient dn/dT (per Kelvin) for common media
# Negative: refractive index decreases as temperature increases
DN_DT = {
    "water":          -1.0e-4,   # /K at 589 nm, 20 deg C
    "glycerol_water": -2.5e-4,   # /K (approx. 50/50 vol)
    "immersion_oil":  -3.0e-4,   # /K (Type A microscopy oil)
}

# ---------------------------------------------------------------------------
# 1. Absorption attenuation (Beer-Lambert)
# ---------------------------------------------------------------------------

def absorption_attenuation(signal, alpha_per_cm, path_length_cm):
    """
    Apply Beer-Lambert absorption attenuation to a scalar signal amplitude.

    I(L) = I_0 * exp(-alpha * L)

    In the normalized state model, the signal is a value in [0, 1].
    Absorption scales the signal toward 0 by the attenuation factor.
    This represents amplitude reduction, which in a multi-wavelength system
    creates differential channel gain.

    Args:
        signal (float): normalized signal amplitude in [0, 1]
        alpha_per_cm (float): absorption coefficient in cm^-1
        path_length_cm (float): optical path length in cm

    Returns:
        float: attenuated signal
    """
    attenuation_factor = math.exp(-alpha_per_cm * path_length_cm)
    return signal * attenuation_factor


def apply_wavelength_absorption(state, alpha_per_cm_per_channel,
                                 path_length_cm, wavelength_dim=0):
    """
    Apply wavelength-dependent absorption to the wavelength dimension.

    In a multi-wavelength encoding, different wavelength channels are
    attenuated by different amounts, which compresses the wavelength
    coordinate toward 0 and shifts relative channel amplitudes.

    The normalized state coordinate is shifted by the fractional
    intensity loss, approximately: delta_v = -alpha * L * (1 - v)
    where v is the normalized wavelength coordinate.

    This is a simplified model. Real systems require calibration.

    Args:
        state (list or tuple): optical bead state vector
        alpha_per_cm_per_channel (dict): {channel_id: alpha} mapping
                                          If single float, applied uniformly.
        path_length_cm (float): path length in cm
        wavelength_dim (int): index of wavelength dimension in state vector

    Returns:
        list: state with absorption applied to wavelength dimension
    """
    noisy = list(state)
    v = state[wavelength_dim]

    # Uniform absorption model: intensity loss -> apparent coordinate shift
    if isinstance(alpha_per_cm_per_channel, (int, float)):
        alpha = alpha_per_cm_per_channel
    else:
        # Interpolate alpha based on normalized coordinate v
        channels = sorted(alpha_per_cm_per_channel.keys())
        if len(channels) == 0:
            alpha = 0.0
        elif len(channels) == 1:
            alpha = list(alpha_per_cm_per_channel.values())[0]
        else:
            # Linear interpolation between first and last channel
            alpha_min = alpha_per_cm_per_channel[channels[0]]
            alpha_max = alpha_per_cm_per_channel[channels[-1]]
            alpha = alpha_min + v * (alpha_max - alpha_min)

    attenuation = math.exp(-alpha * path_length_cm)
    # Amplitude attenuation compresses the coordinate toward 0
    noisy[wavelength_dim] = max(0.0, min(1.0, v * attenuation))
    return noisy

# ---------------------------------------------------------------------------
# 2. Scattering noise from bubbles / impurities
# ---------------------------------------------------------------------------

def scattering_noise(state, scatter_sigma, rng):
    """
    Apply multiplicative lognormal amplitude noise from bubble/impurity scattering.

    Scattering events cause random amplitude drops. Modeled as
    multiplicative lognormal noise: signal * exp(N(0, sigma^2)).
    Applied to all dimensions uniformly (scattering is wavelength-
    dependent in reality but approximated as uniform here).

    Args:
        state (list): optical bead state vector, values in [0, 1]
        scatter_sigma (float): lognormal scale parameter.
                                0.0 = no scattering
                                0.05 = mild scattering (bubble-free liquid)
                                0.15 = moderate scattering (some impurities)
                                0.30 = strong scattering (contaminated liquid)
        rng: random.Random instance

    Returns:
        list: noisy state
    """
    if scatter_sigma <= 0:
        return list(state)

    log_noise = rng.gauss(0.0, scatter_sigma)
    scale = math.exp(log_noise)
    return [max(0.0, min(1.0, v * scale)) for v in state]

# ---------------------------------------------------------------------------
# 3. Temperature-dependent refractive index drift (phase coordinate)
# ---------------------------------------------------------------------------

def thermal_phase_drift(state, dn_dT, delta_T_kelvin, path_length_cm,
                         wavelength_nm=633.0, phase_dim=2):
    """
    Apply phase drift caused by temperature-induced refractive index change.

    The optical path length changes by delta_OPL = delta_n * L where
    delta_n = dn_dT * delta_T. This causes a phase shift of:
        delta_phi = (2 * pi / lambda) * delta_n * L (in radians)

    In the normalized phase coordinate, this shift is mapped to a
    fractional displacement of the phase state.

    Args:
        state (list): optical bead state vector
        dn_dT (float): thermo-optic coefficient in K^-1 (typically negative)
        delta_T_kelvin (float): temperature deviation from calibration setpoint
        path_length_cm (float): optical path length in cm
        wavelength_nm (float): optical wavelength in nm (used for phase calculation)
        phase_dim (int): index of phase dimension in state vector (default: 2)
                         Set to -1 to skip phase noise application.

    Returns:
        list: state with phase drift applied
    """
    if phase_dim < 0 or phase_dim >= len(state):
        return list(state)

    delta_n = dn_dT * delta_T_kelvin
    path_length_m = path_length_cm * 1e-2
    wavelength_m = wavelength_nm * 1e-9

    delta_phi_rad = (2 * math.pi / wavelength_m) * delta_n * path_length_m

    # Map phase shift to normalized [0, 1] coordinate
    # Assume normalized phase spans [0, 2*pi], so delta_phi_norm = delta_phi / (2*pi)
    delta_phi_norm = delta_phi_rad / (2 * math.pi)

    noisy = list(state)
    noisy[phase_dim] = (state[phase_dim] + delta_phi_norm) % 1.0
    return noisy


def stochastic_thermal_drift(state, dn_dT, T_sigma, path_length_cm,
                              wavelength_nm=633.0, phase_dim=2, rng=None):
    """
    Apply stochastic temperature fluctuation as a random phase drift.

    Models short-term thermal noise as a Gaussian-distributed temperature
    fluctuation around the setpoint. Uses thermal_phase_drift internally.

    Args:
        state (list): optical bead state vector
        dn_dT (float): thermo-optic coefficient (K^-1)
        T_sigma (float): standard deviation of temperature fluctuation (K)
        path_length_cm (float): optical path length in cm
        wavelength_nm (float): wavelength in nm
        phase_dim (int): index of phase dimension
        rng: random.Random instance (required if T_sigma > 0)

    Returns:
        list: state with stochastic thermal phase drift applied
    """
    if T_sigma <= 0:
        return list(state)
    if rng is None:
        raise ValueError("rng is required when T_sigma > 0")

    delta_T = rng.gauss(0.0, T_sigma)
    return thermal_phase_drift(state, dn_dT, delta_T, path_length_cm,
                               wavelength_nm=wavelength_nm, phase_dim=phase_dim)

# ---------------------------------------------------------------------------
# 4. Thermal gradient beam steering (spatial mode coordinate)
# ---------------------------------------------------------------------------

def thermal_gradient_steering(state, gradient_sigma, spatial_dim=None, rng=None):
    """
    Apply slow beam-steering noise from refractive index gradients in the liquid.

    A non-uniform temperature distribution across the cell creates a
    gradient in refractive index that acts as a weak prism, slowly
    steering the beam off-axis. In a spatial-mode-encoded state, this
    displaces the beam in the spatial coordinate.

    Args:
        state (list): optical bead state vector
        gradient_sigma (float): standard deviation of spatial displacement
                                 in normalized [0, 1] units.
                                 0.0 = no steering
                                 0.02 = mild gradient (good temperature uniformity)
                                 0.05 = moderate (1-2 K gradient across cell)
        spatial_dim (int or None): index of spatial mode dimension.
                                   If None, no steering is applied.
        rng: random.Random instance

    Returns:
        list: state with spatial displacement applied
    """
    if spatial_dim is None or gradient_sigma <= 0:
        return list(state)
    if rng is None:
        raise ValueError("rng is required when gradient_sigma > 0")

    noisy = list(state)
    noisy[spatial_dim] = max(
        0.0, min(1.0, state[spatial_dim] + rng.gauss(0.0, gradient_sigma))
    )
    return noisy

# ---------------------------------------------------------------------------
# 5. Combined liquid medium noise model
# ---------------------------------------------------------------------------

def liquid_medium_noise(
    state,
    path_length_cm=5.0,
    alpha_per_cm=0.003,
    scatter_sigma=0.03,
    dn_dT=-1.0e-4,
    T_sigma=0.5,
    wavelength_nm=633.0,
    gradient_sigma=0.01,
    gaussian_sigma=0.02,
    phase_dim=2,
    spatial_dim=None,
    rng=None,
):
    """
    Apply the full combined liquid medium noise model.

    Applies noise sources in order:
        1. Gaussian baseline noise (from all sources)
        2. Absorption attenuation (wavelength dim)
        3. Scattering noise (all dims)
        4. Stochastic thermal phase drift (phase dim)
        5. Thermal gradient beam steering (spatial dim, if used)

    Args:
        state (list or tuple): optical bead state vector
        path_length_cm (float): cell path length in cm (default: 5 cm)
        alpha_per_cm (float): absorption coefficient in cm^-1 (default: water at 633 nm)
        scatter_sigma (float): scattering lognormal sigma (default: 0.03, clean liquid)
        dn_dT (float): thermo-optic coefficient (default: water value)
        T_sigma (float): temperature fluctuation std dev in K (default: 0.5 K)
        wavelength_nm (float): wavelength for phase calculation (default: 633 nm)
        gradient_sigma (float): spatial beam-steering sigma (default: 0.01)
        gaussian_sigma (float): baseline Gaussian noise sigma (default: 0.02)
        phase_dim (int): index of phase dimension (default: 2; set to -1 to skip)
        spatial_dim (int or None): index of spatial dim (default: None, no steering)
        rng: random.Random instance (required)

    Returns:
        list: noisy state
    """
    if rng is None:
        raise ValueError("rng must be provided")

    s = list(state)

    # 1. Baseline Gaussian noise
    s = [max(0.0, min(1.0, v + rng.gauss(0.0, gaussian_sigma))) for v in s]

    # 2. Absorption attenuation on wavelength dimension
    s = apply_wavelength_absorption(s, alpha_per_cm, path_length_cm, wavelength_dim=0)

    # 3. Scattering noise
    s = scattering_noise(s, scatter_sigma, rng)

    # 4. Stochastic thermal phase drift
    s = stochastic_thermal_drift(
        s, dn_dT=dn_dT, T_sigma=T_sigma,
        path_length_cm=path_length_cm,
        wavelength_nm=wavelength_nm,
        phase_dim=phase_dim, rng=rng,
    )

    # 5. Thermal gradient beam steering
    s = thermal_gradient_steering(s, gradient_sigma, spatial_dim=spatial_dim, rng=rng)

    return s

# ---------------------------------------------------------------------------
# Parameter presets for common liquid media
# ---------------------------------------------------------------------------

PRESETS = {
    "water_clean": {
        "alpha_per_cm": 0.003,
        "scatter_sigma": 0.01,
        "dn_dT": -1.0e-4,
        "description": "Distilled water, clean, temperature controlled to +/-0.1 K",
    },
    "water_uncontrolled": {
        "alpha_per_cm": 0.003,
        "scatter_sigma": 0.05,
        "dn_dT": -1.0e-4,
        "description": "Distilled water, some bubbles, room temperature drift",
    },
    "glycerol_water": {
        "alpha_per_cm": 0.005,
        "scatter_sigma": 0.02,
        "dn_dT": -2.5e-4,
        "description": "50/50 glycerol-water solution, moderate scatter, higher dn/dT",
    },
    "immersion_oil": {
        "alpha_per_cm": 0.010,
        "scatter_sigma": 0.02,
        "dn_dT": -3.0e-4,
        "description": "Microscopy immersion oil, low scatter, high dn/dT",
    },
    "open_air_baseline": {
        "alpha_per_cm": 0.0,
        "scatter_sigma": 0.0,
        "dn_dT": 0.0,
        "description": "Open air (no absorption, no scattering, no thermal drift) -- baseline",
    },
}

# ---------------------------------------------------------------------------
# Demo and comparison
# ---------------------------------------------------------------------------

def run_demo(path_length_cm=5.0, T_sigma=0.5, n_trials=2000, seed=42):
    rng = random.Random(seed)

    test_state = [0.33, 0.67, 0.50]   # (wavelength, polarization, phase)
    print("=" * 65)
    print("Sealed Liquid Optical Bead Medium - Noise Model Demo")
    print("=" * 65)
    print()
    print(f"  Test state : {test_state}")
    print(f"  Path length: {path_length_cm} cm")
    print(f"  Temperature fluctuation std dev: {T_sigma} K")
    print(f"  Trials     : {n_trials}")
    print()

    for preset_name, preset in PRESETS.items():
        alpha = preset["alpha_per_cm"]
        scatter = preset["scatter_sigma"]
        dn_dT = preset["dn_dT"]

        samples = []
        for _ in range(n_trials):
            noisy = liquid_medium_noise(
                test_state,
                path_length_cm=path_length_cm,
                alpha_per_cm=alpha,
                scatter_sigma=scatter,
                dn_dT=dn_dT,
                T_sigma=T_sigma,
                gaussian_sigma=0.02,
                phase_dim=2,
                spatial_dim=None,
                rng=rng,
            )
            samples.append(noisy)

        # Compute per-dimension std dev as noise metric
        for dim in range(len(test_state)):
            vals = [s[dim] for s in samples]
            mean_v = sum(vals) / len(vals)
            std_v = math.sqrt(sum((v - mean_v) ** 2 for v in vals) / len(vals))

        stds = []
        for dim in range(len(test_state)):
            vals = [s[dim] for s in samples]
            mean_v = sum(vals) / len(vals)
            std_v = math.sqrt(sum((v - mean_v) ** 2 for v in vals) / len(vals))
            stds.append(std_v)

        means = []
        for dim in range(len(test_state)):
            vals = [s[dim] for s in samples]
            means.append(sum(vals) / len(vals))

        dim_labels = ["wavelength", "polarization", "phase    "]
        print(f"  [{preset_name}]")
        print(f"  {preset['description']}")
        for i, label in enumerate(dim_labels):
            print(
                f"    {label}: mean={means[i]:.4f}  std={stds[i]:.4f}  "
                f"(original: {test_state[i]:.4f})"
            )
        print()

    # Show individual noise contributions
    print("  --- Individual noise source breakdown (water_clean, 5 cm) ---")
    print()
    base_state = [0.50, 0.50, 0.50]
    rng2 = random.Random(seed)

    # Absorption only
    absorbed = apply_wavelength_absorption(base_state, 0.003, path_length_cm)
    print(f"  Absorption only (alpha=0.003/cm, L={path_length_cm}cm):")
    print(f"    wavelength: {base_state[0]:.4f} -> {absorbed[0]:.4f}  "
          f"(factor: {math.exp(-0.003*path_length_cm):.4f})")
    print()

    # Phase drift for different temperature deviations
    print("  Phase drift from temperature deviation (water, L=5cm, lambda=633nm):")
    for dT in [0.1, 0.5, 1.0, 2.0, 5.0]:
        drifted = thermal_phase_drift(
            base_state, dn_dT=-1.0e-4, delta_T_kelvin=dT,
            path_length_cm=path_length_cm, phase_dim=2
        )
        delta_phi_rad = (2 * math.pi / 633e-9) * (-1.0e-4 * dT) * (path_length_cm * 1e-2)
        print(
            f"    delta_T={dT:4.1f} K: phase {base_state[2]:.4f} -> {drifted[2]:.4f}  "
            f"(delta_phi={delta_phi_rad:.4f} rad)"
        )
    print()
    print("  IMPORTANT: At 5 cm path length (water), delta_T = 0.1 K causes ~5 rad")
    print("  phase drift -- this completely scrambles phase encoding.")
    print("  For < 0.1 rad phase control at 5 cm, temperature must be held to < 2 mK.")
    print("  For < 10 mrad control, either shorten path to ~0.1 mm or use")
    print("  active interferometric phase stabilization feedback.")
    print("  Practical implication: phase DOF should be deferred to later prototype phases.")
    print("  Wavelength and polarization encoding are far more temperature-tolerant.")
    print()
    print("  See docs/sealed-liquid-optical-bead-medium.md for full explanation.")
    print()
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sealed liquid optical bead medium noise model demo"
    )
    parser.add_argument("--path-length", type=float, default=5.0,
                        help="Optical path length in cm (default: 5.0)")
    parser.add_argument("--delta-T", type=float, default=0.5,
                        help="Temperature fluctuation std dev in K (default: 0.5)")
    parser.add_argument("--trials", type=int, default=2000,
                        help="Number of trials per condition (default: 2000)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    args = parser.parse_args()
    run_demo(
        path_length_cm=args.path_length,
        T_sigma=args.delta_T,
        n_trials=args.trials,
        seed=args.seed,
    )
