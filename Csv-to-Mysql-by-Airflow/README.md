
# Install airflow
https://github.com/zuongthaotn/auto-4works/tree/master/airflow

# Datasets
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
Import csv datasets to mysql database


# Steps
1. Change airflow dags folder
        edit file /home/zuongthao/airflow/airflow.cfg (it maybe depend on the folder you installed airflow)
        change dags_folder = /home/zuongthao/airflow/dags 
        to new folder you write dag scripts
        such dags_folder = /mnt/shares/dae-test-projects/Csv-to-Mysql-by-Airflow/dags
2. Install airflow mysql operator
    pip install apache-airflow-providers-mysql
    If you got error:
        Exception: Can not find valid pkg-config name.
      Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually

    Solved by:
    - sudo apt install libmysqlclient-dev
    - export MYSQLCLIENT_CFLAGS="$(mysql_config --cflags)"
    - export MYSQLCLIENT_LDFLAGS="$(mysql_config --libs)"
    - pip install mysqlclient mysql-connector-python aiomysql 
    - pip install apache-airflow-providers-mysql

3. Add Airfow connection
  - use CLI
  airflow connections add 'mysql_dynamic_test' \
    --conn-type 'mysql' \
    --conn-login 'magento' \
    --conn-password 'magento123' \
    --conn-host 'localhost' \
    --conn-port '3306' \
    --conn-schema 'db_name'

  - use DAG

