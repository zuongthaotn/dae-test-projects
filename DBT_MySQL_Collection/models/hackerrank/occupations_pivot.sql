{{ config(materialized='view') }}

WITH Ranked AS (
  SELECT
    Name,
    Occupation,
    ROW_NUMBER() OVER (PARTITION BY Occupation ORDER BY Name) AS rn
  FROM hackerrank.occupations
),
Pivoted AS (
  SELECT
    MAX(CASE WHEN Occupation = 'Doctor' THEN Name END) AS Doctor,
    MAX(CASE WHEN Occupation = 'Professor' THEN Name END) AS Professor,
    MAX(CASE WHEN Occupation = 'Singer' THEN Name END) AS Singer,
    MAX(CASE WHEN Occupation = 'Actor' THEN Name END) AS Actor
  FROM Ranked
  GROUP BY rn
)
SELECT * FROM Pivoted