{% docs fct_player_game_stats %}

### Fact Table: Skater Game Statistics

This fact model contains detailed, game-level performance statistics for individual NHL skaters. It is built from the cleaned source model `cleaned_game_skater_stats` and includes only rows with valid `team_id`s that exist in the `dim_team` dimension table as some `team_id` recorded no longer exists in the team_info table. 

---

### Relationships to Dimension Tables

This fact table forms the central point of analysis and connects to the following dimension tables:

- `dim_player`: via `player_id`
- `dim_game`: via `game_id`
- `dim_team`: via `team_id`

The surrogate key `skater_game_fact_id` is generated using a combination of these three identifiers to ensure uniqueness per skater-game-team entry.

---

### Transformation Logic

Derived columns are calculated to enrich raw game statistics with per-minute rates and efficiency metrics for better analytical insight:

#### Offensive Metrics
- **`scoring_efficiency_percentage`**:  
  Measures the percentage of goals scored per shot on goal.  
  `= (goals / shots_on_goal) * 100` (fallbacks used to avoid divide-by-zero).

- **`goals_per_minute`**:  
  Number of goals scored per minute of time on ice.
  `= goals / (time_on_ice)`

- **`assists_per_minute`**:  
  Number of assists made per minute of time on ice.  
  `= assists / (time_on_ice)`

#### Face-Off Control
- **`face_off_win_percentage`**:  
  Percentage of face-offs won, indicating puck control.  
  `= (face_off_wins / face_off_taken) * 100`

#### Defensive Metrics
- **`hits_per_minute`**:  
  Number of hits delivered per minute on ice.  
  `= hits / (time_on_ice)`

#### Special Teams Performance
- **`power_play_points_per_minute`**:  
  Combined goals and assists while on power play, per minute.  
  `= (power_play_goals + power_play_assists) / (power_play_time_on_ice)`

- **`short_handed_points_per_minute`**:  
  Combined goals and assists while short-handed, per minute.  
  `= (short_handed_goals + short_handed_assists) / (short_handed_time_on_ice)`

All per-minute and percentage metrics include safeguards (e.g., replacing 0 with 1 in the denominator) to avoid division errors.

---

### Data Quality Filters

Before transformation, the input data is filtered to ensure:
- Only valid team entries are retained (`team_id` must exist in `dim_team`).
- Only cleaned and validated rows from `cleaned_game_skater_stats` are used, which already includes deduplication, type casting, and logical constraint checks.

This curated fact model supports performance-based insights for player analysis, team comparisons, and advanced gameplay metrics.

{% enddocs %}
<!--           DIM GAME BLOCK           -->






<!--           DIM GAME BLOCK           -->

{% docs dim_game %}


### Dimension Table: Game Details

The `dim_game` dimension model provides contextual and descriptive information about each NHL game. It is derived from the `cleaned_game` model and includes both raw attributes and enriched temporal metadata for use in time-based and matchup analyses.

---

### Relationships to Fact Tables

This dimension table is linked to fact models via the `game_id` field. Primary relationships include:

- `fact_skater_game_stats`: Each row in the fact table references a `game_id` from this dimension.
- Other possible fact tables such as `fact_goalie_game_stats` or `fact_team_game_stats` may also join on `game_id`.

This enables analysts to drill down into game-specific details when analyzing player or team performance.

---

### Transformation Logic

#### Game Type Mapping
- **`game_type`**:  
  Converts the raw game type codes into readable labels:  
  `'R' → Regular Season`, `'P' → PlayOffs`, `'A' → All-Star`.

#### Temporal Breakdown
- **`game_year`, `game_month`, `game_day`**:  
  Extracted from the `game_datetime_utc` field to support time-series filtering and aggregation.

- **`day_of_week`**:  
  Uses `EXTRACT(dayofweek)` and `DECODE` to map weekday numbers (0–6) to day names (e.g., Sunday, Monday). This supports weekly trend analysis.

#### Win Type Description
- **`win_type`**:  
  Converts win types from short codes to readable formats:  
  `'REG' → Regular Time`, `'OT' → Overtime`.

---

### Additional Contextual Columns

- **`season_start`, `season_end`**:  
  Indicates the season in which the game was played.

- **`home_team_id`, `away_team_id`**:  
  Useful for joining with `dim_team` or supporting game-level team matchups.

- **`home_team_goals`, `away_team_goals`, `winning_team`**:  
  Supports outcomes and performance comparisons.

- **`home_rink_side_start`**:  
  Describes the side the home team starts on — relevant for strategy analysis.

- **`venue`, `venue_time_zone_id`, `venue_time_zone_offset`, `venue_time_zone_label`**:  
  Venue-level detail, supports geographic and time-zone based insights (e.g., travel fatigue analysis or time-based performance).

---

This `dim_game` table enriches analytical capabilities by providing date and event context around each NHL game, supporting slicing and dicing across both time and team dimensions.


{% enddocs %}
<!--           DIM PLAYER BLOCK           -->






<!--           DIM PLAYER BLOCK           -->
{% docs dim_player %}

### Dimension Table: Player Information

The `dim_player` model serves as the central dimension table for player metadata. It is derived from the `cleaned_player_info` staging model and enriched with additional geographic and descriptive mappings to support more readable and insightful reporting.

---

### Relationships to Fact Tables

This dimension is connected to fact tables through the `player_id` field. It is primarily referenced by:

- `fact_skater_game_stats`: Links each player's game performance to their identity and demographics.
- Any other fact tables related to player performance (e.g., `fact_goalie_game_stats`) will also use this dimension via `player_id`.

This allows aggregation and filtering of player statistics by position, geography, age, handedness, etc.

---

### Transformation Logic

#### Name Formatting
- **`full_name`**:  
  Combines `first_name` (with capitalization using `INITCAP`) and `last_name` into a single full name field for display in reports.

#### Position Mapping
- **`primary_position`**:  
  Converts position codes to full names:  
  `'C' → Center`, `'D' → Defenseman`, `'G' → Goalie`, `'LW' → Left Wing`, `'RW' → Right Wing`.  
  This provides clarity for non-technical users or when building visualizations.

#### Geographic Mapping
- **`country_of_origin`**:  
  Mapped using `country_mapping` table to convert nationality codes (e.g., "CAN", "USA") into full country names.

- **`country_state`**:  
  Uses `state_mapping` table to enrich the state/province code into a human-readable name, primarily for North American players.

#### Other Attributes
- **`birth_city`, `birth_date`**:  
  Useful for age calculations and demographic segmentation.

- **`height_feet`, `height_inches`, `weight_pounds`**:  
  Physical attributes that can be used for scouting profiles, clustering, or performance modeling.

- **`handedness`**:  
  Taken from `shoots_or_catches_side`, it represents the side the player uses for shooting (skaters) or catching (goalies). Critical for analyzing in-game dynamics and matchup strategies.

---

This `dim_player` table enables deep player-level analysis by joining onto player performance fact tables and enriching raw data with clean, interpretable metadata.

{% enddocs %}
<!--           DIM TEAM BLOCK           -->






<!--           DIM TEAM BLOCK           -->
{% docs dim_team %}

### dim_team

The `dim_team` dimension table provides enriched and standardized information about NHL teams. It acts as a lookup for team metadata and supports various fact tables such as `fact_skater_game_stats` and `dim_game` via the `team_id` foreign key.

#### Relationship to Fact Table
- `dim_team.team_id` is used as a foreign key in:
  - `fact_skater_game_stats.team_id`: links each player's in-game performance to their team.
  - `dim_game.home_team_id` and `dim_game.away_team_id`: identifies which teams played in each game.

#### Transformation Logic
- `team_name`: Concatenates `team_location` and `team_nickname` to produce a human-readable full team name (e.g., "Toronto Maple Leafs").
- Other fields like `team_id`, `franchise_id`, and `team_abbreviation` are selected as-is from the cleaned source for consistency and reference integrity.

{% enddocs %}