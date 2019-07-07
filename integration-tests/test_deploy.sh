#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

# Test default target dir.
echo "Testing deploy target."
python3.6 -m prodmodel build integration-tests/example:deploy_json --output_format='none'
DEPLOYED_FILES=$(ls $HOME/deployed.json | wc -l)
if [ "$DEPLOYED_FILES" -eq 0 ]
  then
    echo "No deployed files at $HOME/deployed.json."
    exit 1
fi
