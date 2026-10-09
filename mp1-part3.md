# MP1 Part 3: Build a Data Processor Module

Continue working in the same `mp1-data-pipeline` repository from Parts 1–2.

In Part 3, you will build a reusable data processor that can clean different datasets without changing the processing code.

The processor should work with any compatible CSV file. Instead of hard-coding things like column names and different choices, you will use `config.yaml` to tell the processor how to process and clean.

## Project Structure

At the end of Part 3, your repository should contain:

```text
mp1-data-pipeline/
├── .gitignore
├── pipeline.py         (updated)
├── data_loaders.py
├── data_processor.py   (new)
├── config.yaml         (new)
├── requirements.txt
└── fixtures/
    ├── sample.csv
    ├── sample.json
    └── sample.yaml
```

* `pipeline.py` — update your existing pipeline to use the data processor.
* `data_processor.py` — new module containing reusable data-cleaning functions.
* `config.yaml` — new configuration file controlling how the data is processed.
    * Commit this file to Git (do not add it to `.gitignore`). We do not store passwords, API keys, or other secrets in this file.

## Getting Started

Navigate to your existing repository and activate the virtual environment:

```bash
cd mp1-data-pipeline

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate 
#OR
venv\Scripts\activate.ps1

```

Make sure your Parts 1–2 work is committed:

```bash
git status
```

Create a feature branch for Part 3:

```bash
git switch -c feature/data-processor
git push -u origin feature/data-processor
```

## Starter Code

### 1. Create `config.yaml`

```yaml
processing:
  remove_duplicates: true

  missing:
    enabled: true
    axis: "rows"

  outliers:
    enabled: true
    columns:
      - Score
    method: "iqr"
    threshold: 1.5
```

* Use the configuration file to control how the data is processed.
* In a later section, you will update `pipeline.py` to read `config.yaml`.


### 2. Create `data_processor.py`

Create `data_processor.py` and complete the starter code below. 

```python
# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    pass


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    pass


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    pass


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    pass


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    pass
```

## Required Functions

### 1. `remove_duplicates(df)`

Requirements:

* Remove duplicate rows from any DataFrame.
* Log the number of rows removed at the `DEBUG` level.
* Return the resulting DataFrame.

### 2. `handle_missing(df, axis="rows")`

Support the following values for `axis`:

| Axis | Required behavior |
| ---- | ----------------- |
| `rows` | Remove rows that contain one or more missing values. |
| `columns` | Remove columns that contain one or more missing values. |

Requirements:
* Log an `ERROR` and raise `ValueError` for an unsupported axis.
* Remove rows or columns based on the `axis` value.
* Log the number of rows or columns removed at the `DEBUG` level.
* Return the resulting DataFrame.


### 3. `remove_outliers(df, columns, method, threshold)`

Requirements:
* For any other method, log an `ERROR` and raise `ValueError`.
    * should support only `'iqr'` and `'zscore'` as `method`.
* Use the provided `threshold` to identify outliers.
* Log a `WARNING` and continue if a configured column does not exist.
* Log a `WARNING` and continue if a configured column is not numeric.
* For each valid numeric column from the `columns` list, remove the rows identified as outliers.
* Log the method, threshold, and the number of rows removed at the `DEBUG` level.
* Return the resulting DataFrame.


### 4. `process_data(df, config)`

Requirements:
* Use the values under `processing` in `config.yaml` to determine which functions to call. Only call a processing function if its corresponding step is enabled.
* Apply enabled steps in this order:
    1. Remove duplicates.
    2. Handle missing values.
    3. Remove outliers.
* Return the resulting DataFrame.

**Note:**
- Read the required settings from the configuration and pass them to the appropriate functions. Do not hard-code these values.
- Do not catch exceptions inside `process_data()`. Let them propagate to the `try`/`except` block in `main()` in `pipeline.py`.


### 5. `create_cleaning_report(df_before, df_after)`

Return a dictionary containing:

* `rows_before`
* `rows_after`
* `rows_removed`
* `columns_before`
* `columns_after`
* `columns_removed`

Example:

```text
{
    'rows_before': 1000,
    'rows_after': 942,
    'rows_removed': 58,
    'columns_before': 12,
    'columns_after': 10,
    'columns_removed': 2
}
```


## Update `pipeline.py`

Keep the existing pipeline workflow from Parts 1–2.

### 1. Update the imports:

```python
from data_processor import process_data, create_cleaning_report
```

### 2. Update the Logging Format

Update the logging configuration in `setup_logging()` so that each message shows which module produced it. 

In `setup_logging()`, replace the existing logging format with:

```python
format="%(asctime)s %(levelname)-8s %(name)s — %(message)s"
```

### 3. Update `parse_arguments()`

1. Add the required `--config` argument after the existing `--input` argument. It should accept the path to a YAML configuration file.

2. Remove the existing `--format` argument from `parse_arguments()`.


### 4. Validate and Load the Configuration

1. Validate `args.config` using `validate_input()`. Exit with status code `1` if validation fails.

2. Keep the loading `try`/`except` block from Part 2. Inside the same `try` block, use `load_data()` to load the configuration.
   - The `try` block should load both the input data and configuration and catch `ValueError`.

### 5. Process the Data

After loading the input data and configuration:

1. Save a copy of the original DataFrame.

2. Call `process_data()` inside a separate `try`/`except` block. Catch `ValueError` and exit with status code `1`.

### 6. Create the Output

After processing succeeds:

1. Create and print a cleaning report.
3. Log the processing results.
2. Save the cleaned DataFrame as CSV to the `--output` path without the index.
3. Log the saving results.


## Run the Pipeline

Make sure your virtual environment is active, then run the completed pipeline with `fixtures/sample.csv`:

```bash
python pipeline.py --input fixtures/sample.csv --output cleaned_data.csv --config config.yaml
```

## Example Output

The row counts below apply to the original `sample.csv` file and will change if you modify the data or use different examples. Your log messages should show the module that produced each message.

### Successful Run

```text
10:15:02 INFO     __main__ — Input file validated: fixtures/sample.csv
10:15:02 INFO     __main__ — Input file validated: config.yaml
10:15:02 INFO     data_loaders — Loaded CSV file: fixtures/sample.csv (5 rows)
10:15:02 INFO     data_loaders — Loaded YAML file: config.yaml
10:15:02 INFO     __main__ — Processing complete: 5 → 5 rows
10:15:02 INFO     __main__ — Saved cleaned data to cleaned_data.csv
```

The program should also print a cleaning report:

```text
{
    'rows_before': 5,
    'rows_after': 5,
    'rows_removed': 0,
    'columns_before': 2,
    'columns_after': 2,
    'columns_removed': 0
}
```

### With Verbose Mode

Run the pipeline with `--verbose` to display detailed messages from `data_processor.py`:

```bash
python pipeline.py --input fixtures/sample.csv --output cleaned_data.csv --config config.yaml --verbose
```

The output should also include messages similar to:

```text
10:15:02 DEBUG    data_processor — remove_duplicates: 5 → 5 rows
10:15:02 DEBUG    data_processor — handle_missing: 5 → 5 rows
10:15:02 DEBUG    data_processor — Score: lower=4.0, upper=20.0, removed=0
```

### Try different data
Try adding some missing values, duplicate rows, and/or outliers so you can test the data-processing functions.

### Missing Configured Column

If an outlier column listed in `config.yaml` does not exist, log a warning and continue:

```text
10:16:11 WARNING  data_processor — Column not found: MissingScore
10:16:11 INFO     __main__ — Processing complete
```

### Unsupported Outlier Method

If the configuration contains an unsupported method, log an error and exit with status code `1`:

```text
10:17:20 ERROR    data_processor — Unsupported outlier method: percentile
```

### Missing Input or Configuration File

Validation should stop the program before the loaders are called:

```text
10:18:30 ERROR    __main__ — Input file not found: fixtures/missing.csv
```


## After completing Part 3

Commit and push your work:

```bash
git add data_processor.py config.yaml pipeline.py
# OR git add . 
git commit -m "Add reusable data processing functions"
git push -u origin feature/data-processor
```

When finished, merge the feature branch into `main` and push the updated `main` branch.

```bash
git switch main
git merge feature/data-processor
git push origin main

git branch -d feature/data-processor
git push origin --delete feature/data-processor
```

Your repository should contain:

```text
mp1-data-pipeline/
├── .gitignore
├── pipeline.py         
├── data_loaders.py
├── data_processor.py   
├── config.yaml         
├── requirements.txt
└── fixtures/
    ├── sample.csv
    ├── sample.json
    └── sample.yaml
```

To use another compatible CSV file, update the command-line file paths and the relevant column names in the configuration, not `data_processor.py`.

Make sure that:

* all required functions are implemented
* the pipeline successfully loads and processes data
* all changes are committed to Git
* the feature branch is merged into `main`
* the completed work is pushed to GitHub
