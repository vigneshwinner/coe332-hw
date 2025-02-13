#!/usr/bin/env python3
import csv
import os
import sys
import logging
from gcd_algorithm import great_circle_distance

logging.basicConfig(level=logging.DEBUG)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(SCRIPT_DIR, "meteorite_landings.csv")

def load_data(filename: str) -> list:
    """
    Load meteorite landing data from a CSV file.

    Parameters:
    filename: CSV file containing meteorite landing data

    Returns:
    List of dictionaries with meteorite data
    """
    try:
        with open(filename, newline='') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        logging.info("Successfully loaded CSV data.")
        return data
    except FileNotFoundError:
        logging.error("File not found.")
        return []
    except csv.Error:
        logging.error("Error parsing CSV file.")
        return []

def heaviest_meteorite(data: list) -> dict:
    """
    Find the heaviest meteorite in the dataset.

    Parameters:
    data: List of meteorite dictionaries

    Returns:
    Dictionary containing the heaviest meteorite's details
    """
    heaviest = None
    max_mass = 0
      for item in data:
        try:
            mass = float(item["mass (g)"]) if item["mass (g)"] else 0
            if mass > max_mass:
                max_mass = mass
                heaviest = item
        except ValueError:
            logging.warning(f"Invalid mass value found: {item['mass (g)']}")

    return heaviest

def calculate_avg_latitude(data: list) -> float:
    """
    Compute the average latitude of meteorite landings.

    Parameters:
    data: List of meteorite dictionaries

    Returns:
    Average latitude value
    """
    total_lat = 0
    count = 0
    for item in data:
        try:
            lat = float(item["reclat"]) if item["reclat"] else 0
            total_lat += lat
            count += 1
        except ValueError:
            logging.warning(f"Invalid latitude value found: {item['reclat']}")

    return total_lat / count if count else 0

def main():
    """
    Main function to load data, find the heaviest meteorite,
    calculate the average latitude, and print the results.
    """
    data = load_data(filename)

    if not data:
        print("No data available.")
        returnheaviest = heaviest_meteorite(data)
    avg_latitude = calculate_avg_latitude(data)

    if heaviest:
        print("\nHeaviest Meteorite:")
        print(f"Name: {heaviest.get('name', 'Unknown')}")
        print(f"Mass (g): {heaviest.get('mass (g)', 'Unknown')}")
        print(f"Latitude: {heaviest.get('reclat', 'Unknown')}")
        print(f"Longitude: {heaviest.get('reclong', 'Unknown')}")
    else:
        print("\nNo valid meteorite data found.")

    print(f"\nAverage Latitude of Meteorite Landings: {avg_latitude:.2f}")

if __name__ == "__main__":
    main()
