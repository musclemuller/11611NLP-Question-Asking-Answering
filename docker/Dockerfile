# Ubuntu Linux as the base image
FROM ubuntu:22.04
FROM python:3.7.13-slim-buster
# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python
RUN apt-get -y update && \
    apt-get -y upgrade

# The following line ensures that subsequent install doesn't expect user input
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install python3-pip python3-dev

# Install spaCy
RUN pip3 install --upgrade pip
RUN pip3 install spacy
RUN pip3 install stanza
RUN pip3 install nltk
RUN apt-get install -y wget
RUN apt-get install -y unzip
RUN python3 -m spacy download en_core_web_lg
RUN python3 -c 'import stanza; stanza.download("en")'
RUN python3 -c 'import nltk; nltk.download("punkt")'
#RUN pip3 install tensorflow==1.15
RUN python3 -m pip install --no-cache-dir --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
RUN pip3 install numpy==1.19.5

# Add the files into container, under QA folder, modify this based on your need
RUN mkdir /QA
RUN wget -P /QA https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip
RUN unzip /QA/uncased_L-12_H-768_A-12.zip -d /QA/uncased_L-12_H-768_A-12
ADD docker/ask /QA
ADD docker/answer /QA
ADD Answering /QA/Answering
ADD Asking /QA/Asking
ADD data /QA/data
ADD test_questions.txt /QA
ADD tag.py /QA

# Change the permissions of programs
CMD ["chmod 777 /QA/*"]

# Set working dir as /QA
WORKDIR /QA
ENTRYPOINT ["/bin/bash", "-c"]
