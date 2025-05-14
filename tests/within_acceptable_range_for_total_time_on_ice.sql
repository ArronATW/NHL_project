SELECT 
  *
FROM {{ ref('cleaned_game_skater_stats') }}
WHERE time_on_ice + (penalty_minutes * 60) NOT BETWEEN 0 AND 3900