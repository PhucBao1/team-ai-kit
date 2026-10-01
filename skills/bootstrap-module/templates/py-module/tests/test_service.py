from hypothesis import given
from hypothesis import strategies as st

from src.example.models import ExampleInput  # đổi 'example' thành tên module
from src.example.service import run_example


def test_negative_odometer_returns_unknown_with_reason() -> None:
    r = run_example(ExampleInput(vin="VF8-TEST", odometer_km=-1))
    assert r.status == "UNKNOWN"
    assert r.reasons


@given(st.integers(min_value=0, max_value=1_000_000))
def test_valid_odometer_never_unknown(km: int) -> None:
    assert run_example(ExampleInput(vin="VF8-TEST", odometer_km=km)).status == "OK"
