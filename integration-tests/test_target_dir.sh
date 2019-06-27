#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

# Test default target dir.
echo "Testing integration-tests/example/.target."
rm -rf integration-tests/example/.target
python3.6 -m prodmodel build integration-tests/example:csv_data
CACHE_FILES=$(ls integration-tests/example/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at integration-tests/example/.target/output/csv_data."
    exit 1
fi

# Test custom relative target dir.
echo "Testing integration-tests/example/.my_target."
rm -rf integration-tests/example/.my_target
python3.6 -m prodmodel build integration-tests/example:csv_data --target_dir=.my_target
CACHE_FILES=$(ls integration-tests/example/.my_target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at integration-tests/example/.my_target/output/csv_data."
    exit 1
fi

# Test custom absolute target dir.
echo "Testing /tmp/.target."
rm -rf /tmp/.target
python3.6 -m prodmodel build integration-tests/example:csv_data --target_dir=/tmp/.target
CACHE_FILES=$(ls /tmp/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at /tmp/.target/output/csv_data."
    exit 1
fi
