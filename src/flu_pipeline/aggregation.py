import pandas as pd

def aggregate_monthly_count(df: pd.DataFrame) -> pd.DataFrame:  
    monthly_count = (df.groupby(["year_month", "country", "subtype"])
    .size()
    .reset_index(name="sequence_count")
    .sort_values(["country", "subtype", "year_month"]))
    return monthly_count
