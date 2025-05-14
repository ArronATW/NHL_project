WITH src_player_info AS (
  SELECT
    *
  FROM
  {{ ref('src_player_info') }}
), ranked AS (
  -- deduplication logic is to keep only latest game data for duplicate game_id
  SELECT
    *,  
    ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY birth_date DESC) AS row_num
  FROM src_player_info
), deduplicated AS (
  SELECT 
    *
  FROM ranked
  WHERE row_num = 1
)
SELECT
  player_id::INT as player_id,
  CASE
    WHEN NOT REGEXP_LIKE(first_name, '^[[:alpha:]]+$') THEN
      CASE
        WHEN LENGTH(first_name) <= 4 THEN REPLACE(first_name, '-', '.')
        ELSE first_name
      END 
    ELSE first_name
  END AS first_name,
  CASE
    WHEN REGEXP_LIKE(TRIM(last_name), '.+\\s.+') THEN
      INITCAP(REGEXP_REPLACE(TRIM(last_name), '\\s+', ' '))
    ELSE INITCAP(last_name)
  END AS last_name,
  CASE
    WHEN nationality = 'NA' THEN NULL
    ELSE nationality::CHAR(3)
  END AS nationality,
  CASE
    WHEN REGEXP_LIKE(TRIM(birth_city), '.+\\s.+') THEN
      INITCAP(REGEXP_REPLACE(TRIM(birth_city), '\\s+', ' '))
    ELSE INITCAP(birth_city)
  END AS birth_city,
  primary_position::CHAR(2) AS primary_position,
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
    ELSE (weight_pounds::INT * 0.453592)::NUMERIC(38, 1)
  END AS weight_kilograms,
  CASE
    WHEN shoots_or_catches_side = 'NA' THEN NULL
    ELSE shoots_or_catches_side
  END AS shoots_or_catches_side
FROM deduplicated