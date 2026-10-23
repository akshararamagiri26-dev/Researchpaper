"""Reproducible prototype for knowledge-guided AI decision support.

The bundled benchmark is SYNTHETIC and is intended to test the pipeline, not to
support claims about real organizations. Replace --data with a governed CSV to
run the same evaluation on empirical observations.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
FEATURES = ["strategic_alignment", "data_readiness", "digital_capability", "expected_benefit", "investment_cost", "implementation_risk"]


def synthetic_data(n: int, seed: int) -> pd.DataFrame:
    """Create a transparent toy benchmark with known latent outcome mechanism."""
    rng = np.random.default_rng(seed)
    x = pd.DataFrame({
        "strategic_alignment": rng.uniform(0, 1, n),
        "data_readiness": rng.uniform(0, 1, n),
        "digital_capability": rng.uniform(0, 1, n),
        "expected_benefit": rng.uniform(0.05, 1, n),
        "investment_cost": rng.uniform(0.05, 1, n),
        "implementation_risk": rng.uniform(0, 1, n),
    })
    utility = (0.24*x.strategic_alignment + 0.19*x.data_readiness
               + 0.18*x.digital_capability + 0.25*x.expected_benefit
               - 0.11*x.investment_cost - 0.17*x.implementation_risk
               + 0.14*x.strategic_alignment*x.data_readiness
               + 0.10*x.expected_benefit*(1-x.implementation_risk)
               - 0.07*(x.investment_cost**2))
    x["observed_outcome"] = utility + rng.normal(0, 0.06, n)
    return x


def knowledge_score(df: pd.DataFrame) -> np.ndarray:
    """Explicit, inspectable domain-rule score; coefficients are hypotheses."""
    return (0.24*df.strategic_alignment + 0.19*df.data_readiness
            + 0.18*df.digital_capability + 0.25*df.expected_benefit
            - 0.11*df.investment_cost - 0.17*df.implementation_risk
            + 0.10*df.expected_benefit*(1-df.implementation_risk))


def topk_metrics(y: np.ndarray, score: np.ndarray, fraction: float = 0.2) -> tuple[float, float, float]:
    y = np.asarray(y, dtype=float).ravel()
    score = np.asarray(score, dtype=float).ravel()
    y_ndcg = y - min(0.0, float(np.min(y)))
    k = max(1, int(np.ceil(len(y)*fraction)))
    ndcg = float(ndcg_score(y_ndcg.reshape(1, -1), score.reshape(1, -1), k=k))
    selected = np.argsort(score)[-k:]
    oracle = np.sort(y)[-k:]
    regret = float(np.mean(oracle) - np.mean(y[selected]))
    rho = float(spearmanr(y, score).statistic)
    return ndcg, regret, rho


def load_data(path: str | None, n: int, seed: int) -> pd.DataFrame:
    if path:
        df = pd.read_csv(path)
        required = set(FEATURES + ["observed_outcome"])
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"CSV missing required columns: {sorted(missing)}")
        df = df[FEATURES + ["observed_outcome"]].dropna().copy()
        if len(df) < 100:
            raise ValueError("Need at least 100 complete rows for train/validation/test splits.")
        return df
    return synthetic_data(n, seed)


def evaluate_one(df: pd.DataFrame, seed: int) -> tuple[pd.DataFrame, dict]:
    train, hold = train_test_split(df, test_size=0.4, random_state=seed)
    valid, test = train_test_split(hold, test_size=0.5, random_state=seed+1000)
    model = RandomForestRegressor(n_estimators=300, min_samples_leaf=4,
                                  max_features=0.9, random_state=seed, n_jobs=-1)
    model.fit(train[FEATURES], train.observed_outcome)
    yv = valid.observed_outcome.to_numpy()
    yt = test.observed_outcome.to_numpy()
    pv = model.predict(valid[FEATURES]); pt = model.predict(test[FEATURES])
    kv = knowledge_score(valid); kt = knowledge_score(test)
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    alpha = max(alphas, key=lambda a: topk_metrics(yv, a*kv+(1-a)*pv)[0])
    scores = {
        "Data-driven AI": pt,
        "Knowledge rules": kt,
        "Knowledge-guided hybrid": alpha*kt+(1-alpha)*pt,
        "Benefit-cost heuristic": test.expected_benefit.to_numpy()/(0.15+test.investment_cost.to_numpy()),
    }
    rows = []
    for name, score in scores.items():
        ndcg, regret, rho = topk_metrics(yt, np.asarray(score))
        rows.append({"method": name, "ndcg_at_20pct": ndcg, "top_k_regret": regret,
                     "spearman_rho": rho,
                     "selected_knowledge_weight": alpha if name == "Knowledge-guided hybrid" else np.nan})
    return pd.DataFrame(rows), {"n_total": len(df), "n_train": len(train),
        "n_validation": len(valid), "n_test": len(test), "hybrid_knowledge_weight": alpha}


def make_figures(metrics: pd.DataFrame) -> None:
    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 3.2)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    boxes = [(0.02, "Organizational\ndata"), (0.22, "Knowledge layer\n(rules + constraints)"),
             (0.43, "Predictive AI\n(model + validation)"),
             (0.64, "Knowledge-guided\nranking + explanation"),
             (0.84, "Managerial\ndecision + feedback")]
    for x, label in boxes:
        ax.text(x+0.07, 0.52, label, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.55", fc="#eef3f8", ec="#375a7f", lw=1.2))
    for i in range(len(boxes)-1):
        ax.annotate("", xy=(boxes[i+1][0], 0.52), xytext=(boxes[i][0]+0.14, 0.52),
                    arrowprops=dict(arrowstyle="->", lw=1.4, color="#444"))
    ax.text(0.5, 0.12, "Governance: data quality • audit trail • human review • outcome monitoring",
            ha="center", fontsize=9)
    fig.tight_layout(); fig.savefig(OUT/"figure_1_architecture.png", dpi=300, bbox_inches="tight"); plt.close(fig)
    means = metrics.groupby("method").agg(ndcg=("ndcg_at_20pct", "mean"),
        sd=("ndcg_at_20pct", "std")).sort_values("ndcg")
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    ax.barh(means.index, means.ndcg, xerr=means.sd.fillna(0), capsize=3)
    ax.set_xlabel("NDCG@20% (higher is better)")
    ax.set_title("Synthetic benchmark: ranking quality across random seeds")
    ax.grid(axis="x", alpha=0.25); fig.tight_layout()
    fig.savefig(OUT/"figure_2_benchmark.png", dpi=300, bbox_inches="tight"); plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", help="CSV with six features and observed_outcome; omit for synthetic demo")
    p.add_argument("--n", type=int, default=1200, help="synthetic rows per seed")
    p.add_argument("--seeds", type=int, default=10, help="independent random seeds")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    if args.n < 100 or args.seeds < 2:
        raise SystemExit("Use --n >= 100 and --seeds >= 2.")
    all_rows=[]; split_meta=[]
    for i in range(args.seeds):
        df = load_data(args.data, args.n, args.seed+i)
        result, meta = evaluate_one(df, args.seed+i)
        result["seed"] = args.seed+i; all_rows.append(result); split_meta.append(meta)
    raw = pd.concat(all_rows, ignore_index=True)
    OUT.mkdir(exist_ok=True)
    raw.to_csv(OUT/"run_metrics.csv", index=False)
    summary = raw.groupby("method").agg(
        ndcg_mean=("ndcg_at_20pct", "mean"), ndcg_sd=("ndcg_at_20pct", "std"),
        regret_mean=("top_k_regret", "mean"), regret_sd=("top_k_regret", "std"),
        spearman_mean=("spearman_rho", "mean"), spearman_sd=("spearman_rho", "std")
    ).reset_index()
    summary.to_csv(OUT/"table_2_performance.csv", index=False)
    pd.DataFrame([{"n_total": int(np.mean([m["n_total"] for m in split_meta])),
        "n_train_per_seed": int(np.mean([m["n_train"] for m in split_meta])),
        "n_validation_per_seed": int(np.mean([m["n_validation"] for m in split_meta])),
        "n_test_per_seed": int(np.mean([m["n_test"] for m in split_meta])),
        "seeds": args.seeds,
        "data_source": "user CSV" if args.data else "synthetic demonstration"}]).to_csv(
            OUT/"table_1_data_profile.csv", index=False)
    make_figures(raw)
    print("\nTABLE 2 — performance summary (mean ± SD across seeds)")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nOutputs written to: {OUT}")
    print("WARNING: synthetic-demo results are software validation only, not evidence about real organizations.")

if __name__ == "__main__":
    main()
