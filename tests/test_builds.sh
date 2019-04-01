#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
source $BASEDIR/.env
cd $BASEDIR

python3.6 prodmodel/main.py test_transform
python3.6 prodmodel/main.py evaluate
python3.6 prodmodel/main.py model_in_s3
