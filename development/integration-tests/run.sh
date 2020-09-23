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
  for d in providers/*
  do
    providers+=( ${d#providers/} )
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
  for success in providers/$provider/successes/*
  do
    success=${success#providers/$provider/successes/}
    echo $success

    rm -rf /tmp/pyrraform-test-resources-$provider-$success
    cp -r providers/$provider/successes/$success /tmp/pyrraform-test-resources-$provider-$success
    if ! docker run \
      --rm \
      --volume $PWD/providers/$provider/terraform-provider-$provider:/usr/local/bin/terraform-provider-$provider:ro \
      --volume $PWD/run-test.sh:/run-test.sh:ro \
      --volume /tmp/pyrraform-test-resources-$provider-$success:/resources \
      --workdir /resources \
      $docker_image \
      bash /run-test.sh \
    >providers/$provider/successes/$success/output.txt 2>&1
    then
      echo "Error on an expected success"
      false
    fi
  done
  echo "Errors:"
  for error in providers/$provider/errors/*
  do
    error=${error#providers/$provider/errors/}
    echo $error

    rm -rf /tmp/pyrraform-test-resources-$provider-$error
    cp -r providers/$provider/errors/$error /tmp/pyrraform-test-resources-$provider-$error
    if docker run \
      --rm \
      --volume $PWD/providers/$provider/terraform-provider-$provider:/usr/local/bin/terraform-provider-$provider:ro \
      --volume $PWD/run-test.sh:/run-test.sh:ro \
      --volume /tmp/pyrraform-test-resources-$provider-$error:/resources \
      --workdir /resources \
      $docker_image \
      bash /run-test.sh \
    >providers/$provider/errors/$error/output.txt 2>&1
    then
      echo "Success on an expected error"
      false
    fi
  done
  echo
done
shopt -u nullglob
