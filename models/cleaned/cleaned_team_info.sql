-- no deduplication needed, all team_id are unique
WITH src_team_info AS (
  SELECT
    *
  FROM
  {{ ref('src_team_info') }}
)
SELECT
    team_id::INT AS team_id,
    franchise_id::INT AS franchise_id,
    team_location,
    team_nickname,
    team_abbreviation,
    team_api_link
FROM src_team_info
ORDER BY team_id