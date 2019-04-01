#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR
rm -rf target/

tests/test_builds.sh
