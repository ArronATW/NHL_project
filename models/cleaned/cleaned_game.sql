WITH src_game AS (
  SELECT
    *
  FROM
  {{ ref('src_game') }}
), labeled AS (
  -- deduplication logic is to keep only latest game data for duplicate game_id
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY game_id ORDER BY game_datetime_utc DESC) AS row_num
  FROM src_game
), deduplicated AS (
  SELECT 
    *
  FROM labeled
  WHERE row_num = 1
)
SELECT
    game_id::INT AS game_id,
    LEFT(season, 4)::INT AS season_start, -- ALL SEASON ONLY LAST 1 YEAR, CHECKED
    RIGHT(season, 4)::INT AS season_end,
    game_type,
    game_datetime_utc,
    away_team_id,
    home_team_id,
    away_team_goals,
    home_team_goals,
    CASE
        WHEN SPLIT_PART(game_outcome, ' ', 1) = 'tbc' THEN NULL
        ELSE SPLIT_PART(game_outcome, ' ', 1)
    END AS winning_team,
    CASE
        WHEN SPLIT_PART(game_outcome, ' ', 3) = 'tbc' THEN NULL
        ELSE SPLIT_PART(game_outcome, ' ', 3)
    END AS win_type,
    CASE
        WHEN home_rink_side_start = 'NA' THEN NULL
        ELSE UPPER(home_rink_side_start)
    END as home_rink_side_start,
    venue,
    CASE 
        WHEN venue_api_link = '/api/v1/venues/null' THEN ''
        ELSE venue_api_link
    END AS venue_api_link,
    venue_time_zone_id,
    venue_time_zone_offset,
    venue_time_zone_label
FROM deduplicated