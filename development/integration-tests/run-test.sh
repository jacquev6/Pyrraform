#!/bin/bash

set -o errexit
set -o verbose


/usr/local/bin/terraform-provider-* || true
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform providers
test ! -f /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform init
test ! -f /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform providers schema -json | python -m json.tool
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform plan
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform apply
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate

terraform destroy -auto-approve
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate

terraform plan
sed "s/^........-......\..\{3,4\}://" /terraform-provider-pyrraform-test.log >&2
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate
