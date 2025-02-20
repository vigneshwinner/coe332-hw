# Homework 4

Project Overview: 

This project that fetches, processes, and analyzes real-time orbital data for the International Space Station (ISS).
It ingests Orbital Ephemeris Message (OEM) XML data, parses it, and provides key insights, including:
1. ISS position and velocity at the closest timestamp to "now"
2. Instantaneous speed at that moment
3. Average speed over the entire dataset


Python Scripts:
* iss_tracker.py
  + The main script that: 
    - fetches ISS trajectory data
    - parses it
    - finds and prints the closest epoch to the current time
    - calculates and prints both instantaneous and average speeds
* test_iss_tracker.py
  - Contains unit tests for iss_tracker.py


Data:

The ISS trajectory data is publicly available from NASA’s Orbital Ephemeris Message (OEM) API:

https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml

This dataset contains 15 days of ISS position and velocity data and is constantly updated.


Running the Code:
* python3 iss_tracker.py
  - Fetch the latest Orbital Ephemeris Message (OEM) data for the ISS.
  - Parse and process the dataset.
  - Find the closest epoch (timestamp) to the current time.
  - Compute instantaneous speed at that moment.
  - Calculate average speed over the dataset.
  - Display ISS position and velocity.
* pytest
  - Runs test cases for speed calculations, epoch selection, and data parsing.
  - Ensures correct outputs and error handling.


Running the Code on Docker (build image yourself):
1. Navigate to Project Directory
2. Run: docker build -t vigneshwinner/homework04:1.0 ./
3. Run: docker run --rm vigneshwinner/homework04:1.0
4. Run the Unit Tests: docker run --rm vigneshwinner/homework04:1.0 pytest /code/test_iss_tracker.py

OR (pull directly from DockerHub): docker pull vigneshwinner/homework04:1.0
