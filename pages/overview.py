import streamlit as st
import pandas as pd
from src.database.connection import get_connection

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
st.title("📊 Overview")

def get_overview_metrics():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM spotify_tracks")
            total_tracks = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT artist) FROM spotify_tracks")
            total_artists = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT album) FROM spotify_tracks")
            total_albums = cursor.fetchone()[0]
            
            return total_tracks, total_artists, total_albums
    except Exception:
        return 0, 0, 0

tracks, artists, albums = get_overview_metrics()

col1, col2, col3 = st.columns(3)
col1.metric("Total Tracks", tracks)
col2.metric("Total Artists", artists)
col3.metric("Total Albums", albums)

st.subheader("Top Tracks by Popularity")
try:
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT track_name, artist, popularity FROM spotify_tracks ORDER BY popularity DESC LIMIT 10", conn)

    if not df.empty:
        st.bar_chart(data=df.set_index('track_name')['popularity'], color="#1DB954")
    else:
        st.info("No data available. Please run the ingestion pipeline.")
except Exception:
    st.info("Database not initialized or no data available. Please run the ingestion pipeline.")
