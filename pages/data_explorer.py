import streamlit as st
import pandas as pd
from src.database.connection import get_connection

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")
st.title("🔍 Data Explorer")

try:
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM spotify_tracks ORDER BY fetched_at DESC", conn)

    if df.empty:
        st.info("No tracks found in the database. Run the pipeline first.")
    else:
        search_query = st.text_input("Search tracks, artists, or albums:")
        if search_query:
            mask = (
                df['track_name'].str.contains(search_query, case=False, na=False) |
                df['artist'].str.contains(search_query, case=False, na=False) |
                df['album'].str.contains(search_query, case=False, na=False)
            )
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True)
except Exception:
    st.info("Database not initialized or no data available. Please run the ingestion pipeline.")
