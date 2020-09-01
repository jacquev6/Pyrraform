FROM python:3

COPY src /pyrraform

RUN pip install --editable /pyrraform
