import os
import json
import time
import logging
from datetime import datetime
from jobs import q, update_job_status, get_job_by_id, save_results, rd

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

def parse_date(date_str: str) -> datetime:
    """
    Parse a date string using either "m/d/yyyy" or "YYYY-MM-DD" format.
    """
    date_str = date_str.strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"cannot parse date '{date_str}'")

def get_hgnc_ids_in_range(hgnc_id_start: str, hgnc_id_end: str) -> list:
    """
    Retrieve HGNC IDs from Redis within the numeric range [start, end].
    Assumes gene keys are stored as "gene:HGNC:<number>".

    :param hgnc_id_start: Start HGNC ID (e.g., "HGNC:6")
    :param hgnc_id_end: End HGNC ID (e.g., "HGNC:12345")
    :return: List of HGNC IDs within the range.
    """
    all_keys = rd.keys("gene:HGNC:*")
    gene_list = []
    for key in all_keys:
        try:
            gene_id = key.decode("utf-8").replace("gene:", "")
            num = int(gene_id.split(":")[1])
            gene_list.append((gene_id, num))
        except Exception:
            continue
    try:
        start_num = int(hgnc_id_start.split(":")[1])
        end_num = int(hgnc_id_end.split(":")[1])
    except Exception:
        return []
    filtered = [gid for (gid, num) in gene_list if start_num <= num <= end_num]
    return filtered

@q.worker
def process_job(jid: str) -> None:
    """
    Process a job by:
    - Retrieving gene records in the specified HGNC ID range.
    - Extracting and parsing the 'date_approved_reserved' field.
    - Computing a yearly breakdown, as well as the earliest and latest approval dates.
    - Storing the resulting JSON summary in Redis (db=3) and updating the job status.
    """
    try:
        update_job_status(jid, "in progress")
        logging.info(f"Processing job {jid}")

        job = get_job_by_id(jid)
        if not job:
            logging.error(f"Job {jid} not found.")
            return

        hgnc_start = job["hgnc_id_start"]
        hgnc_end = job["hgnc_id_end"]

        # Retrieve gene IDs within the specified range.
        gene_ids = get_hgnc_ids_in_range(hgnc_start, hgnc_end)
        logging.info(f"Found {len(gene_ids)} gene IDs in range {hgnc_start} to {hgnc_end}")

        total_genes = 0
        earliest_date = None
        latest_date = None
        yearly_breakdown = {}

        for gid in gene_ids:
            key = "gene:" + gid
            gene_str = rd.get(key)
            if not gene_str:
                continue
            gene_data = json.loads(gene_str)
            date_str = gene_data.get("date_approved_reserved", "").strip()
            if not date_str:
                continue
            try:
                dt = parse_date(date_str)
            except Exception as e:
                logging.warning(f"Skipping {gid}: cannot parse date '{date_str}'")
                continue
            
            total_genes += 1
            if earliest_date is None or dt < earliest_date:
                earliest_date = dt
            if latest_date is None or dt > latest_date:
                latest_date = dt

            year = dt.year
            yearly_breakdown[year] = yearly_breakdown.get(year, 0) + 1

        if total_genes == 0:
            results = {"error": "No valid dates found in the specified range."}
        else:
            results = {
                "total_genes": total_genes,
                "earliest_date": earliest_date.strftime("%m/%d/%Y") if earliest_date else None,
                "latest_date": latest_date.strftime("%m/%d/%Y") if latest_date else None,
                "yearly_breakdown": yearly_breakdown
            }

        save_results(jid, json.dumps(results, indent=2, sort_keys=True))
        update_job_status(jid, "complete")
        logging.info(f"Job {jid} complete. Processed {total_genes} genes.")

    except Exception as e:
        logging.error(f"Error processing job {jid}: {str(e)}")

if __name__ == "__main__":
    logging.info("Worker started. Waiting for jobs...")
    process_job()
