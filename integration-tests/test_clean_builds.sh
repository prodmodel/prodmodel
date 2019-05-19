#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR
rm -rf example/.target/

integration-tests/test_builds.sh
