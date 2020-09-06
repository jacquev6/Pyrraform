#!/bin/bash

set -o errexit


rm -f /terraform-provider-pyrraform-test.log

function diagnose {
  echo
  cat /terraform-provider-pyrraform-test.log
  for f in *.cert.pem
  do
    echo
    echo "$f:"
    openssl x509 -in $f -text -noout
  done
  echo
  diff -y <(openssl x509 -in provider-uptimerobot.cert.pem -text -noout) <(openssl x509 -in provider-pyrraform-test.cert.pem -text -noout)
}

trap diagnose EXIT

TF_LOG=TRACE terraform plan
