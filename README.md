# Spotify Global Top 50 ETL Project

# Overview
This project is an Extract, Transform, Load (ETL) pipeline for analyzing the Spotify Global Top 50 playlist. It retrieves track and artist information from the Spotify API, performs data transformations, and loads the data into a SQLite database for further analysis. After that the pulgin files are containerized using docker then automated using Airflow.

# Features

Extracts track and artist data from Spotify's Global Top 50 playlist
Performs data quality checks
Transforms data to calculate track counts per artist
Loads data into a SQLite database with three tables:

1. Top50Tracks: Contains track-level information
2. Artist_Info: Stores detailed artist information
3 .Track_Count_per_Artist: Tracks the number of tracks per artist in the playlist

# Dependencies
Install the required dependencies using:

# bash
pip install -r requirements.txt

# Project libraries
- pandas (2.2.0)
- requests (2.31.0)
- sqlalchemy (2.0.25)
- python-dotenv (1.0.0)

# Setup

1. Create a virtual Environment (.venv) to install dependencies.
2. Obtain Spotify API credentials:
    - Go to the Spotify Developer Dashboard
    - Create a new application
    - Get your Client ID and Client Secret
3. Project Structure
      - Extract.py: Retrieves data from Spotify API
      - Transform.py: Performs data transformations and quality checks
      - Load.py: Loads transformed data into SQLite database
      - requirements.txt: Lists project dependencies

# Usage
Run the ETL pipeline by executing:

# bash
python Load.py

# Database Schema
  Top50Tracks Table

    - artist_id (VARCHAR)
    - artist_name (VARCHAR)
    - track_id (VARCHAR)
    - track_name (VARCHAR)
    - playlist_date (DATE)
    
    Artist_Info Table
    
    - artist_name (VARCHAR)
    - artist_id (VARCHAR)
    - total_followers (BIGINT)
    - genres (TEXT)
    - image_url (VARCHAR)
    - popularity (INT)
    
    Track_Count_per_Artist Table
    
    - artist_id (VARCHAR)
    - artist_name (VARCHAR)
    - count (INT)
    - playlist_date (DATE)

# Project Structure

1. Obtain the Spotify API credentials

![Screenshot (2)](https://github.com/user-attachments/assets/8e7a8f05-7f2e-4868-9d3a-d200a8c2e640)
Update your Credentials access_token.py using spotify api 

Run these files:
1. Extract.py: Data Extraction Script
               The Extract.py script is responsible for retrieving data from the Spotify PI, specifically focusing on the Global Top 50 playlist.

2. Transform.py : Data Transformation Script
                  The Transform.py script performs data quality checks and transformations on the extracted data.

3. Load.py : Data Loading Script
             The Load.py script handles the process of loading transformed data into a SQLite database. 


We completed our ETL pipeline. The structure of the project should look like below.

D:Downloads/Spotify_etl/spotify_etl
│ Extract.py
│ Load.py
│ GlobalTop50Tracks.sqlite
│ spotify_etl.py
│ Transform.py

Afer you run all the three files, a sqlite file will be created. 
You can visit this site [https://inloop.github.io/sqlite-viewer/] for viewing the sql data

![Screenshot (3)](https://github.com/user-attachments/assets/26d17f89-a825-4cb4-98d5-2fe814c669f8)

Here we completed out ETL Process.

## Dockerization and Automation

# Steps to Dockerize the .py files

1. Install Docker Desktop in your computer
2. Create a docker-compose.yaml file according to your requirements
3. Then we should run the below code in cmd.
    - docker-compose up airflow-init
    - docker-compose up

After this seven sub-containers will be created in docker desktop.

![Screenshot (4)](https://github.com/user-attachments/assets/0e4c56a6-f1c7-4bc8-8683-02ca6c5ab8e9)

The Automation and Dockerization file structure should look like below:

│ docker-compose.yml
├───dags
│ │ spotify_etl.py
| | spotify_final_dag.py
├───logs
├───plugins
└───scripts

After this you can visit the local host link  - [ http://localhost:8080 ] to see your created dags

Username - airflow
password - airflow

![Screenshot (5)](https://github.com/user-attachments/assets/1f0499fd-b293-41e4-9cb0-9f351d9634dc)


Setting up the airflow:

1. Click on Connections
![Screenshot (6)](https://github.com/user-attachments/assets/ac39908b-d902-4728-be79-cfc54f761d17)

2. Then Create a Connection
Then create a connection.

Connection id: postgre_sql 
Connection Type: Postgres
Host: Postgres
Schema: airflow - database name (Vary depeneding on your database name)
Login: airflow
Password: airflow
Port: 5432

3. Now it is time to deploy.

![Screenshot (7)](https://github.com/user-attachments/assets/beea2698-42c2-4810-bd33-fe6cc853d6b8)

![Screenshot (8)](https://github.com/user-attachments/assets/e259b7c9-3878-4766-9d39-6ffcb730e398)

![Screenshot (9)](https://github.com/user-attachments/assets/f418174f-2b3c-48ae-91b6-d509864a51ff)

# Limitation

Use a python version < 13.3 to run Airflow. 

# Resutls.

<img width="1237" alt="image" src="https://github.com/user-attachments/assets/e6a38a8f-f9c6-4c0f-9091-34dc70854c2e" />

<img width="389" alt="image" src="https://github.com/user-attachments/assets/aa1f3eaf-9fed-4183-9690-2446f96a44f0" />


## Conclusion 
The Spotify Global Top 50 ETL project serves as an excellent example of how data engineering techniques can transform raw data into meaningful insights, providing a robust framework for music data analysis.


















