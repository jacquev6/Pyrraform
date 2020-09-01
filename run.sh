#!/bin/bash

set -o errexit

image=$(docker build -q .)

echo "Run terraform-provider-pyrraform-test in this shell"
echo "Code changes made to the library are reloaded between runs"

docker run \
  --interactive --tty \
  --rm \
  --volume $PWD/src/Pyrraform:/pyrraform/Pyrraform \
  $image \
  bash
