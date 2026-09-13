# Quorum Coding Challenge: Legislative Data
## Run
Requires **Python 3.10+**.
```bash
python3 -m legislative_data
```
To specify other input and output directories:
```bash
python3 -m legislative_data --input-dir /path/to/data --output-dir /path/to/reports
```

## How the code works

1. `CsvRepository` in `legislative_data/csv_io.py` reads UTF-8 CSVs, validates required
   fields, and converts rows into the dataclasses in `models.py`.
2. `LegislativeAnalyzer` in `analysis.py` indexes records by ID, validates their
   relationships, and visits each vote result once. It updates the legislator and
   bill counters together, then resolves sponsor names.
3. `CsvReportWriter` writes the summary dataclasses using Python's CSV quoting.
   `__main__.py` handles command-line arguments and readable error messages.

## Write-up

**1. Discuss your solution’s time complexity. What tradeoffs did you make?** For L legislators, B bills, V votes, and R vote
results, expected time and memory are both **O(L + B + V + R)**. Indexes avoid
repeated scans. Keeping records and validation sets in memory makes the solution
simple and testable.

**2. How would you change your solution to account for future columns that might be
requested, such as “Bill Voted On Date ” or “Co-Sponsors”?** Add a vote date to `Vote` and its CSV conversion, then extend
the relevant summary and analysis, representing co-sponsors as a bill-to-legislator
relationship, resolve their names, and choose a documented CSV representation.

**3. How would you change your solution if instead of receiving CSVs of data, you were given a
list of legislators or bills that you should generate a CSV for?** Construct `LegislativeData` from lists of model objects
and pass it directly to `LegislativeAnalyzer`, the analyzer and writer need no
changes.

**4. Time spent?** I spent 2 hours and 48 minutes to do the code and answer the questions. 
