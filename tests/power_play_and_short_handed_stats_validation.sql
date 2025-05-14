SELECT 
  *
FROM {{ ref('cleaned_game_skater_stats') }}
WHERE power_play_goals > goals
  OR power_play_assists > assists
  OR short_handed_goals > goals
  OR short_handed_assists > assists