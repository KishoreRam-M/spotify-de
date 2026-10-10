import logging
from src.pipeline.extract import get_track_urls_from_file, extract_track_id, fetch_track_metadata
from src.pipeline.transform import transform_track_data
from src.database.repository import insert_or_update_track, log_pipeline_run, finish_pipeline_run
from src.spotify.client import get_spotify_client

logger = logging.getLogger(__name__)

def run_ingestion_pipeline(urls_file: str = "track.txt"):
    """Run the ETL pipeline for track ingestion."""
    logger.info("Starting ingestion pipeline...")
    run_id = log_pipeline_run("RUNNING")
    
    stats = {
        "fetched": 0,
        "inserted": 0,
        "updated": 0,
        "failed": 0
    }
    
    error_msg = None
    
    try:
        sp = get_spotify_client()
        urls = get_track_urls_from_file(urls_file)
        
        for url in urls:
            try:
                track_id = extract_track_id(url)
                raw_data = fetch_track_metadata(sp, track_id)
                stats["fetched"] += 1
                
                clean_data = transform_track_data(raw_data)
                inserted, updated = insert_or_update_track(clean_data)
                
                if inserted:
                    stats["inserted"] += 1
                if updated:
                    stats["updated"] += 1
                    
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                stats["failed"] += 1
                
        status = "COMPLETED" if stats["failed"] == 0 else "PARTIAL_SUCCESS"
        if len(urls) == 0:
            status = "SKIPPED"
            error_msg = "No URLs found in file."
            
    except Exception as e:
        logger.exception("Pipeline failed critically.")
        status = "FAILED"
        error_msg = str(e)
        
    finally:
        finish_pipeline_run(
            run_id=run_id,
            status=status,
            records_fetched=stats["fetched"],
            records_inserted=stats["inserted"],
            records_updated=stats["updated"],
            records_failed=stats["failed"],
            error_message=error_msg
        )
        logger.info(f"Pipeline finished with status: {status}. Stats: {stats}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_ingestion_pipeline()
