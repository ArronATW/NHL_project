WITH cleaned_game AS (
  SELECT * FROM {{ ref('cleaned_game') }}
)
SELECT
  game_id,
  season_start,
  season_end,
  CASE
    WHEN game_type = 'R' THEN 'Regular Season'
    WHEN game_type = 'P' THEN 'PlayOffs'
    WHEN game_type = 'A' THEN 'All-Star'
    ELSE NULL
  END AS game_type,
  EXTRACT(year from game_datetime_utc) as game_year,
  EXTRACT(month from game_datetime_utc) as game_month,
  EXTRACT(day from game_datetime_utc) as game_day,
  DECODE(EXTRACT(dayofweek FROM game_datetime_utc),
    0, 'Sunday',
    1, 'Monday',
    2, 'Tuesday',
    3, 'Wednesday',
    4, 'Thursday',
    5, 'Friday',
    6, 'Saturday') AS day_of_week,
  away_team_id,
  home_team_id,
  away_team_goals,
  home_team_goals,
  winning_team,
  CASE
    WHEN win_type = 'REG' THEN 'Regular Time'
    WHEN win_type = 'OT' THEN 'OverTime'
    ELSE NULL
  END AS win_type,
  home_rink_side_start,
  venue,
  venue_time_zone_id,
  venue_time_zone_offset,
  venue_time_zone_label
FROM cleaned_game