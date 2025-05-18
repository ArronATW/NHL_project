
-- raw layer table for game_skater_stats.csv
CREATE OR REPLACE TRANSIENT TABLE NHL_DB.STAGE_SCH.game_skater_stats (
  game_id STRING,
  player_id STRING,
  team_id STRING,
  time_on_ice INT,
  assists INT,
  goals INT,
  shots INT,
  hits STRING,
  power_play_goals INT,
  power_play_assists INT,
  penalty_minutes INT,
  face_off_wins INT,
  face_off_taken INT,
  takeaways STRING,
  giveaways STRING,
  short_handed_goals INT,
  short_handed_assists INT,
  blocked STRING,
  plusminus INT,
  even_time_on_ice INT, 
  short_handed_time_on_ice INT,
  power_play_time_on_ice INT
  );

-- raw layer table for player_info.csv
CREATE OR REPLACE TRANSIENT TABLE NHL_DB.STAGE_SCH.player_info (
  player_id STRING,
  first_name STRING,
  last_name STRING,
  nationality STRING,
  birth_city STRING,
  primary_position STRING,
  birth_date DATETIME,
  birth_state_province STRING,
  height STRING,
  height_cm STRING,
  weight STRING,
  shoots_catches STRING
  );

-- raw layer table for game.csv
CREATE OR REPLACE TRANSIENT TABLE NHL_DB.STAGE_SCH.game (
  game_id STRING,
  season STRING,
  type STRING,
  date_time_GMT DATETIME,
  away_team_id INT,
  home_team_id INT,
  away_goals INT,
  home_goals INT,
  outcome STRING,
  home_rink_side_start STRING,
  venue STRING,
  venue_link STRING,
  venue_time_zone_id STRING,
  venue_time_zone_offset INT,
  venue_time_zone_tz STRING
  );

-- raw layer table for team_info.csv
CREATE OR REPLACE TRANSIENT TABLE NHL_DB.STAGE_SCH.team_info (
  team_id STRING,
  franchise_id INT,
  short_name STRING,
  team_name STRING,
  abbreviation STRING,
  link STRING
  );

-- Create file format objects (csv and csv.gz formats) 
CREATE OR REPLACE FILE FORMAT NHL_DB.STAGE_SCH.CSV_FILEFORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  EMPTY_FIELD_AS_NULL = TRUE
  NULL_IF = ('NA')
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- OPTIONAL, do not need any csv_gz format files
CREATE OR REPLACE FILE FORMAT csv_gz_fileformat
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    EMPTY_FIELD_AS_NULL = TRUE
    COMPRESSION = 'GZIP';

    
-- Create stage object with integration object & file format object

-- CHANGE TO ACCOUNTADMIN TO RUN THIS
CREATE OR REPLACE STORAGE INTEGRATION s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUENHL_DB.DEV_SCH
  STORAGE_AWS_ROLE_ARN = '<REPLACE_WITH_YOUR_AWS_ROLE_ARN>'
  STORAGE_ALLOWED_LOCATIONS = ('<REPLACE_WITH_YOUR_S3_BUCKET_LOCATION>');

-- get the STORAGE_AWS_IAM_USER_ARN & EXTERNAL_ID, update Trust policy in IAM
-- the external_id changes and not fixed, need to update regularly
DESC INTEGRATION s3_int;


CREATE OR REPLACE stage NHL_DB.STAGE_SCH.csv_folder
    URL = 's3://ice-breakers-nhl-data-bucket/raw/csv/'
    STORAGE_INTEGRATION = s3_int
    FILE_FORMAT = NHL_DB.STAGE_SCH.CSV_FILEFORMAT;


CREATE OR REPLACE stage NHL_DB.STAGE_SCH.csv_gz_folder
    URL = 's3://ice-breakers-nhl-data-bucket/raw/csv_gz/'
    STORAGE_INTEGRATION = s3_int
    FILE_FORMAT = NHL_DB.STAGE_SCH.CSV_GZ_FILEFORMAT;
    
// List files in stage
LIST @csv_folder;
LIST @csv_gz_folder;

//Load data using copy command

COPY INTO NHL_DB.STAGE_SCH.game_skater_stats 
    FROM @csv_folder
    file_format= csv_fileformat
    FILES = ('game_skater_stats.csv');

COPY INTO NHL_DB.STAGE_SCH.player_info
    FROM @csv_folder
    file_format= csv_fileformat
    FILES = ('player_info.csv');

COPY INTO NHL_DB.STAGE_SCH.game
    FROM @csv_folder
    file_format= csv_fileformat
    FILES = ('game.csv');

COPY INTO NHL_DB.STAGE_SCH.team_info
    FROM @csv_folder
    file_format= csv_fileformat
    FILES = ('team_info.csv');


