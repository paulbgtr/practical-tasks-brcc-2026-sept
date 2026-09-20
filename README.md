# Practical Tasks — BRCC 2026 Sept

## Task 1 — aFRR activation vs. imbalance (Baltic Transparency Dashboard)

Retrieves aFRR activation and imbalance volume data for the Baltic states
(22.09.2025) via the Transparency Dashboard API, computes coverage/direction
metrics, and produces a comparison graph.

- `task-1/main.py` — data retrieval, metric calculation, plotting
- `task-1/aFRR_vs_imbalance_20250922.png` — resulting graph
- `task-1/summary.csv` — per-area metric summary
- `task-1/reasoning.md` — assessment, theoretical background, findings

Run with:
```zsh
pip install -r requirements.txt
cd task-1
python main.py
```

## Task 2 — CGMES EQ profile analysis

Answers to structural/physical questions about a CGMES EQ model (generators,
transformer windings, line limits, slack node) plus a list of found modeling
errors, based on manual inspection of the provided XML.

- `task-2/20210325T1530Z_1D_NL_EQ_001_2026.xml` — the provided model file
- `task-2/reasoning.md` — answers to all 5 questions
