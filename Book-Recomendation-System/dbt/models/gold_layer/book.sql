{{ config(materialized='table') }}

SELECT
    id,
    name,
    url,
    TRIM(REPLACE(SUBSTRING_INDEX(extra_info, '-', 1), 'avg rating', '')) AS avg_rating,
    TRIM(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(extra_info, '-', 2), '-', -1), 'ratings', '')) AS num_ratings,
    TRIM(REPLACE(SUBSTRING_INDEX(extra_info, '-', -1), 'published', '')) AS published_year
FROM 
    {{ source('book_bronze_layer', 'book') }}