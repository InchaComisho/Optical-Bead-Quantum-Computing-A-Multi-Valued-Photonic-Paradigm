"""
noise_model.py - Optical Bead Computing noise models
=====================================================
Provides modular noise functions that can be applied to optical bead
state vectors. Models include:

  - Gaussian noise          (random fluctuation per DOF)
  - Temporal jitter         (timing uncertainty for time-bin DOF)
  - Channel drift           (slow systematic shift over time)
  - Spectral crosstalk      (adjacent wavelength channel leakage)

All functions accept and return normalized state tuples with values in [0, 1].
Values are clipped to [0, 1] after noise application.

No external dependencies required (uses Python standard library only).
"""

import random
import math


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def clip(value, lo=0.0, hi=1.0):
    """Clip value to [lo, hi]."""
    return max(lo, min(hi, value))


def apply_per_dim(state, noise_fn):
    """Apply a scalar noise function independently to each dimension."""
    return tuple(clip(noise_fn(v)) for v in state)


# ---------------------------------------------------------------------------
# Gaussian noise
# ---------------------------------------------------------------------------

def gaussian_noise(state, sigma=0.05):
    """
    Add independent Gaussian noise to each dimension.

    Models: random fluctuations from detector noise, source intensity
    variation, and environmental perturbations affecting all DOFs.

    Args:
        state (tuple): optical bead state, values in [0, 1]
        sigma (float): noise standard deviation (relative to [0, 1] range)

    Returns:
        tuple: noisy state
    """
    return tuple(clip(v + random.gauss(0.0, sigma)) for v in state)


# ---------------------------------------------------------------------------
# Temporal jitter
# ---------------------------------------------------------------------------

def temporal_jitter(state, jitter_sigma=0.05, timebin_dim=2):
    """
    Apply temporal jitter to the time-bin dimension only.

    Models: timing uncertainty in pulse arrival, electronic trigger jitter,
    or detector timing resolution limits.

    Args:
        state (tuple): optical bead state
        jitter_sigma (float): standard deviation of timing jitter,
                              expressed as a fraction of the time-bin range
        timebin_dim (int): index of the time-bin dimension in the state tuple

    Returns:
        tuple: state with jitter applied to the time-bin dimension
    """
    noisy = list(state)
    noisy[timebin_dim] = clip(state[timebin_dim] + random.gauss(0.0, jitter_sigma))
    return tuple(noisy)


# ---------------------------------------------------------------------------
# Channel drift
# ---------------------------------------------------------------------------

def channel_drift(state, drift_rates, elapsed_time=1.0):
    """
    Apply slow systematic drift to all dimensions.

    Models: thermal expansion causing phase path length changes, slow
    laser wavelength drift, polarization component aging.

    The drift is deterministic given drift_rates and elapsed_time,
    representing the expected mean shift after a period of operation
    since last calibration.

    Args:
        state (tuple): optical bead state
        drift_rates (tuple or list): drift rate per dimension,
                                     in units of [range/time_unit]
                                     e.g., (0.001, 0.002, 0.0) per second
        elapsed_time (float): time since last calibration, in time_units

    Returns:
        tuple: drifted state
    """
    noisy = tuple(
        clip(v + rate * elapsed_time)
        for v, rate in zip(state, drift_rates)
    )
    return noisy


# ---------------------------------------------------------------------------
# Spectral crosstalk
# ---------------------------------------------------------------------------

def spectral_crosstalk(state, crosstalk_fraction=0.05, wavelength_dim=0):
    """
    Apply spectral crosstalk to the wavelength dimension.

    Models the effect of adjacent wavelength channels leaking into the
    measured channel due to finite filter bandwidth and source linewidth.

    The measured wavelength coordinate is shifted toward a random
    direction by a fraction proportional to crosstalk_fraction,
    simulating partial leakage from an adjacent channel.

    Args:
        state (tuple): optical bead state
        crosstalk_fraction (float): fraction of the wavelength range
                                    that can be added as crosstalk shift
        wavelength_dim (int): index of the wavelength dimension

    Returns:
        tuple: state with spectral crosstalk applied
    """
    noisy = list(state)
    # Crosstalk displaces the measured wavelength by up to +/-crosstalk_fraction
    shift = random.uniform(-crosstalk_fraction, crosstalk_fraction)
    noisy[wavelength_dim] = clip(state[wavelength_dim] + shift)
    return tuple(noisy)


# ---------------------------------------------------------------------------
# Combined realistic noise model
# ---------------------------------------------------------------------------

def realistic_noise(
    state,
    gaussian_sigma=0.03,
    jitter_sigma=0.03,
    crosstalk_fraction=0.02,
    drift_rates=None,
    elapsed_time=0.0,
    timebin_dim=2,
    wavelength_dim=0,
):
    """
    Apply a combined realistic noise model.

    Applies Gaussian noise, temporal jitter, spectral crosstalk, and
    optional channel drift in sequence.

    Args:
        state (tuple): optical bead state
        gaussian_sigma (float): Gaussian noise standard deviation
        jitter_sigma (float): time-bin jitter sigma
        crosstalk_fraction (float): spectral crosstalk fraction
        drift_rates (tuple or None): per-dimension drift rates;
                                     if None, no drift is applied
        elapsed_time (float): time since calibration for drift calculation
        timebin_dim (int): index of time-bin dimension
        wavelength_dim (int): index of wavelength dimension

    Returns:
        tuple: noisy state
    """
    s = gaussian_noise(state, sigma=gaussian_sigma)
    s = temporal_jitter(s, jitter_sigma=jitter_sigma, timebin_dim=timebin_dim)
    s = spectral_crosstalk(s, crosstalk_fraction=crosstalk_fraction,
                           wavelength_dim=wavelength_dim)
    if drift_rates is not None:
        s = channel_drift(s, drift_rates=drift_rates, elapsed_time=elapsed_time)
    return s


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Optical Bead Computing - noise model demo")
    print("=" * 60)

    test_state = (0.33, 0.67, 0.5)
    print(f"\nOriginal state: {test_state}")

    for sigma in [0.02, 0.05, 0.10]:
        noisy = gaussian_noise(test_state, sigma=sigma)
        print(f"  Gaussian sigma={sigma:.2f}: {tuple(round(v, 4) for v in noisy)}")

    print(f"\nTemporal jitter (sigma=0.08) on time-bin dim:")
    for _ in range(5):
        noisy = temporal_jitter(test_state, jitter_sigma=0.08)
        print(f"  {tuple(round(v, 4) for v in noisy)}")

    print(f"\nSpectral crosstalk (fraction=0.05) on wavelength dim:")
    for _ in range(5):
        noisy = spectral_crosstalk(test_state, crosstalk_fraction=0.05)
        print(f"  {tuple(round(v, 4) for v in noisy)}")

    print(f"\nChannel drift after 100 time units (rates=(0.001, 0.002, 0.0)):")
    drifted = channel_drift(test_state, drift_rates=(0.001, 0.002, 0.0), elapsed_time=100.0)
    print(f"  {tuple(round(v, 4) for v in drifted)}")

    print(f"\nCombined realistic noise:")
    for trial in range(5):
        noisy = realistic_noise(
            test_state,
            gaussian_sigma=0.03,
            jitter_sigma=0.03,
            crosstalk_fraction=0.02,
        )
        print(f"  trial {trial}: {tuple(round(v, 4) for v in noisy)}")

    print("\nDone.")
