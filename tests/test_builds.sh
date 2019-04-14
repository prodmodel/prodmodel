#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
source $BASEDIR/.env
cd $BASEDIR

python3.6 prodmodel/main.py example:test_transform
python3.6 prodmodel/main.py example:evaluate
python3.6 prodmodel/main.py example:model_in_s3
