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
    - Fetches ISS trajectory data
    - Parses it
    - Finds and prints the closest epoch to the current time
    - Calculates and prints both instantaneous and average speeds
* test_iss_tracker.py
  - Contains unit tests for iss_tracker.py


Data:

The ISS trajectory data is publicly available from NASA’s Orbital Ephemeris Message (OEM) API:

https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml

This dataset contains 15 days of ISS position and velocity data and is constantly updated.


Running the Code:
* python3 iss_tracker.py
  - Fetches the latest Orbital Ephemeris Message (OEM) data for the ISS.
  - Parses and processes the dataset.
  - Finds the closest epoch (timestamp) to the current time.
  - Computes instantaneous speed at that moment.
  - Calculates average speed over the dataset.
  - Displays ISS position and velocity.
* pytest
  - Runs test cases for speed calculations, epoch selection, and data parsing.
  - Ensures correct outputs and error handling.


Running the Code on Docker (build image yourself):
1. Navigate to Project Directory
2. Create image: docker build -t vigneshwinner/homework04:1.0 ./
3. Test iss_tracker.py: docker run --rm vigneshwinner/homework04:1.0
4. Run the Unit Tests: docker run --rm vigneshwinner/homework04:1.0 pytest /code/test_iss_tracker.py

OR (pull directly from DockerHub): docker pull vigneshwinner/homework04:1.0
