#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
source $BASEDIR/.env
cd $BASEDIR

python3.6 prodmodel/__main__.py example:test_transform
python3.6 prodmodel/__main__.py example:evaluate
python3.6 prodmodel/__main__.py example:model_in_s3
