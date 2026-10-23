# A Knowledge-Guided AI Decision System for Data-Driven Digital Transformation and Organizational Performance Optimization

**Article type:** Short communication (working draft; empirical validation required)

**Author:** [Author name]  
**Affiliation:** [Department, institution, full postal address, country]  
**Corresponding author:** [Name and institutional email]

## Abstract

Digital transformation requires organizations to prioritize initiatives under constraints involving strategic fit, data readiness, capability, expected benefit, investment, and implementation risk. Predictive models can estimate outcomes from historical data, but may not explicitly encode organizational knowledge or decision constraints. This short communication specifies a compact knowledge-guided decision-support pipeline that combines a supervised predictor with an inspectable rule-based score and selects their mixture using validation data. Four ranking strategies—data-driven prediction, explicit knowledge rules, a knowledge-guided hybrid, and a benefit-to-cost heuristic—are evaluated using normalized discounted cumulative gain at 20%, top-20% decision regret, and Spearman rank correlation. A reproducible synthetic benchmark is used only to verify the implementation and illustrate the evaluation protocol. Across ten random seeds, the hybrid attained mean NDCG@20% of 0.974 (standard deviation 0.004), compared with 0.963 (0.009) for data-driven prediction and 0.971 (0.006) for the rule score. Because the synthetic outcome mechanism is deliberately related to the illustrative rule structure, these results are not evidence of effectiveness in real organizations. The contribution is therefore a transparent, testable evaluation design rather than a validated organizational intervention. Empirical claims require evaluation on an independently documented organizational dataset, sensitivity analysis, and domain-expert validation of the knowledge rules.

**Keywords:** artificial intelligence; knowledge-based systems; data science; digital transformation; decision support; organizational performance

## 1. Introduction

Digital transformation changes how organizations create value and coordinate capabilities, but its outcomes depend on strategic responses, organizational barriers, and implementation choices rather than technology adoption alone [1]. Managers therefore need decision support that prioritizes initiatives using multiple, potentially conflicting criteria. A purely predictive model can learn associations from historical examples, while an explicit rule system can encode domain constraints but may not capture interactions in observed data. Combining the two is a plausible design hypothesis, not an established performance advantage.

This communication defines a compact knowledge-guided ranking pipeline for digital-transformation initiatives. Each candidate is represented by strategic alignment, data readiness, digital capability, expected benefit, investment cost, and implementation risk. A supervised model predicts an outcome score; a transparent knowledge score encodes provisional domain rules; and a hybrid combines the two. The mixture weight is selected on validation data and evaluated on a held-out test set. Ranking quality is measured with normalized discounted cumulative gain (NDCG), which rewards placing higher-utility candidates near the top of a ranked list [2].

The narrow research question is: **Within a transparent synthetic benchmark, does validation-tuned integration of an explicit knowledge score and a supervised predictor improve held-out ranking quality over either component alone?** The manuscript's contribution is a reproducible evaluation protocol for this design question, not a claim that the hybrid architecture is novel in the broader literature or that it improves real organizational performance. Because the benchmark is synthetic, no causal or organization-level effectiveness claim is supported.

## 2. Method

### 2.1. Decision architecture

Figure 1 presents the proposed pipeline. Organizational data are validated, an explicit knowledge layer represents provisional rules and constraints, and a predictive model is trained on a training partition. The validation partition selects the hybrid knowledge weight from {0, 0.25, 0.50, 0.75, 1.00} by NDCG@20%. The test partition is used only for final comparison. Human review and outcome monitoring remain part of the proposed decision process; the system is not intended to automate investment approval.

![Figure 1. Knowledge-guided decision-support architecture.](results/figure_1_architecture.svg)

**Figure 1.** Knowledge-guided decision-support architecture. The diagram is explanatory; it is not an observed result.

The prototype uses a random-forest regressor as the data-driven component [3]. For a candidate initiative, the explicit score is \(s_k = 0.24A + 0.19D + 0.18C + 0.25B - 0.11I - 0.17R + 0.10B(1-R)\), where \(A\) denotes strategic alignment, \(D\) data readiness, \(C\) digital capability, \(B\) expected benefit, \(I\) investment cost, and \(R\) implementation risk. These coefficients are illustrative hypotheses, not expert-validated organizational rules. The hybrid score is \(s_h = \alpha s_k + (1-\alpha)s_m\), where \(s_m\) is the random-forest prediction and \(\alpha\in\{0,0.25,0.50,0.75,1.00\}\) is selected by validation-set NDCG@20% only. The same test partition is then used to evaluate every method.

### 2.2. Benchmark and evaluation

The default benchmark draws the six features from independent uniform distributions (with expected benefit and investment cost bounded away from zero) and generates a noisy continuous outcome using \(y = 0.24A + 0.19D + 0.18C + 0.25B - 0.11I - 0.17R + 0.14AD + 0.10B(1-R) - 0.07I^2 + \epsilon\), where \(\epsilon\sim\mathcal{N}(0,0.06^2)\). The knowledge score shares several terms with this synthetic outcome mechanism; this is a deliberate limitation that may favor rule-based methods. Ten random seeds are used. For each seed, data are divided into training (60%), validation (20%), and test (20%) partitions. The same split is used for each method. Four ranking methods are compared: (i) random-forest prediction; (ii) the explicit knowledge score; (iii) the validation-tuned hybrid; and (iv) expected benefit divided by investment cost plus a small stabilizing constant.

NDCG@20% evaluates the quality of the top-ranked fifth of candidates. Top-k regret is the difference between the mean outcome of the oracle top fifth and the mean outcome among the method's selected fifth; lower is better. Spearman's \(\rho\) measures overall rank association. Results are summarized as means and standard deviations across seeds. The experiment does not report significance tests because the current synthetic exercise is a software-pipeline demonstration and not a confirmatory empirical study.

Table 1 describes the data used in the reproducibility run. The benchmark contains no observed firms, employees, investments, or organizational performance records.

**Table 1. Data profile of the reproducibility demonstration.**

| Item | Specification |
|---|---|
| Data source | Synthetic demonstration generated by the included script |
| Candidate rows per seed | 1,200 |
| Features | Strategic alignment, data readiness, digital capability, expected benefit, investment cost, implementation risk |
| Outcome | Simulated continuous utility with noise |
| Split per seed | 720 train / 240 validation / 240 test |
| Repeated runs | 10 random seeds |
| Empirical organization-level data | None |

## 3. Results

Table 2 reports the ten-seed demonstration results. The hybrid's mean NDCG@20% was 0.974 (SD 0.004), compared with 0.971 (SD 0.006) for the knowledge rules and 0.963 (SD 0.009) for data-driven prediction. The hybrid also had the lowest mean top-k regret (0.018), while the benefit-to-cost heuristic performed worst on the simulated outcome mechanism. Figure 2 visualizes mean NDCG with across-seed standard deviations. The reported standard deviations describe variation across ten synthetic runs; they are not confidence intervals and do not establish statistical significance.

**Table 2. Ranking performance on the synthetic demonstration (mean ± SD across ten seeds).**

| Method | NDCG@20% | Top-k regret (lower is better) | Spearman's \(\rho\) |
|---|---:|---:|---:|
| Benefit-to-cost heuristic | 0.784 ± 0.048 | 0.135 ± 0.022 | 0.482 ± 0.062 |
| Data-driven AI | 0.963 ± 0.009 | 0.023 ± 0.009 | 0.890 ± 0.015 |
| Knowledge rules | 0.971 ± 0.006 | 0.020 ± 0.006 | 0.913 ± 0.012 |
| Knowledge-guided hybrid | 0.974 ± 0.004 | 0.018 ± 0.005 | 0.917 ± 0.014 |

![Figure 2. Ranking quality across synthetic benchmark methods.](results/figure_2_benchmark.svg)

**Figure 2.** Mean NDCG@20% across ten synthetic random seeds; error bars represent one standard deviation. These results describe the synthetic benchmark only.

## 4. Discussion and limitations

The implementation demonstrates how explicit knowledge and supervised prediction can be compared within a common held-out ranking protocol. However, the numerical advantage of the hybrid is small in this run and cannot be generalized. Most importantly, the synthetic outcome-generating mechanism intentionally shares structure with the illustrative knowledge score. This design makes the benchmark useful for checking that the code and metrics operate as expected, but creates a favorable setting for rule-based scoring and does not independently validate the knowledge model.

A credible empirical follow-up should (1) use a documented dataset containing actual transformation initiatives and subsequent outcomes; (2) define outcomes and observation windows before model fitting; (3) elicit rules from qualified domain experts and record provenance and disagreements; (4) compare against strong, tuned baselines and ablate each knowledge component; (5) test robustness to missing data, distribution shift, weight changes, and alternative top-k cutoffs; and (6) report uncertainty and suitable paired statistical tests. If the available data are observational, the analysis should describe associations and ranking utility rather than causal effects of digital transformation. Organizational performance is multidimensional; a single outcome score may obscure differences among financial, operational, employee, and customer outcomes.

The current manuscript therefore offers a concise method and open implementation scaffold, not a completed empirical claim. The novelty of the hybrid design must also be assessed against recent knowledge-based decision-support and digital-transformation literature before submission to *Knowledge-Based Systems*.

## 5. Conclusion

This communication specifies a compact, reproducible architecture for combining explicit business knowledge with data-driven prediction when ranking digital-transformation initiatives. The code supports a validation-tuned hybrid, held-out ranking metrics, and reproducible figures and tables. Synthetic results confirm only that the evaluation pipeline runs; they do not establish that the approach improves organizational performance. The next necessary research step is a rigorous evaluation on documented empirical data with validated knowledge rules and stronger comparative analysis.

## Data and code availability

The code and synthetic-data generator are available in the associated GitHub repository. Regenerate the demonstration with `python run_experiment.py --n 1200 --seeds 10`; the script writes the performance CSV, the two table-data CSVs, and vector SVG/PDF files for the two figures. The synthetic dataset is generated on demand and is not an observed organizational dataset. No empirical organizational dataset is available for this prototype. Before submission, archive a versioned code release and persistent identifier (preferably DOI), and provide any empirical dataset used in a later study or a clear access-restriction statement, consistent with the journal's research-data requirements.

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. **Confirm or revise this statement to match the actual funding situation.**

## Declaration of competing interests

The author declares no known competing financial interests or personal relationships that could have appeared to influence the work. **Confirm this statement before submission.**

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work, the author used ChatGPT to assist with drafting and software prototyping. The author must review and edit the material, verify the analysis and references, and take full responsibility for the content of any submitted manuscript. **Revise this disclosure to reflect the actual tools and uses before submission.**

## References

[1] G. Vial, Understanding digital transformation: A review and a research agenda, *J. Strateg. Inf. Syst.* 28 (2) (2019) 118–144. https://doi.org/10.1016/j.jsis.2019.01.003.

[2] K. Järvelin, J. Kekäläinen, Cumulated gain-based evaluation of IR techniques, *ACM Trans. Inf. Syst.* 20 (4) (2002) 422–446. https://doi.org/10.1145/582415.582418.

[3] L. Breiman, Random forests, *Mach. Learn.* 45 (1) (2001) 5–32. https://doi.org/10.1023/A:1010933404324.
