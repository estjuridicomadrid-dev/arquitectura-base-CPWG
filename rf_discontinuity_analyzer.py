#!/usr/bin/env python3
"""Estimate CPWG impedance and reflection at a geometry transition."""

import argparse
import json
import math
from dataclasses import asdict, dataclass


def _elliptic_k(modulus: float) -> float:
    """Return the complete elliptic integral of the first kind using AGM."""
    if not 0.0 < modulus < 1.0:
        raise ValueError("elliptic modulus must be between 0 and 1")

    arithmetic_mean = 1.0
    geometric_mean = math.sqrt(1.0 - modulus * modulus)
    for _ in range(100):
        next_arithmetic = (arithmetic_mean + geometric_mean) / 2.0
        next_geometric = math.sqrt(arithmetic_mean * geometric_mean)
        if abs(next_arithmetic - next_geometric) <= 1e-15 * next_arithmetic:
            return math.pi / (2.0 * next_arithmetic)
        arithmetic_mean = next_arithmetic
        geometric_mean = next_geometric
    raise ArithmeticError("elliptic integral did not converge")


def estimate_impedance(width_mm: float, gap_mm: float, epsilon_r: float) -> float:
    """Estimate CPWG impedance in ohms using an infinite-ground CPW model."""
    values = (width_mm, gap_mm, epsilon_r)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("width, gap, and relative permittivity must be finite")
    if width_mm <= 0.0 or gap_mm <= 0.0:
        raise ValueError("width and gap must be greater than zero")
    if epsilon_r < 1.0:
        raise ValueError("relative permittivity must be at least 1")

    modulus = width_mm / (width_mm + 2.0 * gap_mm)
    effective_permittivity = (epsilon_r + 1.0) / 2.0
    return (
        30.0
        * math.pi
        / math.sqrt(effective_permittivity)
        * _elliptic_k(math.sqrt(1.0 - modulus * modulus))
        / _elliptic_k(modulus)
    )


@dataclass(frozen=True)
class TransitionAnalysis:
    impedance_before_ohm: float
    impedance_after_ohm: float
    reflection_coefficient: float
    return_loss_db: float
    vswr: float


def analyze_transition(
    width_before_mm: float,
    gap_before_mm: float,
    width_after_mm: float,
    gap_after_mm: float,
    epsilon_r: float,
) -> TransitionAnalysis:
    """Estimate the impedance step and its voltage-wave reflection."""
    impedance_before = estimate_impedance(width_before_mm, gap_before_mm, epsilon_r)
    impedance_after = estimate_impedance(width_after_mm, gap_after_mm, epsilon_r)
    reflection = (impedance_after - impedance_before) / (
        impedance_after + impedance_before
    )
    magnitude = abs(reflection)
    return TransitionAnalysis(
        impedance_before_ohm=impedance_before,
        impedance_after_ohm=impedance_after,
        reflection_coefficient=reflection,
        return_loss_db=math.inf if magnitude == 0.0 else -20.0 * math.log10(magnitude),
        vswr=math.inf if magnitude == 1.0 else (1.0 + magnitude) / (1.0 - magnitude),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width-before", type=float, required=True, help="mm")
    parser.add_argument("--gap-before", type=float, required=True, help="mm")
    parser.add_argument("--width-after", type=float, required=True, help="mm")
    parser.add_argument("--gap-after", type=float, required=True, help="mm")
    parser.add_argument("--epsilon-r", type=float, required=True)
    args = parser.parse_args()
    result = analyze_transition(
        args.width_before,
        args.gap_before,
        args.width_after,
        args.gap_after,
        args.epsilon_r,
    )
    output = asdict(result)
    if not math.isfinite(output["return_loss_db"]):
        output["return_loss_db"] = None
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
