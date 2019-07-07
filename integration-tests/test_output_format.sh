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

OUTPUT=$(python3.6 -m prodmodel build integration-tests/example:average_age --output_format='str')
if [ "$OUTPUT" != "4.567573545675735" ]
  then
    echo "Output mismatch: $OUTPUT."
    exit 1
fi
CACHE_FILES=$(ls integration-tests/example/.target/output/average_age/*/output_1.pickle | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at integration-tests/example/.target/output/average_age."
    exit 1
fi
