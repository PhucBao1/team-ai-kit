# Lệnh của đội — chạy từ gốc repo P-073:  make -f ../team-ai-kit/kit.mk <lệnh>
KIT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PY  := bash scripts/_pyrun.sh

.PHONY: check guardrails contracts diagrams test-core diagrams-export ci-local plan-check

check: guardrails contracts diagrams            ## tất cả kiểm tra của đội

guardrails:                                     ## luật kiến trúc trên file đổi so với develop
	base=$${BASE:-$$(git rev-parse -q --verify origin/develop >/dev/null && echo origin/develop || echo origin/main)}; \
	$(PY) $(KIT)/guardrails/guardrails.py ci $$base

contracts:
	$(PY) $(KIT)/guardrails/check_contracts.py

diagrams:
	$(PY) $(KIT)/guardrails/check_diagrams.py

test-core:                                      ## exit 5 = chưa có test → coi là xanh
	$(PY) -m pytest -q -x tests/test_core tests/test_executor; r=$$?; [ $$r -eq 5 ] || exit $$r

diagrams-export:                                ## sinh sơ đồ 04 từ LangGraph thật
	$(PY) $(KIT)/diagrams/export_langgraph.py

ci-local:                                       ## chạy đúng như CI BTC trước khi push
	ruff check src/ tests/ && pytest tests/ -v --tb=short

plan-check:                                      ## card không để 2 người sửa cùng file trong 1 tuần
	python3 $(KIT)/plan/check_conflicts.py
