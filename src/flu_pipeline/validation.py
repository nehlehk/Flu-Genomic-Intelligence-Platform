import pandas as pd

REQUIRED_COLUMNS = ["date", "country", "subtype"]

def validate_columns(df: pd.DataFrame) -> None:
    """
    Validates that the required columns are present in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
    
    Raises:
        ValueError: If any of the required columns are missing.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")