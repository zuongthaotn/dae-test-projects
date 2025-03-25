from airflow import DAG
from airflow.operators.bash import BashOperator
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
    start_date = datetime(2024, 3, 20),
    schedule="@daily",
    catchup=False,
    tags=["mysql", "magnus's tasks"],
) as dag:
    now = datetime.now()
    sql_filename = BACKUP_FOLDER + 'backup-' + now.strftime("%m-%d-%Y-%H-%M-%S") + '.sql'
    backup_db = BashOperator(
        task_id="backup_db",
        bash_command=f"mysqldump -u{MYSQL_USER} -p{MYSQL_PASS} {DB_NAME} > {sql_filename}"
    )

    backup_db