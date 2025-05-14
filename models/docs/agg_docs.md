{% docs agg_player_season_stats %}

### agg_player_season_stats

The `agg_player_season_stats` model aggregates individual player performance statistics at the **season level**. This table provides a high-level summary of a player's contributions across all games in a given season.

#### Aggregation Logic

- Data is sourced from the `fct_player_game_stats` fact table and joined with `dim_game` to extract seasonal information.
- Grouping is performed by `player_id` and `season_start` to compute seasonal aggregates.
- Season end is derived as `season_start + 1` for readability.

#### Transformation Logic for Derived Columns

- **games_played**: Count of unique `game_id` values per player and season.
- **total_goals, total_assists, total_points**: Summed over all games.
- **total_shots**: Total number of shots on goal.
- **avg_scoring_efficiency_pct**: Average shooting efficiency (goals ÷ shots_on_goal), averaged over all games and rounded to 2 decimal places.
- **total_faceoff_wins, total_faceoffs**: Summed face-off stats.
- **avg_face_off_win_percentage**: Average face-off win rate across games.

- **total_minutes**: Total ice time converted from seconds to minutes and rounded.
- **hits_per_60minute**, **blocked_shots_per_60minute**, **goals_per_60minute**, **assists_per_60minute**:
  - Normalized per-60-minute rates calculated using total counts and total ice time.
  - Handled divide-by-zero cases with fallback logic.

- **total_takeaways**: Sum of takeaways (fallbacks to 0 if null).

- **total_pp_points**, **total_pp_minutes**, **avg_pp_points_per_60minute**:
  - Power-play contributions and normalized scoring rate based on power play ice time.

- **total_sh_points**, **total_sh_minutes**, **avg_sh_points_per_60minute**:
  - Short-handed contributions and normalized scoring rate based on short-handed ice time.

This table supports high-level analysis, season-over-season comparisons, and efficient dashboard reporting for player trends.


{% enddocs %}
<!--           AGG PLAYER CAREER STATS BLOCK           -->






<!--           AGG PLAYER CAREER STATS BLOCK           -->
{% docs agg_player_career_stats %}

### Model: `agg_player_career_stats`

This model aggregates **season-level player statistics** from the `agg_player_season_stats` model to compute **career-level performance metrics** for each NHL player.

#### **Data Source**
- The model reads from the intermediate aggregated model `agg_player_season_stats`, which provides stats for each player per season.

#### **Aggregation Logic**
Each row in the final output corresponds to a single `player_id`, representing their entire NHL career (across all available seasons). The following aggregation logic is applied:

- `COUNT(DISTINCT season_start)`: Calculates the total number of distinct seasons played (`total_seasons`).
- `SUM(...)`: Used to aggregate raw count-based statistics over a player's career:
  - `games_played`, `total_goals`, `total_assists`, `total_points`, `total_shots`, `total_faceoff_wins`, `total_faceoffs`, `total_minutes`, `total_takeaways`, `total_pp_points`, `total_pp_minutes`.
- `ROUND(AVG(...), 2)`: Averages per-season derived metrics and rounds them to two decimal places:
  - `avg_scoring_efficiency_pct`, `avg_face_off_win_percentage`, `hits_per_60minute`, `blocked_shots_per_60minute`, `goals_per_60minute`, `assists_per_60minute`, `avg_pp_points_per_60minute`, `avg_sh_points_per_60minute`.

> ℹ️ This averaging approach helps smooth out outliers and provides a normalized view of player performance over multiple seasons.

#### **Transformation / Derived Metrics**
The model contains derived columns that are **not directly present in the source** but are calculated as follows:

- **Per 60-minute metrics** (`hits_per_60minute`, `goals_per_60minute`, etc.): Season-level per-60 stats are averaged across all seasons played.
- **Efficiency percentages** (`avg_scoring_efficiency_pct`, `avg_face_off_win_percentage`, etc.): Computed as the average of season-level percentages.
- `avg_pp_points_per_60minute` and `avg_sh_points_per_60minute`: Calculated from the per-season power play and short-handed contributions normalized per 60 minutes.

#### **Use Case**
This model is suitable for:
- Player career summary dashboards
- Career comparison across NHL players
- Feeding into downstream models or ML pipelines for player performance prediction or clustering



{% enddocs %}