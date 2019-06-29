#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

echo "Copying project and deleting target dir."
rm -rf /tmp/example_1
cp -r integration-tests/example-external /tmp/example_1
rm -rf /tmp/example_1/.target

OUTPUT=$(python3.6 -m prodmodel /tmp/example_1:csv_data_scores --output_format=str)
if [ "$OUTPUT" != "[{'education': 'primary', 'score': 150}, {'education': 'secondary', 'score': 250}]" ]
  then
    echo "Output mismatch."
    exit 1
fi

echo "Updating external database."
python3.6 /tmp/example_1/update.py

# Output is still the same because the previous result is cached.
OUTPUT=$(python3.6 -m prodmodel /tmp/example_1:csv_data_scores --output_format=str)
if [ "$OUTPUT" != "[{'education': 'primary', 'score': 150}, {'education': 'secondary', 'score': 250}]" ]
  then
    echo "Output mismatch."
    exit 1
fi

# Output is different because of the --force_external flag.
OUTPUT=$(python3.6 -m prodmodel /tmp/example_1:csv_data_scores --force_external --output_format=str)
if [ "$OUTPUT" != "[{'education': 'primary', 'score': 150}, {'education': 'secondary', 'score': 300}]" ]
  then
    echo "Output mismatch."
    exit 1
fi

echo "Test succeeded."
