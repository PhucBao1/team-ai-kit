"""<module> — mô tả một dòng. Spec: ../team-ai-kit/docs/spec/<số>-<tên>.md"""

from .models import ExampleInput, ExampleResult
from .service import run_example

__all__ = ["ExampleInput", "ExampleResult", "run_example"]
