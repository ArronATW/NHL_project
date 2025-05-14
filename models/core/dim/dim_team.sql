WITH cleaned_team_info AS (
  SELECT * FROM {{ ref('cleaned_team_info') }}
)
SELECT
  team_id,
  franchise_id,
  team_location || ' ' || team_nickname AS team_name,
  team_abbreviation
FROM cleaned_team_info
