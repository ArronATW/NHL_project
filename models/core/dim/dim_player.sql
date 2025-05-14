WITH cleaned_player_info AS (
  SELECT * FROM {{ ref('cleaned_player_info') }}
)
SELECT
  player_id,
  INITCAP(first_name) || ' ' || INITCAP(last_name) AS full_name,
  c.country AS country_of_origin,
  birth_city,
  s.state AS country_state,
  birth_date,
  CASE
    WHEN primary_position = 'C' THEN 'Center'
    WHEN primary_position = 'D' THEN 'Defenseman'
    WHEN primary_position = 'G' THEN 'Goalie'
    WHEN primary_position = 'LW' THEN 'Left Wing'
    WHEN primary_position = 'RW' THEN 'Right Wing'
    ELSE NULL
  END AS primary_position,
  height_feet,
  height_inches,
  weight_pounds,
  shoots_or_catches_side AS handedness
FROM cleaned_player_info p
LEFT JOIN {{ ref('country_mapping') }} c ON p.nationality = c.code
LEFT JOIN {{ ref('state_mapping') }} s ON p.birth_state_province = s.abbr