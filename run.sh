#!/bin/bash

set -o errexit

do_pre_build=false
no_cache=""
while [[ "$#" > 0 ]]
do
  case $1 in
    --verbose)
      do_pre_build=true
      ;;
    --no-cache)
      no_cache="--no-cache --pull"
      ;;
    *)
      echo "Unknown parameter passed: $1"
      exit 1;;
  esac
  shift
done

if $do_pre_build
then
  docker build $no_cache .
fi

image=$(docker build $no_cache -q .)

echo "Run terraform-provider-pyrraform-test in this shell"
echo "Code changes made to the library are reloaded between runs"

docker run \
  --interactive --tty \
  --rm \
  --volume $PWD/src/Pyrraform:/pyrraform/Pyrraform \
  --volume $PWD/test-resources:/resources \
  --workdir /resources \
  $image \
  bash
