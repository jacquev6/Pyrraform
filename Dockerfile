FROM python:3

RUN curl -O https://releases.hashicorp.com/terraform/0.13.1/terraform_0.13.1_linux_amd64.zip \
 && unzip terraform_0.13.1_linux_amd64.zip \
 && mv terraform /usr/local/bin \
 && rm terraform_0.13.1_linux_amd64.zip

COPY src /pyrraform

RUN pip install --editable /pyrraform
