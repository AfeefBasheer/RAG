import traceback
from app.queue.queue_service import (
    dequeue_job,
    update_job_to_completed,
    update_job_to_failed,
)
from app.rag.service.ingestion_service import ingest_document
import time
from app.queue.queue_schema import JobRecord

JOB_HANDLER = {"ingestion": ingest_document}


def process_job(job_record):
    job_name = job_record.job_type
    job = JOB_HANDLER.get(job_name)
    if not job:
        print(f"no handler found for job type: {job_name}")
        return
    job(job_record.document_id, job_record.user_id, job_record.tenant_id)


def run_worker():
    while True:
        response = dequeue_job()
        job = None

        if not response:
            time.sleep(5)
            continue

        start = time.perf_counter()
        try:
            job = JobRecord(**response)
            print("job started - ", job.job_id)
            process_job(job)
            print("process_job completed")  # ← add this
            update_job_to_completed(job.job_id)
            job_status = "completed"

        except Exception as e:
            traceback.print_exc()
            if job:
                update_job_to_failed(job.job_id, str(e))
            job_status = "failed"
        finally:
            end = time.perf_counter()
            if job:
                print(
                    f"job {job.job_id} {job_status}. Time took {end - start:.6f} seconds"
                )


if __name__ == "__main__":
    run_worker()
