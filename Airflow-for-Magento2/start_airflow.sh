#!/bin/bash
#
export AIRFLOW_HOME=~/airflow
#
source ../.venv/bin/activate
#
airflow webserver -p 8080 & airflow scheduler &