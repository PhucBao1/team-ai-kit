from typing import Literal

from pydantic import BaseModel, ConfigDict


class ExampleInput(BaseModel):
    vin: str
    odometer_km: int


class ExampleResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    status: Literal["OK", "UNKNOWN"]
    reasons: list[str]
