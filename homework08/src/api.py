import json
import logging
import os
import re
import requests
import redis
from flask import Flask, request
from jobs import add_job, get_job_by_id, get_results

app = Flask(__name__)
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

# HGNC data source URL
DATA_URL = "https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json"

def get_redis_client() -> redis.Redis:
    """Return a Redis client for the gene data (db=0)."""
    redis_ip = os.environ.get("REDIS_IP", "redis-db")
    redis_port = int(os.environ.get("REDIS_PORT", "6379"))
    return redis.Redis(host=redis_ip, port=redis_port, db=0)

rd = get_redis_client()

def fetch_hgnc_data(url: str = DATA_URL) -> list:
    """Fetch HGNC gene data from the remote JSON source."""
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict) and "response" in data and "docs" in data["response"]:
            return data["response"]["docs"]
        return data
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching HGNC data: %s", e)
        return []

def load_data_to_redis(data: list) -> int:
    """Store the HGNC gene data in Redis and return the number of genes loaded."""
    count = 0
    try:
        for gene in data:
            if isinstance(gene, dict) and "hgnc_id" in gene:
                key = "gene:" + gene["hgnc_id"]
                try:
                    rd.set(key, json.dumps(gene))
                    count += 1
                except redis.exceptions.ResponseError as re_err:
                    logging.error("Redis ResponseError for key %s: %s", key, re_err)
    except redis.exceptions.ConnectionError as conn_err:
        logging.error("Redis connection failed: %s", conn_err)
        raise Exception("Failed to connect to Redis")
    logging.info("Loaded %d genes into Redis.", count)
    return count

@app.route("/data", methods=["POST"])
def post_data():
    """Load gene data from the HGNC source into Redis."""
    try:
        data = fetch_hgnc_data()
        count = load_data_to_redis(data)
        return {"message": f"Loaded {count} genes into Redis"}, 201
    except Exception as e:
        logging.error("Error loading data: %s", e)
        return {"error": str(e)}, 500

@app.route("/data", methods=["GET"])
def get_data():
    """Retrieve all gene data stored in Redis."""
    try:
        keys = rd.keys("gene:*")
        genes = [json.loads(rd.get(key)) for key in keys if rd.get(key)]
        return json.dumps(genes, indent=2), 200
    except Exception as e:
        logging.error("Error retrieving gene data: %s", e)
        return json.dumps({"error": str(e)}), 500

@app.route("/data", methods=["DELETE"])
def delete_data():
    """Delete all gene data stored in Redis."""
    try:
        keys = rd.keys("gene:*")
        if keys:
            rd.delete(*keys)
        return json.dumps("Deleted gene data from Redis", indent=2), 200
    except Exception as e:
        logging.error("Error deleting gene data: %s", e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/genes", methods=["GET"])
def list_genes():
    """Return a list of all HGNC gene IDs stored in Redis."""
    try:
        keys = rd.keys("gene:*")
        gene_ids = [key.decode("utf-8").replace("gene:", "") for key in keys]
        return json.dumps(gene_ids, indent=2), 200
    except Exception as e:
        logging.error("Error listing gene IDs: %s", e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/genes/<hgnc_id>", methods=["GET"])
def get_gene(hgnc_id: str):
    """Return detailed information for a specific gene."""
    try:
        key = "gene:" + hgnc_id
        gene_data = rd.get(key)
        if gene_data is None:
            return json.dumps({"error": f"No gene found with id {hgnc_id}"}, indent=2), 404
        return json.dumps(json.loads(gene_data), indent=2), 200
    except Exception as e:
        logging.error("Error retrieving gene %s: %s", hgnc_id, e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/jobs", methods=["POST"])
def create_job():
    """
    Create a new job to analyze the gene approval dates in a given range.
    Expects JSON with 'hgnc_id_start' and 'hgnc_id_end' (e.g., "HGNC:6", "HGNC:12345").
    """
    if not request.is_json:
        return json.dumps({"error": "Content-Type must be application/json"}, indent=2), 400

    job_params = request.get_json()
    if "hgnc_id_start" not in job_params or "hgnc_id_end" not in job_params:
        return json.dumps({"error": "Missing parameters. Required: hgnc_id_start, hgnc_id_end (format: HGNC:<number>)"}, indent=2), 400

    pattern = r"^HGNC:\d+$"
    start = job_params["hgnc_id_start"]
    end = job_params["hgnc_id_end"]

    if not (re.match(pattern, start) and re.match(pattern, end)):
        return json.dumps({"error": "Invalid HGNC ID format. Use HGNC:<number> (e.g., HGNC:5)."}, indent=2), 400

    try:
        job = add_job(start, end)
        return json.dumps(job, indent=2), 201
    except Exception as e:
        logging.error("Error submitting job: %s", e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/jobs", methods=["GET"])
def list_jobs():
    """Return a list of all submitted job IDs."""
    try:
        from jobs import jdb
        keys = jdb.keys("*")
        job_ids = [key.decode("utf-8") for key in keys]
        return json.dumps({"jobs": job_ids}, indent=2), 200
    except Exception as e:
        logging.error("Error listing jobs: %s", e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/jobs/<jid>", methods=["GET"])
def get_job_info(jid: str):
    """Return the status and information for a specific job."""
    try:
        job = get_job_by_id(jid)
        if not job:
            return json.dumps({"error": f"No job found with id {jid}"}, indent=2), 404
        return json.dumps(job, indent=2), 200
    except Exception as e:
        logging.error("Error retrieving job %s: %s", jid, e)
        return json.dumps({"error": str(e)}, indent=2), 500

@app.route("/results/<jid>", methods=["GET"])
def get_job_results(jid: str):
    """
    Return the analysis results for a completed job, which consist of a yearly breakdown of gene approval dates.
    If the job is not complete, it returns a message indicating so.
    """
    job = get_job_by_id(jid)
    if not job:
        return json.dumps({"error": f"No job found with id {jid}"}, indent=2), 404

    if job["status"] != "complete":
        return json.dumps({"message": "Job not complete yet. Please try again later."}, indent=2), 202

    results = get_results(jid)
    if not results:
        return json.dumps({"error": "No results found for this job."}, indent=2), 500

    try:
        return json.dumps(json.loads(results), indent=2), 200
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
