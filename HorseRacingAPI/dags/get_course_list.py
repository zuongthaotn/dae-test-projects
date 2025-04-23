from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

project_folder = '/mnt/shares/dae-test-projects/HorseRacingAPI'
dag_folder = project_folder + '/dags'
data_folder = project_folder + '/data'
load_dotenv(dotenv_path=dag_folder+'/.env')
userame = os.getenv("TRP_USERNAME")
password = os.getenv("TRP_PASSWORD")

def fetch_courses_then_save_json():
    url = "https://api.theracingapi.com/v1/courses"
    params = {}
    response = requests.request("GET", url, auth=HTTPBasicAuth(userame, password), params=params)
    json_data = response.json()
    courses = json_data["courses"]
    # Write in NDJSON format
    with open(data_folder + '/courses.json', "w") as f:
        for item in courses:
            json.dump(item, f)
            f.write("\n")

with DAG(
    dag_id='get_horse_racing_courses',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    get_courses = PythonOperator(task_id="get_courses", python_callable=fetch_courses_then_save_json)
    #
    create_table = BigQueryCreateTableOperator(
        task_id="create_courses_table",
        project_id="gg-bigquery-datawarehouse",
        dataset_id="HorseRacing",
        table_id="courses",
        table_resource={
            "schema": {
                "fields": [
                    {"name": "id", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "course", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "region_code", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "region", "type": "STRING", "mode": "REQUIRED"}
                ]
            },
            "timePartitioning": {
                "type": "DAY"
            }
        },
        gcp_conn_id="google_bigquery_default"
    )
    #
    upload_courses_to_gcs = LocalFilesystemToGCSOperator(
            task_id="upload_local_json_to_gcs",
            src=data_folder+"/courses.json",
            dst="hra/courses.json",
            bucket="magnus-test-01",
            gcp_conn_id="google_bigquery_default",
            mime_type="application/json",
        )
    move_courses_from_gcs_to_bigquery = GCSToBigQueryOperator(
        task_id='move_courses_to_bigquery',
        bucket='magnus-test-01',
        source_objects=['hra/courses.json'],
        destination_project_dataset_table='gg-bigquery-datawarehouse.HorseRacing.courses',
        schema_fields=[
            {"name": "id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "course", "type": "STRING", "mode": "REQUIRED"},
            {"name": "region_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "region", "type": "STRING", "mode": "REQUIRED"}
        ],
        source_format="NEWLINE_DELIMITED_JSON",
        autodetect=True,
        gcp_conn_id="google_bigquery_default",
        write_disposition='WRITE_TRUNCATE',
    )
    
    get_courses >> create_table >> upload_courses_to_gcs >> move_courses_from_gcs_to_bigquery
