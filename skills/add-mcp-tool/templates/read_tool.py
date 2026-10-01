"""src/agents/tools/vehicle.py — mẫu tool ĐỌC (level 0). Giữ mỏng: logic nghiệp vụ ở src/core."""

from langchain_core.tools import tool

from src.sim.world import get_world  # adapter thế giới giả lập (người B)


@tool
def get_vehicle_status(vin: str) -> dict:
    """Trạng thái xe hiện tại: model, odometer_km, soc_pct, sw_version, active_dtcs.

    Dùng trước khi tư vấn bất cứ điều gì về xe. KHÔNG dùng để đặt lịch.
    Ví dụ: {"vin": "VF8-4821"}
    """
    vehicle = get_world().vehicles.get(vin)
    if vehicle is None:
        return {"error": {"code": "VEHICLE_NOT_FOUND", "message": vin, "retryable": False}}
    return vehicle.status().model_dump()
