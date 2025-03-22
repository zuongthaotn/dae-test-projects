
1. Run "dbt run --full-refresh --select orders" có tạo view nhưng dữ liệu không được insert dù dữ liệu nguồn có data
Ngay cả khi run raw sql tren bigQuery cũng ko thấy data đc insert, chỉ thấy view được tạo ra.
View thì ko thấy insert data, tuy nhiên tạo table thì lại ok

  create or replace table `gg-bigquery-datawarehouse`.`SilverLayer`.`orders`
  OPTIONS()
  as SELECT * FROM `gg-bigquery-datawarehouse.BronzeLayer.orders`
--> pending

2. transform orders table from BronzeLayer to SilverLayer
-- Solution 1: JOIN (LEFT or INNER)
-- SELECT 
--     orders.order_id AS order_id,
--     ANY_VALUE(orders.customer_id) AS customer_id,
--     ANY_VALUE(orders.order_status) AS order_status 
-- FROM `gg-bigquery-datawarehouse.BronzeLayer.orders` as orders 
-- LEFT JOIN `gg-bigquery-datawarehouse.BronzeLayer.order_items` as order_items 
-- ON orders.order_id = order_items.order_id 
-- GROUP BY orders.order_id
-- Nhưng BigQuery yêu cầu mọi cột không được tổng hợp phải có trong GROUP BY, nhưng các cột đc lấy nếu có giá trị null hoặc giống nhau sẽ -> kquả bị sai. Sử dụng ANY_VALUE thay vì group by
-- Solution 2: 