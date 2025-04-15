# Homework 07: Gene Data Jobs and Messaging API 

***Project Overview:***                                                                                                                                           

This project is a Flask API that fetches, processes, and provides access to comprehensive human gene data from the HGNC (Human Gene Nomenclature Committee) complete dataset. It incorporates asynchronous job processing to handle long-running tasks and uses Redis for persistent data storage.
The API supports the following functionalities:
1. Fetches the HGNC JSON data from a remote source and loads it into Redis
2. Retrieves all gene records stored in Redis
3. Clears all gene data from Redis
4. Returns a JSON-formatted list of all gene IDs (hgnc_id)
5. Retrieves detailed information for a specific gene based on its hgnc_id
6. Accepts job requests in JSON format to process a specified range of gene IDs
7. Provides an endpoint to list all submitted job IDs stored in the jobs database 
8. Allows retrieval of detailed information and current processing status for a specific job using its unique job ID
9. Uses a dedicated worker service that listens on a Redis-backed queue, picks up submitted jobs, simulates processing, and updates the job status accordingly


***Python Scripts:***
* ```src/api.py```
  - The main Flask API that:
    + Loads gene data from the HGNC dataset into Redis
    + Retrieves and deletes gene records
    + Submits and views jobs via the Jobs API
* ```src/jobs.py```
  - Contains core functionality for job management
  - Does the following tasks:
    + Generates unique job IDs
    + Validates job input
    + Stores job data in Redis
    + Pushes job IDs onto the Redis queue
* ```src/worker.py```
  - Worker script that continuously listens to the Redis queue
  - For every job it retrieves, it simulates work by updating the job status from "submitted" to "in progress" to "complete" after a delay


***Data:***

The gene data is sourced from the HGNC complete dataset provided by the Human Gene Nomenclature Committee.

It is available in JSON and TSV formats at:

[https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json](https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json)

[https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt](https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt)
                                                                                                                                                            
This dataset contains comprehensive and up-to-date information on human genes, including:
* **hgnc_id:** A unique identifier assigned by HGNC
* **symbol:** The official gene symbol
* **name:** The full gene name
* **location:** Chromosomal location data
* **Other Attributes:** Additional identifiers (e.g., Ensembl ID, RefSeq accession), gene groupings, status, etc.


***Deploying the App:***
1. Navigate to the Project Directory
2. Create and start docker containers (Flask & Redis):
   ```docker-compose up --build -d```
   - The Flask API will run locally at http://localhost:5000

**OR (pull directly from DockerHub):**
1. ```docker pull vigneshwinner/gene_api:1.0```
2. ```docker run -p 5000:5000 vigneshwinner/gene_api:1.0```


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
  - Example Output:
    + ```["5", "37133", "24086", "7", ...]```
* ```curl http://127.0.0.1:5000/genes/<hgnc_id>```
  - Retrieves detailed gene data for a specific gene
  - Example Output:
    + ```{"hgnc_id": "HGNC:5", "symbol": "A1BG", "name": "alpha-1-B glycoprotein", "location": "19q13.43", ...}```
* ```curl localhost:5000/jobs -X POST -d '{"hgnc_id_start": "<hgnc_id>", "hgnc_id_end": "<hgnc_id>"}' -H "Content-Type: application/json"```
  - Submits a job that will process a range of gene IDs
* ```curl localhost:5000/jobs```
  - Returns a list of job IDs
  - Example Output:
    + ```{"jobs": ["a1b2c3d4-5e6f-7g8h-9i10-jk11lm12no13", "<another-job-id>", ...]}```
* ```curl localhost:5000/jobs/<job_id>```
  - Returns job details for a specific job
  - Example Output:
    + ```{"id": "a1b2c3d4-5e6f-7g8h-9i10-jk11lm12no13", "status": "complete", "hgnc_id_start": "HGNC:5", "hgnc_id_end": "HGNC:10000"}```
