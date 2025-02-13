# Homework 2

Overview: 
This project provides an analysis of NASA's Meteorite Landings dataset, offering insights into meteorite mass, landing locations, and distances between impact sites. The goal is to apply data processing, geospatial calculations, and statistical analysis while ensuring proper logging, error handling, and unit testing.

Python Scripts:
* gcd_algorithm.py
    - Implements the great-circle distance formula to compute the shortest distance between two latitude/longitude points on Earth.
* ml_data_analysis.py
    - Reads and processes NASA's Meteorite Landings dataset.
    - Computes and prints:
        + Heaviest meteorite in the dataset.
        + Average latitude of all recorded landings.
        + Great-circle distance between a given location and meteorite sites.
    - Implements logging and error handling.
* test_gcd_algorithm.py
    - Contains unit tests for gcd_algorithm.py using pytest.
    - Validates correctness of distance calculations.
* test_ml_data_analysis.py
    - Contains unit tests for ml_data_analysis.py
    - Verifies correct statistical computations and proper error handling for invalid data.

Data:
- Use the following command to download meteorite_landings.csv into the directory: 
    * curl -o meteorite_landings.csv "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD"

Running the Code:
1. python3 ml_data_analysis.py
    - This logs information about the dataset.
    - It prints the heaviest meteorite and average latitude.
    - Computes the great-circle distance to a sample location.
2. pytest
    - Runs test cases for both meteorite analysis and great-circle calculations.
    - Verifies correct outputs and error handling.

Running the Code on Docker (build image yourself):
1. Navigate to Project Directory
2. Run: docker build -t vigneshwinner/homework03:1.0 ./
3. Test ml_data_analysis.py: docker run --rm -v "$(pwd)/meteorite_landings.csv:/code/meteorite_landings.csv" vigneshwinner/homework03 python /code/ml_data_analysis.py
4. Run the Unit Tests: docker run --rm -v "$(pwd)/meteorite_landings.csv:/code/meteorite_landings.csv" vigneshwinner/homework03 pytest /code
OR (pull directly from DockerHub):
docker pull vigneshwinner/homework03:1.0
