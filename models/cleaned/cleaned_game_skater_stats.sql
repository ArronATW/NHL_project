WITH src_game_skater_stats AS (
  SELECT
    *
  FROM
  {{ ref('src_game_skater_stats') }}
), labeled AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY game_id, player_id, team_id ORDER BY game_id) AS row_num
  FROM src_game_skater_stats
), deduplicated AS (
  SELECT 
    *
  FROM labeled
  WHERE row_num = 1
), cleaned as (
  SELECT 
    REPLACE(game_id, '"', '')::INT AS game_id,
    REPLACE(player_id, '"', '')::INT AS player_id,
    REPLACE(team_id, '"', '')::INT as team_id,
    time_on_ice,
    assists,
    goals,
    shots_on_goal,
    CASE
        WHEN hits = 'NA' THEN NULL
        ELSE hits::INT
    END AS hits,
    power_play_goals,
    power_play_assists,
    penalty_minutes,
    face_off_wins,
    face_off_taken,
    CASE
        WHEN takeaways = 'NA' THEN NULL
        ELSE takeaways::INT
    END AS takeaways,
    CASE
        WHEN giveaways = 'NA' THEN NULL
        ELSE giveaways::INT
    END AS giveaways,
    short_handed_goals,
    short_handed_assists,
    CASE
        WHEN blocked_shots = 'NA' THEN NULL
        ELSE blocked_shots::INT
    END AS blocked_shots,
    plus_minus_rating,
    even_time_on_ice,
    short_handed_time_on_ice,
    power_play_time_on_ice
  FROM deduplicated
)
SELECT 
  *
FROM cleaned
where time_on_ice between 0 and 3900 
    and power_play_goals <= goals
    and power_play_assists <= assists
    and time_on_ice + penalty_minutes * 60 <= 3900
    and face_off_taken <= 42  --historical high from NHL site
    and short_handed_goals <= goals 
    and short_handed_assists <= assists
    and even_time_on_ice <= time_on_ice
    and short_handed_time_on_ice <= time_on_ice
    and power_play_time_on_ice <= time_on_ice