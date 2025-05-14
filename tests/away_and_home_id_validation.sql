SELECT 
  *
FROM {{ ref('cleaned_game') }}
WHERE away_team_id = home_team_id