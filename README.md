# Most Active Cookie Finder

This command-line tool written in Python helps you find the most active cookie(s) for a specified day in a CSV log file.

## Features
- Finds the most active cookie(s) based on the number of occurrences in the log file.
- Supports parsing log files in CSV format.
- Provides command-line interface for easy usage.

## Requirements
- Python 3.x
- Standard Python libraries (`argparse`, `datetime`, `os`, `logging`)

## Usage
To use the tool, simply run it from the command line with the following arguments:
```
python3 most_active_cookie.py <file_path> -d <date>
```
- `<file_path>`: Path to the CSV log file.
- `<date>`: Date in the format `YYYY-MM-DD` for which to find the most active cookie(s).

To run unit tests:
```
python3 test_suite.py
```
