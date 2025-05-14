WITH raw_game AS (
    SELECT * FROM {{ source('nhl', 'raw_game') }}
)
SELECT
    game_id,
    season,
    type as game_type,
    date_time_gmt as game_datetime_utc,
    away_team_id,
    home_team_id,
    away_goals as away_team_goals,
    home_goals as home_team_goals,
    outcome as game_outcome,
    home_rink_side_start,
    venue,
    venue_link as venue_api_link,
    venue_time_zone_id,
    venue_time_zone_offset,
    venue_time_zone_tz as venue_time_zone_label
  FROM
    raw_game