# MP1 Data Pipeline

This project is a configurable command-line pipeline that reads a CSV file, validates and cleans it based on a YAML configuration file, and saves the cleaned result as a new CSV. `pipeline.py` is the entry point. It parses the `--input`, `--config`, `--output`, and `--verbose` arguments, sets up logging, and runs each stage in order, exiting with status code 1 if any stage fails. Data moves through five stages: the input and config paths are checked, both files are loaded, the data is validated, it is cleaned, and the result is saved and a cleaning report is printed. The reusable code lives in the `src/` package: `utils.py` configures logging and checks that input paths are real files, and `data_loaders.py` chooses a CSV, JSON, or YAML loader based on the file extension. `data_validator.py` checks that every required column exists, removes rows whose numeric columns contain values that cannot be converted to numbers, and converts those columns to a numeric type. `data_processor.py` removes duplicate rows, drops rows or columns with missing values, removes outliers using the IQR or z-score method, and builds the before-and-after cleaning report, and `data_output.py` writes the final DataFrame to CSV without the index. All dataset-specific settings, such as the required and numeric column names and which cleaning steps are enabled, are stored in `config/config.yaml`, so the pipeline can clean a different dataset without changing any Python code.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
18:34:43 DEBUG    __main__ — Arguments received: Namespace(input='fixtures/sample_data.csv', config='config/config.yaml', output='output/clean.csv', verbose=True)
18:34:43 INFO     src.utils — Input file found: sample_data.csv
18:34:43 INFO     src.utils — Input file found: config.yaml
18:34:43 INFO     __main__ — Starting pipeline
18:34:43 DEBUG    src.data_loaders — Loading CSV file: fixtures/sample_data.csv
18:34:43 DEBUG    src.data_loaders — Loading YAML file: config/config.yaml
18:34:43 INFO     __main__ — Loaded data from fixtures/sample_data.csv and config from config/config.yaml
18:34:43 WARNING  src.data_validator — Column 'rating', row 94: 'not_available' is not a valid number, removing row
18:34:43 WARNING  src.data_validator — Column 'rating', row 95: 'error' is not a valid number, removing row
18:34:43 DEBUG    src.data_validator — Validation kept 98 valid row(s) and removed 2 row(s)
18:34:43 INFO     __main__ — Validation complete: 100 -> 98 rows
18:34:43 DEBUG    src.data_processor — remove_duplicates: removed 2 duplicate row(s)
18:34:43 DEBUG    src.data_processor — handle_missing: removed 2 row(s) with missing values
18:34:43 DEBUG    src.data_processor — remove_outliers: column 'rating', method=iqr, threshold=1.5, removed 2 row(s)
18:34:43 INFO     __main__ — Processing complete: 98 -> 92 rows, removed 6 row(s) and 0 column(s)
18:34:43 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
18:34:43 INFO     __main__ — Saved 92 rows and 5 columns to output/clean.csv
Cleaning report:
  rows_before: 98
  rows_after: 92
  rows_removed: 6
  columns_before: 5
  columns_after: 5
  columns_removed: 0
```

Starting from 100 rows, validation removes 2 rows with non-numeric ratings (`not_available`, `error`). Processing then removes 2 duplicate rows, 2 rows with missing values, and 2 rating outliers (`200` and `-50`), which leaves 92 rows in `output/clean.csv`.
