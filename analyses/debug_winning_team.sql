SELECT DISTINCT winning_team
FROM {{ ref('cleaned_game') }}
WHERE winning_team NOT IN ('home', 'away') OR winning_team IS NULL = FALSE