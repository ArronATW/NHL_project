WITH cleaned_team_info AS (
  SELECT * FROM {{ ref('cleaned_team_info') }}
)
SELECT
  c.team_id,
  franchise_id,
  t.team_name,
  t.TEAM_PIC_URL,
  team_abbreviation
FROM cleaned_team_info c
LEFT JOIN {{ ref('team_logos') }} t ON c.team_id = t.id
