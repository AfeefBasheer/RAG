from app.queue.queue_repository import (
    create_job,
    fetch_job,
    update_job,
    get_job_by_job_id,
)
from uuid import UUID


def enqueue_ingestion_job(document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = create_job("ingestion", document_id, user_id, tenant_id)
    return response


def dequeue_job():
    response = fetch_job()
    return response


def update_job_to_completed(job_id: UUID,attempt_count:int):
    response = update_job("completed", job_id,None,attempt_count)
    return response


def update_job_to_failed(job_id: UUID, error_message: str,attempt_count:int):
    response = update_job("failed", job_id, error_message,attempt_count)
    return response


def get_job(job_id: UUID, user_id: UUID, tenant_id: UUID):
    response = get_job_by_job_id(job_id, user_id, tenant_id)
    return response

def update_job_to_retry(job_id:UUID,error_message:str,attempt_count:int):
    response = update_job("retry",job_id,error_message,attempt_count)
    return response

def enqueue_document_deletion_job(document_id:UUID,user_id:UUID,tenant_id:UUID):
    response = create_job('delete_document',document_id,user_id,tenant_id)
    return response