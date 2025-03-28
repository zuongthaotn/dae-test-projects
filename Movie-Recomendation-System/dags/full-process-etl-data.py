from __future__ import annotations
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path
import pendulum
from service.process_csv import tranform_data, load_data
from service.upcoming_movies import get_imdb_upcoming_movies


with DAG(
    "etl_upcoming_movies",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["magnus"],
) as dag:
    task_start = EmptyOperator(
        task_id="start_ok",
    )
    project_folder = Path(__file__).parent.parent
    remove_old_dataset = BashOperator(
        task_id="remove_old_dataset",
        bash_command=f"rm -rf {project_folder}/datasets/*"
    )
    #
    extract_data = PythonOperator(task_id="get_imdb_upcoming_movies", python_callable=get_imdb_upcoming_movies)
    #
    tranform_movie_data = PythonOperator(task_id="tranform_data_from_csv", python_callable=tranform_data)
    #
    load_data_to_mongodb = PythonOperator(task_id="load_data_to_mongodb", python_callable=load_data)
    # 
    task_end = EmptyOperator(
        task_id="end_ok",
    )
    task_start >> remove_old_dataset >> extract_data >> tranform_movie_data >> load_data_to_mongodb >> task_end
