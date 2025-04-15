import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_data_post():
    response = requests.post(f"{BASE_URL}/data")
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "Loaded" in data["message"]

def test_data_get():
    response = requests.get(f"{BASE_URL}/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_data_delete():
    response = requests.delete(f"{BASE_URL}/data")
    assert response.status_code == 200
    data = response.json()
    assert "Deleted" in data

def test_genes_list():
    response = requests.get(f"{BASE_URL}/genes")
    assert response.status_code == 200
    gene_ids = response.json()
    assert isinstance(gene_ids, list)

def test_get_specific_gene():
    response = requests.get(f"{BASE_URL}/genes/HGNC:5")
    if response.status_code == 200:
        gene = response.json()
        assert isinstance(gene, dict)
        assert gene.get("hgnc_id") == "HGNC:5"
    else:
        assert response.status_code == 404

def test_create_job():
    payload = {"hgnc_id_start": "HGNC:6", "hgnc_id_end": "HGNC:12345"}
    response = requests.post(f"{BASE_URL}/jobs", json=payload)
    assert response.status_code == 201
    job = response.json()
    assert "id" in job
    assert job["status"] == "submitted"
    assert job["hgnc_id_start"] == "HGNC:6"
    assert job["hgnc_id_end"] == "HGNC:12345"
    assert isinstance(job["id"], str) and len(job["id"]) > 0

def test_list_jobs():
    response = requests.get(f"{BASE_URL}/jobs")
    assert response.status_code == 200
    jobs_data = response.json()
    assert "jobs" in jobs_data
    assert isinstance(jobs_data["jobs"], list)

def test_get_invalid_job():
    response = requests.get(f"{BASE_URL}/jobs/invalid-job-id")
    assert response.status_code == 404

def test_get_results_pending():
    payload = {"hgnc_id_start": "HGNC:6", "hgnc_id_end": "HGNC:12345"}
    job_response = requests.post(f"{BASE_URL}/jobs", json=payload)
    job = job_response.json()
    job_id = job["id"]
    results_response = requests.get(f"{BASE_URL}/results/{job_id}")
    assert results_response.status_code in (202, 200)
