# Import Python packages
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go

from snowflake.snowpark import Session
#######################
# Page configuration
st.set_page_config(
  page_title="NHL Player Performance Dashboard",
  page_icon = "🏒",
  layout="wide",
  initial_sidebar_state="expanded")

#######################
def start_session():
  connection_parameters = {
    "account": st.secrets["snowflake"]["account"],
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "role": st.secrets["snowflake"]["role"],
    "warehouse": st.secrets["snowflake"]["warehouse"],
    "database": st.secrets["snowflake"]["database"],
    "schema": st.secrets["snowflake"]["schema"]
  }
  session = Session.builder.configs(connection_parameters).create()
  return session

def season_slider():
  season_query = f"""
    SELECT MIN(SEASON_START) AS MIN_DATE, MAX(SEASON_START) AS MAX_DATE
    FROM NHL_DB.DEV_SCH_CORE.AGG_PLAYER_SEASON_STATS
  """
  season_list = session.sql(season_query).collect()
  min_year, max_year = season_list[0]["MIN_DATE"], season_list[0]["MAX_DATE"]
  year_range = st.slider("Season range", min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)
  return year_range[0], year_range[1]

def get_teams():
  teams_query = f"""
    SELECT DISTINCT TEAM_NAME
    FROM NHL_DB.DEV_SCH_CORE.DIM_TEAM
  """
  team_options = session.sql(teams_query).collect()
  teams = st.multiselect("Select Teams", team_options, default=team_options)
  return teams

def get_positions():
  position_query = f"""
    SELECT DISTINCT PRIMARY_POSITION
    FROM NHL_DB.DEV_SCH_CORE.DIM_PLAYER
  """
  position_options = session.sql(position_query).collect()
  positions = st.multiselect("Select positions", position_options, default=position_options)
  return positions

def get_leaderboard_filtered_df(season_start, season_end, positions, teams):
  positions_str = "', '".join(positions)
  teams_str = "', '".join(teams)

  player_query = f"""
    SELECT
      agg.PLAYER_ID,
      agg.TEAM_ID,
      agg.SEASON_START,
      GAMES_PLAYED,
      TOTAL_TOI_MIN AS TOTAL_MINUTES,
      TOTAL_TAKEAWAYS,
      TOTAL_GIVEAWAYS,
      TOTAL_BLOCKED,
      TOTAL_HITS,
      TAKEAWAYS_PER_60MINS,
      GIVEAWAYS_PER_60MINS,
      BLOCKED_SHOTS_PER_60MINUTE,
      HITS_PER_60MINUTE,
      FULL_NAME,
      PRIMARY_POSITION,
      TEAM_NAME,
      TOTAL_GOALS,
      TOTAL_ASSISTS,
      TOTAL_POINTS,
      GOALS_PER_60MINUTE,
      ASSISTS_PER_60MINUTE,
      GOALS_PER_60MINUTE + ASSISTS_PER_60MINUTE AS TOTAL_POINTS_PER_60MINUTE
    FROM NHL_DB.DEV_SCH_CORE.LEADERBOARD_SEASON_LEVEL_STATS agg
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_PLAYER p
    ON agg.PLAYER_ID = p.PLAYER_ID
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_TEAM t
    ON agg.TEAM_ID = t.TEAM_ID
    WHERE SEASON_START BETWEEN {season_start} AND {season_end} 
        AND p.PRIMARY_POSITION IN ('{positions_str}')
        AND TEAM_NAME IN ('{teams_str}')
    """
  player = session.sql(player_query).collect()
  player_df = pd.DataFrame(player)
  return player_df

def get_player_pics(player_df):
  pics_query = f"""
    SELECT * FROM NHL_DB.STAGE_SCH.PLAYER_PICS
    WHERE PLAYER_ID = {player_df.loc[0, 'PLAYER_ID']}
  """
  player_pics = session.sql(pics_query).collect()
  player_pics_df = pd.DataFrame(player_pics)
  return [player_pics_df.loc[0, 'HEADSHOT'], player_pics_df.loc[0, 'HEROIMAGE']]

def get_team_logo(team_id):
  logo_query = f"""
    SELECT TEAM_PIC_URL
    FROM NHL_DB.DEV_SCH_CORE.DIM_TEAM
    WHERE TEAM_ID = {team_id}
  """
  team_logo = session.sql(logo_query).collect()
  logo_df = pd.DataFrame(team_logo)
  return logo_df.loc[0, 'TEAM_PIC_URL']

def player_name_headshot_markdown(player_name, headshot):
  st.markdown(f"<h3 style='text-align: center;'>{player_name}</h3>", unsafe_allow_html=True)
  st.markdown(
    f"""
    <img src="{headshot}" 
        style="
            width:auto; 
            max-width:100%; 
            height:auto; 
            max-height:150px;
            border-radius: 0.5rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            display: block;
            margin: 0 auto;
        ">
    """,
        unsafe_allow_html=True
  )

def position_box_header(position):
  st.metric(
      label="Position",
      value=position
    )

def season_level_player_team_and_icon(player_team, logo_png):
  inner_col1, inner_col2 = st.columns([3,2])
  with inner_col1:
    st.metric(
      label="Team",
      value=player_team
    )
  with inner_col2:
    st.image(f"{logo_png}", width=150)

def show_offensive_player_stats(games_played, toi, goals, assists, points, pp_60mins):
  st.markdown('---')
  cols = st.columns(6)  # Adjust based on how many stats you want to show
  cols[0].markdown(f"**Games Played**\n\n{games_played}")
  cols[1].markdown(f"**TOI (min)**\n\n{toi}")
  cols[2].markdown(f"**Goals**\n\n{goals}")
  cols[3].markdown(f"**Assists**\n\n{assists}")
  cols[4].markdown(f"**Points**\n\n{points}")
  cols[5].markdown(f"**Points per 60 mins**\n\n{pp_60mins}")
  st.markdown('---')

def show_defensive_player_stats(games_played, toi, takeaways, giveaways, blocked, hits):
  st.markdown('---')
  cols = st.columns(6)
  cols[0].markdown(f"**Games Played**\n\n{games_played}")
  cols[1].markdown(f"**TOI (min)**\n\n{toi}")
  cols[2].markdown(f"**Total Takeaways**\n\n{takeaways}")
  cols[3].markdown(f"**Total Giveaways**\n\n{giveaways}")
  cols[4].markdown(f"**Total Blocked Shots**\n\n{blocked}")
  cols[5].markdown(f"**Total Hits**\n\n{hits}")
  st.markdown('---')

def get_offensive_player_season_level(player_df):
  
  player_df = player_df.sort_values(by='TOTAL_POINTS_PER_60MINUTE', ascending=False).head(1).reset_index(drop=True)

  headshot, heropic = get_player_pics(player_df)

  player_name = player_df.loc[0, "FULL_NAME"]
  player_team = player_df.loc[0, "TEAM_NAME"]
  season = player_df.loc[0, "SEASON_START"]
  games_played = player_df.loc[0, "GAMES_PLAYED"]
  toi = player_df.loc[0, 'TOTAL_MINUTES']
  goals = player_df.loc[0, "TOTAL_GOALS"]
  assists = player_df.loc[0, "TOTAL_ASSISTS"]
  points = player_df.loc[0, "TOTAL_POINTS"]
  pp_60mins = player_df.loc[0, "TOTAL_POINTS_PER_60MINUTE"]
  position = player_df.loc[0, "PRIMARY_POSITION"]
  team_id = player_df.loc[0, 'TEAM_ID']

  logo_png = get_team_logo(team_id)

  st.header(f"Best Offensive Player for {season}-{season + 1} season")
  col1, col2 = st.columns([2, 3])
  with col1:
    player_name_headshot_markdown(player_name, headshot)

  with col2:
    position_box_header(position)
    season_level_player_team_and_icon(player_team, logo_png)

  show_offensive_player_stats(games_played, toi, goals, assists, points, pp_60mins)
  st.image(f"{heropic}", use_container_width=True)

# Used to normalise defensive stats for season_level and across seasons  
def safe_normalize(col):
    min_val = col.min()
    max_val = col.max()
    if max_val == min_val:
        return pd.Series([0] * len(col), index=col.index)
    return (col - min_val) / (max_val - min_val)
      
def get_defensive_player_season_level(player_df):

  player_df['takeaway_norm'] = safe_normalize(player_df['TAKEAWAYS_PER_60MINS'])
  player_df['giveaway_norm'] = safe_normalize(player_df['GIVEAWAYS_PER_60MINS'])
  player_df['blocked_norm'] = safe_normalize(player_df['BLOCKED_SHOTS_PER_60MINUTE'])
  player_df['hits_norm'] = safe_normalize(player_df['HITS_PER_60MINUTE'])
  player_df['defensive_score'] = 0.3 * player_df['blocked_norm'].astype(float) + \
                        0.3 * player_df['takeaway_norm'].astype(float) + \
                        0.2 * (1 - player_df['giveaway_norm'].astype(float)) + \
                        0.2 * player_df['hits_norm'].astype(float)
  player_df = player_df.sort_values(by='defensive_score', ascending=False).head(1).reset_index(drop=True)

  headshot, heropic = get_player_pics(player_df)

  season = player_df.loc[0, 'SEASON_START']
  player_name = player_df.loc[0, 'FULL_NAME']
  player_team = player_df.loc[0, 'TEAM_NAME']
  position = player_df.loc[0, 'PRIMARY_POSITION']
  games_played = player_df.loc[0, 'GAMES_PLAYED']
  toi = player_df.loc[0, "TOTAL_MINUTES"]
  takeaways = player_df.loc[0, 'TOTAL_TAKEAWAYS']
  giveaways = player_df.loc[0, 'TOTAL_GIVEAWAYS']
  blocked = player_df.loc[0, 'TOTAL_BLOCKED']
  hits = player_df.loc[0, 'TOTAL_HITS']
  team_id = player_df.loc[0, 'TEAM_ID']

  logo_png = get_team_logo(team_id) 

  st.header(f"Best Defensive Player for {season}-{season + 1} season")
  col1, col2 = st.columns([2, 3])
  with col1:
    player_name_headshot_markdown(player_name, headshot)

  with col2:
    position_box_header(position)
    season_level_player_team_and_icon(player_team, logo_png)

  show_defensive_player_stats(games_played, toi, takeaways, giveaways, blocked, hits)
  st.image(f"{heropic}", use_container_width=True)

def get_leaderboard_season_level_filtered_df(season_start, season_end, positions):
  positions_str = "', '".join(positions)

  player_query = f"""
    SELECT
      agg.PLAYER_ID,
      p.FULL_NAME,
      MIN(agg.season_start) as season_from,
      MAX(agg.season_start) as season_to,
      SUM(GAMES_PLAYED) AS GAMES_PLAYED,
      SUM(TOTAL_GOALS) AS TOTAL_GOALS,
      SUM(TOTAL_ASSISTS) AS TOTAL_ASSISTS,
      SUM(TOTAL_POINTS) AS TOTAL_POINTS,
      SUM(TOTAL_SHOTS) AS TOTAL_SHOTS,
      SUM(TOTAL_TOI_MIN) AS TOI,
      AVG(GOALS_PER_60MINUTE) + AVG(ASSISTS_PER_60MINUTE) AS AVG_POINTS_PER_60MIN,
      SUM(TOTAL_HITS) AS TOTAL_HITS,
      SUM(TOTAL_BLOCKED) AS TOTAL_BLOCKED,
      SUM(TOTAL_TAKEAWAYS) AS TOTAL_TAKEAWAYS,
      SUM(TOTAL_GIVEAWAYS) AS TOTAL_GIVEAWAYS,
      AVG(GIVEAWAYS_PER_60MINS) AS AVG_GIVEAWAYS_PER_60MIN,
      AVG(TAKEAWAYS_PER_60MINS) AS AVG_TAKEAWAYS_PER_60MIN,
      AVG(BLOCKED_SHOTS_PER_60MINUTE) AS AVG_BLOCKED_SHOTS_PER_60MIN,
      AVG(HITS_PER_60MINUTE) AS AVG_HITS_PER_60MIN
    FROM NHL_DB.DEV_SCH_CORE.LEADERBOARD_SEASON_LEVEL_STATS agg
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_PLAYER p
    ON agg.PLAYER_ID = p.PLAYER_ID
    WHERE SEASON_START BETWEEN {season_start} and {season_end}
    AND p.PRIMARY_POSITION IN ('{positions_str}')
    GROUP BY agg.PLAYER_ID, p.FULL_NAME
  """
  player = session.sql(player_query).collect()
  return pd.DataFrame(player)

def get_career_level_teams(player_df):
  team_query = f"""
    select distinct t.team_name, t.TEAM_PIC_URL
    from NHL_DB.DEV_SCH_CORE.FCT_PLAYER_GAME_STATS f
    left join NHL_DB.DEV_SCH_CORE.DIM_TEAM t
    on f.team_id = t.team_id
    where player_id = {player_df.loc[0, 'PLAYER_ID']}
  """
  teams = session.sql(team_query).collect()
  teams_played_df = pd.DataFrame(teams)
  return [teams_played_df['TEAM_NAME'].tolist(), teams_played_df['TEAM_PIC_URL'].tolist()]

def get_career_level_positions(player_df):
  position_query = f"""
    select PRIMARY_POSITION
    from NHL_DB.DEV_SCH_CORE.DIM_PLAYER
    where PLAYER_ID = {player_df.loc[0, 'PLAYER_ID']}
  """
  position = session.sql(position_query).collect()
  return pd.DataFrame(position)

def career_level_player_team_and_logo(teams_played, team_logos):
  st.write('Played for')
  inner_col1, inner_col2 = st.columns([3,2])
  with inner_col1:
    for team in teams_played:
      st.metric(label="", value=team)
  with inner_col2:
    for logo_png in team_logos:
      st.image(f"{logo_png}", width=125)

def get_best_offensive_player_across_season(player_season_level_df):
  player_df = player_season_level_df.sort_values(by='AVG_POINTS_PER_60MIN', ascending=False).head(1).reset_index(drop=True)

  headshot, heropic = get_player_pics(player_df)

  teams_played, team_logos = get_career_level_teams(player_df)

  position_df = get_career_level_positions(player_df)

  season_from = player_df.loc[0, 'SEASON_FROM']
  season_to = player_df.loc[0, 'SEASON_TO']
  player_name = player_df.loc[0, 'FULL_NAME']
  games_played = player_df.loc[0, "GAMES_PLAYED"]
  toi = player_df.loc[0, 'TOI']
  goals = player_df.loc[0, "TOTAL_GOALS"]
  assists = player_df.loc[0, "TOTAL_ASSISTS"]
  points = player_df.loc[0, "TOTAL_POINTS"]
  pp_60mins = player_df.loc[0, "AVG_POINTS_PER_60MIN"]
  position = position_df.loc[0, "PRIMARY_POSITION"]
  
  st.header(f"Best Offensive Player from {season_from} to {season_to + 1}")
  col1, col2 = st.columns([2, 3])
  with col1:
    player_name_headshot_markdown(player_name, headshot)
  with col2:
    position_box_header(position)
    career_level_player_team_and_logo(teams_played, team_logos)

  show_offensive_player_stats(games_played, toi, goals, assists, points, pp_60mins)

  st.image(f"{heropic}", use_container_width=True)

def get_best_defensive_player_across_seasons(player_season_level_df):
  
  player_df = player_season_level_df
  player_df['takeaway_norm'] = safe_normalize(player_df['AVG_TAKEAWAYS_PER_60MIN'])
  player_df['giveaway_norm'] = safe_normalize(player_df['AVG_GIVEAWAYS_PER_60MIN'])
  player_df['blocked_norm'] = safe_normalize(player_df['AVG_BLOCKED_SHOTS_PER_60MIN'])
  player_df['hits_norm'] = safe_normalize(player_df['AVG_HITS_PER_60MIN'])
  player_df['defensive_score'] = 0.3 * player_df['blocked_norm'].astype(float) + \
                        0.3 * player_df['takeaway_norm'].astype(float) + \
                        0.2 * (1 - player_df['giveaway_norm'].astype(float)) + \
                        0.2 * player_df['hits_norm'].astype(float)
  player_df = player_df.sort_values(by='defensive_score', ascending=False).head(1).reset_index(drop=True)

  headshot, heropic = get_player_pics(player_df)

  teams_played, team_logos = get_career_level_teams(player_df)

  position_df = get_career_level_positions(player_df)

  season_from = player_df.loc[0, 'SEASON_FROM']
  season_to = player_df.loc[0, 'SEASON_TO']
  player_name = player_df.loc[0, 'FULL_NAME']
  games_played = player_df.loc[0, "GAMES_PLAYED"]
  toi = player_df.loc[0, 'TOI']
  position = position_df.loc[0, 'PRIMARY_POSITION']
  takeaways = player_df.loc[0, 'TOTAL_TAKEAWAYS']
  giveaways = player_df.loc[0, 'TOTAL_GIVEAWAYS']
  blocked = player_df.loc[0, 'TOTAL_BLOCKED']
  hits = player_df.loc[0, 'TOTAL_HITS']

  st.header(f"Best Defensive Player from {season_from} to {season_to + 1}")
  col1, col2 = st.columns([2, 3])
  with col1:
    player_name_headshot_markdown(player_name, headshot)
  with col2:
    position_box_header(position)
    career_level_player_team_and_logo(teams_played, team_logos)

  show_defensive_player_stats(games_played, toi, takeaways, giveaways, blocked, hits)
  st.image(f"{heropic}", use_container_width=True)
  
def get_filtered_df(season_start, season_end, positions, teams):
  
  positions_str = "', '".join(positions)
  teams_str = "', '".join(teams)

  player_query = f"""
    SELECT
      agg.PLAYER_ID,
      agg.TEAM_ID,
      agg.SEASON_START,
      GAMES_PLAYED,
      TOTAL_TOI_MIN,
      TOTAL_GOALS,
      TOTAL_ASSISTS,
      TOTAL_POINTS,
      GOALS_PER_60MINUTE + ASSISTS_PER_60MINUTE AS TOTAL_POINTS_PER_60_MINUTE,
      FULL_NAME,
      PRIMARY_POSITION,
      TEAM_NAME
    FROM NHL_DB.DEV_SCH_CORE.AGG_PLAYER_SEASON_STATS agg
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_PLAYER p
    ON agg.PLAYER_ID = p.PLAYER_ID
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_TEAM t
    ON agg.TEAM_ID = t.TEAM_ID
    WHERE GAMES_PLAYED >= 41 AND
        SEASON_START BETWEEN {season_start} 
        AND {season_end} 
        AND p.PRIMARY_POSITION IN ('{positions_str}')
        AND TEAM_NAME IN ('{teams_str}')
  """
  player = session.sql(player_query).collect()
  return pd.DataFrame(player)
  
def total_points_per_60mins_by_position_box_plot(df):

  # Each data point in the boxplot represents a single player's performance for one season.
  st.subheader("Total Points per 60 by Position")
  fig_box = px.box(df, x='PRIMARY_POSITION', y='TOTAL_POINTS_PER_60_MINUTE', points="all")
  st.plotly_chart(fig_box)

def total_points_per_60mins_by_position_violin_chart(df):
  st.subheader("Total Points per 60 by Position")
  fig_violin = px.violin(
    df,
    x='PRIMARY_POSITION',
    y='TOTAL_POINTS_PER_60_MINUTE',
    points='all',  # shows all individual points
    box=True,       # includes a boxplot inside the violin
    color='PRIMARY_POSITION'  # optional: color each violin for clarity
  )

  st.plotly_chart(fig_violin)

def points_per_60mins_by_toi_scatter_plot(df):
  # Scatter plot: TOI vs G+A/60, color-coded by team, with tooltips
  st.subheader("TOI vs Goals+Assists per 60")
  fig_scatter = px.scatter(
      df,
      x='TOTAL_TOI_MIN',
      y='TOTAL_POINTS_PER_60_MINUTE',
      color='PRIMARY_POSITION',
      hover_data=['PLAYER_ID', 'TEAM_NAME', 'SEASON_START'],
      labels={
        "TOTAL_TOI_MIN": "Time on Ice (min)",
        "TOTAL_POINTS_PER_60_MINUTE": "Points per 60 min",
        "PRIMARY_POSITION": "Position"
      },
      title="TOI vs Points per 60min by Position",
      opacity=0.7
  )
  st.plotly_chart(fig_scatter)

def top_pp_bar_chart(season_start, season_end, positions, teams):
  positions_str = "', '".join(positions)
  teams_str = "', '".join(teams)

  player_query = f"""
    WITH CTE AS (
      SELECT *,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY TOTAL_PP_POINTS_PER_60MINUTE DESC) AS ROW_NUM
      FROM NHL_DB.DEV_SCH_CORE.LEADERBOARD_SEASON_LEVEL_STATS agg
    ), deduplicated AS (
      SELECT *
      FROM CTE
      WHERE ROW_NUM = 1
    )
    SELECT
      agg.PLAYER_ID,
      agg.TEAM_ID,
      agg.SEASON_START,
      GAMES_PLAYED,
      TOTAL_PP_POINTS,
      TOTAL_PP_MINUTES,
      TOTAL_PP_POINTS_PER_60MINUTE,
      FULL_NAME,
      PRIMARY_POSITION,
      TEAM_NAME
    FROM deduplicated agg
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_PLAYER p
    ON agg.PLAYER_ID = p.PLAYER_ID
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_TEAM t
    ON agg.TEAM_ID = t.TEAM_ID
    WHERE SEASON_START BETWEEN {season_start} AND {season_end} 
        AND p.PRIMARY_POSITION IN ('{positions_str}')
        AND TEAM_NAME IN ('{teams_str}')
    ORDER BY (TOTAL_PP_POINTS_PER_60MINUTE) DESC
  """
  player = session.sql(player_query).collect()
  player_df = pd.DataFrame(player)
  player_df['TOTAL_PP_POINTS_PER_60MINUTE'] = player_df['TOTAL_PP_POINTS_PER_60MINUTE'].astype(float)
  top_players = player_df.sort_values('TOTAL_PP_POINTS_PER_60MINUTE', ascending=False).head(10)

  top_players['SEASON_LABEL'] = top_players['SEASON_START'].astype(str) + '-' + (top_players['SEASON_START'] + 1).astype(str)

  # Step 2: Bar chart
  fig_bar = alt.Chart(top_players).mark_bar().encode(
    x=alt.X('TOTAL_PP_POINTS_PER_60MINUTE:Q', title='Points per 60min'),
    y=alt.Y('FULL_NAME:N', sort=top_players['FULL_NAME'].tolist(), title='Player'),
    color='PRIMARY_POSITION:N',
    tooltip=[
        'FULL_NAME', 
        'PRIMARY_POSITION', 
        'SEASON_LABEL', 
        'TOTAL_PP_POINTS_PER_60MINUTE']).properties(
        title='Top 10 Power Play Contributors (Points per 60)',
        width=600,
        height=600
    )

  text = alt.Chart(top_players).mark_text(
    align='left',
    baseline='middle',
    dx=5,      # Push text a bit outside the bar end
    color='black'
  ).encode(
      y=alt.Y('FULL_NAME:N', sort=top_players['FULL_NAME'].tolist()),
      x='TOTAL_PP_POINTS_PER_60MINUTE:Q',
      text='SEASON_LABEL:N'
  )

  chart = (fig_bar + text)

  st.altair_chart(chart, use_container_width=True)

def top_pk_bar_chart(season_start, season_end, positions, teams):
  positions_str = "', '".join(positions)
  teams_str = "', '".join(teams)

  player_query = f"""
    WITH CTE AS (
      SELECT *,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY TOTAL_SH_POINTS_PER_60MINUTE DESC) AS ROW_NUM
      FROM NHL_DB.DEV_SCH_CORE.LEADERBOARD_SEASON_LEVEL_STATS agg
    ), deduplicated AS (
      SELECT *
      FROM CTE
      WHERE ROW_NUM = 1
    )
    SELECT
      agg.PLAYER_ID,
      agg.TEAM_ID,
      agg.SEASON_START,
      GAMES_PLAYED,
      TOTAL_SH_POINTS,
      TOTAL_SH_MINUTES,
      TOTAL_SH_POINTS_PER_60MINUTE,
      FULL_NAME,
      PRIMARY_POSITION,
      TEAM_NAME
    FROM deduplicated agg
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_PLAYER p
    ON agg.PLAYER_ID = p.PLAYER_ID
    LEFT JOIN NHL_DB.DEV_SCH_CORE.DIM_TEAM t
    ON agg.TEAM_ID = t.TEAM_ID
    WHERE SEASON_START BETWEEN {season_start} AND {season_end} 
        AND p.PRIMARY_POSITION IN ('{positions_str}')
        AND TEAM_NAME IN ('{teams_str}')
    ORDER BY (TOTAL_PP_POINTS_PER_60MINUTE) DESC
  """
  player = session.sql(player_query).collect()
  player_df = pd.DataFrame(player)
  player_df['TOTAL_SH_POINTS_PER_60MINUTE'] = player_df['TOTAL_SH_POINTS_PER_60MINUTE'].astype(float)
  top_players = player_df.sort_values('TOTAL_SH_POINTS_PER_60MINUTE', ascending=False).head(10)

  top_players['SEASON_LABEL'] = top_players['SEASON_START'].astype(str) + '-' + (top_players['SEASON_START'] + 1).astype(str)
  # Step 2: Bar chart
  fig_bar = alt.Chart(top_players).mark_bar().encode(
    x=alt.X('TOTAL_SH_POINTS_PER_60MINUTE:Q', title='Points per 60min'),
    y=alt.Y('FULL_NAME:N', sort=top_players['FULL_NAME'].tolist(), title='Player'),
    color='PRIMARY_POSITION:N',
    tooltip=[
        'FULL_NAME', 
        'PRIMARY_POSITION', 
        'SEASON_LABEL', 
        'TOTAL_SH_POINTS_PER_60MINUTE']).properties(
        title='Top 10 Penalty Kill Contributors (Points per 60)',
        width=600,
        height=600
    )

  text = alt.Chart(top_players).mark_text(
    align='left',
    baseline='middle',
    dx=5,      # Push text a bit outside the bar end
    color='black'
  ).encode(
      y=alt.Y('FULL_NAME:N', sort=top_players['FULL_NAME'].tolist()),
      x='TOTAL_PK_POINTS_PER_60MINUTE:Q',
      text='SEASON_LABEL:N'
  )

  chart = (fig_bar + text)

  st.altair_chart(chart, use_container_width=True)

#######################
# Start
session = start_session()

#######################
# Sidebar
with st.sidebar:
  st.title('NHL Player Performance Dashboard')  
  season_start, season_end = season_slider()
  teams = get_teams()
  positions = get_positions()
  
#######################
header_col1, header_col2 = st.columns([1,15])
with header_col1:
  st.image("https://nhl-team-logo.s3.ap-southeast-1.amazonaws.com/nhl_logos/05_NHL_Shield.svg.png", width=50)
with header_col2:
  st.markdown("<h1 style='margin-top: -22px;'>NHL Player Dashboard</h1>", unsafe_allow_html=True)

if teams and positions:
  player_df = get_leaderboard_filtered_df(season_start, season_end, positions, teams)
  player_season_level_df = get_leaderboard_season_level_filtered_df(season_start, season_end, positions)

  tab_titles = ['Leaderboard', 'Skater Insights by Positions', 'Special Team Impact']
  tabs = st.tabs(tab_titles)

  with tabs[0]:
    per_season_toggle = st.toggle("get across seasons")
    if per_season_toggle:
      best_offensive_player_across_season = get_best_offensive_player_across_season(player_season_level_df)
      best_defensive_player_across_season = get_best_defensive_player_across_seasons(player_season_level_df)

    else:
      best_offensive_player_season = get_offensive_player_season_level(player_df)
      best_defensive_player_season = get_defensive_player_season_level(player_df)

      
  with tabs[1]:
    df = get_filtered_df(season_start, season_end, positions, teams)
    violin_toggle = st.toggle("switch to violin chart")
    if violin_toggle:
      total_points_per_60mins_by_position_violin_chart(df)
    else:
      total_points_per_60mins_by_position_box_plot(df)

    points_per_60mins_by_toi_scatter_plot(df)

  with tabs[2]:
    top_powerplay_by_points = top_pp_bar_chart(season_start, season_end, positions, teams)
    top_penaltykill_by_points = top_pk_bar_chart(season_start, season_end, positions, teams)
else:
  st.warning("Please select at least one team and one position to display the charts.")
