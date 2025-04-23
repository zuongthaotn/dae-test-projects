from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth

project_folder = '/mnt/shares/dae-test-projects/HorseRacingAPI'
dag_folder = project_folder + '/dags'
data_folder = project_folder + '/data'
load_dotenv(dotenv_path=dag_folder+'/.env')
userame = os.getenv("TRP_USERNAME")
password = os.getenv("TRP_PASSWORD")

def fetch_owners_then_save_json():
    url = "https://api.theracingapi.com/v1/owners/search"
    params = {}
    response = requests.request("GET", url, auth=HTTPBasicAuth(userame, password), params=params)
    with open(data_folder + '/owners.json', 'w') as f:
        json.dump(response.json(), f, indent=2)

with DAG(
    dag_id='get_horse_racing_owners',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    get_owners = PythonOperator(task_id="get_owners", python_callable=fetch_owners_then_save_json)
    #
    get_owners
