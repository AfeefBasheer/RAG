from app.queue.queue_service import (
    update_job_to_completed,
    update_job_to_failed,
    update_job_to_retry,
)

import asyncio
from app.queue.queue_schema import JobRecord
from app.core.exception import JobFailureException
from worker.retry import is_retryable
from logger import log_event
from app.database.postgres import pool


async def process_job(job_record, JOB_HANDLER, WORKER_NAME):
    job_name = job_record.job_type
    job = JOB_HANDLER.get(job_name)

    if not job:
        print(f"no handler found for job type: {job_name} by worker: {WORKER_NAME}")
        raise Exception(f"No handler for job type: {job_name}")

    await job(job_record)


async def run_worker_loop(WORKER_NAME, JOB_HANDLER, fetch_next_job, MAX_ATTEMPT):
    while True:
        response = None
        try:
            await pool.open()
            response = await fetch_next_job()
        except Exception as e:
            print(f"[{WORKER_NAME}] failed to dequeue: {e}, retrying in 3s")
            await asyncio.sleep(3)
            continue

        job = None
        job_status = "unknown_failure"
        errors = None

        if not response:
            await asyncio.sleep(3)
            continue

        start = asyncio.get_running_loop().time()
        try:
            job = JobRecord(**response)
            log_event(
                "job_started",
                job_id=str(job.job_id),
                job_type=job.job_type,
                worker_name=WORKER_NAME,
            )
            print("job started", job.job_id, job.job_type, WORKER_NAME)
            await process_job(job, JOB_HANDLER, WORKER_NAME)
            await update_job_to_completed(job.job_id, job.attempt + 1)
            job_status = "job_completed"

        except JobFailureException as e:
            errors = e.errors
            print(f"[{WORKER_NAME}] job failed: {errors}, job_id: {job.job_id}")
            if job and is_retryable(errors) and job.attempt < MAX_ATTEMPT:
                try:
                    await update_job_to_retry(job.job_id, errors, job.attempt + 1)
                    job_status = "job_retry"
                except Exception as e:
                    print(
                        f"[{WORKER_NAME}] CRITICAL: failed to update retry state: {e}"
                    )
                    log_event(
                        "job_status_update_to_retry_failed",
                        job_id=str(job.job_id),
                        job_type=job.job_type,
                        worker_name=WORKER_NAME,
                    )

            elif job:
                try:
                    await update_job_to_failed(job.job_id, errors, job.attempt)
                    job_status = "job_failed"
                except Exception as e:
                    print(
                        f"[{WORKER_NAME}] CRITICAL: failed to update retry state: {e}"
                    )
                    log_event(
                        "job_status_update_to_fail_failed",
                        job_id=str(job.job_id),
                        job_type=job.job_type,
                        worker_name=WORKER_NAME,
                    )

            else:
                job_status = "job_failed"

        except Exception as e:
            print(f"[{WORKER_NAME}] job failed: {errors}, job_id: {job.job_id}")
            if job:
                try:
                    await update_job_to_failed(
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
                except Exception as e:
                    print(f"[{WORKER_NAME}] CRITICAL: failed to mark job failed: {e}")
                    log_event(
                        "job_status_update_to_fail_failed",
                        job_id=str(job.job_id),
                        job_type=job.job_type,
                        worker_name=WORKER_NAME,
                    )
            job_status = "job_failed"
        finally:
            end = asyncio.get_running_loop().time()
            if job:
                log_event(
                    job_status,
                    job_id=str(job.job_id),
                    job_type=job.job_type,
                    worker_name=WORKER_NAME,
                    time_taken=round(end - start, 6),
                    attempt=job.attempt + 1,
                    errors=errors,
                )
                print("job ended", job.job_id, job.job_type, job_status, WORKER_NAME)
