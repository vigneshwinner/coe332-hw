import requests
import xmltodict
import math
import logging
from datetime import datetime, timezone
from typing import List, Dict, Tuple

# Logging setup
logging.basicConfig(level=logging.INFO)

# NASA ISS data source
ISS_DATA_URL = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"

def fetch_iss_data(url: str = ISS_DATA_URL) -> str:
    """Fetches ISS trajectory data from NASA's website."""
    try:
        res = requests.get(url)
        res.raise_for_status()
        logging.info("Fetched ISS trajectory data successfully.")
        return res.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching ISS data: {e}")
        return ""

def parse_iss_data(xml_data: str) -> List[Dict]:
    """Parses XML data into a list of dictionaries with epoch, position, and velocity."""
    try:
        data = xmltodict.parse(xml_data)
        state_vectors = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
        iss_data = []

        for vec in state_vectors:
            # Extract numerical values correctly
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
    return math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)

def find_closest_epoch(data: List[Dict], now: datetime) -> Dict:
    """Finds the closest epoch to the current time."""
    return min(data, key=lambda d: (abs(d["epoch"] - now), d["epoch"]))

def compute_average_speed(data: List[Dict]) -> float:
    """Computes the average speed over all state vectors."""
    speeds = [compute_speed(entry["velocity"]) for entry in data]
    return sum(speeds) / len(speeds) if speeds else 0.0

def main():
    """Fetches ISS data, processes it, and prints useful information."""
    xml_data = fetch_iss_data()
    if not xml_data:
        logging.error("No data retrieved.")
        return

    iss_data = parse_iss_data(xml_data)
    if not iss_data:
        logging.error("Failed to parse ISS data")
        return

    # Print dataset range
    print(f"Data covers from {iss_data[0]['epoch']} to {iss_data[-1]['epoch']}")

    # Find closest epoch to "now"
    now = datetime.now(timezone.utc)
    closest = find_closest_epoch(iss_data, now)

    print(f"Closest epoch: {closest['epoch']}")
    print(f"Position: {closest['position']}")
    print(f"Velocity: {closest['velocity']}")
    print(f"Instantaneous Speed: {compute_speed(closest['velocity']):.2f} km/s")

    # Compute and display average speed
    avg_speed = compute_average_speed(iss_data)
    print(f"Average ISS Speed: {avg_speed:.2f} km/s")

if __name__ == "__main__":
    main()
