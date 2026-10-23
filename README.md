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
- `results/` — demonstration outputs, table-data CSVs, vector SVG/PDF versions of the two numbered figures, and a separate unnumbered graphical abstract.
- `.github/workflows/reproducibility-and-manuscript-audit.yml` — reruns the synthetic experiment, checks output schemas/split counts, builds an editable Word file, converts it to PDF, and records page count as a CI artifact.
- `make_reference_docx.py` — creates a double-spaced Word reference style for the Pandoc build. This is a review-formatting aid, not an official journal template.
- `NOVELTY_REVIEW.md` — preliminary, explicitly non-systematic scoping review and defensible contribution boundary.

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

## Editorial and research-integrity checklist
- [x] Keep the manuscript to exactly two numbered figures and two numbered tables.
- [x] Keep synthetic results explicitly labeled as a pipeline demonstration, not evidence of organizational effectiveness.
- [x] Generate vector SVG/PDF figures from the same script used for the experiment.
- [ ] Inspect the latest GitHub Actions run; confirm the experiment passes, download the generated DOCX/PDF artifact, and manually verify page count and figure/table rendering. The CI conversion is a check, not an official journal template.
- [x] Author name, affiliation, corresponding-author email, funding, competing-interest, and AI-use declarations finalized from author-confirmed details.
- [ ] Complete the title-page affiliation with the institution's full postal address and country; only the institution name has been author-confirmed so far.
- [ ] Add a CRediT contribution statement only after the author confirms the actual roles; do not infer contribution roles from tool use.
- [ ] Archive a versioned release with a persistent identifier and finalize the research-data statement.
- [ ] Before making empirical claims, use documented organizational data, validate knowledge rules with domain experts, and add ablation, sensitivity, stronger baselines, uncertainty analysis, and appropriate paired statistical tests.
- [ ] Complete a documented literature/novelty review with search databases, dates, search strings, screening criteria, and a comparison matrix. The manuscript now cites three recent adjacent reviews/frameworks but does not claim to be a systematic review or to establish novelty.
