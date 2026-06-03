"""
encode_decode.py - Optical Bead Computing simulator core
=========================================================
Defines an optical bead alphabet, encodes integer values as multi-valued
optical bead state vectors, adds optional noise, and decodes by
nearest-neighbor distance.

No external dependencies required. numpy is used if available for
convenience, but the core logic runs on pure Python lists.

Usage:
    python encode_decode.py
"""

import math
import random

# ---------------------------------------------------------------------------
# Degree-of-freedom definitions
# ---------------------------------------------------------------------------

# Each DOF is represented as a list of discrete normalized values in [0, 1].
# Physical meaning:
#   WAVELENGTH_LEVELS:  normalized wavelength channels  (0=shortest, 1=longest)
#   POLARIZATION_LEVELS: normalized polarization states  (0=H, 0.33=D, 0.67=V, 1=A)
#   TIMEBIN_LEVELS:     normalized time-bin assignments (0=earliest, 1=latest)

WAVELENGTH_LEVELS   = [0.0, 0.33, 0.67, 1.0]   # 4 wavelength channels
POLARIZATION_LEVELS = [0.0, 0.33, 0.67, 1.0]   # 4 polarization states
TIMEBIN_LEVELS      = [0.0, 0.5,  1.0]          # 3 time bins


def build_alphabet(wavelengths=None, polarizations=None, timebins=None):
    """
    Build an optical bead alphabet as a list of state tuples.

    Each state is a tuple (lambda_norm, polarization_norm, timebin_norm)
    representing the normalized values of three degrees of freedom.

    Returns:
        list of tuples: the complete alphabet
    """
    if wavelengths is None:
        wavelengths = WAVELENGTH_LEVELS
    if polarizations is None:
        polarizations = POLARIZATION_LEVELS
    if timebins is None:
        timebins = TIMEBIN_LEVELS

    alphabet = []
    for lam in wavelengths:
        for pol in polarizations:
            for tbin in timebins:
                alphabet.append((lam, pol, tbin))
    return alphabet


def encode(value, alphabet):
    """
    Encode an integer value as an optical bead state vector.

    Args:
        value (int): integer in range [0, len(alphabet)-1]
        alphabet (list): list of state tuples

    Returns:
        tuple: the optical bead state for this value
    """
    if not (0 <= value < len(alphabet)):
        raise ValueError(
            f"Value {value} out of range for alphabet of size {len(alphabet)}"
        )
    return alphabet[value]


def distance(state_a, state_b):
    """
    Euclidean distance between two optical bead state tuples.
    Each component is already normalized to [0, 1], so dimensions are comparable.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(state_a, state_b)))


def decode(received_state, alphabet):
    """
    Decode a (possibly noisy) received state by nearest-neighbor lookup.

    Args:
        received_state (tuple): measured optical bead state
        alphabet (list): reference alphabet

    Returns:
        int: index of the closest state in the alphabet
    """
    best_idx = 0
    best_dist = distance(received_state, alphabet[0])
    for i, state in enumerate(alphabet[1:], start=1):
        d = distance(received_state, state)
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


def add_noise(state, sigma=0.05):
    """
    Add independent Gaussian noise to each dimension of a state vector.

    Args:
        state (tuple): optical bead state
        sigma (float): noise standard deviation (relative to [0, 1] range)

    Returns:
        tuple: noisy state (values may exceed [0, 1]; clipped to [0, 1])
    """
    noisy = []
    for v in state:
        v_noisy = v + random.gauss(0.0, sigma)
        v_noisy = max(0.0, min(1.0, v_noisy))  # clip to valid range
        noisy.append(v_noisy)
    return tuple(noisy)


def symbol_error_rate(alphabet, sigma=0.05, n_trials=500):
    """
    Estimate symbol error rate by Monte Carlo simulation.

    For each symbol in the alphabet, transmit it n_trials times with
    Gaussian noise and count how many times decoding fails.

    Args:
        alphabet (list): optical bead alphabet
        sigma (float): noise standard deviation
        n_trials (int): number of trials per symbol

    Returns:
        float: symbol error rate in [0, 1]
    """
    errors = 0
    total = 0
    for true_idx, true_state in enumerate(alphabet):
        for _ in range(n_trials):
            received = add_noise(true_state, sigma=sigma)
            decoded_idx = decode(received, alphabet)
            if decoded_idx != true_idx:
                errors += 1
            total += 1
    return errors / total


def minimum_inter_state_distance(alphabet):
    """
    Compute the minimum Euclidean distance between any two distinct states.

    This is the separability margin of the alphabet.
    """
    min_dist = float("inf")
    for i in range(len(alphabet)):
        for j in range(i + 1, len(alphabet)):
            d = distance(alphabet[i], alphabet[j])
            if d < min_dist:
                min_dist = d
    return min_dist


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Optical Bead Computing - encode/decode demo")
    print("=" * 60)

    alphabet = build_alphabet()
    print(f"\nAlphabet size: {len(alphabet)} states")
    print(f"Degrees of freedom: wavelength x polarization x time-bin")
    print(f"  Wavelength levels : {len(WAVELENGTH_LEVELS)}")
    print(f"  Polarization levels: {len(POLARIZATION_LEVELS)}")
    print(f"  Time-bin levels   : {len(TIMEBIN_LEVELS)}")

    margin = minimum_inter_state_distance(alphabet)
    print(f"\nMinimum inter-state distance (separability margin): {margin:.4f}")

    print("\nFirst 10 states in alphabet:")
    for i, state in enumerate(alphabet[:10]):
        print(f"  [{i:2d}] lam={state[0]:.2f}  P={state[1]:.2f}  tau={state[2]:.2f}")

    print("\nEncoding digits 0-9:")
    for digit in range(10):
        state = encode(digit, alphabet)
        received = add_noise(state, sigma=0.04)
        decoded = decode(received, alphabet)
        status = "OK" if decoded == digit else f"ERROR->{decoded}"
        print(
            f"  digit {digit}: encoded={state}  "
            f"received=({received[0]:.3f},{received[1]:.3f},{received[2]:.3f})  {status}"
        )

    print("\nSymbol error rate vs noise level:")
    for sigma in [0.01, 0.02, 0.05, 0.08, 0.12, 0.18]:
        ser = symbol_error_rate(alphabet, sigma=sigma, n_trials=300)
        bar = "#" * int(ser * 40)
        print(f"  sigma={sigma:.2f}  SER={ser:.4f}  |{bar}")

    print("\nDone.")
