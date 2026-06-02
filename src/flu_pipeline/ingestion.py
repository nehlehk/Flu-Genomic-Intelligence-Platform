import pandas as pd

def read_input_file(file_path: str) -> pd.DataFrame:
    """
    Reads the input file and returns a DataFrame.

    Args:
        file_path (str): The path to the input file.
    """
    if file_path.endswith('.csv') or file_path.endswith('.txt'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.tsv'):
        return pd.read_csv(file_path, sep='\t')
    
    raise ValueError(f"Unsupported file format: {file_path}", "Supported formats are: .csv, .txt, .tsv")