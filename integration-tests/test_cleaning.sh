#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

# Make sure csv_data target output exists.
python3.6 -m prodmodel example-test:csv_data
CACHE_FILES=$(ls example-test/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at example-test/.target/output/csv_data."
    exit 1
fi

# Cutoff date is in the past, files should still be there.
python3.6 -m prodmodel clean example-test:csv_data --cutoff_date=2019-01-01T00:00:00
CACHE_FILES=$(ls example-test/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at example-test/.target/output/csv_data."
    exit 1
fi

# Default cutoff date is now, files should be deleted.
python3.6 -m prodmodel clean example-test:csv_data
CACHE_FILES=$(ls example-test/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -gt 0 ]
  then
    echo "Output files not deleted at example-test/.target/output/csv_data."
    exit 1
fi
