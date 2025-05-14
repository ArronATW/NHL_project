WITH cleaned_game_skater_stats AS (
  SELECT * FROM {{ ref('cleaned_game_skater_stats') }}
), cleaned_with_valid_team_id_rows AS (
  SELECT * FROM cleaned_game_skater_stats
  WHERE team_id IN (
    SELECT team_id FROM {{ ref('dim_team') }}
  )
)
SELECT
  {{ dbt_utils.generate_surrogate_key(['player_id', 'game_id', 'team_id']) }} AS skater_game_fact_id,
  player_id,
  game_id,
  team_id,
  -- offensive stats
  goals,
  assists,
  shots_on_goal,
  time_on_ice,
  ROUND(((goals::FLOAT * 100) / CASE WHEN shots_on_goal = 0 THEN 1 ELSE shots_on_goal END), 2)  AS scoring_efficiency_percentage,
  ROUND((goals / ((CASE WHEN time_on_ice = 0 THEN 1 ELSE time_on_ice END) / 60.0)), 2) AS goals_per_minute,
  ROUND((assists / ((CASE WHEN time_on_ice = 0 THEN 1 ELSE time_on_ice END) / 60.0)), 2) AS assists_per_minute,
  face_off_wins, 
  face_off_taken,
  -- higher face_off_pct indicate better puck control, both offensive and defensive stat
  ROUND(((face_off_wins::FLOAT * 100) / CASE WHEN face_off_taken = 0 THEN 1 ELSE face_off_taken END), 2) AS face_off_win_percentage,
  takeaways,
  -- lesser giveaways  indirectly means more chances to score via goals/assists
  giveaways,
  -- defensive stats
  hits,
  blocked_shots,
  ROUND((hits / ((CASE WHEN time_on_ice = 0 THEN 1 ELSE time_on_ice END) / 60.0)), 2) AS hits_per_minute,
  -- power play/penalty kill impact
  power_play_goals,
  power_play_assists,
  power_play_time_on_ice,
  short_handed_goals,
  short_handed_assists,
  short_handed_time_on_ice,
  ROUND(((power_play_goals + power_play_assists) / ((CASE WHEN power_play_time_on_ice = 0 THEN 1 ELSE power_play_time_on_ice END) / 60.0)), 1) 
      AS power_play_points_per_minute,
  ROUND(((short_handed_goals + short_handed_assists) / ((CASE WHEN short_handed_time_on_ice = 0 THEN 1 ELSE short_handed_time_on_ice END) / 60.0)), 1) 
      AS short_handed_points_per_minute
FROM cleaned_with_valid_team_id_rows