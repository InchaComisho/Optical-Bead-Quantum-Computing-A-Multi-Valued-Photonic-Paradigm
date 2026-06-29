#!/usr/bin/env python3
"""
OBQC / SCD Hybrid RGBW Decoder Simulation

This script simulates a near-term deterministic Optical Bead Computing (OBQC)
decoder using:

- 4 optical channels: R, G, B, W
- 10 soroban-coded decimal (SCD) digit patterns: 0-9
- 1 active-channel marker bit per optical channel
- nearest-neighbor decoding with confidence, margin, error-risk, and reject logic

Total symbolic states:
    4 channels x 10 SCD digit patterns = 40 states

Important correction:
    Without an active-channel marker, digit 0 is all-zero in every channel,
    so R0, G0, B0, and W0 collapse into the same vector. This script adds
    a marker bit M to each channel so that all 40 states are structurally unique.

Layer 5 framing:
    The correction / verification layer should reject uncertain optical readings
    instead of forcing an output when the signal is ambiguous. A reject event is
    treated as a calibration or re-measurement request, not as a successful decode.

This is an illustrative simulation, not a validated CMOS/LED hardware model.
Observed zero error in a finite run does not prove true zero error in hardware.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np


CHANNELS = ("R", "G", "B", "W")


# Canonical 5-bit soroban/SCD-like decimal patterns:
# [H, L4, L3, L2, L1]
#
# H  = five-bead equivalent
# L* = lower one-bead equivalents
#
# 0 is intentionally all-zero. The separate marker bit M identifies
# the active color channel so that R0/G0/B0/W0 remain distinguishable.
SOROBAN_SCD_PATTERNS: Dict[int, np.ndarray] = {
    0: np.array([0, 0, 0, 0, 0], dtype=float),
    1: np.array([0, 0, 0, 0, 1], dtype=float),
    2: np.array([0, 0, 0, 1, 1], dtype=float),
    3: np.array([0, 0, 1, 1, 1], dtype=float),
    4: np.array([0, 1, 1, 1, 1], dtype=float),
    5: np.array([1, 0, 0, 0, 0], dtype=float),
    6: np.array([1, 0, 0, 0, 1], dtype=float),
    7: np.array([1, 0, 0, 1, 1], dtype=float),
    8: np.array([1, 0, 1, 1, 1], dtype=float),
    9: np.array([1, 1, 1, 1, 1], dtype=float),
}


@dataclass(frozen=True)
class DecodeResult:
    decoded_state: Optional[int]
    best_state: int
    second_state: int
    best_distance: float
    second_distance: float
    margin: float
    confidence: float
    error_risk: float
    status: str
    reject_reason: str


@dataclass(frozen=True)
class TrialSummary:
    noise_level: float
    iterations: int
    accuracy: float
    accepted_accuracy: float
    error_rate: float
    false_accept_rate: float
    false_accept_rate_of_accepted: float
    reject_rate: float
    calibration_request_rate: float
    accepted_count: int
    rejected_count: int
    correct_accept_count: int
    false_accept_count: int
    mean_margin: float
    min_margin: float
    mean_best_distance: float
    mean_confidence: float
    mean_error_risk: float


class OBQCHybridDecoder:
    """
    Hybrid OBQC/SCD decoder using nearest-neighbor decoding.

    Each state is represented as a 4 x 6 matrix:

        channel rows: R, G, B, W
        columns:      M, H, L4, L3, L2, L1

    M is an active-channel marker.
    H/L* are the 5-bit soroban-coded decimal pattern.

    The decoder provides:
    - best / second-best distance
    - margin
    - confidence
    - error-risk estimate
    - reject logic for uncertain readings
    """

    def __init__(
        self,
        noise_level: float = 0.05,
        signal_gain: float = 1.0,
        background_level: float = 0.0,
        crosstalk: float = 0.0,
        quantization_levels: Optional[int] = None,
        reject_threshold: Optional[float] = None,
        margin_threshold: Optional[float] = None,
        confidence_threshold: Optional[float] = None,
        error_risk_threshold: Optional[float] = None,
        confidence_temperature: float = 0.25,
        seed: int = 42,
    ) -> None:
        if noise_level < 0:
            raise ValueError("noise_level must be non-negative.")
        if signal_gain <= 0:
            raise ValueError("signal_gain must be positive.")
        if background_level < 0:
            raise ValueError("background_level must be non-negative.")
        if not 0 <= crosstalk < 1:
            raise ValueError("crosstalk must satisfy 0 <= crosstalk < 1.")
        if quantization_levels is not None and quantization_levels < 2:
            raise ValueError("quantization_levels must be None or >= 2.")
        if confidence_temperature <= 0:
            raise ValueError("confidence_temperature must be positive.")

        self.noise_level = float(noise_level)
        self.signal_gain = float(signal_gain)
        self.background_level = float(background_level)
        self.crosstalk = float(crosstalk)
        self.quantization_levels = quantization_levels
        self.reject_threshold = reject_threshold
        self.margin_threshold = margin_threshold
        self.confidence_threshold = confidence_threshold
        self.error_risk_threshold = error_risk_threshold
        self.confidence_temperature = float(confidence_temperature)
        self.rng = np.random.default_rng(seed)

        self.state_to_symbol: Dict[int, Tuple[str, int]] = {}
        self.symbol_to_state: Dict[Tuple[str, int], int] = {}
        self.templates = self._generate_templates()
        self._validate_unique_templates()

    def _generate_templates(self) -> Dict[int, np.ndarray]:
        templates: Dict[int, np.ndarray] = {}
        state = 0

        for channel_index, channel in enumerate(CHANNELS):
            for digit in range(10):
                matrix = np.zeros((len(CHANNELS), 6), dtype=float)

                # Active channel marker M.
                matrix[channel_index, 0] = 1.0

                # SCD digit pattern [H, L4, L3, L2, L1].
                matrix[channel_index, 1:] = SOROBAN_SCD_PATTERNS[digit]

                templates[state] = (matrix * self.signal_gain).flatten()
                self.state_to_symbol[state] = (channel, digit)
                self.symbol_to_state[(channel, digit)] = state
                state += 1

        return templates

    def _validate_unique_templates(self) -> None:
        unique_templates = {tuple(template.tolist()) for template in self.templates.values()}
        if len(unique_templates) != len(self.templates):
            raise ValueError(
                f"Template collision detected: {len(unique_templates)} unique templates "
                f"for {len(self.templates)} states."
            )

    @staticmethod
    def demonstrate_zero_collision_without_marker() -> Dict[str, Tuple[int, ...]]:
        """
        Show why the marker bit is necessary.

        Without M, digit 0 in every channel is all-zero, so R0/G0/B0/W0 collide.
        """
        zero_digit = SOROBAN_SCD_PATTERNS[0]
        collisions: Dict[str, Tuple[int, ...]] = {}

        for channel_index, channel in enumerate(CHANNELS):
            matrix = np.zeros((len(CHANNELS), 5), dtype=int)
            matrix[channel_index, :] = zero_digit.astype(int)
            collisions[f"{channel}0"] = tuple(matrix.flatten().tolist())

        return collisions

    def _apply_crosstalk(self, clean_matrix: np.ndarray) -> np.ndarray:
        """
        Simplified channel crosstalk model.

        crosstalk=0.0 means no leakage.
        crosstalk=0.03 means a small portion of energy leaks across channels.

        This is not a full optical sensor model; it is a stress-test parameter.
        """
        if self.crosstalk <= 0:
            return clean_matrix

        total_by_position = clean_matrix.sum(axis=0)
        leaked = np.zeros_like(clean_matrix)

        for channel_index in range(len(CHANNELS)):
            own = clean_matrix[channel_index]
            other_total = total_by_position - own
            leaked[channel_index] = (
                own * (1.0 - self.crosstalk)
                + other_total * (self.crosstalk / (len(CHANNELS) - 1))
            )

        return leaked

    def _apply_quantization(self, signal: np.ndarray) -> np.ndarray:
        if self.quantization_levels is None:
            return signal

        upper = self.signal_gain + self.background_level
        normalized = np.clip(signal / upper, 0.0, 1.0)
        quantized = np.round(normalized * (self.quantization_levels - 1)) / (
            self.quantization_levels - 1
        )
        return quantized * upper

    def simulate_hardware_signal(self, target_state: int) -> np.ndarray:
        """
        Generate a noisy sensor-like reading for a target state.

        Modeled effects:
        - channel crosstalk
        - background illumination
        - additive Gaussian noise
        - clipping / saturation
        - optional ADC-like quantization
        """
        if target_state not in self.templates:
            raise ValueError("target_state must be between 0 and 39.")

        ideal = self.templates[target_state].reshape(len(CHANNELS), 6)
        signal = self._apply_crosstalk(ideal)
        signal = signal + self.background_level

        noise = self.rng.normal(0.0, self.noise_level, signal.shape)
        signal = signal + noise

        upper = self.signal_gain + self.background_level
        signal = np.clip(signal, 0.0, upper)
        signal = self._apply_quantization(signal)

        return signal.flatten()

    def _confidence_from_top_two_distances(self, d1: float, d2: float) -> float:
        """
        Convert the top-two distances into a bounded confidence proxy.

        This is not a calibrated probability. It is a monotonic confidence score:
        the score rises when the best state is much closer than the second-best state.
        """
        # Stable two-class softmax over negative distances.
        z1 = -d1 / self.confidence_temperature
        z2 = -d2 / self.confidence_temperature
        zmax = max(z1, z2)
        e1 = math.exp(z1 - zmax)
        e2 = math.exp(z2 - zmax)
        return float(e1 / (e1 + e2))

    def decode_nearest_neighbor(self, noisy_signal: np.ndarray) -> DecodeResult:
        distances: List[Tuple[float, int]] = []

        for state, template in self.templates.items():
            distance = float(np.linalg.norm(noisy_signal - template))
            distances.append((distance, state))

        distances.sort(key=lambda item: item[0])

        best_distance, best_state = distances[0]
        second_distance, second_state = distances[1]
        margin = second_distance - best_distance

        confidence = self._confidence_from_top_two_distances(best_distance, second_distance)
        error_risk = 1.0 - confidence

        reject_reason = ""

        if self.reject_threshold is not None and best_distance > self.reject_threshold:
            reject_reason = "best_distance_above_threshold"
        elif self.margin_threshold is not None and margin < self.margin_threshold:
            reject_reason = "margin_below_threshold"
        elif self.confidence_threshold is not None and confidence < self.confidence_threshold:
            reject_reason = "confidence_below_threshold"
        elif self.error_risk_threshold is not None and error_risk > self.error_risk_threshold:
            reject_reason = "error_risk_above_threshold"

        if reject_reason:
            return DecodeResult(
                decoded_state=None,
                best_state=best_state,
                second_state=second_state,
                best_distance=best_distance,
                second_distance=second_distance,
                margin=margin,
                confidence=confidence,
                error_risk=error_risk,
                status="REJECT",
                reject_reason=reject_reason,
            )

        return DecodeResult(
            decoded_state=best_state,
            best_state=best_state,
            second_state=second_state,
            best_distance=best_distance,
            second_distance=second_distance,
            margin=margin,
            confidence=confidence,
            error_risk=error_risk,
            status="ACCEPT",
            reject_reason="",
        )

    def run_stress_test(self, iterations: int = 10_000) -> Tuple[TrialSummary, np.ndarray]:
        if iterations <= 0:
            raise ValueError("iterations must be positive.")

        false_accepts = 0
        correct_accepts = 0
        rejects = 0

        margins: List[float] = []
        best_distances: List[float] = []
        confidences: List[float] = []
        error_risks: List[float] = []
        confusion = np.zeros((40, 40), dtype=int)

        for _ in range(iterations):
            target_state = int(self.rng.integers(0, 40))
            received = self.simulate_hardware_signal(target_state)
            result = self.decode_nearest_neighbor(received)

            margins.append(result.margin)
            best_distances.append(result.best_distance)
            confidences.append(result.confidence)
            error_risks.append(result.error_risk)

            if result.decoded_state is None:
                rejects += 1
                continue

            confusion[target_state, result.decoded_state] += 1

            if result.decoded_state == target_state:
                correct_accepts += 1
            else:
                false_accepts += 1

        accepted_count = correct_accepts + false_accepts
        accuracy = correct_accepts / iterations
        error_rate = false_accepts / iterations
        reject_rate = rejects / iterations
        accepted_accuracy = correct_accepts / accepted_count if accepted_count else 0.0
        false_accept_rate_of_accepted = false_accepts / accepted_count if accepted_count else 0.0

        summary = TrialSummary(
            noise_level=self.noise_level,
            iterations=iterations,
            accuracy=accuracy,
            accepted_accuracy=accepted_accuracy,
            error_rate=error_rate,
            false_accept_rate=error_rate,
            false_accept_rate_of_accepted=false_accept_rate_of_accepted,
            reject_rate=reject_rate,
            calibration_request_rate=reject_rate,
            accepted_count=accepted_count,
            rejected_count=rejects,
            correct_accept_count=correct_accepts,
            false_accept_count=false_accepts,
            mean_margin=float(np.mean(margins)),
            min_margin=float(np.min(margins)),
            mean_best_distance=float(np.mean(best_distances)),
            mean_confidence=float(np.mean(confidences)),
            mean_error_risk=float(np.mean(error_risks)),
        )

        return summary, confusion


def sweep_noise_levels(
    noise_levels: Iterable[float],
    iterations: int,
    signal_gain: float,
    background_level: float,
    crosstalk: float,
    quantization_levels: Optional[int],
    reject_threshold: Optional[float],
    margin_threshold: Optional[float],
    confidence_threshold: Optional[float],
    error_risk_threshold: Optional[float],
    confidence_temperature: float,
    seed: int,
) -> List[TrialSummary]:
    rows: List[TrialSummary] = []

    for index, noise_level in enumerate(noise_levels):
        decoder = OBQCHybridDecoder(
            noise_level=noise_level,
            signal_gain=signal_gain,
            background_level=background_level,
            crosstalk=crosstalk,
            quantization_levels=quantization_levels,
            reject_threshold=reject_threshold,
            margin_threshold=margin_threshold,
            confidence_threshold=confidence_threshold,
            error_risk_threshold=error_risk_threshold,
            confidence_temperature=confidence_temperature,
            seed=seed + index,
        )
        summary, _ = decoder.run_stress_test(iterations=iterations)
        rows.append(summary)

    return rows


def write_summary_csv(rows: List[TrialSummary], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dict__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def print_summary(summary: TrialSummary) -> None:
    print("OBQC / SCD Hybrid Decoder Simulation")
    print("-------------------------------------")
    print(f"Noise level:                  {summary.noise_level:.4f}")
    print(f"Iterations:                   {summary.iterations}")
    print(f"Accepted count:               {summary.accepted_count}")
    print(f"Rejected count:               {summary.rejected_count}")
    print(f"Correct accepted count:       {summary.correct_accept_count}")
    print(f"False accepted count:         {summary.false_accept_count}")
    print(f"Correct output rate / total:  {summary.accuracy * 100:.4f}%")
    print(f"Accepted accuracy:            {summary.accepted_accuracy * 100:.4f}%")
    print(f"False accept rate / total:    {summary.false_accept_rate * 100:.4f}%")
    print(f"False accept rate / accepted: {summary.false_accept_rate_of_accepted * 100:.4f}%")
    print(f"Reject rate:                  {summary.reject_rate * 100:.4f}%")
    print(f"Calibration request rate:     {summary.calibration_request_rate * 100:.4f}%")
    print(f"Mean margin:                  {summary.mean_margin:.6f}")
    print(f"Minimum margin:               {summary.min_margin:.6f}")
    print(f"Mean best distance:           {summary.mean_best_distance:.6f}")
    print(f"Mean confidence:              {summary.mean_confidence:.6f}")
    print(f"Mean error risk:              {summary.mean_error_risk:.6f}")

    if summary.false_accept_count == 0:
        print("Note: observed zero false accepts in this finite run does not prove true zero false-accept risk.")
    if summary.false_accept_rate > 0.05:
        print("Warning: false accept rate exceeds 5%. Consider increasing signal margin, sensing area, shielding, redundancy, or stricter rejection thresholds.")
    if summary.reject_rate > 0.50:
        print("Warning: reject rate exceeds 50%. The system may be safe but inefficient under the current thresholds.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate a 40-state RGBW + SCD hybrid OBQC decoder with confidence and reject logic."
    )
    parser.add_argument("--noise", type=float, default=0.05, help="Gaussian noise standard deviation.")
    parser.add_argument("--iterations", type=int, default=10_000, help="Trials per run.")
    parser.add_argument("--signal-gain", type=float, default=1.0, help="Ideal active signal amplitude.")
    parser.add_argument("--background", type=float, default=0.0, help="Background light level.")
    parser.add_argument("--crosstalk", type=float, default=0.02, help="Simplified channel crosstalk ratio.")
    parser.add_argument(
        "--quantization-levels",
        type=int,
        default=None,
        help="Optional ADC quantization levels, e.g. 256.",
    )
    parser.add_argument("--reject-threshold", type=float, default=None, help="Reject if best distance exceeds this value.")
    parser.add_argument("--margin-threshold", type=float, default=None, help="Reject if nearest/second-nearest margin is below this value.")
    parser.add_argument("--confidence-threshold", type=float, default=None, help="Reject if confidence is below this value.")
    parser.add_argument("--error-risk-threshold", type=float, default=None, help="Reject if error risk is above this value.")
    parser.add_argument("--confidence-temperature", type=float, default=0.25, help="Softmax temperature for confidence proxy.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")

    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run a noise sweep from 0.00 to --noise instead of a single run.",
    )
    parser.add_argument("--sweep-steps", type=int, default=21, help="Number of noise sweep steps.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("simulator/results/obqc_hybrid_decoder_sweep.csv"),
        help="CSV output path for sweep results.",
    )

    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    collisions = OBQCHybridDecoder.demonstrate_zero_collision_without_marker()
    unique_without_marker = len(set(collisions.values()))

    if unique_without_marker != len(collisions):
        print("Marker-bit check: without M, R0/G0/B0/W0 collide. This model uses M to avoid that collision.")

    if args.sweep:
        if args.sweep_steps < 2:
            raise ValueError("--sweep-steps must be at least 2.")
        noise_levels = np.linspace(0.0, args.noise, args.sweep_steps)
        rows = sweep_noise_levels(
            noise_levels=noise_levels,
            iterations=args.iterations,
            signal_gain=args.signal_gain,
            background_level=args.background,
            crosstalk=args.crosstalk,
            quantization_levels=args.quantization_levels,
            reject_threshold=args.reject_threshold,
            margin_threshold=args.margin_threshold,
            confidence_threshold=args.confidence_threshold,
            error_risk_threshold=args.error_risk_threshold,
            confidence_temperature=args.confidence_temperature,
            seed=args.seed,
        )
        write_summary_csv(rows, args.csv)
        print(f"Wrote sweep CSV: {args.csv}")
        print_summary(rows[-1])
        return

    decoder = OBQCHybridDecoder(
        noise_level=args.noise,
        signal_gain=args.signal_gain,
        background_level=args.background,
        crosstalk=args.crosstalk,
        quantization_levels=args.quantization_levels,
        reject_threshold=args.reject_threshold,
        margin_threshold=args.margin_threshold,
        confidence_threshold=args.confidence_threshold,
        error_risk_threshold=args.error_risk_threshold,
        confidence_temperature=args.confidence_temperature,
        seed=args.seed,
    )
    summary, _ = decoder.run_stress_test(iterations=args.iterations)
    print_summary(summary)


if __name__ == "__main__":
    main()
