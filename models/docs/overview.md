{% docs __overview__ %}
# NHL Data Warehouse Project Overview

Welcome to the **NHL Data Warehouse** dbt project!

This project transforms raw NHL datasets into clean, well-structured, and analytics-ready tables using dbt (data build tool). It is built on top of Snowflake and is designed to support data analysis and dashboarding for hockey performance metrics.

---

## 🎯 Project Goals

- Ingest and standardize raw NHL datasets.
- Create cleaned, enriched models for downstream analytics.
- Provide aggregated stats for players, teams, and games.
- Enable data quality checks and testing using dbt features.
- Generate and host documentation for easier exploration and collaboration.

---

## 📦 Data Sources

This project uses the following raw datasets (via seeds or Snowflake external stage):

- `game.csv` – Game-level metadata and schedules.
- `player_info.csv` – Player personal and demographic information.
- `game_skater_stats.csv` – Skater-level performance stats per game.
- `team_info.csv` – Team-level metadata.
- External mappings:
  - `country_mapping` – Mapping country codes to full names.
  - `state_mapping` – Mapping US state abbreviations to full names.

---

## 🏗️ Key Models

### **Staging Models**
These models clean and standardize raw source tables.

- `stg_player_info`
- `stg_team_info`
- `stg_game_skater_stats`
- `stg_game`

### **Core Models**
These models include business logic and calculated metrics.

- `fct_player_game_stats` – Game-level player statistics.
- `dim_players` – Cleaned and enriched player dimension.
- `dim_teams` – Cleaned team dimension.
- `dim_games` – Game dimension with enriched fields.

### **Aggregates**
Higher-level aggregated models for quick insights:

- `agg_player_season_stats` – Player stats by season.
- `agg_player_career_stats` – Player cumulative career stats.

---

## ✅ Testing & Documentation

- dbt tests ensure data quality (e.g., not null, uniqueness).
- Documentation includes descriptions for all models and columns.
- Use `dbt docs generate` and `dbt docs serve` to explore the lineage and metadata.

---

## 🔗 Usage

### Running Locally
```bash
dbt seed
dbt run
dbt test
dbt docs generate
dbt docs serve


{% enddocs %}