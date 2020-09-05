#!/bin/bash

set -o errexit


rm -f /terraform-provider-pyrraform-test.log
trap "echo; cat /terraform-provider-pyrraform-test.log" EXIT

TF_LOG=TRACE terraform plan
