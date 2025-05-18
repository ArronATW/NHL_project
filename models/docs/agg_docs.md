{% docs agg_player_season_stats %}

### agg_player_season_stats

The `agg_player_season_stats` model aggregates individual player performance statistics at the **season level**. This table provides a high-level summary of a player's contributions across all games in a given season.

#### Aggregation Logic

- Data is sourced from the `fct_player_game_stats` fact table and joined with `dim_game` to extract seasonal information.
- Grouping is performed by `player_id` and `season_start` to compute seasonal aggregates.

#### Transformation Logic for Derived Columns

- **games_played**: Count of unique `game_id` values per player and season.
- **total_goals, total_assists, total_points**: Summed over all games.
- **total_shots**: Total number of shots on goal.
- **total_toi_min**: Total ice time converted from seconds to minutes and rounded.
- **total_faceoff_wins, total_faceoffs, total_hits, total_blocked**: Summed over all games.
- **total_takeaways**: Sum of takeaways (fallbacks to 0 if null).
- **total_giveaways**: Sum of giveaways (fallbacks to 0 if null).
- **Per 60-Minute Rates** (normalized for playing time):
    - `hits_per_60minute`, `blocked_shots_per_60minute`
    - `goals_per_60minute`, `assists_per_60minute`
    - `takeaways_per_60mins`, `giveaways_per_60mins`
    - `total_pp_points_per_60minute`, `total_sh_points_per_60minute`
 - **Special Teams**:
     - Power Play: `total_pp_points` and `total_pp_minutes` are summed.
     - Short-Handed: `total_sh_points` and `total_sh_minutes` are summed.

This table supports high-level analysis, season-over-season comparisons, and efficient dashboard reporting for player trends.


{% enddocs %}
<!--           LEADERBOARD SEASON LEVEL STATS BLOCK           -->






<!--           LEADERBOARD SEASON LEVEL STATS BLOCK           -->
{% docs leaderboard_season_level_stats %}

### Model: `leaderboard_season_level_stats`

This model filters season-level player statistics to identify **offensive qualifiers** — players who have played a sufficient number of games and meet minimum per-game performance thresholds in goals, assists, and total points.

#### **Data Source**
- `agg_player_season_stats`: A season-level aggregation of player statistics, containing fields such as `total_goals`, `total_assists`, `total_points`, and `games_played`.

## Transformation Logic

The logic filters the source data using the following **criteria**:

- `games_played >= 41`: Ensures the player participated in at least half of an 82-game NHL season.
- `total_goals / games_played >= 0.25`: At least 0.25 goals per game (~20+ goals in a full season).
- `total_assists / games_played >= 0.375`: At least 0.375 assists per game (~30+ assists in a full season).
- `total_points / games_played >= 0.625`: At least 0.625 points per game (~50+ points in a full season).

All ratio-based conditions cast the numerator and denominator to `FLOAT` to prevent integer division issues.

---

## Use Case

- To **identify consistently performing offensive players** across a season.
- Used as a filter layer for dashboards, leaderboards, or awards modeling.

---


{% enddocs %}