#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

echo "Testing json output format."
python3.6 -m prodmodel build integration-tests/example:csv_data_to_json --output_format='none'
CACHE_FILES=$(ls integration-tests/example/.target/output/csv_data_to_json/*/output_1.json | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No json output files at integration-tests/example/.target/output/csv_data_to_json."
    exit 1
fi
