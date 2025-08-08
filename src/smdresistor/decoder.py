"""
SMD resistor code decoder.
Supports:
- 3-digit (e.g., 103 => 10kΩ)
- 4-digit (e.g., 1002 => 10kΩ)
- R-as-decimal (e.g., 4R7 => 4.7Ω, 0R0 => 0Ω)
- EIA-96 (e.g., 01C, 68X)
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Optional, Tuple

# EIA-96 base values corresponding to codes 01..96
# Source: Standard E96 series
EIA96_BASES = [
    100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130,
    133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174,
    178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232,
    237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
    316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412,
    422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549,
    562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732,
    750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976,
]

# EIA-96 multiplier letters
EIA96_MULTIPLIERS = {
    "Z": 1e-3,
    "Y": 1e-2,
    "R": 1e-2,  # sometimes R is used for 0.01 as well
    "X": 1e-1,
    "S": 1e-1,  # sometimes S is used for 0.1
    "A": 1,
    "B": 10,
    "H": 10,    # H sometimes used for 10
    "C": 100,
    "D": 1_000,
    "E": 10_000,
    "F": 100_000,
}

_R_CODE_RE = re.compile(r"(?i)^(\d*)r(\d*)$")  # e.g., 4R7, 0R0
_EIA96_RE = re.compile(r"(?i)^(\d{2})([a-z])$")  # e.g., 01C
_DIGIT_RE = re.compile(r"^(\d{3,4})$")           # 3- or 4-digit

@dataclass
class DecodeResult:
    ohms: float
    scheme: str


def decode(code: str) -> DecodeResult:
    """Decode an SMD resistor code string to ohms.

    Raises ValueError if the code is not recognized.
    """
    if not isinstance(code, str) or not code.strip():
        raise ValueError("code must be a non-empty string")

    s = code.strip().replace(" ", "").upper()

    # R-as-decimal, like 4R7 or 0R0
    m = _R_CODE_RE.match(s)
    if m:
        int_part, frac_part = m.groups()
        int_part = int_part or "0"
        frac_part = frac_part or "0"
        try:
            value = float(f"{int(int_part)}.{frac_part}")
        except Exception as e:
            raise ValueError(f"invalid R-code: {code}") from e
        return DecodeResult(ohms=value, scheme="R")

    # EIA-96 like 01C
    m = _EIA96_RE.match(s)
    if m:
        num_str, letter = m.groups()
        idx = int(num_str)
        if not (1 <= idx <= 96):
            raise ValueError(f"EIA-96 index out of range: {num_str}")
        base = EIA96_BASES[idx - 1]
        mult = EIA96_MULTIPLIERS.get(letter)
        if mult is None:
            raise ValueError(f"unknown EIA-96 multiplier letter: {letter}")
        return DecodeResult(ohms=base * mult / 100.0, scheme="EIA-96")

    # 3- or 4-digit
    m = _DIGIT_RE.match(s)
    if m:
        digits = m.group(1)
        if len(digits) == 3:
            sig = int(digits[:2])
            exp = int(digits[2])
        else:  # 4-digit
            sig = int(digits[:3])
            exp = int(digits[3])
        value = sig * (10 ** exp)
        return DecodeResult(ohms=float(value), scheme=f"{len(digits)}-digit")

    raise ValueError(f"unrecognized SMD resistor code: {code}")


def format_ohms(ohms: float, precision: int = 3) -> str:
    """Format an ohms value into a human-friendly string.

    Examples: 0.0Ω, 4.7Ω, 10kΩ, 4.99MΩ
    """
    if ohms < 0:
        raise ValueError("ohms must be non-negative")

    units: Tuple[float, str] = (
        (1e6, "MΩ"),
        (1e3, "kΩ"),
        (1.0, "Ω"),
        (1e-3, "mΩ"),
    )
    for factor, suffix in units:
        if ohms >= factor:
            return f"{ohms / factor:.{precision}g}{suffix}"
    # very small
    return f"{ohms / 1e-6:.{precision}g}µΩ"

