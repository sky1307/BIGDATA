#!/bin/bash
docker build -t pyspark-notebook:release ./docker/pyspark-notebook
docker build -t spark-base:release ./docker/spark-base
docker build -t spark-master:release ./docker/spark-master
docker build -t spark-worker:release ./docker/spark-worker
