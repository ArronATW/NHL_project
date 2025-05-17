WITH fct_player_game_stats AS (
  SELECT * FROM {{ ref('fct_player_game_stats') }}
)
SELECT
  p.player_id,
  t.team_id,
  g.season_start,
  COUNT(DISTINCT p.game_id) AS games_played,
  SUM(p.goals) AS total_goals,
  SUM(p.assists) AS total_assists,
  SUM(p.goals + p.assists) AS total_points,
  SUM(p.shots_on_goal) AS total_shots,
  ROUND(SUM(p.time_on_ice) / 60.0) AS total_toi_min,
  SUM(p.face_off_wins) AS total_faceoff_wins,
  SUM(p.face_off_taken) AS total_faceoffs,
  SUM(p.hits) AS total_hits,
  SUM(p.blocked_shots) AS total_blocked,
  SUM(takeaways) AS total_takeaways,
  SUM(giveaways) AS total_giveaways,
  IFNULL(
    ROUND(
      SUM(p.hits) * 60 / 
      CASE 
        WHEN SUM(p.time_on_ice) = 0 THEN 1 
        ELSE (SUM(p.time_on_ice) / 60.0) 
      END, 2), 0) AS hits_per_60minute,
  IFNULL(
    ROUND(
      SUM(p.blocked_shots) * 60 / 
      CASE 
        WHEN SUM(p.time_on_ice) = 0 THEN 1 
        ELSE (SUM(p.time_on_ice) / 60.0) 
      END, 2), 0) AS blocked_shots_per_60minute,
  ROUND(SUM(p.goals) * 60 / CASE WHEN SUM(p.time_on_ice) = 0 THEN 1 ELSE (SUM(p.time_on_ice) / 60.0) END, 2) AS goals_per_60minute,
  ROUND(SUM(p.assists) * 60 / CASE WHEN SUM(p.time_on_ice) = 0 THEN 1 ELSE (SUM(p.time_on_ice) / 60.0) END, 2) AS assists_per_60minute,
  IFNULL(
    ROUND(
      SUM(takeaways) * 60 /
      CASE
        WHEN SUM(p.time_on_ice) = 0 THEN 1
        ELSE (SUM(p.time_on_ice) / 60.0)
      END, 2), 0) AS takeaways_per_60mins,
  IFNULL(
    ROUND(
      SUM(giveaways) * 60 /
      CASE
        WHEN SUM(p.time_on_ice) = 0 THEN 1
        ELSE (SUM(p.time_on_ice) / 60.0)
      END, 2), 0) AS giveaways_per_60mins,
  SUM(p.power_play_goals + p.power_play_assists) AS total_pp_points,
  ROUND(SUM(p.power_play_time_on_ice) / 60.0) AS total_pp_minutes,
  ROUND(
    SUM(p.power_play_goals + p.power_play_assists) * 60
     / CASE WHEN SUM(p.power_play_time_on_ice) = 0 THEN 1 ELSE (SUM(p.power_play_time_on_ice) / 60.0) END, 2) AS total_pp_points_per_60minute,
  SUM(p.short_handed_goals + p.short_handed_assists) AS total_sh_points,
  ROUND(SUM(p.short_handed_time_on_ice) / 60.0) AS total_sh_minutes,
  ROUND(
    SUM(p.short_handed_goals + p.short_handed_assists) * 60
     / CASE WHEN SUM(p.short_handed_time_on_ice) = 0 THEN 1 ELSE (SUM(p.short_handed_time_on_ice) / 60.0) END, 2) AS total_sh_points_per_60minute

FROM {{ ref('fct_player_game_stats') }} p
JOIN {{ ref('dim_game') }} g 
ON p.game_id = g.game_id
JOIN {{ ref('dim_team')}} t
ON p.team_id = t.team_id
GROUP BY p.player_id, t.team_id, g.season_start
