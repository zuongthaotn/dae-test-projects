## Requirements:
- Collect Upcoming releases movies(US base) data from IMDB
- Design database for saving movie information
- Write ETL pipeline for automating workflow.
- Building recommendation systems


## Tech stacks:
- Data Ingestion: IMDB, python
- Processing: Apache Spark, pandas
- Storage: MongoDB
- Visualization: powerBI


## Steps
1. Start airflow
- ./start_airflow.sh

2. install mongoDB
    - Follow steps in reference

3. Start mongoDB
    - sudo systemctl start mongod
    - sudo systemctl stop mongod
    - sudo systemctl restart mongod

## Reference
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu