from app.core.uuid import generate_uuid

from app.document.schema.document import RawDocument
from app.document.persistance.admission import insert_document


async def admit_text(document) -> dict:
    document_id = generate_uuid()

    document_record = RawDocument(
        document_id=document_id,
        source_type="text",
        status="admitted",
    )

    response = await insert_document(document_record)
    return response
