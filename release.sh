#!/bin/bash
set -e

if [ -z "$1" ]
  then
    echo "No version specified."
    exit 1
fi
if [ -z "$TWINE_USERNAME" ]
  then
    echo "No TWINE_USERNAME specified."
    exit 1
fi
if [ -z "$TWINE_PASSWORD" ]
  then
    echo "No TWINE_PASSWORD specified."
    exit 1
fi

export PRODMODEL_RELEASE_VERSION=$1
python3.6 prodmodel/setup.py sdist bdist_wheel
twine upload dist/prodmodel-"$PRODMODEL_RELEASE_VERSION"*
