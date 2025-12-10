-- Pixar Films Fact Table
-- This model joins public_response, pixar_films, and box_office tables
-- to create a comprehensive view of Pixar films with all related metrics

with pixar_films as (
    select * from {{ ref('pixar_films') }}
),

public_response as (
    select * from {{ ref('public_response') }}
),

box_office as (
    select * from {{ ref('box_office') }}
),

pixar_people as (
    select * from {{ ref('pixar_people') }}
)

select
    -- Film identification and details
    pf.number as film_number,
    pf.film,
    pf.release_date,
    pf.run_time,
    pf.film_rating,
    pf.plot,
    
    -- Public response metrics
    pr.rotten_tomatoes_score,
    pr.rotten_tomatoes_counts,
    pr.metacritic_score,
    pr.metacritic_counts,
    pr.cinema_score,
    pr.imdb_score,
    pr.imdb_counts,
    
    -- Box office metrics
    bo.box_office_us_canada,
    bo.box_office_other,
    bo.box_office_worldwide,
    case 
        when bo.budget = 'NA'
        then null
        else bo.budget
    end as film_budget,
    case 
        when bo.budget = 'NA' and bo.budget is null
        then null
        else bo.box_office_worldwide - bo.budget
    end as profit,
    case 
        when bo.budget = 'NA' and bo.budget = 0 and bo.budget is null
        then null
        else (bo.box_office_worldwide - bo.budget) / bo.budget
    end as profit_ratio,
    pp.name as director

from pixar_films as pf
left join public_response as pr on pf.film = pr.film
left join box_office as bo on pf.film = bo.film
left join pixar_people as pp on pf.film = pp.film
where pp.role_type = 'Director'
