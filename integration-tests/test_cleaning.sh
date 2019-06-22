#!/bin/bash
set -e

# Make sure csv_data target output exists.
python -m prodmodel example:csv_data
FILES=$(ls example/.target/output/csv_data | wc -l)
if [ "$FILES" -eq 0 ]
  then
    echo "No output files at example/.target/output/csv_data."
    exit 1
fi

# Cutoff date is in the past, files should still be there.
python -m prodmodel clean example:csv_data --cutoff_date=2019-01-01T00:00:00
FILES=$(ls example/.target/output/csv_data | wc -l)
if [ "$FILES" -eq 0 ]
  then
    echo "No output files at example/.target/output/csv_data."
    exit 1
fi

# Default cutoff date is now, files should be deleted.
python -m prodmodel clean example:csv_data
FILES=$(ls example/.target/output/csv_data | wc -l)
if [ "$FILES" -gt 0 ]
  then
    echo "Output files not deleted at example/.target/output/csv_data."
    exit 1
fi
