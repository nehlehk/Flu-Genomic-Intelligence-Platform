import pandas as pd
import numpy as np   

def calculate_posterior(monthly_counts: pd.DataFrame, group_cols: list[str], 
                        count_col: str = "sequence_count", prior_mean: float = 1 ,
                        prior_std: float = 5 , min_hist : int = 3
                         ) -> pd.DataFrame:
    results = []

    for _, group in monthly_counts.groupby(group_cols):
        group = group.sort_values("year_month").copy()
        
        posterior_means = []
        posterior_sds = []
        predictive_means = []
        predictive_sds = []
        lower_bounds = []
        upper_bounds = []

        for i in range(len(group)):
            history = group.iloc[:i][count_col]
            if len(history) < min_hist:
                posterior_means.append(np.nan)
                posterior_sds.append(np.nan)
                predictive_means.append(np.nan)
                predictive_sds.append(np.nan)
                lower_bounds.append(np.nan)
                upper_bounds.append(np.nan)
                continue

            n = len(history)
            sample_mean = history.mean()
            sigma = history.var(ddof=1)

            if sigma == 0 or np.isnan(sigma):
                sigma = 1.0

            # Update posterior parameters
            post_var = 1 / (n / sigma + 1 / prior_std**2)

            posterior_means.append(post_var * (n * sample_mean / sigma + prior_mean / prior_std**2))
            posterior_sds.append(np.sqrt(post_var))

            predictive_mean = posterior_means[-1]
            predictive_sd = np.sqrt(posterior_sds[-1]**2 + sigma)
            predictive_means.append(predictive_mean)
            predictive_sds.append(predictive_sd)     

            lower = predictive_mean - 1.96 * predictive_sd
            upper = predictive_mean + 1.96 * predictive_sd
            lower_bounds.append(lower)
            upper_bounds.append(upper)  
        group["posterior_mean"] = posterior_means
        group["posterior_sd"] = posterior_sds
        group["predictive_mean"] = predictive_means
        group["predictive_sd"] = predictive_sds
        group["lower_bound"] = lower_bounds
        group["upper_bound"] = upper_bounds
        group["bayesian_is_outlier"] = group[count_col] > group["upper_bound"]
        results.append(group) 


    return pd.concat(results, ignore_index=True)
