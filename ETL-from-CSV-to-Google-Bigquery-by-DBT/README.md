## Requirements:
1. Create 3 layers(BronzeLayer, SilverLayer, GoldLayer) in Googgle BigQuery
2. Upload csv files (brazilian-ecommerce dataset) to BronzeLayer
3. Transform data from BronzeLayer to SilverLayer
4. Modeling data from SilverLayer and save to GoldLayer


## Preparation Steps
1. Create project folder (name such as dbt-goole-bigquery)
2. cd to project folder
3. Install dbt 
    - source ./venv/bin/activate
    - pip install dbt-core dbt-bigquery
4. Create folder "Extract" for Extract Steps, "Transform" for Transformation Steps, "Load" for Load Steps.

## Extract Steps:
1. Go to Goole BigQuery -> create BronzeLayer dataset
2. Create folder ./datasets
3. Download dataset "brazilian-ecommerce" from kaggle
then extract to ./datasets
4. Copy and rename files .csv from ./datasets to ./seeds as name as you want to be in Google BigQuery
4. Create google keyfile.json
run:
    - sudo bash install-gcloud.sh
    - gcloud auth login
    - gcloud config set project gg-bigquery-datawarehouse
    - gcloud iam service-accounts keys create google-key.json --iam-account=gg-21032025@gg-bigquery-datawarehouse.iam.gserviceaccount.com
    Don't forget changing the "gg-bigquery-datawarehouse" by your bigquery projectID and "gg-21032025" by other one
4.1. if you can not create google-key.json by command you can follow UI steps:
    - Go to Goolge console
    - Navigation menu (top left) -> AIM & Admin -> Services Account -> Create service account -> create a new one
    - Click the keynew created Service Account -> Keys -> Add key -> choose JSON -> a file JSOn is downloaded -> copy file JSON to here and rename to google-key.json
5. copy file profiles.sample.yml -> profiles.yml
Change by your own information
6. cd to dbt-goole-bigquery and run 
dbt seed --select "file_name_without_.csv"
You need to run one by one or run "dbt seed" to seed all file csv to Google BigQuery

## Tranform Steps:
1. Go to Goole BigQuery -> create SilverLayer dataset
2. Go to Transform folder, create new profiles.yml  & dbt_project.yml
3. Create folder "models", "analytics" folders
4. Create file "orders.sql"
5. run "dbt run --full-refresh --select orders"
* Các bảng khác tương tự
* BigQuery yêu cầu mọi cột không được tổng hợp phải có trong GROUP BY, nhưng các cột đc lấy nếu có giá trị null hoặc giống nhau sẽ -> kquả bị sai. Sử dụng ANY_VALUE thay vì group by

## Load Steps:
1. Go to Goole BigQuery -> create GoldLayer dataset
2. Go to Load folder, create new profiles.yml  & dbt_project.yml
3. Create folder "models", "analytics" folders
4. Create file "orders.sql"
5. Thay đổi file dbt_project.yml, chuyển từ cơ chế tạo view sang tạo table.
Load steps tương tự Transform steps tuy nhiên thay vì tạo view sẽ tạo table và có thể  sử dụng để phân tích được luôn.
    - phương thức Load Data full load

### Reference 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup
https://docs.getdbt.com/docs/build/seeds
https://cloud.google.com/sdk/docs/install#deb
https://docs.getdbt.com/docs/build/sql-models
