#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

# Test default target dir.
echo "Testing example-test/.target."
rm -rf example-test/.target
python3.6 -m prodmodel build example-test:csv_data
CACHE_FILES=$(ls example-test/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at example-test/.target/output/csv_data."
    exit 1
fi

# Test custom relative target dir.
echo "Testing example-test/.my_target."
rm -rf example-test/.my_target
python3.6 -m prodmodel build example-test:csv_data --target_dir=.my_target
CACHE_FILES=$(ls example-test/.my_target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at example-test/.my_target/output/csv_data."
    exit 1
fi

# Test custom absolute target dir.
echo "Testing /tmp/.target."
rm -rf /tmp/.target
python3.6 -m prodmodel build example-test:csv_data --target_dir=/tmp/.target
CACHE_FILES=$(ls /tmp/.target/output/csv_data | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at /tmp/.target/output/csv_data."
    exit 1
fi
