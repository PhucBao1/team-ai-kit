from .models import ExampleInput, ExampleResult


def run_example(inp: ExampleInput) -> ExampleResult:
    """Giữ chỗ — thay bằng logic thật. Luật nghiệp vụ ghi nguồn: # kb:<doc>_v<ver>§<điều>"""
    if inp.odometer_km < 0:
        return ExampleResult(status="UNKNOWN", reasons=["odometer âm — dữ liệu xe không hợp lệ"])
    return ExampleResult(status="OK", reasons=[])
