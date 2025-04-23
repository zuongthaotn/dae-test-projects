from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator, BigQueryCreateTableOperator

project_folder = '/mnt/shares/dae-test-projects/HorseRacingAPI'
dag_folder = project_folder + '/dags'
data_folder = project_folder + '/data'
load_dotenv(dotenv_path=dag_folder+'/.env')
userame = os.getenv("TRP_USERNAME")
password = os.getenv("TRP_PASSWORD")

def fetch_regions():
    url = "https://api.theracingapi.com/v1/courses/regions"
    params = {}
    response = requests.request("GET", url, auth=HTTPBasicAuth(userame, password), params=params)
    return response.json()

def fetch_regions_then_save_json():
    json_regions = fetch_regions()
    if json_regions:
        with open(data_folder+'/courses_regions.json', 'w') as f:
            json.dump(json_regions, f, indent=2)

def get_insert_query():
    with open(data_folder+'/courses_regions.json', 'r') as f:
        data = json.load(f)
    if data:
        insert_query = "INSERT INTO `gg-bigquery-datawarehouse.HorseRacing.courses_regions` (region, region_code) VALUES "
        for item in data:
            insert_query += f"('{item['region']}', '{item['region_code']}'), "
        insert_query = insert_query[:-2] + ";"
        # print(insert_query)
        return insert_query
    else:
        return ''

with DAG(
    dag_id='get_horse_racing_courses_regions',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    get_courses_regions = PythonOperator(task_id="get_courses_regions", python_callable=fetch_regions_then_save_json)
    #
    create_table = BigQueryCreateTableOperator(
        task_id="create_courses_regions_table",
        dataset_id="HorseRacing",
        table_id="courses_regions",
        project_id="gg-bigquery-datawarehouse",
        table_resource={
            "schema": {
                "fields": [
                    {"name": "region", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "region_code", "type": "STRING", "mode": "REQUIRED"}
                ]
            },
            "timePartitioning": {
                "type": "DAY"
            }
        },
        gcp_conn_id="google_bigquery_default"
    )
    #
    insert_query = get_insert_query()
    if insert_query:
        push_courses_regions = BigQueryInsertJobOperator(
            task_id="push_courses",
            gcp_conn_id="google_bigquery_default",  
            configuration={
                "query": {
                    "query": insert_query,
                    "useLegacySql": False
                }
            },
        )
        get_courses_regions >> create_table >> push_courses_regions
    else:
        get_courses_regions >> create_table
