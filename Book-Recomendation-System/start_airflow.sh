#!/bin/bash
#
export AIRFLOW_HOME=~/airflow
#
CUR_DIR=$(pwd)
#
export AIRFLOW__CORE__DAGS_FOLDER=$CUR_DIR/dags
#
export PYTHONPATH=$CUR_DIR
#
source ../.venv/bin/activate
#
pkill -f "airflow webserver" &
wait; pkill -f "airflow scheduler" &
#
wait; airflow webserver -p 8080 & airflow scheduler &
