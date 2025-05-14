WITH src_player_info AS (
  SELECT
    *
  FROM
  {{ ref('src_player_info') }}
), labeled AS (
  -- deduplication logic is to keep only earliest birth data for duplicate player_id
  SELECT
    *,  
    ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY birth_date ASC) AS row_num
  FROM src_player_info
), deduplicated AS (
  SELECT 
    *
  FROM labeled
  WHERE row_num = 1
)
SELECT
  player_id::INT as player_id,
  first_name,
  last_name,
  CASE
    WHEN nationality = 'NA' THEN NULL
    ELSE nationality
  END AS nationality,
  birth_city,
  primary_position,
  birth_date,
  CASE
    WHEN birth_state_province = 'NA' THEN NULL
    ELSE birth_state_province
  END AS birth_state_province,
  CASE
    WHEN split_part(height_inches, ' ', 1) != 'NA' THEN 
      REPLACE(split_part(height_inches, ' ', 1), '''', '')::INT
    ELSE NULL
  END AS height_feet,
  CASE
    WHEN split_part(height_inches, ' ', 2) != '' THEN 
      REPLACE(split_part(height_inches, ' ', 2), '"', '')::INT
    ELSE NULL
  END AS height_inches,
  CASE
    WHEN weight_pounds = 'NA' THEN NULL
    ELSE weight_pounds::INT
  END AS weight_pounds,
  CASE
    WHEN weight_pounds = 'NA' THEN NULL
    ELSE ROUND((weight_pounds::INT * 0.453592), 1)
  END AS weight_kilograms,
  CASE
    WHEN shoots_or_catches_side = 'NA' THEN NULL
    ELSE shoots_or_catches_side
  END AS shoots_or_catches_side
FROM deduplicated