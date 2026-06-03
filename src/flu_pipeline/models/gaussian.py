import pandas as pd
from scipy.stats import norm    

def detect_gaussian_outliers(monthly_counts: pd.DataFrame, group_cols: list[str], count_col: str = "sequence_count", alpha: float = 0.05) -> pd.DataFrame:
    result = []
    for _, group in monthly_counts.groupby(group_cols):
        group = group.sort_values("year_month").copy()
        
        group["expected_count"] = (
            group[count_col]
            .expanding()
            .mean()
            .shift(1)
        )
        # Calculate the Gaussian confidence interval
        std_dev = group[count_col].expanding().std().shift(1)
        z_score = norm.ppf(1 - alpha / 2)
        group["lower_bound"] = group["expected_count"] - z_score * std_dev
        group["upper_bound"] = group["expected_count"] + z_score * std_dev
        group["is_outlier"] = (group[count_col] > group["upper_bound"])
        result.append(group)
    return pd.concat(result, ignore_index=True)