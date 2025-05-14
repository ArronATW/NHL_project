WITH raw_player_info AS (
    SELECT * FROM {{  source('nhl', 'raw_player_info') }}
)
SELECT
    player_id,
    first_name,
    last_name,
    nationality,
    birth_city,
    primary_position,
    birth_date,
    birth_state_province,
    height AS height_inches,
    height_cm,
    weight AS weight_pounds,
    shoots_catches AS shoots_or_catches_side
FROM
    raw_player_info