from app.document.repository.admission import create_document,get_document_by_content_hash
from postgrest.exceptions import APIError
from app.document.input_normalizer.text import normalize_text
from app.core.hash import hash_text
from app.document.schema.document import DocumentRecord

async def insert_document(raw_document):
    try:    
        normalized_text = normalize_text(raw_document.text)
        content_hash = hash_text(normalized_text)
        document_record = DocumentRecord(
            document_id=raw_document.document_id,
            status=raw_document.status,
            source_type=raw_document.source_type,
            normalized_text=normalized_text,
            content_hash=content_hash,

        )
        response = create_document(document_record)
        return response
    except APIError as error:
        if error.code == "23505":
            response = get_document_by_content_hash(document_record.content_hash)
            if response.data.get('document_id') : return response
        
        raise