#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

python3.5 -m prodmodel example:*
