from qdrant_client.http.exceptions import ResponseHandlingException
import httpx


def is_retryable(errors: list) -> bool:
    for item in errors:
        if item.get("retry"):
            return True
    return False


def classify_error_type(error: Exception) -> bool:
    if isinstance(error, (httpx.TimeoutException,)):
        return True
    if isinstance(error, (httpx.ConnectError, ResponseHandlingException)):
        return True

    return False
