{{ config(materialized='view') }}
SELECT * FROM {{ get_primes_up_to(500) }}