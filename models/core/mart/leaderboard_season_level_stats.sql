WITH agg_player_season_stats AS (
  SELECT * FROM {{ ref('agg_player_season_stats') }}
)
SELECT *
FROM agg_player_season_stats
WHERE (TOTAL_GOALS::FLOAT/GAMES_PLAYED) >= 0.25
    AND (TOTAL_ASSISTS::FLOAT/GAMES_PLAYED) >= 0.375
    AND (TOTAL_POINTS::FLOAT/GAMES_PLAYED) >= 0.625
    AND GAMES_PLAYED >= 41
-- https://www.hockey-reference.com/about/rate_stat_req.html
