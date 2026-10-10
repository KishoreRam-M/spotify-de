import streamlit as st

st.set_page_config(
    page_title="Spotify Data Engineering",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and green accents
st.markdown("""
<style>
    :root {
        --spotify-green: #1DB954;
        --spotify-black: #191414;
        --spotify-dark-gray: #212121;
        --spotify-light-gray: #535353;
        --spotify-white: #FFFFFF;
    }
    
    .stApp {
        background-color: var(--spotify-black);
        color: var(--spotify-white);
    }
    
    h1, h2, h3 {
        color: var(--spotify-white);
    }
    
    .stButton>button {
        background-color: var(--spotify-green);
        color: var(--spotify-white);
        border: none;
        border-radius: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎵 Spotify Data Engineering Project")
st.markdown("""
Welcome to the Spotify Data Engineering dashboard!

This project demonstrates an end-to-end data pipeline:
- **Extract**: Fetch track metadata from the Spotify Web API.
- **Transform**: Clean and normalize data.
- **Load**: Store data into a local SQLite database.

Use the sidebar to navigate through the dashboard.
""")
