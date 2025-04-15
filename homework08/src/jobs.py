import os
import json
import uuid
import redis
from hotqueue import HotQueue

_redis_ip = os.environ.get("REDIS_IP", "redis-db")
_redis_port = int(os.environ.get("REDIS_PORT", "6379"))

rd = redis.Redis(host=_redis_ip, port=_redis_port, db=0) # Gene data
q = HotQueue("queue", host=_redis_ip, port=_redis_port, db=1) # Queue
jdb = redis.Redis(host=_redis_ip, port=_redis_port, db=2) # Jobs DB
rdb = redis.Redis(host=_redis_ip, port=_redis_port, db=3) # Results DB

def _generate_jid() -> str:
    """Generate a unique job ID using UUID4."""
    return str(uuid.uuid4())

def _instantiate_job(jid: str, status: str, hgnc_id_start: str, hgnc_id_end: str) -> dict:
    """
    Create the job object as a dictionary.
    The job records the range of HGNC IDs to process.
    """
    return {
        "id": jid,
        "status": status,
        "hgnc_id_start": hgnc_id_start,
        "hgnc_id_end": hgnc_id_end
    }

def _save_job(jid: str, job_dict: dict) -> None:
    """Save the job object to the jobs database (db=2)."""
    jdb.set(jid, json.dumps(job_dict))

def _queue_job(jid: str) -> None:
    """Place the job ID onto the task queue."""
    q.put(jid)

def add_job(hgnc_id_start: str, hgnc_id_end: str, status: str = "submitted") -> dict:
    """
    Add a new job specifying a range of HGNC Gene IDs.
    Returns the created job dictionary.
    """
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, hgnc_id_start, hgnc_id_end)
    _save_job(jid, job_dict)
    _queue_job(jid)
    return job_dict

def get_job_by_id(jid: str) -> dict:
    """Retrieve job details by job ID."""
    data = jdb.get(jid)
    if data:
        return json.loads(data)
    return None

def update_job_status(jid: str, status: str) -> None:
    """Update the job status for a given job ID."""
    job = get_job_by_id(jid)
    if job:
        job["status"] = status
        _save_job(jid, job)
    else:
        raise Exception(f"No job found with id {jid}")

def save_results(jid: str, results: str) -> None:
    """Save analysis results to Redis (db=3)."""
    rdb.set(jid, results)

def get_results(jid: str) -> str:
    """Retrieve analysis results for a job from Redis (db=3)."""
    data = rdb.get(jid)
    if data:
        return data.decode("utf-8")
    return None
