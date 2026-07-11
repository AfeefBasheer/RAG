from app.queue.queue_repository import (
    create_job,
    fetch_embed_job,
    fetch_general_job,
    update_job,
    get_job_by_job_id,
)
from uuid import UUID


async def enqueue_chunk_job(document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = await create_job("chunk_document", document_id, user_id, tenant_id)
    return response


async def enqueue_embed_job(document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = await create_job("embed_document", document_id, user_id, tenant_id)
    return response


async def dequeue_embed_job():
    response = await fetch_embed_job()
    return response

async def dequeue_general_job():
    response = await fetch_general_job()
    return response


async def update_job_to_completed(job_id: UUID, attempt_count: int):
    response = await update_job("completed", job_id, None, attempt_count)
    return response


async def update_job_to_failed(job_id: UUID, errors: list, attempt_count: int):
    response = await update_job("failed", job_id, errors, attempt_count)
    return response


async def get_job(job_id: UUID, user_id: UUID, tenant_id: UUID):
    response = await get_job_by_job_id(job_id, user_id, tenant_id)
    return response


async def update_job_to_retry(job_id: UUID, errors: list, attempt_count: int):
    response = await update_job("retry", job_id, errors, attempt_count)
    return response


async def enqueue_document_deletion_job(document_id: UUID, user_id: UUID, tenant_id: UUID):
    response = await create_job("delete_document", document_id, user_id, tenant_id)
    return response
