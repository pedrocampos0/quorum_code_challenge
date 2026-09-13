import argparse
import csv
from pathlib import Path

from analysis import LegislativeAnalyzer
from csv_io import CsvReportWriter, CsvRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate legislative voting CSV reports.")
    parser.add_argument("--input-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    input_bill = (args.input_dir / "bills.csv").resolve()
    output_bill = (args.output_dir / "bills.csv").resolve()
    if input_bill == output_bill:
        parser.error("output bills.csv would overwrite the input; use another directory")

    try:
        data = CsvRepository(args.input_dir).load()
        reports = LegislativeAnalyzer(data).analyze()
        paths = CsvReportWriter(args.output_dir).write(reports)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")

    for path in paths:
        print(f"Created {path}")


if __name__ == "__main__":
    main()
