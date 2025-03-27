#!/bin/bash
#
export AIRFLOW_HOME=~/airflow
#
CUR_DIR=$(pwd)
#
export AIRFLOW__CORE__DAGS_FOLDER=$CUR_DIR/dags
#
source ../.venv/bin/activate
#
airflow webserver -p 8080 & airflow scheduler &