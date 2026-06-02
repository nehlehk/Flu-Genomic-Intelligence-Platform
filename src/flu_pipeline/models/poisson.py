import pandas as pd
from scipy.stats import poisson

def detect_poisson_outliers(monthly_counts: pd.DataFrame, group_cols: list[str],count_col: str = "sequence_count", alpha: float = 0.05) -> pd.DataFrame:
    result = []
    for _, group in monthly_counts.groupby(group_cols):

        group = group.sort_values("year_month").copy()
        
        group["expected_count"] = (
            group[count_col]
            .expanding()
            .mean()
            .shift(1)
        )
        # Calculate the Poisson confidence interval
        lower_bound = poisson.ppf(alpha / 2, group["expected_count"])
        upper_bound = poisson.ppf(1 - alpha / 2, group["expected_count"])
               
        group["lower_bound"] = lower_bound
        group["upper_bound"] = upper_bound
        group["is_outlier"] =  (group[count_col] > group["upper_bound"])
        result.append(group)
    return pd.concat(result, ignore_index=True)