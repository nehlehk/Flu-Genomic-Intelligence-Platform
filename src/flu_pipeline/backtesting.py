import numpy as np
import pandas as pd

def backtest_model( bayesian_results: pd.DataFrame,count_col: str = "sequence_count",
    prediction_col: str = "predictive_mean",
    lower_col: str = "lower_bound",
    upper_col: str = "upper_bound") -> pd.DataFrame:
    

    valid = bayesian_results.dropna(subset=[prediction_col, lower_col, upper_col]).copy()

    valid["absolute_error"] = np.abs(valid[count_col] - valid[prediction_col])
    valid["squared_error"] = (valid[count_col] - valid[prediction_col]) ** 2
    valid["within_interval"] = (valid[count_col] >= valid[lower_col]) & (valid[count_col] <= valid[upper_col])

    mae = valid["absolute_error"].mean()
    rmse = np.sqrt(valid["squared_error"].mean())
    coverage = valid["within_interval"].mean() * 100 

    summary = pd.DataFrame({
        "MAE": [mae],
        "MSE": [rmse],
        "Coverage": [coverage]
    })

    return summary