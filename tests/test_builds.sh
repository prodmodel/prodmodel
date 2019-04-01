#!/bin/bash
set -e

cd ..
rm -rf target/
source .env

python3.6 prodmodel/main.py test_transform
python3.6 prodmodel/main.py evaluate
python3.6 prodmodel/main.py model_in_s3
