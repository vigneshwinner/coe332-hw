# Homework 06: Gene Data API

***Project Overview:*** 

This project is a Flask API that fetches, processes, and provides access to comprehensive human gene data from the HGNC (Human Gene Nomenclature Committee) complete dataset. It uses Redis for persistent data storage.  
The API performs the following functions:
1. Fetches the HGNC JSON data from a remote source and loads it into Redis
2. Retrieves all gene records stored in Redis
3. Clears all gene data from Redis
4. Returns a JSON-formatted list of all gene IDs (hgnc_id)
5. Retrieves detailed information for a specific gene based on its hgnc_id

***Python Scripts:***
* ```gene_api.py```  
  - The main Flask API that:  
    + Fetches gene data from the HGNC's complete dataset (JSON)
    + Processes and loads the gene data into a Redis database
    + Defines API endpoints for data insertion, retrieval, deletion, and specific gene queries

***Data:***

The gene data is sourced from the HGNC complete dataset provided by the Human Gene Nomenclature Committee.  

It is available in JSON and TSV formats at:  
[https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json](https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json)

[https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt](https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt)

This dataset contains comprehensive and up-to-date information on human genes, including identifiers, gene symbols, names, chromosomal locations, and additional attributes.

***Deploying the App:*** 
1. Navigate to the Project Directory
2. Create and start docker containers (Flask & Redis):
   ```docker-compose up --build -d```
   - The Flask API will run locally at http://localhost:5000

**OR (pull directly from DockerHub):** 
1. ```docker pull vigneshwinner/gene_data:1.0```
2. ```docker run -p 5000:5000 vigneshwinner/gene_data:1.0```


***Accessing the Flask API:***

Once the API is running, to access and test the endpoints:

* ```curl -X POST http://127.0.0.1:5000/data```
  - Loads the HGNC gene data into Redis
* ```curl http://127.0.0.1:5000/data```
  - Retrieves all the gene records stored in Redis
* ```curl -X DELETE http://127.0.0.1:5000/data```
  - Clears all gene data from Redis
* ```curl http://127.0.0.1:5000/genes```
  - Returns a list of all gene IDs (hgnc_id)
* ```curl http://127.0.0.1:5000/genes/<hgnc_id>```
  - Retrieves detailed gene data for a specific gene
 
***Using AI***

ChatGPT was used to generate the following line in ```docker-compose.yaml```:

```command: ["redis-server", "--save", "1", "1", "--stop-writes-on-bgsave-error", "no" ]```
