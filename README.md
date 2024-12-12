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





