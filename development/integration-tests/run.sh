#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"


providers=()
no_cache=""
while [[ "$#" -gt 0 ]]
do
  case $1 in
    --no-cache)
      no_cache="--no-cache --pull"
      ;;
    --provider)
      providers+=( $2 )
      shift
      ;;
    *)
      echo "Unknown parameter passed: $1"
      exit 1;;
  esac
  shift
done

if [ ${#providers[@]} -eq 0 ]
then
  for d in $(find * -type d -depth 0)
  do
    providers+=( $d )
  done
fi

docker_image=$(
  docker build \
  --quiet \
  $no_cache \
  --file Dockerfile \
  ../..
)

shopt -s nullglob
for provider in ${providers[@]}; do
  echo $provider
  echo $provider | sed s/./=/g
  echo "Successes:"
  for success in $provider/successes/*
  do
    success=${success#$provider/successes/}
    echo $success

    rm -rf /tmp/pyrraform-test-resources
    cp -r $provider/successes/$success /tmp/pyrraform-test-resources
    if ! docker run \
      --rm \
      --volume $PWD/$provider/terraform-provider-$provider:/usr/local/bin/terraform-provider-$provider:ro \
      --volume $PWD/run-test.sh:/run-test.sh:ro \
      --volume /tmp/pyrraform-test-resources:/resources \
      --workdir /resources \
      $docker_image \
      bash /run-test.sh \
    >$provider/successes/$success/output.txt 2>&1
    then
      echo "Error on an expected success"
      false
    fi
  done
  echo "Errors:"
  for error in $provider/errors/*
  do
    error=${error#$provider/errors/}
    echo $error

    rm -rf /tmp/pyrraform-test-resources
    cp -r $provider/errors/$error /tmp/pyrraform-test-resources
    if docker run \
      --rm \
      --volume $PWD/$provider/terraform-provider-$provider:/usr/local/bin/terraform-provider-$provider:ro \
      --volume $PWD/run-test.sh:/run-test.sh:ro \
      --volume /tmp/pyrraform-test-resources:/resources \
      --workdir /resources \
      $docker_image \
      bash /run-test.sh \
    >$provider/errors/$error/output.txt 2>&1
    then
      echo "Success on an expected error"
      false
    fi
  done
  echo
done
shopt -u nullglob
