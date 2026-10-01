"""Thêm vào tests/conftest.py (file template BTC) — giữ nguyên fixture client, mock_llm đã có."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


class FakeClock:
    def __init__(self, start: datetime) -> None:
        self.now = start

    def advance(self, hours: float) -> None:
        self.now += timedelta(hours=hours)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock(datetime(2026, 10, 1, 9, 0, tzinfo=VN_TZ))


@pytest.fixture
def seeded_world(clock):
    """Thế giới giả lập với seed 'default'.

    Khi src/sim có: `from src.sim.seed import build_world` rồi `return build_world("default", clock)`.
    """
    pytest.skip("src/sim chưa có seed")


class FakeLLM:
    """LLM giả cho unit test: trả lần lượt các câu/tool call đã định sẵn."""

    def __init__(self, responses: list):
        self.responses, self.calls = list(responses), []

    async def ainvoke(self, messages, **kw):
        self.calls.append(messages)
        return self.responses.pop(0)


@pytest.fixture
def fake_llm():
    return FakeLLM
