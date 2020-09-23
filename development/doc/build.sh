#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"


image_id=$(
  docker build \
    --quiet \
    .
)

cd ../..

rm -rf docs

docker run \
  --rm \
  --volume $PWD:/project \
  --workdir /project \
  $image_id

cp -r build/sphinx/html docs
