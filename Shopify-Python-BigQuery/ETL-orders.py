import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Thông tin cấu hình
SHOP_NAME = os.getenv("SHOP_NAME")
X_TOKEN = os.getenv("ACCESS_TOKEN")

# URL Shopify API
url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2025-04/graphql.json"


headers = {
    "X-Shopify-Access-Token": X_TOKEN,
    "Content-Type": "application/json"
}

payload = '{"query": "query { orders(first: 10) { edges { cursor node { name createdAt customer { displayName }  totalPriceSet { shopMoney { amount currencyCode } } } } pageInfo { hasNextPage hasPreviousPage startCursor endCursor } } }"}'

# Gọi API
response = requests.post(url, headers=headers, data=payload)
response_json = response.json()

orders = []
data = response_json['data']['orders']['edges']
for item in data:
    order = {
            "name": item['node']['name'], 
             "created_at": pd.to_datetime(item['node']['createdAt']), 
             "customer": item['node']['customer']['displayName'], 
             "total_price": item['node']['totalPriceSet']['shopMoney']['amount'], 
             "currency_code": item['node']['totalPriceSet']['shopMoney']['currencyCode']
            }
    orders.append(order)

df = pd.DataFrame(orders)

current_folder = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_folder, "shopify_orders.csv")

# Lưu vào CSV (hoặc push vào DB)
df.to_csv(csv_file, index=False)

# Connect to BigQuery
from google.cloud import bigquery
key_file = os.path.join(current_folder, "google-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file
client = bigquery.Client()
project_id = "gg-bigquery-datawarehouse"
dataset_id = "Test"
table_id = "shopify_orders"

# Full table name
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# Insert dữ liệu vào BigQuery
job = client.load_table_from_dataframe(df, table_ref)

job.result()  # Chờ job hoàn tất

