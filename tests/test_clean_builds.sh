#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR
rm -rf example/.target/

tests/test_builds.sh
