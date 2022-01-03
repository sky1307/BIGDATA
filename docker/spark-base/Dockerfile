FROM python:3.7-stretch
LABEL version="0.2"

ENV DAEMON_RUN=true
ENV APACHE_SPARK_VERSION=2.4.1
ENV HADOOP_VERSION=2.7

RUN apt-get update \
 && apt-get install -y openjdk-8-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
 
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates jq

# Add Dependencies for PySpark
RUN apt-get install -y python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy
RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1
RUN pip install pymongo pyspark

COPY spark-2.4.1-bin-hadoop2.7.tgz /tmp/
WORKDIR /tmp
RUN tar xzf "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" --owner root --group root --no-same-owner && \
    rm "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mv "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" "spark" && \
    mv "spark" "/"
    

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV PYTHONHASHSEED 1


