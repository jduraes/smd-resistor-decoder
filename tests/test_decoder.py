import pytest
from smdresistor.decoder import decode, format_ohms

@pytest.mark.parametrize("code,expected_ohms", [
    ("103", 10_000.0),
    ("1002", 10_000.0),
    ("4R7", 4.7),
    ("0R0", 0.0),
])
def test_basic_codes(code, expected_ohms):
    assert pytest.approx(decode(code).ohms, rel=1e-9, abs=1e-12) == expected_ohms


def test_eia96_example():
    # 01C => base 100 with multiplier 100 => 100 * 100 / 100 = 100Ω
    res = decode("01C")
    assert pytest.approx(res.ohms, rel=1e-9) == 100.0


def test_formatting():
    assert format_ohms(4.7) == "4.7Ω"
    assert format_ohms(10_000) == "10kΩ"
    assert format_ohms(1_000_000) == "1MΩ"

