# Hiệu chỉnh LLM judge + so sánh theo cặp — tham khảo

Đọc khi thêm / đổi LLM judge, hoặc khi viết phần thống kê của `eval.compare`. Luật trong `../SKILL.md` thắng file này.
Đường dẫn file nhãn dưới đây là MINH HOẠ — theo cấu trúc `eval/` thật (owner D).

## 1. Đầu ra của judge

```python
from typing import Literal
from pydantic import BaseModel

class JudgeVerdict(BaseModel):
    """Một tiêu chí soft, một quyết định nhị phân."""
    criterion: str
    verdict: Literal["PASS", "FAIL"]
    reason: str          # 1–2 câu, trích bằng chứng từ hội thoại
```

- Gọi với `with_structured_output(JudgeVerdict, method="json_schema")`, nhiệt độ 0, timeout. Lỗi parse / timeout → retry ≤ 2;
  vẫn lỗi → ghi `status: judge_error`, ca này **chạy lại**, không tính FAIL, không vào mẫu số.
- Mỗi lời gọi chấm MỘT tiêu chí với rubric ngắn (điều kiện PASS viết thành câu "PASS khi và chỉ khi …").
- Judge model ≠ họ của agent (agent gpt-4o-mini). Ghi `judge_model` + phiên bản snapshot + `judge_prompt_version` vào `config.yaml`.

## 2. Tập nhãn người

- Lấy mẫu từ trace thật của các lần chạy (đủ cả PASS và FAIL; cố ý thêm ca biên). Không dùng id kịch bản / golden làm ví dụ trong prompt judge.
- Hai người gán nhãn độc lập một phần chồng nhau để biết người với người lệch bao nhiêu; bất đồng → thảo luận, ghi luật vào rubric.
- Chia **dev** (dùng để sửa rubric / prompt judge) và **sealed** (niêm phong — đo 1 lần cho mỗi phiên bản judge, không sửa prompt theo nó).
  Gợi ý quy mô cho 3 tuần: ~40–60 mẫu / tiêu chí quan trọng, sealed ≥ 20 mẫu mỗi lớp nếu kịp; ít hơn → ghi rõ "n nhỏ", judge chỉ tham khảo.

## 3. Chỉ số (trên tập sealed)

```python
def judge_agreement(human: list[bool], judge: list[bool]) -> dict[str, float]:
    """TPR, TNR và Cohen kappa giữa nhãn người (True = PASS) và judge."""
    tp = sum(h and j for h, j in zip(human, judge))
    tn = sum((not h) and (not j) for h, j in zip(human, judge))
    pos, neg, n = sum(human), len(human) - sum(human), len(human)
    p_obs = (tp + tn) / n
    p_judge_pass = sum(judge) / n
    p_exp = (pos / n) * p_judge_pass + (neg / n) * (1 - p_judge_pass)
    kappa = (p_obs - p_exp) / (1 - p_exp) if p_exp < 1 else 1.0
    return {"tpr": tp / pos, "tnr": tn / neg, "kappa": kappa, "n": n}
```

- Cổng: **TPR ≥ 0.85 VÀ TNR ≥ 0.85** → judge được dùng làm cổng. Một trong hai < 0.85 → chỉ tham khảo (gắn cờ cho người xem lại).
- Báo κ cạnh TPR/TNR (κ thấp dù accuracy cao = judge gần như luôn trả một phía). Không báo một con số "accuracy" gộp.
- Đổi model judge, phiên bản, prompt hoặc rubric → đo lại trên sealed.

## 4. So sánh theo cặp

```python
import math

def half_width(p: float, n: int) -> float:
    """Nửa khoảng tin cậy 95% (xấp xỉ chuẩn) của tỉ lệ p trên n kịch bản."""
    return 1.96 * math.sqrt(p * (1 - p) / n)

def paired_compare(a: dict[str, bool], b: dict[str, bool]) -> dict[str, float]:
    """a, b: scenario_id -> pass (pass^k hoặc đa số k lần) trên CÙNG bộ kịch bản và seed."""
    ids = sorted(a.keys() & b.keys())
    n = len(ids)
    pa, pb = sum(a[i] for i in ids) / n, sum(b[i] for i in ids) / n
    return {"n": n, "p_a": pa, "hw_a": half_width(pa, n), "p_b": pb, "hw_b": half_width(pb, n),
            "a_only": sum(a[i] and not b[i] for i in ids), "b_only": sum(b[i] and not a[i] for i in ids)}
```

- Kết luận: `|p_a − p_b| < max(hw_a, hw_b)` → **"không chắc"**. Ngoài ra mới viết "A hơn B", kèm `a_only` / `b_only` (số kịch bản chỉ một bên pass).
- Xấp xỉ chuẩn kém khi p gần 0 hoặc 1 hoặc n nhỏ (< ~30) → coi kết luận là yếu, ghi rõ; bootstrap theo kịch bản (bước 4 của SKILL) là số chính.
- Ablation: đổi đúng MỘT yếu tố mỗi cấu hình; báo luôn các metric an toàn / chi phí / p95 của cấu hình đó để thấy thứ bị tụt.

## 5. Trước khi viết số vào báo cáo

- Mở file kết quả thật của đúng `run_id`, đọc số từ đó (không từ trí nhớ, không từ log terminal của lần khác).
- Đối chiếu `config.yaml` của lần chạy với bảng: model, prompt, dataset, seed, judge khớp.
- Có ca `judge_error` / lỗi hạ tầng chưa chạy lại → ghi số ca bị loại, không im lặng bỏ.

Nguồn ý tưởng (diễn đạt lại): wshobson/agents `llm-finetuning/skills/eval-harness-first` (+ `references/judge-calibration.md`),
`checkpoint-promotion` (MIT, commit 156b7a5e7a); google/skills `skills/cloud/agent-platform-eval-flywheel` (Apache-2.0, commit d5d905232e);
langchain-ai/langchain-skills `eval-engineering/references/verifier-design.md`, `calibration.md` (MIT, commit a76fef33ed).
