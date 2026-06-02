import argparse
import os

from .ingestion import read_input_file
from .validation import validate_columns
from .preprocessing import preprocess_data
from .aggregation import aggregate_monthly_count    


def main():
    parser = argparse.ArgumentParser(description="Flu surveillance pipeline")
    parser.add_argument("-i" ,"--input", required=True, help="Path to the input file (CSV, TXT, TSV)")
    parser.add_argument("-o" ,"--output", required=True, help="Path to the output file (CSV)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Ingest data
    print("Reading input file...")
    df = read_input_file(args.input)

    # Validate data
    print("Validating required columns...")
    validate_columns(df)

    # Preprocess data
    print("Cleaning dates...")
    df = preprocess_data(df)

    # Aggregate data
    print("Aggregating monthly counts...")
    monthly_count = aggregate_monthly_count(df)

    # Save output
    monthly_count.to_csv(args.output, index=False)
    print(f"Monthly count saved to {args.output}")

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()