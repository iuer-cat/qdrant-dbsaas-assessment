#!/bin/bash

BASH_SCRIPT_DIR=$( cd  $(dirname "$BASH_SOURCE") && pwd)

function start_service {
  echo "Starting Service: $SERVICE"
  cd ${BASH_SCRIPT_DIR}/${SERVICE}/src/${SERVICE}/
  exec python ${BASH_SCRIPT_DIR}/${SERVICE}/src/${SERVICE}/service_startup.py
}

SERVICE=$1

start_service $SERVICE


