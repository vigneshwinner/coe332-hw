# Homework 5

***Project Overview:***

This project is a Flask API that fetches, processes, and analyzes real-time orbital data for the International Space Station (ISS).
The API ingests Orbital Ephemeris Message (OEM) XML data, parses it, and provides key insights through REST API endpoints, including:
1. All available timestamps (epochs) for the ISS position and velocity
2. Filtered timestamps (using **limit** and **offset**)
3. State vectors (position & velocity) for a specific timestamp
4. Instantaneous speed at a given epoch
5. ISS position, velocity, and speed for the closest epoch to "now"  


***Python Scripts:***
* iss_tracker.py
  - The main Flask API that:
    + Fetches ISS trajectory data
    + Parses and processes the dataset
    + Exposes Flask routes for querying ISS state vectors and speed
* test_iss_tracker.py
  - Contains unit tests for iss_tracker.py:
    + Speed calculations
    + Epoch selection logic
    + API responses  


***Data:***

The ISS trajectory data is publicly available from NASA’s Orbital Ephemeris Message (OEM) API:

https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml

This dataset contains 15 days of ISS position and velocity data and is constantly updated.  


***Running the Code Locally:***
* python3 iss_tracker.py
    - Starts the Flask web server on http://127.0.0.1:5000
    - Fetches the latest Orbital Ephemeris Message (OEM) data for the ISS
    - Parses and processes the dataset
    - Provides access to Flask API endpoints for querying ISS position, velocity, and speed
* pytest
  - Runs unit tests for speed calculations, epoch selection, data parsing, and API responses
  - Ensures correct outputs and error handling  
  

***Running the Code on Docker (build image yourself):***
1. Navigate to Project Directory
2. Create image: docker build -t vigneshwinner/homework05:1.0 ./
3. Run container: docker run -p 5000:5000 -v $(pwd):/app vigneshwinner/homework05:1.0

**OR (pull directly from DockerHub):**
1. docker pull vigneshwinner/homework05:latest
2. docker run -p 5000:5000 vigneshwinner/homework05:latest  


***Accessing the Flask API:***

Once the API is running, navigate to a new terminal and ssh into virtual machine. To access and test the endpoints:

* curl http://127.0.0.1:5000/epochs
    - Returns all available timestamps in the dataset
* curl "http://127.0.0.1:5000/epochs?limit=5&offset=2"
    - Filters epochs using **limit** and **offset** query parameters
* curl "http://127.0.0.1:5000/epochs/*specific epoch*"
    - Fetches ISS position and velocity for a specific epoch
* curl "http://127.0.0.1:5000/epochs/*specific epoch*/speed"
    - Computes the ISS speed at a specific epoch
* curl http://127.0.0.1:5000/now
    - Finds the closest timestamp to the current time and returns position, velocity, and speed
