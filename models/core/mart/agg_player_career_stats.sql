WITH agg_player_season_stats AS (
  SELECT * FROM {{ ref('agg_player_season_stats') }}
)
SELECT 
  player_id,
  COUNT(DISTINCT season_start) AS total_seasons,
  SUM(games_played) AS total_games,
  SUM(total_goals) AS total_goals,
  SUM(total_assists) AS total_assists,
  SUM(total_points) AS total_points,
  SUM(total_shots) AS total_shots,
  ROUND(AVG(avg_scoring_efficiency_pct), 2) AS avg_scoring_efficiency_pct,
  SUM(total_faceoff_wins) AS total_faceoff_wins,
  SUM(total_faceoffs) AS total_faceoffs,
  ROUND(AVG(avg_face_off_win_percentage), 2) AS avg_face_off_win_percentage,
  SUM(total_minutes) AS total_minutes,
  ROUND(AVG(hits_per_60minute), 2) AS hits_per_60minute,
  ROUND(AVG(blocked_shots_per_60minute), 2) AS blocked_shots_per_60minute,
  ROUND(AVG(goals_per_60minute), 2) AS goals_per_60minute,
  ROUND(AVG(assists_per_60minute), 2) AS assists_per_60minute,
  SUM(total_takeaways) AS total_takeaways,
  SUM(total_pp_points) AS total_pp_points,
  SUM(total_pp_minutes) AS total_pp_minutes,
  ROUND(AVG(avg_pp_points_per_60minute), 2) AS avg_pp_points_per_60minute,
  ROUND(AVG(avg_sh_points_per_60minute), 2) AS avg_sh_points_per_60minute
FROM agg_player_season_stats
GROUP BY player_id
