from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.hooks.base import BaseHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import Connection
from airflow.settings import Session
from airflow import settings
from airflow.models import BaseOperator
import time

# 1️⃣ Define Default Arguments
_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 20),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1
}

MYSQL_USER = 'magento'
MYSQL_PASS = 'magento123'
DB_NAME = 'test_airflow'


# 2️⃣ Define DAG using 'with' statement
with DAG(
    dag_id="data_from_csv_to_mysql",  # DAG ID
    default_args=_args,
    description="The DAG works with csv & mysql process.",
    schedule_interval="@daily",  # Runs daily
    catchup=False,  # Prevents running past dates
    tags=["mysql", "magnus's tasks"],
) as dag:
    
    drop_db_if_exist = BashOperator(
        task_id="drop_db_if_exist",
        bash_command=f"mysql -u{MYSQL_USER} -p{MYSQL_PASS} --execute='DROP DATABASE IF EXISTS {DB_NAME};'",
    )

    create_db = BashOperator(
        task_id="create_db_if_not_exist",
        bash_command=f"mysql -u{MYSQL_USER} -p{MYSQL_PASS} --execute='CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET = \"utf8mb4\" DEFAULT COLLATE \"utf8mb4_unicode_ci\";'",
    )

    def create_hook_connection():
        try:
            conn = BaseHook.get_connection("mysql_dynamic")
        except Exception:
            conn = Connection(
                conn_id="mysql_dynamic",
                conn_type="mysql",
                host="localhost",
                schema=f"{DB_NAME}",
                login=f"{MYSQL_USER}",
                password=f"{MYSQL_PASS}",
                port=3306
            )
            session = settings.Session()
            session.add(conn)
            session.commit()

    mysql_dynamic = PythonOperator(task_id="create_hook_connection", python_callable=create_hook_connection)

    def mysql_create_table():
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        hook = MySqlHook(mysql_conn_id='mysql_dynamic', schema='test_airflow')
        hook.run(sql, autocommit=True, parameters=None)

    create_table = PythonOperator(task_id="create_mysql_table", python_callable=mysql_create_table)

    def mysql_insert_data():
        ts = time.time()
        sql = "INSERT into test_airflow.users(name, email) VALUES('Test', 'test-" + str(ts) +"@gmail.com')"
        hook = MySqlHook(mysql_conn_id = 'mysql_dynamic', schema = 'test_airflow')
        hook.run(sql, autocommit=True, parameters=None)

    insert_data = PythonOperator(task_id="insert_mysql_data", python_callable=mysql_insert_data)

    # Define Task Dependencies
    drop_db_if_exist >> create_db >> mysql_dynamic >> create_table >> insert_data
