from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import datetime

# Define Default Arguments
_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}

MYSQL_USER = 'magento'
MYSQL_PASS = 'magento123'
DB_NAME = 'kjcom'
BACKUP_FOLDER = '/var/www/html/db/'

with DAG(
    dag_id="backup_database_midnight",
    default_args=_args,
    description="The DAG for backing up database every day",
    start_date = pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["mysql", "magnus-tasks"],
) as dag:
    now = datetime.now()
    sql_filename = BACKUP_FOLDER + 'schema-backup-' + now.strftime("%m-%d-%Y-%H-%M-%S") + '.sql'
    BashOperator(
        task_id="backup_db",
        bash_command=f"mysqldump -d -u{MYSQL_USER} -p{MYSQL_PASS} {DB_NAME} > {sql_filename}"
    )
