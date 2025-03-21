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

## Tranform Steps:
1. Data Cleaning(Làm sạch dữ liệu)
    - Xử lý giá trị thiếu (Missing Values)
    - Loại bỏ dữ liệu trùng lặp (Deduplication)
    - Chuẩn hóa định dạng dữ liệu
    - Loại bỏ dữ liệu ngoại lệ (Outliers Handling)
2. Biến đổi cấu trúc dữ liệu (Data Structuring)
    - Chuẩn hóa tên cột (từ viết tắt, tên không rõ ràng)
    - Gom nhóm dữ liệu (Aggregation)
    - Chuyển đổi dữ liệu dạng bảng (Pivoting & Unpivoting)
    - Chuẩn hóa dữ liệu về dạng chuẩn (Data Normalization)
3. Xác thực dữ liệu (Data Validation)
4. Ánh xạ dữ liệu (Data Join & Merging)
5. Tạo đặc trưng (Feature Engineering)

## Load Steps:
1. Xác định phương thức Load Data (full load or Incremental Load)
2. Định dạng dữ liệu trước khi Load
3.  Kiểm tra ràng buộc dữ liệu (Data Integrity Checks)
4. Xử lý lỗi và đảm bảo tính toàn vẹn dữ liệu
5. Kiểm tra hiệu suất và tối ưu hóa Load Data
6.  Kiểm tra lại sau khi Load (Data Validation)

### Reference 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup
https://docs.getdbt.com/docs/build/seeds
https://cloud.google.com/sdk/docs/install#deb

