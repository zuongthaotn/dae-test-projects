## Requirements:
- Collect books data from Goodreads
- Design database for saving books information
- Write ETL pipeline for automating workflow.
- Building recommendation systems


## Tech stacks:
- Data Ingestion: python, scrapy
- Processing: pandas, DBT
- Storage: Mysql, csv
- Orchestration: Airflow
- Visualization: matplotlib


## Steps
1. Move airflow dag folder to current project dags
2. Start airflow
- ./start_airflow.sh

3. Install dbt mysql
4. Init project 
    - create files in folder dbt/

5. update content files
./dbt_project.yml
./profiles.yml

6. dun "dbt debug" for testing config & connection

7. run "dbt run"