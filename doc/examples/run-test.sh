#!/bin/bash

set -o errexit
set -o verbose

terraform providers

terraform init
test ! -f /terraform-provider-pyrraform-test.log

terraform providers schema -json | python -m json.tool
sed "s/^........-......\....://" /terraform-provider-pyrraform-test.log
rm /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform plan
sed "s/^........-......\....://" /terraform-provider-pyrraform-test.log
rm /terraform-provider-pyrraform-test.log
test ! -f terraform.tfstate

terraform apply
sed "s/^........-......\....://" /terraform-provider-pyrraform-test.log
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate

terraform destroy -auto-approve
sed "s/^........-......\....://" /terraform-provider-pyrraform-test.log
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate

terraform plan
sed "s/^........-......\....://" /terraform-provider-pyrraform-test.log
rm /terraform-provider-pyrraform-test.log
grep -v "lineage" terraform.tfstate
