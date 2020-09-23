#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"


image_id=$(
  docker build \
    --quiet \
    .
)

cd ../..

rm -f Pyrraform/*_pb2*.py

docker run \
  --rm \
  --volume $PWD:/project \
  --workdir /project \
  $image_id \
  python -m grpc_tools.protoc \
    -Idevelopment/compile-protobuf \
    --python_out=Pyrraform --grpc_python_out=Pyrraform \
    development/compile-protobuf/*.proto

# Use relative imports
# https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-673566872
sed -i "" "s/\(import .*_pb2.*\)/from . \1/g" Pyrraform/*_pb2_grpc.py
