# MP1 Part 4: Assemble the Complete Pipeline

Continue working in the same `mp1-data-pipeline` repository from Parts 1–3.

In Part 4, you will reorganize your existing code, add data validation and output modules, and connect everything into one end-to-end pipeline.

Download the provided `sample_data.csv` and place it in the fixtures/ directory. You will use this file to test the completed pipeline.

## Project Structure

At the end of Part 4, your repository should contain:

```text
mp1-data-pipeline/
├── .gitignore
├── README.md 
├── pipeline.py
├── requirements.txt
├── config/
│   └── config.yaml
├── src/
│   ├── __init__.py
│   ├── data_loaders.py
│   ├── data_processor.py
│   ├── data_validator.py
│   ├── data_output.py
│   └── utils.py
├── fixtures/
│   ├── sample.csv
│   ├── sample.json
│   ├── sample.yaml
│   └── sample_data.csv
└── output/
```

* `pipeline.py` — coordinates the complete pipeline.
* `src/` — contains the Python modules.
* `config/` — contains the pipeline configuration.
    * Do not add it to `.gitignore` -- you will commit `config/config.yaml` to Git; 
* `fixtures/` — contains the simple test data.
* `README.md` — contains a brief description of your completed MP1 pipeline.

## Getting Started

Make sure your Parts 1–3 work is committed. Then create a feature branch for Part 4:

```bash
git status
git switch -c feature/pipeline-assembly
git push -u origin feature/pipeline-assembly
```

## 1. Reorganize the Project

1. Create these directories:

```text
src/
config/
```

2. Create `src/__init__.py`.

3. Move the existing files:

```bash
git mv data_loaders.py src/data_loaders.py
git mv data_processor.py src/data_processor.py
git mv config.yaml config/config.yaml
```

4. Make sure the old top-level files no longer remain. 

5. Commit the reorganization:

```bash
git add .
git commit -m "Reorganize pipeline project"
```

## 2. Create `src/utils.py`

1. Move these existing functions from `pipeline.py` into `src/utils.py`:

* `setup_logging()`
* `validate_input()`

2. Add the code below (imports and module-level logger required by these functions above) to `src/utils.py`.

```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
```


## 3. Create `src/data_validator.py`

1. Create the following starter code:

```python
# src/data_validator.py
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    pass
```

Requirements:

* Check that every name in `required_columns` exists in the DataFrame.
* Log an `ERROR` and raise `ValueError` if a required column is missing.
* For each configured numeric column, 
    * identify non-missing values that cannot be converted to a number.
    * Log a `WARNING` and remove rows containing those invalid numeric values.
    * After removing invalid values, convert each configured numeric column to a numeric data type.
    * Use the following skeleton:
    ```python
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    # TODO: Log a warning and record this row's index.
                    pass
        
        # TODO: Remove the invalid rows.


        #convert to a numeric data type
        df[col] = pd.to_numeric(df[col])
    ```
* Log the number of valid and removed rows at the `DEBUG` level.
* Return the validated DataFrame.


## 4. Create `src/data_output.py`

1. Create the following starter code:

```python
# src/data_output.py
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""
    pass
```

Requirements:

* Use `pathlib` to work with the output path.
* Create the output directory if it does not exist.
    * Hint: Path(filepath).parent.mkdir(parents=True, exist_ok=True) 
* Save the DataFrame as CSV without the index.
* Log the number of rows saved and the output path at the `DEBUG` level.
* Return the output path.

## 5. Update `src/__init__.py`

1. After creating all modules, add the selected functions:

```python
from .data_loaders import load_data
from .data_output import save_data
from .data_processor import process_data, create_cleaning_report
from .data_validator import validate_dataframe
from .utils import setup_logging, validate_input
```


## 6. Add `output/`  to `.gitignore`

## 7. Update `config/config.yaml`

1. Inspect the columns and values in fixtures/sample_data.csv. 

2. Update your configuration:

- Add a `validation` section:
  - `required_columns`: a list of all column names in the sample data.
  - `numeric_columns`: a list of column name(s) whose values should be numeric and meaningful for validation.

- Under the existing `processing` section:
  - Enable duplicate removal.
  - Enable missing-value handling with `axis: "rows"`.
  - Enable outlier removal for numeric column(s), using `method: "iqr"` and `threshold: 1.5`.

This configuration matches the provided `fixtures/sample_data.csv`. Do not modify the validation or processing modules to match the sample data.

## 8. Update `pipeline.py`

1. Update the imports:

```python
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)
```

2. Update the existing pipeline workflow:

- After loading the input data and configuration, read `required_columns` and `numeric_columns` from the `validation` section in the cofig data.
- Before processing, call `validate_dataframe()` inside a separate `try`/`except` block. Catch `ValueError` and exit with status code `1`. 
- Use the returned DataFrame for all subsequent processing steps.
- Log the number of rows before and after validation at the `INFO` level.
- Keep the report creation, printing, and processing logs from Part 3.
- Replace the existing CSV-saving code with a call to `save_data()`. Keep the saving result log in `pipeline.py` at the `INFO` level.
- Move the cleaning report print statement to the end of main().

## 9. Run the Complete Pipeline

Make sure your virtual environment is active, then run:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

### Expected Results

The exact wording may differ, but the output should include information similar to:

```text
10:15:02 INFO     src.utils — Input file validated: fixtures/sample_data.csv
10:15:02 INFO     src.utils — Input file validated: config/config.yaml
10:15:02 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
10:15:02 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
10:15:02 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
10:15:02 DEBUG    src.data_validator — Validation: 100 -> 98 rows
10:15:02 INFO     __main__ — Validation complete: 100 -> 98 rows
10:15:02 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
10:15:02 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
10:15:02 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
10:15:02 INFO     __main__ — Processing complete: 98 -> 92 rows
10:15:02 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
10:15:02 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{
    'rows_before': 98,
    'rows_after': 92,
    'rows_removed': 6,
    'columns_before': 5,
    'columns_after': 5,
    'columns_removed': 0
}
```

## 10. Create `README.md` in the repository root

1. Write a short paragraph of 5-8 sentences describing what your pipeline does, how data moves through it, how your completed pipeline is organized, and the main responsibility of each module. 

2. Include an example command to run the pipeline with the provided sample data and the output produced by your code.


## After Completing Part 4

Commit and push the completed work:

```bash
git status
git add .gitignore pipeline.py src config README.md fixtures/sample_data.csv
git commit -m "Complete MP1 data pipeline"
git push -u origin feature/pipeline-assembly
```

Merge the feature branch into `main` and push it,

```bash
git switch main
git merge feature/pipeline-assembly
git push origin main

git branch -d feature/pipeline-assembly
git push origin --delete feature/pipeline-assembly
```

Verify that:
* the old top-level module files have been moved;
* the complete pipeline runs with the provided sample data;
* `config/config.yaml` and `fixtures/sample_data.csv` are committed;
* generated files under `output/` and `venv/` are not committed;
* the completed work is pushed to GitHub


> Great work! You now have an end-to-end pipeline that loads, validates, cleans, and saves data using configurable settings.
