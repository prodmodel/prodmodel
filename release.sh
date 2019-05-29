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
if [ -z "$GITHUB_API_USERNAME" ]
  then
    echo "No GITHUB_API_USERNAME specified."
    exit 1
fi
if [ -z "$GITHUB_API_TOKEN" ]
  then
    echo "No GITHUB_API_TOKEN specified."
    exit 1
fi

export PRODMODEL_RELEASE_VERSION=$1
export GITHUB_POST_DATA="'{\"tag_name\": \"v${PRODMODEL_RELEASE_VERSION}\", \"target_commitish\": \"master\", \"name\": \"v${PRODMODEL_RELEASE_VERSION}\", \"draft\": false, \"prerelease\": false}'"

curl -u $GITHUB_API_USERNAME:$GITHUB_API_TOKEN -X POST https://api.github.com/repos/prodmodel/prodmodel/releases -d $GITHUB_POST_DATA

python3.6 prodmodel/setup.py sdist bdist_wheel
twine upload dist/prodmodel-"$PRODMODEL_RELEASE_VERSION"*
