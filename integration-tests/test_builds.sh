#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
source $BASEDIR/.env
cd $BASEDIR

python3.6 -m prodmodel example:test_transform
python3.6 -m prodmodel example:evaluate
python3.6 -m prodmodel example:model_in_s3
