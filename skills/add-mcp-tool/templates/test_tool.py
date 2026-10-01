"""tests/test_tools/test_vehicle.py — mẫu test tool đọc (tool ghi: tests/test_executor/)."""

from src.agents.tools.vehicle import get_vehicle_status


def test_known_vin_returns_status(seeded_world):
    out = get_vehicle_status.invoke({"vin": "VF8-4821"})
    assert out["odometer_km"] >= 0


def test_unknown_vin_returns_structured_error(seeded_world):
    out = get_vehicle_status.invoke({"vin": "NOPE"})
    assert out["error"]["code"] == "VEHICLE_NOT_FOUND"


# Tool GHI: gọi 2 lần cùng idempotency_key → chỉ 1 thay đổi trạng thái (đặt ở tests/test_executor/).
