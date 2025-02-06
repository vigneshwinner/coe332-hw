import csv
import logging
import argparse
from gcd_algorithm import great_circle_distance

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def read_csv(file_path: str) -> list[dict]:
    """
    Reads a CSV file and returns a list of dictionaries.

    Args:
        file_path (str): Path to CSV file.

    Returns:
        list[dict]: List of meteorite landing data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    except FileNotFoundError:
        logging.error("CSV file not found.")
        return []
    except Exception as e:
        logging.error(f"Unexpected error reading file: {e}")
        return []

def heaviest_meteorite(landings: list[dict]) -> dict:
    """
    Finds the heaviest meteorite from the dataset.

    Args:
        landings (list[dict]): Meteorite landing records.

    Returns:
        dict: The meteorite with the highest mass.
    """
    try:
        return max(landings, key=lambda x: float(x['mass (g)']) if x['mass (g)'] else 0)
    except ValueError:
        logging.error("Invalid data in 'mass (g)' field.")
        return {}

def calculate_avg_latitude(landings: list[dict]) -> float:
    """
    Computes the average latitude of meteorite landings.

    Args:
        landings (list[dict]): Meteorite landing records.

    Returns:
        float: Average latitude.
    """
    latitudes = [float(m['reclat']) for m in landings if m.get('reclat')]
    return sum(latitudes) / len(latitudes) if latitudes else 0.0

def main():
    parser = argparse.ArgumentParser(description="Analyze NASA Meteorite Landings data.")
    parser.add_argument("csv_file", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    data = read_csv(args.csv_file)

    if data:
        logging.info(f"Heaviest Meteorite: {heaviest_meteorite(data)}")
        logging.info(f"Average Latitude: {calculate_avg_latitude(data)}")
        logging.info(f"Nearest Meteorite to (0, 0): {great_circle_distance(0, 0, 40, -75)}")

if __name__ == '__main__':
    main()


