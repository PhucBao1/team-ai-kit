# PBT Library (Python / Hypothesis)

> P-073: chỉ dùng Hypothesis (đã có trong `requirements.txt`). Bảng thư viện các ngôn ngữ
> khác và phần Echidna/Medusa (Solidity) của bản gốc đã bị bỏ.

Match the project's existing choice. Introducing a second PBT library into a codebase
that already has one is not worth the property you wanted to write.

| Language | Default |
|---|---|
| Python | Hypothesis |

Detect what a repo already uses before proposing anything:

```bash
rg "from hypothesis import|import hypothesis" --type py
```

## Settings profiles (P-073 addition)

Keep CI fast and deterministic; register profiles once in `tests/conftest.py`
(shared file — tell the team before editing it):

```python
from hypothesis import settings

settings.register_profile("ci", max_examples=100, deadline=None)
settings.register_profile("dev", max_examples=20, deadline=None)
settings.load_profile("ci")
```

Per-test overrides (`@settings(max_examples=...)`) stay within the team budget in SKILL.md.
