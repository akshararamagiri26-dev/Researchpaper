# Knowledge-guided AI for digital transformation decisions

Reproducible prototype accompanying a proposed short communication for *Knowledge-Based Systems*.

## Research question
Can an explicit business-knowledge layer improve the ranking of digital-transformation initiatives over data-driven prediction, rule-only scoring, and a benefit/cost heuristic?

## Important scope limitation
The bundled benchmark is **synthetic**. It validates the experimental pipeline under a toy data-generating process; it does **not** establish effectiveness in real organizations or justify real-world claims. Before journal submission, use documented empirical data, justify knowledge rules, conduct leakage and robustness checks, and revise the manuscript with empirical results.

## Compact repository
- `run_experiment.py` — data validation, synthetic benchmark, train/validation/test split, four methods, ranking metrics, and generated figures/tables.
- `manuscript.md` — short communication draft with exactly two figures and two tables.
- `requirements.txt` — runtime dependencies.
- `results/` — demonstration outputs and vector figures.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_experiment.py --n 1200 --seeds 10
```

For a supplied empirical CSV, include numeric columns `strategic_alignment`, `data_readiness`, `digital_capability`, `expected_benefit`, `investment_cost`, `implementation_risk`, and `observed_outcome`:
```bash
python run_experiment.py --data path/to/your_data.csv --seeds 10
```

## Metrics
- **NDCG@20%:** ranking quality for the top-ranked fifth.
- **Top-k regret:** gap between oracle and selected top-fifth mean outcomes; lower is better.
- **Spearman rho:** overall rank association.

## Research integrity checklist
1. Replace the synthetic demonstration with documented, legally shareable data before making empirical claims.
2. Do not describe illustrative rule weights as validated organizational knowledge.
3. Add baselines, ablations, sensitivity analysis, uncertainty estimates, and suitable statistical tests.
4. Archive data or explain access restrictions; use a persistent identifier where possible.
5. Verify all references and ensure the AI-use declaration accurately reflects actual use and author review.
