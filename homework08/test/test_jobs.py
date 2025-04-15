import pytest
import json
from jobs import add_job, get_job_by_id, save_results, get_results

def test_add_job_and_retrieve():
    job = add_job("HGNC:6", "HGNC:12345")
    assert "id" in job
    jid = job["id"]
    retrieved = get_job_by_id(jid)
    assert retrieved is not None
    assert retrieved["id"] == jid

def test_save_and_get_results():
    test_id = "test-job-123"
    sample_results = {
        "total_genes": 10,
        "earliest_date": "1/1/1986",
        "latest_date": "12/31/2020",
        "yearly_breakdown": {"1986": 2, "2020": 8}
    }
    results_str = json.dumps(sample_results)
    save_results(test_id, results_str)
    ret = get_results(test_id)
    assert ret is not None
    assert json.loads(ret) == sample_results
