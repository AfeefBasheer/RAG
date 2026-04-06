import traceback
from app.queue.queue_service import (
    dequeue_job,
    update_job_to_completed,
    update_job_to_failed,
    update_job_to_retry,
)
import time
import httpx
from app.queue.queue_schema import JobRecord
import argparse
from worker_config import JOB_HANDLER, MAX_ATTEMPT
from qdrant_client.http.exceptions import ResponseHandlingException

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="worker-1")
args = parser.parse_args()

WORKER_NAME = args.name


def is_retryable(error: Exception) -> bool:
    return isinstance(
        error,
        (
            httpx.WriteTimeout,
            httpx.ConnectTimeout,
            httpx.ReadTimeout,
            ResponseHandlingException,
        ),
    )


def process_job(job_record):
    job_name = job_record.job_type
    job = JOB_HANDLER.get(job_name)

    if not job:
        print(f"no handler found for job type: {job_name} by worker: {WORKER_NAME}")
        return
    job(job_record.document_id, job_record.user_id, job_record.tenant_id)


def run_worker():
    while True:
        response = None
        try:
            response = dequeue_job()
        except Exception as e:
            print(f"[{WORKER_NAME}] failed to dequeue: {e}, retrying in 10s")
            time.sleep(10)
            continue

        job = None
        job_status = "no status"

        if not response:
            time.sleep(10)
            continue

        start = time.perf_counter()
        try:
            job = JobRecord(**response)
            print(f"job.attempt = {job.attempt}")
            print(f"job started : {job.job_id} by worker: {WORKER_NAME}")
            process_job(job)
            update_job_to_completed(job.job_id, job.attempt+1)
            job_status = "completed"

        except Exception as e:
            traceback.print_exc()
            if job and is_retryable(e) and job.attempt < MAX_ATTEMPT:
                update_job_to_retry(job.job_id, job.attempt + 1, str(e))
                job_status = "retry"
            else:
                update_job_to_failed(job.job_id, str(e), job.attempt+1)
                job_status = "failed"
        finally:
            end = time.perf_counter()
            if job:
                print(
                    f"job {job.job_id} {job_status} by worker: {WORKER_NAME}. Time took {end - start:.6f} seconds"
                )


if __name__ == "__main__":
    run_worker()
