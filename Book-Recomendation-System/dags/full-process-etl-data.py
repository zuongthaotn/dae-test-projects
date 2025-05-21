from __future__ import annotations
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from pathlib import Path
import pendulum
from services.get_new_released_book_url import get_goodreads_books_list


with DAG(
    "etl_book_list",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["magnus"],
) as dag:
    task_start = EmptyOperator(
        task_id="start_ok",
    )
    project_folder = Path(__file__).parent.parent
    #
    extract_data = PythonOperator(task_id="get_goodreads_book_list", python_callable=get_goodreads_books_list)
    #
    def mysql_insert_data():
        print("inserting data")
        current_folder = Path(__file__)
        csv_file = str(current_folder.parent.parent) + "/book-list.csv"
        cfg_mysql_conn = 'mysql_dynamic'
        cfg_mysql_db = 'book_bronze_layer'
        with open(csv_file, 'r') as file:
            for line in file:
                try:
                    row_data = line.split(",")
                    sql = f"INSERT into {cfg_mysql_db}.book(name, url, extra_info) \
                        VALUES(\"{row_data[0]}\", \"{row_data[1]}\", \"{row_data[2]}\")"
                    hook = MySqlHook(mysql_conn_id = cfg_mysql_conn, schema = cfg_mysql_db)
                    hook.run(sql, autocommit=True, parameters=None)
                except Exception:
                    print("Error while inserting data")
                    print(sql)
                    continue

    insert_data = PythonOperator(task_id="insert_mysql_data", python_callable=mysql_insert_data)
    #
    task_end = EmptyOperator(
        task_id="end_ok",
    )
    task_start >> extract_data >> insert_data >> task_end
