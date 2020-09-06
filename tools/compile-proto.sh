#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"/..

image=$(docker build --quiet tools/compile-proto)

docker run \
  --volume $PWD:/application \
  --workdir /application \
  $image \
  python -m grpc_tools.protoc \
    -Itools/compile-proto \
    --python_out=src/Pyrraform --grpc_python_out=src/Pyrraform \
    tools/compile-proto/tfplugin5_0.proto

# Use relative imports
# https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-673566872
sed -i "" "s/\(import .*_pb2.*\)/from . \1/g" src/Pyrraform/*_pb2_grpc.py
