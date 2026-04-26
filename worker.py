from app.queue.queue_service import (
    dequeue_job,
    update_job_to_completed,
    update_job_to_failed,
    update_job_to_retry,
)
import time
from app.queue.queue_schema import JobRecord
import argparse
from worker_config import JOB_HANDLER, MAX_ATTEMPT
from app.core.exception import JobFailureException
from retry import is_retryable
from logger import log_event

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="worker-1")
args = parser.parse_args()

WORKER_NAME = args.name


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
        job_status = None

        if not response:
            time.sleep(10)
            continue

        start = time.perf_counter()
        try:
            job = JobRecord(**response)
            log_event(
                "job_started",
                job_id=str(job.job_id),
                job_type=job.job_type,
                worker_name=WORKER_NAME,
            )
            process_job(job)
            update_job_to_completed(job.job_id, job.attempt + 1)
            job_status = "job_completed"

        except JobFailureException as e:
            errors = e.errors
            if job and is_retryable(errors) and job.attempt < MAX_ATTEMPT:
                update_job_to_retry(job.job_id, errors, job.attempt + 1)
                log_event(
                    "job_retry",
                    job_id=str(job.job_id),
                    job_type=job.job_type,
                    worker_name=WORKER_NAME,
                    attempt=job.attempt + 1,
                    error_count=len(errors),
                    targets=[e["target"] for e in errors],
                    errors=errors  
                )
                job_status = "job_retry"

            elif job:
                update_job_to_failed(job.job_id, errors, job.attempt)
                log_event(
                    "job_failed",
                    job_id=str(job.job_id),
                    job_type=job.job_type,
                    worker_name=WORKER_NAME,
                    attempt=job.attempt,
                    error_count=len(errors),
                    targets=[e["target"] for e in errors],
                    errors=errors  
                )
                job_status = "job_failed"
            else:
                log_event(
                    "fatal error before job init",
                    worker_name=WORKER_NAME,
                    error=str(e),
                )
                job_status = "job_failed"

        except Exception as e:
            if job:
                update_job_to_failed(
                    job.job_id,
                    [
                        {
                            "target": job.job_type,
                            "error": str(e),
                            "type": type(e).__name__,
                            "retry": False,
                        }
                    ],
                    job.attempt + 1,
                )
            else:
                log_event(
                    "fatal error before job init",
                    worker_name=WORKER_NAME,
                    error=str(e),
                )
            job_status = "job_failed"
        finally:
            end = time.perf_counter()
            if job:
                log_event(
                    job_status,
                    job_id=str(job.job_id),
                    job_type=job.job_type,
                    worker_name=WORKER_NAME,
                    time_taken=round(end - start, 6),
                    attempt=job.attempt + 1,
                )


if __name__ == "__main__":
    run_worker()
