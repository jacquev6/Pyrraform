FROM python:3

# @todo Support Terraform 0.13. (Release notes say that local providers discovery has changed)
RUN curl -O https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip \
 && unzip terraform_0.12.29_linux_amd64.zip \
 && mv terraform /usr/local/bin \
 && rm terraform_0.12.29_linux_amd64.zip

COPY src /pyrraform

RUN pip install --editable /pyrraform
