{{ config(materialized='table') }}

SELECT
    id,
    name,
    url,
    CAST(TRIM(REPLACE(SUBSTRING_INDEX(extra_info, '-', 1), 'avg rating', '')) AS DECIMAL(3,2))  AS avg_rating,
    CAST(TRIM(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(extra_info, '-', 2), '-', -1), 'ratings', ''), ',', '')) AS UNSIGNED) AS num_ratings,
    CAST(TRIM(REPLACE(SUBSTRING_INDEX(extra_info, '-', -1), 'published', '')) AS UNSIGNED) AS published_year
FROM 
    {{ source('book_bronze_layer', 'book') }}