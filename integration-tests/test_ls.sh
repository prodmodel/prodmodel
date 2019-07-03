#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

OUTPUT=$(python3.6 -m prodmodel ls example-s3 --output_format=str)
echo "$OUTPUT"
if [ "$OUTPUT" != "['csv_data', 'data_in_s3']" ]
  then
    echo "Output mismatch."
    exit 1
fi

echo "Test succeeded."
