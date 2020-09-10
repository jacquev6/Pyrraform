#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"


root="."
no_cache=""
while [[ "$#" > 0 ]]
do
  case $1 in
    --no-cache)
      no_cache="--no-cache --pull"
      ;;
    --root)
      root=./$2
      shift
      ;;
    *)
      echo "Unknown parameter passed: $1"
      exit 1;;
  esac
  shift
done


docker_image=$(docker build --quiet $no_cache --file Dockerfile ../..)


for main_config_file_path in $(find $root -name main.tf)
do
  config_directory_path=$PWD/${main_config_file_path%/main.tf}
  echo $config_directory_path
  provider_name=$(echo $main_config_file_path | cut -d / -f 2)
  provider_path=$PWD/$provider_name/terraform-provider-$provider_name

  rm -rf /tmp/pyrraform-test-resources
  cp -r $config_directory_path /tmp/pyrraform-test-resources

  docker run \
    --rm \
    --volume $provider_path:/usr/local/bin/terraform-provider-$provider_name:ro \
    --volume $PWD/run-test.sh:/run-test.sh:ro \
    --volume /tmp/pyrraform-test-resources:/resources \
    --workdir /resources \
    $docker_image \
    /run-test.sh \
  >$config_directory_path/output.txt 2>&1 || true

  echo
done
