#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR

python3.6 -m prodmodel example:*
