from app.queue.queue_repository import create_job,fetch_job,update_job
from uuid import UUID

def enqueue_ingestion_job(document_id:UUID,user_id:UUID,tenant_id:UUID):
    response = create_job("ingestion",document_id,user_id,tenant_id)
    return response

def dequeue_job():
    response = fetch_job()
    return response

def update_job_to_completed(job_id:UUID):
    response = update_job('completed',job_id)
    return response

def update_job_to_failed(job_id:UUID,error_message:str):
    response = update_job('failed',job_id,error_message)
    return response
