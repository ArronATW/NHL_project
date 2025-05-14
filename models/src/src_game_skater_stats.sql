WITH raw_game_skater_stats AS (
    SELECT * FROM {{ source('nhl', 'raw_game_skater_stats') }}
)
SELECT
    game_id,
    player_id,
    team_id,
    time_on_ice,
    assists,
    goals,
    shots as shots_on_goal,
    hits,
    power_play_goals,
    power_play_assists,
    penalty_minutes,
    face_off_wins,
    face_off_taken,
    takeaways,
    giveaways,
    short_handed_goals,
    short_handed_assists,
    blocked as blocked_shots,
    plusminus as plus_minus_rating,
    even_time_on_ice,
    short_handed_time_on_ice,
    power_play_time_on_ice
FROM
    raw_game_skater_stats