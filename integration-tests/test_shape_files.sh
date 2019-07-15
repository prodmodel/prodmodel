#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

echo "Testing shape files."
python3.5 -m prodmodel build integration-tests/example:shape_file --output_format='none'
CACHE_FILES=$(ls integration-tests/example/.target/output/shape_file/*/output_1.pickle | wc -l)
if [ "$CACHE_FILES" -eq 0 ]
  then
    echo "No output files at integration-tests/example/.target/output/shape_file."
    exit 1
fi
