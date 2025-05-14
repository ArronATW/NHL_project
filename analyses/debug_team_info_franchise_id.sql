SELECT franchise_id, COUNT(*)
FROM {{ ref('cleaned_team_info') }}
GROUP BY franchise_id
HAVING COUNT(*) > 1;