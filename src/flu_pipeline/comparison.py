import pandas as pd

def compare_outlier_detection_methods(poisson_df: pd.DataFrame, gaussian_df: pd.DataFrame) -> pd.DataFrame:

    key_cols = ["country", "subtype", "year_month", "sequence_count"]
    poisson_subset = poisson_df[key_cols + ["is_outlier"]].rename(columns={"is_outlier": "poisson_outlier"})
    gaussian_subset = gaussian_df[key_cols + ["is_outlier"]].rename(columns={"is_outlier": "gaussian_outlier"})
    comparison_df = pd.merge(poisson_subset, gaussian_subset, on=key_cols, how="inner")
    comparison_df["outlier_agreement"] = comparison_df["poisson_outlier"] == comparison_df["gaussian_outlier"]

    return comparison_df


def generate_comparison_summary(comparison_df: pd.DataFrame) -> pd.DataFrame:

    total = len(comparison_df)

    poisson_count = comparison_df["poisson_outlier"].sum()

    gaussian_count = comparison_df["gaussian_outlier"].sum()

    agreement_pct = (
        (
            comparison_df["poisson_outlier"]
            ==
            comparison_df["gaussian_outlier"]
        ).mean()
        * 100
    )

    summary = pd.DataFrame({
        "metric": [
            "total_observations",
            "poisson_outliers",
            "gaussian_outliers",
            "agreement_percent"
        ],
        "value": [
            total,
            poisson_count,
            gaussian_count,
            round(agreement_pct, 2)
        ]
    })

    return summary