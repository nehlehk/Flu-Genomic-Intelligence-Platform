import argparse
import os

from flu_pipeline.ingestion import read_input_file
from flu_pipeline.validation import validate_columns
from flu_pipeline.preprocessing import clean_dates
from flu_pipeline.aggregation import aggregate_monthly_count    
from flu_pipeline.models.poisson import detect_poisson_outliers
from flu_pipeline.models.gaussian import detect_gaussian_outliers
from flu_pipeline.comparison import compare_outlier_detection_methods   
from flu_pipeline.comparison import generate_comparison_summary

def main():
    parser = argparse.ArgumentParser(description="Flu surveillance pipeline")
    parser.add_argument("-i" ,"--input", required=True, help="Path to the input file (CSV, TXT, TSV)")
    parser.add_argument("-o" ,"--output", required=True, help="Path to the output file (CSV)")
    parser.add_argument("-s" ,"--subtype", required=True, help="Subtype to filter the data")
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
    df = clean_dates(df)

    cleaned_path = os.path.join(
    args.output,
    args.subtype + "_cleaned_data.csv"
)
    df.to_csv(cleaned_path, index=False)
    print(f"Cleaned data saved to {cleaned_path}")


    # Aggregate data
    print("Aggregating monthly counts...")
    monthly_count = aggregate_monthly_count(df)

    # Save output
    monthly_path = os.path.join(
    args.output,
    args.subtype + "_monthly_counts.csv"
)
    monthly_count.to_csv(monthly_path, index=False)
    print(f"Monthly count saved to {monthly_path}")

    # Detect outliers
    print("Detecting outliers using Poisson model...")
    outliers = detect_poisson_outliers(monthly_count, group_cols=["country", "subtype"], count_col="sequence_count", alpha=0.05)

    poisson_path = os.path.join(args.output, args.subtype + "_poisson_anomaly_report.csv")
    outliers.to_csv(poisson_path, index=False)

    # Detect outliers using Gaussian model
    print("Detecting outliers using Gaussian model...")
    gaussian_outliers = detect_gaussian_outliers(monthly_count, group_cols=["country", "subtype"], count_col="sequence_count", alpha=0.05)

    gaussian_path = os.path.join(args.output, args.subtype + "_gaussian_anomaly_report.csv")
    gaussian_outliers.to_csv(gaussian_path, index=False)

    # Compare methods
    print("Comparing outlier detection methods...")
    comparison_df = compare_outlier_detection_methods(outliers, gaussian_outliers)

    comparison_path = os.path.join(args.output, args.subtype + "_comparison_report.csv")
    comparison_df.to_csv(comparison_path, index=False)

    # Generate summary    
    print("Generating comparison summary...")
    summary_df = generate_comparison_summary(comparison_df) 
    summary_path = os.path.join(args.output, args.subtype + "_comparison_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Comparison summary saved to {summary_path}")

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()