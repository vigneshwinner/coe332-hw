from flask import Flask, request
import requests
import xmltodict
import math
import logging
from datetime import datetime, timezone
from typing import List, Dict, Tuple

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# NASA ISS data source
ISS_DATA_URL = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"


def fetch_iss_data(url: str = ISS_DATA_URL) -> str:
    """Fetches ISS trajectory data from NASA's public data source."""
    try:
        res = requests.get(url)
        res.raise_for_status()
        logging.info("Fetched ISS trajectory data successfully.")
        return res.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching ISS data: {e}")
        return ""
      
  
def parse_iss_data(xml_data: str) -> List[Dict[str, object]]:
    """Parses XML data into a list of dictionaries with epoch, position, and velocity."""
    try:
        data = xmltodict.parse(xml_data)
        state_vectors = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
        iss_data = []

        for vec in state_vectors:
            iss_data.append({
                "epoch": datetime.strptime(vec["EPOCH"], "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
                "position": (float(vec["X"]["#text"]), float(vec["Y"]["#text"]), float(vec["Z"]["#text"])),
                "velocity": (float(vec["X_DOT"]["#text"]), float(vec["Y_DOT"]["#text"]), float(vec["Z_DOT"]["#text"]))
            })

        logging.info(f"Parsed {len(iss_data)} state vectors.")
        return iss_data

    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"Error parsing XML: {e}")
        return []


def compute_speed(velocity: Tuple[float, float, float]) -> float:
    """Calculates speed from a velocity vector (km/s)."""
    return math.sqrt(velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2)


def find_closest_epoch(data: List[Dict], now: datetime) -> Dict:
    """Finds the closest epoch to the current time."""
    return min(data, key=lambda d: (abs(d["epoch"] - now), d["epoch"]))


def compute_average_speed(data: List[Dict]) -> float:
    """Computes the average speed over all state vectors."""
    speeds = [compute_speed(entry["velocity"]) for entry in data]
    return sum(speeds) / len(speeds) if speeds else 0.0


# Load ISS data on startup
xml_data = fetch_iss_data()
iss_data = parse_iss_data(xml_data) if xml_data else []


@app.route("/epochs", methods=["GET"])
def get_epochs() -> str:
    """Returns all epochs or a subset using optional `limit` and `offset` query parameters."""
    limit = request.args.get("limit", default=None, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if not iss_data:
        return "No data available", 500

    subset = iss_data[offset:offset + limit] if limit else iss_data[offset:]
    return "\n".join([entry["epoch"].isoformat() for entry in subset]) + "\n"


@app.route("/epochs/<epoch>", methods=["GET"])
def get_epoch(epoch: str) -> str:
    """Returns the state vectors for a specific epoch."""
    for entry in iss_data:
        if entry["epoch"].isoformat() == epoch:
            return f"Epoch: {entry['epoch'].isoformat()}\nPosition: {entry['position']}\nVelocity: {entry['velocity']}\n"
    return "Epoch not found", 404


@app.route("/epochs/<epoch>/speed", methods=["GET"])
def get_epoch_speed(epoch: str) -> str:
    """Returns the instantaneous speed at a specific epoch."""
    for entry in iss_data:
        if entry["epoch"].isoformat() == epoch:
            speed = compute_speed(entry["velocity"])
            return f"Epoch: {epoch}\nSpeed: {speed:.2f} km/s\n"
    return "Epoch not found", 404


@app.route("/now", methods=["GET"])
def get_now() -> str:
    """Returns the state vectors and speed for the epoch closest to the current time."""
    if not iss_data:
        return "No data available", 500

    now = datetime.now(timezone.utc)
    closest = find_closest_epoch(iss_data, now)

    if not closest:
        return "No data available", 500

    avg_speed = compute_average_speed(iss_data)

    return (
        f"Closest Epoch: {closest['epoch'].isoformat()}\n"
        f"Position: {closest['position']}\n"
        f"Velocity: {closest['velocity']}\n"
        f"Instananeous Speed: {compute_speed(closest['velocity']):.2f} km/s\n"
        f"Average ISS Speed: {avg_speed:.2f} km/s\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
