#!/bin/bash
#
export AIRFLOW_HOME=~/airflow
#
# source ../.venv/bin/activate
#
airflow webserver -p 9090 & airflow scheduler &