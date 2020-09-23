FROM python:3.8

RUN curl -O https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip \
 && unzip terraform_0.12.29_linux_amd64.zip \
 && mv terraform /usr/local/bin/ \
 && rm terraform_0.12.29_linux_amd64.zip

# Make "pip install" step quicker by pre-installing dependencies
RUN pip install protobuf grpcio cryptography u-msgpack-python

COPY . /Pyrraform
RUN pip install /Pyrraform
