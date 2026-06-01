# Bayesian Influenza Surveillance Pipeline

End-to-end cloud-native ML project for disease surveillance.

## Objectives

- Data ingestion
- Data validation
- Time-series aggregation
- Poisson anomaly detection
- Gaussian anomaly detection
- Bayesian forecasting
- MLflow tracking
- Cloud deployment

## Run

```bash
python -m flu_pipeline.cli \
    -i data/raw/flu_H1N1.txt \
    -o outputs