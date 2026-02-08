from app.core.uuid import generate_uuid
from app.document.input_normalizer.text import normalize_text
from app.core.hash import hash_text
from app.document.schema.document import DocumentRecord
from app.document.persistance.admission import insert_document


async def admit_text(document) -> dict:
    document_id = generate_uuid()
    normalized_text = normalize_text(document.text)
    content_hash = hash_text(normalized_text)

    document_record = DocumentRecord(
        document_id=document_id,
        text=normalized_text,
        content_hash=content_hash,
        status="admitted",
    )

    response = await insert_document(document_record)
    return response
