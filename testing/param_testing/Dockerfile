# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:2.0-python3.7-appservice
FROM ubuntu:18.04


RUN apt-get update && apt-get install -y \
    software-properties-common 

#poppler-utils

RUN apt-get install  curl wget -y
RUN apt-get install python3-pip python3-venv libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev -y
RUN pip3 install -U pip


RUN apt-get install  libtesseract4 tesseract-ocr-osd tesseract-ocr -y
RUN apt-get install tesseract-ocr-eng -y
#RUN apt-get install tesseract-ocr-dev -y

COPY /diagramprep_package/dist/diagramprep-0.1-py3-none-any.whl /
COPY /testing/param_testing/requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /testing/param_testing/paramtest.py /app

ENV BLOB_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=searchstoragejstest;AccountKey=ecPjevJLinqMRmslQPyHtAoJ9NdzOQGLz/h8kTm6YSleu65nXVR6sPe+f1KVLt01Ok9EkdPDoY2vWrEHogDwhQ==;EndpointSuffix=core.windows.net'
ENV BLOB_CONTAINER='paramtesting'

ENTRYPOINT [ "/env3/bin/python3", "-u", "./paramtest.py" ]
