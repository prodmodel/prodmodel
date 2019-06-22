#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
source $BASEDIR/.env
cd $BASEDIR

python3.6 -m prodmodel example-s3:data_in_s3
python3.6 -m prodmodel example-s3:csv_data
