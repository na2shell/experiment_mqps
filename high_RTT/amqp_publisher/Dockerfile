FROM centos:centos7

WORKDIR /home

RUN yum update -y
RUN yum install -y python3
RUN pip3 install pika

COPY ./src ./src
