## Requirements:
1. Create 3 layers(BronzeLayer, SilverLayer, GoldLayer) in Googgle BigQuery
2. Upload csv files (Wide World Importers dataset) to BronzeLayer
3. Transform data from BronzeLayer to SilverLayer
4. Modeling data from SilverLayer and save to GoldLayer


## Steps:
1. Go to Goole BigQuery -> create 3 datasets
    - BronzeLayer
    - SilverLayer
    - GoldLayer
2. Create folder ./dbt-goole-bigquery/datasets
3. Download dataset "brazilian-ecommerce" from kaggle
then extract to ./dbt-goole-bigquery/datasets
4. Copy and rename files .csv from ./datasets to ./seeds as name as you want to be in Google BigQuery
4. Create google keyfile.json
run:
    - sudo bash install-gcloud.sh
    - gcloud auth login
    - gcloud config set project gg-bigquery-datawarehouse
    - gcloud iam service-accounts keys create google-key.json --iam-account=gg-21032025@gg-bigquery-datawarehouse.iam.gserviceaccount.com
    Don't forget changing the "gg-bigquery-datawarehouse" by your bigquery projectID
4.1. if you can not create google-key.json by command you can follow UI steps:
    - Go to Goolge console
    - Navigation menu (top left) -> AIM & Admin -> Services Account -> Create service account -> create a new one
    - Click the keynew created Service Account -> Keys -> Add key -> choose JSON -> a file JSOn is downloaded -> copy file JSON to here and rename to google-key.json
5. copy file profiles.sample.yml -> profiles.yml
Change by your own information
6. cd to dbt-goole-bigquery and run 
dbt seed --select "file_name_without_.csv"
You need to run one by one or run "dbt seed" to seed all file csv to Google BigQuery


### Reference 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup
https://docs.getdbt.com/docs/build/seeds
https://cloud.google.com/sdk/docs/install#deb

