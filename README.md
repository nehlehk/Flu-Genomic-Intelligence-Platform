# End-to-End Flu Genomic Intelligence Platform

## Overview

This project implements an end-to-end probabilistic disease surveillance pipeline for influenza genomic data. The pipeline ingests influenza sequence metadata, aggregates monthly sequence counts, applies multiple anomaly detection approaches, and uses Bayesian inference to forecast future disease activity with uncertainty-aware prediction intervals.

The primary goal is to demonstrate practical applications of:

- Statistical inference
- Bayesian forecasting
- Time-series monitoring
- Anomaly detection
- Model evaluation and validation
- MLflow experiment tracking
- Reproducible machine learning pipelines

---

## Problem Statement

Public health surveillance systems often rely on fixed thresholds or point estimates to identify unusual disease activity.

Such approaches do not explicitly quantify uncertainty, making it difficult to distinguish between:

- normal seasonal variation
- random fluctuations
- genuine outbreak signals

This project investigates probabilistic outbreak monitoring using Bayesian forecasting. Instead of producing a single prediction, the system generates posterior predictive distributions and uncertainty-aware prediction intervals that can be used for anomaly detection and decision support.

---

## Project Architecture

```text
Influenza Metadata
        │
        ▼
Data Validation
        │
        ▼
Date Cleaning
        │
        ▼
Monthly Count Aggregation
        │
        ▼
Statistical Modelling
 ├── Poisson Anomaly Detection
 ├── Gaussian Anomaly Detection
 └── Bayesian Forecasting
        │
        ▼
Rolling Backtesting
(MAE, RMSE, Coverage)
        │
        ▼
Forecast Visualisation
        │
        ▼
MLflow Tracking
```

---

## Repository Structure

```text
flu-pipeline/
│
├── src/
│   └── flu_pipeline/
│       ├── cli.py
│       ├── ingestion.py
│       ├── validation.py
│       ├── preprocessing.py
│       ├── aggregation.py
│       ├── comparison.py
│       ├── backtesting.py
│       ├── evaluation.py
│       ├── visualisation.py
│       ├── mlflow_tracking.py
│       └── models/
│           ├── poisson.py
│           ├── gaussian.py
│           └── bayesian_gaussian.py
│
├── data/
├── outputs/
├── mlruns/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Statistical Models

### Poisson Anomaly Detection

Monthly sequence counts are modelled as count data using a Poisson distribution.

`X ~ Poisson(λ)`

Potential outbreaks are detected when observed counts exceed the upper prediction bound derived from the Poisson distribution.

### Gaussian Anomaly Detection

Monthly counts are modelled using a Gaussian distribution.

`X ~ Normal(μ, σ²)`

Rolling historical means and standard deviations are used to generate prediction intervals.

### Bayesian Forecasting

Prior belief:

`μ ~ Normal(μ₀, τ₀²)`

Observed data:

`X ~ Normal(μ, σ²)`

Posterior:

`μ | X ~ Normal(μₙ, τₙ²)`

Posterior predictive distribution:

`X_new | X ~ Normal(μₙ, σ² + τₙ²)`

Anomalies are identified when observed counts fall outside the 95% posterior predictive interval.

---

## Why Bayesian?

Classical anomaly detection methods produce fixed thresholds based on historical observations.

Bayesian forecasting extends this idea by:

- explicitly modelling uncertainty
- updating beliefs as new data arrive
- generating posterior predictive distributions
- providing confidence intervals around future observations

This enables uncertainty-aware outbreak detection rather than relying solely on point estimates.

---

## Model Evaluation

Rolling backtesting is used to assess forecasting performance.

### Metrics

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- Coverage (% observations contained within the predictive interval)

### Example Results

#### H1N1

| Metric | Value |
|----------|----------|
| MAE | 17.34 |
| Coverage | 90.40% |

#### H3N2

| Metric | Value |
|----------|----------|
| MAE | 10.60 |
| Coverage | 84.38% |

---

## Running the Pipeline

```bash
PYTHONPATH=src .venv/bin/python -m flu_pipeline.cli \
    -i data/raw/flu_H1N1.txt \
    -o outputs \
    --subtype H1N1
```

---

## Docker

Build image:

```bash
docker build -t flu-bayesian-pipeline .
```

Run container:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/outputs:/app/outputs" \
  -v "$(pwd)/mlruns:/app/mlruns" \
  flu-bayesian-pipeline \
  -i /app/data/raw/flu_H1N1.txt \
  -o /app/outputs \
  --subtype H1N1
```
