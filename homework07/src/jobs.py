import os
import json
import uuid
import redis
from hotqueue import HotQueue

# Read Redis settings from environment variables (with defaults)
_redis_ip = os.environ.get("REDIS_IP", "redis-db")
_redis_port = int(os.environ.get("REDIS_PORT", "6379"))

# Set up Redis connections:
rd = redis.Redis(host=_redis_ip, port=_redis_port, db=0)      # Main data
q = HotQueue("queue", host=_redis_ip, port=_redis_port, db=1)  # Task queue
jdb = redis.Redis(host=_redis_ip, port=_redis_port, db=2)       # Jobs database

def _generate_jid():
    """Generate a unique job identifier using UUID4."""
    return str(uuid.uuid4())

def _instantiate_job(jid, status, hgnc_id_start, hgnc_id_end):
    """Create a job dictionary using a range of HGNC Gene IDs."""
    return {
        "id": jid,
        "status": status,
        "hgnc_id_start": hgnc_id_start,
        "hgnc_id_end": hgnc_id_end
    }

def _save_job(jid, job_dict):
    """Save job in the Redis jobs database."""
    jdb.set(jid, json.dumps(job_dict))

def _queue_job(jid):
    """Push job ID onto the Redis queue."""
    q.put(jid)

def add_job(hgnc_id_start, hgnc_id_end, status="submitted"):
    """
    Add a job specifying the range of HGNC Gene IDs to process.
    Returns the created job dictionary.
    """
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, hgnc_id_start, hgnc_id_end)
    _save_job(jid, job_dict)
    _queue_job(jid)
    return job_dict

def get_job_by_id(jid):
    """Retrieve job information by job ID."""
    job_data = jdb.get(jid)
    if job_data:
        return json.loads(job_data)
    return None

def update_job_status(jid, status):
    """Update the status of given job."""
    job = get_job_by_id(jid)
    if job:
        job["status"] = status
        _save_job(jid, job)
    else:
        raise Exception(f"No job found with id {jid}")
