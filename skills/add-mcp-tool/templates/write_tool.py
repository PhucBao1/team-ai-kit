"""src/tools/service.py — mẫu tool GHI (level 2). CHỈ src/executor gọi; agent không import file này."""

from pydantic import BaseModel

from src.sim.world import get_world


class BookInput(BaseModel):
    option_id: str
    confirmation_token: str


class BookResult(BaseModel):
    appointment_id: str
    promise_id: str


class ToolError(BaseModel):
    code: str
    message: str
    retryable: bool = False


def book_appointment(inp: BookInput, idempotency_key: str) -> BookResult | ToolError:
    """Đặt lịch theo phương án đã được khách xác nhận. Idempotent theo option_id."""
    world = get_world()
    existing = world.appointments.find_by_idempotency(idempotency_key)
    if existing is not None:
        return BookResult(appointment_id=existing.id, promise_id=existing.promise_id)
    option = world.options.get(inp.option_id)
    if option is None or not option.is_locked():
        return ToolError(code="OPTION_EXPIRED", message=inp.option_id, retryable=False)
    appt = world.appointments.create(option, idempotency_key=idempotency_key)
    return BookResult(appointment_id=appt.id, promise_id=appt.promise_id)
