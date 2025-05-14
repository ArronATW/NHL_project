{% docs cleaned_game_skater_stats %}
### Cleaning

The following cleaning and validation steps were performed on the `src_game_skater_stats` source data:

1. **Deduplication**:  
   - For each unique combination of `game_id`, `player_id`, and `team_id`, only the first occurrence is retained using `ROW_NUMBER()` partitioned by these columns.

2. **Data Type Conversion**:  
   - `game_id`, `player_id`, and `team_id` are cleaned by removing quotation marks and casting to integers.

3. **Null Handling**:  
   - Columns with potential `'NA'` string values (`hits`, `takeaways`, `giveaways`, `blocked_shots`) are converted to `NULL` and cast to integers.

4. **Data Validity Checks**:  
   Rows are filtered to include only those that meet the following logical constraints:
   - `time_on_ice` is between 0 and 3900 seconds (maximum possible game time).
   - `power_play_goals` ≤ `goals`
   - `power_play_assists` ≤ `assists`
   - `time_on_ice` + (`penalty_minutes` * 60) ≤ 3900 (to ensure total time does not exceed game duration).
   - `face_off_taken` ≤ 42 (based on historical maximum from NHL data).
   - `short_handed_goals` ≤ `goals`
   - `short_handed_assists` ≤ `assists`
   - `even_time_on_ice`, `short_handed_time_on_ice`, and `power_play_time_on_ice` must each be ≤ `time_on_ice`

These steps ensure that only valid, well-formed records are passed downstream for analysis.


{% enddocs %}
<!--           CLEANED GAME BLOCK           -->






<!--           CLEANED GAME BLOCK           -->
{% docs cleaned_game %}
### Cleaning

The following cleaning and validation steps were performed on the `src_game` source data:

1. **Deduplication**:  
   - In cases where multiple rows share the same `game_id`, only the **latest record** (based on `game_datetime_utc`) is retained.
   - This is done using `ROW_NUMBER()` partitioned by `game_id` and ordered in descending order of `game_datetime_utc`.

2. **Data Type Casting and Season Handling**:
   - `game_id` is cast to an integer.
   - The `season` string (formatted like `"20192020"`) is split into two integers:
     - `season_start`: the first 4 digits (e.g., `2019`)
     - `season_end`: the last 4 digits (e.g., `2020`)
   - It is confirmed that each `season` spans only **one year**, which was validated in the data.

3. **Game Outcome Parsing**:
   - `game_outcome` is a string (e.g., `"away win OT"`) and is split to extract:
     - `winning_team`: the first word, unless it is `'tbc'` (in which case it's set to `NULL` as data was updated 4 years ago hence can safely assumed that `'tbc'` will no longer be updated anymore)
     - `win_type`: the third word, unless it is `'tbc'` (then set to `NULL` for the reasons above)

4. **Null and Format Normalization**:
   - `home_rink_side_start`:
     - Values equal to `'NA'` are replaced with `NULL`
     - All non-null values are converted to uppercase
   - `venue_api_link`:  
     - If the link is `'/api/v1/venues/null'`, it is replaced with an empty string `''`

5. **Final Column Selection**:
   - Only relevant and cleaned columns are selected and returned for downstream use, such as:
     - Game metadata (`game_id`, `season_start`, `game_type`, etc.)
     - Scores, teams, venue info, and outcome results

These steps ensure the game-level dataset is deduplicated, well-structured, and normalized for reliable analytical use.



{% enddocs %}

<!--           CLEANED PLAYER INFO DOC BLOCK           -->






<!--           CLEANED PLAYER INFO DOC BLOCK           -->
{% docs cleaned_player_info %}

### Cleaning Logic

This model processes the `src_player_info` source table by applying the following cleaning and transformation logic:

1. **Deduplication**:
   - For each `player_id`, only the most recent record (based on `birth_date`) is retained using `ROW_NUMBER()`.

2. **ID and Type Casting**:
   - `player_id` is cast to an integer.

3. **Name Normalization**:
   - **`first_name`**:
     - If it contains only alphabetic characters (`^[[:alpha:]]+$`), it is kept as-is.
     - If it's 4 characters or fewer and contains non-alphabetic characters (e.g., hyphen), it replaces hyphens with periods.
   - **`last_name`**:
     - Trimmed and extra spaces reduced to a single space.
     - If it contains multiple words (e.g., middle names or compound names), it is title-cased.

4. **Nationality**:
   - Values equal to `'NA'` are converted to `NULL`.
   - Other values are cast to a 3-character format.

5. **Birthplace Fields**:
   - **`birth_city`**:
     - Trimmed, extra spaces normalized, and title-cased.
   - **`birth_state_province`**:
     - Converted to `NULL` if equal to `'NA'`.

6. **Physical Attributes**:
   - **Height**:
     - `height_feet` and `height_inches` are parsed separately from their respective columns.
     - `'NA'` values are converted to `NULL`.
   - **Weight**:
     - If `weight_pounds` is `'NA'`, it is set to `NULL`.
     - Otherwise, it is cast to `INT` and also converted to kilograms (rounded to 1 decimal place).

7. **Player Orientation**:
   - `shoots_or_catches_side` is set to `NULL` if it is `'NA'`.

8. **Final Column Selection**:
   - The cleaned and formatted fields are selected for downstream use, ensuring consistency and eliminating placeholder or malformed values.


{% enddocs %}
<!--           CLEANED TEAM INFO DOC BLOCK           -->








<!--           CLEANED TEAM INFO DOC BLOCK           -->

{% docs cleaned_team_info %}

### Cleaning

This model performs light transformation and cleaning of team information from the `src_team_info` source.

#### Cleaning Steps Applied:

- **Type Casting**  
  - `team_id` and `franchise_id` are cast to integers to standardize data types for consistency and compatibility with downstream models.

- **Column Selection**  
  - Only the following relevant columns are selected:
    - `team_location`: Name of the team's city or region
    - `team_nickname`: Team's nickname
    - `team_abbreviation`: Official team abbreviation
    - `team_api_link`: Reference to the team's endpoint in the NHL API

- **Ordering**  
  - Output is sorted by `team_id` to ensure consistent row ordering.

#### Not Needed:

- **Deduplication**  
  - Not needed, as all `team_id` values are unique in the source.

- **Null/Invalid Value Handling**  
  - Not performed, since the selected fields are assumed to be clean and well-formed.

{% enddocs %}