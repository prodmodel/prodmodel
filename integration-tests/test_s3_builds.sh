#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

echo "Cleaning target directory example-s3/.target/output." 
rm -rf example-s3/.target/output

python3.6 -m prodmodel example-s3:data_in_s3
python3.6 -m prodmodel example-s3:csv_data
