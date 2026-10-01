# eval/ — kịch bản, khách ảo, chấm điểm (owner: D) · spec `../team-ai-kit/docs/spec/22-evalmod.md` … `25-agenteval.md`

- Kịch bản YAML trong `scenarios/` (skill `add-eval-scenario`). `golden/` và kỳ vọng `hard` là hợp đồng — không sửa để test pass.
- Kết quả nộp BTC: `eval/results/report.md` (template BTC: accuracy > 80%, latency < 3s, satisfaction > 4/5, coverage > 60%, user feedback).
- So baseline B0–B3 bằng cờ trong `configs/baselines.yaml` (skill `run-eval-compare`). Báo cáo có k, pass^k, khoảng tin cậy.
