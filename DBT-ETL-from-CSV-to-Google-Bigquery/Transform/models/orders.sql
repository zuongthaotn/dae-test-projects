SELECT 
    orders.order_id as order_id
    , ANY_VALUE(orders.customer_id) as customer_id
    , ANY_VALUE(orders.order_status) as order_status
    , ANY_VALUE(orders.order_purchase_timestamp) as purchase_time
FROM `gg-bigquery-datawarehouse.BronzeLayer.orders` as orders 
INNER JOIN `gg-bigquery-datawarehouse.BronzeLayer.order_items` as order_items 
ON orders.order_id = order_items.order_id 
GROUP BY orders.order_id