import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_bayesian_forecast(bayesian_results: pd.DataFrame, output_dir: str, subtype: str, country: str, count_col: str = "sequence_count",) -> str:
    
    os.makedirs(output_dir, exist_ok=True)

    df = bayesian_results[(bayesian_results["country"] == country)  & (bayesian_results["subtype"] == subtype)].copy()

    df = df.sort_values("year_month") 
    df["year_month"] = df["year_month"].astype(str)

    plt.figure(figsize=(12, 6))

    plt.plot(df["year_month"], df[count_col], marker="o",label="Observed count", color="blue")

    plt.plot( df["year_month"],df["predictive_mean"], linestyle="--",label="Predictive mean",color="red")

    plt.fill_between(df["year_month"], df["lower_bound"],df["upper_bound"],alpha=0.2,label="95% predictive interval",color="red")

    outliers = df[df["bayesian_is_outlier"] == True]

    plt.scatter(outliers["year_month"], outliers[count_col],marker="x",s=100,label="Bayesian outlier",)

    plt.xticks(rotation=45)
    plt.xlabel("Month")
    plt.ylabel("Sequence count")
    plt.title(f"Bayesian Forecast - {country} {subtype}")
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join( output_dir,f"{subtype}_{country}_bayesian_forecast.png")

    plt.savefig(output_path, dpi=300)
    plt.close()
    
    return output_path