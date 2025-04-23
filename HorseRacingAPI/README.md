# Requirements

Ingest data from the API into big query to allow me to carryout downstream analysis and machine learning.
Key deliverables include
- Ingesting all API data into the Big Query including all historical data to form the initial database
- Create an automated pipeline that will update the database twice per day.
- Clearly documented schema and database design documents to allow interpretation and understanding
- Ideally the pipeline will be self sustaining and no touch unless there are major API updates but would appreciate a handover document for quick tips and FAQs to support day to day running and any issues with daily operation.
- Insight on the ongoing monthly costs I can expect from google to store the database and run the daily updates based on estimated final database sizes.

# Tools & tech stacks
    - Apache Airflows
    - Google BigQuery
    - Python
# Environments
    - Distributor ID: Ubuntu
        Description:    Ubuntu 22.04.5 LTS
        Release:        22.04
        Codename:       jammy
    - Python 3.11.4 (/mnt/shares/dae-test-projects/.venv/bin/python)
    - pip 25.0.1 from /mnt/shares/dae-test-projects/.venv/lib/python3.11/site-packages/pip (python 3.11)
    - Apache Airflows (installed)

# Steps
1. Change airflow dags folder
    - edit file /home/zuongthao/airflow/airflow.cfg (it maybe depend on the folder you installed airflow)
        change dags_folder = /home/zuongthao/airflow/dags 
        to new folder you write dag scripts
        such dags_folder = /mnt/shares/dae-test-projects/HorseRacingAPI/dags
2. Check airflow bigquery operator
    - pip list | grep apache-airflow[google]
    - pip install 'apache-airflow[google]'
3. Register 
    - https://www.theracingapi.com/#subscribe
4. Run airflow
    - cd /mnt/shares/dae-test-projects/
    - run source .venv/bin/activate
    - reset airflow db by 
        - airflow db reset
        - airflow db init
        - airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
    - cd HorseRacingAPI
    - bash start_airflow.sh

5. Configure Google Bigquery Connection via Airflow UI
    - the Airflow web UI (usually at http://localhost:8080)

    - Go to Admin > Connections
    - Click "+ Add a new record"
    - Set the following:
        Field	Value
        Conn Id	google_cloud_default (or any custom name)
        Conn Type	Google Cloud
        Project Id	Your GCP project ID
        Keyfile Path	Path to your JSON key (e.g. /path/to/service-account.json)
        Scopes	https://www.googleapis.com/auth/cloud-platform
        Alt`ernatively, if you're using keyfile JSON string, set Keyfile JSON instead of Path.
    - Click Save
6. Run DAGs