#!/bin/bash
set -e

BASEDIR=$(dirname "$0")/..
cd $BASEDIR
rm -rf example/.target/data
rm -rf example/.target/output

integration-tests/test_builds.sh
