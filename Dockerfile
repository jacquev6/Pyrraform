FROM ubuntu:18.04 AS terraform_provider_uptimerobot
RUN apt-get update \
 && apt-get install --yes wget unzip golang git

WORKDIR /mygo
RUN wget https://dl.google.com/go/go1.13.8.linux-amd64.tar.gz
RUN tar zxf go1.13.8.linux-amd64.tar.gz
WORKDIR /
ENV PATH=/mygo/go/bin:$PATH

RUN git clone https://github.com/louy/terraform-provider-uptimerobot.git
RUN cd terraform-provider-uptimerobot && go build


FROM python:3

# @todo Support Terraform 0.13. (Release notes say that local providers discovery has changed)
RUN curl -O https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip \
 && unzip terraform_0.12.29_linux_amd64.zip \
 && mv terraform /usr/local/bin/ \
 && rm terraform_0.12.29_linux_amd64.zip

COPY --from=terraform_provider_uptimerobot /terraform-provider-uptimerobot/terraform-provider-uptimerobot /usr/local/bin/

RUN pip install grpcio cryptography

COPY src /pyrraform

RUN pip install --editable /pyrraform
