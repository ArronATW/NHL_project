# 🏒 NHL Data Engineering Pipeline & Dashboard

This project showcases a complete data engineering pipeline for NHL game data. It integrates data ingestion, transformation, and visualization using modern tools such as AWS S3, Snowflake, dbt, and Streamlit.

## 🚀 Project Overview

The pipeline processes raw NHL game data from Kaggle, stores it in a data lake (AWS S3), transforms it in a Snowflake data warehouse using dbt, and presents the final analytics in a cloud-deployed Streamlit dashboard.

---
## 🗂️ Data Source

The data used in this project is sourced from Kaggle:

[NHL Game Data on Kaggle](https://www.kaggle.com/datasets/martinellis/nhl-game-data/data) which includes detailed player stats, game outcomes, and team performance from 2000 to 2020.

[NHL Player API](https://api-web.nhle.com/v1/player/{player_id}/landing) was also used to get pictures for dashboard

---

## 📊 NHL Players Dashboard
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nhlproject-bb5zrbxkdsohil5tabdbqf.streamlit.app/)

The dashboard allows users to:
- Explore player statistics by season, team, and position
- View leaderboards for offensive and defensive performance
- Top Offensive and Defensive players during Power Plays or Penalty Kills
- How points varies by positions
---


## Architecture
![architecture diagram](https://github.com/ArronATW/NHL_project/blob/main/NHL_architecture.png)

1. **Data Collection**: CSVs from [Kaggle](https://www.kaggle.com/datasets/martinellis/nhl-game-data/data)
2. **Data Lake**: Raw files stored in an AWS S3 bucket
3. **Data Warehouse**:
   - Loaded into Snowflake staging schema
   - Transformed using dbt (cleaning, transforming, testing)
     
### Modeling
![modeling_diagram](https://github.com/ArronATW/NHL_project/blob/main/NHL_data_modeling.png)
4. **Transformation Logic**:
   - Cleaning and normalization
   - Deriving new metrics (e.g., points per 60 minutes)
   - Joins between player and game stats

📄 **Detailed transformation logic is documented in dbt**:  
🔗 [View dbt Documentation](https://dbt-documentation-nhl-project.s3.ap-southeast-2.amazonaws.com/index.html#!/model/model.nhl_project.leaderboard_season_level_stats)

5. **Data Presentation**:
   - Streamlit app pulls from transformed Snowflake tables
   - Deployed online for interactive user access
