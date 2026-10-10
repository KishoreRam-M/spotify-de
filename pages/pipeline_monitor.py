import streamlit as st
import pandas as pd
from src.pipeline.load import run_ingestion_pipeline
from src.database.schema import init_db
from src.database.connection import get_connection

st.set_page_config(page_title="Pipeline Monitor", page_icon="⚙️", layout="wide")
st.title("⚙️ Pipeline Monitor")

st.markdown("Monitor and manually trigger the ETL ingestion pipeline.")

if st.button("Trigger Ingestion Pipeline"):
    with st.spinner("Initializing database schema..."):
        init_db()
    with st.spinner("Running ingestion pipeline..."):
        try:
            run_ingestion_pipeline()
            st.success("Pipeline executed successfully!")
        except Exception as e:
            st.error(f"Pipeline execution failed: {e}")

st.subheader("Recent Pipeline Runs")
try:
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM pipeline_runs ORDER BY run_id DESC LIMIT 10", conn)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No pipeline runs found.")
except Exception:
    st.info("No pipeline history available. Run the pipeline first.")
