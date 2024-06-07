#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
CODE_DIR=$SCRIPT_DIR/../src/

set -e

export PYTHONPATH=$CODE_DIR

rm -rf versions/${VERSION}
sphinx-build -b html -d html/doctrees source html/html