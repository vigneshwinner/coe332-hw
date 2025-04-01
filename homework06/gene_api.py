from flask import Flask, request
import requests
import redis
import json
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# HGNC Data source URL (JSON format)
DATA_URL = "https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json"

def get_redis_client():
    return redis.Redis(host="redis-db", port=6379, db=0)

rd = get_redis_client()


def fetch_hgnc_data(url=DATA_URL):
    """
    Fetches HGNC gene data from the dataset.
    Returns a list of gene objects (dictionaries) or an empty list on failure.
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        logging.info("Fetched data of type: %s", type(data))
        # If the data is a dict with a 'response' key that contains 'docs', extract it.
        if isinstance(data, dict):
            if "response" in data and "docs" in data["response"]:
                data = data["response"]["docs"]
                logging.info("Extracted %d gene entries from data['response']['docs'].", len(data))
            else:
                # Fallback: convert dict values to a list
                data = list(data.values())
                logging.info("Converted dict to list with %d items.", len(data))
        # Log type of first element if available
        if isinstance(data, list) and data:
            logging.info("Type of first element: %s", type(data[0]))
        return data
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching HGNC data: %s", e)
        return []

def load_data_to_redis(data):
    """
    Loads gene data into Redis.
    """
    count = 0
    for gene in data:
        # Ensure the item is a dictionary
        if isinstance(gene, dict):
            hgnc_id = gene.get("hgnc_id")
            if hgnc_id:
                key = "gene:" + hgnc_id
                try:
                    rd.set(key, json.dumps(gene))
                    count += 1
                except redis.exceptions.ResponseError as re:
                    logging.error("Redis ResponseError for key %s: %s", key, re)
            else:
                logging.warning("Skipping gene without 'hgnc_id': %s", gene)
        else:
            logging.warning("Skipping non-dictionary item: %s", gene)
    logging.info("Loaded %d genes into Redis.", count)
    return count

@app.route("/data", methods=["POST"])
def post_data():
    """
    Fetches HGNC data and loads it into Redis.
    """
    data = fetch_hgnc_data()
    count = load_data_to_redis(data)
    response = "Loaded {} genes into Redis".format(count)
    return json.dumps(response), 201

@app.route("/data", methods=["GET"])
def get_data():
    """
    Retrieves all gene data from Redis and returns it as a JSON list.
    """
    try:
        keys = rd.keys("gene:*")
        genes = []
        for key in keys:
            gene_data = rd.get(key)
            if gene_data:
                genes.append(json.loads(gene_data))
        return json.dumps(genes), 200
    except Exception as e:
        logging.error("Error retrieving gene data: %s", e)
        response = {"error": str(e)}
        return json.dumps(response), 500

@app.route("/data", methods=["DELETE"])
def delete_data():
    """
    Deletes all gene data from Redis.
    """
    try:
        keys = rd.keys("gene:*")
        if keys:
            rd.delete(*keys)
        response = "Deleted gene data from Redis"
        return json.dumps(response), 200
    except Exception as e:
        logging.error("Error deleting gene data: %s", e)
        response = {"error": str(e)}
        return json.dumps(response), 500

@app.route("/genes", methods=["GET"])
def list_genes():
    """
    Returns a JSON-formatted list of all hgnc_id values stored in Redis.
    """
    try:
        keys = rd.keys("gene:*")
        gene_ids = [key.decode("utf-8").replace("gene:", "") for key in keys]
        return json.dumps(gene_ids), 200
    except Exception as e:
        logging.error("Error listing gene IDs: %s", e)
        response = {"error": str(e)}
        return json.dumps(response), 500

@app.route("/genes/<hgnc_id>", methods=["GET"])
def get_gene(hgnc_id):
    """
    Retrieves detailed gene data for the specified hgnc_id from Redis.
    """
    try:
        key = "gene:" + hgnc_id
        gene_data = rd.get(key)
        if gene_data is None:
            response = {"error": "No gene found with id {}".format(hgnc_id)}
            return json.dumps(response, indent=2), 404
        gene = json.loads(gene_data)
        return json.dumps(gene, indent=2), 200
    except Exception as e:
        logging.error("Error retrieving gene %s: %s", hgnc_id, e)
        response = {"error": str(e)}
        return json.dumps(response, indent=2), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
