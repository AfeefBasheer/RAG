from app.document.repository.admission import create_document,get_document_by_content_hash
from postgrest.exceptions import APIError

async def insert_document(document):
    try:
        return create_document(document)
    except APIError as error:
        if error.code == "23505":
            response = get_document_by_content_hash(document.content_hash)
            if response.data.get('document_id') : return response
        
        raise