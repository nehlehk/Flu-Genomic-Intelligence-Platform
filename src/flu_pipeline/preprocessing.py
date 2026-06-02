import pandas as pd

def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'date' column in the DataFrame by converting it to datetime format.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
    """
    df = df.copy()
    df['collection_date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=["collection_date", "country"])
    df["year_month"] = df["collection_date"].dt.to_period("M").astype(str)
    return df