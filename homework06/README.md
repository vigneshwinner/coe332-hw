# Gene Data Analysis API

***Project Overview:*** 

This project is a Flask API that fetches, processes, and provides access to comprehensive human gene data from the HGNC (Human Gene Nomenclature Committee) complete dataset.  
It uses Redis for persistent data storage.  
The API performs the following functions:
1. **POST /data:** Fetches the HGNC JSON data from a remote source and loads it into Redis.
2. **GET /data:** Retrieves all gene records stored in Redis.
3. **DELETE /data:** Clears all gene data from Redis.
4. **GET /genes:** Returns a JSON-formatted list of all gene IDs (hgnc_id).
5. **GET /genes/<hgnc_id>:** Retrieves detailed information for a specific gene based on its hgnc_id.

***Python Scripts:***
* **gene_api.py**  
  - The main Flask API that:  
    + Fetches HGNC gene data from the provided JSON source  
    + Processes and loads the gene data into a Redis database  
    + Defines API endpoints for data insertion, retrieval, deletion, and specific gene queries

* **Dockerfile**  
  - Containerizes the Flask application

* **docker-compose.yaml**  
  - Orchestrates the Flask application container alongside a Redis container

* **requirements.txt**  
  - Lists all the required Python packages for the project

***Data:***

The gene data is sourced from the HGNC complete dataset provided by the Human Gene Nomenclature Committee.  
It is available in JSON format at:  
[https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json](https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json)

This dataset contains comprehensive and up-to-date information on human genes, including identifiers, gene symbols, names, chromosomal locations, and additional attributes.

***Deploying the App:*** 
1. **Navigate to the Project Directory.**
2. **Create and start docker containers (Flask & Redis):**
   ```bash
   docker-compose up --build -d
