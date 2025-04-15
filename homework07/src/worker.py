import time
import logging
from jobs import q, update_job_status

logging.basicConfig(level=logging.INFO)

@q.worker
def process_job(jid):
    try:
        update_job_status(jid, "in progress")
        logging.info(f"Processing job: {jid}")
        time.sleep(5)
        update_job_status(jid, "complete")
        logging.info(f"Completed job: {jid}")
    except Exception as e:
        logging.error(f"Error processing job {jid}: {e}")

if __name__ == "__main__":
    logging.info("Worker started. Waiting for jobs...")
    process_job()
