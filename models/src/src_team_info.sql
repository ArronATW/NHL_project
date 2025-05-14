WITH raw_team_info AS (
     SELECT * FROM {{ source('nhl', 'raw_team_info') }}
)
SELECT
     team_id,
     franchise_id,
     short_name AS team_location,
     team_name AS team_nickname,
     abbreviation AS team_abbreviation,
     link AS team_api_link
FROM
     raw_team_info